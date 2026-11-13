"""Aquisições e recursos físicos (PMBOK 7, seções 2.4.5, 2.4.6, 2.5.5 e 2.5.6) — v8.

- Aquisições: decisão de fazer ou comprar, documento de licitação (RFI, RFP, RFQ), tipo de contrato,
  prazos, critérios de desempenho e avaliação do fornecedor. O fornecedor contratado vira parte interessada (2.5.6.2).
- Recursos físicos: materiais, equipamentos, licenças e ambientes, com prazo de pedido, uso e desperdício.
"""
from datetime import date, timedelta

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

import pmbok
from db import get_db
from util import decimal, inteiro, obter_projeto, tocar_projeto

bp = Blueprint("suprimentos", __name__, url_prefix="/p/<int:projeto_id>/suprimentos")

DIAS_AVISO = 30        # aquisição precisa estar contratada com esta antecedência da data de necessidade
DIAS_AVISO_RECURSO = 7  # recurso precisa ser pedido com esta antecedência


def _data(valor):
    try:
        return date.fromisoformat(str(valor)[:10]) if valor else None
    except ValueError:
        return None


def _iso(valor):
    d = _data(valor)
    return d.isoformat() if d else None


# --------------------------------------------------------------------------
# Consultas e regras
# --------------------------------------------------------------------------
def listar_aquisicoes(projeto_id):
    hoje = date.today()
    rows = get_db().execute(
        """SELECT a.*, s.nome AS parte_nome FROM aquisicao a LEFT JOIN parte_interessada s ON s.id = a.parte_id
           WHERE a.projeto_id = ? ORDER BY a.codigo""", (projeto_id,)).fetchall()
    out = []
    for r in rows:
        a = dict(r)
        a["rotulo"] = f"A-{a['codigo']}"
        a["ativa"] = a["status"] in pmbok.STATUS_AQUISICAO_ATIVOS
        a["externa"] = a["decisao"] == "comprar"
        necessario = _data(a["necessario_em"])
        entrega = _data(a["entrega_prevista"])
        a["sem_contrato_a_tempo"] = bool(a["externa"] and a["status"] in ("planejada", "em_licitacao") and necessario
                                         and necessario <= hoje + timedelta(days=DIAS_AVISO))
        a["necessidade_vencida"] = bool(a["sem_contrato_a_tempo"] and necessario < hoje)
        a["entrega_atrasada"] = bool(a["status"] == "contratada" and entrega and entrega < hoje)
        out.append(a)
    return out


def listar_recursos(projeto_id):
    hoje = date.today()
    rows = get_db().execute("SELECT * FROM recurso_fisico WHERE projeto_id = ? ORDER BY necessario_em IS NULL, necessario_em, id",
                            (projeto_id,)).fetchall()
    out = []
    for r in rows:
        x = dict(r)
        necessario = _data(x["necessario_em"])
        pedir_ate = necessario - timedelta(days=x["antecedencia_dias"] or 0) if necessario else None
        x["pedir_ate"] = pedir_ate.isoformat() if pedir_ate else None
        x["pedido_atrasado"] = bool(x["status"] == "planejado" and pedir_ate and pedir_ate < hoje)
        x["pedido_proximo"] = bool(x["status"] == "planejado" and pedir_ate and hoje <= pedir_ate <= hoje + timedelta(days=DIAS_AVISO_RECURSO))
        base = x["usado"] if x["usado"] else None
        x["pct_desperdicio"] = round(100 * x["desperdicio"] / base) if base and x["desperdicio"] else None
        out.append(x)
    return out


