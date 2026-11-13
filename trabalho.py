"""Domínio de desempenho Trabalho do Projeto (PMBOK 7, seção 2.5).

Registro de questões (issue log), registro de mudanças (change log) e
registro de lições aprendidas (2.5.8), além do painel do domínio.
"""
from datetime import date, timedelta

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

import pmbok
from db import get_db
from util import decimal, inteiro, obter_projeto, tocar_projeto

bp = Blueprint("trabalho", __name__, url_prefix="/p/<int:projeto_id>/trabalho")

DIAS_DECISAO_PENDENTE = 7
CAMPOS_IMPACTO = [c for c, *_ in pmbok.IMPACTOS_MUDANCA]


# --------------------------------------------------------------------------
# Consultas
# --------------------------------------------------------------------------
def _parte_valida(projeto_id, parte_id):
    if parte_id is None:
        return None
    ok = get_db().execute("SELECT 1 FROM parte_interessada WHERE id = ? AND projeto_id = ?", (parte_id, projeto_id)).fetchone()
    return parte_id if ok else None


def _partes(projeto_id):
    return get_db().execute(
        "SELECT id, nome FROM parte_interessada WHERE projeto_id = ? AND ativa = 1 ORDER BY nome", (projeto_id,)
    ).fetchall()


def enriquecer_questao(row):
    q = dict(row)
    q["rotulo"] = f"Q-{q['codigo']}"
    q["aberta"] = q["status"] != "resolvida"
    hoje = date.today().isoformat()
    q["atrasada"] = q["aberta"] and bool(q["prazo"]) and q["prazo"] < hoje
    fim = q["resolvido_em"] or hoje
    q["dias_aberta"] = (date.fromisoformat(fim[:10]) - date.fromisoformat(q["criado_em"][:10])).days
    return q


def listar_questoes(projeto_id):
    rows = get_db().execute(
        """SELECT q.*, s.nome AS parte_nome, r.codigo AS risco_codigo
           FROM questao q
           LEFT JOIN parte_interessada s ON s.id = q.parte_id
           LEFT JOIN risco r ON r.id = q.risco_id
           WHERE q.projeto_id = ?""", (projeto_id,)
    ).fetchall()
    ordem_prio = {"alta": 0, "media": 1, "baixa": 2}
    qs = [enriquecer_questao(r) for r in rows]
    qs.sort(key=lambda q: (not q["aberta"], not q["atrasada"], ordem_prio.get(q["prioridade"], 3), q["prazo"] or "9999", q["codigo"]))
    return qs


def enriquecer_mudanca(row, projeto):
    m = dict(row)
    m["rotulo"] = f"M-{m['codigo']}"
    m["impactos_avaliados"] = sum(1 for c in CAMPOS_IMPACTO if (m.get(c) or "").strip())
    m["pendente"] = m["status"] in pmbok.STATUS_MUDANCA_PENDENTES
    limite = (date.today() - timedelta(days=DIAS_DECISAO_PENDENTE)).isoformat()
    m["decisao_atrasada"] = m["pendente"] and m["criado_em"][:10] < limite
    m["exige_avaliacao"] = projeto["abordagem"] != "adaptativa"
    return m


def listar_mudancas(projeto):
    rows = get_db().execute(
        """SELECT m.*, s.nome AS parte_nome FROM mudanca m LEFT JOIN parte_interessada s ON s.id = m.parte_id
           WHERE m.projeto_id = ? ORDER BY m.codigo DESC""", (projeto["id"],)
    ).fetchall()
    return [enriquecer_mudanca(r, projeto) for r in rows]


def listar_licoes(projeto_id):
    return get_db().execute(
        """SELECT l.*, q.codigo AS questao_codigo FROM licao l LEFT JOIN questao q ON q.id = l.questao_id
           WHERE l.projeto_id = ? ORDER BY l.data DESC, l.id DESC""", (projeto_id,)
    ).fetchall()


