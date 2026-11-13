"""Login e usuários (v11).

Com o app publicado na internet, ninguém entra sem usuário e senha. O primeiro acesso cria o administrador;
depois, só o administrador cadastra pessoas (por exemplo, os estagiários do PMO) e redefine senhas.
"""
import time
from urllib.parse import urlparse

from flask import Blueprint, abort, current_app, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from db import get_db

bp = Blueprint("auth", __name__)

LIVRES = {"auth.entrar", "auth.primeiro_acesso", "static"}
SENHA_MINIMA = 8
MAX_TENTATIVAS = 5
BLOQUEIO_SEGUNDOS = 300
_tentativas = {}  # ip -> (falhas, bloqueado_ate)


def login_ativo():
    return current_app.config.get("LOGIN_OBRIGATORIO", True)


def existe_usuario():
    return get_db().execute("SELECT 1 FROM usuario LIMIT 1").fetchone() is not None


def _destino_seguro(alvo):
    """Só aceita caminhos internos (evita redirecionar para outro site depois do login)."""
    if not alvo or not alvo.startswith("/") or alvo.startswith("//") or urlparse(alvo).netloc:
        return url_for("inicio")
    return alvo


def _validar_senha(senha, confirmacao):
    if len(senha) < SENHA_MINIMA:
        return f"A senha precisa ter pelo menos {SENHA_MINIMA} caracteres."
    if senha != confirmacao:
        return "As senhas não conferem."
    return None


@bp.before_app_request
def exigir_login():
    g.usuario = None
    uid = session.get("uid")
    if uid:
        g.usuario = get_db().execute("SELECT * FROM usuario WHERE id = ? AND ativo = 1", (uid,)).fetchone()
        # Trocar a senha encerra as outras sessões abertas dessa pessoa.
        if g.usuario is None or session.get("sv") != _versao_sessao(g.usuario):
            g.usuario = None
            session.clear()
    # gestor.interno: requisições feitas pelo próprio servidor (ex.: criar o projeto de exemplo); não vêm da rede
    if not login_ativo() or request.endpoint in LIVRES or request.environ.get("gestor.interno"):
        return None
    if g.usuario is None:
        if not existe_usuario():
            return redirect(url_for("auth.primeiro_acesso"))
        return redirect(url_for("auth.entrar", proximo=request.full_path.rstrip("?")))
    return None


def _versao_sessao(usuario):
    return usuario["senha_hash"][-16:]


def _iniciar_sessao(usuario):
    session.clear()
    session["uid"] = usuario["id"]
    session["sv"] = _versao_sessao(usuario)
    session.permanent = True


def exigir_admin():
    if login_ativo() and not (g.usuario and g.usuario["admin"]):
        abort(403)


@bp.app_context_processor
def contexto_usuario():
    return {"usuario_atual": g.get("usuario"), "login_ativo": login_ativo()}


@bp.route("/primeiro-acesso", methods=["GET", "POST"])
def primeiro_acesso():
    if existe_usuario():
        return redirect(url_for("auth.entrar"))
    erro = None
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        login = request.form.get("login", "").strip().lower()
        erro = (None if nome and login else "Preencha nome e usuário.") or _validar_senha(
            request.form.get("senha", ""), request.form.get("confirmacao", ""))
        if not erro:
            db = get_db()
            cur = db.execute("INSERT INTO usuario (nome, login, senha_hash, admin) VALUES (?, ?, ?, 1)",
                             (nome, login, generate_password_hash(request.form["senha"])))
            db.commit()
            _iniciar_sessao(db.execute("SELECT * FROM usuario WHERE id = ?", (cur.lastrowid,)).fetchone())
            flash("Conta de administrador criada. Cadastre os outros usuários em “Usuários”, no topo.", "ok")
            return redirect(url_for("inicio"))
    return render_template("primeiro_acesso.html", erro=erro)


