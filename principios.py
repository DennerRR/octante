"""Princípios de gerenciamento de projetos (The Standard for Project Management, seção 3) — v7.

- Autoavaliação dos 12 princípios com evidências calculadas a partir de todos os módulos.
- Business case e valor (princípio 4).
- Conformidade e sustentabilidade (princípio 1, administração).
- Mudança organizacional e adoção (princípio 12, diferente do controle de mudanças do projeto).
- Registro de decisões e de premissas (princípios 5, 6 e 9).
"""
import json
from datetime import date, timedelta

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

import graficos
import pmbok
from db import get_db
from util import decimal, inteiro, moeda, obter_projeto, tocar_projeto

bp = Blueprint("principios", __name__, url_prefix="/p/<int:projeto_id>")

DIAS_REVISAO_BC = 90
DOMINIO_VERIFICACAO = "principios"


def _data(v):
    try:
        return date.fromisoformat(str(v)[:10]) if v else None
    except ValueError:
        return None


def _hoje_ou_antes(valor):
    d = _data(valor) or date.today()
    return min(d, date.today()).isoformat()


# --------------------------------------------------------------------------
# Business case (princípio 4)
# --------------------------------------------------------------------------
def analise_financeira(p):
    """VPL, ROI e payback simples a partir do business case. Devolve None se faltar dado."""
    inv, ben, n = p["bc_investimento"], p["bc_beneficio_anual"], p["bc_horizonte_anos"]
    if not inv or ben is None or not n:
        return None
    custo = p["bc_custo_anual"] or 0
    taxa = (p["bc_taxa"] or 0) / 100
    fluxo = ben - custo
    vpl = -inv + sum(fluxo / (1 + taxa) ** t for t in range(1, n + 1))
    roi = (fluxo * n - inv) / inv
    payback = inv / fluxo if fluxo > 0 else None
    acumulado, serie = -inv, [-inv]
    for t in range(1, n + 1):
        acumulado += fluxo / (1 + taxa) ** t
        serie.append(acumulado)
    return {"fluxo": fluxo, "vpl": vpl, "roi": roi, "payback": payback, "viavel": vpl >= 0, "serie": serie, "taxa": taxa * 100}


def custo_previsto(projeto):
    """Melhor previsão do custo do projeto: ENT do valor agregado ou custos planejados + reservas."""
    import entrega
    import incerteza
    import medicao
    itens = entrega.listar_itens(projeto["id"])
    va = medicao.valor_agregado(projeto, itens)
    res = incerteza.resumo_riscos(projeto, incerteza.listar_riscos(projeto))
    reservas = (res["contingencia_custo"] or 0) + (projeto["reserva_gerenciamento"] or 0)
    if va and va["ent"]:
        return va["ent"] + reservas, "estimativa no término (valor agregado) + reservas"
    planejado = sum(i["custo_planejado"] or 0 for i in entrega.folhas(itens))
    if planejado:
        return planejado + reservas, "custos planejados dos itens + reservas"
    return None, None


@bp.route("/business-case", methods=["GET", "POST"])
def business_case(projeto_id):
    p = obter_projeto(projeto_id)
    if request.method == "POST":
        f = request.form
        db = get_db()
        db.execute(
            """UPDATE projeto SET bc_necessidade = ?, bc_justificativa = ?, bc_estrategia = ?, bc_alternativas = ?,
               bc_beneficios_nao_financeiros = ?, bc_investimento = ?, bc_beneficio_anual = ?, bc_custo_anual = ?,
               bc_horizonte_anos = ?, bc_taxa = ?, bc_revisado_em = date('now','localtime') WHERE id = ?""",
            (f.get("bc_necessidade", "").strip(), f.get("bc_justificativa", "").strip(), f.get("bc_estrategia", "").strip(),
             f.get("bc_alternativas", "").strip(), f.get("bc_beneficios_nao_financeiros", "").strip(),
             decimal(f.get("bc_investimento")), decimal(f.get("bc_beneficio_anual")), decimal(f.get("bc_custo_anual")),
             inteiro(f.get("bc_horizonte_anos"), 1, 50), decimal(f.get("bc_taxa")), projeto_id))
        tocar_projeto(projeto_id)
        db.commit()
        flash("Business case salvo e marcado como revisado hoje.", "ok")
        return redirect(url_for("principios.business_case", projeto_id=projeto_id))
    fin = analise_financeira(p)
    grafico = None
    if fin:
        grafico = graficos.linhas([{"nome": "Valor presente acumulado", "valores": fin["serie"]}],
                                  ["Início"] + [f"Ano {t}" for t in range(1, len(fin["serie"]))],
                                  "Valor presente acumulado em reais", largura=560, altura=210)
    previsto, base = custo_previsto(p)
    beneficios = get_db().execute("SELECT * FROM beneficio WHERE projeto_id = ? ORDER BY data_prevista IS NULL, data_prevista", (projeto_id,)).fetchall()
    return render_template("business_case.html", projeto=p, fin=fin, grafico=grafico, previsto=previsto, base_previsto=base,
                           beneficios=beneficios, secao="principios", sub="valor")


