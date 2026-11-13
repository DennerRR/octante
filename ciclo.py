"""Ciclo de vida e fases (PMBOK 7, 2.3.5), tailoring (Guia, seção 3) e encerramento do projeto.

Fases com critérios de saída e revisão de fase (phase gate); perguntas e
registro das decisões de tailoring; diagnóstico da Tabela 3-1 a partir dos
dados do app; encerramento com checklist e comparação com as linhas de base.
"""
import json
from datetime import date, timedelta

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

import pmbok
from db import get_db
from util import inteiro, obter_projeto, tocar_projeto

bp = Blueprint("ciclo", __name__, url_prefix="/p/<int:projeto_id>")


def _data(v):
    try:
        return date.fromisoformat(str(v)[:10]) if v else None
    except ValueError:
        return None


# --------------------------------------------------------------------------
# Fases
# --------------------------------------------------------------------------
def enriquecer_fase(row):
    f = dict(row)
    f["criterios"] = [c.strip() for c in (f["criterios_saida"] or "").splitlines() if c.strip()]
    marcados = set(json.loads(f["criterios_ok"] or "[]"))
    f["marcados"] = [i for i in range(len(f["criterios"])) if i in marcados]
    f["todos_ok"] = len(f["marcados"]) == len(f["criterios"])
    hoje = date.today()
    f["atrasada"] = f["status"] != "concluida" and bool(f["fim"]) and _data(f["fim"]) < hoje
    f["atual"] = f["status"] == "em_andamento"
    return f


def listar_fases(projeto_id):
    rows = get_db().execute("SELECT * FROM fase WHERE projeto_id = ? ORDER BY ordem, id", (projeto_id,)).fetchall()
    return [enriquecer_fase(r) for r in rows]


def gerar_alertas_ciclo(projeto):
    pid = projeto["id"]
    alertas = []
    fases = listar_fases(pid)
    link = url_for("ciclo.fases", projeto_id=pid)
    if not fases and projeto["abordagem"] in ("preditiva", "hibrida"):
        alertas.append(("info", "O ciclo de vida ainda não tem fases definidas.", link))
    for f in fases:
        if f["atrasada"]:
            alertas.append(("medio", f"A fase “{f['nome']}” passou da data de término ({_data(f['fim']).strftime('%d/%m/%Y')}) sem revisão de fase.", link + f"#fase{f['id']}"))
        if f["status"] == "concluida" and f["revisao_decisao"] == "seguir_com_ressalvas" and (f["revisao_notas"] or "").strip() == "":
            alertas.append(("info", f"A fase “{f['nome']}” seguiu com ressalvas sem registrá-las.", link + f"#fase{f['id']}"))
    for d in diagnostico(projeto):
        alertas.append(("info", f"Tailoring: {d['situacao']} Sugestão: {d['sugestao']}", url_for("ciclo.tailoring", projeto_id=pid)))
    return [{"nivel": n, "texto": t, "link": lk} for n, t, lk in alertas]


@bp.route("/fases", methods=["GET", "POST"])
def fases(projeto_id):
    p = obter_projeto(projeto_id)
    db = get_db()
    if request.method == "POST":
        f = request.form
        acao = f.get("acao")
        if acao == "sugeridas":
            if db.execute("SELECT 1 FROM fase WHERE projeto_id = ?", (projeto_id,)).fetchone():
                flash("O projeto já tem fases; as sugestões só são aplicadas a um ciclo vazio.", "erro")
            else:
                modelo = pmbok.FASES_SUGERIDAS.get(p["abordagem"] or "hibrida")
                for n, (nome, objetivo, criterios) in enumerate(modelo, start=1):
                    db.execute("INSERT INTO fase (projeto_id, nome, ordem, objetivo, criterios_saida) VALUES (?, ?, ?, ?, ?)",
                               (projeto_id, nome, n, objetivo, criterios))
                flash("Fases sugeridas criadas. Ajuste nomes, datas e critérios de saída ao seu projeto.", "ok")
        elif acao == "nova":
            nome = f.get("nome", "").strip()
            if not nome:
                flash("Dê um nome à fase.", "erro")
            else:
                ordem = db.execute("SELECT COALESCE(MAX(ordem), 0) + 1 FROM fase WHERE projeto_id = ?", (projeto_id,)).fetchone()[0]
                db.execute("INSERT INTO fase (projeto_id, nome, ordem, objetivo, criterios_saida) VALUES (?, ?, ?, ?, ?)",
                           (projeto_id, nome, ordem, f.get("objetivo", "").strip(), f.get("criterios_saida", "").strip()))
                flash("Fase criada.", "ok")
        tocar_projeto(projeto_id)
        db.commit()
        return redirect(url_for("ciclo.fases", projeto_id=projeto_id))
    return render_template("fases.html", projeto=p, fases=listar_fases(projeto_id), secao="abordagem", sub="fases")


