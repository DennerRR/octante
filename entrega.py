"""Domínio de desempenho Entrega (PMBOK 7, seção 2.6) e planejamento do escopo (2.4.2.1).

Backlog / escopo decomposto, critérios de aceite, definição de pronto, aceite
das entregas, linha de base do escopo, custo da qualidade e benefícios.
"""
import json
from datetime import date, timedelta

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

import pmbok
from db import get_db
from util import decimal, inteiro, moeda, obter_projeto, tocar_projeto

bp = Blueprint("entrega", __name__, url_prefix="/p/<int:projeto_id>/entrega")

DIAS_AGUARDANDO_ACEITE = 14
JANELA_FLUXO_DIAS = 30
MUDANCA_APROVADA = ("aprovada", "implementada")


# --------------------------------------------------------------------------
# Consultas e regras
# --------------------------------------------------------------------------
def enriquecer_item(row):
    i = dict(row)
    i["rotulo"] = f"I-{i['codigo']}"
    checks = {
        "claro": bool(i["q_claro"]),
        "conciso": bool(i["q_conciso"]),
        "verificavel": bool((i["criterios_aceite"] or "").strip()),
        "consistente": bool(i["q_consistente"]),
        "rastreavel": True,
    }
    i["qualidade"] = checks
    i["qualidade_n"] = sum(checks.values())
    i["bem_documentado"] = all(checks.values())
    i["feito"] = i["status"] in ("concluido", "aceito")
    hoje = date.today()
    i["dias_em_andamento"] = None
    if i["status"] == "em_andamento" and i["iniciado_em"]:
        i["dias_em_andamento"] = (hoje - date.fromisoformat(i["iniciado_em"][:10])).days
    i["dias_aguardando_aceite"] = None
    if i["status"] == "concluido" and i["concluido_em"]:
        i["dias_aguardando_aceite"] = (hoje - date.fromisoformat(i["concluido_em"][:10])).days
    return i


def listar_itens(projeto_id):
    """Itens em ordem de árvore (pai antes dos filhos), com nível, folha e progresso dos filhos."""
    rows = get_db().execute(
        """SELECT i.*, s.nome AS parte_nome, m.codigo AS mudanca_codigo, m.status AS mudanca_status,
                  r.codigo AS risco_codigo
           FROM item i
           LEFT JOIN parte_interessada s ON s.id = i.parte_id
           LEFT JOIN mudanca m ON m.id = i.mudanca_id
           LEFT JOIN risco r ON r.id = i.risco_id
           WHERE i.projeto_id = ?""", (projeto_id,)
    ).fetchall()
    itens = [enriquecer_item(r) for r in rows]
    ids = {i["id"] for i in itens}
    por_pai = {}
    for i in itens:
        por_pai.setdefault(i["pai_id"] if i["pai_id"] in ids else None, []).append(i)

    def chave(i):
        return (i["ordem"] if i["ordem"] is not None else 10**9, i["codigo"])

    ordenados, vistos = [], set()

    def visitar(pai, nivel):
        feitas = total = 0
        for i in sorted(por_pai.get(pai, []), key=chave):
            if i["id"] in vistos:
                continue
            vistos.add(i["id"])
            i["nivel"] = nivel
            ordenados.append(i)
            f, t = visitar(i["id"], nivel + 1)
            i["folha"] = t == 0 and not por_pai.get(i["id"])
            i["folhas_feitas"], i["folhas_total"] = f, t
            if i["folha"]:
                if i["status"] != "cancelado":
                    total += 1
                    feitas += 1 if i["feito"] else 0
            else:
                feitas += f
                total += t
        return feitas, total

    visitar(None, 0)
    for i in itens:  # proteção: itens órfãos por inconsistência aparecem na raiz
        if i["id"] not in vistos:
            i.update(nivel=0, folha=True, folhas_feitas=0, folhas_total=0)
            ordenados.append(i)
    return ordenados


def folhas(itens):
    """Itens que representam trabalho (sem filhos) e não foram cancelados."""
    return [i for i in itens if i["folha"] and i["status"] != "cancelado"]


def obter_item(projeto_id, item_id):
    row = get_db().execute("SELECT * FROM item WHERE id = ? AND projeto_id = ?", (item_id, projeto_id)).fetchone()
    if row is None:
        abort(404)
    return row


