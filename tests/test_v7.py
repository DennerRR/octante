"""Testes da versão 7: princípios (autoavaliação, business case, conformidade, mudança organizacional, decisões e premissas)."""
import os
import shutil
import sqlite3
from datetime import date, timedelta

import pytest

from ajuda import concluir_fase_iniciar, banco_na_versao, criar, html, novo_projeto
from app import create_app
from db import VERSAO_ATUAL, get_db

PAGINAS_V7 = ["principios", "business-case", "conformidade", "mudanca-organizacional", "decisoes"]


def test_banco_da_v6_migra(tmp_path):
    caminho = tmp_path / "v6.db"
    banco_na_versao(caminho, 6)
    c = create_app({"TESTING": True, "DATABASE": str(caminho), "SECRET_KEY": "x"}).test_client()
    assert sqlite3.connect(caminho).execute("PRAGMA user_version").fetchone()[0] == VERSAO_ATUAL
    for u in ["/p/1", "/p/1/trabalho/licoes", "/p/1/encerramento"] + [f"/p/1/{x}" for x in PAGINAS_V7]:
        assert c.get(u).status_code == 200, u


@pytest.mark.skipif(not os.path.exists("/home/claude/v6_backup/instance/gestor.db"), reason="sem banco real da v6")
def test_banco_real_da_v6_migra(tmp_path):
    caminho = tmp_path / "real.db"
    shutil.copy("/home/claude/v6_backup/instance/gestor.db", caminho)
    c = create_app({"TESTING": True, "DATABASE": str(caminho), "SECRET_KEY": "x"}).test_client()
    ids = [r[0] for r in sqlite3.connect(caminho).execute("SELECT id FROM projeto")]
    assert ids
    for pid in ids:
        for u in [f"/p/{pid}"] + [f"/p/{pid}/{x}" for x in PAGINAS_V7]:
            assert c.get(u).status_code == 200, u


def test_autoavaliacao_tem_12_principios_e_salva_reflexao(client):
    pid = novo_projeto(client, "adaptativa")
    pagina = html(client, f"/p/{pid}/principios")
    assert pagina.count('class="cartao principio principio-') == 12
    client.post(f"/p/{pid}/principios", data={"status_0": "parcial", "reflexao_0": "Falta olhar o impacto ambiental"})
    pagina = html(client, f"/p/{pid}/principios")
    assert "Falta olhar o impacto ambiental" in pagina
    # projeto novo: o alerta dos princípios fica oculto até concluir a fase Iniciar (v10)
    assert "Princípios com pouca evidência" not in html(client, f"/p/{pid}")
    concluir_fase_iniciar(client, pid)
    assert "Princípios com pouca evidência" in html(client, f"/p/{pid}")


def test_business_case_calcula_vpl_roi_payback(client):
    pid = novo_projeto(client)
    client.post(f"/p/{pid}/business-case", data={
        "bc_necessidade": "Muitas faltas", "bc_justificativa": "Perda de receita", "bc_estrategia": "Digitalização",
        "bc_investimento": "100.000", "bc_beneficio_anual": "50.000", "bc_custo_anual": "10.000", "bc_horizonte_anos": "3", "bc_taxa": "10"})
    with client.application.app_context():
        import principios
        p = get_db().execute("SELECT * FROM projeto WHERE id = ?", (pid,)).fetchone()
        fin = principios.analise_financeira(p)
        assert p["bc_revisado_em"] == date.today().isoformat()
    # fluxo 40 mil/ano por 3 anos a 10%: VPL = -100000 + 40000*(1/1,1 + 1/1,21 + 1/1,331) = -525,92
    assert fin["fluxo"] == 40000
    assert fin["vpl"] == pytest.approx(-525.92, abs=0.01)
    assert fin["roi"] == pytest.approx(0.2)
    assert fin["payback"] == pytest.approx(2.5)
    assert not fin["viavel"]
    assert "VPL negativo" in html(client, f"/p/{pid}")
    pagina = html(client, f"/p/{pid}/business-case")
    assert "-R$ 525,92" in pagina and "2,5 anos" in pagina


