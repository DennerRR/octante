"""Domínio de desempenho Partes Interessadas (PMBOK 7, seção 2.1): consultas e regras.

As rotas ficam em app.py; este módulo concentra o que outros módulos também usam.
"""
import math
from datetime import date, datetime, timedelta

from flask import abort, url_for

import pmbok
from db import get_db

DIAS_SEM_INTERACAO = 30


def obter_parte(projeto_id, parte_id):
    s = get_db().execute(
        "SELECT * FROM parte_interessada WHERE id = ? AND projeto_id = ?", (parte_id, projeto_id)
    ).fetchone()
    if s is None:
        abort(404)
    return s


def enriquecer_parte(row, interacoes_por_parte=None):
    s = dict(row)
    s["quadrante"] = pmbok.quadrante_poder_interesse(s["poder"], s["interesse"])
    s["salience"], s["salience_classe"] = pmbok.classificar_salience(
        s["sal_poder"], s["sal_legitimidade"], s["sal_urgencia"]
    )
    s["analisada"] = s["poder"] is not None and s["interesse"] is not None and s["atitude"] != "desconhecida"
    s["priorizada"] = s["prioridade_manual"] is not None
    s["plano_engajamento"] = bool(
        s["engajamento_atual"] and s["engajamento_desejado"] and s["metodo_comunicacao"]
    )
    s["lacuna"] = (
        (s["engajamento_desejado"] - s["engajamento_atual"])
        if s["engajamento_atual"] and s["engajamento_desejado"] else None
    )
    ints = (interacoes_por_parte or {}).get(s["id"], [])
    s["ultima_interacao"] = ints[0]["data"] if ints else None
    s["satisfacoes"] = [i["satisfacao"] for i in reversed(ints) if i["satisfacao"]]
    s["ultima_satisfacao"] = s["satisfacoes"][-1] if s["satisfacoes"] else None
    limite = (date.today() - timedelta(days=DIAS_SEM_INTERACAO)).isoformat()
    s["monitorada"] = bool(s["ultima_interacao"] and s["ultima_interacao"] >= limite)
    palavras = [p for p in s["nome"].replace(".", " ").split() if p.lower() not in ("de", "da", "do", "das", "dos", "e", "dr", "dra")]
    s["iniciais"] = "".join(p[0] for p in (palavras or s["nome"].split())[:2]).upper()
    return s


def listar_partes(projeto_id, incluir_inativas=False):
    db = get_db()
    sql = "SELECT * FROM parte_interessada WHERE projeto_id = ?"
    if not incluir_inativas:
        sql += " AND ativa = 1"
    rows = db.execute(sql, (projeto_id,)).fetchall()
    ints = db.execute(
        """SELECT i.* FROM interacao i JOIN parte_interessada p ON p.id = i.parte_id
           WHERE p.projeto_id = ? ORDER BY i.data DESC, i.id DESC""",
        (projeto_id,),
    ).fetchall()
    por_parte = {}
    for i in ints:
        por_parte.setdefault(i["parte_id"], []).append(i)
    partes = [enriquecer_parte(r, por_parte) for r in rows]
    partes.sort(key=chave_prioridade)
    return partes


def chave_prioridade(s):
    manual = s["prioridade_manual"] if s["prioridade_manual"] is not None else 10**6
    return (
        manual,
        pmbok.ORDEM_QUADRANTE[s["quadrante"]],
        -((s["poder"] or 0) * (s["interesse"] or 0)),
        s["nome"].lower(),
    )


def ordem_sugerida(partes):
    """Ordem baseada apenas na análise (ignora a prioridade manual)."""
    return sorted(
        partes,
        key=lambda s: (
            pmbok.ORDEM_QUADRANTE[s["quadrante"]],
            -((s["poder"] or 0) * (s["interesse"] or 0)),
            -(s["influencia"] or 0),
            s["nome"].lower(),
        ),
    )


def pontos_grade(partes):
    """Coordenadas normalizadas (0..1) para a grade poder × interesse, afastando pontos sobrepostos."""
    grupos = {}
    for s in partes:
        if s["poder"] and s["interesse"]:
            grupos.setdefault((s["interesse"], s["poder"]), []).append(s)
    pontos = []
    for (interesse, poder), membros in grupos.items():
        n = len(membros)
        for k, s in enumerate(membros):
            dx = dy = 0.0
            if n > 1:
                ang = 2 * math.pi * k / n
                dx, dy = 0.05 * math.cos(ang), 0.05 * math.sin(ang)
            pontos.append({"s": s, "x": (interesse - 0.5) / 5 + dx, "y": (poder - 0.5) / 5 + dy})
    return pontos


def resumo_fluxo(partes):
    total = len(partes)
    return [
        {"chave": "identificar", "nome": "Identificar", "feitos": total, "total": total,
         "url": "partes_registro"},
        {"chave": "analisar", "nome": "Compreender e analisar",
         "feitos": sum(s["analisada"] for s in partes), "total": total, "url": "partes_analise"},
        {"chave": "priorizar", "nome": "Priorizar",
         "feitos": sum(s["priorizada"] for s in partes), "total": total, "url": "partes_priorizacao"},
        {"chave": "engajar", "nome": "Engajar",
         "feitos": sum(s["plano_engajamento"] for s in partes), "total": total, "url": "partes_engajamento"},
        {"chave": "monitorar", "nome": "Monitorar",
         "feitos": sum(s["monitorada"] for s in partes), "total": total, "url": "partes_monitoramento"},
    ]


def gerar_alertas_partes(projeto, partes):
    pid = projeto["id"]
    alertas = []
    if not partes:
        alertas.append(("medio", "Nenhuma parte interessada identificada.",
                        url_for("parte_nova", projeto_id=pid)))
    for s in partes:
        link = url_for("parte_detalhe", projeto_id=pid, parte_id=s["id"])
        if s["atitude"] == "opositor" and (s["poder"] or 0) >= 4:
            alertas.append(("alto", f"{s['nome']} tem alto poder e se opõe ao projeto.", link))
        if s["ultima_satisfacao"] is not None and s["ultima_satisfacao"] <= 2:
            alertas.append(("alto", f"Última satisfação registrada de {s['nome']} foi baixa ({s['ultima_satisfacao']}/5).", link))
        if s["quadrante"] == "Gerenciar de perto" and not s["monitorada"]:
            quando = f"desde {datetime.fromisoformat(s['ultima_interacao']).strftime('%d/%m/%Y')}" if s["ultima_interacao"] else "nenhuma registrada"
            alertas.append(("alto", f"{s['nome']} deve ser gerenciada de perto, mas não há interação nos últimos {DIAS_SEM_INTERACAO} dias ({quando}).", link))
        if s["lacuna"] is not None and s["lacuna"] >= 2:
            alertas.append(("medio", f"Lacuna de engajamento de {s['nome']}: {pmbok.NIVEIS_ENGAJAMENTO_DICT[s['engajamento_atual']]} → {pmbok.NIVEIS_ENGAJAMENTO_DICT[s['engajamento_desejado']]}.", link))
        if not s["analisada"]:
            alertas.append(("info", f"{s['nome']} ainda não foi analisada (poder, interesse e atitude).", link))
    return [{"nivel": n, "texto": t, "link": l} for n, t, l in alertas]