def linha_base_atual(projeto_id):
    row = get_db().execute("SELECT * FROM linha_base WHERE projeto_id = ? ORDER BY id DESC LIMIT 1", (projeto_id,)).fetchone()
    if row is None:
        return None
    lb = dict(row)
    lb["dados"] = json.loads(row["dados_json"] or "{}")
    lb["ids"] = {int(k) for k in lb["dados"].get("itens", {})}
    lb["versao"] = get_db().execute("SELECT COUNT(*) FROM linha_base WHERE projeto_id = ?", (projeto_id,)).fetchone()[0]
    return lb


def fora_da_linha_base(itens, lb):
    """Itens de trabalho que entraram depois da linha de base: (todos, sem mudança aprovada)."""
    if lb is None:
        return [], []
    novos = [i for i in folhas(itens) if i["id"] not in lb["ids"]]
    sem_mudanca = [i for i in novos if i["mudanca_status"] not in MUDANCA_APROVADA]
    return novos, sem_mudanca


def custo_qualidade(projeto_id):
    rows = get_db().execute(
        "SELECT categoria, COUNT(*) AS n, COALESCE(SUM(custo), 0) AS total FROM qualidade_custo WHERE projeto_id = ? GROUP BY categoria",
        (projeto_id,),
    ).fetchall()
    por_cat = {r["categoria"]: {"n": r["n"], "total": r["total"]} for r in rows}
    resumo = {"categorias": [], "conformidade": 0.0, "nao_conformidade": 0.0, "n": 0}
    for chave, nome, grupo, _ in pmbok.CUSTO_QUALIDADE:
        d = por_cat.get(chave, {"n": 0, "total": 0.0})
        resumo["categorias"].append({"chave": chave, "nome": nome, "grupo": grupo, **d})
        resumo[grupo] += d["total"]
        resumo["n"] += d["n"]
    resumo["total"] = resumo["conformidade"] + resumo["nao_conformidade"]
    defeitos = get_db().execute(
        """SELECT COUNT(*) AS n, COALESCE(SUM(resolvido), 0) AS resolvidos FROM qualidade_custo
           WHERE projeto_id = ? AND categoria IN ('falha_interna', 'falha_externa')""", (projeto_id,)
    ).fetchone()
    resumo["defeitos"], resumo["defeitos_resolvidos"] = defeitos["n"], defeitos["resolvidos"]
    return resumo


def resumo_entrega(projeto, itens=None):
    pid = projeto["id"]
    itens = listar_itens(pid) if itens is None else itens
    trabalho = folhas(itens)
    usar_estimativa = bool(trabalho) and all(i["estimativa"] for i in trabalho)

    def tamanho(lista):
        return sum(i["estimativa"] for i in lista) if usar_estimativa else len(lista)

    total = tamanho(trabalho)
    aceitos = [i for i in trabalho if i["status"] == "aceito"]
    feitos = [i for i in trabalho if i["feito"]]
    ativos = [i for i in trabalho if i["status"] in ("a_fazer", "em_andamento")]
    lb = linha_base_atual(pid)
    novos, sem_mudanca = fora_da_linha_base(itens, lb)
    desde = (date.today() - timedelta(days=JANELA_FLUXO_DIAS)).isoformat()
    # Trabalho novo: o que entrou na janela e não fazia parte do escopo inicial. Sem linha de base,
    # só conta quando o projeto já existia antes da janela (senão é apenas o backlog sendo montado).
    if lb is not None:
        criados = [i for i in trabalho if i["criado_em"][:10] >= desde and i["id"] not in lb["ids"]]
    elif any(i["criado_em"][:10] < desde for i in trabalho):
        criados = [i for i in trabalho if i["criado_em"][:10] >= desde]
    else:
        criados = []
    concluidos = [i for i in trabalho if i["feito"] and (i["concluido_em"] or "")[:10] >= desde]
    hoje = date.today().isoformat()
    bens = get_db().execute("SELECT * FROM beneficio WHERE projeto_id = ?", (pid,)).fetchall()
    return {
        "n_itens": len(trabalho),
        "base": "estimativa" if usar_estimativa else "itens",
        "total": total,
        "feito": tamanho(feitos),
        "aceito": tamanho(aceitos),
        "pct_feito": round(100 * tamanho(feitos) / total) if total else 0,
        "pct_aceito": round(100 * tamanho(aceitos) / total) if total else 0,
        "aguardando_aceite": sum(1 for i in trabalho if i["status"] == "concluido"),
        "wip": sum(1 for i in trabalho if i["status"] == "em_andamento"),
        "limite_wip": projeto["limite_wip"],
        "ativos": len(ativos),
        "bem_documentados": sum(1 for i in ativos if i["bem_documentado"]),
        "linha_base": lb,
        "novos_pos_base": novos,
        "sem_mudanca": sem_mudanca,
        "fluxo_criados": tamanho(criados),
        "fluxo_concluidos": tamanho(concluidos),
        "beneficios": len(bens),
        "beneficios_realizados": sum(1 for b in bens if b["status"] == "realizado"),
        "beneficios_atrasados": [b for b in bens if b["status"] in ("planejado", "parcial") and b["data_prevista"] and b["data_prevista"] < hoje],
        "coq": custo_qualidade(pid),
    }


