"""Testes da versão 11: login e usuários para publicar o app."""
import pytest

from app import create_app


@pytest.fixture()
def c(tmp_path):
    app = create_app({"TESTING": True, "LOGIN_OBRIGATORIO": True, "DATABASE": str(tmp_path / "l.db"), "SECRET_KEY": "x"})
    with app.test_client() as cliente:
        yield cliente


def admin(c, login="admin", senha="senhaforte1"):
    return c.post("/primeiro-acesso", data={"nome": "Denner Ramiro", "login": login, "senha": senha, "confirmacao": senha})


def test_sem_usuarios_vai_para_primeiro_acesso(c):
    r = c.get("/")
    assert r.status_code == 302 and "/primeiro-acesso" in r.headers["Location"]


def test_primeiro_acesso_cria_admin_e_depois_fecha(c):
    assert admin(c).status_code == 302
    assert c.get("/").status_code == 200
    c.post("/sair")
    r = c.get("/primeiro-acesso")
    assert "/entrar" in r.headers["Location"]
    assert c.post("/primeiro-acesso", data={"nome": "X", "login": "x", "senha": "12345678", "confirmacao": "12345678"}).status_code == 302
    r = c.post("/entrar", data={"login": "x", "senha": "12345678"})
    assert "incorretos" in r.get_data(as_text=True)


def test_paginas_e_posts_exigem_login(c):
    admin(c)
    c.post("/sair")
    for url in ["/", "/projetos/novo", "/backup", "/usuarios", "/p/1"]:
        r = c.get(url)
        assert r.status_code == 302 and "/entrar" in r.headers["Location"], url
    assert c.post("/projetos/novo", data={"nome": "invasor"}).status_code == 302
    assert c.get("/static/style.css").status_code == 200


def test_senha_curta_e_senhas_diferentes(c):
    r = c.post("/primeiro-acesso", data={"nome": "A", "login": "a", "senha": "123", "confirmacao": "123"})
    assert "pelo menos 8" in r.get_data(as_text=True)
    r = c.post("/primeiro-acesso", data={"nome": "A", "login": "a", "senha": "12345678", "confirmacao": "87654321"})
    assert "não conferem" in r.get_data(as_text=True)


def test_redirecionamento_apos_login_e_seguro(c):
    admin(c)
    c.post("/sair")
    assert c.post("/entrar", data={"login": "admin", "senha": "senhaforte1", "proximo": "/projetos/novo"}).headers["Location"].endswith("/projetos/novo")
    c.post("/sair")
    for ruim in ["https://malicioso.com", "//malicioso.com", "javascript:alert(1)"]:
        r = c.post("/entrar", data={"login": "admin", "senha": "senhaforte1", "proximo": ruim})
        assert "malicioso" not in r.headers["Location"] and "javascript" not in r.headers["Location"]
        c.post("/sair")


def test_bloqueio_apos_tentativas_erradas(c):
    admin(c)
    c.post("/sair")
    for _ in range(5):
        c.post("/entrar", data={"login": "admin", "senha": "errada"})
    r = c.post("/entrar", data={"login": "admin", "senha": "senhaforte1"})
    assert "Muitas tentativas" in r.get_data(as_text=True)
    import auth
    auth._tentativas.clear()


def test_admin_cadastra_estagiario_que_nao_e_admin(c):
    admin(c)
    c.post("/usuarios", data={"acao": "criar", "nome": "Ana", "login": "Ana.Souza", "senha": "estagio123"})
    c.post("/sair")
    assert c.post("/entrar", data={"login": "ana.souza", "senha": "estagio123"}).status_code == 302
    assert c.get("/").status_code == 200
    assert c.get("/usuarios").status_code == 403
    assert c.get("/backup").status_code == 403
    # troca a própria senha
    c.post("/minha-senha", data={"atual": "estagio123", "senha": "novasenha9", "confirmacao": "novasenha9"})
    c.post("/sair")
    assert c.post("/entrar", data={"login": "ana.souza", "senha": "novasenha9"}).status_code == 302


def test_usuario_desativado_perde_acesso(c, tmp_path):
    admin(c)
    c.post("/usuarios", data={"acao": "criar", "nome": "Ana", "login": "ana", "senha": "estagio123"})
    c.post("/sair")
    c.post("/entrar", data={"login": "ana", "senha": "estagio123"})
    with c.application.app_context():
        from db import get_db
        db = get_db()
        db.execute("UPDATE usuario SET ativo = 0 WHERE login = 'ana'")
        db.commit()
    r = c.get("/")
    assert r.status_code == 302 and "/entrar" in r.headers["Location"]


def test_wsgi_liga_cookie_seguro(monkeypatch, tmp_path):
    monkeypatch.setenv("GESTOR_PRODUCAO", "1")
    app = create_app({"DATABASE": str(tmp_path / "w.db"), "SECRET_KEY": "x"})
    assert app.config["SESSION_COOKIE_SECURE"] and app.config["LOGIN_OBRIGATORIO"]
