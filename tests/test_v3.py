"""Testes da versão 3: domínio Trabalho do Projeto e integrações."""
import os
import sqlite3
import sys
from datetime import date, timedelta

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pmbok  # noqa: E402
from app import create_app  # noqa: E402
from db import VERSAO_ATUAL  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def criar_banco_na_versao(caminho, versao):
    """Cria um banco como uma versão antiga do app o deixaria (migrações até `versao`)."""
    from db import MIGRACOES, _comandos
    conn = sqlite3.connect(caminho, isolation_level=None)
    with open(os.path.join(RAIZ, "schema.sql"), encoding="utf-8") as f:
        conn.executescript(f.read())
    for v in sorted(MIGRACOES):
        if v <= versao:
            for comando in _comandos(MIGRACOES[v]):
                conn.execute(comando)
    conn.execute(f"PRAGMA user_version = {versao}")
    conn.execute("INSERT INTO projeto (nome) VALUES ('Antigo')")
    conn.close()
IMPACTOS_OK = {c: "sem impacto" for c, *_ in pmbok.IMPACTOS_MUDANCA}


@pytest.fixture()
def app(tmp_path):
    return create_app({"TESTING": True, "DATABASE": str(tmp_path / "t.db"), "SECRET_KEY": "t"})


@pytest.fixture()
def client(app):
    with app.test_client() as c:
        yield c


def projeto(client, abordagem=None):
    r = client.post("/projetos/novo", data={"nome": "P"})
    pid = int(r.headers["Location"].split("/p/")[1].split("/")[0])
    if abordagem:
        client.post(f"/p/{pid}/abordagem", data={"acao": "salvar", "abordagem": abordagem})
    return pid


def nova_questao(client, pid, **campos):
    dados = {"titulo": "Questão", "prioridade": "media", "status": "aberta"}
    dados.update(campos)
    r = client.post(f"/p/{pid}/trabalho/questoes/nova", data=dados)
    assert r.status_code == 302
    return int(r.headers["Location"].split("/")[-1])


def nova_mudanca(client, pid, **campos):
    dados = {"titulo": "Mudança", "status": "solicitada"}
    dados.update(campos)
    return client.post(f"/p/{pid}/trabalho/mudancas/nova", data=dados, follow_redirects=True)


