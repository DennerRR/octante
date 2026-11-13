"""Recursos de PMO (v14): modelos de projeto, portfólio, minhas pendências, revisão do PMO, busca, agenda,
exportação para Excel, nível de exigência e completude dos registros."""
import csv
import io
import re
from datetime import date, datetime, timedelta

from flask import (Blueprint, Response, abort, current_app, flash, g, redirect, render_template, request,
                   send_file, url_for)

import auth
import pmbok
from db import get_db
from util import filtro_projetos, obter_projeto, tocar_projeto

bp = Blueprint("pmo", __name__)

# ------------------------------------------------------------------ modelos de projeto
MODELOS = {
    "": {"nome": "Em branco", "descricao": "Você define tudo."},
    "agil": {
        "nome": "Software ágil (Scrum)", "descricao": "Sprints de 2 semanas, backlog em pontos, entregas periódicas.",
        "abordagem": "adaptativa", "cadencia": "periodica", "unidade_estimativa": "pontos", "limite_wip": 3,
        "definicao_pronto": "Código revisado por outra pessoa\nTestes automatizados passando\nPublicado em homologação\nCritérios de aceite conferidos",
        "riscos": [("Requisitos mudarem com frequência e o escopo crescer sem controle", "Mercado/cliente"),
                   ("Pessoa-chave da equipe sair no meio do projeto", "Equipe"),
                   ("Integração com sistema legado ser mais difícil que o previsto", "Técnico")],
    },
    "hibrido": {
        "nome": "Software híbrido", "descricao": "Fases com marcos de aprovação e construção em iterações.",
        "abordagem": "hibrida", "cadencia": "multiplas", "unidade_estimativa": "pontos", "limite_wip": 3,
        "definicao_pronto": "Código revisado\nTestes passando\nDocumentação mínima atualizada",
        "riscos": [("Aprovação de fase atrasar e travar a equipe", "Partes interessadas"),
                   ("Requisitos da fase de design mudarem durante a construção", "Mercado/cliente"),
                   ("Fornecedor de componente atrasar a entrega", "Fornecedor")],
    },
    "preditivo": {
        "nome": "Implantação/infraestrutura (preditivo)", "descricao": "Escopo estável, cronograma e orçamento definidos antes.",
        "abordagem": "preditiva", "cadencia": "unica", "unidade_estimativa": "dias", "limite_wip": None,
        "definicao_pronto": "Instalado e configurado\nTestado no ambiente de produção\nAceite assinado pelo cliente",
        "riscos": [("Equipamento chegar fora do prazo", "Fornecedor"),
                   ("Janela de manutenção não ser aprovada pela operação", "Partes interessadas"),
                   ("Ambiente real diferente do levantado na fase de design", "Técnico")],
    },
}


def aplicar_modelo(db, projeto_id, chave):
    m = MODELOS.get(chave)
    if not m or not chave:
        return
    db.execute("""UPDATE projeto SET modelo = ?, abordagem = ?, cadencia = ?, unidade_estimativa = ?, limite_wip = ?,
                  definicao_pronto = ? WHERE id = ?""",
               (chave, m["abordagem"], m["cadencia"], m["unidade_estimativa"], m["limite_wip"], m["definicao_pronto"], projeto_id))
    for n, (nome, objetivo, criterios) in enumerate(pmbok.FASES_SUGERIDAS.get(m["abordagem"], []), start=1):
        db.execute("INSERT INTO fase (projeto_id, nome, ordem, objetivo, criterios_saida) VALUES (?, ?, ?, ?, ?)",
                   (projeto_id, nome, n, objetivo, criterios))
    for n, (titulo, fonte) in enumerate(m["riscos"], start=1):
        db.execute("INSERT INTO risco (projeto_id, codigo, titulo, fonte, status) VALUES (?, ?, ?, ?, 'aberto')",
                   (projeto_id, n, titulo, fonte))


# ------------------------------------------------------------------ nível de exigência e completude
def nivel_exigencia():
    r = get_db().execute("SELECT valor FROM configuracao WHERE chave = 'nivel_exigencia'").fetchone()
    return r["valor"] if r else "essencial"


