"""Testes da versão 4: domínio Entrega e planejamento do escopo."""
import sqlite3
from datetime import date, timedelta

import pmbok
from ajuda import banco_na_versao, criar, html, novo_projeto
from app import create_app
from db import VERSAO_ATUAL, get_db

IMPACTOS_OK = {c: "sem impacto" for c, *_ in pmbok.IMPACTOS_MUDANCA}


def item(client, pid, **campos):
    dados = {"titulo": "Item", "tipo": "historia", "status": "a_fazer"}
    dados.update(campos)
    return criar(client, f"/p/{pid}/entrega/itens/novo", **dados)


def editar(client, pid, iid, **campos):
    dados = {"titulo": "Item", "tipo": "historia", "status": "a_fazer"}
    dados.update(campos)
    return client.post(f"/p/{pid}/entrega/itens/{iid}", data=dados, follow_redirects=True).get_data(as_text=True)


def test_banco_da_v3_migra_para_a_versao_atual(tmp_path):
    caminho = tmp_path / "v3.db"
    banco_na_versao(caminho, 3)
    conn = sqlite3.connect(caminho)
    conn.execute("INSERT INTO mudanca (projeto_id, codigo, titulo, status) VALUES (1, 1, 'Antiga', 'aprovada')")
    conn.commit()
    conn.close()
    c = create_app({"TESTING": True, "DATABASE": str(caminho), "SECRET_KEY": "x"}).test_client()
    assert sqlite3.connect(caminho).execute("PRAGMA user_version").fetchone()[0] == VERSAO_ATUAL
    for u in ["/p/1", "/p/1/entrega", "/p/1/entrega/itens", "/p/1/entrega/quadro", "/p/1/trabalho/mudancas/1"]:
        assert c.get(u).status_code == 200, u
    assert "M-1 (Antiga) foi aprovada e ainda não foi incorporada ao escopo" in html(c, "/p/1")


def test_paginas_e_isolamento(client):
    a, b = novo_projeto(client), novo_projeto(client)
    iid = item(client, a)
    for u in ["", "/itens", "/itens?status=todos", "/itens/novo", f"/itens/{iid}", "/quadro", "/qualidade", "/beneficios"]:
        assert client.get(f"/p/{a}/entrega{u}").status_code == 200, u
    assert client.get(f"/p/{b}/entrega/itens/{iid}").status_code == 404
    assert client.post(f"/p/{b}/entrega/itens/{iid}/mover", data={"destino": "aceito"}).status_code == 404
    assert client.get(f"/p/{a}/dominios/entrega").status_code == 200


def test_conclusao_exige_definicao_de_pronto_e_aceite_exige_criterios(client):
    pid = novo_projeto(client)
    client.post(f"/p/{pid}/entrega", data={"definicao_pronto": "Testes passando\nRevisado", "unidade_estimativa": "pontos"})
    iid = item(client, pid, titulo="Agendar consulta")
    base = {"titulo": "Agendar consulta"}
    assert "confirme que ele atende à definição de pronto" in editar(client, pid, iid, **base, status="concluido")
    pagina = editar(client, pid, iid, **base, status="concluido", dod_ok="1")
    assert "I-1 atualizado" in pagina and "concluído em " + date.today().strftime("%d/%m/%Y") in pagina
    assert "sem critérios de aceite" in editar(client, pid, iid, **base, status="aceito", dod_ok="1", aceito_por="Dra. Lúcia")
    assert "Informe quem aceitou" in editar(client, pid, iid, **base, status="aceito", dod_ok="1", criterios_aceite="Agenda em 2 min")
    pagina = editar(client, pid, iid, **base, status="aceito", dod_ok="1", criterios_aceite="Agenda em 2 min", aceito_por="Dra. Lúcia")
    assert "aceito em " + date.today().strftime("%d/%m/%Y") in pagina
    assert "1 de 1 itens aceitos (100%)" in html(client, f"/p/{pid}/dominios/entrega")
    # reabrir limpa as datas de conclusão e aceite
    pagina = editar(client, pid, iid, **base, status="em_andamento", criterios_aceite="Agenda em 2 min")
    assert "concluído em" not in pagina and "aceito em" not in pagina


