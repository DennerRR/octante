"""Testes da versão 2: migrações, segurança e domínio de Incerteza."""
import os
import sqlite3
import sys
from datetime import date, timedelta

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pmbok  # noqa: E402
from app import create_app  # noqa: E402
from db import VERSAO_ATUAL  # noqa: E402
from util import decimal, moeda  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture()
def app(tmp_path):
    return create_app({"TESTING": True, "DATABASE": str(tmp_path / "teste.db"), "SECRET_KEY": "teste"})


@pytest.fixture()
def client(app):
    with app.test_client() as c:
        yield c


def criar_projeto(client, nome="App"):
    r = client.post("/projetos/novo", data={"nome": nome})
    return int(r.headers["Location"].split("/p/")[1].split("/")[0])


def criar_risco(client, pid, **campos):
    dados = {"titulo": "Risco", "tipo": "ameaca", "status": "aberto"}
    dados.update(campos)
    r = client.post(f"/p/{pid}/incerteza/riscos/novo", data=dados)
    assert r.status_code == 302, r.get_data(as_text=True)[:500]
    return int(r.headers["Location"].rstrip("/").split("/")[-1])


# ---------------- Migrações ----------------
def test_banco_da_v1_e_migrado_sem_perder_dados(tmp_path):
    caminho = tmp_path / "v1.db"
    conn = sqlite3.connect(caminho)
    with open(os.path.join(RAIZ, "schema.sql"), encoding="utf-8") as f:
        conn.executescript(f.read())  # exatamente o que a v1 criava (user_version = 0)
    conn.execute("INSERT INTO projeto (nome) VALUES ('Projeto antigo')")
    conn.execute("INSERT INTO parte_interessada (projeto_id, nome, poder, interesse) VALUES (1, 'Ana', 5, 5)")
    conn.commit()
    conn.close()

    app = create_app({"TESTING": True, "DATABASE": str(caminho), "SECRET_KEY": "x"})
    conn = sqlite3.connect(caminho)
    assert conn.execute("PRAGMA user_version").fetchone()[0] == VERSAO_ATUAL
    assert conn.execute("SELECT limite_risco, revisao_risco_dias FROM projeto").fetchone() == (12, 14)
    conn.close()
    c = app.test_client()
    assert "Projeto antigo" in c.get("/").get_data(as_text=True)
    assert c.get("/p/1/partes/1").status_code == 200
    assert c.get("/p/1/incerteza").status_code == 200
    # abrir de novo não reaplica migrações
    create_app({"TESTING": True, "DATABASE": str(caminho), "SECRET_KEY": "x"})


# ---------------- Revisão da v1 ----------------
def test_post_de_outra_origem_e_bloqueado(client):
    assert client.post("/projetos/novo", data={"nome": "X"}, headers={"Origin": "http://site-malicioso.com"}).status_code == 403
    assert client.post("/projetos/novo", data={"nome": "X"}, headers={"Origin": "http://localhost"}).status_code == 302


def test_chave_secreta_gerada_e_persistida(tmp_path):
    a = create_app({"DATABASE": str(tmp_path / "a.db")})
    b = create_app({"DATABASE": str(tmp_path / "a.db")})
    assert a.config["SECRET_KEY"] == b.config["SECRET_KEY"] and len(a.config["SECRET_KEY"]) == 64


def test_interacao_com_data_futura_e_rejeitada(client):
    pid = criar_projeto(client)
    client.post(f"/p/{pid}/partes/nova", data={"nome": "Ana", "interna": "1", "ativa": "1"})
    amanha = (date.today() + timedelta(days=1)).isoformat()
    html = client.post(f"/p/{pid}/partes/monitoramento", data={"parte_id": "1", "data": amanha, "resumo": "Futuro"},
                       follow_redirects=True).get_data(as_text=True)
    assert "não pode estar no futuro" in html
    assert "Futuro" not in html.split("Interações recentes")[1]


def test_aviso_ao_alterar_termo_aprovado(client):
    pid = criar_projeto(client)
    base = {"status": "aprovado", "proposito": "p", "objetivos": "o", "criterios_sucesso": "c", "patrocinador": "s", "gerente": "g", "aprovado_por": "s"}
    client.post(f"/p/{pid}/abertura", data=base)
    html = client.post(f"/p/{pid}/abertura", data={**base, "objetivos": "novo"}, follow_redirects=True).get_data(as_text=True)
    assert "já estava aprovado e foi alterado" in html
    html = client.post(f"/p/{pid}/abertura", data={**base, "objetivos": "novo", "visao_texto": "só a visão"},
                       follow_redirects=True).get_data(as_text=True)
    assert "já estava aprovado" not in html


