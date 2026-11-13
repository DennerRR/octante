"""Funções compartilhadas entre os módulos de rotas."""
import re

from flask import abort

from db import get_db


def inteiro(valor, minimo=1, maximo=5):
    try:
        n = int(valor)
    except (TypeError, ValueError):
        return None
    return n if minimo <= n <= maximo else None


def decimal(valor, minimo=0.0):
    """Converte valores em formato brasileiro para float; vazio ou inválido -> None.

    '1.234,56' -> 1234.56 · '50.000' -> 50000 (ponto como milhar) · '1500.5' -> 1500.5
    """
    if valor is None:
        return None
    texto = str(valor).strip().replace("R$", "").replace(" ", "")
    if not texto:
        return None
    if "," in texto:
        texto = texto.replace(".", "").replace(",", ".")
    elif re.fullmatch(r"-?\d{1,3}(\.\d{3})+", texto):
        texto = texto.replace(".", "")
    try:
        n = float(texto)
    except ValueError:
        return None
    return n if n >= minimo else None


def pode_acessar(projeto_id):
    """Administrador vê tudo; os demais só os projetos em que foram incluídos (v14)."""
    from flask import current_app, g
    from flask import request
    if not current_app.config.get("LOGIN_OBRIGATORIO", True) or request.environ.get("gestor.interno"):
        return True
    u = g.get("usuario")
    if u is None:
        return False
    if u["admin"]:
        return True
    return get_db().execute("SELECT 1 FROM usuario_projeto WHERE usuario_id = ? AND projeto_id = ?",
                            (u["id"], projeto_id)).fetchone() is not None


def filtro_projetos(coluna="p.id"):
    """Trecho SQL + argumentos que restringem uma consulta aos projetos visíveis ao usuário."""
    from flask import current_app, g
    u = g.get("usuario")
    if not current_app.config.get("LOGIN_OBRIGATORIO", True) or (u is not None and u["admin"]):
        return "1 = 1", []
    if u is None:
        return "0 = 1", []
    return f"{coluna} IN (SELECT projeto_id FROM usuario_projeto WHERE usuario_id = ?)", [u["id"]]


def obter_projeto(projeto_id):
    p = get_db().execute("SELECT * FROM projeto WHERE id = ?", (projeto_id,)).fetchone()
    if p is None or not pode_acessar(projeto_id):
        abort(404)  # não revela se o projeto existe
    return p


def tocar_projeto(projeto_id):
    get_db().execute(
        "UPDATE projeto SET atualizado_em = datetime('now','localtime') WHERE id = ?", (projeto_id,)
    )


def moeda(valor):
    if valor is None:
        return "—"
    inteiro_, _, frac = f"{abs(valor):,.2f}".partition(".")
    sinal = "-" if valor < 0 else ""
    return f"{sinal}R$ {inteiro_.replace(',', '.')},{frac}"