# ---------------- Migração ----------------
def test_migracao_da_v1_e_da_v2_ate_a_versao_atual(tmp_path):
    v1 = tmp_path / "v1.db"
    conn = sqlite3.connect(v1)
    with open(os.path.join(RAIZ, "schema.sql"), encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.execute("INSERT INTO projeto (nome) VALUES ('Antigo')")
    conn.commit()
    conn.close()
    app = create_app({"TESTING": True, "DATABASE": str(v1), "SECRET_KEY": "x"})
    assert sqlite3.connect(v1).execute("PRAGMA user_version").fetchone()[0] == VERSAO_ATUAL >= 3
    c = app.test_client()
    for u in ["/p/1", "/p/1/trabalho", "/p/1/trabalho/questoes", "/p/1/trabalho/mudancas", "/p/1/trabalho/licoes"]:
        assert c.get(u).status_code == 200, u

    # banco que parou na v2 (user_version = 2) com um risco
    v2 = tmp_path / "v2.db"
    criar_banco_na_versao(v2, 2)
    conn = sqlite3.connect(v2)
    conn.execute("INSERT INTO risco (projeto_id, codigo, titulo, status) VALUES (1, 1, 'Legado', 'ocorreu')")
    conn.commit()
    conn.close()
    app = create_app({"TESTING": True, "DATABASE": str(v2), "SECRET_KEY": "x"})
    assert sqlite3.connect(v2).execute("PRAGMA user_version").fetchone()[0] == VERSAO_ATUAL
    html = app.test_client().get("/p/1").get_data(as_text=True)
    assert "R-1 (Legado) ocorreu e não tem questão aberta" in html


# ---------------- Questões ----------------
def test_questao_ciclo_e_alertas(client):
    pid = projeto(client)
    ontem = (date.today() - timedelta(days=1)).isoformat()
    qid = nova_questao(client, pid, titulo="Servidor fora do ar", prioridade="alta", prazo=ontem)
    visao = client.get(f"/p/{pid}").get_data(as_text=True)
    assert "Q-1 (Servidor fora do ar) passou do prazo" in visao
    assert "Q-1 (Servidor fora do ar) não tem responsável" in visao

    # resolver exige descrição da resolução
    base = {"titulo": "Servidor fora do ar", "prioridade": "alta", "prazo": ontem, "responsavel": "Ana"}
    html = client.post(f"/p/{pid}/trabalho/questoes/{qid}", data={**base, "status": "resolvida"},
                       follow_redirects=True).get_data(as_text=True)
    assert "descreva a resolução" in html
    html = client.post(f"/p/{pid}/trabalho/questoes/{qid}", data={**base, "status": "resolvida", "resolucao": "Reiniciado"},
                       follow_redirects=True).get_data(as_text=True)
    assert "Há uma lição a registrar?" in html
    assert "Registrar lição aprendida" in html
    assert "passou do prazo" not in client.get(f"/p/{pid}").get_data(as_text=True)
    assert "Tempo médio de resolução: 0.0 dias" in client.get(f"/p/{pid}/dominios/trabalho").get_data(as_text=True)
    # reabrir limpa a data de resolução
    client.post(f"/p/{pid}/trabalho/questoes/{qid}", data={**base, "status": "em_andamento"})
    assert "resolvida em" not in client.get(f"/p/{pid}/trabalho/questoes/{qid}").get_data(as_text=True)


def test_risco_que_ocorre_abre_questao_uma_unica_vez(client):
    pid = projeto(client)
    r = client.post(f"/p/{pid}/incerteza/riscos/novo", data={"titulo": "API mudar preço", "tipo": "ameaca", "status": "aberto",
                                                              "plano_contingencia": "Usar SMS", "responsavel": "Denner"})
    rid = int(r.headers["Location"].split("/")[-1])
    html = client.post(f"/p/{pid}/incerteza/riscos/{rid}/revisar", data={"status": "ocorreu", "nota": "Aumento anunciado"},
                       follow_redirects=True).get_data(as_text=True)
    assert "foi aberta a questão Q-1" in html
    assert "Tratamento após ocorrer" in html
    lista = client.get(f"/p/{pid}/trabalho/questoes").get_data(as_text=True)
    assert "API mudar preço" in lista and "R-1" in lista
    q = client.get(f"/p/{pid}/trabalho/questoes/1").get_data(as_text=True)
    assert "Plano de contingência: Usar SMS" in q and 'value="Denner"' in q
    # nova revisão como "ocorreu" não duplica
    client.post(f"/p/{pid}/incerteza/riscos/{rid}/revisar", data={"status": "ocorreu"})
    assert client.get(f"/p/{pid}/trabalho/questoes/2").status_code == 404


def test_consumo_de_reservas(client):
    pid = projeto(client)
    client.post(f"/p/{pid}/incerteza", data={"limite_risco": "12", "revisao_risco_dias": "14", "reserva_gerenciamento": "1.000"})
    r = client.post(f"/p/{pid}/incerteza/riscos/novo", data={"titulo": "R", "tipo": "ameaca", "status": "ocorreu",
                                                              "reserva_custo": "2.000", "responsavel": "A"})
    assert r.status_code == 302
    client.post(f"/p/{pid}/trabalho/questoes/1", data={"titulo": "R", "prioridade": "alta", "status": "em_andamento",
                                                        "risco_id": "1", "reserva_usada_custo": "2.500"})
    nova_questao(client, pid, titulo="Imprevisto", reserva_usada_custo="300", responsavel="B")
    painel = client.get(f"/p/{pid}/incerteza").get_data(as_text=True)
    assert "usada: R$ 2.500,00" in painel and "usada: R$ 300,00" in painel
    assert "Reserva de contingência usada (R$ 2.500,00) excede a reservada (R$ 2.000,00)" in client.get(f"/p/{pid}").get_data(as_text=True)


def test_questao_nao_aceita_risco_ou_parte_de_outro_projeto(client):
    a = projeto(client)
    b = projeto(client)
    client.post(f"/p/{a}/incerteza/riscos/novo", data={"titulo": "Risco do A", "tipo": "ameaca", "status": "aberto"})
    qid = nova_questao(client, b, titulo="Q do B", risco_id="1")
    html = client.get(f"/p/{b}/trabalho/questoes/{qid}").get_data(as_text=True)
    assert "veio do risco" not in html and "Risco do A" not in html


# ---------------- Mudanças ----------------
def test_decisao_exige_avaliacao_holistica_no_preditivo(client):
    pid = projeto(client, "preditiva")
    html = nova_mudanca(client, pid, titulo="Pagamento online", status="aprovada", decidido_por="Dra. Lúcia").get_data(as_text=True)
    assert "avalie todos os impactos" in html and "Faltando: Escopo, Cronograma" in html
    html = nova_mudanca(client, pid, titulo="Pagamento online", status="aprovada", **IMPACTOS_OK).get_data(as_text=True)
    assert "Informe quem decidiu" in html
    html = nova_mudanca(client, pid, titulo="Pagamento online", status="aprovada", decidido_por="Dra. Lúcia", **IMPACTOS_OK).get_data(as_text=True)
    assert "M-1 registrada" in html
    assert "foi aprovada e ainda não foi comunicada" in client.get(f"/p/{pid}").get_data(as_text=True)


def test_adaptativo_nao_exige_avaliacao_completa(client):
    pid = projeto(client, "adaptativa")
    html = nova_mudanca(client, pid, titulo="Nova tela", status="aprovada", decidido_por="PO").get_data(as_text=True)
    assert "M-1 registrada" in html
    assert "trabalho novo normalmente entra no backlog" in client.get(f"/p/{pid}/trabalho/mudancas").get_data(as_text=True)


def test_so_mudanca_aprovada_pode_ser_implementada(client):
    pid = projeto(client, "preditiva")
    nova_mudanca(client, pid, titulo="X")
    html = client.post(f"/p/{pid}/trabalho/mudancas/1", data={"titulo": "X", "status": "implementada", "decidido_por": "S"},
                       follow_redirects=True).get_data(as_text=True)
    assert "Só mudanças aprovadas podem ser implementadas" in html
    client.post(f"/p/{pid}/trabalho/mudancas/1", data={"titulo": "X", "status": "aprovada", "decidido_por": "S", **IMPACTOS_OK})
    html = client.post(f"/p/{pid}/trabalho/mudancas/1", data={"titulo": "X", "status": "implementada", "decidido_por": "S",
                                                               "comunicada": "1", **IMPACTOS_OK}, follow_redirects=True).get_data(as_text=True)
    assert "M-1 atualizada" in html
    dom = client.get(f"/p/{pid}/dominios/trabalho").get_data(as_text=True)
    assert "1 de 1 mudanças decididas com avaliação holística completa" in dom


def test_mudanca_pendente_ha_muito_tempo_e_mudancas_por_parte(client, app):
    pid = projeto(client)
    r = client.post(f"/p/{pid}/partes/nova", data={"nome": "Carlos", "interna": "1", "ativa": "1"})
    sid = r.headers["Location"].split("/")[-1]
    nova_mudanca(client, pid, titulo="Trocar banco de dados", parte_id=sid)
    nova_mudanca(client, pid, titulo="Trocar framework", parte_id=sid)
    with app.app_context():
        from db import get_db
        db = get_db()
        db.execute("UPDATE mudanca SET criado_em = ? WHERE codigo = 1", ((date.today() - timedelta(days=10)).isoformat(),))
        db.commit()
    assert "M-1 (Trocar banco de dados) aguarda decisão há mais de 7 dias" in client.get(f"/p/{pid}").get_data(as_text=True)
    assert "Carlos (2)" in client.get(f"/p/{pid}/dominios/partes-interessadas").get_data(as_text=True)


def test_termo_aprovado_aponta_para_registro_de_mudancas(client):
    pid = projeto(client)
    base = {"status": "aprovado", "proposito": "p", "objetivos": "o", "criterios_sucesso": "c", "patrocinador": "s", "gerente": "g", "aprovado_por": "s"}
    client.post(f"/p/{pid}/abertura", data=base)
    html = client.get(f"/p/{pid}/abertura").get_data(as_text=True)
    assert "Alterações devem passar pelo" in html
    form = client.get(f"/p/{pid}/trabalho/mudancas/nova?titulo=Alteração no termo de abertura").get_data(as_text=True)
    assert 'value="Alteração no termo de abertura"' in form


# ---------------- Lições ----------------
def test_licao_a_partir_de_questao(client):
    pid = projeto(client)
    qid = nova_questao(client, pid, titulo="Deploy quebrou", status="resolvida", resolucao="Faltava variável de ambiente")
    form = client.get(f"/p/{pid}/trabalho/licoes?questao={qid}").get_data(as_text=True)
    assert "Faltava variável de ambiente" in form
    amanha = (date.today() + timedelta(days=1)).isoformat()
    r = client.post(f"/p/{pid}/trabalho/licoes", data={"descricao": "Checklist de deploy", "tipo": "melhorar", "questao_id": str(qid),
                                                       "voltar": "questao", "conhecimento": "tacito", "alcance": "organizacao",
                                                       "data": amanha, "dominio": "trabalho", "origem": "questao"})
    assert r.headers["Location"].endswith(f"/trabalho/questoes/{qid}")
    assert "Checklist de deploy" in client.get(f"/p/{pid}/trabalho/questoes/{qid}").get_data(as_text=True)
    lista = client.get(f"/p/{pid}/trabalho/licoes").get_data(as_text=True)
    assert "Tácito" in lista and "Toda a organização" in lista and "Q-1" in lista
    assert date.today().strftime("%d/%m/%Y") in lista  # data futura é limitada a hoje
    assert "Checklist de deploy" not in client.get(f"/p/{pid}/trabalho/licoes?tipo=manter").get_data(as_text=True).split("Registro (")[1]
    client.post(f"/p/{pid}/trabalho/licoes", data={"acao": "excluir", "licao_id": "1"})
    assert "Checklist de deploy" not in client.get(f"/p/{pid}/trabalho/licoes").get_data(as_text=True)


def test_paginas_do_modulo_e_isolamento(client):
    a = projeto(client)
    b = projeto(client)
    qid = nova_questao(client, a)
    nova_mudanca(client, a)
    for u in ["", "/questoes", "/questoes/nova", f"/questoes/{qid}", "/mudancas", "/mudancas/nova", "/mudancas/1", "/licoes",
              "/questoes?status=todas", "/questoes?status=resolvida"]:
        assert client.get(f"/p/{a}/trabalho{u}").status_code == 200, u
    assert client.get(f"/p/{b}/trabalho/questoes/{qid}").status_code == 404
    assert client.get(f"/p/{b}/trabalho/mudancas/1").status_code == 404
    assert client.post(f"/p/{b}/trabalho/questoes/{qid}", data={"acao": "excluir"}).status_code == 404
    assert client.get(f"/p/{a}/trabalho/questoes/{qid}").status_code == 200