def exigir(tipo, dados, contexto=None):
    """Regras extras do nível 'rigoroso'. Devolve a mensagem de erro ou None."""
    if nivel_exigencia() != "rigoroso":
        return None
    contexto = contexto or {}
    faltam = []
    if tipo == "questao":
        faltam = [n for c, n in (("responsavel", "responsável"), ("prazo", "prazo")) if not dados.get(c)]
    elif tipo == "risco":
        p, i, limite = dados.get("probabilidade"), dados.get("impacto"), contexto.get("limite", 12)
        if p and i and p * i >= limite:
            faltam = [n for c, n in (("responsavel", "responsável"), ("estrategia", "estratégia de resposta")) if not dados.get(c)]
            if faltam:
                return f"Risco alto (pontuação {p * i}) precisa de: {', '.join(faltam)}. Nível de exigência: rigoroso."
    elif tipo == "mudanca":
        faltam = [n for c, n in (("solicitante", "solicitante"), ("justificativa", "justificativa")) if not dados.get(c)]
    elif tipo == "item" and dados.get("status") == "em_andamento":
        if not (dados.get("criterios_aceite") or "").strip():
            return "Antes de começar, escreva os critérios de aceite (definição de preparado). Nível de exigência: rigoroso."
    elif tipo == "parte":
        faltam = ["papel"] if not dados.get("papel") else []
    elif tipo == "abertura":
        faltam = ["patrocinador"] if not dados.get("patrocinador") else []
    return f"Preencha: {', '.join(faltam)} (nível de exigência: rigoroso)." if faltam else None


CAMPOS_COMPLETUDE = {
    "risco": [("causa", "causa"), ("efeito", "efeito"), ("probabilidade", "probabilidade"), ("impacto", "impacto"),
              ("responsavel", "responsável"), ("estrategia", "estratégia"), ("plano_resposta", "plano de resposta"), ("gatilho", "gatilho")],
    "questao": [("descricao", "descrição"), ("responsavel", "responsável"), ("prazo", "prazo"), ("prioridade", "prioridade")],
    "mudanca": [("solicitante", "solicitante"), ("justificativa", "justificativa"), ("imp_escopo", "impacto no escopo"),
                ("imp_cronograma", "impacto no cronograma"), ("imp_custo", "impacto no custo"), ("imp_riscos", "impacto nos riscos")],
    "item": [("descricao", "descrição"), ("criterios_aceite", "critérios de aceite"), ("valor", "valor"), ("estimativa", "estimativa"),
             ("responsavel", "responsável")],
    "parte": [("papel", "papel"), ("contato", "contato"), ("poder", "poder"), ("interesse", "interesse"), ("atitude", "atitude"),
              ("engajamento_atual", "engajamento atual"), ("engajamento_desejado", "engajamento desejado"), ("estrategia", "estratégia")],
}


def completude(tipo, registro):
    campos = CAMPOS_COMPLETUDE.get(tipo, [])
    if not campos or registro is None:
        return None
    reg = dict(registro)
    vazio = lambda v: v is None or v == "" or v == "desconhecida"  # noqa: E731
    faltam = [nome for c, nome in campos if c in reg and vazio(reg[c])]
    considerados = [c for c, _ in campos if c in reg]
    if not considerados:
        return None
    return {"pct": round(100 * (len(considerados) - len(faltam)) / len(considerados)), "faltam": faltam}


@bp.app_context_processor
def contexto_pmo():
    return {"completude": completude, "nivel_exigencia": nivel_exigencia}


@bp.route("/admin/exigencia", methods=["POST"])
def definir_exigencia():
    auth.exigir_admin()
    valor = request.form.get("nivel")
    if valor in ("essencial", "rigoroso"):
        db = get_db()
        db.execute("INSERT INTO configuracao (chave, valor) VALUES ('nivel_exigencia', ?) "
                   "ON CONFLICT(chave) DO UPDATE SET valor = excluded.valor", (valor,))
        db.commit()
        flash("Nível de exigência: " + ("rigoroso (mais campos obrigatórios)." if valor == "rigoroso" else "essencial (padrão)."), "ok")
    return redirect(request.referrer or url_for("pmo.portfolio"))