def test_custo_previsto_acima_do_investimento_gera_alerta(client):
    pid = novo_projeto(client)
    iid = criar(client, f"/p/{pid}/entrega/itens/novo", titulo="Módulo")
    client.post(f"/p/{pid}/medicao/cronograma", data={"acao": "itens", f"inicio_{iid}": "", f"fim_{iid}": "", f"custo_planejado_{iid}": "80.000"})
    with client.application.app_context():
        assert get_db().execute("SELECT custo_planejado FROM item WHERE id = ?", (iid,)).fetchone()[0] == 80000
    client.post(f"/p/{pid}/business-case", data={"bc_investimento": "50.000", "bc_beneficio_anual": "60.000", "bc_horizonte_anos": "2"})
    assert "passou do investimento do business case" in html(client, f"/p/{pid}")


def test_business_case_desatualizado(client):
    pid = novo_projeto(client)
    client.post(f"/p/{pid}/business-case", data={"bc_necessidade": "x"})
    with client.application.app_context():
        get_db().execute("UPDATE projeto SET bc_revisado_em = ? WHERE id = ?", ((date.today() - timedelta(days=120)).isoformat(), pid))
        get_db().commit()
    assert "não é revisado há mais de 90 dias" in html(client, f"/p/{pid}")


def test_conformidade_exige_evidencia_e_alerta_prazo(client):
    pid = novo_projeto(client)
    url = f"/p/{pid}/conformidade"
    ontem = (date.today() - timedelta(days=1)).isoformat()
    client.post(url, data={"area": "privacidade", "requisito": "Consentimento LGPD", "prazo": ontem, "status": "pendente"})
    assert "passou do prazo" in html(client, f"/p/{pid}")
    with client.application.app_context():
        rid = get_db().execute("SELECT id FROM conformidade WHERE projeto_id = ?", (pid,)).fetchone()["id"]
    r = client.post(url, data={"registro_id": rid, "area": "privacidade", "requisito": "Consentimento LGPD", "status": "atendido"},
                    follow_redirects=True).get_data(as_text=True)
    assert "registre a evidência" in r
    client.post(url, data={"registro_id": rid, "area": "privacidade", "requisito": "Consentimento LGPD", "status": "atendido",
                           "evidencia": "Termo no cadastro"})
    assert "passou do prazo" not in html(client, f"/p/{pid}")
    # área inválida é recusada; outro projeto não pode editar
    client.post(url, data={"area": "inventada", "requisito": "x"})
    outro = novo_projeto(client, nome="Outro")
    assert client.post(f"/p/{outro}/conformidade", data={"registro_id": rid, "area": "legal", "requisito": "y"}).status_code == 404
    with client.application.app_context():
        assert get_db().execute("SELECT COUNT(*) FROM conformidade").fetchone()[0] == 1


def test_mudanca_organizacional_grupos_e_medicoes(client):
    pid = novo_projeto(client)
    parte = criar(client, f"/p/{pid}/partes/nova", nome="Recepção")
    url = f"/p/{pid}/mudanca-organizacional"
    client.post(url, data={"acao": "estados", "mudanca_estado_atual": "Agenda em papel", "mudanca_estado_futuro": "Agenda online"})
    client.post(url, data={"grupo": "Recepcionistas", "parte_id": parte, "impacto": "5", "prontidao": "2", "meta_adocao": "90"})
    assert "prontidão baixa para a mudança" in html(client, f"/p/{pid}")
    with client.application.app_context():
        gid = get_db().execute("SELECT id FROM adocao_grupo WHERE projeto_id = ?", (pid,)).fetchone()["id"]
    client.post(url, data={"acao": "medir", "grupo_id": gid, "adocao": "30", "data": (date.today() - timedelta(days=7)).isoformat()})
    client.post(url, data={"acao": "medir", "grupo_id": gid, "adocao": "95", "prontidao": "4"})
    client.post(url, data={"acao": "medir", "grupo_id": gid, "adocao": "150"})  # inválido
    with client.application.app_context():
        import principios
        g = principios.listar_grupos(pid)[0]
    assert g["serie"] == [30, 95] and g["na_meta"] and g["prontidao"] == 4 and not g["risco_resistencia"]
    pagina = html(client, url)
    assert "Agenda online" in pagina and "<svg" in pagina
    # parte de outro projeto não é aceita
    outro = novo_projeto(client, nome="O")
    p2 = criar(client, f"/p/{outro}/partes/nova", nome="X")
    client.post(url, data={"grupo": "Médicos", "parte_id": p2})
    with client.application.app_context():
        assert get_db().execute("SELECT parte_id FROM adocao_grupo WHERE grupo = 'Médicos'").fetchone()[0] is None
    # encerramento acusa grupo não adotado
    assert "grupo(s) ainda não adotaram" in html(client, f"/p/{pid}/encerramento")