# ---------------- Regras de incerteza ----------------
def test_nivel_risco_respeita_limite():
    assert pmbok.nivel_risco(12, 12) == "alto"
    assert pmbok.nivel_risco(6, 12) == "medio"
    assert pmbok.nivel_risco(5, 12) == "baixo"
    assert pmbok.nivel_risco(5, 5) == "alto"
    assert pmbok.nivel_risco(None, 12) is None


def test_conversao_de_valores():
    assert decimal("1.234,56") == 1234.56
    assert decimal("R$ 500") == 500.0
    assert decimal("1500.5") == 1500.5
    assert decimal("50.000") == 50000.0
    assert decimal("1.250.000") == 1250000.0
    assert decimal("8000,00") == 8000.0
    assert decimal("abc") is None and decimal("") is None and decimal("-3") is None
    assert moeda(-1234.5) == "-R$ 1.234,50"
    assert moeda(None) == "—"


# ---------------- Fluxo de riscos ----------------
def test_codigo_sequencial_e_paginas(client):
    pid = criar_projeto(client)
    r1 = criar_risco(client, pid, titulo="A")
    r2 = criar_risco(client, pid, titulo="B", tipo="oportunidade")
    html = client.get(f"/p/{pid}/incerteza/riscos").get_data(as_text=True)
    assert "R-1" in html and "R-2" in html
    for u in ["", "/riscos", "/riscos/novo", f"/riscos/{r1}", f"/riscos/{r2}/editar", "/outras"]:
        assert client.get(f"/p/{pid}/incerteza{u}").status_code == 200, u
    outro = criar_projeto(client, "Outro")
    assert criar_risco(client, outro, titulo="C") > 0
    assert "R-1" in client.get(f"/p/{outro}/incerteza/riscos").get_data(as_text=True)
    assert client.get(f"/p/{outro}/incerteza/riscos/{r1}").status_code == 404


def test_estrategia_invalida_para_o_tipo_e_descartada(client):
    pid = criar_projeto(client)
    rid = criar_risco(client, pid, tipo="oportunidade", estrategia_oportunidade="mitigar", estrategia_ameaca="mitigar")
    assert "Estratégia</dt><dd>—" in client.get(f"/p/{pid}/incerteza/riscos/{rid}").get_data(as_text=True)
    rid = criar_risco(client, pid, tipo="oportunidade", estrategia_oportunidade="explorar", estrategia_ameaca="mitigar")
    assert "Estratégia</dt><dd>Explorar" in client.get(f"/p/{pid}/incerteza/riscos/{rid}").get_data(as_text=True)


def test_alertas_de_ameaca_acima_do_limite(client):
    pid = criar_projeto(client)
    rid = criar_risco(client, pid, titulo="Fornecedor atrasar", probabilidade="4", impacto="4")
    html = client.get(f"/p/{pid}").get_data(as_text=True)
    assert "R-1 (Fornecedor atrasar) está acima do limite de risco e não tem estratégia" in html
    assert "R-1 (Fornecedor atrasar) não tem responsável" in html
    client.post(f"/p/{pid}/incerteza/riscos/{rid}/editar", data={
        "titulo": "Fornecedor atrasar", "tipo": "ameaca", "status": "aberto", "probabilidade": "4", "impacto": "4",
        "estrategia_ameaca": "aceitar", "responsavel": "Denner"})
    html = client.get(f"/p/{pid}").get_data(as_text=True)
    assert "aceitação passiva" in html
    client.post(f"/p/{pid}/incerteza/riscos/{rid}/editar", data={
        "titulo": "Fornecedor atrasar", "tipo": "ameaca", "status": "aberto", "probabilidade": "4", "impacto": "4",
        "estrategia_ameaca": "aceitar", "plano_contingencia": "Trocar de fornecedor", "responsavel": "Denner"})
    html = client.get(f"/p/{pid}").get_data(as_text=True)
    assert "Fornecedor atrasar" not in html.split("Pontos de atenção")[1]
    # subir o limite tira o risco da faixa alta
    client.post(f"/p/{pid}/incerteza", data={"limite_risco": "20", "revisao_risco_dias": "14"})
    painel = client.get(f"/p/{pid}/incerteza").get_data(as_text=True)
    assert "Alto (≥ 20)" in painel


