"""Testes da versão 14: PMO, estagiários e modelos do PMBOK."""
import io
from datetime import date, timedelta

import pytest

from ajuda import criar, html, novo_projeto
from app import create_app
from db import get_db


def dia(n):
    return (date.today() + timedelta(days=n)).isoformat()


def contar(c, sql, *a):
    with c.application.app_context():
        return get_db().execute(sql, a).fetchone()[0]


@pytest.fixture()
def pmo_app(tmp_path):
    """App com login: administrador (PMO) e uma estagiária."""
    app = create_app({"TESTING": True, "LOGIN_OBRIGATORIO": True, "DATABASE": str(tmp_path / "pmo.db"), "SECRET_KEY": "x"})
    adm = app.test_client()
    adm.post("/primeiro-acesso", data={"nome": "Denner Ramiro", "login": "denner", "senha": "senha12345", "confirmacao": "senha12345"})
    adm.post("/usuarios", data={"acao": "criar", "nome": "Ana Souza", "login": "ana", "senha": "estagio123"})
    ana = app.test_client()
    ana.post("/entrar", data={"login": "ana", "senha": "estagio123"})
    return app, adm, ana


def test_modelo_de_projeto_preenche_o_inicio(client):
    r = client.post("/projetos/novo", data={"nome": "Portal", "modelo": "agil"})
    pid = int(r.headers["Location"].split("/p/")[1].split("/")[0])
    with client.application.app_context():
        p = get_db().execute("SELECT * FROM projeto WHERE id = ?", (pid,)).fetchone()
        assert p["abordagem"] == "adaptativa" and p["unidade_estimativa"] == "pontos" and p["definicao_pronto"]
    assert contar(client, "SELECT COUNT(*) FROM fase WHERE projeto_id = ?", pid) >= 3
    assert contar(client, "SELECT COUNT(*) FROM risco WHERE projeto_id = ?", pid) == 3


def test_acesso_por_projeto(pmo_app):
    app, adm, ana = pmo_app
    do_pmo = novo_projeto(adm, nome="Projeto sigiloso")
    da_ana = novo_projeto(ana, nome="Projeto da Ana")          # quem cria ganha acesso
    assert ana.get(f"/p/{do_pmo}").status_code == 404           # não vê o que não é dela
    assert ana.get(f"/p/{da_ana}").status_code == 200
    assert "Projeto sigiloso" not in html(ana, "/") and "Projeto sigiloso" not in html(ana, "/portfolio")
    assert adm.get(f"/p/{da_ana}").status_code == 200           # PMO vê tudo
    with app.app_context():
        ana_id = get_db().execute("SELECT id FROM usuario WHERE login = 'ana'").fetchone()[0]
    adm.post(f"/p/{do_pmo}/editar", data={"nome": "Projeto sigiloso", "acesso_enviado": "1", "acesso": str(ana_id)})
    assert ana.get(f"/p/{do_pmo}").status_code == 200


def test_minhas_pendencias_e_revisao_do_pmo(pmo_app):
    app, adm, ana = pmo_app
    pid = novo_projeto(ana, "adaptativa")
    criar(ana, f"/p/{pid}/trabalho/questoes/nova", titulo="Servidor fora do ar", responsavel="Ana (estagiária)", prazo=dia(-1), status="aberta", prioridade="alta")
    pag = html(ana, "/minhas-pendencias")
    assert "Servidor fora do ar" in pag and "atrasado" in pag
    rid = criar(ana, f"/p/{pid}/incerteza/riscos/novo", titulo="API mudar de preço", tipo="ameaca", status="aberto")
    ana.post(f"/p/{pid}/revisao", data={"tabela": "risco", "registro_id": rid, "titulo": "R-1 API", "link": f"/p/{pid}/incerteza/riscos/{rid}"})
    assert ana.get("/revisoes").status_code == 403
    assert "R-1 API" in html(adm, "/revisoes")
    with app.app_context():
        rev = get_db().execute("SELECT id FROM revisao_pmo").fetchone()[0]
    r = adm.post("/revisoes", data={"revisao_id": rev, "decisao": "devolvida"}, follow_redirects=True)
    assert "explique o que precisa ser ajustado" in r.get_data(as_text=True)
    adm.post("/revisoes", data={"revisao_id": rev, "decisao": "devolvida", "comentario": "Detalhe o gatilho."})
    assert "Detalhe o gatilho." in html(ana, "/minhas-pendencias")
    assert "Detalhe o gatilho." in html(ana, f"/p/{pid}/incerteza/riscos/{rid}")