@bp.route("/entrar", methods=["GET", "POST"])
def entrar():
    if not existe_usuario():
        return redirect(url_for("auth.primeiro_acesso"))
    erro = None
    if request.method == "POST":
        login = request.form.get("login", "").strip().lower()
        chaves = ("ip:" + (request.remote_addr or "?"), "login:" + login)  # bloqueia por máquina e por conta
        if any(_tentativas.get(k, (0, 0))[1] > time.time() for k in chaves):
            erro = "Muitas tentativas erradas. Aguarde alguns minutos e tente de novo."
        else:
            u = get_db().execute("SELECT * FROM usuario WHERE login = ? AND ativo = 1", (login,)).fetchone()
            if u and check_password_hash(u["senha_hash"], request.form.get("senha", "")):
                for k in chaves:
                    _tentativas.pop(k, None)
                _iniciar_sessao(u)
                return redirect(_destino_seguro(request.form.get("proximo")))
            for k in chaves:
                falhas = _tentativas.get(k, (0, 0))[0] + 1
                _tentativas[k] = (0, time.time() + BLOQUEIO_SEGUNDOS) if falhas >= MAX_TENTATIVAS else (falhas, 0)
            erro = "Usuário ou senha incorretos."
    return render_template("entrar.html", erro=erro, proximo=request.values.get("proximo", ""))


@bp.route("/sair", methods=["POST"])
def sair():
    session.clear()
    flash("Você saiu.", "ok")
    return redirect(url_for("auth.entrar"))


@bp.route("/minha-senha", methods=["GET", "POST"])
def minha_senha():
    if g.usuario is None:
        return redirect(url_for("auth.entrar"))
    erro = None
    if request.method == "POST":
        if not check_password_hash(g.usuario["senha_hash"], request.form.get("atual", "")):
            erro = "A senha atual está incorreta."
        else:
            erro = _validar_senha(request.form.get("senha", ""), request.form.get("confirmacao", ""))
        if not erro:
            db = get_db()
            db.execute("UPDATE usuario SET senha_hash = ? WHERE id = ?", (generate_password_hash(request.form["senha"]), g.usuario["id"]))
            db.commit()
            _iniciar_sessao(db.execute("SELECT * FROM usuario WHERE id = ?", (g.usuario["id"],)).fetchone())
            flash("Senha alterada. Outras sessões abertas com a senha antiga foram encerradas.", "ok")
            return redirect(url_for("inicio"))
    return render_template("minha_senha.html", erro=erro)


@bp.route("/usuarios", methods=["GET", "POST"])
def usuarios():
    exigir_admin()
    db = get_db()
    erro = None
    if request.method == "POST":
        acao = request.form.get("acao")
        uid = request.form.get("usuario_id", type=int)
        if acao == "criar":
            nome = request.form.get("nome", "").strip()
            login = request.form.get("login", "").strip().lower()
            erro = (None if nome and login else "Preencha nome e usuário.") or _validar_senha(
                request.form.get("senha", ""), request.form.get("senha", ""))
            if not erro and db.execute("SELECT 1 FROM usuario WHERE login = ?", (login,)).fetchone():
                erro = "Já existe alguém com esse usuário."
            if not erro:
                db.execute("INSERT INTO usuario (nome, login, senha_hash, admin) VALUES (?, ?, ?, ?)",
                           (nome, login, generate_password_hash(request.form["senha"]), 1 if request.form.get("admin") else 0))
                db.commit()
                flash(f"Usuário {login} criado. Passe a senha à pessoa e peça que a troque em “Minha senha”.", "ok")
                return redirect(url_for("auth.usuarios"))
        elif uid:
            alvo = db.execute("SELECT * FROM usuario WHERE id = ?", (uid,)).fetchone()
            if alvo is None:
                abort(404)
            if acao == "senha":
                erro = _validar_senha(request.form.get("senha", ""), request.form.get("senha", ""))
                if not erro:
                    db.execute("UPDATE usuario SET senha_hash = ? WHERE id = ?", (generate_password_hash(request.form["senha"]), uid))
                    db.commit()
                    flash(f"Senha de {alvo['login']} redefinida.", "ok")
                    return redirect(url_for("auth.usuarios"))
            elif acao == "ativo":
                if uid == g.usuario["id"]:
                    erro = "Você não pode desativar a própria conta."
                else:
                    db.execute("UPDATE usuario SET ativo = 1 - ativo WHERE id = ?", (uid,))
                    db.commit()
                    return redirect(url_for("auth.usuarios"))
    lista = db.execute("SELECT * FROM usuario ORDER BY ativo DESC, nome").fetchall()
    return render_template("usuarios.html", usuarios=lista, erro=erro)