def gerar_alertas_suprimentos(projeto):
    pid = projeto["id"]
    link = url_for("suprimentos.painel", projeto_id=pid)
    alertas = []
    for a in listar_aquisicoes(pid):
        nome = f"{a['rotulo']} ({a['item']})"
        if a["necessidade_vencida"]:
            alertas.append(("alto", f"{nome} era necessária em {_data(a['necessario_em']).strftime('%d/%m/%Y')} e ainda não foi contratada.", link + f"#a{a['id']}"))
        elif a["sem_contrato_a_tempo"]:
            alertas.append(("medio", f"{nome} é necessária em {_data(a['necessario_em']).strftime('%d/%m/%Y')} e ainda não foi contratada.", link + f"#a{a['id']}"))
        if a["entrega_atrasada"]:
            alertas.append(("alto", f"{nome}: a entrega do fornecedor passou da data prevista ({_data(a['entrega_prevista']).strftime('%d/%m/%Y')}).", link + f"#a{a['id']}"))
        if a["externa"] and a["fornecedor"] and not a["parte_id"] and a["status"] in ("contratada", "entregue"):
            alertas.append(("info", f"{nome}: o fornecedor contratado passa a ser parte interessada. Cadastre-o para acompanhá-lo (2.5.6.2).", link + f"#a{a['id']}"))
        if (a["entrega_prevista"] and a["necessario_em"] and a["entrega_prevista"] > a["necessario_em"]
                and a["status"] not in ("entregue", "encerrada", "cancelada")):
            alertas.append(("alto", f"{nome}: o fornecedor promete entregar em {_data(a['entrega_prevista']).strftime('%d/%m/%Y')}, "
                                    f"depois da data em que o projeto precisa ({_data(a['necessario_em']).strftime('%d/%m/%Y')}).", link + f"#a{a['id']}"))
        if a["nota_desempenho"] and a["nota_desempenho"] <= 2 and a["status"] != "cancelada":
            alertas.append(("medio", f"{nome}: o desempenho do fornecedor foi avaliado com nota {a['nota_desempenho']}.", link + f"#a{a['id']}"))
    for r in listar_recursos(pid):
        if r["pedido_atrasado"]:
            alertas.append(("alto", f"“{r['nome']}” devia ter sido pedido até {_data(r['pedir_ate']).strftime('%d/%m/%Y')} para chegar a tempo.", link + f"#r{r['id']}"))
        elif r["pedido_proximo"]:
            alertas.append(("medio", f"“{r['nome']}” precisa ser pedido até {_data(r['pedir_ate']).strftime('%d/%m/%Y')}.", link + f"#r{r['id']}"))
        if r["quantidade"] and r["usado"] and r["usado"] > r["quantidade"]:
            alertas.append(("medio", f"“{r['nome']}”: já foi usado mais do que o planejado ({r['usado']:g} de {r['quantidade']:g}). Revise a estimativa.", link + f"#r{r['id']}"))
        if r["pct_desperdicio"] is not None and r["pct_desperdicio"] >= 15:
            alertas.append(("info", f"“{r['nome']}” tem {r['pct_desperdicio']}% de desperdício: veja como reduzir sucata e retrabalho.", link + f"#r{r['id']}"))
    return [{"nivel": n, "texto": t, "link": lk} for n, t, lk in alertas]


def indicadores(projeto):
    pid = projeto["id"]
    aq, rec = listar_aquisicoes(pid), listar_recursos(pid)
    ind = []
    if aq:
        ativas = [a for a in aq if a["ativa"]]
        notas = [a["nota_desempenho"] for a in aq if a["nota_desempenho"]]
        ind.append(f"Aquisições: {len(aq)} registradas, {len(ativas)} em andamento, {sum(1 for a in aq if a['entrega_atrasada'])} com entrega atrasada.")
        if notas:
            ind.append(f"Desempenho médio dos fornecedores avaliados: {sum(notas) / len(notas):.1f}/5.")
    if rec:
        ind.append(f"Recursos físicos: {len(rec)} planejados, {sum(1 for r in rec if r['pedido_atrasado'])} com pedido atrasado.")
    return ind


# --------------------------------------------------------------------------
# Tela
# --------------------------------------------------------------------------
def _parte_valida(projeto_id, parte_id):
    if parte_id and get_db().execute("SELECT 1 FROM parte_interessada WHERE id = ? AND projeto_id = ?", (parte_id, projeto_id)).fetchone():
        return parte_id
    return None


