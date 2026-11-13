"""Domínio de desempenho Medição (PMBOK 7, seção 2.7) e cronograma/orçamento (2.4.2.3 e 2.4.2.4).

Painel com semáforo, valor agregado, burnup, velocidade, fluxo e previsões;
indicadores (KPIs) com metas e limites; relatórios de status; cronograma
com iterações e datas/custos planejados por item.
"""
import json
from datetime import date, timedelta

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

import graficos
import incerteza
import pmbok
import trabalho
from db import get_db
from entrega import folhas, linha_base_atual, listar_itens, resumo_entrega
from partes import listar_partes
from util import decimal, inteiro, moeda, obter_projeto, tocar_projeto

bp = Blueprint("medicao", __name__, url_prefix="/p/<int:projeto_id>/medicao")

DIAS_SEM_MEDICAO = 30


def _data(valor):
    try:
        return date.fromisoformat(str(valor)[:10]) if valor else None
    except ValueError:
        return None


def _semanas(inicio, fim):
    """Datas semanais de `inicio` até `fim` (inclui o fim)."""
    pontos, d = [], inicio
    while d < fim:
        pontos.append(d)
        d += timedelta(days=7)
    pontos.append(fim)
    return pontos


def _tamanho(itens):
    usar = bool(itens) and all(i["estimativa"] for i in itens)
    return (lambda lst: sum(i["estimativa"] for i in lst)) if usar else len, "estimativa" if usar else "itens"


# --------------------------------------------------------------------------
# Valor agregado (2.7.2.3 e 2.7.2.7)
# --------------------------------------------------------------------------
def _fracao_planejada(inicio, fim, d):
    if inicio is None or fim is None:
        return None
    if d < inicio:
        return 0.0
    if d >= fim:
        return 1.0
    return ((d - inicio).days + 1) / ((fim - inicio).days + 1)


def _plano(projeto, itens):
    """Custo e datas planejados por item, preferindo os valores da linha de base (linha de base de medição)."""
    lb = linha_base_atual(projeto["id"])
    base = (lb or {}).get("dados", {}).get("itens", {})
    plano = []
    for i in folhas(itens):
        b = base.get(str(i["id"]), {})
        custo = b.get("custo_planejado") or i["custo_planejado"]
        if not custo:
            continue
        plano.append({
            "item": i, "custo": custo,
            "inicio": _data(b.get("inicio_planejado") or i["inicio_planejado"]),
            "fim": _data(b.get("fim_planejado") or i["fim_planejado"]),
        })
    return plano


def valor_agregado(projeto, itens, hoje=None):
    """VP, VA e CR com a regra 0/100 (o item agrega valor só quando concluído) e os índices do guia."""
    hoje = hoje or date.today()
    plano = _plano(projeto, itens)
    if not plano:
        return None
    onp = sum(p["custo"] for p in plano)  # orçamento no término (BAC)
    sem_datas = [p for p in plano if p["inicio"] is None or p["fim"] is None]
    vp = sum(p["custo"] * _fracao_planejada(p["inicio"], p["fim"], hoje) for p in plano if p not in sem_datas)
    va = sum(p["custo"] for p in plano if p["item"]["feito"])
    cr = sum(i["custo_real"] or 0 for i in folhas(itens))
    r = {"onp": onp, "vp": vp, "va": va, "cr": cr, "sem_datas": len(sem_datas), "n": len(plano),
         "vprazo": va - vp, "vcusto": va - cr,
         "idp": va / vp if vp else None, "idc": va / cr if cr else None}
    r["ent"] = onp / r["idc"] if r["idc"] else None                 # estimativa no término (EAC)
    r["ept"] = r["ent"] - cr if r["ent"] is not None else None       # estimativa para terminar (ETC)
    r["vnt"] = onp - r["ent"] if r["ent"] is not None else None      # variação no término (VAC)
    r["idpt"] = (onp - va) / (onp - cr) if onp - cr > 0 else None    # índice de desempenho para término (TCPI)
    return r