# ------------------------------------------------------------------ portfólio
@bp.route("/portfolio")
def portfolio():
    import guia
    import medicao
    from app import listar_partes, obter_abertura
    onde, args = filtro_projetos()
    linhas = []
    for p in get_db().execute(f"SELECT * FROM projeto p WHERE {onde} ORDER BY p.nome", args).fetchall():
        sem = medicao.semaforo(p)
        fases = guia.fluxo_do_projeto(p, listar_partes(p["id"]), obter_abertura(p["id"]))
        prox = next(((f, e) for f in fases for e in f["etapas"] if e["proximo"]), (None, None))
        criticos = sum(1 for s in sem if s["status"] == "critico")
        atencao = sum(1 for s in sem if s["status"] == "atencao")
        linhas.append({"p": p, "sem": sem, "fase": prox[0], "etapa": prox[1], "criticos": criticos, "atencao": atencao,
                       "pendentes": get_db().execute("SELECT COUNT(*) FROM revisao_pmo WHERE projeto_id = ? AND status = 'pendente'",
                                                     (p["id"],)).fetchone()[0]})
    ordem = {"ativo": 0, "encerrado": 1, "cancelado": 2}
    linhas.sort(key=lambda l: (ordem.get(l["p"]["situacao"], 3), -l["criticos"], -l["atencao"], l["p"]["nome"].lower()))
    return render_template("portfolio.html", linhas=linhas, nivel=nivel_exigencia())


# ------------------------------------------------------------------ minhas pendências
def _nomes_do_usuario(u):
    nomes = {u["nome"].strip().lower(), u["login"].strip().lower(), u["nome"].split()[0].strip().lower()}
    for (n,) in get_db().execute("SELECT nome FROM membro WHERE usuario_id = ?", (u["id"],)):
        nomes.add(n.strip().lower())
    return [n for n in nomes if n]


def _e_meu(responsavel, nomes):
    r = (responsavel or "").strip().lower()
    if not r:
        return False
    r_base = re.sub(r"\s*\(.*\)$", "", r)  # "Ana (desenvolvedora)" -> "ana"
    return any(r == n or r_base == n or r_base.split()[0] == n for n in nomes)


@bp.route("/minhas-pendencias")
def pendencias():
    u = g.get("usuario")
    if u is None:
        flash("Entre com seu usuário para ver suas pendências.", "erro")
        return redirect(url_for("inicio"))
    nomes = _nomes_do_usuario(u)
    onde, args = filtro_projetos("q.projeto_id")
    db = get_db()
    hoje = date.today().isoformat()
    itens = []
    consultas = [
        ("Questão", "Q", f"SELECT q.*, p.nome AS projeto FROM questao q JOIN projeto p ON p.id = q.projeto_id WHERE q.status != 'resolvida' AND p.situacao = 'ativo' AND {onde}",
         lambda r: url_for("trabalho.questao", projeto_id=r["projeto_id"], questao_id=r["id"]), "prazo"),
        ("Risco", "R", f"SELECT q.*, p.nome AS projeto FROM risco q JOIN projeto p ON p.id = q.projeto_id WHERE q.status IN ('aberto', 'em_resposta') AND p.situacao = 'ativo' AND {onde}",
         lambda r: url_for("incerteza.risco_detalhe", projeto_id=r["projeto_id"], risco_id=r["id"]), None),
        ("Item", "I", f"SELECT q.*, p.nome AS projeto FROM item q JOIN projeto p ON p.id = q.projeto_id WHERE q.status IN ('a_fazer', 'em_andamento', 'concluido') AND p.situacao = 'ativo' AND {onde}",
         lambda r: url_for("entrega.item", projeto_id=r["projeto_id"], item_id=r["id"]), "fim_planejado"),
    ]
    for tipo, prefixo, sql, link, campo_prazo in consultas:
        for r in db.execute(sql, args):
            if _e_meu(r["responsavel"], nomes):
                prazo = r[campo_prazo] if campo_prazo else None
                itens.append({"tipo": tipo, "rotulo": f"{prefixo}-{r['codigo']}", "titulo": r["titulo"], "projeto": r["projeto"],
                              "link": link(r), "prazo": prazo, "atrasado": bool(prazo and prazo < hoje), "status": r["status"]})
    itens.sort(key=lambda i: (not i["atrasado"], i["prazo"] or "9999", i["projeto"]))
    revisoes = db.execute(f"SELECT r.*, p.nome AS projeto FROM revisao_pmo r JOIN projeto p ON p.id = r.projeto_id "
                          f"WHERE r.solicitado_por = ? AND r.status != 'pendente' AND r.decidido_em >= date('now', '-30 days') "
                          f"ORDER BY r.decidido_em DESC", (u["nome"],)).fetchall()
    return render_template("pendencias.html", itens=itens, revisoes=revisoes, nomes=nomes)


