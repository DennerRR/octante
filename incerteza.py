"""Domínio de desempenho Incerteza (PMBOK 7, seção 2.8).

Registro de riscos (ameaças e oportunidades), revisões periódicas, reservas,
risco global do projeto e incertezas não-risco (ambiguidade, complexidade,
volatilidade).
"""
from datetime import date, timedelta

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

import pmbok
from db import get_db
from util import decimal, inteiro, moeda, obter_projeto, tocar_projeto

bp = Blueprint("incerteza", __name__, url_prefix="/p/<int:projeto_id>/incerteza")

CAMPOS_TEXTO_RISCO = ["titulo", "causa", "efeito", "responsavel", "plano_resposta", "gatilho",
                      "plano_contingencia", "riscos_secundarios"]


# --------------------------------------------------------------------------
# Consultas e regras
# --------------------------------------------------------------------------
def enriquecer_risco(row, projeto):
    r = dict(row)
    limite = projeto["limite_risco"]
    r["rotulo"] = f"R-{r['codigo']}"
    r["pontuacao"] = r["probabilidade"] * r["impacto"] if r["probabilidade"] and r["impacto"] else None
    r["nivel"] = pmbok.nivel_risco(r["pontuacao"], limite)
    r["ativo"] = r["status"] in pmbok.STATUS_RISCO_ATIVOS
    r["estrategia_nome"] = pmbok.ESTRATEGIAS_NOME.get(r["tipo"], {}).get(r["estrategia"], "")
    r["emv"] = None
    if r["impacto_custo"] is not None and r["probabilidade"]:
        valor = pmbok.PROB_PERCENTUAL[r["probabilidade"]] * r["impacto_custo"]
        r["emv"] = -valor if r["tipo"] == "ameaca" else valor
    referencia = r["revisado_em"] or r["identificado_em"]
    limite_data = (date.today() - timedelta(days=projeto["revisao_risco_dias"])).isoformat()
    r["revisao_atrasada"] = r["ativo"] and (referencia or "") < limite_data
    return r


def listar_riscos(projeto, so_ativos=False):
    db = get_db()
    sql = """SELECT r.*, s.nome AS parte_nome FROM risco r
             LEFT JOIN parte_interessada s ON s.id = r.parte_id
             WHERE r.projeto_id = ?"""
    if so_ativos:
        sql += " AND r.status IN ('aberto', 'em_resposta')"
    rows = db.execute(sql, (projeto["id"],)).fetchall()
    riscos = [enriquecer_risco(r, projeto) for r in rows]
    riscos.sort(key=lambda r: (not r["ativo"], -(r["pontuacao"] or 0), r["codigo"]))
    return riscos


def obter_risco(projeto, risco_id):
    row = get_db().execute(
        """SELECT r.*, s.nome AS parte_nome FROM risco r LEFT JOIN parte_interessada s ON s.id = r.parte_id
           WHERE r.id = ? AND r.projeto_id = ?""", (risco_id, projeto["id"])
    ).fetchone()
    if row is None:
        abort(404)
    return enriquecer_risco(row, projeto)


def matriz(riscos, tipo, limite):
    """Matriz probabilidade × impacto (linhas: probabilidade 5→1; colunas: impacto 1→5)."""
    linhas = []
    for p in range(5, 0, -1):
        celulas = []
        for i in range(1, 6):
            itens = [r for r in riscos if r["ativo"] and r["tipo"] == tipo and r["probabilidade"] == p and r["impacto"] == i]
            celulas.append({"p": p, "i": i, "nivel": pmbok.nivel_risco(p * i, limite), "riscos": itens})
        linhas.append({"p": p, "celulas": celulas})
    return linhas


