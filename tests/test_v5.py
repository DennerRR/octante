"""Testes da versão 5: cronograma, orçamento e domínio Medição."""
import sqlite3
from datetime import date, timedelta

import graficos
import medicao
from ajuda import concluir_fase_iniciar, banco_na_versao, criar, html, novo_projeto
from app import create_app
from db import VERSAO_ATUAL, get_db

HOJE = date.today()


def d(dias):
    return (HOJE + timedelta(days=dias)).isoformat()


def item(client, pid, **campos):
    dados = {"titulo": "Item", "tipo": "historia", "status": "a_fazer"}
    dados.update(campos)
    return criar(client, f"/p/{pid}/entrega/itens/novo", **dados)


def planejar(client, pid, linhas):
    """linhas: {item_id: (inicio, fim, custo_planejado, custo_real, iteracao)}"""
    dados = {"acao": "itens"}
    for iid, (ini, fim, cp, cr, it) in linhas.items():
        dados.update({f"inicio_{iid}": ini or "", f"fim_{iid}": fim or "", f"custo_planejado_{iid}": cp or "",
                      f"custo_real_{iid}": cr or "", f"iteracao_{iid}": it or ""})
    return client.post(f"/p/{pid}/medicao/cronograma", data=dados, follow_redirects=True).get_data(as_text=True)


def test_escala_e_numeros():
    assert graficos.escala(37) == [0, 10, 20, 30, 40]
    assert graficos.escala(8) == [0, 2, 4, 6, 8]
    assert graficos.escala(0) == [0, 1]
    assert graficos.numero(1234.5) == "1234,5" and graficos.numero(25000) == "25 mil" and graficos.numero(3.0) == "3"


def test_banco_da_v4_migra(tmp_path):
    caminho = tmp_path / "v4.db"
    banco_na_versao(caminho, 4)
    conn = sqlite3.connect(caminho)
    conn.execute("INSERT INTO item (projeto_id, codigo, titulo, status) VALUES (1, 1, 'Antigo', 'em_andamento')")
    conn.commit()
    conn.close()
    c = create_app({"TESTING": True, "DATABASE": str(caminho), "SECRET_KEY": "x"}).test_client()
    assert sqlite3.connect(caminho).execute("PRAGMA user_version").fetchone()[0] == VERSAO_ATUAL
    for u in ["/p/1", "/p/1/medicao", "/p/1/medicao/cronograma", "/p/1/medicao/indicadores", "/p/1/medicao/relatorios",
              "/p/1/dominios/medicao", "/p/1/entrega/itens/1"]:
        assert c.get(u).status_code == 200, u


def test_valor_agregado_calcula_os_indices(client, app):
    pid = novo_projeto(client, "preditiva")
    a = item(client, pid, titulo="A", status="concluido")
    b = item(client, pid, titulo="B")
    # A: 1.000 planejado, terminou no passado, custou 1.250. B: 1.000 planejado, metade do período já passou.
    planejar(client, pid, {a: (d(-20), d(-11), "1.000", "1.250", None), b: (d(-9), d(10), "1.000", "", None)})
    with app.test_request_context():
        p = get_db().execute("SELECT * FROM projeto WHERE id = ?", (pid,)).fetchone()
        r = medicao.valor_agregado(p, medicao.listar_itens(pid))
    assert r["onp"] == 2000 and r["va"] == 1000 and r["cr"] == 1250
    assert r["vp"] == 1500  # A inteiro + B 10 de 20 dias
    assert round(r["idp"], 3) == 0.667 and r["idc"] == 0.8
    assert r["ent"] == 2500 and r["ept"] == 1250 and r["vnt"] == -500 and r["idpt"] == 1000 / 750
    pagina = html(client, f"/p/{pid}/medicao")
    assert "R$ 2.500,00" in pagina and "0,80" in pagina
    concluir_fase_iniciar(client, pid)
    visao = html(client, f"/p/{pid}")
    assert "Prazo" in visao and "IDP 0,67" in visao and "IDC 0,8" in visao
    assert "Prazo em estado crítico e o projeto não tem plano de exceção" in visao
    client.post(f"/p/{pid}/medicao", data={"limite_variacao": "10", "plano_excecao": "Reunião com a patrocinadora"})
    assert "não tem plano de exceção" not in html(client, f"/p/{pid}")


def test_valor_agregado_usa_a_linha_de_base(client, app):
    pid = novo_projeto(client, "preditiva")
    a = item(client, pid, titulo="A")
    planejar(client, pid, {a: (d(-10), d(9), "1.000", "", None)})
    client.post(f"/p/{pid}/entrega/linha-base", data={})
    planejar(client, pid, {a: (d(-10), d(9), "5.000", "", None)})  # replanejar sem nova linha de base
    with app.test_request_context():
        p = get_db().execute("SELECT * FROM projeto WHERE id = ?", (pid,)).fetchone()
        assert medicao.valor_agregado(p, medicao.listar_itens(pid))["onp"] == 1000


def test_cronograma_valida_datas_e_iteracoes(client):
    pid = novo_projeto(client)
    a = item(client, pid)
    assert "término antes do início" in planejar(client, pid, {a: (d(5), d(1), "10", "", None)})
    r = client.post(f"/p/{pid}/medicao/cronograma", data={"acao": "datas", "data_inicio": d(5), "data_fim_planejada": d(1)},
                    follow_redirects=True).get_data(as_text=True)
    assert "não pode ser anterior" in r
    r = client.post(f"/p/{pid}/medicao/cronograma", data={"acao": "iteracao", "nome": "S1", "inicio": d(3), "fim": d(1)},
                    follow_redirects=True).get_data(as_text=True)
    assert "o fim não pode ser antes do início" in r
    outro = novo_projeto(client)
    client.post(f"/p/{outro}/medicao/cronograma", data={"acao": "iteracao", "nome": "Alheia", "inicio": d(0), "fim": d(13)})
    planejar(client, pid, {a: (None, None, None, None, "1")})  # iteração 1 é de outro projeto
    assert "Alheia" not in html(client, f"/p/{pid}/medicao/cronograma")