def gerar_alertas_entrega(projeto, itens=None):
    pid = projeto["id"]
    itens = listar_itens(pid) if itens is None else itens
    r = resumo_entrega(projeto, itens)
    alertas = []
    url_itens = url_for("entrega.itens", projeto_id=pid)

    def link(i):
        return url_for("entrega.item", projeto_id=pid, item_id=i["id"])

    if r["sem_mudanca"] and projeto["abordagem"] != "adaptativa":
        codigos = ", ".join(i["rotulo"] for i in r["sem_mudanca"][:4]) + ("…" if len(r["sem_mudanca"]) > 4 else "")
        alertas.append(("alto", f"{len(r['sem_mudanca'])} item(ns) entraram no escopo depois da linha de base sem mudança aprovada "
                                f"({codigos}): possível scope creep.", url_itens))
    if projeto["abordagem"] == "adaptativa" and r["fluxo_criados"] > r["fluxo_concluidos"]:
        unidade = projeto["unidade_estimativa"] if r["base"] == "estimativa" else "itens"
        alertas.append(("medio", f"Nos últimos {JANELA_FLUXO_DIAS} dias entrou mais trabalho novo ({r['fluxo_criados']:g} {unidade}) do que foi "
                                 f"concluído ({r['fluxo_concluidos']:g}). Nesse ritmo o projeto não termina.", url_itens))
    if r["limite_wip"] and r["wip"] > r["limite_wip"]:
        alertas.append(("medio", f"Trabalho em andamento ({r['wip']}) acima do limite definido ({r['limite_wip']}).",
                        url_for("entrega.quadro", projeto_id=pid)))
    for i in folhas(itens):
        if i["status"] == "em_andamento" and not i["qualidade"]["verificavel"]:
            alertas.append(("medio", f"{i['rotulo']} ({i['titulo']}) está em andamento sem critérios de aceite.", link(i)))
        if (i["dias_aguardando_aceite"] or 0) > DIAS_AGUARDANDO_ACEITE:
            alertas.append(("medio", f"{i['rotulo']} ({i['titulo']}) foi concluído há {i['dias_aguardando_aceite']} dias e ainda não foi aceito.", link(i)))
    for b in r["beneficios_atrasados"]:
        alertas.append(("medio", f"Benefício “{b['descricao']}” passou da data prevista ({date.fromisoformat(b['data_prevista']).strftime('%d/%m/%Y')}) sem ser realizado.",
                        url_for("entrega.beneficios", projeto_id=pid)))
    sem_item = get_db().execute(
        """SELECT m.id, m.codigo, m.titulo FROM mudanca m WHERE m.projeto_id = ? AND m.status = 'aprovada'
           AND NOT EXISTS (SELECT 1 FROM item i WHERE i.mudanca_id = m.id)""", (pid,)
    ).fetchall()
    for m in sem_item:
        alertas.append(("info", f"M-{m['codigo']} ({m['titulo']}) foi aprovada e ainda não foi incorporada ao escopo.",
                        url_for("trabalho.mudanca", projeto_id=pid, mudanca_id=m["id"]) + "#escopo"))
    coq = r["coq"]
    if coq["nao_conformidade"] > coq["conformidade"] and coq["nao_conformidade"] > 0:
        alertas.append(("medio", f"O custo das falhas ({moeda(coq['nao_conformidade'])}) é maior que o investido em prevenção e avaliação "
                                 f"({moeda(coq['conformidade'])}).", url_for("entrega.qualidade", projeto_id=pid)))
    if r["n_itens"] and not (projeto["definicao_pronto"] or "").strip() and projeto["abordagem"] in ("adaptativa", "hibrida"):
        alertas.append(("info", "A definição de pronto ainda não foi escrita.", url_for("entrega.painel", projeto_id=pid) + "#parametros"))
    return [{"nivel": n, "texto": t, "link": l} for n, t, l in alertas]


