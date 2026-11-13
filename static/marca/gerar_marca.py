"""Gera a marca Octante (símbolo, logotipo horizontal, versão negativa e favicon) em SVG."""
import math
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

TINTA = "#3A1D6E"     # roxo profundo
AMBAR = "#FF9A1F"     # laranja (o octante em destaque)
MUDO = "#6B5A88"
BRANCO = "#FFFFFF"


def texto_em_caminho(texto, fonte, tamanho, x, y, espacamento=0):
    f = TTFont(fonte)
    gs = f.getGlyphSet()
    cmap = f.getBestCmap()
    upm = f["head"].unitsPerEm
    esc = tamanho / upm
    hmtx = f["hmtx"]
    caminhos, cursor = [], x
    for ch in texto:
        nome = cmap[ord(ch)]
        pen = SVGPathPen(gs)
        tp = TransformPen(pen, (esc, 0, 0, -esc, cursor, y))
        gs[nome].draw(tp)
        caminhos.append(pen.getCommands())
        cursor += hmtx[nome][0] * esc + espacamento
    return " ".join(caminhos), cursor - x


def polar(cx, cy, r, graus):
    a = math.radians(graus - 90)  # 0° = norte
    return cx + r * math.cos(a), cy + r * math.sin(a)


def simbolo(cx=32, cy=32, r=28, fundo=TINTA, linhas="rgba(255,255,255,.16)", destaque=AMBAR, divisoes=True):
    """Círculo dividido em 8 partes (os 8 domínios); um octante destacado e deslocado para fora: o projeto avançando no rumo certo."""
    partes = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fundo}"/>']
    if divisoes:
        for k in range(8):
            x, y = polar(cx, cy, r - 3, k * 45)
            partes.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.2f}" y2="{y:.2f}" stroke="{linhas}" stroke-width="1.4"/>')
        # 12 marcas no aro: os 12 princípios
        for k in range(12):
            x1, y1 = polar(cx, cy, r - 2.2, k * 30)
            x2, y2 = polar(cx, cy, r - 5.2, k * 30)
            partes.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{linhas}" stroke-width="1.6" stroke-linecap="round"/>')
    # octante: de 0° a 45°, deslocado 3,5 px na direção da bissetriz (22,5°)
    dx, dy = polar(0, 0, 3.5, 22.5)
    ox, oy = cx + dx, cy + dy
    a = polar(ox, oy, r, 0)
    b = polar(ox, oy, r, 45)
    partes.append(f'<path d="M{ox:.2f} {oy:.2f} L{a[0]:.2f} {a[1]:.2f} A{r} {r} 0 0 1 {b[0]:.2f} {b[1]:.2f} Z" fill="{destaque}"/>')
    partes.append(f'<circle cx="{cx}" cy="{cy}" r="3" fill="{destaque}"/>')
    return "\n  ".join(partes)


def svg(conteudo, w, h, titulo):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-labelledby="t">\n'
            f'  <title id="t">{titulo}</title>\n  {conteudo}\n</svg>\n')


POP_SB = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
POP_M = "/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf"
POP_R = "/usr/share/fonts/truetype/google-fonts/Poppins-Regular.ttf"

# Símbolo
open("octante-simbolo.svg", "w").write(svg(simbolo(), 64, 64, "Octante"))
# Favicon: sem divisões (legível em 16 px)
open("octante-favicon.svg", "w").write(svg(simbolo(divisoes=False), 64, 64, "Octante"))

# Logotipo horizontal
d_nome, larg_nome = texto_em_caminho("octante", POP_SB, 44, 0, 0, espacamento=-0.6)
d_tag, larg_tag = texto_em_caminho("GESTÃO DE PROJETOS · PMBOK® 7", POP_M, 10.5, 0, 0, espacamento=1.6)
L = 64 + 16 + max(larg_nome, larg_tag) + 6


def logotipo(cor_nome, cor_tag, fundo_simbolo, linhas):
    return (simbolo(fundo=fundo_simbolo, linhas=linhas) +
            f'\n  <path transform="translate(80 43)" fill="{cor_nome}" d="{d_nome}"/>'
            f'\n  <path transform="translate(82 60)" fill="{cor_tag}" d="{d_tag}"/>')


open("octante-logo.svg", "w").write(svg(logotipo(TINTA, MUDO, TINTA, "rgba(255,255,255,.16)"), round(L), 64, "Octante: gestão de projetos"))
# Negativo (para fundos escuros): símbolo com aro claro
open("octante-logo-negativo.svg", "w").write(svg(logotipo(BRANCO, "#CDBFEA", "#5A35A0", "rgba(255,255,255,.22)"), round(L), 64, "Octante: gestão de projetos"))
# Só o nome (para o topo do app)
d_topo, larg_topo = texto_em_caminho("octante", POP_SB, 22, 0, 0, espacamento=-0.3)
open("octante-nome-negativo.svg", "w").write(svg(f'<path transform="translate(0 20)" fill="{BRANCO}" d="{d_topo}"/>', round(larg_topo) + 2, 26, "Octante"))
print("ok", round(L))
open("octante-simbolo-negativo.svg", "w").write(svg(simbolo(fundo="#5A35A0", linhas="rgba(255,255,255,.24)"), 64, 64, "Octante"))
