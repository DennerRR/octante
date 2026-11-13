import os
import sys
from datetime import date, timedelta

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pmbok  # noqa: E402
from app import create_app  # noqa: E402


@pytest.fixture()
def client(tmp_path):
    app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "teste.db")})
    with app.test_client() as c:
        yield c


def criar_projeto(client, nome="App Clínica"):
    r = client.post("/projetos/novo", data={"nome": nome, "descricao": "Agendamento online"})
    assert r.status_code == 302
    return int(r.headers["Location"].split("/p/")[1].split("/")[0])


def criar_parte(client, pid, **campos):
    dados = {"nome": "Ana", "interna": "1", "ativa": "1", "atitude": "desconhecida"}
    dados.update(campos)
    r = client.post(f"/p/{pid}/partes/nova", data=dados)
    assert r.status_code == 302
    return int(r.headers["Location"].rstrip("/").split("/")[-1])


# ---------------- Regras de domínio (pmbok.py) ----------------
def test_quadrantes():
    assert pmbok.quadrante_poder_interesse(5, 5) == "Gerenciar de perto"
    assert pmbok.quadrante_poder_interesse(4, 2) == "Manter satisfeita"
    assert pmbok.quadrante_poder_interesse(2, 4) == "Manter informada"
    assert pmbok.quadrante_poder_interesse(3, 3) == "Monitorar"
    assert pmbok.quadrante_poder_interesse(None, 3) is None


def test_saliencia():
    assert pmbok.classificar_salience(1, 1, 1) == ("Definitiva", "definitiva")
    assert pmbok.classificar_salience(1, 0, 1) == ("Perigosa", "expectante")
    assert pmbok.classificar_salience(0, 1, 0) == ("Discricionária", "latente")
    assert pmbok.classificar_salience(0, 0, 0)[0] == "Sem saliência"


def test_recomendacao_abordagem():
    todos = {k: 1 for k, *_ in pmbok.FATORES_ABORDAGEM}
    assert pmbok.recomendar_abordagem(todos)[1] == "preditiva"
    assert pmbok.recomendar_abordagem({k: 5 for k in todos})[1] == "adaptativa"
    assert pmbok.recomendar_abordagem({k: 3 for k in todos})[1] == "hibrida"
    assert pmbok.recomendar_abordagem({}) == (None, None, {})


def test_conteudo_dominios_completo():
    assert len(pmbok.DOMINIOS) == 8
    assert len(pmbok.PRINCIPIOS) == 12
    esperados = {"partes-interessadas": 3, "equipe": 3, "abordagem": 3, "planejamento": 6,
                 "trabalho": 7, "entrega": 5, "medicao": 4, "incerteza": 7}
    assert {d["chave"]: len(d["resultados"]) for d in pmbok.DOMINIOS} == esperados


# ---------------- Fluxo pela aplicação ----------------
def test_todas_as_paginas_abrem(client):
    pid = criar_projeto(client)
    sid = criar_parte(client, pid, poder="5", interesse="5")
    urls = ["/", "/principios", f"/p/{pid}", f"/p/{pid}/editar", f"/p/{pid}/abordagem", f"/p/{pid}/abertura",
            f"/p/{pid}/partes", f"/p/{pid}/partes/nova", f"/p/{pid}/partes/{sid}", f"/p/{pid}/partes/{sid}/editar",
            f"/p/{pid}/partes/analise", f"/p/{pid}/partes/priorizacao", f"/p/{pid}/partes/engajamento",
            f"/p/{pid}/partes/monitoramento", f"/p/{pid}/dominios"]
    urls += [f"/p/{pid}/dominios/{d['chave']}" for d in pmbok.DOMINIOS]
    for u in urls:
        assert client.get(u).status_code == 200, u
    assert client.get("/p/999").status_code == 404
    assert client.get(f"/p/{pid}/dominios/inexistente").status_code == 404