def indicadores(projeto):
    r = resumo_entrega(projeto)
    if not r["n_itens"]:
        ind = ["Nenhum item de escopo registrado."]
    else:
        unidade = projeto["unidade_estimativa"] if r["base"] == "estimativa" else "itens"
        ind = [f"Escopo: {r['aceito']:g} de {r['total']:g} {unidade} aceitos ({r['pct_aceito']}%); {r['pct_feito']}% concluídos.",
               f"Requisitos bem documentados: {r['bem_documentados']} de {r['ativos']} itens ainda não concluídos."]
        if r["linha_base"]:
            ind.append(f"Depois da linha de base entraram {len(r['novos_pos_base'])} itens, {len(r['sem_mudanca'])} sem mudança aprovada.")
    if r["beneficios"]:
        ind.append(f"Benefícios realizados: {r['beneficios_realizados']} de {r['beneficios']}; {len(r['beneficios_atrasados'])} atrasados.")
    coq = r["coq"]
    if coq["n"]:
        ind.append(f"Custo da qualidade: {moeda(coq['conformidade'])} em conformidade e {moeda(coq['nao_conformidade'])} em falhas; "
                   f"{coq['defeitos_resolvidos']} de {coq['defeitos']} defeitos resolvidos.")
    return ind


# --------------------------------------------------------------------------
# Regras de escrita
# --------------------------------------------------------------------------
def _existe(tabela, projeto_id, valor):
    if valor is None:
        return None
    ok = get_db().execute(f"SELECT 1 FROM {tabela} WHERE id = ? AND projeto_id = ?", (valor, projeto_id)).fetchone()
    return valor if ok else None


def _pai_valido(projeto_id, pai_id, item_id):
    """O pai precisa ser do mesmo projeto e não pode ser o próprio item nem um descendente dele."""
    db = get_db()
    atual = db.execute("SELECT id, pai_id FROM item WHERE id = ? AND projeto_id = ?", (pai_id, projeto_id)).fetchone() if pai_id else None
    if atual is None:
        return None
    vistos = set()
    while atual is not None:
        if atual["id"] == item_id or atual["id"] in vistos:
            return None
        vistos.add(atual["id"])
        atual = db.execute("SELECT id, pai_id FROM item WHERE id = ?", (atual["pai_id"],)).fetchone() if atual["pai_id"] else None
    return pai_id


def _ler_item(projeto, item_id=None):
    f = request.form
    pid = projeto["id"]
    return {
        "titulo": f.get("titulo", "").strip(),
        "descricao": f.get("descricao", "").strip(),
        "criterios_aceite": f.get("criterios_aceite", "").strip(),
        "tipo": f.get("tipo") if f.get("tipo") in dict(pmbok.TIPOS_ITEM) else "historia",
        "pai_id": _pai_valido(pid, inteiro(f.get("pai_id"), 1, 10**9), item_id),
        "ordem": inteiro(f.get("ordem"), 1, 10**6),
        "valor": inteiro(f.get("valor")),
        "estimativa": decimal(f.get("estimativa")),
        "q_claro": 1 if f.get("q_claro") else 0,
        "q_conciso": 1 if f.get("q_conciso") else 0,
        "q_consistente": 1 if f.get("q_consistente") else 0,
        "status": f.get("status") if f.get("status") in dict(pmbok.STATUS_ITEM) else "a_fazer",
        "dod_ok": 1 if f.get("dod_ok") else 0,
        "responsavel": f.get("responsavel", "").strip(),
        "aceito_por": f.get("aceito_por", "").strip(),
        "parte_id": _existe("parte_interessada", pid, inteiro(f.get("parte_id"), 1, 10**9)),
        "mudanca_id": _existe("mudanca", pid, inteiro(f.get("mudanca_id"), 1, 10**9)),
        "risco_id": _existe("risco", pid, inteiro(f.get("risco_id"), 1, 10**9)),
        "moscow": f.get("moscow") if f.get("moscow") in ("must", "should", "could", "wont") else "",
    }