@bp.route("/fases/<int:fase_id>", methods=["POST"])
def fase(projeto_id, fase_id):
    p = obter_projeto(projeto_id)
    db = get_db()
    row = db.execute("SELECT * FROM fase WHERE id = ? AND projeto_id = ?", (fase_id, projeto_id)).fetchone()
    if row is None:
        abort(404)
    f = request.form
    ancora = f"#fase{fase_id}"
    if f.get("acao") == "excluir":
        db.execute("DELETE FROM fase WHERE id = ?", (fase_id,))
        db.commit()
        flash("Fase removida.", "ok")
        return redirect(url_for("ciclo.fases", projeto_id=projeto_id))
    ini, fim = _data(f.get("inicio")), _data(f.get("fim"))
    if ini and fim and fim < ini:
        flash("O término da fase não pode ser antes do início.", "erro")
        return redirect(url_for("ciclo.fases", projeto_id=projeto_id) + ancora)
    criterios = f.get("criterios_saida", "").strip()
    n_criterios = len([c for c in criterios.splitlines() if c.strip()])
    marcados = sorted({i for i in (inteiro(x, 0, 1000) for x in f.getlist("criterio_ok")) if i is not None and i < n_criterios})
    status = f.get("status") if f.get("status") in dict(pmbok.STATUS_FASE) else row["status"]
    decisao = f.get("revisao_decisao") if f.get("revisao_decisao") in dict(pmbok.DECISOES_PORTAO) else ""
    revisao_por = f.get("revisao_por", "").strip()
    if status == "concluida" and row["status"] != "concluida":
        # Revisão de fase (phase gate): os critérios de saída precisam ter sido atingidos (2.3.5)
        if len(marcados) < n_criterios:
            flash("Para concluir a fase, todos os critérios de saída precisam estar atendidos na revisão de fase.", "erro")
            status = row["status"]
        elif not decisao or not revisao_por:
            flash("Para concluir a fase, registre a decisão da revisão de fase e quem decidiu.", "erro")
            status = row["status"]
        elif decisao == "repetir":
            flash("A decisão foi repetir ou estender a fase, então ela continua em andamento.", "aviso")
            status = "em_andamento"
    revisao_data = row["revisao_data"]
    if decisao and decisao != row["revisao_decisao"]:
        revisao_data = date.today().isoformat()
    db.execute(
        """UPDATE fase SET nome = ?, inicio = ?, fim = ?, objetivo = ?, criterios_saida = ?, criterios_ok = ?, status = ?,
           revisao_data = ?, revisao_decisao = ?, revisao_por = ?, revisao_notas = ?, ordem = ? WHERE id = ?""",
        (f.get("nome", "").strip() or row["nome"], ini.isoformat() if ini else None, fim.isoformat() if fim else None,
         f.get("objetivo", "").strip(), criterios, json.dumps(marcados), status, revisao_data, decisao, revisao_por,
         f.get("revisao_notas", "").strip(), inteiro(f.get("ordem"), 1, 1000) or row["ordem"], fase_id))
    tocar_projeto(projeto_id)
    db.commit()
    if status == "concluida" and row["status"] != "concluida":
        flash(f"Fase “{row['nome']}” concluída." + (" A decisão foi encerrar o projeto: veja a página de encerramento." if decisao == "encerrar" else ""), "ok")
        if decisao == "encerrar":
            return redirect(url_for("ciclo.encerramento", projeto_id=projeto_id))
    elif status == row["status"] or status == "em_andamento":
        flash("Fase atualizada.", "ok")
    return redirect(url_for("ciclo.fases", projeto_id=projeto_id) + ancora)


