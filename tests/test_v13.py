"""Testes da versão 13: segurança dos dados."""
import os
import re
import shutil
import sqlite3

import pytest

import backup
from ajuda import banco_na_versao, html, novo_projeto
from app import create_app
from db import VERSAO_ATUAL, get_db


def contar(client, sql, *args):
    with client.application.app_context():
        return get_db().execute(sql, args).fetchone()[0]


def test_historico_registra_quem_e_o_que_sem_senha(tmp_path):
    app = create_app({"TESTING": True, "LOGIN_OBRIGATORIO": True, "DATABASE": str(tmp_path / "h.db"), "SECRET_KEY": "x"})
    c = app.test_client()
    c.post("/primeiro-acesso", data={"nome": "Denner Ramiro", "login": "denner", "senha": "senha12345", "confirmacao": "senha12345"})
    pid = novo_projeto(c, "adaptativa")
    c.post(f"/p/{pid}/incerteza/riscos/novo", data={"titulo": "API mudar de preço", "tipo": "ameaca", "status": "aberto"})
    pagina = html(c, f"/p/{pid}/historico")
    assert "Denner Ramiro" in pagina and "API mudar de preço" in pagina and "criou" in pagina
    assert contar(c, "SELECT COUNT(*) FROM auditoria WHERE antes LIKE '%senha_hash%' OR depois LIKE '%senha_hash%'") == 0


def test_so_atualizado_em_nao_gera_historico(client):
    pid = novo_projeto(client)
    antes = contar(client, "SELECT COUNT(*) FROM auditoria")
    with client.application.app_context():
        db = get_db(); db.execute("UPDATE projeto SET atualizado_em = '2030-01-01' WHERE id = ?", (pid,)); db.commit()
    assert contar(client, "SELECT COUNT(*) FROM auditoria") == antes


def test_projeto_excluido_volta_inteiro_da_lixeira(client):
    pid = novo_projeto(client, "adaptativa")
    client.post(f"/p/{pid}/partes/nova", data={"nome": "Patrocinadora", "papel": "Diretora", "categoria": "Patrocinador", "ativa": "1"})
    client.post(f"/p/{pid}/incerteza/riscos/novo", data={"titulo": "R", "tipo": "ameaca", "status": "aberto", "probabilidade": "3", "impacto": "4"})
    tabelas = ["projeto", "abertura", "parte_interessada", "risco"]
    antes = {t: contar(client, f"SELECT COUNT(*) FROM {t}") for t in tabelas}
    client.post(f"/p/{pid}/excluir", data={"confirmar": "sim"})
    assert contar(client, "SELECT COUNT(*) FROM projeto") == 0
    assert "Restaurar projeto" in html(client, "/admin/dados")
    lote = contar(client, "SELECT lote FROM auditoria WHERE acao = 'D' AND tabela = 'projeto'")
    client.post("/admin/dados", data={"acao": "restaurar_lote", "lote": lote})
    assert {t: contar(client, f"SELECT COUNT(*) FROM {t}") for t in tabelas} == antes
    assert client.get(f"/p/{pid}/incerteza/riscos").status_code == 200


def test_registro_excluido_pode_ser_restaurado(client):
    pid = novo_projeto(client)
    client.post(f"/p/{pid}/incerteza/riscos/novo", data={"titulo": "Volta", "tipo": "ameaca", "status": "aberto"})
    rid = contar(client, "SELECT id FROM risco")
    client.post(f"/p/{pid}/incerteza/riscos/{rid}/excluir")
    assert contar(client, "SELECT COUNT(*) FROM risco") == 0
    lote = contar(client, "SELECT lote FROM auditoria WHERE acao = 'D' AND tabela = 'risco'")
    client.post("/admin/dados", data={"acao": "restaurar_lote", "lote": lote})
    assert contar(client, "SELECT titulo FROM risco") == "Volta"


def test_validacoes_dentro_do_banco(client):
    pid = novo_projeto(client)
    with client.application.app_context():
        db = get_db()
        with pytest.raises(sqlite3.IntegrityError):
            db.execute("INSERT INTO risco (projeto_id, codigo, titulo, probabilidade) VALUES (?, 1, 'x', 9)", (pid,))
        with pytest.raises(sqlite3.IntegrityError):
            db.execute("INSERT INTO iteracao (projeto_id, nome, inicio, fim) VALUES (?, 'S', '2026-02-01', '2026-01-01')", (pid,))


def test_backup_antes_de_migrar(tmp_path):
    caminho = tmp_path / "antigo.db"
    banco_na_versao(caminho, 9)
    con = sqlite3.connect(caminho); con.execute("INSERT INTO projeto (nome) VALUES ('Antigo')"); con.commit(); con.close()
    create_app({"TESTING": True, "DATABASE": str(caminho), "SECRET_KEY": "x"})
    feitos = backup.listar(str(caminho))
    assert any(b["motivo"] == "antes de migrar" for b in feitos)
    ok, _, info = backup.verificar(os.path.join(backup.pasta(str(caminho)), feitos[0]["nome"]))
    assert ok and info["versao"] == 9 and info["projetos"] >= 1


