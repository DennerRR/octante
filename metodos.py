"""Modelos e métodos da seção 4 do PMBOK 7 que faltavam (v14): MoSCoW, dependências e Gantt, burndown,
Cynefin e Stacey (complexidade) e pré-mortem."""
from datetime import date, datetime, timedelta

from flask import Blueprint, flash, redirect, render_template, request, url_for

import graficos
from db import get_db
from entrega import folhas, listar_itens
from medicao import _tamanho, listar_iteracoes
from util import inteiro, obter_projeto, tocar_projeto

bp = Blueprint("metodos", __name__, url_prefix="/p/<int:projeto_id>")

MOSCOW = [("must", "Deve ter"), ("should", "Deveria ter"), ("could", "Poderia ter"), ("wont", "Não terá agora")]

CYNEFIN = [
    ("claro", "Claro", "Causa e efeito óbvios; existem boas práticas. Planejar e seguir o processo (preditivo funciona)."),
    ("complicado", "Complicado", "Causa e efeito existem mas exigem análise de especialistas. Analisar e então agir."),
    ("complexo", "Complexo", "Causa e efeito só aparecem depois. Experimentar em ciclos curtos (abordagem adaptativa)."),
    ("caotico", "Caótico", "Não há relação clara de causa e efeito. Agir primeiro para estabilizar, depois avaliar."),
]


def _d(v):
    try:
        return datetime.fromisoformat(str(v)[:10]).date() if v else None
    except ValueError:
        return None


# ------------------------------------------------------------------ dependências (usadas no formulário do item)
def dependencias(item_id):
    if not isinstance(item_id, int):
        return set()
    return {r[0] for r in get_db().execute("SELECT depende_de FROM item_dependencia WHERE item_id = ?", (item_id,))}


def salvar_dependencias(db, projeto_id, item_id, ids):
    validos = {r[0] for r in db.execute("SELECT id FROM item WHERE projeto_id = ? AND id != ?", (projeto_id, item_id))}
    escolhidos = {i for i in ids if i in validos}
    # evita ciclos: não pode depender de quem (direta ou indiretamente) depende dele
    dependentes, fila = set(), [item_id]
    while fila:
        atual = fila.pop()
        for (d,) in db.execute("SELECT item_id FROM item_dependencia WHERE depende_de = ?", (atual,)):
            if d not in dependentes:
                dependentes.add(d)
                fila.append(d)
    ciclo = escolhidos & dependentes
    db.execute("DELETE FROM item_dependencia WHERE item_id = ?", (item_id,))
    for d in escolhidos - ciclo:
        db.execute("INSERT INTO item_dependencia (item_id, depende_de) VALUES (?, ?)", (item_id, d))
    return ciclo


@bp.app_context_processor
def contexto_metodos():
    def outros_itens(projeto_id, item_id=None):
        item_id = item_id if isinstance(item_id, int) else None
        return get_db().execute("SELECT id, codigo, titulo FROM item WHERE projeto_id = ? AND id IS NOT ? ORDER BY codigo",
                                (projeto_id, item_id)).fetchall()
    return {"MOSCOW": MOSCOW, "CYNEFIN": CYNEFIN, "sugestao_stacey": sugestao_stacey,
            "dependencias_do_item": dependencias, "outros_itens": outros_itens}


# ------------------------------------------------------------------ Gantt
@bp.route("/gantt")
def gantt(projeto_id):
    p = obter_projeto(projeto_id)
    db = get_db()
    itens = [i for i in folhas(listar_itens(projeto_id)) if i["status"] != "cancelado"]
    deps = {}
    for a, b in db.execute("SELECT d.item_id, d.depende_de FROM item_dependencia d JOIN item i ON i.id = d.item_id WHERE i.projeto_id = ?", (projeto_id,)):
        deps.setdefault(a, []).append(b)
    por_id = {i["id"]: i for i in itens}
    datados = [i for i in itens if _d(i["inicio_planejado"]) and _d(i["fim_planejado"])]
    sem_data = [i for i in itens if i not in datados]
    conflitos = []
    for i in datados:
        for d in deps.get(i["id"], []):
            pre = por_id.get(d)
            if pre and _d(pre["fim_planejado"]) and _d(i["inicio_planejado"]) <= _d(pre["fim_planejado"]):
                conflitos.append(f"{i['rotulo']} começa em {_d(i['inicio_planejado']):%d/%m} mas depende de {pre['rotulo']}, que termina em {_d(pre['fim_planejado']):%d/%m}.")
    barras, ini, fim = [], None, None
    if datados:
        ini = min(_d(i["inicio_planejado"]) for i in datados)
        fim = max(_d(i["fim_planejado"]) for i in datados)
        total = max((fim - ini).days + 1, 1)
        hoje = date.today()
        for i in sorted(datados, key=lambda x: (_d(x["inicio_planejado"]), x["codigo"])):
            a, b = _d(i["inicio_planejado"]), _d(i["fim_planejado"])
            atrasado = not i["feito"] and b < hoje
            barras.append({"i": i, "esq": 100 * (a - ini).days / total, "larg": max(100 * ((b - a).days + 1) / total, 1.2),
                           "deps": [por_id[d]["rotulo"] for d in deps.get(i["id"], []) if d in por_id], "atrasado": atrasado})
        marca_hoje = 100 * (hoje - ini).days / total if ini <= hoje <= fim else None
    else:
        marca_hoje = None
    return render_template("gantt.html", projeto=p, barras=barras, sem_data=sem_data, conflitos=conflitos, ini=ini, fim=fim,
                           marca_hoje=marca_hoje, secao="cronograma", sub="gantt")