def resumo_trabalho(projeto):
    qs = listar_questoes(projeto["id"])
    ms = listar_mudancas(projeto)
    resolvidas = [q for q in qs if not q["aberta"]]
    return {
        "questoes_abertas": sum(q["aberta"] for q in qs),
        "questoes_atrasadas": sum(q["atrasada"] for q in qs),
        "questoes_total": len(qs),
        "tempo_medio_resolucao": (sum(q["dias_aberta"] for q in resolvidas) / len(resolvidas)) if resolvidas else None,
        "mudancas_pendentes": sum(m["pendente"] for m in ms),
        "mudancas_aprovadas": sum(m["status"] in ("aprovada", "implementada") for m in ms),
        "mudancas_rejeitadas": sum(m["status"] == "rejeitada" for m in ms),
        "mudancas_total": len(ms),
        "licoes": get_db().execute("SELECT COUNT(*) FROM licao WHERE projeto_id = ?", (projeto["id"],)).fetchone()[0],
    }


def gerar_alertas_trabalho(projeto):
    pid = projeto["id"]
    alertas = []
    for q in listar_questoes(pid):
        if not q["aberta"]:
            continue
        link = url_for("trabalho.questao", projeto_id=pid, questao_id=q["id"])
        if q["atrasada"]:
            alertas.append(("alto", f"{q['rotulo']} ({q['titulo']}) passou do prazo ({date.fromisoformat(q['prazo']).strftime('%d/%m/%Y')}).", link))
        if not q["responsavel"] and not q["parte_nome"]:
            alertas.append(("medio", f"{q['rotulo']} ({q['titulo']}) não tem responsável.", link))
        if q["prioridade"] == "alta" and not q["prazo"]:
            alertas.append(("medio", f"{q['rotulo']} ({q['titulo']}) tem prioridade alta e nenhum prazo.", link))
    for m in listar_mudancas(projeto):
        link = url_for("trabalho.mudanca", projeto_id=pid, mudanca_id=m["id"])
        if m["decisao_atrasada"]:
            alertas.append(("medio", f"{m['rotulo']} ({m['titulo']}) aguarda decisão há mais de {DIAS_DECISAO_PENDENTE} dias.", link))
        if m["status"] in ("aprovada", "implementada") and not m["comunicada"]:
            alertas.append(("medio", f"{m['rotulo']} ({m['titulo']}) foi aprovada e ainda não foi comunicada às partes interessadas.", link))
    return [{"nivel": n, "texto": t, "link": l} for n, t, l in alertas]


def indicadores(projeto):
    r = resumo_trabalho(projeto)
    ind = [f"Questões: {r['questoes_abertas']} abertas ({r['questoes_atrasadas']} atrasadas) de {r['questoes_total']} registradas."]
    if r["tempo_medio_resolucao"] is not None:
        ind.append(f"Tempo médio de resolução: {r['tempo_medio_resolucao']:.1f} dias.")
    ind.append(f"Mudanças: {r['mudancas_total']} registradas, {r['mudancas_aprovadas']} aprovadas, "
               f"{r['mudancas_rejeitadas']} rejeitadas e {r['mudancas_pendentes']} aguardando decisão.")
    decididas = [m for m in listar_mudancas(projeto) if m["status"] in ("aprovada", "rejeitada", "implementada")]
    if decididas:
        completas = sum(1 for m in decididas if m["impactos_avaliados"] == len(CAMPOS_IMPACTO))
        ind.append(f"{completas} de {len(decididas)} mudanças decididas com avaliação holística completa (6 dimensões).")
    ind.append(f"{r['licoes']} lições aprendidas registradas.")
    return ind


def mudancas_por_parte(projeto_id):
    """Tabela 2-2: muitas mudanças podem indicar partes interessadas desalinhadas."""
    return get_db().execute(
        """SELECT s.nome, COUNT(*) AS n FROM mudanca m JOIN parte_interessada s ON s.id = m.parte_id
           WHERE m.projeto_id = ? GROUP BY s.id ORDER BY n DESC""", (projeto_id,)
    ).fetchall()


# --------------------------------------------------------------------------
# Painel
# --------------------------------------------------------------------------
@bp.route("")
def painel(projeto_id):
    p = obter_projeto(projeto_id)
    qs = listar_questoes(projeto_id)
    ms = listar_mudancas(p)
    return render_template(
        "trabalho_painel.html", projeto=p, resumo=resumo_trabalho(p), questoes=[q for q in qs if q["aberta"]][:8],
        mudancas=[m for m in ms if m["pendente"] or (m["status"] == "aprovada")][:8],
        licoes=listar_licoes(projeto_id)[:5], alertas=gerar_alertas_trabalho(p),
        secao="trabalho", sub="painel",
    )