# --------------------------------------------------------------------------
# Tailoring
# --------------------------------------------------------------------------
def diagnostico(projeto):
    """Situações comuns e sugestões de tailoring (Tabela 3-1), detectadas a partir dos registros do projeto."""
    import entrega
    import medicao
    import partes
    import trabalho
    pid = projeto["id"]
    db = get_db()
    achados = []
    coq = entrega.custo_qualidade(pid)
    if coq["nao_conformidade"] > coq["conformidade"] and coq["nao_conformidade"] > 0:
        achados.append(("Entregas com baixa qualidade: o custo de falhas supera o de prevenção e avaliação.",
                        "Adicionar mais ciclos de feedback e verificação e etapas de garantia da qualidade."))
    pendentes = [m for m in trabalho.listar_mudancas(projeto) if m["decisao_atrasada"]]
    if pendentes:
        achados.append((f"Longas esperas por aprovação: {len(pendentes)} mudança(s) aguardam decisão há mais de {trabalho.DIAS_DECISAO_PENDENTE} dias.",
                        "Agilizar as aprovações com menos pessoas autorizadas a decidir até certos valores."))
    itens = entrega.listar_itens(pid)
    trab = entrega.folhas(itens)
    wip = sum(1 for i in trab if i["status"] == "em_andamento")
    if (projeto["limite_wip"] and wip > projeto["limite_wip"]) or (not projeto["limite_wip"] and wip >= 5 and wip > len(trab) / 2):
        achados.append((f"Muito trabalho em andamento ({wip} itens).",
                        "Usar mapeamento do fluxo de valor e quadros kanban para visualizar o trabalho e achar os gargalos."))
    sats = [s["ultima_satisfacao"] for s in partes.listar_partes(pid) if s["ultima_satisfacao"]]
    if sats and sum(sats) / len(sats) < 3:
        achados.append(("Partes interessadas pouco engajadas ou com feedback negativo.",
                        "Verificar se a informação compartilhada é suficiente, se os ciclos de feedback funcionam e se um engajamento mais profundo funcionaria melhor do que só comunicar."))
    ultimo_rel = db.execute("SELECT MAX(data) FROM relatorio_status WHERE projeto_id = ?", (pid,)).fetchone()[0]
    sem_metricas = not medicao.listar_metricas(pid)
    antigo = (date.today() - timedelta(days=30)).isoformat()
    if trab and (not ultimo_rel or ultimo_rel < antigo) and sem_metricas:
        achados.append(("Pouca visibilidade do progresso: nenhum relatório de status recente e nenhum indicador definido.",
                        "Garantir que as medidas certas são coletadas, analisadas e discutidas nas reuniões da equipe e com as partes interessadas."))
    sem_origem = db.execute("SELECT COUNT(*) FROM questao WHERE projeto_id = ? AND risco_id IS NULL AND criado_em >= ?",
                            (pid, (date.today() - timedelta(days=60)).isoformat())).fetchone()[0]
    if sem_origem >= 3:
        achados.append((f"Questões para as quais a equipe não estava preparada continuam surgindo ({sem_origem} sem risco previsto nos últimos 60 dias).",
                        "Investigar as causas-raiz para achar lacunas nos processos ou atividades do projeto, incluindo a identificação de riscos."))
    import equipe
    av = equipe.avaliacoes(pid)
    if av and av[-1]["notas"].get("entendimento") and av[-1]["notas"]["entendimento"] <= 2:
        achados.append(("Membros da equipe sem clareza de como seguir com o trabalho.",
                        "Adicionar mais orientação, treinamento e etapas de verificação."))
    return [{"situacao": s, "sugestao": g} for s, g in achados]


@bp.route("/tailoring", methods=["GET", "POST"])
def tailoring(projeto_id):
    p = obter_projeto(projeto_id)
    db = get_db()
    if request.method == "POST":
        f = request.form
        acao = f.get("acao")
        if acao == "respostas":
            respostas = {k: f.get(k, "").strip() for _, k, *_ in pmbok.PERGUNTAS_TAILORING if f.get(k, "").strip()}
            db.execute("UPDATE projeto SET tailoring_json = ? WHERE id = ?", (json.dumps(respostas, ensure_ascii=False), projeto_id))
            flash("Respostas salvas.", "ok")
        elif acao == "decisao":
            elemento = f.get("elemento", "").strip()
            if not elemento or f.get("tipo") not in dict(pmbok.TIPOS_DECISAO_TAILORING):
                flash("Informe o que foi adicionado, removido ou ajustado.", "erro")
            else:
                db.execute("INSERT INTO decisao_tailoring (projeto_id, data, tipo, elemento, motivo, origem) VALUES (?, ?, ?, ?, ?, ?)",
                           (projeto_id, date.today().isoformat(), f.get("tipo"), elemento, f.get("motivo", "").strip(), f.get("origem", "").strip()))
                flash("Decisão de tailoring registrada.", "ok")
        elif acao == "excluir":
            db.execute("DELETE FROM decisao_tailoring WHERE id = ? AND projeto_id = ?", (inteiro(f.get("decisao_id"), 1, 10**9), projeto_id))
            flash("Decisão removida.", "ok")
        tocar_projeto(projeto_id)
        db.commit()
        return redirect(url_for("ciclo.tailoring", projeto_id=projeto_id))
    decisoes = db.execute("SELECT * FROM decisao_tailoring WHERE projeto_id = ? ORDER BY data DESC, id DESC", (projeto_id,)).fetchall()
    return render_template("tailoring.html", projeto=p, respostas=json.loads(p["tailoring_json"] or "{}"), decisoes=decisoes,
                           diagnostico=diagnostico(p), secao="abordagem", sub="tailoring")


