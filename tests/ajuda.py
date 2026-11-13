"""Funções de apoio compartilhadas pelos testes."""
import os
import sqlite3

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def novo_projeto(client, abordagem=None, nome="P"):
    r = client.post("/projetos/novo", data={"nome": nome})
    pid = int(r.headers["Location"].split("/p/")[1].split("/")[0])
    if abordagem:
        client.post(f"/p/{pid}/abordagem", data={"acao": "salvar", "abordagem": abordagem})
    return pid


def criar(client, url, **dados):
    """POST que cria um registro e devolve o id do redirecionamento."""
    r = client.post(url, data=dados)
    assert r.status_code == 302, r.get_data(as_text=True)[:400]
    return int(r.headers["Location"].split("#")[0].rstrip("/").split("/")[-1])


def html(client, url, **kw):
    return client.get(url, **kw).get_data(as_text=True)


def banco_na_versao(caminho, versao):
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


def concluir_fase_iniciar(client, pid):
    """Preenche o mínimo da fase Iniciar (termo e uma parte interessada) para liberar os painéis da visão geral."""
    client.post(f"/p/{pid}/abertura", data={"status": "rascunho", "proposito": "Motivo", "objetivos": "Objetivo"})
    client.post(f"/p/{pid}/partes/nova", data={"nome": "Patrocinadora", "papel": "Diretora", "categoria": "Patrocinador", "ativa": "1"})
