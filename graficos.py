"""Gráficos em SVG gerados no servidor, sem bibliotecas externas.

Especificações seguidas: linhas de 2px, marcador final com anel na cor da superfície,
colunas de até 24px com topo arredondado, grade em hairline, texto sempre em tons de
tinta (nunca na cor da série), legenda para duas ou mais séries e tabela de dados.
A paleta categórica (azul, laranja, água, nessa ordem) foi validada para daltonismo.
"""
import math

from markupsafe import Markup, escape

CORES = ("#5b33a8", "#d9741f", "#1a9bb0")  # v17: paleta da marca, validada (luminosidade, croma, daltonismo, contraste)
SUPERFICIE = "#ffffff"
TINTA2, MUDO, GRADE, EIXO = "#3b3150", "#625877", "#e5dff0", "#cbc2dc"


def numero(v, casas=1):
    """Número em formato brasileiro, compacto acima de 10 mil."""
    if v is None:
        return "—"

    def limpar(texto):
        return texto.rstrip("0").rstrip(".") if "." in texto else texto

    if abs(v) >= 10000:
        return limpar(f"{v / 1000:.1f}").replace(".", ",") + " mil"
    return limpar(f"{v:.{casas}f}").replace(".", ",")


def escala(maximo, n=4):
    """Marcas do eixo em números redondos, de 0 até cobrir o máximo."""
    if maximo <= 0:
        return [0, 1]
    bruto = maximo / n
    mag = 10 ** math.floor(math.log10(bruto))
    passo = next(m * mag for m in (1, 2, 2.5, 5, 10) if bruto <= m * mag + 1e-12)
    qtd = math.ceil(maximo / passo - 1e-9)
    return [round(passo * k, 10) for k in range(qtd + 1)]


def _base(largura, altura, ml, mt, pw, ph, ticks, descricao):
    topo, fundo = ticks[-1], ticks[0]
    partes = [f'<svg class="grafico" viewBox="0 0 {largura} {altura}" role="img" aria-label="{escape(descricao)}">']
    for t in ticks:
        y = mt + ph - ph * (t - fundo) / (topo - fundo)
        cor = EIXO if t == 0 else GRADE
        partes.append(f'<line x1="{ml}" x2="{ml + pw}" y1="{y:.1f}" y2="{y:.1f}" stroke="{cor}" stroke-width="1"/>')
        partes.append(f'<text x="{ml - 6}" y="{y + 3.5:.1f}" text-anchor="end" font-size="11" fill="{MUDO}">{numero(t)}</text>')
    return partes


def _tabela(series, rotulos):
    return {"rotulos": rotulos, "series": [{"nome": s["nome"], "valores": [numero(v, 2) for v in s["valores"]]} for s in series]}


def linhas(series, rotulos, descricao, largura=640, altura=250, marca=None, marca_rotulo="hoje"):
    """Gráfico de linhas. `series`: [{"nome", "valores"}], valores alinhados a `rotulos` (None = sem dado).

    `marca` é o índice (pode ser fracionário) de uma linha vertical de referência.
    """
    ml, mr, mt, mb = 48, 62, 16, 28
    pw, ph = largura - ml - mr, altura - mt - mb
    todos = [v for s in series for v in s["valores"] if v is not None]
    menor = min(todos) if todos else 0
    if menor < 0:  # valores negativos (ex.: valor presente acumulado): eixo simétrico em passos redondos
        maior = max(max(todos), 0)
        base = escala(max(maior, -menor))
        passo = base[1] - base[0]
        ticks = [round(passo * k, 10) for k in range(math.floor(menor / passo + 1e-9), math.ceil(maior / passo - 1e-9) + 1)]
        if len(ticks) < 2:
            ticks.append(ticks[-1] + passo)
    else:
        ticks = escala(max(todos) if todos else 1)
    topo, fundo, n = ticks[-1], ticks[0], len(rotulos)

    def x(i):
        return ml + (pw * i / (n - 1) if n > 1 else pw / 2)

    def y(v):
        return mt + ph - ph * (v - fundo) / (topo - fundo)

    p = _base(largura, altura, ml, mt, pw, ph, ticks, descricao)
    passo = max(1, math.ceil(n / 7))
    for i, r in enumerate(rotulos):
        if i % passo == 0:
            p.append(f'<text x="{x(i):.1f}" y="{altura - 8}" text-anchor="middle" font-size="11" fill="{MUDO}">{escape(r)}</text>')
    if marca is not None and n > 1:
        xm = x(min(max(marca, 0), n - 1))
        p.append(f'<line x1="{xm:.1f}" x2="{xm:.1f}" y1="{mt}" y2="{mt + ph}" stroke="{EIXO}" stroke-width="1"/>')
        p.append(f'<text x="{xm:.1f}" y="{mt - 4}" text-anchor="middle" font-size="10" fill="{MUDO}">{escape(marca_rotulo)}</text>')
    ocupados = []
    for k, s in enumerate(series):
        cor = CORES[k % len(CORES)]
        pontos = [(i, v) for i, v in enumerate(s["valores"]) if v is not None]
        if len(pontos) > 1:
            caminho = " ".join(f"{x(i):.1f},{y(v):.1f}" for i, v in pontos)
            p.append(f'<polyline points="{caminho}" fill="none" stroke="{cor}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>')
        for i, v in pontos:
            p.append(f'<circle cx="{x(i):.1f}" cy="{y(v):.1f}" r="9" fill="transparent"><title>{escape(s["nome"])} · {escape(rotulos[i])}: {numero(v, 2)}</title></circle>')
        if pontos:
            i, v = pontos[-1]
            p.append(f'<circle cx="{x(i):.1f}" cy="{y(v):.1f}" r="4.5" fill="{cor}" stroke="{SUPERFICIE}" stroke-width="2" pointer-events="none"/>')
            if all(abs(y(v) - o) >= 13 for o in ocupados):  # rótulo final só quando não colide com outro
                ocupados.append(y(v))
                p.append(f'<text x="{x(i) + 9:.1f}" y="{y(v) + 4:.1f}" font-size="11" font-weight="600" fill="{TINTA2}">{numero(v)}</text>')
    p.append("</svg>")
    return {"svg": Markup("".join(p)), "legenda": [(s["nome"], CORES[k % len(CORES)]) for k, s in enumerate(series)],
            "tabela": _tabela(series, rotulos)}


