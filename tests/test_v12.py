"""Testes da versão 12: regras de negócio revisadas."""
from datetime import date, timedelta

from ajuda import html, novo_projeto
from db import get_db


def dia(n):
    return (date.today() + timedelta(days=n)).isoformat()


def test_projeto_encerrado_e_somente_leitura(client):
    pid = novo_projeto(client, "adaptativa")
    client.post(f"/p/{pid}/encerramento", data={"acao": "cancelar", "justificativa": "Diretoria cancelou", "avaliacao_objetivos": "Não atingidos"})
    with client.application.app_context():
        assert get_db().execute("SELECT situacao FROM projeto WHERE id = ?", (pid,)).fetchone()[0] == "cancelado"
    client.post(f"/p/{pid}/partes/nova", data={"nome": "Depois do fim", "papel": "x", "categoria": "Cliente", "ativa": "1"})
    with client.application.app_context():
        assert get_db().execute("SELECT COUNT(*) FROM parte_interessada WHERE nome = 'Depois do fim'").fetchone()[0] == 0
    assert "só pode ser consultado" in html(client, f"/p/{pid}")
    client.post(f"/p/{pid}/encerramento", data={"acao": "reabrir"})
    client.post(f"/p/{pid}/partes/nova", data={"nome": "Depois do fim", "papel": "x", "categoria": "Cliente", "ativa": "1"})
    with client.application.app_context():
        assert get_db().execute("SELECT COUNT(*) FROM parte_interessada WHERE nome = 'Depois do fim'").fetchone()[0] == 1


def test_aprovar_termo_exige_quem_aprovou(client):
    pid = novo_projeto(client)
    base = {"status": "aprovado", "proposito": "p", "objetivos": "o", "criterios_sucesso": "c", "patrocinador": "s", "gerente": "g"}
    client.post(f"/p/{pid}/abertura", data=base)
    with client.application.app_context():
        assert get_db().execute("SELECT status FROM abertura WHERE projeto_id = ?", (pid,)).fetchone()[0] != "aprovado"
    client.post(f"/p/{pid}/abertura", data={**base, "aprovado_por": "Dra. Lúcia"})
    with client.application.app_context():
        assert get_db().execute("SELECT status FROM abertura WHERE projeto_id = ?", (pid,)).fetchone()[0] == "aprovado"


def test_parte_interessada_duplicada(client):
    pid = novo_projeto(client)
    dados = {"nome": "Recepção", "papel": "x", "categoria": "Usuário final", "ativa": "1"}
    client.post(f"/p/{pid}/partes/nova", data=dados)
    r = client.post(f"/p/{pid}/partes/nova", data={**dados, "nome": "recepção"})
    assert "já está no registro" in r.get_data(as_text=True)


def test_mudanca_aprovada_nao_pode_ser_excluida(client):
    pid = novo_projeto(client, "adaptativa")
    client.post(f"/p/{pid}/trabalho/mudancas/nova", data={"titulo": "Pagamento no app", "status": "aprovada", "decidido_por": "Patrocinadora"})
    with client.application.app_context():
        mid = get_db().execute("SELECT id FROM mudanca").fetchone()[0]
    client.post(f"/p/{pid}/trabalho/mudancas/{mid}", data={"acao": "excluir"})
    with client.application.app_context():
        assert get_db().execute("SELECT COUNT(*) FROM mudanca").fetchone()[0] == 1


def test_iteracoes_nao_se_sobrepoem(client):
    pid = novo_projeto(client, "adaptativa")
    u = f"/p/{pid}/medicao/cronograma"
    client.post(u, data={"acao": "iteracao", "nome": "Sprint 1", "inicio": dia(0), "fim": dia(13)})
    r = client.post(u, data={"acao": "iteracao", "nome": "Sprint 2", "inicio": dia(10), "fim": dia(23)}, follow_redirects=True)
    assert "coincidem" in r.get_data(as_text=True)
    client.post(u, data={"acao": "iteracao", "nome": "Sprint 2", "inicio": dia(14), "fim": dia(27)})
    with client.application.app_context():
        assert get_db().execute("SELECT COUNT(*) FROM iteracao").fetchone()[0] == 2


def test_recurso_desperdicio_maior_que_uso_e_uso_acima_do_planejado(client):
    pid = novo_projeto(client, "adaptativa")
    u = f"/p/{pid}/suprimentos"
    client.post(u, data={"acao": "recurso", "nome": "Licenças", "tipo": "licenca", "quantidade": "3", "usado": "1", "desperdicio": "2"})
    with client.application.app_context():
        assert get_db().execute("SELECT COUNT(*) FROM recurso_fisico").fetchone()[0] == 0
    client.post(u, data={"acao": "recurso", "nome": "Licenças", "tipo": "licenca", "quantidade": "3", "usado": "5", "desperdicio": "0"})
    assert "mais do que o planejado" in html(client, f"/p/{pid}")


def test_fornecedor_promete_depois_da_necessidade(client):
    pid = novo_projeto(client, "adaptativa")
    client.post(f"/p/{pid}/suprimentos", data={"acao": "aquisicao", "item": "API", "decisao": "comprar", "fornecedor": "Zap",
                                                 "status": "contratada", "necessario_em": dia(10), "entrega_prevista": dia(20)})
    assert "depois da data em que o projeto precisa" in html(client, f"/p/{pid}")


def test_fluxo_so_conta_termo_aprovado(client):
    pid = novo_projeto(client, "adaptativa")
    client.post(f"/p/{pid}/abertura", data={"status": "em_revisao", "proposito": "p", "objetivos": "o"})
    assert "Termo de abertura aprovado" in html(client, f"/p/{pid}")  # ainda é o próximo passo


def test_acessibilidade_basica_no_layout(client):
    pid = novo_projeto(client)
    pagina = html(client, f"/p/{pid}")
    assert 'class="pular" href="#conteudo"' in pagina and 'id="conteudo"' in pagina
    assert 'id="abrir-menu"' in pagina and 'aria-controls="menu-lateral"' in pagina
    r = client.post(f"/p/{pid}/partes/nova", data={"nome": ""})
    assert 'role="alert"' in r.get_data(as_text=True)


def test_css_sem_cores_fixas_fora_dos_tokens():
    import re
    import os
    css = open(os.path.join(os.path.dirname(__file__), "..", "static", "style.css"), encoding="utf-8").read()
    corpo = css[css.index("}", css.index(":root")):]
    assert not re.findall(r"#[0-9a-fA-F]{3,6}\b", corpo)