# --------------------------------------------------------------------------
# Questões
# --------------------------------------------------------------------------
def _ler_questao(projeto_id):
    f = request.form
    prioridade = f.get("prioridade") if f.get("prioridade") in dict(pmbok.PRIORIDADES) else "media"
    status = f.get("status") if f.get("status") in dict(pmbok.STATUS_QUESTAO) else "aberta"
    prazo = f.get("prazo") or None
    if prazo:
        try:
            date.fromisoformat(prazo)
        except ValueError:
            prazo = None
    risco_id = inteiro(f.get("risco_id"), 1, 10**9)
    if risco_id and not get_db().execute("SELECT 1 FROM risco WHERE id = ? AND projeto_id = ?", (risco_id, projeto_id)).fetchone():
        risco_id = None
    return {
        "titulo": f.get("titulo", "").strip(), "descricao": f.get("descricao", "").strip(),
        "prioridade": prioridade, "responsavel": f.get("responsavel", "").strip(),
        "parte_id": _parte_valida(projeto_id, inteiro(f.get("parte_id"), 1, 10**9)),
        "risco_id": risco_id, "prazo": prazo, "status": status, "resolucao": f.get("resolucao", "").strip(),
        "reserva_usada_custo": decimal(f.get("reserva_usada_custo")),
        "reserva_usada_dias": inteiro(f.get("reserva_usada_dias"), 0, 100000),
    }


def _riscos_select(projeto_id):
    return get_db().execute("SELECT id, codigo, titulo FROM risco WHERE projeto_id = ? ORDER BY codigo", (projeto_id,)).fetchall()


@bp.route("/questoes")
def questoes(projeto_id):
    p = obter_projeto(projeto_id)
    filtro = request.args.get("status", "abertas")
    qs = listar_questoes(projeto_id)
    total = len(qs)
    if filtro == "abertas":
        qs = [q for q in qs if q["aberta"]]
    elif filtro in dict(pmbok.STATUS_QUESTAO):
        qs = [q for q in qs if q["status"] == filtro]
    return render_template("questoes.html", projeto=p, questoes=qs, total=total, filtro=filtro, secao="trabalho", sub="questoes")


@bp.route("/questoes/nova", methods=["GET", "POST"])
def questao_nova(projeto_id):
    p = obter_projeto(projeto_id)
    if request.method == "POST":
        dados = _ler_questao(projeto_id)
        import pmo
        erro_q = "Descreva a questão no campo título." if not dados["titulo"] else pmo.exigir("questao", dados)
        if erro_q:
            flash(erro_q, "erro")
            return render_template("questao_form.html", projeto=p, q=dados, novo=True, partes=_partes(projeto_id),
                                   riscos=_riscos_select(projeto_id), licoes=[], secao="trabalho", sub="questoes")
        if dados["status"] == "resolvida":
            dados["resolvido_em"] = date.today().isoformat()
        db = get_db()
        codigo = db.execute("SELECT COALESCE(MAX(codigo), 0) + 1 FROM questao WHERE projeto_id = ?", (projeto_id,)).fetchone()[0]
        cols = list(dados)
        cur = db.execute(f"INSERT INTO questao (projeto_id, codigo, {', '.join(cols)}) VALUES (?, ?, {', '.join('?' for _ in cols)})",
                         [projeto_id, codigo] + [dados[c] for c in cols])
        tocar_projeto(projeto_id)
        db.commit()
        flash(f"Q-{codigo} registrada.", "ok")
        return redirect(url_for("trabalho.questao", projeto_id=projeto_id, questao_id=cur.lastrowid))
    return render_template("questao_form.html", projeto=p, q={"prioridade": "media", "status": "aberta"}, novo=True,
                           partes=_partes(projeto_id), riscos=_riscos_select(projeto_id), licoes=[],
                           secao="trabalho", sub="questoes")