# ------------------------------------------------------------------ revisão do PMO
@bp.route("/p/<int:projeto_id>/revisao", methods=["POST"])
def pedir_revisao(projeto_id):
    obter_projeto(projeto_id)
    f = request.form
    tabela, rid = f.get("tabela", ""), f.get("registro_id", type=int)
    if tabela not in ("abertura", "risco", "mudanca", "item", "relatorio_status", "questao") or rid is None:
        abort(400)
    db = get_db()
    if db.execute("SELECT 1 FROM revisao_pmo WHERE projeto_id = ? AND tabela = ? AND registro_id = ? AND status = 'pendente'",
                  (projeto_id, tabela, rid)).fetchone():
        flash("Este registro já está aguardando revisão do PMO.", "erro")
    else:
        destino = f.get("link", "")
        destino = destino if destino.startswith("/p/") else ""
        db.execute("INSERT INTO revisao_pmo (projeto_id, tabela, registro_id, titulo, link, solicitado_por, mensagem) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (projeto_id, tabela, rid, f.get("titulo", "")[:200], destino,
                    g.usuario["nome"] if g.get("usuario") else "", f.get("mensagem", "").strip()[:1000]))
        db.commit()
        flash("Enviado para revisão do PMO. Você verá a resposta em “Minhas pendências”.", "ok")
    return redirect(request.referrer or url_for("projeto", projeto_id=projeto_id))


@bp.route("/revisoes", methods=["GET", "POST"])
def revisoes():
    auth.exigir_admin()
    db = get_db()
    if request.method == "POST":
        r = db.execute("SELECT * FROM revisao_pmo WHERE id = ?", (request.form.get("revisao_id", type=int),)).fetchone()
        decisao = request.form.get("decisao")
        comentario = request.form.get("comentario", "").strip()
        if r is None or decisao not in ("aprovada", "devolvida"):
            abort(400)
        if decisao == "devolvida" and not comentario:
            flash("Ao devolver, explique o que precisa ser ajustado.", "erro")
        else:
            db.execute("UPDATE revisao_pmo SET status = ?, comentario = ?, revisor = ?, decidido_em = datetime('now','localtime') WHERE id = ?",
                       (decisao, comentario, g.usuario["nome"] if g.get("usuario") else "PMO", r["id"]))
            db.commit()
            flash("Revisão registrada.", "ok")
        return redirect(url_for("pmo.revisoes"))
    pendentes = db.execute("SELECT r.*, p.nome AS projeto FROM revisao_pmo r JOIN projeto p ON p.id = r.projeto_id "
                           "WHERE r.status = 'pendente' ORDER BY r.solicitado_em").fetchall()
    recentes = db.execute("SELECT r.*, p.nome AS projeto FROM revisao_pmo r JOIN projeto p ON p.id = r.projeto_id "
                          "WHERE r.status != 'pendente' ORDER BY r.decidido_em DESC LIMIT 30").fetchall()
    return render_template("revisoes.html", pendentes=pendentes, recentes=recentes)


def revisoes_do_registro(projeto_id, tabela, registro_id):
    return get_db().execute("SELECT * FROM revisao_pmo WHERE projeto_id = ? AND tabela = ? AND registro_id = ? ORDER BY id DESC LIMIT 5",
                            (projeto_id, tabela, registro_id)).fetchall()


def url_exemplo():
    """Mesma tela no projeto de exemplo (AgendaFácil), quando ele existe e o usuário pode vê-lo."""
    from util import pode_acessar
    va = request.view_args or {}
    if set(va) != {"projeto_id"} or not request.endpoint:
        return None
    ex = get_db().execute("SELECT id FROM projeto WHERE nome LIKE '%AgendaFácil%' ORDER BY id LIMIT 1").fetchone()
    if not ex or ex["id"] == va["projeto_id"] or not pode_acessar(ex["id"]):
        return None
    return url_for(request.endpoint, projeto_id=ex["id"])


