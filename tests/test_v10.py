"""Testes da versão 10: experiência do iniciante e robustez."""
import sqlite3

from ajuda import concluir_fase_iniciar, html, novo_projeto


def test_novo_projeto_leva_ao_fluxo(client):
    r = client.post("/projetos/novo", data={"nome": "Portal"})
    assert "/fluxo" in r.headers["Location"]


def test_visao_geral_de_projeto_novo_mostra_so_o_essencial(client):
    pid = novo_projeto(client)
    pagina = html(client, f"/p/{pid}")
    assert "Fazer agora" in pagina and "Como vamos trabalhar" in pagina
    assert "Situação do projeto" not in pagina and "Domínios de desempenho" not in pagina
    client.post(f"/p/{pid}/abordagem", data={"acao": "salvar", "abordagem": "adaptativa"})
    concluir_fase_iniciar(client, pid)
    pagina = html(client, f"/p/{pid}")
    assert "Situação do projeto" in pagina and "Domínios de desempenho" in pagina


def test_projeto_de_exemplo_pelo_navegador(client):
    assert "Ver projeto de exemplo" in html(client, "/")
    r = client.post("/exemplo")
    assert r.status_code == 302 and "/fluxo" in r.headers["Location"]
    # segundo clique não duplica
    client.post("/exemplo")
    with client.application.app_context():
        from db import get_db
        assert get_db().execute("SELECT COUNT(*) FROM projeto WHERE nome LIKE '%AgendaFácil%'").fetchone()[0] == 1


def test_backup_baixa_banco_sqlite_valido(client, tmp_path):
    novo_projeto(client, nome="Projeto do backup")
    r = client.get("/backup")
    assert r.status_code == 200 and "attachment" in r.headers["Content-Disposition"]
    arquivo = tmp_path / "b.db"
    arquivo.write_bytes(r.data)
    assert sqlite3.connect(arquivo).execute("SELECT nome FROM projeto").fetchone()[0] == "Projeto do backup"


def test_menu_tem_modo_essencial(client):
    pid = novo_projeto(client)
    pagina = html(client, f"/p/{pid}")
    assert 'id="alternar-modo"' in pagina and pagina.count("data-avancado") >= 5


def test_abordagem_tem_atalho_para_iniciante(client):
    pid = novo_projeto(client)
    assert "Primeira vez?" in html(client, f"/p/{pid}/abordagem")