@bp.route("/questoes/<int:questao_id>", methods=["GET", "POST"])
def questao(projeto_id, questao_id):
    p = obter_projeto(projeto_id)
    db = get_db()
    row = db.execute(
        """SELECT q.*, s.nome AS parte_nome, r.codigo AS risco_codigo FROM questao q
           LEFT JOIN parte_interessada s ON s.id = q.parte_id LEFT JOIN risco r ON r.id = q.risco_id
           WHERE q.id = ? AND q.projeto_id = ?""", (questao_id, projeto_id)
    ).fetchone()
    if row is None:
        abort(404)
    if request.method == "POST":
        if request.form.get("acao") == "excluir":
            db.execute("DELETE FROM questao WHERE id = ?", (questao_id,))
            db.commit()
            flash(f"Q-{row['codigo']} excluída.", "ok")
            return redirect(url_for("trabalho.questoes", projeto_id=projeto_id))
        dados = _ler_questao(projeto_id)
        import pmo
        erro_q = "Descreva a questão no campo título." if not dados["titulo"] else pmo.exigir("questao", dados)
        if erro_q:
            flash(erro_q, "erro")
            return redirect(url_for("trabalho.questao", projeto_id=projeto_id, questao_id=questao_id))
        if dados["status"] == "resolvida" and not dados["resolucao"]:
            flash("Para marcar como resolvida, descreva a resolução.", "erro")
            dados["status"] = row["status"] if row["status"] != "resolvida" else "em_andamento"
        if dados["status"] == "resolvida":
            dados["resolvido_em"] = row["resolvido_em"] or date.today().isoformat()
        else:
            dados["resolvido_em"] = None
        db.execute("UPDATE questao SET " + ", ".join(f"{c} = ?" for c in dados)
                   + ", atualizado_em = datetime('now','localtime') WHERE id = ?", list(dados.values()) + [questao_id])
        tocar_projeto(projeto_id)
        db.commit()
        if dados["status"] == "resolvida" and row["status"] != "resolvida":
            flash(f"Q-{row['codigo']} resolvida. Há uma lição a registrar?", "ok")
        else:
            flash(f"Q-{row['codigo']} atualizada.", "ok")
        return redirect(url_for("trabalho.questao", projeto_id=projeto_id, questao_id=questao_id))
    q = enriquecer_questao(row)
    licoes = db.execute("SELECT * FROM licao WHERE questao_id = ? ORDER BY data DESC", (questao_id,)).fetchall()
    return render_template("questao_form.html", projeto=p, q=q, novo=False, partes=_partes(projeto_id),
                           riscos=_riscos_select(projeto_id), licoes=licoes, secao="trabalho", sub="questoes")


# --------------------------------------------------------------------------
# Mudanças
# --------------------------------------------------------------------------
def _ler_mudanca(projeto_id):
    f = request.form
    dados = {c: f.get(c, "").strip() for c in ["titulo", "descricao", "justificativa", "solicitante", "decidido_por", "notas_decisao"] + CAMPOS_IMPACTO}
    dados["parte_id"] = _parte_valida(projeto_id, inteiro(f.get("parte_id"), 1, 10**9))
    dados["status"] = f.get("status") if f.get("status") in dict(pmbok.STATUS_MUDANCA) else "solicitada"
    dados["comunicada"] = 1 if f.get("comunicada") else 0
    return dados


def _validar_transicao(projeto, anterior, dados):
    """Regras do controle de mudanças. Devolve uma mensagem de erro ou None."""
    novo = dados["status"]
    if novo in ("aprovada", "rejeitada", "implementada") and not dados["decidido_por"]:
        return "Informe quem decidiu (patrocinador, comitê de controle de mudanças ou product owner)."
    if novo in ("aprovada", "rejeitada") and projeto["abordagem"] != "adaptativa":
        faltando = [nome for c, nome, _ in pmbok.IMPACTOS_MUDANCA if not dados[c]]
        if faltando:
            return ("Antes de decidir, avalie todos os impactos (use “sem impacto” quando for o caso). Faltando: "
                    + ", ".join(faltando) + ".")
    if novo == "implementada" and anterior not in ("aprovada", "implementada"):
        return "Só mudanças aprovadas podem ser implementadas."
    return None


@bp.route("/mudancas")
def mudancas(projeto_id):
    p = obter_projeto(projeto_id)
    return render_template("mudancas.html", projeto=p, mudancas=listar_mudancas(p), por_parte=mudancas_por_parte(projeto_id),
                           secao="trabalho", sub="mudancas")