def test_hierarquia_conta_so_itens_sem_decomposicao(client, app):
    pid = novo_projeto(client)
    outro = novo_projeto(client)
    epico = item(client, pid, titulo="Agendamento", tipo="epico", estimativa="100")
    h1 = item(client, pid, titulo="Marcar", pai_id=str(epico), estimativa="3", status="concluido")
    item(client, pid, titulo="Desmarcar", pai_id=str(epico), estimativa="5")
    lista = html(client, f"/p/{pid}/entrega/itens?status=todos")
    assert "1/2 itens concluídos" in lista
    assert "Escopo: 0 de 8 pontos aceitos (0%); 38% concluídos." in html(client, f"/p/{pid}/dominios/entrega")
    # ciclo (pai vira filho do próprio filho) e pai de outro projeto são ignorados
    editar(client, pid, epico, titulo="Agendamento", tipo="epico", pai_id=str(h1))
    alheio = item(client, outro, titulo="De outro projeto")
    editar(client, pid, h1, titulo="Marcar", pai_id=str(alheio), status="concluido")
    with app.app_context():
        linhas = dict(get_db().execute("SELECT id, pai_id FROM item WHERE projeto_id = ?", (pid,)).fetchall())
    assert linhas[epico] is None and linhas[h1] is None


def test_linha_de_base_e_scope_creep(client):
    pid = novo_projeto(client, "preditiva")
    r = client.post(f"/p/{pid}/entrega/linha-base", data={}, follow_redirects=True).get_data(as_text=True)
    assert "Registre os itens do escopo antes" in r
    item(client, pid, titulo="Cadastro")
    item(client, pid, titulo="Agenda")
    client.post(f"/p/{pid}/entrega/linha-base", data={"motivo": "Escopo aprovado"})
    assert "possível scope creep" not in html(client, f"/p/{pid}")
    novo = item(client, pid, titulo="Pagamento online")
    visao = html(client, f"/p/{pid}")
    assert "1 item(ns) entraram no escopo depois da linha de base sem mudança aprovada (I-3): possível scope creep." in visao
    assert "fora da linha de base" in html(client, f"/p/{pid}/entrega/itens")
    # ligar o item a uma mudança aprovada resolve
    client.post(f"/p/{pid}/trabalho/mudancas/nova", data={"titulo": "Pagamento", "status": "aprovada", "decidido_por": "S",
                                                         "comunicada": "1", **IMPACTOS_OK})
    editar(client, pid, novo, titulo="Pagamento online", mudanca_id="1")
    assert "possível scope creep" not in html(client, f"/p/{pid}")
    # refazer a linha de base exige motivo
    r = client.post(f"/p/{pid}/entrega/linha-base", data={}, follow_redirects=True).get_data(as_text=True)
    assert "informe o motivo" in r
    r = client.post(f"/p/{pid}/entrega/linha-base", data={"motivo": "M-1 aprovada"}, follow_redirects=True).get_data(as_text=True)
    assert "Versão 2" in r and "3 itens" in r


def test_fluxo_no_adaptativo_e_limite_de_wip(client):
    pid = novo_projeto(client, "adaptativa")
    ids = [item(client, pid, titulo=f"H{n}") for n in range(3)]
    assert "entrou mais trabalho" not in html(client, f"/p/{pid}")  # montar o backlog inicial não é crescimento de escopo
    client.post(f"/p/{pid}/entrega/linha-base", data={})
    item(client, pid, titulo="Nova ideia")
    assert "entrou mais trabalho novo (1 itens) do que foi concluído (0)" in html(client, f"/p/{pid}")
    assert "A definição de pronto ainda não foi escrita" in html(client, f"/p/{pid}")
    client.post(f"/p/{pid}/entrega", data={"limite_wip": "1", "unidade_estimativa": "pontos"})
    for iid in ids[:2]:
        r = client.post(f"/p/{pid}/entrega/itens/{iid}/mover", data={"destino": "em_andamento"})
        assert r.headers["Location"].endswith("/entrega/quadro")
    assert "Trabalho em andamento (2) acima do limite definido (1)" in html(client, f"/p/{pid}")
    quadro = html(client, f"/p/{pid}/entrega/quadro")
    assert "Acima do limite" in quadro and "sem critérios de aceite" in quadro
    assert "(H0) está em andamento sem critérios de aceite" in html(client, f"/p/{pid}/entrega")


def test_mover_pelo_quadro_respeita_as_regras(client):
    pid = novo_projeto(client)
    client.post(f"/p/{pid}/entrega", data={"definicao_pronto": "Testado", "unidade_estimativa": "horas"})
    iid = item(client, pid)
    r = client.post(f"/p/{pid}/entrega/itens/{iid}/mover", data={"destino": "concluido"})
    assert r.headers["Location"].endswith(f"/entrega/itens/{iid}#conclusao")
    assert client.post(f"/p/{pid}/entrega/itens/{iid}/mover", data={"destino": "cancelado"}).status_code == 400
    assert 'selo-item-a_fazer' in html(client, f"/p/{pid}/entrega/itens/{iid}")


