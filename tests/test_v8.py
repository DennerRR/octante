"""Testes da versão 8: aquisições, recursos físicos, plano de comunicação e dicas de preenchimento."""
import json
import os
import shutil
import sqlite3
from datetime import date, timedelta

import pytest

from ajuda import banco_na_versao, html, novo_projeto
from app import create_app
from db import VERSAO_ATUAL, get_db
import dicas


def dia(n):
    return (date.today() + timedelta(days=n)).isoformat()


def test_banco_da_v7_migra(tmp_path):
    caminho = tmp_path / "v7.db"
    banco_na_versao(caminho, 7)
    c = create_app({"TESTING": True, "DATABASE": str(caminho), "SECRET_KEY": "x"}).test_client()
    assert sqlite3.connect(caminho).execute("PRAGMA user_version").fetchone()[0] == VERSAO_ATUAL
    for u in ["/p/1", "/p/1/suprimentos", "/p/1/partes/engajamento"]:
        assert c.get(u).status_code == 200, u


@pytest.mark.skipif(not os.path.exists("/home/claude/v7_backup/instance/gestor.db"), reason="sem banco real da v7")
def test_banco_real_da_v7_migra(tmp_path):
    caminho = tmp_path / "real.db"
    shutil.copy("/home/claude/v7_backup/instance/gestor.db", caminho)
    c = create_app({"TESTING": True, "DATABASE": str(caminho), "SECRET_KEY": "x"}).test_client()
    for (pid,) in sqlite3.connect(caminho).execute("SELECT id FROM projeto"):
        for u in [f"/p/{pid}", f"/p/{pid}/suprimentos"]:
            assert c.get(u).status_code == 200, u


def test_aquisicao_exige_fornecedor_e_nota(client):
    pid = novo_projeto(client, "adaptativa")
    u = f"/p/{pid}/suprimentos"
    client.post(u, data={"acao": "aquisicao", "item": "API", "decisao": "comprar", "status": "contratada"})
    assert "informe o fornecedor" in html(client, u)
    client.post(u, data={"acao": "aquisicao", "item": "API", "decisao": "comprar", "fornecedor": "Zap", "status": "encerrada"})
    assert "avalie o desempenho" in html(client, u)
    client.post(u, data={"acao": "aquisicao", "item": "API", "decisao": "comprar", "fornecedor": "Zap", "status": "encerrada", "nota_desempenho": "4"})
    assert "API" in html(client, u)


def test_alertas_de_aquisicao_atrasada_e_recurso(client):
    pid = novo_projeto(client, "adaptativa")
    u = f"/p/{pid}/suprimentos"
    client.post(u, data={"acao": "aquisicao", "item": "Licença X", "decisao": "comprar", "necessario_em": dia(-3), "status": "planejada"})
    client.post(u, data={"acao": "recurso", "nome": "Servidor", "tipo": "equipamento", "necessario_em": dia(5), "antecedencia_dias": "30", "status": "planejado"})
    pagina = html(client, f"/p/{pid}")
    assert "Licença X" in pagina and "Servidor" in pagina


def test_fornecedor_vira_parte_interessada(client):
    pid = novo_projeto(client, "adaptativa")
    u = f"/p/{pid}/suprimentos"
    client.post(u, data={"acao": "aquisicao", "item": "API", "decisao": "comprar", "fornecedor": "Zap Ltda", "status": "contratada"})
    with client.application.app_context():
        aid = get_db().execute("SELECT id FROM aquisicao").fetchone()[0]
    client.post(u, data={"acao": "fornecedor_parte", "registro_id": str(aid)})
    with client.application.app_context():
        r = get_db().execute("SELECT categoria, interna FROM parte_interessada WHERE nome = 'Zap Ltda'").fetchone()
        assert r["categoria"] == "Fornecedor" and r["interna"] == 0


def test_aquisicao_de_outro_projeto_da_404(client):
    a = novo_projeto(client, "adaptativa")
    b = novo_projeto(client, "adaptativa")
    client.post(f"/p/{a}/suprimentos", data={"acao": "aquisicao", "item": "API", "decisao": "fazer"})
    with client.application.app_context():
        aid = get_db().execute("SELECT id FROM aquisicao").fetchone()[0]
    assert client.post(f"/p/{b}/suprimentos", data={"acao": "excluir_aquisicao", "registro_id": str(aid)}).status_code == 404


def test_encerramento_avisa_aquisicao_aberta(client):
    pid = novo_projeto(client, "adaptativa")
    client.post(f"/p/{pid}/suprimentos", data={"acao": "aquisicao", "item": "API", "decisao": "comprar", "fornecedor": "Zap", "status": "contratada"})
    assert "ainda em andamento" in html(client, f"/p/{pid}/encerramento")


def test_dicas_cobrem_os_campos_principais():
    d = dicas.dicas_da_pagina("abertura")
    for campo in ("proposito", "objetivos", "criterios_sucesso", "premissas", "restricoes"):
        assert d[campo][0] and d[campo][1], campo
    assert "impacto" in dicas.dicas_da_pagina("incerteza.riscos")
    assert dicas.dicas_da_pagina(None)  # ao menos as dicas gerais


def test_pagina_publica_dicas_e_botao(client):
    pid = novo_projeto(client, "adaptativa")
    pagina = html(client, f"/p/{pid}/abertura")
    assert 'id="alternar-dicas"' in pagina
    dados = pagina.split('id="dicas-dados" type="application/json">')[1].split("</script>")[0]
    assert "proposito" in json.loads(dados.replace("&#34;", '"'))


def test_visao_geral_mostra_por_onde_comecar(client):
    pid = novo_projeto(client, "adaptativa")
    assert "Por onde começar" in html(client, f"/p/{pid}")


def test_campos_de_comunicacao_sao_salvos(client):
    pid = novo_projeto(client, "adaptativa")
    client.post(f"/p/{pid}/partes/nova", data={"nome": "Recepção", "papel": "x", "categoria": "Usuário final", "ativa": "1"})
    with client.application.app_context():
        parte = get_db().execute("SELECT id FROM parte_interessada").fetchone()[0]
    client.post(f"/p/{pid}/partes/engajamento", data={f"atual_{parte}": "2", f"info_{parte}": "Status quinzenal", f"quem_{parte}": "Gerente"})
    with client.application.app_context():
        r = get_db().execute("SELECT info_necessaria, info_responsavel FROM parte_interessada WHERE id = ?", (parte,)).fetchone()
        assert r["info_necessaria"] == "Status quinzenal" and r["info_responsavel"] == "Gerente"


# ---------------------------------------------------------------- v9: guia para iniciantes
def test_fluxo_mostra_5_fases_e_proximo_passo(client):
    pid = novo_projeto(client, "adaptativa")
    pagina = html(client, f"/p/{pid}/fluxo")
    assert pagina.count('class="fase ') + pagina.count('class="fase"') == 5
    assert "próximo" in pagina and "Termo de abertura" in pagina


def test_glossario_e_ajuda_da_pagina(client):
    pid = novo_projeto(client, "adaptativa")
    assert "Stakeholder" in html(client, f"/p/{pid}/glossario") or "stakeholder" in html(client, f"/p/{pid}/glossario")
    assert "Para que serve" in html(client, f"/p/{pid}/abertura")


def test_menu_lateral_segue_as_fases(client):
    pid = novo_projeto(client, "adaptativa")
    pagina = html(client, f"/p/{pid}")
    for fase in ("1. Iniciar", "2. Planejar", "3. Executar", "4. Acompanhar", "5. Encerrar"):
        assert fase in pagina