def aplicar_status(projeto, anterior, dados):
    """Valida a mudança de status e ajusta as datas. Devolve uma mensagem de erro ou None.

    Regras (2.6.2.2): concluir exige atender à definição de pronto, quando houver;
    aceitar exige critérios de aceite e o nome de quem aceitou.
    """
    novo = dados["status"]
    hoje = date.today().isoformat()
    import pmo
    if novo == "em_andamento" and (anterior is None or anterior["status"] != "em_andamento"):
        exigencia = pmo.exigir("item", dados)
        if exigencia:
            return exigencia
    for campo in ("iniciado_em", "concluido_em", "aceito_em"):
        dados[campo] = anterior[campo] if anterior is not None else None
    if novo in ("concluido", "aceito") and (projeto["definicao_pronto"] or "").strip() and not dados["dod_ok"]:
        return "Para concluir o item, confirme que ele atende à definição de pronto."
    if novo == "aceito":
        if not dados["criterios_aceite"]:
            return "Não é possível aceitar um item sem critérios de aceite: o aceite precisa ser verificável."
        if not dados["aceito_por"]:
            return "Informe quem aceitou a entrega."
    if novo == "a_fazer":
        dados["iniciado_em"] = dados["concluido_em"] = dados["aceito_em"] = None
    elif novo == "em_andamento":
        dados["iniciado_em"] = dados["iniciado_em"] or hoje
        dados["concluido_em"] = dados["aceito_em"] = None
    elif novo == "concluido":
        dados["iniciado_em"] = dados["iniciado_em"] or hoje
        dados["concluido_em"] = dados["concluido_em"] or hoje
        dados["aceito_em"] = None
    elif novo == "aceito":
        dados["iniciado_em"] = dados["iniciado_em"] or hoje
        dados["concluido_em"] = dados["concluido_em"] or hoje
        dados["aceito_em"] = dados["aceito_em"] or hoje
    return None


def _contexto_form(projeto, item_id=None):
    pid = projeto["id"]
    db = get_db()
    candidatos = [i for i in listar_itens(pid) if i["id"] != item_id]
    return {
        "partes": db.execute("SELECT id, nome FROM parte_interessada WHERE projeto_id = ? AND ativa = 1 ORDER BY nome", (pid,)).fetchall(),
        "mudancas": db.execute("SELECT id, codigo, titulo, status FROM mudanca WHERE projeto_id = ? ORDER BY codigo", (pid,)).fetchall(),
        "riscos": db.execute("SELECT id, codigo, titulo FROM risco WHERE projeto_id = ? ORDER BY codigo", (pid,)).fetchall(),
        "pais": candidatos,
        "dod": [x.strip() for x in (projeto["definicao_pronto"] or "").splitlines() if x.strip()],
    }


# --------------------------------------------------------------------------
# Rotas: painel e linha de base
# --------------------------------------------------------------------------
@bp.route("", methods=["GET", "POST"])
def painel(projeto_id):
    p = obter_projeto(projeto_id)
    if request.method == "POST":
        unidade = request.form.get("unidade_estimativa")
        db = get_db()
        db.execute(
            "UPDATE projeto SET definicao_pronto = ?, unidade_estimativa = ?, limite_wip = ?, atualizado_em = datetime('now','localtime') WHERE id = ?",
            (request.form.get("definicao_pronto", "").strip(),
             unidade if unidade in dict(pmbok.UNIDADES_ESTIMATIVA) else p["unidade_estimativa"],
             inteiro(request.form.get("limite_wip"), 1, 1000), projeto_id),
        )
        db.commit()
        flash("Parâmetros de entrega salvos.", "ok")
        return redirect(url_for("entrega.painel", projeto_id=projeto_id))
    itens = listar_itens(projeto_id)
    return render_template("entrega_painel.html", projeto=p, resumo=resumo_entrega(p, itens),
                           alertas=gerar_alertas_entrega(p, itens), secao="entrega", sub="painel")


def capturar_linha_base(itens):
    campos = ("estimativa", "custo_planejado", "inicio_planejado", "fim_planejado")
    dados = {str(i["id"]): {"titulo": i["titulo"], **{c: i.get(c) for c in campos}} for i in folhas(itens)}
    return {"itens": dados, "n": len(dados), "total_estimativa": sum(i["estimativa"] or 0 for i in folhas(itens))}


@bp.route("/linha-base", methods=["POST"])
def linha_base(projeto_id):
    p = obter_projeto(projeto_id)
    itens = listar_itens(projeto_id)
    if not folhas(itens):
        flash("Registre os itens do escopo antes de definir a linha de base.", "erro")
        return redirect(url_for("entrega.painel", projeto_id=projeto_id))
    motivo = request.form.get("motivo", "").strip()
    if linha_base_atual(projeto_id) is not None and not motivo:
        flash("Para refazer a linha de base, informe o motivo (ex.: a mudança aprovada que a justifica).", "erro")
        return redirect(url_for("entrega.painel", projeto_id=projeto_id) + "#linha-base")
    db = get_db()
    db.execute("INSERT INTO linha_base (projeto_id, motivo, dados_json) VALUES (?, ?, ?)",
               (projeto_id, motivo, json.dumps(capturar_linha_base(itens))))
    tocar_projeto(projeto_id)
    db.commit()
    flash("Linha de base definida." + (" Itens novos devem vir de mudanças aprovadas." if p["abordagem"] != "adaptativa" else ""), "ok")
    return redirect(url_for("entrega.painel", projeto_id=projeto_id) + "#linha-base")