@bp.route("/mudancas/nova", methods=["GET", "POST"])
def mudanca_nova(projeto_id):
    p = obter_projeto(projeto_id)
    if request.method == "POST":
        dados = _ler_mudanca(projeto_id)
        import pmo
        erro = None if dados["titulo"] else "Descreva a mudança no campo título."
        erro = erro or pmo.exigir("mudanca", dados) or _validar_transicao(p, None, dados)
        if erro:
            flash(erro, "erro")
            return render_template("mudanca_form.html", projeto=p, m={**dados, "exige_avaliacao": p["abordagem"] != "adaptativa"},
                                   novo=True, partes=_partes(projeto_id), secao="trabalho", sub="mudancas")
        if dados["status"] in ("aprovada", "rejeitada", "implementada"):
            dados["decidido_em"] = date.today().isoformat()
        db = get_db()
        codigo = db.execute("SELECT COALESCE(MAX(codigo), 0) + 1 FROM mudanca WHERE projeto_id = ?", (projeto_id,)).fetchone()[0]
        cols = list(dados)
        cur = db.execute(f"INSERT INTO mudanca (projeto_id, codigo, {', '.join(cols)}) VALUES (?, ?, {', '.join('?' for _ in cols)})",
                         [projeto_id, codigo] + [dados[c] for c in cols])
        tocar_projeto(projeto_id)
        db.commit()
        flash(f"M-{codigo} registrada.", "ok")
        return redirect(url_for("trabalho.mudanca", projeto_id=projeto_id, mudanca_id=cur.lastrowid))
    inicial = {"status": "solicitada", "titulo": request.args.get("titulo", "")[:200],
               "exige_avaliacao": p["abordagem"] != "adaptativa"}
    return render_template("mudanca_form.html", projeto=p, m=inicial, novo=True, partes=_partes(projeto_id),
                           secao="trabalho", sub="mudancas")


@bp.route("/mudancas/<int:mudanca_id>", methods=["GET", "POST"])
def mudanca(projeto_id, mudanca_id):
    p = obter_projeto(projeto_id)
    db = get_db()
    row = db.execute("SELECT * FROM mudanca WHERE id = ? AND projeto_id = ?", (mudanca_id, projeto_id)).fetchone()
    if row is None:
        abort(404)
    if request.method == "POST":
        if request.form.get("acao") == "excluir":
            if row["status"] in ("aprovada", "implementada"):
                flash("Mudanças aprovadas ou implementadas não podem ser excluídas: elas fazem parte da trilha de auditoria "
                      "do controle de mudanças. Se ela não vale mais, registre uma nova mudança revertendo-a.", "erro")
                return redirect(url_for("trabalho.mudanca", projeto_id=projeto_id, mudanca_id=mudanca_id))
            db.execute("DELETE FROM mudanca WHERE id = ?", (mudanca_id,))
            db.commit()
            flash(f"M-{row['codigo']} excluída.", "ok")
            return redirect(url_for("trabalho.mudancas", projeto_id=projeto_id))
        dados = _ler_mudanca(projeto_id)
        erro = None if dados["titulo"] else "Descreva a mudança no campo título."
        erro = erro or _validar_transicao(p, row["status"], dados)
        if erro:
            flash(erro, "erro")
            m = enriquecer_mudanca({**dict(row), **dados}, p)
            return render_template("mudanca_form.html", projeto=p, m=m, novo=False, partes=_partes(projeto_id),
                                   secao="trabalho", sub="mudancas")
        if dados["status"] != row["status"] and dados["status"] in ("aprovada", "rejeitada"):
            dados["decidido_em"] = date.today().isoformat()
        db.execute("UPDATE mudanca SET " + ", ".join(f"{c} = ?" for c in dados)
                   + ", atualizado_em = datetime('now','localtime') WHERE id = ?", list(dados.values()) + [mudanca_id])
        tocar_projeto(projeto_id)
        db.commit()
        flash(f"M-{row['codigo']} atualizada.", "ok")
        return redirect(url_for("trabalho.mudanca", projeto_id=projeto_id, mudanca_id=mudanca_id))
    itens = db.execute("SELECT id, codigo, titulo, status FROM item WHERE mudanca_id = ? ORDER BY codigo", (mudanca_id,)).fetchall()
    return render_template("mudanca_form.html", projeto=p, m=enriquecer_mudanca(row, p), novo=False, partes=_partes(projeto_id),
                           itens=itens, secao="trabalho", sub="mudancas")


