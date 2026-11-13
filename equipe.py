"""Domínio de desempenho Equipe (PMBOK 7, seção 2.2).

Membros, modelo de liderança e estágio da equipe, acordo de trabalho
(team charter), matriz RACI e avaliação dos fatores de alto desempenho.
"""
import json
from datetime import date, timedelta

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

import graficos
import pmbok
from db import get_db
from util import inteiro, obter_projeto, tocar_projeto

bp = Blueprint("equipe", __name__, url_prefix="/p/<int:projeto_id>/equipe")

CAMPOS_ACORDO = ["acordo_valores", "acordo_comunicacao", "acordo_decisoes", "acordo_conflitos", "acordo_reunioes"]
DIAS_SEM_AVALIACAO = 45
TAMANHO_ADAPTATIVO = 9  # equipes de 7 ± 2 (2.3.4.3)


def listar_membros(projeto_id, so_ativos=False):
    sql = """SELECT m.*, s.nome AS parte_nome FROM membro m LEFT JOIN parte_interessada s ON s.id = m.parte_id
             WHERE m.projeto_id = ?"""
    if so_ativos:
        sql += " AND m.ativo = 1"
    return get_db().execute(sql + " ORDER BY m.ativo DESC, m.nome", (projeto_id,)).fetchall()


def raci(projeto_id):
    db = get_db()
    linhas = db.execute(
        """SELECT r.*, i.codigo AS item_codigo FROM raci_linha r LEFT JOIN item i ON i.id = r.item_id
           WHERE r.projeto_id = ? ORDER BY COALESCE(r.ordem, 1000000), r.id""", (projeto_id,)
    ).fetchall()
    papeis = {}
    for p in db.execute("""SELECT rp.* FROM raci_papel rp JOIN raci_linha r ON r.id = rp.linha_id WHERE r.projeto_id = ?""", (projeto_id,)):
        papeis.setdefault(p["linha_id"], {})[p["membro_id"]] = p["papel"]
    out = []
    for linha in linhas:
        atrib = papeis.get(linha["id"], {})
        n_a = sum(1 for v in atrib.values() if v == "A")
        problemas = []
        if n_a == 0:
            problemas.append("ninguém aprova (A)")
        elif n_a > 1:
            problemas.append("mais de um aprovador (A)")
        if not any(v == "R" for v in atrib.values()):
            problemas.append("ninguém executa (R)")
        out.append({**dict(linha), "papeis": atrib, "problemas": problemas})
    return out


def avaliacoes(projeto_id):
    rows = get_db().execute("SELECT * FROM avaliacao_equipe WHERE projeto_id = ? ORDER BY data, id", (projeto_id,)).fetchall()
    out = []
    for r in rows:
        notas = json.loads(r["notas_json"] or "{}")
        validas = [v for v in notas.values() if v]
        out.append({**dict(r), "notas": notas, "media": sum(validas) / len(validas) if validas else None})
    return out


def resumo_equipe(projeto):
    pid = projeto["id"]
    membros = listar_membros(pid, so_ativos=True)
    avs = avaliacoes(pid)
    ultima = avs[-1] if avs else None
    fracos = []
    if ultima:
        fracos = [nome for k, nome, _ in pmbok.FATORES_ALTO_DESEMPENHO if (ultima["notas"].get(k) or 5) <= 2]
    linhas_raci = raci(pid)
    return {
        "membros": len(membros),
        "remotos": sum(1 for m in membros if m["local"] == "remoto"),
        "com_lacunas": sum(1 for m in membros if (m["lacunas"] or "").strip()),
        "lacunas_sem_plano": [m for m in membros if (m["lacunas"] or "").strip() and not (m["plano_desenvolvimento"] or "").strip()],
        "acordo": sum(1 for c in CAMPOS_ACORDO if (projeto[c] or "").strip()),
        "avaliacoes": len(avs),
        "ultima": ultima,
        "fracos": fracos,
        "raci_linhas": len(linhas_raci),
        "raci_problemas": [x for x in linhas_raci if x["problemas"]],
    }