# --------------------------------------------------------------------------
# Rotas: itens
# --------------------------------------------------------------------------
@bp.route("/itens")
def itens(projeto_id):
    p = obter_projeto(projeto_id)
    todos = listar_itens(projeto_id)
    filtro = request.args.get("status", "ativos")
    lista = todos
    if filtro == "ativos":
        lista = [i for i in todos if i["status"] != "cancelado" and not (i["folha"] and i["status"] == "aceito")]
    elif filtro in dict(pmbok.STATUS_ITEM):
        lista = [i for i in todos if i["status"] == filtro]
    lb = linha_base_atual(projeto_id)
    _, sem_mudanca = fora_da_linha_base(todos, lb)
    return render_template("itens.html", projeto=p, itens=lista, total=len(todos), filtro=filtro, linha_base=lb,
                           fora_base={i["id"] for i in sem_mudanca} if p["abordagem"] != "adaptativa" else set(),
                           secao="entrega", sub="itens")


@bp.route("/itens/ordem", methods=["POST"])
def itens_ordem(projeto_id):
    obter_projeto(projeto_id)
    db = get_db()
    for chave, valor in request.form.items():
        if chave.startswith("ordem_"):
            item_id = inteiro(chave[6:], 1, 10**9)
            if item_id:
                db.execute("UPDATE item SET ordem = ? WHERE id = ? AND projeto_id = ?",
                           (inteiro(valor, 1, 10**6), item_id, projeto_id))
    tocar_projeto(projeto_id)
    db.commit()
    flash("Ordem de prioridade salva.", "ok")
    return redirect(url_for("entrega.itens", projeto_id=projeto_id))


def _salvar_dependencias(db, projeto_id, item_id):
    if not request.form.get("dependencias_enviadas"):
        return
    import metodos
    ids = [inteiro(v, 1, 10**9) for v in request.form.getlist("depende_de")]
    ciclo = metodos.salvar_dependencias(db, projeto_id, item_id, [i for i in ids if i])
    if ciclo:
        flash("Algumas dependências foram ignoradas porque criariam um ciclo (um item dependendo de si mesmo).", "aviso")


@bp.route("/itens/novo", methods=["GET", "POST"])
def item_novo(projeto_id):
    p = obter_projeto(projeto_id)
    db = get_db()
    if request.method == "POST":
        dados = _ler_item(p)
        erro = None if dados["titulo"] else "Dê um título ao item."
        erro = erro or aplicar_status(p, None, dados)
        if erro:
            flash(erro, "erro")
            return render_template("item_form.html", projeto=p, i=dados, novo=True, filhos=[], secao="entrega", sub="itens",
                                   **_contexto_form(p))
        codigo = db.execute("SELECT COALESCE(MAX(codigo), 0) + 1 FROM item WHERE projeto_id = ?", (projeto_id,)).fetchone()[0]
        cols = list(dados)
        cur = db.execute(f"INSERT INTO item (projeto_id, codigo, {', '.join(cols)}) VALUES (?, ?, {', '.join('?' for _ in cols)})",
                         [projeto_id, codigo] + [dados[c] for c in cols])
        _salvar_dependencias(db, projeto_id, cur.lastrowid)
        tocar_projeto(projeto_id)
        db.commit()
        flash(f"I-{codigo} registrado.", "ok")
        if request.form.get("acao") == "outro":
            return redirect(url_for("entrega.item_novo", projeto_id=projeto_id, pai=dados["pai_id"] or ""))
        return redirect(url_for("entrega.item", projeto_id=projeto_id, item_id=cur.lastrowid))
    inicial = {"status": "a_fazer", "tipo": "entregavel" if p["abordagem"] == "preditiva" else "historia",
               "pai_id": inteiro(request.args.get("pai"), 1, 10**9)}
    mudanca = db.execute("SELECT * FROM mudanca WHERE id = ? AND projeto_id = ?",
                         (inteiro(request.args.get("mudanca"), 1, 10**9), projeto_id)).fetchone()
    if mudanca:
        inicial.update(mudanca_id=mudanca["id"], titulo=mudanca["titulo"], descricao=mudanca["descricao"], parte_id=mudanca["parte_id"])
    risco = db.execute("SELECT * FROM risco WHERE id = ? AND projeto_id = ?",
                       (inteiro(request.args.get("risco"), 1, 10**9), projeto_id)).fetchone()
    if risco:
        inicial.update(risco_id=risco["id"], titulo=f"Resposta ao risco R-{risco['codigo']}: {risco['titulo']}",
                       descricao=risco["plano_resposta"], responsavel=risco["responsavel"])
    return render_template("item_form.html", projeto=p, i=inicial, novo=True, filhos=[], secao="entrega", sub="itens",
                           **_contexto_form(p))