# ------------------------------------------------------------------ burndown da iteração
def burndown(projeto, iteracao, itens):
    trabalho_ = [i for i in folhas(itens) if i["iteracao_id"] == iteracao["id"] and i["status"] != "cancelado"]
    ini, fim = _d(iteracao["inicio"]), _d(iteracao["fim"])
    if not trabalho_ or not ini or not fim:
        return None
    tam, base = _tamanho(trabalho_)
    total = tam(trabalho_)
    dias = [ini + timedelta(days=n) for n in range((fim - ini).days + 1)]
    hoje = date.today()
    ideal = [round(total - total * n / max(len(dias) - 1, 1), 2) for n in range(len(dias))]
    real = []
    for d in dias:
        if d > hoje:
            real.append(None)
            continue
        feitos = [i for i in trabalho_ if i["feito"] and _d(i["concluido_em"]) and _d(i["concluido_em"]) <= d]
        real.append(total - tam(feitos))
    unidade = projeto["unidade_estimativa"] if base == "estimativa" else "itens"
    marca = (hoje - ini).days if ini <= hoje <= fim else None
    g = graficos.linhas([{"nome": "Ideal", "valores": ideal}, {"nome": "Restante", "valores": real}],
                        [d.strftime("%d/%m") for d in dias], f"Burndown da {iteracao['nome']} em {unidade}", marca=marca)
    g["unidade"], g["total"], g["restante"] = unidade, total, next((v for v in reversed(real) if v is not None), total)
    return g


@bp.route("/burndown")
def burndown_pagina(projeto_id):
    p = obter_projeto(projeto_id)
    iteracoes = listar_iteracoes(projeto_id)
    escolhida = inteiro(request.args.get("iteracao"), 1, 10**9)
    hoje = date.today().isoformat()
    it = next((x for x in iteracoes if x["id"] == escolhida), None) or \
        next((x for x in iteracoes if x["inicio"] <= hoje <= x["fim"]), None) or (iteracoes[-1] if iteracoes else None)
    grafico = burndown(p, it, listar_itens(projeto_id)) if it else None
    return render_template("burndown.html", projeto=p, iteracoes=iteracoes, it=it, bd=grafico, secao="medicao", sub="burndown")


# ------------------------------------------------------------------ complexidade (Cynefin e Stacey)
def sugestao_stacey(req, tec):
    """Matriz de Stacey: acordo sobre requisitos (1 = muito acordo) x certeza tecnológica (1 = muita certeza)."""
    if not req or not tec:
        return None
    s = req + tec
    if s <= 4:
        return ("Simples", "preditiva", "Requisitos acordados e tecnologia conhecida: planejar antes funciona bem.")
    if s <= 6:
        return ("Complicado", "hibrida", "Alguma incerteza: planeje o que é estável e itere no restante.")
    if s <= 8:
        return ("Complexo", "adaptativa", "Muita incerteza: entregue em ciclos curtos e ajuste com o feedback.")
    return ("Caótico", "adaptativa", "Incerteza extrema: estabilize primeiro (protótipos, provas de conceito) antes de planejar.")


@bp.route("/complexidade", methods=["POST"])
def complexidade(projeto_id):
    obter_projeto(projeto_id)
    f = request.form
    cyn = f.get("cynefin") if f.get("cynefin") in dict((c, n) for c, n, _ in CYNEFIN) else ""
    db = get_db()
    db.execute("UPDATE projeto SET cynefin = ?, stacey_requisitos = ?, stacey_tecnologia = ? WHERE id = ?",
               (cyn, inteiro(f.get("stacey_requisitos")), inteiro(f.get("stacey_tecnologia")), projeto_id))
    tocar_projeto(projeto_id)
    db.commit()
    flash("Complexidade registrada.", "ok")
    return redirect(url_for("abordagem", projeto_id=projeto_id) + "#complexidade")


# ------------------------------------------------------------------ pré-mortem
@bp.route("/premortem", methods=["GET", "POST"])
def premortem(projeto_id):
    p = obter_projeto(projeto_id)
    if request.method == "POST":
        motivos = [l.strip(" -•\t") for l in request.form.get("motivos", "").splitlines() if l.strip(" -•\t")]
        if not motivos:
            flash("Escreva pelo menos um motivo, um por linha.", "erro")
            return redirect(url_for("metodos.premortem", projeto_id=projeto_id))
        db = get_db()
        codigo = db.execute("SELECT COALESCE(MAX(codigo), 0) FROM risco WHERE projeto_id = ?", (projeto_id,)).fetchone()[0]
        for n, m in enumerate(motivos[:30], start=1):
            db.execute("INSERT INTO risco (projeto_id, codigo, titulo, fonte, status) VALUES (?, ?, ?, 'Pré-mortem', 'aberto')",
                       (projeto_id, codigo + n, m[:300]))
        tocar_projeto(projeto_id)
        db.commit()
        flash(f"{min(len(motivos), 30)} risco(s) criados a partir do pré-mortem. Agora avalie probabilidade e impacto de cada um.", "ok")
        return redirect(url_for("incerteza.riscos", projeto_id=projeto_id))
    vindos = get_db().execute("SELECT COUNT(*) FROM risco WHERE projeto_id = ? AND fonte = 'Pré-mortem'", (projeto_id,)).fetchone()[0]
    return render_template("premortem.html", projeto=p, vindos=vindos, secao="incerteza", sub="premortem")