def test_nivel_rigoroso(client):
    pid = novo_projeto(client, "adaptativa")
    client.post("/admin/exigencia", data={"nivel": "rigoroso"})
    r = client.post(f"/p/{pid}/trabalho/questoes/nova", data={"titulo": "Sem dono", "status": "aberta"})
    assert "responsável" in r.get_data(as_text=True) and contar(client, "SELECT COUNT(*) FROM questao") == 0
    r = client.post(f"/p/{pid}/incerteza/riscos/novo", data={"titulo": "Alto sem dono", "tipo": "ameaca", "status": "aberto", "probabilidade": "4", "impacto": "4"})
    assert contar(client, "SELECT COUNT(*) FROM risco") == 0
    client.post(f"/p/{pid}/incerteza/riscos/novo", data={"titulo": "Baixo", "tipo": "ameaca", "status": "aberto", "probabilidade": "1", "impacto": "2"})
    assert contar(client, "SELECT COUNT(*) FROM risco") == 1
    r = client.post(f"/p/{pid}/entrega/itens/novo", data={"titulo": "Sem critério", "tipo": "historia", "status": "em_andamento"})
    assert "critérios de aceite" in r.get_data(as_text=True)
    client.post("/admin/exigencia", data={"nivel": "essencial"})
    assert client.post(f"/p/{pid}/trabalho/questoes/nova", data={"titulo": "Sem dono", "status": "aberta"}).status_code == 302


def test_completude_no_risco(client):
    pid = novo_projeto(client)
    rid = criar(client, f"/p/{pid}/incerteza/riscos/novo", titulo="Pouco preenchido", tipo="ameaca", status="aberto")
    pag = html(client, f"/p/{pid}/incerteza/riscos/{rid}")
    assert "% preenchido" in pag and "Falta:" in pag


def test_busca_respeita_acesso(pmo_app):
    app, adm, ana = pmo_app
    pid = novo_projeto(adm, nome="Do PMO")
    criar(adm, f"/p/{pid}/incerteza/riscos/novo", titulo="Integração WhatsApp", tipo="ameaca", status="aberto")
    assert "Integração WhatsApp" in html(adm, "/busca?q=whats")
    assert "Integração WhatsApp" not in html(ana, "/busca?q=whats")


def test_agenda_e_ics(client):
    pid = novo_projeto(client, "adaptativa")
    criar(client, f"/p/{pid}/trabalho/questoes/nova", titulo="Prazo vencido", prazo=dia(-2), status="aberta")
    pag = html(client, f"/p/{pid}/agenda")
    assert "Atrasados" in pag and "Prazo vencido" in pag
    r = client.get(f"/p/{pid}/agenda.ics")
    assert r.mimetype == "text/calendar" and b"BEGIN:VEVENT" in r.data


def test_exportar_excel_sem_injecao_de_formula(client):
    from openpyxl import load_workbook
    pid = novo_projeto(client)
    criar(client, f"/p/{pid}/incerteza/riscos/novo", titulo="=HYPERLINK(\"http://mal\")", tipo="ameaca", status="aberto")
    r = client.get(f"/p/{pid}/exportar/riscos")
    assert r.status_code == 200 and r.headers["Content-Disposition"].endswith(".xlsx")
    ws = load_workbook(io.BytesIO(r.data)).active
    assert ws["B1"].value == "Risco" and ws["B2"].value.startswith("'=")
    assert client.get(f"/p/{pid}/exportar/inexistente").status_code == 404


def test_moscow_dependencias_e_gantt(client):
    pid = novo_projeto(client, "preditiva")
    a = criar(client, f"/p/{pid}/entrega/itens/novo", titulo="Banco de dados", tipo="entregavel", status="a_fazer", moscow="must")
    b = criar(client, f"/p/{pid}/entrega/itens/novo", titulo="Telas", tipo="entregavel", status="a_fazer",
              dependencias_enviadas="1", depende_de=str(a))
    assert contar(client, "SELECT moscow FROM item WHERE id = ?", a) == "must"
    assert contar(client, "SELECT depende_de FROM item_dependencia WHERE item_id = ?", b) == a
    # ciclo: A não pode depender de B
    client.post(f"/p/{pid}/entrega/itens/{a}", data={"titulo": "Banco de dados", "tipo": "entregavel", "status": "a_fazer",
                                                      "dependencias_enviadas": "1", "depende_de": str(b)})
    assert contar(client, "SELECT COUNT(*) FROM item_dependencia WHERE item_id = ?", a) == 0
    client.post(f"/p/{pid}/medicao/cronograma", data={"acao": "itens", f"inicio_{a}": dia(0), f"fim_{a}": dia(10),
                                                      f"inicio_{b}": dia(5), f"fim_{b}": dia(15)})
    pag = html(client, f"/p/{pid}/gantt")
    assert "gantt-barra" in pag and "depende de I-1" in pag and "Dependências em conflito" in pag