def test_nome_obrigatorio(client):
    r = client.post("/projetos/novo", data={"nome": "  "})
    assert r.status_code == 200
    assert "Informe o nome do projeto" in r.get_data(as_text=True)


def test_abordagem_salva_e_sugere(client):
    pid = criar_projeto(client)
    dados = {k: "5" for k, *_ in pmbok.FATORES_ABORDAGEM}
    dados.update(acao="calcular", cadencia="periodica")
    client.post(f"/p/{pid}/abordagem", data=dados)
    html = client.get(f"/p/{pid}/abordagem").get_data(as_text=True)
    assert "Sugestão: <strong>Adaptativa</strong>" in html
    dados.update(acao="salvar", abordagem="adaptativa", justificativa="Requisitos voláteis")
    r = client.post(f"/p/{pid}/abordagem", data=dados)
    assert r.headers["Location"].endswith(f"/p/{pid}")
    assert "Adaptativa" in client.get(f"/p/{pid}").get_data(as_text=True)


def test_aprovacao_exige_campos_essenciais(client):
    pid = criar_projeto(client)
    r = client.post(f"/p/{pid}/abertura", data={"status": "aprovado", "proposito": "x"}, follow_redirects=True)
    html = r.get_data(as_text=True)
    assert "Para aprovar" in html
    assert 'selo-status-aprovado' not in html
    completo = {"status": "aprovado", "proposito": "p", "objetivos": "o", "criterios_sucesso": "c",
                "patrocinador": "Dra. Lúcia", "gerente": "Denner", "aprovado_por": "Dra. Lúcia"}
    html = client.post(f"/p/{pid}/abertura", data=completo, follow_redirects=True).get_data(as_text=True)
    assert "selo-status-aprovado" in html
    assert date.today().isoformat() in html  # data de aprovação preenchida automaticamente


def test_montar_visao(client):
    pid = criar_projeto(client)
    dados = {"status": "rascunho", "visao_publico": "pacientes", "visao_necessidade": "querem marcar consultas",
             "visao_produto": "AgendaFácil", "visao_categoria": "app web", "visao_beneficio": "agenda em 2 minutos",
             "gerar_visao": "1"}
    html = client.post(f"/p/{pid}/abertura", data=dados, follow_redirects=True).get_data(as_text=True)
    assert "Para pacientes que querem marcar consultas, o AgendaFácil é um(a) app web que agenda em 2 minutos." in html