def resumo_riscos(projeto, riscos):
    ativos = [r for r in riscos if r["ativo"]]
    ameacas = [r for r in ativos if r["tipo"] == "ameaca"]
    oportunidades = [r for r in ativos if r["tipo"] == "oportunidade"]
    emv_ameacas = sum(r["emv"] for r in ameacas if r["emv"] is not None)
    emv_oport = sum(r["emv"] for r in oportunidades if r["emv"] is not None)
    # A reserva continua comprometida quando o risco ocorre (é aí que ela é usada);
    # só é liberada quando o risco é encerrado.
    comprometidas = [r for r in riscos if r["tipo"] == "ameaca" and r["status"] != "encerrado"]
    contingencia = sum(r["reserva_custo"] or 0 for r in comprometidas)
    usado = get_db().execute(
        """SELECT COALESCE(SUM(CASE WHEN risco_id IS NOT NULL THEN reserva_usada_custo END), 0),
                  COALESCE(SUM(CASE WHEN risco_id IS NULL THEN reserva_usada_custo END), 0)
           FROM questao WHERE projeto_id = ?""", (projeto["id"],)
    ).fetchone()
    return {
        "total": len(riscos),
        "ativos": len(ativos),
        "ameacas": len(ameacas),
        "oportunidades": len(oportunidades),
        "altos": sum(1 for r in ameacas if r["nivel"] == "alto"),
        "oport_altas": sum(1 for r in oportunidades if r["nivel"] == "alto"),
        "emv_ameacas": emv_ameacas,
        "emv_oportunidades": emv_oport,
        "tem_emv": any(r["emv"] is not None for r in ativos),
        "contingencia_custo": contingencia,
        "contingencia_prazo": sum(r["reserva_prazo_dias"] or 0 for r in comprometidas),
        "gerenciamento": projeto["reserva_gerenciamento"],
        "contingencia_usada": usado[0],
        "gerenciamento_usado": usado[1],
        "ocorridos": sum(1 for r in riscos if r["status"] == "ocorreu"),
    }


def gerar_alertas_incerteza(projeto, riscos):
    pid = projeto["id"]
    alertas = []

    def link(r):
        return url_for("incerteza.risco_detalhe", projeto_id=pid, risco_id=r["id"])

    if projeto["risco_global"] == "alto":
        alertas.append(("alto", "O risco global do projeto foi avaliado como alto. Reavalie a viabilidade com o patrocinador.",
                        url_for("incerteza.painel", projeto_id=pid) + "#global"))
    if not riscos:
        alertas.append(("info", "Nenhum risco identificado. Todo projeto tem riscos: comece pelas ameaças e oportunidades já percebidas.",
                        url_for("incerteza.risco_novo", projeto_id=pid)))
    com_questao = {row[0] for row in get_db().execute(
        "SELECT risco_id FROM questao WHERE projeto_id = ? AND risco_id IS NOT NULL", (pid,))}
    res = resumo_riscos(projeto, riscos)
    if res["contingencia_usada"] > res["contingencia_custo"]:
        alertas.append(("alto", f"Reserva de contingência usada ({moeda(res['contingencia_usada'])}) excede a reservada ({moeda(res['contingencia_custo'])}).",
                        url_for("incerteza.painel", projeto_id=pid)))
    if res["gerenciamento_usado"] > (res["gerenciamento"] or 0):
        alertas.append(("alto", f"Reserva de gerenciamento usada ({moeda(res['gerenciamento_usado'])}) excede a disponível ({moeda(res['gerenciamento'] or 0)}).",
                        url_for("incerteza.painel", projeto_id=pid) + "#global"))
    for r in riscos:
        if r["status"] == "ocorreu" and r["id"] not in com_questao:
            alertas.append(("medio", f"{r['rotulo']} ({r['titulo']}) ocorreu e não tem questão aberta para tratá-lo.", link(r)))
        if not r["ativo"]:
            continue
        nome = f"{r['rotulo']} ({r['titulo']})"
        if r["tipo"] == "ameaca" and r["nivel"] == "alto":
            if not r["estrategia"]:
                alertas.append(("alto", f"{nome} está acima do limite de risco e não tem estratégia de resposta.", link(r)))
            elif r["estrategia"] == "aceitar" and not r["plano_contingencia"]:
                alertas.append(("alto", f"{nome} está acima do limite de risco com aceitação passiva (sem plano de contingência).", link(r)))
        if r["tipo"] == "oportunidade" and r["nivel"] == "alto" and not r["estrategia"]:
            alertas.append(("medio", f"Oportunidade {nome} tem pontuação alta e nenhuma estratégia para aproveitá-la.", link(r)))
        if r["pontuacao"] is None:
            alertas.append(("info", f"{nome} ainda não tem probabilidade e impacto avaliados.", link(r)))
        if not r["responsavel"] and not r["parte_nome"]:
            alertas.append(("medio", f"{nome} não tem responsável.", link(r)))
        if r["revisao_atrasada"]:
            alertas.append(("medio", f"{nome} não é revisado há mais de {projeto['revisao_risco_dias']} dias.", link(r)))
    return [{"nivel": n, "texto": t, "link": l} for n, t, l in alertas]