@bp.route("/itens/<int:item_id>", methods=["GET", "POST"])
def item(projeto_id, item_id):
    p = obter_projeto(projeto_id)
    atual = obter_item(projeto_id, item_id)
    db = get_db()
    if request.method == "POST":
        if request.form.get("acao") == "excluir":
            db.execute("DELETE FROM item WHERE id = ?", (item_id,))
            tocar_projeto(projeto_id)
            db.commit()
            flash(f"I-{atual['codigo']} excluído.", "ok")
            return redirect(url_for("entrega.itens", projeto_id=projeto_id))
        dados = _ler_item(p, item_id)
        erro = None if dados["titulo"] else "Dê um título ao item."
        erro = erro or aplicar_status(p, atual, dados)
        if erro:
            flash(erro, "erro")
            visao = enriquecer_item({**dict(atual), **dados, "status": atual["status"]})
            return render_template("item_form.html", projeto=p, i=visao, novo=False, pedido=dados["status"],
                                   filhos=[x for x in listar_itens(projeto_id) if x["pai_id"] == item_id],
                                   secao="entrega", sub="itens", **_contexto_form(p, item_id))
        db.execute("UPDATE item SET " + ", ".join(f"{c} = ?" for c in dados)
                   + ", atualizado_em = datetime('now','localtime') WHERE id = ?", list(dados.values()) + [item_id])
        _salvar_dependencias(db, projeto_id, item_id)
        tocar_projeto(projeto_id)
        db.commit()
        flash(f"I-{atual['codigo']} atualizado.", "ok")
        return redirect(url_for("entrega.item", projeto_id=projeto_id, item_id=item_id))
    return render_template("item_form.html", projeto=p, i=enriquecer_item(atual), novo=False,
                           filhos=[x for x in listar_itens(projeto_id) if x["pai_id"] == item_id],
                           secao="entrega", sub="itens", **_contexto_form(p, item_id))


@bp.route("/itens/<int:item_id>/mover", methods=["POST"])
def item_mover(projeto_id, item_id):
    """Movimento rápido pelo quadro. Quando falta informação (pronto, aceite), leva à página do item."""
    p = obter_projeto(projeto_id)
    atual = obter_item(projeto_id, item_id)
    destino = request.form.get("destino")
    if destino not in pmbok.COLUNAS_QUADRO:
        abort(400)
    dados = {c: atual[c] for c in ("status", "dod_ok", "criterios_aceite", "aceito_por")}
    dados["status"] = destino
    erro = aplicar_status(p, atual, dados)
    if erro:
        flash(erro, "erro")
        return redirect(url_for("entrega.item", projeto_id=projeto_id, item_id=item_id) + "#conclusao")
    db = get_db()
    db.execute("UPDATE item SET status = ?, iniciado_em = ?, concluido_em = ?, aceito_em = ?, atualizado_em = datetime('now','localtime') WHERE id = ?",
               (destino, dados["iniciado_em"], dados["concluido_em"], dados["aceito_em"], item_id))
    tocar_projeto(projeto_id)
    db.commit()
    return redirect(url_for("entrega.quadro", projeto_id=projeto_id))


@bp.route("/quadro")
def quadro(projeto_id):
    p = obter_projeto(projeto_id)
    trabalho = folhas(listar_itens(projeto_id))
    colunas = [{"chave": c, "nome": dict(pmbok.STATUS_ITEM)[c], "itens": [i for i in trabalho if i["status"] == c]}
               for c in pmbok.COLUNAS_QUADRO]
    return render_template("quadro.html", projeto=p, colunas=colunas, secao="entrega", sub="quadro")