def curva_valor_agregado(projeto, itens):
    plano = [p for p in _plano(projeto, itens) if p["inicio"] and p["fim"]]
    if not plano:
        return None
    hoje = date.today()
    inicio = min(p["inicio"] for p in plano)
    fim = max(max(p["fim"] for p in plano), min(hoje, max(p["fim"] for p in plano) + timedelta(days=60)))
    datas = _semanas(inicio, fim)
    vp, va, cr = [], [], []
    for d in datas:
        vp.append(sum(p["custo"] * _fracao_planejada(p["inicio"], p["fim"], d) for p in plano))
        if d <= hoje:
            va.append(sum(p["custo"] for p in plano if p["item"]["feito"] and (_data(p["item"]["concluido_em"]) or hoje) <= d))
            cr.append(sum((i["custo_real"] or 0) for i in folhas(itens) if i["custo_real"]
                          and (_data(i["concluido_em"]) if i["feito"] else hoje) <= d))
        else:
            va.append(None)
            cr.append(None)
    marca = next((k - 1 + (hoje - datas[k - 1]).days / max(1, (datas[k] - datas[k - 1]).days)
                  for k in range(1, len(datas)) if datas[k] >= hoje), None) if inicio <= hoje <= fim else None
    return graficos.linhas(
        [{"nome": "Valor planejado (VP)", "valores": vp}, {"nome": "Valor agregado (VA)", "valores": va},
         {"nome": "Custo real (CR)", "valores": cr}],
        [d.strftime("%d/%m") for d in datas], "Curva de valor agregado em reais", marca=marca)


# --------------------------------------------------------------------------
# Burnup, velocidade, fluxo e previsões
# --------------------------------------------------------------------------
def burnup(projeto, itens):
    trabalho_ = folhas(itens)
    if not trabalho_:
        return None
    tam, base = _tamanho(trabalho_)
    hoje = date.today()
    inicio = min(_data(i["criado_em"]) for i in trabalho_)
    if projeto["data_inicio"] and _data(projeto["data_inicio"]) and _data(projeto["data_inicio"]) < inicio:
        inicio = _data(projeto["data_inicio"])
    datas = _semanas(inicio, hoje) if inicio < hoje else [hoje]
    escopo = [tam([i for i in trabalho_ if _data(i["criado_em"]) <= d]) for d in datas]
    feito = [tam([i for i in trabalho_ if i["feito"] and (_data(i["concluido_em"]) or hoje) <= d]) for d in datas]
    unidade = projeto["unidade_estimativa"] if base == "estimativa" else "itens"
    g = graficos.linhas([{"nome": "Escopo total", "valores": escopo}, {"nome": "Concluído", "valores": feito}],
                        [d.strftime("%d/%m") for d in datas], f"Burnup em {unidade}", largura=440, altura=230)
    g["unidade"] = unidade
    return g


def listar_iteracoes(projeto_id):
    return get_db().execute("SELECT * FROM iteracao WHERE projeto_id = ? ORDER BY inicio, id", (projeto_id,)).fetchall()


def velocidade(projeto, itens):
    iteracoes = listar_iteracoes(projeto["id"])
    if not iteracoes:
        return None
    trabalho_ = folhas(itens)
    tam, base = _tamanho(trabalho_)
    hoje = date.today()
    linhas_ = []
    for it in iteracoes:
        dela = [i for i in trabalho_ if i["iteracao_id"] == it["id"]]
        fim = _data(it["fim"])
        feitos = [i for i in dela if i["feito"] and (_data(i["concluido_em"]) or hoje) <= fim]
        linhas_.append({"it": it, "planejado": tam(dela), "concluido": tam(feitos), "encerrada": fim < hoje,
                        "atual": _data(it["inicio"]) <= hoje <= fim, "capacidade": it["capacidade"],
                        "dias": (fim - _data(it["inicio"])).days + 1})
    encerradas = [x for x in linhas_ if x["encerrada"]][-3:]
    media = sum(x["concluido"] for x in encerradas) / len(encerradas) if encerradas else None
    duracao = sum(x["dias"] for x in encerradas) / len(encerradas) if encerradas else None
    mostrar = linhas_[-8:]
    grafico = graficos.colunas(
        [{"nome": "Planejado", "valores": [x["planejado"] for x in mostrar]},
         {"nome": "Concluído", "valores": [x["concluido"] if (x["encerrada"] or x["atual"]) else None for x in mostrar]}],
        [x["it"]["nome"] for x in mostrar], "Velocidade por iteração")
    return {"linhas": linhas_, "media": media, "duracao": duracao, "grafico": grafico,
            "unidade": projeto["unidade_estimativa"] if base == "estimativa" else "itens"}