def indicadores(projeto):
    riscos = listar_riscos(projeto)
    res = resumo_riscos(projeto, riscos)
    ind = [f"{res['ativos']} riscos ativos: {res['ameacas']} ameaças ({res['altos']} acima do limite) e {res['oportunidades']} oportunidades."]
    ativos_altos = [r for r in riscos if r["ativo"] and r["tipo"] == "ameaca" and r["nivel"] == "alto"]
    if ativos_altos:
        com_resposta = sum(1 for r in ativos_altos if r["estrategia"] and not (r["estrategia"] == "aceitar" and not r["plano_contingencia"]))
        ind.append(f"{com_resposta} de {len(ativos_altos)} ameaças acima do limite com resposta ativa.")
    atrasados = sum(1 for r in riscos if r["revisao_atrasada"])
    ind.append(f"Revisões em dia: {res['ativos'] - atrasados} de {res['ativos']} (cadência de {projeto['revisao_risco_dias']} dias).")
    if res["tem_emv"]:
        ind.append(f"EMV das ameaças: {moeda(res['emv_ameacas'])}; reserva de contingência: {moeda(res['contingencia_custo'])}.")
    if res["ocorridos"]:
        ind.append(f"{res['ocorridos']} risco(s) já ocorreram.")
    abertas = get_db().execute(
        "SELECT COUNT(*) FROM incerteza WHERE projeto_id = ? AND status != 'resolvida'", (projeto["id"],)
    ).fetchone()[0]
    ind.append(f"{abertas} incerteza(s) de ambiguidade, complexidade ou volatilidade em aberto.")
    if projeto["risco_global"]:
        ind.append("Risco global avaliado como " + dict(pmbok.RISCO_GLOBAL)[projeto["risco_global"]].lower() + ".")
    return ind


def ler_form_risco():
    f = request.form
    tipo = f.get("tipo") if f.get("tipo") in dict(pmbok.TIPOS_RISCO) else "ameaca"
    estrategia = f.get(f"estrategia_{tipo}", f.get("estrategia", ""))
    if estrategia not in pmbok.ESTRATEGIAS_NOME[tipo]:
        estrategia = ""
    status = f.get("status") if f.get("status") in dict(pmbok.STATUS_RISCO) else "aberto"
    fonte = f.get("fonte") if f.get("fonte") in dict(pmbok.FONTES_RISCO) else ""
    dados = {c: f.get(c, "").strip() for c in CAMPOS_TEXTO_RISCO}
    dados.update(
        tipo=tipo, estrategia=estrategia, status=status, fonte=fonte,
        probabilidade=inteiro(f.get("probabilidade")), impacto=inteiro(f.get("impacto")),
        impacto_custo=decimal(f.get("impacto_custo")),
        impacto_prazo_dias=inteiro(f.get("impacto_prazo_dias"), 0, 100000),
        reserva_custo=decimal(f.get("reserva_custo")),
        reserva_prazo_dias=inteiro(f.get("reserva_prazo_dias"), 0, 100000),
        parte_id=inteiro(f.get("parte_id"), 1, 10**9),
    )
    return dados


def partes_do_projeto(projeto_id):
    return get_db().execute(
        "SELECT id, nome FROM parte_interessada WHERE projeto_id = ? AND ativa = 1 ORDER BY nome", (projeto_id,)
    ).fetchall()


def validar_parte(projeto_id, parte_id):
    if parte_id is None:
        return None
    ok = get_db().execute("SELECT 1 FROM parte_interessada WHERE id = ? AND projeto_id = ?", (parte_id, projeto_id)).fetchone()
    return parte_id if ok else None