def test_backup_detecta_adulteracao_e_restaura(client):
    banco = client.application.config["DATABASE"]
    novo_projeto(client, nome="Original")
    client.post("/admin/dados", data={"acao": "backup_agora"})
    nome = backup.listar(banco)[0]["nome"]
    novo_projeto(client, nome="Depois do backup")
    client.post("/admin/dados", data={"acao": "restaurar_backup", "nome": nome})
    assert contar(client, "SELECT COUNT(*) FROM projeto") == 1
    assert any(b["motivo"] == "antes de restaurar" for b in backup.listar(banco))
    cam = os.path.join(backup.pasta(banco), nome)
    with open(cam, "r+b") as f:  # adultera 1 byte no meio do arquivo
        f.seek(2000); b = f.read(1); f.seek(2000); f.write(bytes([b[0] ^ 1]))
    ok, msg, _ = backup.verificar(cam)
    assert not ok


def test_envio_de_arquivo_invalido_e_recusado(client):
    import io
    novo_projeto(client, nome="Fica")
    r = client.post("/admin/dados", data={"acao": "enviar_backup", "arquivo": (io.BytesIO(b"nao sou um banco"), "x.db")},
                    content_type="multipart/form-data", follow_redirects=True)
    assert "não é um banco SQLite" in r.get_data(as_text=True)
    assert contar(client, "SELECT COUNT(*) FROM projeto") == 1


def test_csrf_e_cabecalhos(tmp_path):
    app = create_app({"TESTING": True, "CSRF_ATIVO": True, "DATABASE": str(tmp_path / "c.db"), "SECRET_KEY": "x"})
    c = app.test_client()
    r = c.get("/projetos/novo")
    assert r.headers["X-Frame-Options"] == "DENY" and "frame-ancestors 'none'" in r.headers["Content-Security-Policy"]
    token = re.search(r'name="_csrf" value="([^"]+)"', r.get_data(as_text=True)).group(1)
    assert c.post("/projetos/novo", data={"nome": "Sem token"}).status_code == 400
    assert c.post("/projetos/novo", data={"nome": "Com token", "_csrf": token}).status_code == 302


def test_trocar_senha_encerra_outras_sessoes(tmp_path):
    app = create_app({"TESTING": True, "LOGIN_OBRIGATORIO": True, "DATABASE": str(tmp_path / "s.db"), "SECRET_KEY": "x"})
    a, b = app.test_client(), app.test_client()
    a.post("/primeiro-acesso", data={"nome": "Ana", "login": "ana", "senha": "senha12345", "confirmacao": "senha12345"})
    b.post("/entrar", data={"login": "ana", "senha": "senha12345"})
    assert b.get("/").status_code == 200
    a.post("/minha-senha", data={"atual": "senha12345", "senha": "outra12345", "confirmacao": "outra12345"})
    assert a.get("/").status_code == 200          # quem trocou continua
    assert "/entrar" in b.get("/").headers["Location"]  # a outra sessão caiu


def test_bloqueio_por_conta_mesmo_trocando_de_ip(tmp_path):
    import auth
    auth._tentativas.clear()
    app = create_app({"TESTING": True, "LOGIN_OBRIGATORIO": True, "DATABASE": str(tmp_path / "b.db"), "SECRET_KEY": "x"})
    c = app.test_client()
    c.post("/primeiro-acesso", data={"nome": "Ana", "login": "ana", "senha": "senha12345", "confirmacao": "senha12345"})
    c.post("/sair")
    for i in range(5):
        c.post("/entrar", data={"login": "ana", "senha": "errada"}, environ_base={"REMOTE_ADDR": f"10.0.0.{i}"})
    r = c.post("/entrar", data={"login": "ana", "senha": "senha12345"}, environ_base={"REMOTE_ADDR": "10.0.0.99"})
    assert "Muitas tentativas" in r.get_data(as_text=True)
    auth._tentativas.clear()


def test_anonimizar_projeto_encerrado(client):
    pid = novo_projeto(client, "adaptativa")
    client.post(f"/p/{pid}/partes/nova", data={"nome": "Lúcia", "papel": "x", "categoria": "Cliente", "ativa": "1",
                                               "contato": "lucia@clinica.com", "crencas": "Desconfia de apps"})
    client.post(f"/p/{pid}/anonimizar")
    assert contar(client, "SELECT contato FROM parte_interessada") == "lucia@clinica.com"  # projeto ativo: recusa
    client.post(f"/p/{pid}/encerramento", data={"acao": "cancelar", "justificativa": "x", "avaliacao_objetivos": "x"})
    client.post(f"/p/{pid}/anonimizar")
    assert contar(client, "SELECT contato || crencas FROM parte_interessada") == ""


def test_fuso_horario_de_brasilia():
    assert os.environ.get("TZ") == "America/Sao_Paulo"


def test_backup_automatico_diario(tmp_path):
    caminho = str(tmp_path / "auto.db")
    app = create_app({"TESTING": True, "BACKUP_AUTOMATICO": True, "DATABASE": caminho, "SECRET_KEY": "x"})
    c = app.test_client()
    novo_projeto(c, nome="Com dados")
    app2 = create_app({"TESTING": True, "BACKUP_AUTOMATICO": True, "DATABASE": caminho, "SECRET_KEY": "x"})
    app2.test_client().get("/")
    assert any(b["motivo"] == "automatico" for b in backup.listar(caminho))