def gerar_alertas_equipe(projeto):
    pid = projeto["id"]
    r = resumo_equipe(projeto)
    alertas = []
    if r["membros"] == 0:
        alertas.append(("info", "Nenhum membro da equipe cadastrado.", url_for("equipe.membros", projeto_id=pid)))
        return [{"nivel": n, "texto": t, "link": lk} for n, t, lk in alertas]
    if r["acordo"] == 0:
        alertas.append(("medio", "A equipe ainda não tem acordo de trabalho (valores, comunicação, decisões e conflitos).",
                        url_for("equipe.acordo", projeto_id=pid)))
    for x in r["raci_problemas"]:
        alertas.append(("medio", f"Matriz RACI, “{x['descricao']}”: {' e '.join(x['problemas'])}.", url_for("equipe.matriz", projeto_id=pid)))
    for m in r["lacunas_sem_plano"]:
        alertas.append(("info", f"{m['nome']} tem lacunas de habilidade sem plano de desenvolvimento.",
                        url_for("equipe.membro", projeto_id=pid, membro_id=m["id"])))
    if r["fracos"]:
        alertas.append(("medio", "Na última avaliação da equipe, estes fatores ficaram baixos (≤ 2): " + ", ".join(r["fracos"]) + ".",
                        url_for("equipe.saude", projeto_id=pid)))
    limite = (date.today() - timedelta(days=DIAS_SEM_AVALIACAO)).isoformat()
    if r["avaliacoes"] == 0 or r["ultima"]["data"] < limite:
        alertas.append(("info", f"A equipe não faz uma avaliação de saúde há mais de {DIAS_SEM_AVALIACAO} dias.", url_for("equipe.saude", projeto_id=pid)))
    if projeto["abordagem"] == "adaptativa" and r["membros"] > TAMANHO_ADAPTATIVO:
        alertas.append(("info", f"Abordagens adaptativas costumam funcionar melhor com equipes de 7 ± 2 pessoas; esta tem {r['membros']}.",
                        url_for("equipe.membros", projeto_id=pid)))
    return [{"nivel": n, "texto": t, "link": lk} for n, t, lk in alertas]


def indicadores(projeto):
    r = resumo_equipe(projeto)
    ind = [f"{r['membros']} membros ativos ({r['remotos']} remotos); {r['com_lacunas']} com lacunas de habilidade identificadas."]
    if projeto["estagio_equipe"]:
        ind.append("Estágio da equipe (Tuckman): " + {k: n for k, n, _ in pmbok.ESTAGIOS_EQUIPE}[projeto["estagio_equipe"]] + ".")
    ind.append(f"Acordo de trabalho: {r['acordo']} de {len(CAMPOS_ACORDO)} seções preenchidas.")
    ind.append(f"Matriz RACI: {r['raci_linhas']} linhas, {len(r['raci_problemas'])} com problema.")
    if r["ultima"] and r["ultima"]["media"]:
        ind.append(f"Última avaliação de alto desempenho ({r['ultima']['data'][8:10]}/{r['ultima']['data'][5:7]}): "
                   f"média {graficos.numero(r['ultima']['media'])}/5.")
    return ind


# --------------------------------------------------------------------------
# Rotas
# --------------------------------------------------------------------------
def _usuario_valido(valor):
    uid = inteiro(valor, 1, 10**9)
    if uid and get_db().execute("SELECT 1 FROM usuario WHERE id = ? AND ativo = 1", (uid,)).fetchone():
        return uid
    return None


@bp.app_context_processor
def contexto_usuarios():
    return {"usuarios_ativos": lambda: get_db().execute("SELECT id, nome, login FROM usuario WHERE ativo = 1 ORDER BY nome").fetchall()}


def _ler_membro(projeto_id):
    f = request.form
    parte = inteiro(f.get("parte_id"), 1, 10**9)
    if parte and not get_db().execute("SELECT 1 FROM parte_interessada WHERE id = ? AND projeto_id = ?", (parte, projeto_id)).fetchone():
        parte = None
    motivador = f.get("motivador", "")
    return {
        "nome": f.get("nome", "").strip(), "papel": f.get("papel", "").strip(),
        "dedicacao": f.get("dedicacao") if f.get("dedicacao") in dict(pmbok.DEDICACOES) else "integral",
        "local": f.get("local") if f.get("local") in dict(pmbok.LOCAIS) else "presencial",
        "habilidades": f.get("habilidades", "").strip(), "lacunas": f.get("lacunas", "").strip(),
        "plano_desenvolvimento": f.get("plano_desenvolvimento", "").strip(),
        "motivador": motivador if motivador in pmbok.MOTIVADORES else "", "parte_id": parte,
        "usuario_id": _usuario_valido(f.get("usuario_id")),
    }