def colunas(series, rotulos, descricao, largura=640, altura=230, ticks=None):
    """Colunas agrupadas (até 3 séries). O valor aparece no topo das colunas da última série."""
    linhas_rotulo = max((len(str(r).split(" ")) for r in rotulos), default=1) if len(rotulos) > 6 else 1
    ml, mr, mt, mb = 48, 12, 18, 14 + 14 * linhas_rotulo
    pw, ph = largura - ml - mr, altura - mt - mb
    todos = [v for s in series for v in s["valores"] if v is not None]
    ticks = ticks or escala(max(todos) if todos else 1)
    topo, n, k = ticks[-1], max(len(rotulos), 1), max(len(series), 1)
    banda = pw / n
    larg = max(4, min(24, (banda - 12) / k - 2))
    grupo = k * larg + (k - 1) * 2
    base = mt + ph
    p = _base(largura, altura, ml, mt, pw, ph, ticks, descricao)
    passo = max(1, math.ceil(n / 12))
    for i, r in enumerate(rotulos):
        centro = ml + banda * i + banda / 2
        if i % passo == 0:
            partes_rotulo = str(r).split(" ") if linhas_rotulo > 1 else [str(r)]
            spans = "".join(f'<tspan x="{centro:.1f}" dy="{0 if k == 0 else 13}">{escape(t)}</tspan>' for k, t in enumerate(partes_rotulo))
            p.append(f'<text x="{centro:.1f}" y="{base + 18}" text-anchor="middle" font-size="11" fill="{MUDO}">{spans}</text>')
        for j, s in enumerate(series):
            v = s["valores"][i]
            if v is None:
                continue
            h = ph * v / topo
            x0 = centro - grupo / 2 + j * (larg + 2)
            raio = min(4, h, larg / 2)
            y0 = base - h
            p.append(
                f'<path d="M{x0:.1f},{base} L{x0:.1f},{y0 + raio:.1f} Q{x0:.1f},{y0:.1f} {x0 + raio:.1f},{y0:.1f} '
                f'L{x0 + larg - raio:.1f},{y0:.1f} Q{x0 + larg:.1f},{y0:.1f} {x0 + larg:.1f},{y0 + raio:.1f} L{x0 + larg:.1f},{base} Z" '
                f'fill="{CORES[j % len(CORES)]}"><title>{escape(s["nome"])} · {escape(r)}: {numero(v, 2)}</title></path>'
            )
            if j == k - 1 and n <= 10:
                p.append(f'<text x="{x0 + larg / 2:.1f}" y="{y0 - 4:.1f}" text-anchor="middle" font-size="11" font-weight="600" fill="{TINTA2}">{numero(v)}</text>')
    p.append("</svg>")
    return {"svg": Markup("".join(p)), "legenda": [(s["nome"], CORES[j % len(CORES)]) for j, s in enumerate(series)],
            "tabela": _tabela(series, rotulos)}
