"""Proteções da aplicação web (v13): CSRF, cabeçalhos de segurança, limites de tamanho e fuso horário."""
import hmac
import os
import re
import secrets
import time

from flask import abort, current_app, render_template, request, session

TAMANHO_MAX_CAMPO = 20000          # caracteres por campo de formulário
FORM_POST = re.compile(r'(<form\b[^>]*\bmethod=["\']?post["\']?[^>]*>)', re.IGNORECASE)


def configurar_fuso():
    """Datas do app no horário de Brasília, mesmo em servidores em UTC (ex.: PythonAnywhere)."""
    os.environ.setdefault("TZ", os.environ.get("GESTOR_FUSO", "America/Sao_Paulo"))
    if hasattr(time, "tzset"):
        time.tzset()


def token_csrf():
    if "_csrf" not in session:
        session["_csrf"] = secrets.token_urlsafe(32)
    return session["_csrf"]


def registrar(app):
    app.config.setdefault("MAX_CONTENT_LENGTH", 60 * 1024 * 1024)  # 60 MB (restauração de backup)
    app.config.setdefault("CSRF_ATIVO", not app.config.get("TESTING", False))

    @app.before_request
    def validar_post():
        if request.method != "POST":
            return None
        for valor in request.form.values():
            if len(valor) > TAMANHO_MAX_CAMPO:
                abort(413)
        if current_app.config["CSRF_ATIVO"] and not request.environ.get("gestor.interno"):
            enviado = request.form.get("_csrf") or request.headers.get("X-CSRF-Token", "")
            if not enviado or not hmac.compare_digest(enviado, session.get("_csrf", "")):
                return render_template("erro.html", titulo="Formulário expirado",
                                       mensagem="Por segurança, o formulário expirou. Volte, recarregue a página e envie de novo."), 400
        return None

    @app.context_processor
    def contexto_csrf():
        return {"csrf_token": token_csrf}

    @app.after_request
    def proteger_resposta(resposta):
        if resposta.mimetype == "text/html" and not resposta.direct_passthrough:
            html = resposta.get_data(as_text=True)
            if "<form" in html.lower():
                campo = f'<input type="hidden" name="_csrf" value="{token_csrf()}">'
                resposta.set_data(FORM_POST.sub(lambda m: m.group(1) + campo, html))
        h = resposta.headers
        h.setdefault("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; "
                     "img-src 'self' data:; object-src 'none'; base-uri 'self'; form-action 'self'; frame-ancestors 'none'")
        h.setdefault("X-Content-Type-Options", "nosniff")
        h.setdefault("X-Frame-Options", "DENY")
        h.setdefault("Referrer-Policy", "same-origin")
        h.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        if current_app.config.get("SESSION_COOKIE_SECURE"):
            h.setdefault("Strict-Transport-Security", "max-age=31536000")
        if request.endpoint and request.endpoint != "static":
            h.setdefault("Cache-Control", "no-store")  # páginas com dados não ficam no cache do navegador
        return resposta