# --------------------------------------------------------------------------
# Encerramento
# --------------------------------------------------------------------------
def checklist_encerramento(projeto):
    import entrega
    import equipe
    import incerteza
    import medicao
    import trabalho
    pid = projeto["id"]
    db = get_db()
    manual = json.loads(projeto["encerramento_json"] or "{}").get("manual", {})
    itens = entrega.folhas(entrega.listar_itens(pid))
    abertos = [i for i in itens if i["status"] not in ("aceito", "cancelado")]
    questoes = [q for q in trabalho.listar_questoes(pid) if q["aberta"]]
    riscos = [r for r in incerteza.listar_riscos(projeto) if r["status"] in ("aberto", "em_resposta", "ocorreu")]
    mudancas = [m for m in trabalho.listar_mudancas(projeto) if m["status"] in ("solicitada", "em_analise", "aprovada")]
    beneficios = db.execute("SELECT COUNT(*) FROM beneficio WHERE projeto_id = ? AND status = 'planejado'", (pid,)).fetchone()[0]
    licoes = db.execute("SELECT COUNT(*) FROM licao WHERE projeto_id = ?", (pid,)).fetchone()[0]
    fases = [f for f in listar_fases(pid) if f["status"] != "concluida" and f["nome"].lower() != "encerramento"]
    membros = equipe.listar_membros(pid, so_ativos=True)
    import principios
    conformidade_aberta = [r for r in principios.listar_conformidade(pid) if r["status"] in ("pendente", "em_andamento")]
    grupos = principios.listar_grupos(pid)
    sem_adocao = [g for g in grupos if g["status"] != "adotado"]
    import suprimentos
    aquisicoes_abertas = [a for a in suprimentos.listar_aquisicoes(pid) if a["ativa"]]
    auto = [
        ("Todas as entregas aceitas ou canceladas", not abertos, f"{len(abertos)} item(ns) ainda não aceitos", url_for("entrega.itens", projeto_id=pid)),
        ("Mudanças decididas e implementadas", not mudancas, f"{len(mudancas)} mudança(s) pendentes ou não implementadas", url_for("trabalho.mudancas", projeto_id=pid)),
        ("Questões resolvidas", not questoes, f"{len(questoes)} questão(ões) abertas", url_for("trabalho.questoes", projeto_id=pid)),
        ("Riscos encerrados", not riscos, f"{len(riscos)} risco(s) não encerrados", url_for("incerteza.riscos", projeto_id=pid, status="todos")),
        ("Benefícios avaliados (os de longo prazo podem ficar como parciais)", beneficios == 0, f"{beneficios} benefício(s) ainda só planejados", url_for("entrega.beneficios", projeto_id=pid)),
        ("Lições aprendidas registradas", licoes > 0, "nenhuma lição registrada", url_for("trabalho.licoes", projeto_id=pid)),
        ("Fases anteriores concluídas com revisão", not fases, f"{len(fases)} fase(s) sem revisão", url_for("ciclo.fases", projeto_id=pid)),
        ("Aquisições encerradas ou canceladas, com o fornecedor avaliado", not aquisicoes_abertas, f"{len(aquisicoes_abertas)} aquisição(ões) ainda em andamento", url_for("suprimentos.painel", projeto_id=pid)),
        ("Requisitos de conformidade atendidos", not conformidade_aberta, f"{len(conformidade_aberta)} requisito(s) em aberto", url_for("principios.conformidade", projeto_id=pid)),
        ("Mudança organizacional: grupos afetados adotaram a entrega", not sem_adocao, f"{len(sem_adocao)} grupo(s) ainda não adotaram", url_for("principios.adocao", projeto_id=pid)),
        ("Equipe liberada", not membros, f"{len(membros)} membro(s) ainda ativos", url_for("equipe.membros", projeto_id=pid)),
    ]
    manuais = [
        ("contratos", "Contratos e aquisições encerrados"),
        ("arquivo", "Conhecimento e artefatos do projeto arquivados"),
        ("transicao", "Entregas transferidas para a operação ou sustentação"),
        ("termo_revisado", "Termo de abertura e business case revisados para saber se os benefícios pretendidos foram alcançados"),
    ]
    va = medicao.valor_agregado(projeto, entrega.listar_itens(pid))
    return {
        "auto": [{"rotulo": r, "ok": ok, "pendencia": pend, "link": lk} for r, ok, pend, lk in auto],
        "manual": [{"chave": k, "rotulo": r, "ok": bool(manual.get(k))} for k, r in manuais],
        "comparacao": {
            "escopo_total": len(itens), "escopo_aceito": sum(1 for i in itens if i["status"] == "aceito"),
            "orcamento": va["onp"] if va else None, "custo_real": va["cr"] if va else None,
            "fim_planejado": projeto["data_fim_planejada"],
        },
    }