@bp.route("", methods=["GET", "POST"])
def membros(projeto_id):
    p = obter_projeto(projeto_id)
    db = get_db()
    if request.method == "POST":
        f = request.form
        if f.get("acao") == "lideranca":
            modelo, estagio = f.get("modelo_lideranca", ""), f.get("estagio_equipe", "")
            db.execute("UPDATE projeto SET modelo_lideranca = ?, estagio_equipe = ? WHERE id = ?",
                       (modelo if modelo in dict(pmbok.MODELOS_LIDERANCA) else "",
                        estagio if estagio in {k for k, *_ in pmbok.ESTAGIOS_EQUIPE} else "", projeto_id))
            flash("Liderança e estágio da equipe salvos.", "ok")
        else:
            dados = _ler_membro(projeto_id)
            if not dados["nome"]:
                flash("Informe o nome do membro.", "erro")
                return redirect(url_for("equipe.membros", projeto_id=projeto_id))
            cols = list(dados)
            db.execute(f"INSERT INTO membro (projeto_id, {', '.join(cols)}) VALUES (?, {', '.join('?' for _ in cols)})",
                       [projeto_id] + [dados[c] for c in cols])
            flash(f"{dados['nome']} adicionado à equipe.", "ok")
        tocar_projeto(projeto_id)
        db.commit()
        return redirect(url_for("equipe.membros", projeto_id=projeto_id))
    partes = db.execute("SELECT id, nome FROM parte_interessada WHERE projeto_id = ? AND ativa = 1 ORDER BY nome", (projeto_id,)).fetchall()
    return render_template("equipe.html", projeto=p, membros=listar_membros(projeto_id), partes=partes,
                           resumo=resumo_equipe(p), alertas=gerar_alertas_equipe(p), secao="equipe", sub="membros")


@bp.route("/membros/<int:membro_id>", methods=["GET", "POST"])
def membro(projeto_id, membro_id):
    p = obter_projeto(projeto_id)
    db = get_db()
    m = db.execute("SELECT * FROM membro WHERE id = ? AND projeto_id = ?", (membro_id, projeto_id)).fetchone()
    if m is None:
        abort(404)
    if request.method == "POST":
        acao = request.form.get("acao")
        if acao == "excluir":
            db.execute("DELETE FROM membro WHERE id = ?", (membro_id,))
            db.commit()
            flash(f"{m['nome']} removido da equipe.", "ok")
            return redirect(url_for("equipe.membros", projeto_id=projeto_id))
        if acao in ("liberar", "reativar"):
            liberar = acao == "liberar"
            db.execute("UPDATE membro SET ativo = ?, liberado_em = ? WHERE id = ?",
                       (0 if liberar else 1, date.today().isoformat() if liberar else None, membro_id))
            flash(f"{m['nome']} {'liberado do projeto' if liberar else 'de volta à equipe'}.", "ok")
        else:
            dados = _ler_membro(projeto_id)
            if not dados["nome"]:
                flash("Informe o nome do membro.", "erro")
                return redirect(url_for("equipe.membro", projeto_id=projeto_id, membro_id=membro_id))
            db.execute("UPDATE membro SET " + ", ".join(f"{c} = ?" for c in dados) + " WHERE id = ?", list(dados.values()) + [membro_id])
            flash("Membro atualizado.", "ok")
        tocar_projeto(projeto_id)
        db.commit()
        return redirect(url_for("equipe.membro", projeto_id=projeto_id, membro_id=membro_id))
    partes = db.execute("SELECT id, nome FROM parte_interessada WHERE projeto_id = ? AND ativa = 1 ORDER BY nome", (projeto_id,)).fetchall()
    papeis = db.execute(
        """SELECT r.descricao, rp.papel FROM raci_papel rp JOIN raci_linha r ON r.id = rp.linha_id WHERE rp.membro_id = ? ORDER BY r.id""",
        (membro_id,)).fetchall()
    return render_template("membro.html", projeto=p, m=m, partes=partes, papeis=papeis, secao="equipe", sub="membros")


@bp.route("/acordo", methods=["GET", "POST"])
def acordo(projeto_id):
    p = obter_projeto(projeto_id)
    if request.method == "POST":
        db = get_db()
        valores = [request.form.get(c, "").strip() for c in CAMPOS_ACORDO]
        db.execute("UPDATE projeto SET " + ", ".join(f"{c} = ?" for c in CAMPOS_ACORDO)
                   + ", acordo_atualizado_em = date('now','localtime') WHERE id = ?", valores + [projeto_id])
        tocar_projeto(projeto_id)
        db.commit()
        flash("Acordo de trabalho da equipe salvo.", "ok")
        return redirect(url_for("equipe.acordo", projeto_id=projeto_id))
    return render_template("acordo.html", projeto=p, secao="equipe", sub="acordo")