def test_burndown(client):
    pid = novo_projeto(client, "adaptativa")
    client.post(f"/p/{pid}/medicao/cronograma", data={"acao": "iteracao", "nome": "Sprint 1", "inicio": dia(-3), "fim": dia(10)})
    it = contar(client, "SELECT id FROM iteracao")
    i1 = criar(client, f"/p/{pid}/entrega/itens/novo", titulo="A", tipo="historia", status="a_fazer", estimativa="5")
    client.post(f"/p/{pid}/medicao/cronograma", data={"acao": "itens", f"iteracao_{i1}": str(it), f"inicio_{i1}": "", f"fim_{i1}": ""})
    pag = html(client, f"/p/{pid}/burndown")
    assert "Restante" in pag and "<svg" in pag


def test_complexidade_cynefin_stacey(client):
    pid = novo_projeto(client, "preditiva")
    client.post(f"/p/{pid}/complexidade", data={"cynefin": "complexo", "stacey_requisitos": "4", "stacey_tecnologia": "4"})
    pag = html(client, f"/p/{pid}/abordagem")
    assert "Complexo" in pag and "Adaptativa" in pag and "você escolheu preditiva" in pag


def test_premortem_cria_riscos(client):
    pid = novo_projeto(client)
    client.post(f"/p/{pid}/premortem", data={"motivos": "- TI não liberou acesso\n• Usuários não adotaram\n\n"})
    assert contar(client, "SELECT COUNT(*) FROM risco WHERE fonte = 'Pré-mortem'") == 2


def test_link_para_exemplo_preenchido(client):
    client.post("/exemplo")
    pid = novo_projeto(client)
    assert "Ver exemplo preenchido" in html(client, f"/p/{pid}/abertura")


def test_membro_ligado_ao_usuario_entra_nas_pendencias(pmo_app):
    app, adm, ana = pmo_app
    pid = novo_projeto(ana, "adaptativa")
    with app.app_context():
        ana_id = get_db().execute("SELECT id FROM usuario WHERE login = 'ana'").fetchone()[0]
    ana.post(f"/p/{pid}/equipe", data={"nome": "Aninha", "papel": "Dev", "usuario_id": str(ana_id)})
    assert contar(ana, "SELECT usuario_id FROM membro") == ana_id
    criar(ana, f"/p/{pid}/trabalho/questoes/nova", titulo="Com apelido", responsavel="Aninha", status="aberta")
    assert "Com apelido" in html(ana, "/minhas-pendencias")


def test_exemplo_funciona_com_login_e_csrf_ligados(tmp_path):
    import re as _re
    app = create_app({"TESTING": True, "LOGIN_OBRIGATORIO": True, "CSRF_ATIVO": True, "DATABASE": str(tmp_path / "e.db"), "SECRET_KEY": "x"})
    c = app.test_client()
    tok = lambda url: _re.search(r'name="_csrf" value="([^"]+)"', c.get(url).get_data(as_text=True)).group(1)  # noqa: E731
    c.post("/primeiro-acesso", data={"nome": "Ana", "login": "ana", "senha": "senha12345", "confirmacao": "senha12345", "_csrf": tok("/primeiro-acesso")})
    r = c.post("/exemplo", data={"_csrf": tok("/")})
    assert r.status_code == 302 and "/fluxo" in r.headers["Location"]
    assert contar(c, "SELECT COUNT(*) FROM projeto WHERE nome LIKE '%AgendaFácil%'") == 1
    # a marca interna não pode ser forjada por cabeçalho HTTP
    externo = app.test_client()
    assert externo.post("/projetos/novo", data={"nome": "x"}, headers={"gestor.interno": "1"}).status_code in (302, 400)
    assert contar(c, "SELECT COUNT(*) FROM projeto WHERE nome = 'x'") == 0


def test_exemplo_antigo_e_renomeado(tmp_path):
    import sqlite3
    from ajuda import banco_na_versao
    cam = tmp_path / "antigo.db"
    banco_na_versao(cam, 11)
    con = sqlite3.connect(cam); con.execute("INSERT INTO projeto (nome) VALUES ('AgendaFácil — app de agendamento')"); con.commit(); con.close()
    create_app({"TESTING": True, "DATABASE": str(cam), "SECRET_KEY": "x"})
    nomes = [r[0] for r in sqlite3.connect(cam).execute("SELECT nome FROM projeto")]
    assert "Exemplo: AgendaFácil" in nomes and "AgendaFácil — app de agendamento" not in nomes