def test_item_concluido_ha_muito_tempo_sem_aceite(client, app):
    pid = novo_projeto(client)
    iid = item(client, pid, titulo="Relatório", status="concluido")
    with app.app_context():
        db = get_db()
        db.execute("UPDATE item SET concluido_em = ? WHERE id = ?", ((date.today() - timedelta(days=20)).isoformat(), iid))
        db.commit()
    assert "I-1 (Relatório) foi concluído há 20 dias e ainda não foi aceito" in html(client, f"/p/{pid}")


def test_custo_da_qualidade(client):
    pid = novo_projeto(client)
    url = f"/p/{pid}/entrega/qualidade"
    client.post(url, data={"categoria": "prevencao", "descricao": "Treinamento", "custo": "1.000"})
    client.post(url, data={"categoria": "falha_interna", "descricao": "Refazer tela de agenda", "custo": "2.500"})
    client.post(url, data={"categoria": "invalida", "descricao": "X"})
    pagina = html(client, url)
    assert "Conformidade: <strong>R$ 1.000,00</strong>" in pagina and "Não conformidade: <strong>R$ 2.500,00</strong>" in pagina
    assert "Defeitos resolvidos: <strong>0</strong> de 1" in pagina
    assert "O custo das falhas (R$ 2.500,00) é maior que o investido em prevenção e avaliação (R$ 1.000,00)" in html(client, f"/p/{pid}")
    client.post(url, data={"acao": "resolver", "registro_id": "2"})
    assert "1 de 1 defeitos resolvidos" in html(client, f"/p/{pid}/dominios/entrega")
    client.post(url, data={"acao": "excluir", "registro_id": "2"})
    assert "Refazer tela de agenda" not in html(client, url)


def test_beneficios(client):
    pid = novo_projeto(client)
    url = f"/p/{pid}/entrega/beneficios"
    ontem = (date.today() - timedelta(days=1)).isoformat()
    client.post(url, data={"descricao": "Menos ligações", "meta": "-40%", "data_prevista": ontem})
    assert "Benefício “Menos ligações” passou da data prevista" in html(client, f"/p/{pid}")
    r = client.post(f"{url}/1", data={"descricao": "Menos ligações", "status": "realizado"}, follow_redirects=True).get_data(as_text=True)
    assert "registre o resultado medido" in r
    client.post(f"{url}/1", data={"descricao": "Menos ligações", "status": "realizado", "resultado": "-45%", "data_prevista": ontem})
    assert "passou da data prevista" not in html(client, f"/p/{pid}")
    assert "Benefícios realizados: 1 de 1" in html(client, f"/p/{pid}/dominios/entrega")
    assert client.post(f"/p/{novo_projeto(client)}/entrega/beneficios/1", data={"acao": "excluir"}).status_code == 404


def test_mudanca_aprovada_e_risco_viram_itens(client):
    pid = novo_projeto(client, "preditiva")
    client.post(f"/p/{pid}/trabalho/mudancas/nova", data={"titulo": "Pagamento online", "descricao": "Gateway", "status": "aprovada",
                                                         "decidido_por": "S", "comunicada": "1", **IMPACTOS_OK})
    assert "M-1 (Pagamento online) foi aprovada e ainda não foi incorporada ao escopo" in html(client, f"/p/{pid}")
    form = html(client, f"/p/{pid}/entrega/itens/novo?mudanca=1")
    assert 'value="Pagamento online"' in form and "Gateway" in form
    item(client, pid, titulo="Pagamento online", mudanca_id="1")
    assert "ainda não foi incorporada" not in html(client, f"/p/{pid}")
    assert "I-1</strong> Pagamento online" in html(client, f"/p/{pid}/trabalho/mudancas/1")

    client.post(f"/p/{pid}/incerteza/riscos/novo", data={"titulo": "Vazamento", "tipo": "ameaca", "status": "aberto",
                                                        "plano_resposta": "Criptografar dados"})
    form = html(client, f"/p/{pid}/entrega/itens/novo?risco=1")
    assert "Resposta ao risco R-1: Vazamento" in form and "Criptografar dados" in form
    item(client, pid, titulo="Criptografia", risco_id="1")
    assert "I-2</strong> Criptografia" in html(client, f"/p/{pid}/incerteza/riscos/1")
    assert "R-1</a>" in html(client, f"/p/{pid}/entrega/itens")


def test_ordem_de_prioridade(client):
    pid = novo_projeto(client)
    a, b = item(client, pid, titulo="Primeiro criado"), item(client, pid, titulo="Segundo criado")
    client.post(f"/p/{pid}/entrega/itens/ordem", data={f"ordem_{a}": "2", f"ordem_{b}": "1", "ordem_999": "1"})
    lista = html(client, f"/p/{pid}/entrega/itens")
    assert lista.index("Segundo criado") < lista.index("Primeiro criado")
