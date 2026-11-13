"""Testes da versão 6: Equipe, ciclo de vida, tailoring e encerramento."""
import sqlite3
from datetime import date, timedelta

import pmbok
from ajuda import banco_na_versao, criar, html, novo_projeto
from app import create_app
from db import VERSAO_ATUAL, get_db

IMPACTOS_OK = {c: "sem impacto" for c, *_ in pmbok.IMPACTOS_MUDANCA}


def membro(client, pid, nome, **campos):
    client.post(f"/p/{pid}/equipe", data={"nome": nome, **campos})
    with client.application.app_context():
        return get_db().execute("SELECT id FROM membro WHERE projeto_id = ? AND nome = ?", (pid, nome)).fetchone()["id"]


def test_banco_da_v5_migra(tmp_path):
    caminho = tmp_path / "v5.db"
    banco_na_versao(caminho, 5)
    c = create_app({"TESTING": True, "DATABASE": str(caminho), "SECRET_KEY": "x"}).test_client()
    assert sqlite3.connect(caminho).execute("PRAGMA user_version").fetchone()[0] == VERSAO_ATUAL
    for u in ["/", "/p/1", "/p/1/equipe", "/p/1/equipe/acordo", "/p/1/equipe/raci", "/p/1/equipe/saude", "/p/1/fases",
              "/p/1/tailoring", "/p/1/encerramento", "/p/1/dominios/equipe", "/p/1/dominios/abordagem"]:
        assert c.get(u).status_code == 200, u


def test_membros_e_lideranca(client):
    pid = novo_projeto(client, "adaptativa")
    assert "Nenhum membro da equipe cadastrado" in html(client, f"/p/{pid}")
    mid = membro(client, pid, "Ana Souza", papel="Back-end", lacunas="Testes automatizados", local="remoto", motivador="Desafio")
    visao = html(client, f"/p/{pid}")
    assert "Ana Souza tem lacunas de habilidade sem plano de desenvolvimento" in visao
    assert "não tem acordo de trabalho" in visao
    client.post(f"/p/{pid}/equipe/membros/{mid}", data={"nome": "Ana Souza", "lacunas": "Testes", "plano_desenvolvimento": "Mentoria"})
    assert "sem plano de desenvolvimento" not in html(client, f"/p/{pid}")
    client.post(f"/p/{pid}/equipe", data={"acao": "lideranca", "modelo_lideranca": "distribuida", "estagio_equipe": "confronto"})
    assert "Estágio da equipe (Tuckman): Confronto." in html(client, f"/p/{pid}/dominios/equipe")
    for n in range(9):
        membro(client, pid, f"Pessoa {n}")
    assert "equipes de 7 ± 2 pessoas; esta tem 10" in html(client, f"/p/{pid}")
    client.post(f"/p/{pid}/equipe/membros/{mid}", data={"acao": "liberar"})
    assert "liberado em" in html(client, f"/p/{pid}/equipe")
    assert client.get(f"/p/{novo_projeto(client)}/equipe/membros/{mid}").status_code == 404


def test_matriz_raci_valida_aprovador_e_executor(client):
    pid = novo_projeto(client)
    a, b = membro(client, pid, "Ana"), membro(client, pid, "Bruno")
    client.post(f"/p/{pid}/equipe/raci", data={"acao": "linha", "descricao": "Aprovar alterações"})
    assert "ninguém aprova (A) e ninguém executa (R)" in html(client, f"/p/{pid}")
    client.post(f"/p/{pid}/equipe/raci", data={"acao": "salvar", f"p_1_{a}": "A", f"p_1_{b}": "A"})
    assert "mais de um aprovador (A)" in html(client, f"/p/{pid}/equipe/raci")
    client.post(f"/p/{pid}/equipe/raci", data={"acao": "salvar", f"p_1_{a}": "A", f"p_1_{b}": "R"})
    assert "Matriz RACI" not in html(client, f"/p/{pid}").split("Pontos de atenção")[1].split("Domínios de desempenho")[0]
    assert "<strong>A</strong> · Aprovar alterações" in html(client, f"/p/{pid}/equipe/membros/{a}")
    client.post(f"/p/{pid}/equipe/raci", data={"excluir_linha": "1"})
    assert "Aprovar alterações" not in html(client, f"/p/{pid}/equipe/raci")


def test_avaliacao_de_saude(client):
    pid = novo_projeto(client)
    membro(client, pid, "Ana")
    r = client.post(f"/p/{pid}/equipe/saude", data={}, follow_redirects=True).get_data(as_text=True)
    assert "Dê nota a pelo menos um fator" in r
    client.post(f"/p/{pid}/equipe/saude", data={"comunicacao": "4", "confianca": "2", "entendimento": "2"})
    visao = html(client, f"/p/{pid}")
    assert "fatores ficaram baixos (≤ 2): Entendimento compartilhado, Confiança" in visao
    assert "Membros da equipe sem clareza de como seguir" in html(client, f"/p/{pid}/tailoring")
    assert "média 2,7/5" in html(client, f"/p/{pid}/dominios/equipe")