@bp.route("/encerramento", methods=["GET", "POST"])
def encerramento(projeto_id):
    p = obter_projeto(projeto_id)
    db = get_db()
    dados = json.loads(p["encerramento_json"] or "{}")
    if request.method == "POST":
        f = request.form
        acao = f.get("acao")
        if acao == "reabrir":
            db.execute("UPDATE projeto SET situacao = 'ativo', encerrado_em = NULL WHERE id = ?", (projeto_id,))
            flash("Projeto reaberto.", "ok")
        else:
            dados["manual"] = {k: bool(f.get(f"manual_{k}")) for k in ("contratos", "arquivo", "transicao", "termo_revisado")}
            dados["avaliacao_objetivos"] = f.get("avaliacao_objetivos", "").strip()
            dados["resultado"] = f.get("resultado", "").strip()
            dados["justificativa"] = f.get("justificativa", "").strip()
            dados["recomendacoes"] = f.get("recomendacoes", "").strip()
            db.execute("UPDATE projeto SET encerramento_json = ? WHERE id = ?", (json.dumps(dados, ensure_ascii=False), projeto_id))
            if acao in ("encerrar", "cancelar"):
                db.commit()
                p = obter_projeto(projeto_id)
                check = checklist_encerramento(p)
                pendentes = [x["rotulo"] for x in check["auto"] + check["manual"] if not x["ok"]]
                if acao == "cancelar" and not dados["justificativa"]:
                    flash("Para cancelar o projeto, explique o motivo (ex.: a oportunidade de mercado passou).", "erro")
                elif not dados["avaliacao_objetivos"]:
                    flash("Antes de encerrar, registre a avaliação dos objetivos e benefícios em relação ao termo de abertura.", "erro")
                elif pendentes and acao == "encerrar" and not dados["justificativa"]:
                    flash("Há pendências no checklist (" + "; ".join(pendentes[:3]) + ("…" if len(pendentes) > 3 else "")
                          + "). Resolva-as ou explique na justificativa por que o projeto pode ser encerrado assim mesmo.", "erro")
                else:
                    situacao = "cancelado" if acao == "cancelar" else "encerrado"
                    db.execute("UPDATE projeto SET situacao = ?, encerrado_em = ?, estagio_equipe = 'dissolucao' WHERE id = ?",
                               (situacao, date.today().isoformat(), projeto_id))
                    flash(f"Projeto {situacao}. O histórico continua disponível para consulta.", "ok")
            else:
                flash("Encerramento salvo.", "ok")
        tocar_projeto(projeto_id)
        db.commit()
        return redirect(url_for("ciclo.encerramento", projeto_id=projeto_id))
    licoes_org = db.execute("SELECT * FROM licao WHERE projeto_id = ? AND alcance != 'projeto' ORDER BY data DESC", (projeto_id,)).fetchall()
    objetivos = db.execute("SELECT objetivos, criterios_sucesso FROM abertura WHERE projeto_id = ?", (projeto_id,)).fetchone()
    return render_template("encerramento.html", projeto=p, check=checklist_encerramento(p), dados=dados, licoes_org=licoes_org,
                           objetivos=objetivos, secao="encerramento")