# --------------------------------------------------------------------------
# Lições aprendidas
# --------------------------------------------------------------------------
@bp.route("/licoes", methods=["GET", "POST"])
def licoes(projeto_id):
    p = obter_projeto(projeto_id)
    db = get_db()
    if request.method == "POST":
        f = request.form
        if f.get("acao") == "excluir":
            lid = inteiro(f.get("licao_id"), 1, 10**9)
            db.execute("DELETE FROM licao WHERE id = ? AND projeto_id = ?", (lid, projeto_id))
            db.commit()
            flash("Lição removida.", "ok")
            return redirect(url_for("trabalho.licoes", projeto_id=projeto_id))
        if f.get("acao") == "aplicar":
            # Princípio 11 (melhoria contínua): a lição só gera valor quando muda a forma de trabalhar.
            lid = inteiro(f.get("licao_id"), 1, 10**9)
            aplicada = 1 if f.get("aplicada") == "1" else 0
            db.execute("""UPDATE licao SET aplicada = ?, aplicada_em = CASE WHEN ? = 1 THEN date('now','localtime') END
                          WHERE id = ? AND projeto_id = ?""", (aplicada, aplicada, lid, projeto_id))
            tocar_projeto(projeto_id)
            db.commit()
            flash("Lição marcada como aplicada no projeto." if aplicada else "Lição desmarcada.", "ok")
            return redirect(url_for("trabalho.licoes", projeto_id=projeto_id))
        descricao = f.get("descricao", "").strip()
        if not descricao:
            flash("Descreva a lição aprendida.", "erro")
            return redirect(url_for("trabalho.licoes", projeto_id=projeto_id))
        questao_id = inteiro(f.get("questao_id"), 1, 10**9)
        if questao_id and not db.execute("SELECT 1 FROM questao WHERE id = ? AND projeto_id = ?", (questao_id, projeto_id)).fetchone():
            questao_id = None
        data = f.get("data") or date.today().isoformat()
        try:
            data = min(date.fromisoformat(data), date.today()).isoformat()
        except ValueError:
            data = date.today().isoformat()
        escolha = lambda campo, lista, padrao: f.get(campo) if f.get(campo) in dict(lista) else padrao  # noqa: E731
        db.execute(
            """INSERT INTO licao (projeto_id, data, tipo, descricao, recomendacao, origem, dominio, conhecimento, alcance, questao_id)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (projeto_id, data, escolha("tipo", pmbok.TIPOS_LICAO, "melhorar"), descricao, f.get("recomendacao", "").strip(),
             escolha("origem", pmbok.ORIGENS_LICAO, ""),
             f.get("dominio") if f.get("dominio") in pmbok.DOMINIOS_POR_CHAVE else "",
             escolha("conhecimento", pmbok.TIPOS_CONHECIMENTO, "explicito"),
             escolha("alcance", pmbok.ALCANCES_LICAO, "projeto"), questao_id),
        )
        tocar_projeto(projeto_id)
        db.commit()
        flash("Lição registrada.", "ok")
        if questao_id and f.get("voltar") == "questao":
            return redirect(url_for("trabalho.questao", projeto_id=projeto_id, questao_id=questao_id))
        return redirect(url_for("trabalho.licoes", projeto_id=projeto_id))
    todas = listar_licoes(projeto_id)
    tipo = request.args.get("tipo", "")
    lista = [x for x in todas if not tipo or x["tipo"] == tipo]
    questao_ref = inteiro(request.args.get("questao"), 1, 10**9)
    q = None
    if questao_ref:
        q = db.execute("SELECT * FROM questao WHERE id = ? AND projeto_id = ?", (questao_ref, projeto_id)).fetchone()
    return render_template("licoes.html", projeto=p, licoes=lista, total=len(todas), tipo=tipo, questao_ref=q,
                           secao="trabalho", sub="licoes")