def test_fases_e_revisao_de_fase(client):
    pid = novo_projeto(client, "preditiva")
    client.post(f"/p/{pid}/fases", data={"acao": "sugeridas"})
    pagina = html(client, f"/p/{pid}/fases")
    assert "1. Viabilidade" in pagina and "6. Encerramento" in pagina
    r = client.post(f"/p/{pid}/fases", data={"acao": "sugeridas"}, follow_redirects=True).get_data(as_text=True)
    assert "já tem fases" in r
    base = {"nome": "Viabilidade", "criterios_saida": "Business case aprovado\nTermo de abertura aprovado"}
    r = client.post(f"/p/{pid}/fases/1", data={**base, "status": "concluida"}, follow_redirects=True).get_data(as_text=True)
    assert "todos os critérios de saída precisam estar atendidos" in r
    r = client.post(f"/p/{pid}/fases/1", data={**base, "status": "concluida", "criterio_ok": ["0", "1"]}, follow_redirects=True).get_data(as_text=True)
    assert "registre a decisão da revisão de fase" in r
    r = client.post(f"/p/{pid}/fases/1", data={**base, "status": "concluida", "criterio_ok": ["0", "1"], "revisao_decisao": "seguir",
                                                "revisao_por": "Patrocinadora"}, follow_redirects=True).get_data(as_text=True)
    assert "Fase “Viabilidade” concluída" in r
    assert "1 concluídas com revisão de fase" in html(client, f"/p/{pid}/dominios/abordagem")
    ontem = (date.today() - timedelta(days=1)).isoformat()
    client.post(f"/p/{pid}/fases/2", data={"nome": "Design", "fim": ontem, "inicio": ontem, "status": "em_andamento"})
    assert "A fase “Design” passou da data de término" in html(client, f"/p/{pid}")
    r = client.post(f"/p/{pid}/fases/2", data={"nome": "Design", "inicio": ontem, "fim": (date.today() - timedelta(days=3)).isoformat()},
                    follow_redirects=True).get_data(as_text=True)
    assert "não pode ser antes do início" in r
    assert client.post(f"/p/{novo_projeto(client)}/fases/1", data={"acao": "excluir"}).status_code == 404


def test_diagnostico_e_decisoes_de_tailoring(client, app):
    pid = novo_projeto(client, "preditiva")
    for n in range(2):
        client.post(f"/p/{pid}/trabalho/mudancas/nova", data={"titulo": f"M{n}"})
    with app.app_context():
        db = get_db()
        db.execute("UPDATE mudanca SET criado_em = ?", ((date.today() - timedelta(days=12)).isoformat(),))
        db.commit()
    pagina = html(client, f"/p/{pid}/tailoring")
    assert "Longas esperas por aprovação: 2 mudança(s)" in pagina
    client.post(f"/p/{pid}/tailoring", data={"acao": "decisao", "tipo": "ajustar", "elemento": "Agilizar aprovações", "origem": "Diagnóstico"})
    client.post(f"/p/{pid}/tailoring", data={"acao": "respostas", "tecnologia": "Estável", "invalida": "x"})
    pagina = html(client, f"/p/{pid}/tailoring")
    assert "Agilizar aprovações" in pagina and 'value="Estável"' in pagina
    assert "1 decisão(ões) de tailoring registradas" in html(client, f"/p/{pid}/dominios/abordagem")


def test_encerramento(client):
    pid = novo_projeto(client)
    client.post(f"/p/{pid}/entrega/itens/novo", data={"titulo": "Agenda", "status": "a_fazer"})
    url = f"/p/{pid}/encerramento"
    pagina = html(client, url)
    assert "1 item(ns) ainda não aceitos" in pagina and "nenhuma lição registrada" in pagina
    r = client.post(url, data={"acao": "encerrar"}, follow_redirects=True).get_data(as_text=True)
    assert "registre a avaliação dos objetivos" in r
    r = client.post(url, data={"acao": "encerrar", "avaliacao_objetivos": "Parcial"}, follow_redirects=True).get_data(as_text=True)
    assert "Há pendências no checklist" in r
    r = client.post(url, data={"acao": "cancelar", "avaliacao_objetivos": "Não atingidos"}, follow_redirects=True).get_data(as_text=True)
    assert "explique o motivo" in r
    r = client.post(url, data={"acao": "cancelar", "avaliacao_objetivos": "Não atingidos", "justificativa": "Concorrente lançou antes"},
                    follow_redirects=True).get_data(as_text=True)
    assert "Projeto cancelado" in r
    assert "Projeto cancelado em" in html(client, f"/p/{pid}/entrega")
    assert "Cancelado" in html(client, "/")
    client.post(url, data={"acao": "reabrir"})
    assert "Projeto cancelado em" not in html(client, f"/p/{pid}")


def test_encerramento_completo_sem_pendencias(client):
    pid = novo_projeto(client)
    criar(client, f"/p/{pid}/entrega/itens/novo", titulo="Agenda", status="aceito", criterios_aceite="ok", aceito_por="Cliente")
    client.post(f"/p/{pid}/trabalho/licoes", data={"descricao": "Demos frequentes ajudam"})
    url = f"/p/{pid}/encerramento"
    dados = {"acao": "encerrar", "avaliacao_objetivos": "Atingidos", **{f"manual_{k}": "1" for k in ("contratos", "arquivo", "transicao", "termo_revisado")}}
    r = client.post(url, data=dados, follow_redirects=True).get_data(as_text=True)
    assert "Projeto encerrado" in r
    assert "Estágio da equipe (Tuckman): Dissolução." in html(client, f"/p/{pid}/dominios/equipe")