def contar_revisoes():
    u = g.get("usuario")
    if u is None or not u["admin"]:
        return 0
    return get_db().execute("SELECT COUNT(*) FROM revisao_pmo WHERE status = 'pendente'").fetchone()[0]


bp.app_context_processor(lambda: {"revisoes_do_registro": revisoes_do_registro, "contar_revisoes": contar_revisoes,
                                   "url_exemplo": url_exemplo})


# ------------------------------------------------------------------ busca
BUSCA = [
    ("risco", "Risco", "R", "titulo", "incerteza.risco_detalhe", "risco_id"),
    ("questao", "Questão", "Q", "titulo", "trabalho.questao", "questao_id"),
    ("mudanca", "Mudança", "M", "titulo", "trabalho.mudanca", "mudanca_id"),
    ("item", "Item de escopo", "I", "titulo", "entrega.item", "item_id"),
    ("parte_interessada", "Parte interessada", None, "nome", "parte_detalhe", "parte_id"),
    ("licao", "Lição aprendida", None, "descricao", "trabalho.licoes", None),
    ("decisao", "Decisão", None, "titulo", "principios.decisoes", None),
    ("premissa", "Premissa", None, "descricao", "principios.decisoes", None),
    ("aquisicao", "Aquisição", "A", "item", "suprimentos.painel", None),
]


@bp.route("/busca")
def busca():
    q = request.args.get("q", "").strip()
    resultados = []
    if len(q) >= 2:
        onde, args = filtro_projetos("t.projeto_id")
        termo = "%" + q.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_") + "%"
        db = get_db()
        for p in db.execute(f"SELECT id, nome FROM projeto t WHERE nome LIKE ? ESCAPE '\\' AND {onde.replace('t.projeto_id', 't.id')}", [termo] + args):
            resultados.append({"tipo": "Projeto", "titulo": p["nome"], "projeto": "", "link": url_for("projeto", projeto_id=p["id"])})
        for tabela, tipo, prefixo, campo, endpoint, arg in BUSCA:
            sql = (f"SELECT t.*, p.nome AS projeto FROM {tabela} t JOIN projeto p ON p.id = t.projeto_id "
                   f"WHERE t.{campo} LIKE ? ESCAPE '\\' AND {onde} LIMIT 20")
            for r in db.execute(sql, [termo] + args):
                kw = {"projeto_id": r["projeto_id"]}
                if arg:
                    kw[arg] = r["id"]
                rot = f"{prefixo}-{r['codigo']} " if prefixo and "codigo" in r.keys() else ""
                resultados.append({"tipo": tipo, "titulo": rot + (r[campo] or "")[:120], "projeto": r["projeto"],
                                   "link": url_for(endpoint, **kw)})
    return render_template("busca.html", q=q, resultados=resultados[:150])