def test_decisoes_e_premissas(client):
    pid = novo_projeto(client)
    url = f"/p/{pid}/decisoes"
    client.post(url, data={"acao": "decisao", "titulo": "WhatsApp em vez de SMS", "alternativas": "SMS, e-mail",
                           "efeitos": "Custo menor; depende de conta comercial", "envolvidos": "Equipe e recepção", "decidido_por": "PO"})
    ontem = (date.today() - timedelta(days=1)).isoformat()
    client.post(url, data={"acao": "premissa", "descricao": "Pacientes têm WhatsApp", "validar_ate": ontem})
    assert "devia ter sido validada" in html(client, f"/p/{pid}")
    with client.application.app_context():
        xid = get_db().execute("SELECT id FROM premissa WHERE projeto_id = ?", (pid,)).fetchone()["id"]
    r = client.post(url, data={"acao": "status_premissa", "registro_id": xid, "status": "invalidada"}, follow_redirects=True).get_data(as_text=True)
    assert "vira um risco" in r
    assert "devia ter sido validada" not in html(client, f"/p/{pid}")
    with client.application.app_context():
        import principios
        p = get_db().execute("SELECT * FROM projeto WHERE id = ?", (pid,)).fetchone()
        p5 = principios.avaliar_principios(p)[4]
    rotulos = {c["rotulo"]: c["ok"] for c in p5["checks"]}
    assert rotulos["Premissas registradas"] and rotulos["Decisões registram alternativas e efeitos em outras áreas"]


def test_licao_aplicada_conta_no_principio_11(client):
    pid = novo_projeto(client)
    client.post(f"/p/{pid}/trabalho/licoes", data={"descricao": "Demos frequentes ajudam"})
    with client.application.app_context():
        lid = get_db().execute("SELECT id FROM licao WHERE projeto_id = ?", (pid,)).fetchone()["id"]
    client.post(f"/p/{pid}/trabalho/licoes", data={"acao": "aplicar", "licao_id": lid, "aplicada": "1"})
    assert "desfazer" in html(client, f"/p/{pid}/trabalho/licoes")
    with client.application.app_context():
        import principios
        p = get_db().execute("SELECT * FROM projeto WHERE id = ?", (pid,)).fetchone()
        p11 = principios.avaliar_principios(p)[10]
    assert {c["rotulo"]: c["ok"] for c in p11["checks"]}["Lições aplicadas no próprio projeto"]


def test_exemplo_tem_principios_fortes(tmp_path):
    """O projeto de demonstração deve exercitar todos os princípios (nenhum fraco)."""
    import exemplo
    app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "ex.db"), "SECRET_KEY": "x"})
    pid = exemplo.criar(app)
    with app.app_context():
        import principios
        with app.test_request_context():
            p = get_db().execute("SELECT * FROM projeto WHERE id = ?", (pid,)).fetchone()
            niveis = {a["numero"]: (a["nivel"], [c["rotulo"] for c in a["checks"] if not c["ok"]]) for a in principios.avaliar_principios(p)}
    # a demonstração tem lacunas de propósito (para mostrar os alertas), mas nenhum princípio fica sem evidência
    fracos = {k: v for k, v in niveis.items() if v[0] == "fraco"}
    assert not fracos, fracos
    assert sum(1 for v in niveis.values() if v[0] == "forte") >= 10