def test_revisao_registra_historico_e_cadencia(client, app):
    pid = criar_projeto(client)
    rid = criar_risco(client, pid, titulo="Rotatividade", probabilidade="4", impacto="3", responsavel="Ana")
    antiga = (date.today() - timedelta(days=30)).isoformat()
    with app.app_context():
        from db import get_db
        db = get_db()
        db.execute("UPDATE risco SET revisado_em = ?, identificado_em = ? WHERE id = ?", (antiga, antiga, rid))
        db.commit()
    assert "não é revisado há mais de 14 dias" in client.get(f"/p/{pid}").get_data(as_text=True)
    client.post(f"/p/{pid}/incerteza/riscos/{rid}/revisar", data={"probabilidade": "2", "impacto": "3", "status": "em_resposta",
                                                                  "nota": "Contratação concluída"})
    html = client.get(f"/p/{pid}/incerteza/riscos/{rid}").get_data(as_text=True)
    assert "Contratação concluída" in html and "Identificação" in html
    assert 'aria-label="Evolução da pontuação do risco"' in html
    assert "não é revisado" not in client.get(f"/p/{pid}").get_data(as_text=True)


def test_emv_e_reservas(client):
    pid = criar_projeto(client)
    criar_risco(client, pid, titulo="Multa LGPD", probabilidade="3", impacto="5", impacto_custo="10.000,00", reserva_custo="2000")
    criar_risco(client, pid, titulo="Desconto do fornecedor", tipo="oportunidade", probabilidade="5", impacto="2", impacto_custo="1000")
    client.post(f"/p/{pid}/incerteza", data={"limite_risco": "12", "revisao_risco_dias": "14", "reserva_gerenciamento": "5.000"})
    html = client.get(f"/p/{pid}/incerteza").get_data(as_text=True)
    metricas = html.split("Matrizes de probabilidade")[0]
    assert "EMV das ameaças</span>\n    <span class=\"metrica-valor pequeno\">-R$ 5.000,00" in metricas  # 50% de 10.000
    assert "Reserva de contingência</span>\n    <span class=\"metrica-valor pequeno\">R$ 2.000,00" in metricas
    assert "Reserva de gerenciamento</span>\n    <span class=\"metrica-valor pequeno\">R$ 5.000,00" in metricas
    assert "menor que o valor monetário esperado" in html


def test_risco_vinculado_a_parte_interessada(client):
    pid = criar_projeto(client)
    r = client.post(f"/p/{pid}/partes/nova", data={"nome": "Carlos", "interna": "1", "ativa": "1"})
    sid = int(r.headers["Location"].split("/")[-1])
    form = client.get(f"/p/{pid}/incerteza/riscos/novo?parte={sid}").get_data(as_text=True)
    assert f'<option value="{sid}" selected>Carlos</option>' in form
    criar_risco(client, pid, titulo="Carlos bloquear a integração", parte_id=str(sid))
    assert "Carlos bloquear a integração" in client.get(f"/p/{pid}/partes/{sid}").get_data(as_text=True)
    # parte de outro projeto não pode ser vinculada
    outro = criar_projeto(client, "Outro")
    rid = criar_risco(client, outro, titulo="X", parte_id=str(sid))
    assert "Carlos" not in client.get(f"/p/{outro}/incerteza/riscos/{rid}").get_data(as_text=True)


def test_incertezas_nao_risco(client):
    pid = criar_projeto(client)
    client.post(f"/p/{pid}/incerteza/outras", data={"natureza": "ambiguidade", "descricao": "Termo confirmado é ambíguo",
                                                     "respostas": ["definicoes", "iterar"]})
    html = client.get(f"/p/{pid}/incerteza/outras").get_data(as_text=True)
    assert "Termo confirmado é ambíguo" in html
    assert 'value="definicoes" checked' in html
    assert 'value="iterar" checked' not in html  # resposta de outra natureza é descartada
    client.post(f"/p/{pid}/incerteza/outras/1", data={"respostas": ["prototipos"], "status": "resolvida", "acoes": "Glossário"})
    html = client.get(f"/p/{pid}/dominios/incerteza").get_data(as_text=True)
    assert "0 incerteza(s)" in html
    client.post(f"/p/{pid}/incerteza/outras/1", data={"acao": "excluir"})
    assert "Termo confirmado" not in client.get(f"/p/{pid}/incerteza/outras").get_data(as_text=True)