# --------------------------------------------------------------------------
# Rotas: qualidade e benefícios
# --------------------------------------------------------------------------
@bp.route("/qualidade", methods=["GET", "POST"])
def qualidade(projeto_id):
    p = obter_projeto(projeto_id)
    db = get_db()
    if request.method == "POST":
        f = request.form
        reg_id = inteiro(f.get("registro_id"), 1, 10**9)
        if f.get("acao") == "excluir":
            db.execute("DELETE FROM qualidade_custo WHERE id = ? AND projeto_id = ?", (reg_id, projeto_id))
            flash("Registro removido.", "ok")
        elif f.get("acao") == "resolver":
            db.execute("UPDATE qualidade_custo SET resolvido = 1 - resolvido WHERE id = ? AND projeto_id = ?", (reg_id, projeto_id))
        else:
            descricao = f.get("descricao", "").strip()
            if f.get("categoria") not in pmbok.CUSTO_QUALIDADE_NOME or not descricao:
                flash("Escolha a categoria e descreva a atividade ou a falha.", "erro")
                return redirect(url_for("entrega.qualidade", projeto_id=projeto_id))
            data = f.get("data") or date.today().isoformat()
            try:
                data = min(date.fromisoformat(data), date.today()).isoformat()
            except ValueError:
                data = date.today().isoformat()
            db.execute("INSERT INTO qualidade_custo (projeto_id, data, categoria, descricao, custo, item_id) VALUES (?, ?, ?, ?, ?, ?)",
                       (projeto_id, data, f.get("categoria"), descricao, decimal(f.get("custo")),
                        _existe("item", projeto_id, inteiro(f.get("item_id"), 1, 10**9))))
            flash("Registro de qualidade adicionado.", "ok")
        tocar_projeto(projeto_id)
        db.commit()
        return redirect(url_for("entrega.qualidade", projeto_id=projeto_id))
    registros = db.execute(
        """SELECT q.*, i.codigo AS item_codigo FROM qualidade_custo q LEFT JOIN item i ON i.id = q.item_id
           WHERE q.projeto_id = ? ORDER BY q.data DESC, q.id DESC""", (projeto_id,)
    ).fetchall()
    return render_template("qualidade.html", projeto=p, registros=registros, coq=custo_qualidade(projeto_id),
                           itens=listar_itens(projeto_id), secao="entrega", sub="qualidade")


def _ler_beneficio():
    f = request.form
    prevista = f.get("data_prevista") or None
    if prevista:
        try:
            date.fromisoformat(prevista)
        except ValueError:
            prevista = None
    return {
        "descricao": f.get("descricao", "").strip(), "medida": f.get("medida", "").strip(), "meta": f.get("meta", "").strip(),
        "data_prevista": prevista, "resultado": f.get("resultado", "").strip(),
        "status": f.get("status") if f.get("status") in dict(pmbok.STATUS_BENEFICIO) else "planejado",
    }


@bp.route("/beneficios", methods=["GET", "POST"])
def beneficios(projeto_id):
    p = obter_projeto(projeto_id)
    db = get_db()
    if request.method == "POST":
        dados = _ler_beneficio()
        if not dados["descricao"]:
            flash("Descreva o benefício esperado.", "erro")
        else:
            cols = list(dados)
            db.execute(f"INSERT INTO beneficio (projeto_id, {', '.join(cols)}) VALUES (?, {', '.join('?' for _ in cols)})",
                       [projeto_id] + [dados[c] for c in cols])
            tocar_projeto(projeto_id)
            db.commit()
            flash("Benefício registrado.", "ok")
        return redirect(url_for("entrega.beneficios", projeto_id=projeto_id))
    lista = db.execute("SELECT * FROM beneficio WHERE projeto_id = ? ORDER BY data_prevista IS NULL, data_prevista, id", (projeto_id,)).fetchall()
    return render_template("beneficios.html", projeto=p, beneficios=lista, secao="entrega", sub="beneficios")


@bp.route("/beneficios/<int:beneficio_id>", methods=["POST"])
def beneficio(projeto_id, beneficio_id):
    obter_projeto(projeto_id)
    db = get_db()
    if db.execute("SELECT 1 FROM beneficio WHERE id = ? AND projeto_id = ?", (beneficio_id, projeto_id)).fetchone() is None:
        abort(404)
    if request.form.get("acao") == "excluir":
        db.execute("DELETE FROM beneficio WHERE id = ?", (beneficio_id,))
        flash("Benefício removido.", "ok")
    else:
        dados = _ler_beneficio()
        if not dados["descricao"]:
            flash("Descreva o benefício esperado.", "erro")
            return redirect(url_for("entrega.beneficios", projeto_id=projeto_id))
        if dados["status"] in ("realizado", "parcial") and not dados["resultado"]:
            flash("Para marcar como realizado, registre o resultado medido.", "erro")
            return redirect(url_for("entrega.beneficios", projeto_id=projeto_id))
        db.execute("UPDATE beneficio SET " + ", ".join(f"{c} = ?" for c in dados)
                   + ", atualizado_em = datetime('now','localtime') WHERE id = ?", list(dados.values()) + [beneficio_id])
        flash("Benefício atualizado.", "ok")
    tocar_projeto(projeto_id)
    db.commit()
    return redirect(url_for("entrega.beneficios", projeto_id=projeto_id))