# --------------------------------------------------------------------------
# Conformidade e sustentabilidade (princípio 1)
# --------------------------------------------------------------------------
@bp.route("/conformidade", methods=["GET", "POST"])
def conformidade(projeto_id):
    p = obter_projeto(projeto_id)
    db = get_db()
    if request.method == "POST":
        f = request.form
        reg_id = inteiro(f.get("registro_id"), 1, 10**9)
        if f.get("acao") == "excluir":
            db.execute("DELETE FROM conformidade WHERE id = ? AND projeto_id = ?", (reg_id, projeto_id))
            flash("Requisito removido.", "ok")
        else:
            area = f.get("area")
            requisito = f.get("requisito", "").strip()
            status = f.get("status") if f.get("status") in dict(pmbok.STATUS_CONFORMIDADE) else "pendente"
            if area not in dict(pmbok.AREAS_CONFORMIDADE) or not requisito:
                flash("Escolha a área e descreva o requisito.", "erro")
                return redirect(url_for("principios.conformidade", projeto_id=projeto_id))
            if status == "atendido" and not f.get("evidencia", "").strip():
                flash("Para marcar como atendido, registre a evidência.", "erro")
                return redirect(url_for("principios.conformidade", projeto_id=projeto_id) + (f"#c{reg_id}" if reg_id else ""))
            prazo = _data(f.get("prazo"))
            valores = (area, requisito, f.get("como_atender", "").strip(), f.get("responsavel", "").strip(),
                       prazo.isoformat() if prazo else None, status, f.get("evidencia", "").strip())
            if reg_id:
                if db.execute("SELECT 1 FROM conformidade WHERE id = ? AND projeto_id = ?", (reg_id, projeto_id)).fetchone() is None:
                    abort(404)
                db.execute("""UPDATE conformidade SET area = ?, requisito = ?, como_atender = ?, responsavel = ?, prazo = ?, status = ?,
                              evidencia = ?, atualizado_em = date('now','localtime') WHERE id = ?""", valores + (reg_id,))
                flash("Requisito atualizado.", "ok")
            else:
                db.execute("""INSERT INTO conformidade (projeto_id, area, requisito, como_atender, responsavel, prazo, status, evidencia)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", (projeto_id,) + valores)
                flash("Requisito registrado.", "ok")
        tocar_projeto(projeto_id)
        db.commit()
        return redirect(url_for("principios.conformidade", projeto_id=projeto_id))
    regs = listar_conformidade(projeto_id)
    cobertura = {a: [r for r in regs if r["area"] == a] for a, _ in pmbok.AREAS_CONFORMIDADE}
    return render_template("conformidade.html", projeto=p, registros=regs, cobertura=cobertura, secao="principios", sub="conformidade")


def listar_conformidade(projeto_id):
    hoje = date.today().isoformat()
    rows = get_db().execute("SELECT * FROM conformidade WHERE projeto_id = ? ORDER BY status = 'atendido', status = 'nao_aplicavel', prazo IS NULL, prazo, id",
                            (projeto_id,)).fetchall()
    return [{**dict(r), "atrasado": r["status"] in ("pendente", "em_andamento") and bool(r["prazo"]) and r["prazo"] < hoje} for r in rows]


# --------------------------------------------------------------------------
# Mudança organizacional (princípio 12)
# --------------------------------------------------------------------------
def listar_grupos(projeto_id):
    db = get_db()
    grupos = db.execute("""SELECT g.*, s.nome AS parte_nome FROM adocao_grupo g LEFT JOIN parte_interessada s ON s.id = g.parte_id
                           WHERE g.projeto_id = ? ORDER BY COALESCE(g.impacto, 0) DESC, g.id""", (projeto_id,)).fetchall()
    out = []
    for g in grupos:
        meds = db.execute("SELECT * FROM adocao_medicao WHERE grupo_id = ? ORDER BY data, id", (g["id"],)).fetchall()
        ultima = meds[-1] if meds else None
        d = dict(g)
        d["medicoes"] = meds
        d["adocao_atual"] = ultima["adocao"] if ultima else None
        d["serie"] = [m["adocao"] for m in meds]
        d["na_meta"] = d["adocao_atual"] is not None and g["meta_adocao"] is not None and d["adocao_atual"] >= g["meta_adocao"]
        # risco de resistência: impacto alto com prontidão baixa (3.12: adaptar o ritmo à capacidade de absorção)
        d["risco_resistencia"] = (g["impacto"] or 0) >= 4 and (g["prontidao"] or 5) <= 2
        out.append(d)
    return out


@bp.route("/mudanca-organizacional", methods=["GET", "POST"])
def adocao(projeto_id):
    p = obter_projeto(projeto_id)
    db = get_db()
    if request.method == "POST":
        f = request.form
        acao = f.get("acao")
        gid = inteiro(f.get("grupo_id"), 1, 10**9)
        if gid and db.execute("SELECT 1 FROM adocao_grupo WHERE id = ? AND projeto_id = ?", (gid, projeto_id)).fetchone() is None:
            abort(404)
        if acao == "estados":
            db.execute("UPDATE projeto SET mudanca_estado_atual = ?, mudanca_estado_futuro = ? WHERE id = ?",
                       (f.get("mudanca_estado_atual", "").strip(), f.get("mudanca_estado_futuro", "").strip(), projeto_id))
            flash("Estados atual e futuro salvos.", "ok")
        elif acao == "medir":
            valor = decimal(f.get("adocao"))
            if valor is None or valor > 100:
                flash("Informe a adoção em % (0 a 100).", "erro")
            else:
                db.execute("INSERT INTO adocao_medicao (grupo_id, data, adocao, prontidao, nota) VALUES (?, ?, ?, ?, ?)",
                           (gid, _hoje_ou_antes(f.get("data")), valor, inteiro(f.get("prontidao")), f.get("nota", "").strip()))
                if inteiro(f.get("prontidao")):
                    db.execute("UPDATE adocao_grupo SET prontidao = ? WHERE id = ?", (inteiro(f.get("prontidao")), gid))
                flash("Medição de adoção registrada.", "ok")
        elif acao == "excluir":
            db.execute("DELETE FROM adocao_grupo WHERE id = ?", (gid,))
            flash("Grupo removido.", "ok")
        else:
            grupo = f.get("grupo", "").strip()
            if not grupo:
                flash("Informe o grupo afetado.", "erro")
                return redirect(url_for("principios.adocao", projeto_id=projeto_id))
            parte = inteiro(f.get("parte_id"), 1, 10**9)
            if parte and not db.execute("SELECT 1 FROM parte_interessada WHERE id = ? AND projeto_id = ?", (parte, projeto_id)).fetchone():
                parte = None
            meta = decimal(f.get("meta_adocao"))
            valores = (grupo, parte, f.get("o_que_muda", "").strip(), inteiro(f.get("impacto")), inteiro(f.get("prontidao")),
                       f.get("resistencias", "").strip(), f.get("acoes", "").strip(), meta if meta is None or meta <= 100 else 100,
                       f.get("status") if f.get("status") in dict(pmbok.STATUS_ADOCAO) else "nao_iniciado")
            if gid:
                db.execute("""UPDATE adocao_grupo SET grupo = ?, parte_id = ?, o_que_muda = ?, impacto = ?, prontidao = ?, resistencias = ?,
                              acoes = ?, meta_adocao = ?, status = ? WHERE id = ?""", valores + (gid,))
                flash("Grupo atualizado.", "ok")
            else:
                db.execute("""INSERT INTO adocao_grupo (projeto_id, grupo, parte_id, o_que_muda, impacto, prontidao, resistencias, acoes,
                              meta_adocao, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (projeto_id,) + valores)
                flash("Grupo afetado registrado.", "ok")
        tocar_projeto(projeto_id)
        db.commit()
        return redirect(url_for("principios.adocao", projeto_id=projeto_id) + (f"#g{gid}" if gid and acao != "excluir" else ""))
    grupos = listar_grupos(projeto_id)
    for g in grupos:
        g["grafico"] = graficos.linhas([{"nome": "Adoção (%)", "valores": g["serie"]}],
                                       [m["data"][8:10] + "/" + m["data"][5:7] for m in g["medicoes"]],
                                       f"Adoção de {g['grupo']} em %", largura=380, altura=140) if len(g["serie"]) > 1 else None
    partes = [(r["id"], r["nome"]) for r in
              db.execute("SELECT id, nome FROM parte_interessada WHERE projeto_id = ? AND ativa = 1 ORDER BY nome", (projeto_id,))]
    simultaneas = sum(1 for g in grupos if g["status"] in ("preparando", "em_transicao"))
    return render_template("adocao.html", projeto=p, grupos=grupos, partes=partes, simultaneas=simultaneas,
                           secao="principios", sub="adocao")


# --------------------------------------------------------------------------
# Decisões e premissas (princípios 5, 6 e 9)
# --------------------------------------------------------------------------
@bp.route("/decisoes", methods=["GET", "POST"])
def decisoes(projeto_id):
    p = obter_projeto(projeto_id)
    db = get_db()
    if request.method == "POST":
        f = request.form
        acao = f.get("acao")
        rid = inteiro(f.get("registro_id"), 1, 10**9)
        if acao == "decisao":
            titulo = f.get("titulo", "").strip()
            if not titulo:
                flash("Dê um título à decisão.", "erro")
            else:
                revisar = _data(f.get("revisar_em"))
                db.execute("""INSERT INTO decisao (projeto_id, data, titulo, contexto, alternativas, decisao, decidido_por, envolvidos, efeitos, revisar_em)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                           (projeto_id, _hoje_ou_antes(f.get("data")), titulo, f.get("contexto", "").strip(), f.get("alternativas", "").strip(),
                            f.get("decisao", "").strip(), f.get("decidido_por", "").strip(), f.get("envolvidos", "").strip(),
                            f.get("efeitos", "").strip(), revisar.isoformat() if revisar else None))
                flash("Decisão registrada.", "ok")
        elif acao == "excluir_decisao":
            db.execute("DELETE FROM decisao WHERE id = ? AND projeto_id = ?", (rid, projeto_id))
            flash("Decisão removida.", "ok")
        elif acao == "premissa":
            descricao = f.get("descricao", "").strip()
            if not descricao:
                flash("Descreva a premissa.", "erro")
            else:
                ate = _data(f.get("validar_ate"))
                db.execute("INSERT INTO premissa (projeto_id, descricao, se_falsa, como_validar, validar_ate) VALUES (?, ?, ?, ?, ?)",
                           (projeto_id, descricao, f.get("se_falsa", "").strip(), f.get("como_validar", "").strip(), ate.isoformat() if ate else None))
                flash("Premissa registrada.", "ok")
        elif acao == "status_premissa":
            status = f.get("status")
            if status in dict(pmbok.STATUS_PREMISSA):
                db.execute("UPDATE premissa SET status = ?, atualizado_em = date('now','localtime') WHERE id = ? AND projeto_id = ?",
                           (status, rid, projeto_id))
                if status == "invalidada":
                    flash("Premissa invalidada. Avalie se ela vira um risco, uma questão ou uma mudança no plano.", "aviso")
                else:
                    flash("Premissa atualizada.", "ok")
        elif acao == "excluir_premissa":
            db.execute("DELETE FROM premissa WHERE id = ? AND projeto_id = ?", (rid, projeto_id))
            flash("Premissa removida.", "ok")
        tocar_projeto(projeto_id)
        db.commit()
        return redirect(url_for("principios.decisoes", projeto_id=projeto_id))
    hoje = date.today().isoformat()
    decs = [{**dict(d), "revisar": bool(d["revisar_em"]) and d["revisar_em"] <= hoje}
            for d in db.execute("SELECT * FROM decisao WHERE projeto_id = ? ORDER BY data DESC, id DESC", (projeto_id,))]
    prems = [{**dict(x), "vencida": x["status"] == "nao_validada" and bool(x["validar_ate"]) and x["validar_ate"] < hoje}
             for x in db.execute("SELECT * FROM premissa WHERE projeto_id = ? ORDER BY status != 'nao_validada', validar_ate IS NULL, validar_ate, id", (projeto_id,))]
    abertura = db.execute("SELECT premissas FROM abertura WHERE projeto_id = ?", (projeto_id,)).fetchone()
    return render_template("decisoes.html", projeto=p, decisoes=decs, premissas=prems,
                           premissas_termo=(abertura["premissas"] if abertura else ""), secao="principios", sub="decisoes")


# --------------------------------------------------------------------------
# Autoavaliação dos 12 princípios
# --------------------------------------------------------------------------
def avaliar_principios(projeto):
    """Para cada princípio, verificações objetivas calculadas a partir dos registros do projeto."""
    import ciclo
    import entrega
    import equipe
    import incerteza
    import medicao
    import partes
    import trabalho
    pid = projeto["id"]
    db = get_db()
    hoje = date.today()
    U = lambda nome, **kw: url_for(nome, projeto_id=pid, **kw)  # noqa: E731

    def conta(sql, *args):
        return db.execute(sql, (pid,) + args).fetchone()[0]

    ab = db.execute("SELECT * FROM abertura WHERE projeto_id = ?", (pid,)).fetchone()
    lista_partes = partes.listar_partes(pid)
    itens = entrega.listar_itens(pid)
    trab = entrega.folhas(itens)
    ativos = [i for i in trab if not i["feito"]]
    riscos = incerteza.listar_riscos(projeto)
    riscos_ativos = [r for r in riscos if r["ativo"]]
    res_riscos = incerteza.resumo_riscos(projeto, riscos)
    mudancas = trabalho.listar_mudancas(projeto)
    eq = equipe.resumo_equipe(projeto)
    avs = equipe.avaliacoes(pid)
    ultima = avs[-1] if avs else None
    nota = lambda k: (ultima["notas"].get(k) if ultima else None)  # noqa: E731
    fases = ciclo.listar_fases(pid)
    regs = listar_conformidade(pid)
    grupos = listar_grupos(pid)
    fin = analise_financeira(projeto)
    previsto, _ = custo_previsto(projeto)
    coq = entrega.custo_qualidade(pid)
    n_decisoes = conta("SELECT COUNT(*) FROM decisao WHERE projeto_id = ?")
    decs_efeitos = conta("SELECT COUNT(*) FROM decisao WHERE projeto_id = ? AND TRIM(efeitos) != '' AND TRIM(alternativas) != ''")
    decs_envolvidos = conta("SELECT COUNT(*) FROM decisao WHERE projeto_id = ? AND TRIM(envolvidos) != ''")
    prems_total = conta("SELECT COUNT(*) FROM premissa WHERE projeto_id = ?")
    prems_validadas = conta("SELECT COUNT(*) FROM premissa WHERE projeto_id = ? AND status != 'nao_validada'")
    prems_vencidas = conta("SELECT COUNT(*) FROM premissa WHERE projeto_id = ? AND status = 'nao_validada' AND validar_ate < ?", hoje.isoformat())
    incertezas = conta("SELECT COUNT(*) FROM incerteza WHERE projeto_id = ?")
    incertezas_resp = conta("SELECT COUNT(*) FROM incerteza WHERE projeto_id = ? AND status != 'resolvida' AND TRIM(respostas) != ''")
    incertezas_abertas = conta("SELECT COUNT(*) FROM incerteza WHERE projeto_id = ? AND status != 'resolvida'")
    licoes = conta("SELECT COUNT(*) FROM licao WHERE projeto_id = ?")
    licoes_aplicadas = conta("SELECT COUNT(*) FROM licao WHERE projeto_id = ? AND aplicada = 1")
    dec_tailoring = conta("SELECT COUNT(*) FROM decisao_tailoring WHERE projeto_id = ?")
    linhas_base = conta("SELECT COUNT(*) FROM linha_base WHERE projeto_id = ?")
    n_iteracoes = conta("SELECT COUNT(*) FROM iteracao WHERE projeto_id = ?")
    respostas_tailoring = json.loads(projeto["tailoring_json"] or "{}")
    fatores = json.loads(projeto["fatores_json"] or "{}")
    bc_rev = _data(projeto["bc_revisado_em"])
    lim_bc = hoje - timedelta(days=DIAS_REVISAO_BC)
    altos = [r for r in riscos_ativos if r["tipo"] == "ameaca" and r["nivel"] == "alto"]
    altos_resp = [r for r in altos if r["estrategia"] and not (r["estrategia"] == "aceitar" and not r["plano_contingencia"])]
    decididas = [m for m in mudancas if m["status"] in ("aprovada", "rejeitada", "implementada")]
    opositores_fortes = [s for s in lista_partes if s["atitude"] == "opositor" and (s["poder"] or 0) >= 4]
    areas_externas = {r["area"] for r in regs if r["area"] in ("ambiental", "social")}

    def frac(a, b):
        return b > 0 and a / b

    principios = [
        # 1. Administração
        [
            ("Requisitos de conformidade registrados (legal, privacidade, segurança, ética…)", bool(regs), U("principios.conformidade")),
            ("Impacto ambiental e social avaliado (mesmo que “não se aplica”)", len(areas_externas) == 2, U("principios.conformidade")),
            ("Nenhum requisito de conformidade pendente com prazo vencido", bool(regs) and not any(r["atrasado"] for r in regs), U("principios.conformidade")),
            ("Termo de abertura aprovado (autoridade e responsabilidades claras)", bool(ab) and ab["status"] == "aprovado", U("abertura")),
            ("Uso das reservas dentro do reservado", res_riscos["contingencia_usada"] <= res_riscos["contingencia_custo"]
             and res_riscos["gerenciamento_usado"] <= (res_riscos["gerenciamento"] or 0), U("incerteza.painel")),
        ],
        # 2. Equipe colaborativa
        [
            ("Acordo de trabalho com pelo menos 3 seções", eq["acordo"] >= 3, U("equipe.acordo")),
            ("Matriz RACI preenchida e sem problemas", eq["raci_linhas"] > 0 and not eq["raci_problemas"], U("equipe.matriz")),
            ("Saúde da equipe avaliada nos últimos 45 dias", bool(ultima) and _data(ultima["data"]) >= hoje - timedelta(days=45), U("equipe.saude")),
            ("Colaboração e comunicação com nota ≥ 3", bool(ultima) and (nota("colaboracao") or 0) >= 3 and (nota("comunicacao") or 0) >= 3, U("equipe.saude")),
            ("Lacunas de habilidade com plano de desenvolvimento", eq["membros"] > 0 and not eq["lacunas_sem_plano"], U("equipe.membros")),
        ],
        # 3. Partes interessadas
        [
            ("Partes interessadas identificadas", bool(lista_partes), U("partes_registro")),
            ("Analisadas: poder, interesse e atitude (≥ 80%)", frac(sum(s["analisada"] for s in lista_partes), len(lista_partes)) >= 0.8, U("partes_analise")),
            ("Priorização confirmada", bool(lista_partes) and all(s["priorizada"] for s in lista_partes), U("partes_priorizacao")),
            ("Plano de engajamento (≥ 80%)", frac(sum(s["plano_engajamento"] for s in lista_partes), len(lista_partes)) >= 0.8, U("partes_engajamento")),
            ("Ao menos metade com interação nos últimos 30 dias", frac(sum(s["monitorada"] for s in lista_partes), len(lista_partes)) >= 0.5, U("partes_monitoramento")),
            ("Opositores com alto poder têm estratégia de engajamento", not any(not (s["estrategia"] or "").strip() for s in opositores_fortes), U("partes_engajamento")),
        ],
        # 4. Valor
        [
            ("Business case com necessidade, justificativa e estratégia", all((projeto[c] or "").strip() for c in ("bc_necessidade", "bc_justificativa", "bc_estrategia")), U("principios.business_case")),
            ("Viabilidade calculada (VPL ≥ 0) ou benefícios não financeiros descritos",
             (fin is not None and fin["viavel"]) or bool((projeto["bc_beneficios_nao_financeiros"] or "").strip()), U("principios.business_case")),
            ("Business case revisado nos últimos 90 dias", bool(bc_rev) and bc_rev >= lim_bc, U("principios.business_case")),
            ("Custo previsto dentro do investimento do business case",
             not (previsto and projeto["bc_investimento"]) or previsto <= projeto["bc_investimento"], U("principios.business_case")),
            ("Benefícios registrados com medida", conta("SELECT COUNT(*) FROM beneficio WHERE projeto_id = ? AND TRIM(medida) != ''") > 0, U("entrega.beneficios")),
            ("Itens de escopo com valor de negócio (≥ 80%)", frac(sum(1 for i in trab if i["valor"]), len(trab)) >= 0.8, U("entrega.itens")),
        ],
        # 5. Pensamento sistêmico
        [
            ("Premissas registradas", prems_total > 0, U("principios.decisoes")),
            ("Premissas sendo validadas (≥ 50% e nenhuma vencida)", frac(prems_validadas, prems_total) >= 0.5 and not prems_vencidas, U("principios.decisoes")),
            ("Decisões registram alternativas e efeitos em outras áreas", decs_efeitos > 0, U("principios.decisoes")),
            ("Mudanças decididas com avaliação dos 6 impactos", bool(decididas) and all(m["impactos_avaliados"] == 6 for m in decididas), U("trabalho.mudancas")),
            ("Riscos ligados a partes interessadas ou a itens de resposta",
             any(r["parte_id"] for r in riscos) or conta("SELECT COUNT(*) FROM item WHERE projeto_id = ? AND risco_id IS NOT NULL") > 0, U("incerteza.riscos")),
        ],
        # 6. Liderança
        [
            ("Modelo de liderança definido (centralizado ou distribuído)", bool(projeto["modelo_lideranca"]), U("equipe.membros")),
            ("Estágio da equipe acompanhado (Tuckman)", bool(projeto["estagio_equipe"]), U("equipe.membros")),
            ("Visão do projeto escrita e compartilhável", bool(ab) and bool((ab["visao_texto"] or "").strip()), U("abertura")),
            ("Regras de tomada de decisão no acordo da equipe", bool((projeto["acordo_decisoes"] or "").strip()), U("equipe.acordo")),
            ("Decisões registradas com quem decidiu e quem foi envolvido", decs_envolvidos > 0, U("principios.decisoes")),
            ("Empoderamento e reconhecimento com nota ≥ 3", bool(ultima) and (nota("empoderamento") or 0) >= 3 and (nota("reconhecimento") or 0) >= 3, U("equipe.saude")),
        ],
        # 7. Tailoring
        [
            ("Abordagem escolhida e justificada", bool(projeto["abordagem"]) and bool((projeto["abordagem_justificativa"] or "").strip()), U("abordagem")),
            ("Fatores de seleção avaliados (≥ 10 de 15)", len(fatores) >= 10, U("abordagem")),
            ("Contexto do projeto respondido (≥ 5 perguntas)", len(respostas_tailoring) >= 5, U("ciclo.tailoring")),
            ("Decisões de tailoring registradas", dec_tailoring > 0, U("ciclo.tailoring")),
            ("Nenhuma situação da Tabela 3-1 sem tratamento", not ciclo.diagnostico(projeto), U("ciclo.tailoring")),
        ],
        # 8. Qualidade
        [
            ("Definição de pronto escrita", bool((projeto["definicao_pronto"] or "").strip()), U("entrega.painel") + "#parametros"),
            ("Itens a fazer bem documentados (≥ 70%)", frac(sum(1 for i in ativos if i["bem_documentado"]), len(ativos)) >= 0.7 if ativos else bool(trab), U("entrega.itens")),
            ("Atividades de prevenção ou avaliação registradas", any(c["n"] for c in coq["categorias"] if c["grupo"] == "conformidade"), U("entrega.qualidade")),
            ("Defeitos resolvidos (≥ 80%)", coq["defeitos"] == 0 or frac(coq["defeitos_resolvidos"], coq["defeitos"]) >= 0.8, U("entrega.qualidade")),
            ("Itens aceitos com critérios de aceite", any(i["status"] == "aceito" for i in trab) and all(i["criterios_aceite"] for i in trab if i["status"] == "aceito"), U("entrega.itens")),
        ],
        # 9. Complexidade
        [
            ("Ambiguidade, complexidade ou volatilidade registradas", incertezas > 0, U("incerteza.outras")),
            ("Incertezas em aberto com resposta escolhida", incertezas_abertas == 0 or incertezas_resp == incertezas_abertas, U("incerteza.outras")),
            ("Risco global do projeto avaliado", bool(projeto["risco_global"]), U("incerteza.painel") + "#global"),
            ("Premissas registradas e acompanhadas", prems_total > 0 and not prems_vencidas, U("principios.decisoes")),
            ("Entrega iterativa ou incremental para aprender com feedback", n_iteracoes > 0 or projeto["cadencia"] in ("multiplas", "periodica", "continua"), U("medicao.cronograma")),
        ],
        # 10. Riscos
        [
            ("Ameaças registradas", any(r["tipo"] == "ameaca" for r in riscos), U("incerteza.riscos")),
            ("Oportunidades registradas", any(r["tipo"] == "oportunidade" for r in riscos), U("incerteza.riscos")),
            ("Ameaças acima do limite com resposta ativa", len(altos_resp) == len(altos), U("incerteza.riscos")),
            ("Revisões de risco em dia", bool(riscos_ativos) and not any(r["revisao_atrasada"] for r in riscos_ativos), U("incerteza.riscos")),
            ("Apetite a risco e reservas definidos", bool((projeto["apetite_risco"] or "").strip()) and (res_riscos["contingencia_custo"] > 0 or bool(projeto["reserva_gerenciamento"])), U("incerteza.painel") + "#global"),
        ],
        # 11. Adaptabilidade e resiliência
        [
            ("Plano de exceção definido", bool((projeto["plano_excecao"] or "").strip()), U("medicao.painel") + "#excecao"),
            ("Lições aprendidas registradas", licoes > 0, U("trabalho.licoes")),
            ("Lições aplicadas no próprio projeto", licoes_aplicadas > 0, U("trabalho.licoes")),
            ("Planos adaptados (iterações, nova linha de base ou mudança aprovada)",
             n_iteracoes > 0 or linhas_base > 1 or any(m["status"] in ("aprovada", "implementada") for m in mudancas), U("medicao.cronograma")),
            ("Resiliência e adaptabilidade da equipe com nota ≥ 3", bool(ultima) and (nota("resiliencia") or 0) >= 3 and (nota("adaptabilidade") or 0) >= 3, U("equipe.saude")),
        ],
        # 12. Mudança organizacional
        [
            ("Estado atual e estado futuro descritos", bool((projeto["mudanca_estado_atual"] or "").strip()) and bool((projeto["mudanca_estado_futuro"] or "").strip()), U("principios.adocao")),
            ("Grupos afetados pela mudança identificados", bool(grupos), U("principios.adocao")),
            ("Ações de comunicação e treinamento para cada grupo", bool(grupos) and all((g["acoes"] or "").strip() for g in grupos), U("principios.adocao")),
            ("Prontidão avaliada e metas de adoção definidas", bool(grupos) and all(g["prontidao"] and g["meta_adocao"] is not None for g in grupos), U("principios.adocao")),
            ("Adoção medida", any(g["medicoes"] for g in grupos), U("principios.adocao")),
            ("Nenhum grupo de alto impacto com prontidão baixa sem ação", not any(g["risco_resistencia"] and not (g["acoes"] or "").strip() for g in grupos), U("principios.adocao")),
        ],
    ]
    verifs = {r["indice"]: r for r in db.execute("SELECT * FROM verificacao WHERE projeto_id = ? AND dominio = ?", (pid, DOMINIO_VERIFICACAO))}
    out = []
    for i, ((nome, texto), checks) in enumerate(zip(pmbok.PRINCIPIOS, principios)):
        ok = sum(1 for _, v, _ in checks if v)
        pct = round(100 * ok / len(checks))
        nivel = "forte" if pct >= 80 else ("parcial" if pct >= 50 else "fraco")
        v = verifs.get(i)
        out.append({"i": i, "numero": i + 1, "nome": nome, "texto": texto, "pct": pct, "nivel": nivel, "ok": ok, "total": len(checks),
                    "checks": [{"rotulo": r, "ok": bool(v_), "link": lk} for r, v_, lk in checks],
                    "status": v["status"] if v else "nao_avaliado", "reflexao": v["evidencia"] if v else "",
                    "atualizado_em": v["atualizado_em"] if v else None})
    return out


def gerar_alertas_principios(projeto):
    pid = projeto["id"]
    alertas = []
    p = projeto
    fin = analise_financeira(p)
    if fin and not fin["viavel"]:
        alertas.append(("alto", f"O business case tem VPL negativo ({moeda(fin['vpl'])}): o projeto não se paga no horizonte definido.",
                        url_for("principios.business_case", projeto_id=pid)))
    previsto, base = custo_previsto(p)
    if previsto and p["bc_investimento"] and previsto > p["bc_investimento"]:
        alertas.append(("alto", f"O custo previsto ({moeda(previsto)}) passou do investimento do business case ({moeda(p['bc_investimento'])}). "
                                "Reavalie se o projeto ainda entrega o valor pretendido (princípio 4).", url_for("principios.business_case", projeto_id=pid)))
    bc = _data(p["bc_revisado_em"])
    if bc and bc < date.today() - timedelta(days=DIAS_REVISAO_BC):
        alertas.append(("info", f"O business case não é revisado há mais de {DIAS_REVISAO_BC} dias.", url_for("principios.business_case", projeto_id=pid)))
    for r in listar_conformidade(pid):
        if r["atrasado"]:
            alertas.append(("alto", f"Requisito de conformidade “{r['requisito']}” passou do prazo.", url_for("principios.conformidade", projeto_id=pid)))
    for g in listar_grupos(pid):
        if g["risco_resistencia"]:
            alertas.append(("medio", f"“{g['grupo']}” terá impacto alto e tem prontidão baixa para a mudança: reforce comunicação e treinamento.",
                            url_for("principios.adocao", projeto_id=pid) + f"#g{g['id']}"))
    grupos = listar_grupos(pid)
    if sum(1 for g in grupos if g["status"] in ("preparando", "em_transicao")) >= 4:
        alertas.append(("info", "Quatro ou mais grupos em transição ao mesmo tempo: cuidado com a saturação de mudanças (3.12).",
                        url_for("principios.adocao", projeto_id=pid)))
    hoje = date.today().isoformat()
    for x in get_db().execute("SELECT * FROM premissa WHERE projeto_id = ? AND status = 'nao_validada' AND validar_ate < ?", (pid, hoje)):
        alertas.append(("medio", f"A premissa “{x['descricao']}” devia ter sido validada até {x['validar_ate'][8:10]}/{x['validar_ate'][5:7]}.",
                        url_for("principios.decisoes", projeto_id=pid)))
    fracos = [f"{a['numero']}. {a['nome']}" for a in avaliar_principios(p) if a["nivel"] == "fraco"]
    if fracos:
        alertas.append(("info", "Princípios com pouca evidência no projeto: " + ", ".join(fracos) + ".",
                        url_for("principios.autoavaliacao", projeto_id=pid)))
    return [{"nivel": n, "texto": t, "link": lk} for n, t, lk in alertas]


@bp.route("/principios", methods=["GET", "POST"])
def autoavaliacao(projeto_id):
    p = obter_projeto(projeto_id)
    if request.method == "POST":
        db = get_db()
        validos = dict(pmbok.STATUS_VERIFICACAO)
        for i in range(len(pmbok.PRINCIPIOS)):
            if f"status_{i}" not in request.form:
                continue
            status = request.form.get(f"status_{i}")
            db.execute(
                """INSERT INTO verificacao (projeto_id, dominio, indice, status, evidencia, atualizado_em)
                   VALUES (?, ?, ?, ?, ?, datetime('now','localtime'))
                   ON CONFLICT(projeto_id, dominio, indice) DO UPDATE SET
                   status = excluded.status, evidencia = excluded.evidencia, atualizado_em = excluded.atualizado_em""",
                (projeto_id, DOMINIO_VERIFICACAO, i, status if status in validos else "nao_avaliado", request.form.get(f"reflexao_{i}", "").strip()))
        tocar_projeto(projeto_id)
        db.commit()
        flash("Autoavaliação dos princípios salva.", "ok")
        return redirect(url_for("principios.autoavaliacao", projeto_id=projeto_id))
    avaliacao = avaliar_principios(p)
    grafico = graficos.colunas([{"nome": "Evidências atendidas (%)", "valores": [a["pct"] for a in avaliacao]}],
                               [str(a["numero"]) for a in avaliacao], "Percentual de evidências atendidas por princípio",
                               largura=760, altura=200, ticks=[0, 25, 50, 75, 100])
    return render_template("principios_avaliacao.html", projeto=p, avaliacao=avaliacao, grafico=grafico, secao="principios", sub="avaliacao")