def test_ciclo_completo_partes_interessadas(client):
    pid = criar_projeto(client)
    a = criar_parte(client, pid, nome="Dra. Lúcia Prado", papel="Diretora")
    b = criar_parte(client, pid, nome="Recepção")

    # 2. Analisar
    client.post(f"/p/{pid}/partes/analise", data={
        f"poder_{a}": "5", f"interesse_{a}": "5", f"influencia_{a}": "4", f"impacto_{a}": "4",
        f"atitude_{a}": "opositor", f"sal_poder_{a}": "1", f"sal_legitimidade_{a}": "1", f"sal_urgencia_{a}": "1",
        f"poder_{b}": "2", f"interesse_{b}": "4", f"atitude_{b}": "apoiador",
    })
    html = client.get(f"/p/{pid}/partes/analise").get_data(as_text=True)
    assert "Definitiva" in html

    # 3. Priorizar (ordem sugerida coloca quem deve ser gerenciado de perto em primeiro)
    client.post(f"/p/{pid}/partes/priorizacao", data={"acao": "sugerida"})
    html = client.get(f"/p/{pid}/partes/priorizacao").get_data(as_text=True)
    assert html.index("Dra. Lúcia Prado") < html.index("Recepção")
    assert f'name="ordem_{a}" value="1"' in html

    # ordem manual inverte
    client.post(f"/p/{pid}/partes/priorizacao", data={"acao": "manual", f"ordem_{a}": "2", f"ordem_{b}": "1"})
    html = client.get(f"/p/{pid}/partes/priorizacao").get_data(as_text=True)
    assert f'name="ordem_{b}" value="1"' in html

    # 4. Engajar
    client.post(f"/p/{pid}/partes/engajamento", data={
        f"atual_{a}": "2", f"desejado_{a}": "4", f"metodo_{a}": "interativa", f"frequencia_{a}": "Semanal",
        f"atual_{b}": "4", f"desejado_{b}": "4", f"metodo_{b}": "push",
    })
    visao = client.get(f"/p/{pid}").get_data(as_text=True)
    assert "alto poder e se opõe" in visao
    assert "Lacuna de engajamento de Dra. Lúcia Prado" in visao
    assert "não há interação nos últimos" in visao

    # 5. Monitorar
    client.post(f"/p/{pid}/partes/monitoramento", data={
        "parte_id": str(a), "data": date.today().isoformat(), "metodo": "interativa",
        "resumo": "Demo do protótipo", "satisfacao": "2"})
    client.post(f"/p/{pid}/partes/engajamento", data={
        f"atual_{a}": "3", f"desejado_{a}": "4", f"metodo_{a}": "interativa",
        f"atual_{b}": "4", f"desejado_{b}": "4", f"metodo_{b}": "push"})
    mon = client.get(f"/p/{pid}/partes/monitoramento").get_data(as_text=True)
    assert "Demo do protótipo" in mon
    assert "satisfação registrada de Dra. Lúcia Prado foi baixa" in mon
    assert "avançou" in mon  # Resistente -> Neutro
    assert "não há interação nos últimos" not in mon

    # contadores do fluxo: todas analisadas, priorizadas e com plano
    assert mon.count('class="fluxo-cont">2/2</span>') == 4
    assert 'class="fluxo-cont">1/2</span>' in mon  # só uma monitorada


def test_interacao_antiga_nao_conta_como_monitorada(client):
    pid = criar_projeto(client)
    a = criar_parte(client, pid, nome="Patrocinador", poder="5", interesse="5", atitude="apoiador")
    antiga = (date.today() - timedelta(days=45)).isoformat()
    client.post(f"/p/{pid}/partes/monitoramento", data={"parte_id": str(a), "data": antiga, "resumo": "Kickoff"})
    html = client.get(f"/p/{pid}").get_data(as_text=True)
    assert "não há interação nos últimos 30 dias" in html


def test_verificacao_de_dominio(client):
    pid = criar_projeto(client)
    client.post(f"/p/{pid}/dominios/equipe", data={"status_0": "atendido", "evidencia_0": "Todos conhecem a visão",
                                                    "status_1": "parcial", "status_2": "valor_invalido"})
    html = client.get(f"/p/{pid}/dominios/equipe").get_data(as_text=True)
    assert "Todos conhecem a visão" in html
    assert 'name="status_2" value="nao_avaliado" checked' in html
    painel = client.get(f"/p/{pid}/dominios").get_data(as_text=True)
    assert "1 atendidos · 1 parciais" in painel


def test_isolamento_entre_projetos(client):
    p1 = criar_projeto(client, "P1")
    p2 = criar_projeto(client, "P2")
    s1 = criar_parte(client, p1, nome="Só do P1")
    assert client.get(f"/p/{p2}/partes/{s1}").status_code == 404
    client.post(f"/p/{p2}/partes/analise", data={f"poder_{s1}": "5", f"interesse_{s1}": "5", f"atitude_{s1}": "opositor"})
    html = client.get(f"/p/{p1}/partes/{s1}").get_data(as_text=True)
    assert "selo-opositor" not in html


def test_excluir_projeto_exige_confirmacao(client):
    pid = criar_projeto(client)
    criar_parte(client, pid)
    client.post(f"/p/{pid}/excluir", data={})
    assert client.get(f"/p/{pid}").status_code == 200
    client.post(f"/p/{pid}/excluir", data={"confirmar": "sim"})
    assert client.get(f"/p/{pid}").status_code == 404