@bp.route("/raci", methods=["GET", "POST"])
def matriz(projeto_id):
    p = obter_projeto(projeto_id)
    db = get_db()
    membros_ = listar_membros(projeto_id, so_ativos=True)
    if request.method == "POST":
        f = request.form
        acao = "excluir" if f.get("excluir_linha") else f.get("acao")
        if acao == "linha":
            descricao = f.get("descricao", "").strip()
            item_id = inteiro(f.get("item_id"), 1, 10**9)
            if item_id:
                item = db.execute("SELECT codigo, titulo FROM item WHERE id = ? AND projeto_id = ?", (item_id, projeto_id)).fetchone()
                if item is None:
                    item_id = None
                elif not descricao:
                    descricao = f"I-{item['codigo']} {item['titulo']}"
            if not descricao:
                flash("Descreva a atividade, decisão ou entrega.", "erro")
            else:
                db.execute("INSERT INTO raci_linha (projeto_id, descricao, item_id) VALUES (?, ?, ?)", (projeto_id, descricao, item_id))
                flash("Linha adicionada à matriz.", "ok")
        elif acao == "excluir":
            db.execute("DELETE FROM raci_linha WHERE id = ? AND projeto_id = ?", (inteiro(f.get("excluir_linha"), 1, 10**9), projeto_id))
            flash("Linha removida.", "ok")
        else:
            ids_membros = {m["id"] for m in membros_}
            for linha in db.execute("SELECT id FROM raci_linha WHERE projeto_id = ?", (projeto_id,)).fetchall():
                for mid in ids_membros:
                    chave = f"p_{linha['id']}_{mid}"
                    if chave not in f:
                        continue
                    valor = f.get(chave)
                    db.execute("DELETE FROM raci_papel WHERE linha_id = ? AND membro_id = ?", (linha["id"], mid))
                    if valor in dict(pmbok.PAPEIS_RACI):
                        db.execute("INSERT INTO raci_papel (linha_id, membro_id, papel) VALUES (?, ?, ?)", (linha["id"], mid, valor))
            flash("Matriz RACI salva.", "ok")
        tocar_projeto(projeto_id)
        db.commit()
        return redirect(url_for("equipe.matriz", projeto_id=projeto_id))
    itens = db.execute("SELECT id, codigo, titulo FROM item WHERE projeto_id = ? AND status != 'cancelado' ORDER BY codigo", (projeto_id,)).fetchall()
    return render_template("raci.html", projeto=p, linhas=raci(projeto_id), membros=membros_, itens=itens, secao="equipe", sub="raci")


@bp.route("/saude", methods=["GET", "POST"])
def saude(projeto_id):
    p = obter_projeto(projeto_id)
    db = get_db()
    if request.method == "POST":
        f = request.form
        if f.get("acao") == "excluir":
            db.execute("DELETE FROM avaliacao_equipe WHERE id = ? AND projeto_id = ?", (inteiro(f.get("avaliacao_id"), 1, 10**9), projeto_id))
            flash("Avaliação removida.", "ok")
        else:
            notas = {k: inteiro(f.get(k)) for k, *_ in pmbok.FATORES_ALTO_DESEMPENHO}
            if not any(notas.values()):
                flash("Dê nota a pelo menos um fator.", "erro")
                return redirect(url_for("equipe.saude", projeto_id=projeto_id))
            quando = f.get("data") or date.today().isoformat()
            try:
                quando = min(date.fromisoformat(quando), date.today()).isoformat()
            except ValueError:
                quando = date.today().isoformat()
            db.execute("INSERT INTO avaliacao_equipe (projeto_id, data, notas_json, participantes, observacoes) VALUES (?, ?, ?, ?, ?)",
                       (projeto_id, quando, json.dumps(notas), inteiro(f.get("participantes"), 1, 1000), f.get("observacoes", "").strip()))
            flash("Avaliação registrada.", "ok")
        tocar_projeto(projeto_id)
        db.commit()
        return redirect(url_for("equipe.saude", projeto_id=projeto_id))
    avs = avaliacoes(projeto_id)
    grafico = None
    if avs:
        ultimas = avs[-2:]
        grafico = graficos.colunas(
            [{"nome": f"Avaliação de {a['data'][8:10]}/{a['data'][5:7]}", "valores": [a["notas"].get(k) for k, *_ in pmbok.FATORES_ALTO_DESEMPENHO]}
             for a in ultimas],
            [nome for _, nome, _ in pmbok.FATORES_ALTO_DESEMPENHO],
            "Notas de 1 a 5 por fator de alto desempenho", largura=880, altura=270, ticks=[0, 1, 2, 3, 4, 5])
    return render_template("saude_equipe.html", projeto=p, avaliacoes=list(reversed(avs)), grafico=grafico, secao="equipe", sub="saude")