def abrir_questao_para_risco(projeto_id, risco_id):
    """Quando um risco ocorre, ele vira uma questão no registro de questões (2.5 / 4.6.2).

    Retorna o código da questão criada, ou None se o risco já tinha uma questão.
    """
    db = get_db()
    if db.execute("SELECT 1 FROM questao WHERE risco_id = ?", (risco_id,)).fetchone():
        return None
    r = db.execute("SELECT * FROM risco WHERE id = ?", (risco_id,)).fetchone()
    codigo = db.execute("SELECT COALESCE(MAX(codigo), 0) + 1 FROM questao WHERE projeto_id = ?", (projeto_id,)).fetchone()[0]
    prioridade = "alta" if r["tipo"] == "ameaca" else "media"
    descricao = "Risco R-{} ocorreu.".format(r["codigo"])
    if r["plano_contingencia"]:
        descricao += " Plano de contingência: " + r["plano_contingencia"]
    db.execute(
        """INSERT INTO questao (projeto_id, codigo, titulo, descricao, prioridade, responsavel, parte_id, risco_id)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (projeto_id, codigo, r["titulo"], descricao, prioridade, r["responsavel"], r["parte_id"], risco_id),
    )
    return codigo


def avisar_questao(codigo):
    if codigo:
        flash(f"O risco ocorreu e foi aberta a questão Q-{codigo} no registro de questões.", "aviso")


def registrar_revisao(risco_id, prob, imp, status, nota):
    hoje = date.today().isoformat()
    db = get_db()
    db.execute("INSERT INTO risco_revisao (risco_id, data, probabilidade, impacto, status, nota) VALUES (?, ?, ?, ?, ?, ?)",
               (risco_id, hoje, prob, imp, status, nota))
    db.execute("UPDATE risco SET revisado_em = ? WHERE id = ?", (hoje, risco_id))


# --------------------------------------------------------------------------
# Rotas
# --------------------------------------------------------------------------
@bp.route("", methods=["GET", "POST"])
def painel(projeto_id):
    p = obter_projeto(projeto_id)
    if request.method == "POST":
        global_ = request.form.get("risco_global", "")
        db = get_db()
        db.execute(
            """UPDATE projeto SET limite_risco = ?, revisao_risco_dias = ?, reserva_gerenciamento = ?, apetite_risco = ?,
               risco_global = ?, risco_global_notas = ?, atualizado_em = datetime('now','localtime') WHERE id = ?""",
            (inteiro(request.form.get("limite_risco"), 1, 25) or p["limite_risco"],
             inteiro(request.form.get("revisao_risco_dias"), 1, 365) or p["revisao_risco_dias"],
             decimal(request.form.get("reserva_gerenciamento")),
             request.form.get("apetite_risco", "").strip(),
             global_ if global_ in dict(pmbok.RISCO_GLOBAL) else "",
             request.form.get("risco_global_notas", "").strip(), projeto_id),
        )
        db.commit()
        flash("Parâmetros de incerteza salvos.", "ok")
        return redirect(url_for("incerteza.painel", projeto_id=projeto_id))
    riscos = listar_riscos(p)
    return render_template(
        "incerteza_painel.html", projeto=p, riscos=riscos, resumo=resumo_riscos(p, riscos),
        matriz_ameacas=matriz(riscos, "ameaca", p["limite_risco"]),
        matriz_oport=matriz(riscos, "oportunidade", p["limite_risco"]),
        alertas=gerar_alertas_incerteza(p, riscos), secao="incerteza", sub="painel",
    )


@bp.route("/riscos")
def riscos(projeto_id):
    p = obter_projeto(projeto_id)
    todos = listar_riscos(p)
    tipo = request.args.get("tipo", "")
    status = request.args.get("status", "ativos")
    lista = todos
    if tipo in dict(pmbok.TIPOS_RISCO):
        lista = [r for r in lista if r["tipo"] == tipo]
    if status == "ativos":
        lista = [r for r in lista if r["ativo"]]
    elif status in dict(pmbok.STATUS_RISCO):
        lista = [r for r in lista if r["status"] == status]
    return render_template("riscos.html", projeto=p, riscos=lista, total=len(todos), tipo=tipo, status=status,
                           secao="incerteza", sub="riscos")


@bp.route("/riscos/novo", methods=["GET", "POST"])
def risco_novo(projeto_id):
    p = obter_projeto(projeto_id)
    if request.method == "POST":
        dados = ler_form_risco()
        dados["parte_id"] = validar_parte(projeto_id, dados["parte_id"])
        import pmo
        erro_r = "Descreva o risco no campo título." if not dados["titulo"] else pmo.exigir("risco", dados, {"limite": p["limite_risco"] or 12})
        if erro_r:
            flash(erro_r, "erro")
            return render_template("risco_form.html", projeto=p, r=dados, novo=True, partes=partes_do_projeto(projeto_id),
                                   secao="incerteza", sub="riscos")
        db = get_db()
        codigo = db.execute("SELECT COALESCE(MAX(codigo), 0) + 1 FROM risco WHERE projeto_id = ?", (projeto_id,)).fetchone()[0]
        cols = list(dados)
        cur = db.execute(
            f"INSERT INTO risco (projeto_id, codigo, {', '.join(cols)}) VALUES (?, ?, {', '.join('?' for _ in cols)})",
            [projeto_id, codigo] + [dados[c] for c in cols],
        )
        registrar_revisao(cur.lastrowid, dados["probabilidade"], dados["impacto"], dados["status"], "Identificação")
        q = abrir_questao_para_risco(projeto_id, cur.lastrowid) if dados["status"] == "ocorreu" else None
        tocar_projeto(projeto_id)
        db.commit()
        avisar_questao(q)
        flash(f"R-{codigo} registrado.", "ok")
        if request.form.get("acao") == "outro":
            return redirect(url_for("incerteza.risco_novo", projeto_id=projeto_id))
        return redirect(url_for("incerteza.risco_detalhe", projeto_id=projeto_id, risco_id=cur.lastrowid))
    tipo = request.args.get("tipo")
    inicial = {"tipo": tipo if tipo in dict(pmbok.TIPOS_RISCO) else "ameaca", "status": "aberto"}
    parte = validar_parte(projeto_id, inteiro(request.args.get("parte"), 1, 10**9))
    if parte:
        inicial.update(parte_id=parte, fonte="partes")
    return render_template("risco_form.html", projeto=p, r=inicial, novo=True, partes=partes_do_projeto(projeto_id),
                           secao="incerteza", sub="riscos")


@bp.route("/riscos/<int:risco_id>")
def risco_detalhe(projeto_id, risco_id):
    p = obter_projeto(projeto_id)
    r = obter_risco(p, risco_id)
    revisoes = get_db().execute("SELECT * FROM risco_revisao WHERE risco_id = ? ORDER BY data DESC, id DESC", (risco_id,)).fetchall()
    pontos = [rv["probabilidade"] * rv["impacto"] for rv in reversed(revisoes) if rv["probabilidade"] and rv["impacto"]]
    questoes = get_db().execute("SELECT * FROM questao WHERE risco_id = ? ORDER BY codigo", (risco_id,)).fetchall()
    itens = get_db().execute("SELECT id, codigo, titulo, status FROM item WHERE risco_id = ? ORDER BY codigo", (risco_id,)).fetchall()
    return render_template("risco_detalhe.html", projeto=p, r=r, revisoes=revisoes, pontos=pontos, questoes=questoes, itens=itens,
                           secao="incerteza", sub="riscos")


@bp.route("/riscos/<int:risco_id>/editar", methods=["GET", "POST"])
def risco_editar(projeto_id, risco_id):
    p = obter_projeto(projeto_id)
    atual = obter_risco(p, risco_id)
    if request.method == "POST":
        dados = ler_form_risco()
        dados["parte_id"] = validar_parte(projeto_id, dados["parte_id"])
        import pmo
        erro_r = "Descreva o risco no campo título." if not dados["titulo"] else pmo.exigir("risco", dados, {"limite": p["limite_risco"] or 12})
        if erro_r:
            flash(erro_r, "erro")
            return render_template("risco_form.html", projeto=p, r={**dados, "id": risco_id, "rotulo": atual["rotulo"]},
                                   novo=False, partes=partes_do_projeto(projeto_id), secao="incerteza", sub="riscos")
        db = get_db()
        db.execute(
            "UPDATE risco SET " + ", ".join(f"{c} = ?" for c in dados) + ", atualizado_em = datetime('now','localtime') WHERE id = ?",
            list(dados.values()) + [risco_id],
        )
        if (dados["probabilidade"], dados["impacto"], dados["status"]) != (atual["probabilidade"], atual["impacto"], atual["status"]):
            registrar_revisao(risco_id, dados["probabilidade"], dados["impacto"], dados["status"], "Alterado na edição")
        q = abrir_questao_para_risco(projeto_id, risco_id) if dados["status"] == "ocorreu" else None
        tocar_projeto(projeto_id)
        db.commit()
        avisar_questao(q)
        flash(f"{atual['rotulo']} atualizado.", "ok")
        return redirect(url_for("incerteza.risco_detalhe", projeto_id=projeto_id, risco_id=risco_id))
    return render_template("risco_form.html", projeto=p, r=atual, novo=False, partes=partes_do_projeto(projeto_id),
                           secao="incerteza", sub="riscos")


@bp.route("/riscos/<int:risco_id>/revisar", methods=["POST"])
def risco_revisar(projeto_id, risco_id):
    p = obter_projeto(projeto_id)
    r = obter_risco(p, risco_id)
    prob = inteiro(request.form.get("probabilidade")) or r["probabilidade"]
    imp = inteiro(request.form.get("impacto")) or r["impacto"]
    status = request.form.get("status") if request.form.get("status") in dict(pmbok.STATUS_RISCO) else r["status"]
    db = get_db()
    db.execute("UPDATE risco SET probabilidade = ?, impacto = ?, status = ?, atualizado_em = datetime('now','localtime') WHERE id = ?",
               (prob, imp, status, risco_id))
    registrar_revisao(risco_id, prob, imp, status, request.form.get("nota", "").strip())
    q = abrir_questao_para_risco(projeto_id, risco_id) if status == "ocorreu" else None
    tocar_projeto(projeto_id)
    db.commit()
    avisar_questao(q)
    flash(f"Revisão de {r['rotulo']} registrada.", "ok")
    return redirect(url_for("incerteza.risco_detalhe", projeto_id=projeto_id, risco_id=risco_id))


@bp.route("/riscos/<int:risco_id>/excluir", methods=["POST"])
def risco_excluir(projeto_id, risco_id):
    p = obter_projeto(projeto_id)
    r = obter_risco(p, risco_id)
    db = get_db()
    db.execute("DELETE FROM risco WHERE id = ?", (risco_id,))
    db.commit()
    flash(f"{r['rotulo']} excluído.", "ok")
    return redirect(url_for("incerteza.riscos", projeto_id=projeto_id))


@bp.route("/outras", methods=["GET", "POST"])
def outras(projeto_id):
    p = obter_projeto(projeto_id)
    db = get_db()
    if request.method == "POST":
        natureza = request.form.get("natureza")
        descricao = request.form.get("descricao", "").strip()
        if natureza not in pmbok.NATUREZAS_POR_CHAVE or not descricao:
            flash("Escolha a natureza e descreva a incerteza.", "erro")
            return redirect(url_for("incerteza.outras", projeto_id=projeto_id))
        validas = {k for k, *_ in pmbok.NATUREZAS_POR_CHAVE[natureza]["respostas"]}
        respostas = ",".join(x for x in request.form.getlist("respostas") if x in validas)
        db.execute("INSERT INTO incerteza (projeto_id, natureza, descricao, respostas, acoes) VALUES (?, ?, ?, ?, ?)",
                   (projeto_id, natureza, descricao, respostas, request.form.get("acoes", "").strip()))
        tocar_projeto(projeto_id)
        db.commit()
        flash("Incerteza registrada.", "ok")
        return redirect(url_for("incerteza.outras", projeto_id=projeto_id) + f"#{natureza}")
    itens = db.execute("SELECT * FROM incerteza WHERE projeto_id = ? ORDER BY status = 'resolvida', id DESC", (projeto_id,)).fetchall()
    por_natureza = {n["chave"]: [] for n in pmbok.NATUREZAS_INCERTEZA}
    for i in itens:
        d = dict(i)
        d["respostas_lista"] = [x for x in (i["respostas"] or "").split(",") if x]
        por_natureza.setdefault(i["natureza"], []).append(d)
    return render_template("incertezas_outras.html", projeto=p, por_natureza=por_natureza, secao="incerteza", sub="outras")


@bp.route("/outras/<int:item_id>", methods=["POST"])
def outra_atualizar(projeto_id, item_id):
    obter_projeto(projeto_id)
    db = get_db()
    item = db.execute("SELECT * FROM incerteza WHERE id = ? AND projeto_id = ?", (item_id, projeto_id)).fetchone()
    if item is None:
        abort(404)
    if request.form.get("acao") == "excluir":
        db.execute("DELETE FROM incerteza WHERE id = ?", (item_id,))
        flash("Incerteza removida.", "ok")
    else:
        validas = {k for k, *_ in pmbok.NATUREZAS_POR_CHAVE[item["natureza"]]["respostas"]}
        status = request.form.get("status") if request.form.get("status") in dict(pmbok.STATUS_INCERTEZA) else item["status"]
        db.execute("UPDATE incerteza SET respostas = ?, acoes = ?, status = ?, atualizado_em = datetime('now','localtime') WHERE id = ?",
                   (",".join(x for x in request.form.getlist("respostas") if x in validas),
                    request.form.get("acoes", "").strip(), status, item_id))
        flash("Incerteza atualizada.", "ok")
    tocar_projeto(projeto_id)
    db.commit()
    return redirect(url_for("incerteza.outras", projeto_id=projeto_id) + f"#{item['natureza']}")