# ------------------------------------------------------------------ agenda
def eventos_do_projeto(p):
    db, pid = get_db(), p["id"]
    ev = []

    def add(data, tipo, texto, link, feito=False):
        if data:
            ev.append({"data": str(data)[:10], "tipo": tipo, "texto": texto, "link": link, "feito": feito})
    for q in db.execute("SELECT * FROM questao WHERE projeto_id = ?", (pid,)):
        add(q["prazo"], "Questão", f"Q-{q['codigo']} {q['titulo']}", url_for("trabalho.questao", projeto_id=pid, questao_id=q["id"]), q["status"] == "resolvida")
    for it in db.execute("SELECT * FROM iteracao WHERE projeto_id = ?", (pid,)):
        add(it["inicio"], "Iteração", f"Início: {it['nome']}", url_for("medicao.cronograma", projeto_id=pid))
        add(it["fim"], "Iteração", f"Fim: {it['nome']}" + (f" (meta: {it['meta']})" if it["meta"] else ""), url_for("medicao.cronograma", projeto_id=pid))
    for i in db.execute("SELECT * FROM item WHERE projeto_id = ? AND fim_planejado IS NOT NULL", (pid,)):
        add(i["fim_planejado"], "Entrega", f"I-{i['codigo']} {i['titulo']}", url_for("entrega.item", projeto_id=pid, item_id=i["id"]), i["status"] in ("concluido", "aceito"))
    for a in db.execute("SELECT * FROM aquisicao WHERE projeto_id = ?", (pid,)):
        add(a["necessario_em"], "Compra", f"A-{a['codigo']} necessária: {a['item']}", url_for("suprimentos.painel", projeto_id=pid), a["status"] in ("entregue", "encerrada", "cancelada"))
        add(a["entrega_prevista"], "Compra", f"A-{a['codigo']} entrega do fornecedor", url_for("suprimentos.painel", projeto_id=pid), a["status"] in ("entregue", "encerrada", "cancelada"))
    for pr in db.execute("SELECT * FROM premissa WHERE projeto_id = ?", (pid,)):
        add(pr["validar_ate"], "Premissa", f"Validar: {pr['descricao']}", url_for("principios.decisoes", projeto_id=pid), pr["status"] != "a_validar")
    for d in db.execute("SELECT * FROM decisao WHERE projeto_id = ?", (pid,)):
        add(d["revisar_em"], "Decisão", f"Revisar: {d['titulo']}", url_for("principios.decisoes", projeto_id=pid))
    for b in db.execute("SELECT * FROM beneficio WHERE projeto_id = ?", (pid,)):
        add(b["data_prevista"], "Benefício", f"Medir: {b['descricao']}", url_for("entrega.beneficios", projeto_id=pid), bool(b["resultado"]))
    dias = p["revisao_risco_dias"] or 14
    for r in db.execute("SELECT * FROM risco WHERE projeto_id = ? AND status IN ('aberto', 'em_resposta')", (pid,)):
        base = r["revisado_em"] or r["identificado_em"]
        if base:
            proxima = datetime.fromisoformat(base[:10]).date() + timedelta(days=dias)
            add(proxima.isoformat(), "Risco", f"Revisar R-{r['codigo']} {r['titulo']}", url_for("incerteza.risco_detalhe", projeto_id=pid, risco_id=r["id"]))
    add(p["data_fim_planejada"], "Marco", "Fim planejado do projeto", url_for("medicao.cronograma", projeto_id=pid))
    hoje = date.today().isoformat()
    for e in ev:
        e["atrasado"] = not e["feito"] and e["data"] < hoje
    return sorted(ev, key=lambda e: e["data"])


@bp.route("/p/<int:projeto_id>/agenda")
def agenda(projeto_id):
    p = obter_projeto(projeto_id)
    ev = eventos_do_projeto(p)
    hoje = date.today().isoformat()
    atrasados = [e for e in ev if e["atrasado"]]
    proximos = [e for e in ev if e["data"] >= hoje and not e["feito"]]
    passados = [e for e in ev if e["data"] < hoje and not e["atrasado"]][-15:]
    return render_template("agenda.html", projeto=p, atrasados=atrasados, proximos=proximos, passados=passados, secao="agenda")


@bp.route("/p/<int:projeto_id>/agenda.ics")
def agenda_ics(projeto_id):
    p = obter_projeto(projeto_id)
    esc = lambda t: t.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", " ")  # noqa: E731
    linhas = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Octante//PT-BR", f"X-WR-CALNAME:{esc(p['nome'])}"]
    for n, e in enumerate(eventos_do_projeto(p)):
        if e["feito"]:
            continue
        d = e["data"].replace("-", "")
        linhas += ["BEGIN:VEVENT", f"UID:gp7-{projeto_id}-{n}-{d}@gestor", f"DTSTAMP:{datetime.now():%Y%m%dT%H%M%S}",
                   f"DTSTART;VALUE=DATE:{d}", f"SUMMARY:{esc(e['tipo'] + ': ' + e['texto'])}", "END:VEVENT"]
    linhas.append("END:VCALENDAR")
    return Response("\r\n".join(linhas), mimetype="text/calendar",
                    headers={"Content-Disposition": f"attachment; filename=agenda-projeto-{projeto_id}.ics"})