def fluxo(itens):
    hoje = date.today()
    desde = hoje - timedelta(days=90)
    feitos = [i for i in folhas(itens) if i["feito"] and _data(i["concluido_em"]) and _data(i["concluido_em"]) >= desde]
    lead = [(_data(i["concluido_em"]) - _data(i["criado_em"])).days for i in feitos]
    ciclo = [(_data(i["concluido_em"]) - _data(i["iniciado_em"])).days for i in feitos if i["iniciado_em"]]
    ult30 = [i for i in feitos if _data(i["concluido_em"]) >= hoje - timedelta(days=30)]
    return {
        "wip": sum(1 for i in folhas(itens) if i["status"] == "em_andamento"),
        "fila": sum(1 for i in folhas(itens) if i["status"] == "a_fazer"),
        "lead": sum(lead) / len(lead) if lead else None,
        "ciclo": sum(ciclo) / len(ciclo) if ciclo else None,
        "vazao30": len(ult30),
        "n": len(feitos),
    }


def previsao(projeto, itens, vel=None):
    """Data provável de término do escopo restante, pela velocidade ou pela vazão (análise de vazão, 2.7.2.7)."""
    trabalho_ = folhas(itens)
    tam, base = _tamanho(trabalho_)
    restante = tam([i for i in trabalho_ if not i["feito"]])
    hoje = date.today()
    res = {"restante": restante, "unidade": projeto["unidade_estimativa"] if base == "estimativa" else "itens",
           "data": None, "metodo": None}
    if restante == 0:
        return res
    vel = vel if vel is not None else velocidade(projeto, itens)
    if vel and vel["media"]:
        n = -(-restante // vel["media"])  # arredonda para cima
        res.update(data=hoje + timedelta(days=int(n * vel["duracao"])), metodo=f"velocidade média de {graficos.numero(vel['media'])} "
                   f"{res['unidade']} por iteração ({int(n)} iteração(ões) restantes)")
        return res
    desde = hoje - timedelta(days=30)
    feitos = [i for i in trabalho_ if i["feito"] and _data(i["concluido_em"]) and _data(i["concluido_em"]) >= desde]
    ritmo = tam(feitos) / 30 if feitos else 0
    if ritmo:
        res.update(data=hoje + timedelta(days=int(restante / ritmo + 0.999)),
                   metodo=f"vazão dos últimos 30 dias ({graficos.numero(tam(feitos))} {res['unidade']})")
    return res


# --------------------------------------------------------------------------
# Semáforo (painel com status por dimensão, 2.7.3.1)
# --------------------------------------------------------------------------
def _por_indice(valor, limite):
    if valor is None:
        return "sem_dados"
    if valor >= 1 - limite / 100:
        return "ok"
    return "atencao" if valor >= 1 - 2 * limite / 100 else "critico"


def semaforo(projeto, itens=None):
    pid = projeto["id"]
    itens = listar_itens(pid) if itens is None else itens
    lim = projeto["limite_variacao"]
    va = valor_agregado(projeto, itens)
    prev = previsao(projeto, itens)
    out = []

    # Prazo
    fim_plan = _data(projeto["data_fim_planejada"])
    if va and va["idp"] is not None:
        out.append(("Prazo", _por_indice(va["idp"], lim), f"IDP {graficos.numero(va['idp'], 2)} (valor agregado)."))
    elif fim_plan and prev["data"]:
        atraso = (prev["data"] - fim_plan).days
        total = max(1, (fim_plan - (_data(projeto["data_inicio"]) or _data(projeto["criado_em"]))).days)
        st = "ok" if atraso <= 0 else ("atencao" if atraso <= total * lim / 100 else "critico")
        out.append(("Prazo", st, f"Previsão de término {prev['data'].strftime('%d/%m/%Y')}, planejado {fim_plan.strftime('%d/%m/%Y')}."))
    elif fim_plan and prev["restante"] == 0:
        out.append(("Prazo", "ok", "Todo o escopo está concluído."))
    else:
        out.append(("Prazo", "sem_dados", "Defina a data de término e registre progresso (ou custos e datas planejados)."))

    # Custo
    if va and va["idc"] is not None:
        out.append(("Custo", _por_indice(va["idc"], lim), f"IDC {graficos.numero(va['idc'], 2)}; estimativa no término {moeda(va['ent'])}."))
    else:
        out.append(("Custo", "sem_dados", "Informe custos planejados e reais dos itens."))

    # Escopo
    ent = resumo_entrega(projeto, itens)
    if not ent["n_itens"]:
        out.append(("Escopo", "sem_dados", "Nenhum item de escopo registrado."))
    elif ent["sem_mudanca"] and projeto["abordagem"] != "adaptativa":
        out.append(("Escopo", "critico", f"{len(ent['sem_mudanca'])} item(ns) fora da linha de base sem mudança aprovada."))
    else:
        st = "atencao" if (projeto["abordagem"] == "adaptativa" and ent["fluxo_criados"] > ent["fluxo_concluidos"]) else "ok"
        out.append(("Escopo", st, f"{ent['pct_aceito']}% aceito, {ent['pct_feito']}% concluído."))

    # Riscos
    riscos = incerteza.listar_riscos(projeto, so_ativos=True)
    altos = [r for r in riscos if r["tipo"] == "ameaca" and r["nivel"] == "alto"]
    sem_resp = [r for r in altos if not r["estrategia"] or (r["estrategia"] == "aceitar" and not r["plano_contingencia"])]
    if not riscos:
        out.append(("Riscos", "sem_dados", "Nenhum risco ativo registrado."))
    else:
        st = "critico" if sem_resp else ("atencao" if altos or projeto["risco_global"] == "alto" else "ok")
        out.append(("Riscos", st, f"{len(altos)} ameaça(s) acima do limite, {len(sem_resp)} sem resposta ativa."))

    # Partes interessadas
    sats = [s["ultima_satisfacao"] for s in listar_partes(pid) if s["ultima_satisfacao"]]
    if sats:
        media = sum(sats) / len(sats)
        st = "ok" if media >= 3.5 else ("atencao" if media >= 2.5 else "critico")
        out.append(("Partes interessadas", st, f"Satisfação média {graficos.numero(media)}/5 ({len(sats)} avaliadas)."))
    else:
        out.append(("Partes interessadas", "sem_dados", "Nenhuma satisfação registrada nas interações."))

    # Questões
    tr = trabalho.resumo_trabalho(projeto)
    st = "critico" if tr["questoes_atrasadas"] else ("atencao" if tr["questoes_abertas"] else "ok")
    out.append(("Questões", st, f"{tr['questoes_abertas']} aberta(s), {tr['questoes_atrasadas']} atrasada(s)."))
    return [{"dimensao": d, "status": s, "texto": t, "rotulo": pmbok.STATUS_SEMAFORO[s][0], "icone": pmbok.STATUS_SEMAFORO[s][1]}
            for d, s, t in out]


# --------------------------------------------------------------------------
# Indicadores (KPIs, 2.7.1)
# --------------------------------------------------------------------------
def avaliar_metrica(m, medicoes):
    d = dict(m)
    valores = [x["valor"] for x in medicoes]
    d["medicoes"] = medicoes
    d["valores"] = valores
    d["ultima"] = medicoes[-1] if medicoes else None
    v = valores[-1] if valores else None
    melhor = (lambda a, b: a >= b) if m["direcao"] == "maior" else (lambda a, b: a <= b)
    if v is None:
        d["status"] = "sem_dados"
    elif m["limite"] is not None and not melhor(v, m["limite"]) and v != m["limite"]:
        d["status"] = "critico"
    elif m["meta"] is None or melhor(v, m["meta"]):
        d["status"] = "ok"
    else:
        d["status"] = "atencao"
    d["tendencia"] = None
    if len(valores) >= 2 and valores[-1] != valores[-2]:
        d["tendencia"] = "melhora" if melhor(valores[-1], valores[-2]) else "piora"
    d["piora_seguida"] = len(valores) >= 3 and all(not melhor(valores[k], valores[k - 1]) and valores[k] != valores[k - 1]
                                                  for k in (len(valores) - 1, len(valores) - 2))
    d["desatualizada"] = bool(d["ultima"]) and d["ultima"]["data"] < (date.today() - timedelta(days=DIAS_SEM_MEDICAO)).isoformat()
    return d


def listar_metricas(projeto_id):
    db = get_db()
    metricas = db.execute("SELECT * FROM metrica WHERE projeto_id = ? ORDER BY tipo, nome", (projeto_id,)).fetchall()
    out = []
    for m in metricas:
        meds = db.execute("SELECT * FROM medicao WHERE metrica_id = ? ORDER BY data, id", (m["id"],)).fetchall()
        out.append(avaliar_metrica(m, meds))
    return out


def gerar_alertas_medicao(projeto, sem=None):
    pid = projeto["id"]
    alertas = []
    link = url_for("medicao.indicadores", projeto_id=pid)
    for m in listar_metricas(pid):
        if m["status"] == "critico":
            alertas.append(("alto", f"O indicador “{m['nome']}” ({graficos.numero(m['ultima']['valor'], 2)} {m['unidade']}) passou do limite.", link))
        elif m["tipo"] == "antecedente" and m["piora_seguida"]:
            alertas.append(("medio", f"O indicador antecedente “{m['nome']}” piorou em duas medições seguidas: aja antes de chegar ao limite.", link))
        if m["desatualizada"]:
            alertas.append(("info", f"O indicador “{m['nome']}” não é medido há mais de {DIAS_SEM_MEDICAO} dias.", link))
    sem = sem if sem is not None else semaforo(projeto)
    criticos = [s["dimensao"] for s in sem if s["status"] == "critico"]
    if criticos and not (projeto["plano_excecao"] or "").strip():
        alertas.append(("alto", f"{', '.join(criticos)} em estado crítico e o projeto não tem plano de exceção definido.",
                        url_for("medicao.painel", projeto_id=pid) + "#excecao"))
    return [{"nivel": n, "texto": t, "link": lk} for n, t, lk in alertas]


def indicadores_dominio(projeto):
    itens = listar_itens(projeto["id"])
    sem = semaforo(projeto, itens)
    ind = ["Semáforo: " + "; ".join(f"{s['dimensao']} {s['rotulo'].lower()}" for s in sem) + "."]
    va = valor_agregado(projeto, itens)
    if va:
        ind.append(f"Valor agregado: IDP {graficos.numero(va['idp'], 2) if va['idp'] else '—'}, IDC {graficos.numero(va['idc'], 2) if va['idc'] else '—'}, "
                   f"estimativa no término {moeda(va['ent'])} para um orçamento de {moeda(va['onp'])}.")
    prev = previsao(projeto, itens)
    if prev["data"]:
        ind.append(f"Previsão de término do escopo restante: {prev['data'].strftime('%d/%m/%Y')} ({prev['metodo']}).")
    metricas = listar_metricas(projeto["id"])
    if metricas:
        ind.append(f"{len(metricas)} indicadores: {sum(1 for m in metricas if m['tipo'] == 'antecedente')} antecedentes; "
                   f"{sum(1 for m in metricas if m['status'] == 'critico')} além do limite.")
    n_rel = get_db().execute("SELECT COUNT(*) FROM relatorio_status WHERE projeto_id = ?", (projeto["id"],)).fetchone()[0]
    ind.append(f"{n_rel} relatório(s) de status emitidos.")
    return ind


# --------------------------------------------------------------------------
# Rotas: painel
# --------------------------------------------------------------------------
@bp.route("", methods=["GET", "POST"])
def painel(projeto_id):
    p = obter_projeto(projeto_id)
    if request.method == "POST":
        db = get_db()
        db.execute("UPDATE projeto SET limite_variacao = ?, plano_excecao = ?, atualizado_em = datetime('now','localtime') WHERE id = ?",
                   (inteiro(request.form.get("limite_variacao"), 1, 50) or p["limite_variacao"],
                    request.form.get("plano_excecao", "").strip(), projeto_id))
        db.commit()
        flash("Limites e plano de exceção salvos.", "ok")
        return redirect(url_for("medicao.painel", projeto_id=projeto_id) + "#excecao")
    itens = listar_itens(projeto_id)
    vel = velocidade(p, itens)
    sem = semaforo(p, itens)
    return render_template(
        "medicao_painel.html", projeto=p, semaforo=sem, va=valor_agregado(p, itens), curva=curva_valor_agregado(p, itens),
        burnup=burnup(p, itens), vel=vel, fluxo=fluxo(itens), prev=previsao(p, itens, vel),
        alertas=gerar_alertas_medicao(p, sem), secao="medicao", sub="painel",
    )


# --------------------------------------------------------------------------
# Rotas: indicadores
# --------------------------------------------------------------------------
@bp.route("/indicadores", methods=["GET", "POST"])
def indicadores(projeto_id):
    p = obter_projeto(projeto_id)
    if request.method == "POST":
        f = request.form
        nome = f.get("nome", "").strip()
        if not nome:
            flash("Dê um nome ao indicador.", "erro")
            return redirect(url_for("medicao.indicadores", projeto_id=projeto_id))
        db = get_db()
        db.execute(
            """INSERT INTO metrica (projeto_id, nome, tipo, categoria, unidade, direcao, meta, limite, relevancia)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (projeto_id, nome, f.get("tipo") if f.get("tipo") in dict(pmbok.TIPOS_INDICADOR) else "resultado",
             f.get("categoria") if f.get("categoria") in dict(pmbok.CATEGORIAS_METRICA) else "",
             f.get("unidade", "").strip(), f.get("direcao") if f.get("direcao") in dict(pmbok.DIRECOES_METRICA) else "maior",
             decimal(f.get("meta"), minimo=-1e18), decimal(f.get("limite"), minimo=-1e18), f.get("relevancia", "").strip()),
        )
        tocar_projeto(projeto_id)
        db.commit()
        flash("Indicador criado. Registre a primeira medição.", "ok")
        return redirect(url_for("medicao.indicadores", projeto_id=projeto_id))
    metricas = listar_metricas(projeto_id)
    for m in metricas:
        m["grafico"] = graficos.linhas([{"nome": m["nome"], "valores": m["valores"]}],
                                       [graficos_data(x["data"]) for x in m["medicoes"]],
                                       f"Histórico de {m['nome']}", largura=420, altura=150) if len(m["valores"]) > 1 else None
    return render_template("indicadores.html", projeto=p, metricas=metricas, secao="medicao", sub="indicadores")


def graficos_data(iso):
    d = _data(iso)
    return d.strftime("%d/%m") if d else iso


@bp.route("/indicadores/<int:metrica_id>", methods=["POST"])
def indicador(projeto_id, metrica_id):
    obter_projeto(projeto_id)
    db = get_db()
    if db.execute("SELECT 1 FROM metrica WHERE id = ? AND projeto_id = ?", (metrica_id, projeto_id)).fetchone() is None:
        abort(404)
    f = request.form
    if f.get("acao") == "excluir":
        db.execute("DELETE FROM metrica WHERE id = ?", (metrica_id,))
        flash("Indicador removido.", "ok")
    elif f.get("acao") == "excluir_medicao":
        db.execute("DELETE FROM medicao WHERE id = ? AND metrica_id = ?", (inteiro(f.get("medicao_id"), 1, 10**9), metrica_id))
        flash("Medição removida.", "ok")
    else:
        valor = decimal(f.get("valor"), minimo=-1e18)
        if valor is None:
            flash("Informe o valor medido.", "erro")
            return redirect(url_for("medicao.indicadores", projeto_id=projeto_id) + f"#m{metrica_id}")
        quando = _data(f.get("data")) or date.today()
        if quando > date.today():
            flash("A data da medição não pode estar no futuro.", "erro")
            return redirect(url_for("medicao.indicadores", projeto_id=projeto_id) + f"#m{metrica_id}")
        db.execute("INSERT INTO medicao (metrica_id, data, valor, nota) VALUES (?, ?, ?, ?)",
                   (metrica_id, quando.isoformat(), valor, f.get("nota", "").strip()))
        flash("Medição registrada.", "ok")
    tocar_projeto(projeto_id)
    db.commit()
    return redirect(url_for("medicao.indicadores", projeto_id=projeto_id) + f"#m{metrica_id}")


# --------------------------------------------------------------------------
# Rotas: relatórios de status (4.6.7)
# --------------------------------------------------------------------------
def montar_dados_relatorio(projeto):
    import app as aplicacao  # evita import circular; só usado na geração do relatório
    pid = projeto["id"]
    itens = listar_itens(pid)
    vel = velocidade(projeto, itens)
    prev = previsao(projeto, itens, vel)
    va = valor_agregado(projeto, itens)
    ent = resumo_entrega(projeto, itens)
    riscos = [r for r in incerteza.listar_riscos(projeto, so_ativos=True)][:5]
    questoes = [q for q in trabalho.listar_questoes(pid) if q["aberta"]][:5]
    alertas = [a["texto"] for a in aplicacao.alertas_do_projeto(projeto) if a["nivel"] == "alto"][:8]
    return {
        "semaforo": semaforo(projeto, itens),
        "escopo": {"pct_aceito": ent["pct_aceito"], "pct_feito": ent["pct_feito"], "aguardando_aceite": ent["aguardando_aceite"]},
        "valor_agregado": {k: va[k] for k in ("onp", "vp", "va", "cr", "idp", "idc", "ent")} if va else None,
        "previsao": {"data": prev["data"].isoformat() if prev["data"] else None, "metodo": prev["metodo"],
                     "restante": prev["restante"], "unidade": prev["unidade"]},
        "riscos": [{"rotulo": r["rotulo"], "titulo": r["titulo"], "tipo": r["tipo"], "pontuacao": r["pontuacao"],
                    "estrategia": r["estrategia_nome"]} for r in riscos],
        "questoes": [{"rotulo": q["rotulo"], "titulo": q["titulo"], "prazo": q["prazo"], "atrasada": q["atrasada"]} for q in questoes],
        "alertas": alertas,
    }


def sugestoes_relatorio(projeto_id):
    db = get_db()
    ultimo = db.execute("SELECT data FROM relatorio_status WHERE projeto_id = ? ORDER BY data DESC, id DESC LIMIT 1", (projeto_id,)).fetchone()
    desde = ultimo["data"] if ultimo else "0000-00-00"
    itens = folhas(listar_itens(projeto_id))
    feitos = [i for i in itens if i["feito"] and (i["concluido_em"] or "") > desde]
    andamento = [i for i in itens if i["status"] == "em_andamento"]
    proximos = sorted([i for i in itens if i["status"] == "a_fazer"], key=lambda i: (i["ordem"] or 10**9, i["codigo"]))[:3]
    return {
        "realizacoes": "\n".join(f"{i['rotulo']} {i['titulo']} ({'aceito' if i['status'] == 'aceito' else 'concluído'})" for i in feitos),
        "proximos_passos": "\n".join([f"Concluir {i['rotulo']} {i['titulo']}" for i in andamento]
                                     + [f"Iniciar {i['rotulo']} {i['titulo']}" for i in proximos]),
    }


@bp.route("/relatorios", methods=["GET", "POST"])
def relatorios(projeto_id):
    p = obter_projeto(projeto_id)
    db = get_db()
    if request.method == "POST":
        f = request.form
        quando = _data(f.get("data")) or date.today()
        quando = min(quando, date.today())
        cur = db.execute(
            "INSERT INTO relatorio_status (projeto_id, data, resumo, realizacoes, proximos_passos, dados_json) VALUES (?, ?, ?, ?, ?, ?)",
            (projeto_id, quando.isoformat(), f.get("resumo", "").strip(), f.get("realizacoes", "").strip(),
             f.get("proximos_passos", "").strip(), json.dumps(montar_dados_relatorio(p))),
        )
        tocar_projeto(projeto_id)
        db.commit()
        flash("Relatório de status emitido. Os números ficam congelados com a situação de hoje.", "ok")
        return redirect(url_for("medicao.relatorio", projeto_id=projeto_id, relatorio_id=cur.lastrowid))
    lista = db.execute("SELECT * FROM relatorio_status WHERE projeto_id = ? ORDER BY data DESC, id DESC", (projeto_id,)).fetchall()
    resumos = []
    for r in lista:
        dados = json.loads(r["dados_json"] or "{}")
        resumos.append({**dict(r), "semaforo": dados.get("semaforo", [])})
    return render_template("relatorios.html", projeto=p, relatorios=resumos, sugestao=sugestoes_relatorio(projeto_id),
                           secao="medicao", sub="relatorios")


@bp.route("/relatorios/<int:relatorio_id>", methods=["GET", "POST"])
def relatorio(projeto_id, relatorio_id):
    p = obter_projeto(projeto_id)
    db = get_db()
    r = db.execute("SELECT * FROM relatorio_status WHERE id = ? AND projeto_id = ?", (relatorio_id, projeto_id)).fetchone()
    if r is None:
        abort(404)
    if request.method == "POST" and request.form.get("acao") == "excluir":
        db.execute("DELETE FROM relatorio_status WHERE id = ?", (relatorio_id,))
        db.commit()
        flash("Relatório excluído.", "ok")
        return redirect(url_for("medicao.relatorios", projeto_id=projeto_id))
    return render_template("relatorio.html", projeto=p, r=r, dados=json.loads(r["dados_json"] or "{}"),
                           secao="medicao", sub="relatorios")


# --------------------------------------------------------------------------
# Rotas: cronograma e orçamento (domínio Planejamento)
# --------------------------------------------------------------------------
@bp.route("/cronograma", methods=["GET", "POST"])
def cronograma(projeto_id):
    p = obter_projeto(projeto_id)
    db = get_db()
    if request.method == "POST":
        f = request.form
        acao = f.get("acao")
        if acao == "datas":
            ini, fim = _data(f.get("data_inicio")), _data(f.get("data_fim_planejada"))
            if ini and fim and fim < ini:
                flash("A data de término não pode ser anterior à de início.", "erro")
            else:
                db.execute("UPDATE projeto SET data_inicio = ?, data_fim_planejada = ? WHERE id = ?",
                           (ini.isoformat() if ini else None, fim.isoformat() if fim else None, projeto_id))
                flash("Datas do projeto salvas.", "ok")
        elif acao == "iteracao":
            nome, ini, fim = f.get("nome", "").strip(), _data(f.get("inicio")), _data(f.get("fim"))
            sobreposta = ini and fim and db.execute(
                "SELECT nome FROM iteracao WHERE projeto_id = ? AND inicio <= ? AND fim >= ?",
                (projeto_id, fim.isoformat(), ini.isoformat())).fetchone()
            if not nome or not ini or not fim or fim < ini:
                flash("Informe nome, início e fim da iteração (o fim não pode ser antes do início).", "erro")
            elif sobreposta:
                flash(f"As datas coincidem com a iteração “{sobreposta['nome']}”. Iterações são períodos fixos e não se sobrepõem.", "erro")
            else:
                db.execute("INSERT INTO iteracao (projeto_id, nome, inicio, fim, meta, capacidade) VALUES (?, ?, ?, ?, ?, ?)",
                           (projeto_id, nome, ini.isoformat(), fim.isoformat(), f.get("meta", "").strip(), decimal(f.get("capacidade"))))
                flash(f"Iteração “{nome}” criada.", "ok")
        elif acao == "excluir_iteracao":
            db.execute("DELETE FROM iteracao WHERE id = ? AND projeto_id = ?", (inteiro(f.get("iteracao_id"), 1, 10**9), projeto_id))
            flash("Iteração removida; os itens dela voltaram para o backlog.", "ok")
        elif acao == "itens":
            iteracoes = {it["id"] for it in listar_iteracoes(projeto_id)}
            erros = []
            for i in folhas(listar_itens(projeto_id)):
                k = i["id"]
                if f"inicio_{k}" not in f:
                    continue
                ini, fim = _data(f.get(f"inicio_{k}")), _data(f.get(f"fim_{k}"))
                if ini and fim and fim < ini:
                    erros.append(i["rotulo"])
                    continue
                it = inteiro(f.get(f"iteracao_{k}"), 1, 10**9)
                db.execute(
                    """UPDATE item SET iteracao_id = ?, inicio_planejado = ?, fim_planejado = ?, custo_planejado = ?, custo_real = ?,
                       atualizado_em = datetime('now','localtime') WHERE id = ? AND projeto_id = ?""",
                    (it if it in iteracoes else None, ini.isoformat() if ini else None, fim.isoformat() if fim else None,
                     decimal(f.get(f"custo_planejado_{k}")), decimal(f.get(f"custo_real_{k}")), k, projeto_id))
            if erros:
                flash("Datas ignoradas (término antes do início): " + ", ".join(erros) + ".", "erro")
            else:
                flash("Cronograma e custos salvos.", "ok")
        tocar_projeto(projeto_id)
        db.commit()
        return redirect(url_for("medicao.cronograma", projeto_id=projeto_id))
    itens = folhas(listar_itens(projeto_id))
    iteracoes = listar_iteracoes(projeto_id)
    vel = velocidade(p, listar_itens(projeto_id))
    hoje = date.today().isoformat()
    total_plan = sum(i["custo_planejado"] or 0 for i in itens)
    total_real = sum(i["custo_real"] or 0 for i in itens)
    return render_template("cronograma.html", projeto=p, itens=itens, iteracoes=iteracoes,
                           vel={x["it"]["id"]: x for x in (vel["linhas"] if vel else [])}, hoje_iso=hoje,
                           total_plan=total_plan, total_real=total_real, secao="cronograma")