def test_velocidade_e_previsao(client, app):
    pid = novo_projeto(client, "adaptativa")
    url = f"/p/{pid}/medicao/cronograma"
    client.post(url, data={"acao": "iteracao", "nome": "S1", "inicio": d(-28), "fim": d(-15), "capacidade": "10"})
    client.post(url, data={"acao": "iteracao", "nome": "S2", "inicio": d(-14), "fim": d(-1), "capacidade": "10"})
    client.post(url, data={"acao": "iteracao", "nome": "S3", "inicio": d(0), "fim": d(13), "capacidade": "10"})
    feitos = [item(client, pid, titulo=f"F{n}", estimativa="4", status="concluido") for n in range(4)]
    resto = [item(client, pid, titulo=f"R{n}", estimativa="4") for n in range(4)]
    with app.app_context():
        db = get_db()
        for n, iid in enumerate(feitos):
            db.execute("UPDATE item SET iteracao_id = ?, concluido_em = ? WHERE id = ?", (1 + n // 2, d(-16 if n < 2 else -2), iid))
        db.commit()
    planejar(client, pid, {resto[0]: (None, None, None, None, "3")})
    with app.test_request_context():
        p = get_db().execute("SELECT * FROM projeto WHERE id = ?", (pid,)).fetchone()
        itens = medicao.listar_itens(pid)
        vel = medicao.velocidade(p, itens)
        prev = medicao.previsao(p, itens, vel)
    assert vel["media"] == 8 and vel["duracao"] == 14
    assert prev["restante"] == 16 and prev["data"] == HOJE + timedelta(days=28)
    pagina = html(client, f"/p/{pid}/medicao")
    assert "Velocidade por iteração" in pagina and "velocidade média de 8 pontos por iteração (2 iteração(ões) restantes)" in pagina
    # término planejado antes da previsão deixa o prazo em atenção ou crítico
    client.post(url, data={"acao": "datas", "data_inicio": d(-28), "data_fim_planejada": d(14)})
    with app.test_request_context():
        p = get_db().execute("SELECT * FROM projeto WHERE id = ?", (pid,)).fetchone()
        prazo = medicao.semaforo(p)[0]
    assert prazo["dimensao"] == "Prazo" and prazo["status"] == "critico"


def test_indicadores(client):
    pid = novo_projeto(client)
    url = f"/p/{pid}/medicao/indicadores"
    client.post(url, data={"nome": "Defeitos abertos", "tipo": "antecedente", "direcao": "menor", "meta": "2", "limite": "5", "unidade": "defeitos"})
    for v in ["1", "3", "4"]:
        client.post(f"{url}/1", data={"valor": v})
    visao = html(client, f"/p/{pid}")
    assert "O indicador antecedente “Defeitos abertos” piorou em duas medições seguidas" in visao
    client.post(f"{url}/1", data={"valor": "7"})
    assert "O indicador “Defeitos abertos” (7 defeitos) passou do limite." in html(client, f"/p/{pid}")
    r = client.post(f"{url}/1", data={"valor": "1", "data": d(2)}, follow_redirects=True).get_data(as_text=True)
    assert "não pode estar no futuro" in r
    assert client.post(f"/p/{novo_projeto(client)}/medicao/indicadores/1", data={"valor": "1"}).status_code == 404
    client.post(f"{url}/1", data={"acao": "excluir"})
    assert "Defeitos abertos" not in html(client, url)


def test_relatorio_de_status_congela_a_situacao(client):
    pid = novo_projeto(client)
    item(client, pid, titulo="Login", status="concluido")
    sug = html(client, f"/p/{pid}/medicao/relatorios")
    assert "I-1 Login (concluído)" in sug
    r = client.post(f"/p/{pid}/medicao/relatorios", data={"resumo": "Tudo em dia", "realizacoes": "I-1 Login"})
    rid = int(r.headers["Location"].split("/")[-1])
    html(client, f"/p/{pid}/medicao/relatorios/{rid}")  # consome a mensagem de confirmação
    pagina = html(client, f"/p/{pid}/medicao/relatorios/{rid}")
    assert "Tudo em dia" in pagina and "Situação por dimensão" in pagina and "100% concluído" in pagina
    item(client, pid, titulo="Agenda")
    assert "Questões" in html(client, f"/p/{pid}/medicao/relatorios")
    # o relatório antigo não muda
    assert html(client, f"/p/{pid}/medicao/relatorios/{rid}") == pagina
    assert client.get(f"/p/{novo_projeto(client)}/medicao/relatorios/{rid}").status_code == 404
    client.post(f"/p/{pid}/medicao/relatorios/{rid}", data={"acao": "excluir"})
    assert client.get(f"/p/{pid}/medicao/relatorios/{rid}").status_code == 404


def test_paginas_sem_dados(client):
    pid = novo_projeto(client)
    for u in ["/medicao", "/medicao/indicadores", "/medicao/relatorios", "/medicao/cronograma", "/dominios/medicao", ""]:
        assert client.get(f"/p/{pid}{u}").status_code == 200, u
    assert "Sem dados" in html(client, f"/p/{pid}/medicao")