# ------------------------------------------------------------------ exportação (Excel)
REGISTROS = {
    "riscos": ("Registro de riscos", "risco", [("codigo", "Código"), ("titulo", "Risco"), ("tipo", "Tipo"), ("causa", "Causa"), ("efeito", "Efeito"),
               ("probabilidade", "Probabilidade"), ("impacto", "Impacto"), ("responsavel", "Responsável"), ("estrategia", "Estratégia"),
               ("plano_resposta", "Plano de resposta"), ("status", "Status"), ("identificado_em", "Identificado em"), ("revisado_em", "Revisado em")]),
    "questoes": ("Registro de questões", "questao", [("codigo", "Código"), ("titulo", "Questão"), ("prioridade", "Prioridade"), ("responsavel", "Responsável"),
                 ("prazo", "Prazo"), ("status", "Status"), ("resolucao", "Resolução"), ("criado_em", "Criada em")]),
    "mudancas": ("Registro de mudanças", "mudanca", [("codigo", "Código"), ("titulo", "Mudança"), ("solicitante", "Solicitante"), ("justificativa", "Justificativa"),
                 ("status", "Status"), ("decidido_por", "Decidido por"), ("decidido_em", "Decidido em")]),
    "partes": ("Registro das partes interessadas", "parte_interessada", [("nome", "Nome"), ("papel", "Papel"), ("organizacao", "Organização"),
               ("categoria", "Categoria"), ("poder", "Poder"), ("interesse", "Interesse"), ("atitude", "Atitude"),
               ("engajamento_atual", "Engajamento atual"), ("engajamento_desejado", "Engajamento desejado"), ("estrategia", "Estratégia")]),
    "backlog": ("Escopo e backlog", "item", [("codigo", "Código"), ("titulo", "Item"), ("tipo", "Tipo"), ("moscow", "MoSCoW"), ("valor", "Valor"),
                ("estimativa", "Estimativa"), ("status", "Status"), ("responsavel", "Responsável"), ("criterios_aceite", "Critérios de aceite")]),
    "licoes": ("Lições aprendidas", "licao", [("tipo", "Tipo"), ("descricao", "Lição"), ("recomendacao", "Recomendação"), ("dominio", "Domínio"), ("criado_em", "Data")]),
}


def _seguro_planilha(v):
    """Evita injeção de fórmulas ao abrir no Excel (=, +, -, @ no começo da célula)."""
    if isinstance(v, str) and v[:1] in ("=", "+", "-", "@", "\t", "\r"):
        return "'" + v
    return v


@bp.route("/p/<int:projeto_id>/exportar/<registro>")
def exportar(projeto_id, registro):
    p = obter_projeto(projeto_id)
    if registro not in REGISTROS:
        abort(404)
    titulo, tabela, colunas = REGISTROS[registro]
    existentes = {r[1] for r in get_db().execute(f"PRAGMA table_info({tabela})")}
    colunas = [(c, n) for c, n in colunas if c in existentes]
    ordem = "codigo" if "codigo" in existentes else "id"
    linhas = get_db().execute(f"SELECT * FROM {tabela} WHERE projeto_id = ? ORDER BY {ordem}", (projeto_id,)).fetchall()
    nome = re.sub(r"[^a-z0-9]+", "-", f"{registro}-{p['nome']}".lower()).strip("-")[:60]
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font, PatternFill
        wb = Workbook()
        ws = wb.active
        ws.title = titulo[:31]
        ws.append([n for _, n in colunas])
        for cel in ws[1]:
            cel.font = Font(bold=True, color="FFFFFF")
            cel.fill = PatternFill("solid", fgColor="5B33A8")
        for r in linhas:
            ws.append([_seguro_planilha(r[c]) for c, _ in colunas])
        for col in ws.columns:
            ws.column_dimensions[col[0].column_letter].width = min(60, max(10, *(len(str(c.value or "")) for c in col)) + 2)
        ws.freeze_panes = "A2"
        buf = io.BytesIO()
        wb.save(buf)
        buf.seek(0)
        return send_file(buf, as_attachment=True, download_name=nome + ".xlsx",
                         mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except ImportError:  # sem openpyxl: CSV que o Excel abre em português
        buf = io.StringIO()
        w = csv.writer(buf, delimiter=";")
        w.writerow([n for _, n in colunas])
        for r in linhas:
            w.writerow([_seguro_planilha(r[c]) for c, _ in colunas])
        return Response("\ufeff" + buf.getvalue(), mimetype="text/csv",
                        headers={"Content-Disposition": f"attachment; filename={nome}.csv"})