@bp.route("", methods=["GET", "POST"])
def painel(projeto_id):
    p = obter_projeto(projeto_id)
    db = get_db()
    destino = url_for("suprimentos.painel", projeto_id=projeto_id)
    if request.method == "POST":
        f = request.form
        acao = f.get("acao")
        rid = inteiro(f.get("registro_id"), 1, 10**9)
        if acao in ("excluir_aquisicao", "fornecedor_parte") or (acao == "aquisicao" and rid):
            if rid and not db.execute("SELECT 1 FROM aquisicao WHERE id = ? AND projeto_id = ?", (rid, projeto_id)).fetchone():
                abort(404)
        if acao in ("excluir_recurso",) or (acao == "recurso" and rid):
            if rid and not db.execute("SELECT 1 FROM recurso_fisico WHERE id = ? AND projeto_id = ?", (rid, projeto_id)).fetchone():
                abort(404)

        if acao == "aquisicao":
            item = f.get("item", "").strip()
            escolha = lambda campo, lista, padrao: f.get(campo) if f.get(campo) in dict(lista) else padrao  # noqa: E731
            decisao = escolha("decisao", pmbok.DECISOES_FAZER_COMPRAR, "comprar")
            status = escolha("status", pmbok.STATUS_AQUISICAO, "planejada")
            fornecedor = f.get("fornecedor", "").strip()
            nota = inteiro(f.get("nota_desempenho"))
            erro = None
            if not item:
                erro = "Descreva o que será adquirido."
            elif decisao == "comprar" and status in ("contratada", "entregue", "encerrada") and not fornecedor:
                erro = "Para marcar como contratada, entregue ou encerrada, informe o fornecedor."
            elif status == "encerrada" and not nota:
                erro = "Antes de encerrar, avalie o desempenho do fornecedor (nota de 1 a 5): isso ajuda nas próximas compras."
            if erro:
                flash(erro, "erro")
                return redirect(destino + (f"#a{rid}" if rid else ""))
            valores = (item, decisao, fornecedor, _parte_valida(projeto_id, inteiro(f.get("parte_id"), 1, 10**9)),
                       escolha("documento", pmbok.DOCUMENTOS_LICITACAO, ""), escolha("contrato", pmbok.TIPOS_CONTRATO, ""),
                       decimal(f.get("valor")), _iso(f.get("necessario_em")), _iso(f.get("entrega_prevista")), status,
                       f.get("criterios", "").strip(), nota, f.get("observacoes", "").strip())
            if rid:
                db.execute("""UPDATE aquisicao SET item = ?, decisao = ?, fornecedor = ?, parte_id = ?, documento = ?, contrato = ?, valor = ?,
                              necessario_em = ?, entrega_prevista = ?, status = ?, criterios = ?, nota_desempenho = ?, observacoes = ?,
                              atualizado_em = datetime('now','localtime') WHERE id = ?""", valores + (rid,))
                flash("Aquisição atualizada.", "ok")
            else:
                codigo = db.execute("SELECT COALESCE(MAX(codigo), 0) + 1 FROM aquisicao WHERE projeto_id = ?", (projeto_id,)).fetchone()[0]
                db.execute("""INSERT INTO aquisicao (projeto_id, codigo, item, decisao, fornecedor, parte_id, documento, contrato, valor,
                              necessario_em, entrega_prevista, status, criterios, nota_desempenho, observacoes)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (projeto_id, codigo) + valores)
                flash("Aquisição registrada.", "ok")
        elif acao == "excluir_aquisicao":
            db.execute("DELETE FROM aquisicao WHERE id = ?", (rid,))
            flash("Aquisição removida.", "ok")
        elif acao == "fornecedor_parte":
            a = db.execute("SELECT * FROM aquisicao WHERE id = ?", (rid,)).fetchone()
            if not a["fornecedor"]:
                flash("Informe o nome do fornecedor antes.", "erro")
            elif not a["parte_id"]:
                cur = db.execute("""INSERT INTO parte_interessada (projeto_id, nome, papel, categoria, interna, ativa)
                                    VALUES (?, ?, ?, 'Fornecedor', 0, 1)""", (projeto_id, a["fornecedor"], f"Fornecedor de {a['item']}"))
                db.execute("UPDATE aquisicao SET parte_id = ? WHERE id = ?", (cur.lastrowid, rid))
                flash("Fornecedor cadastrado como parte interessada. Analise poder, interesse e atitude dele na etapa 2 das partes interessadas.", "ok")
        elif acao == "recurso":
            nome = f.get("nome", "").strip()
            if not nome:
                flash("Dê um nome ao recurso.", "erro")
                return redirect(destino)
            usado, desperdicio = decimal(f.get("usado")), decimal(f.get("desperdicio"))
            if desperdicio and desperdicio > (usado or 0):
                flash("O desperdício não pode ser maior que o total usado (o desperdício faz parte do que foi consumido).", "erro")
                return redirect(destino + (f"#r{rid}" if rid else ""))
            escolha = lambda campo, lista, padrao: f.get(campo) if f.get(campo) in dict(lista) else padrao  # noqa: E731
            valores = (nome, escolha("tipo", pmbok.TIPOS_RECURSO, "equipamento"), decimal(f.get("quantidade")), f.get("unidade", "").strip(),
                       decimal(f.get("usado")), decimal(f.get("desperdicio")), _iso(f.get("necessario_em")),
                       inteiro(f.get("antecedencia_dias"), 0, 730), escolha("status", pmbok.STATUS_RECURSO, "planejado"),
                       f.get("armazenamento_descarte", "").strip())
            if rid:
                db.execute("""UPDATE recurso_fisico SET nome = ?, tipo = ?, quantidade = ?, unidade = ?, usado = ?, desperdicio = ?, necessario_em = ?,
                              antecedencia_dias = ?, status = ?, armazenamento_descarte = ?, atualizado_em = datetime('now','localtime')
                              WHERE id = ?""", valores + (rid,))
                flash("Recurso atualizado.", "ok")
            else:
                db.execute("""INSERT INTO recurso_fisico (projeto_id, nome, tipo, quantidade, unidade, usado, desperdicio, necessario_em,
                              antecedencia_dias, status, armazenamento_descarte) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (projeto_id,) + valores)
                flash("Recurso registrado.", "ok")
        elif acao == "excluir_recurso":
            db.execute("DELETE FROM recurso_fisico WHERE id = ?", (rid,))
            flash("Recurso removido.", "ok")
        tocar_projeto(projeto_id)
        db.commit()
        return redirect(destino + (f"#a{rid}" if rid and acao in ("aquisicao", "fornecedor_parte") else ""))
    partes = [(r["id"], r["nome"]) for r in db.execute("SELECT id, nome FROM parte_interessada WHERE projeto_id = ? AND ativa = 1 ORDER BY nome", (projeto_id,))]
    return render_template("suprimentos.html", projeto=p, aquisicoes=listar_aquisicoes(projeto_id), recursos=listar_recursos(projeto_id),
                           partes=partes, secao="suprimentos")
