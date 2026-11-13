"""Octante — aplicação Flask para gerenciamento de projetos
organizada pelos 8 domínios de desempenho do PMBOK Guide 7ª edição.

Executar:  python app.py   ->  http://localhost:5000
"""
import functools
import json
import os
import secrets
import sqlite3
import subprocess
import sys
import tempfile
import threading
import webbrowser
from datetime import date, datetime, timedelta
from urllib.parse import urlparse

from flask import Flask, abort, current_app, flash, redirect, render_template, request, send_file, url_for, g

import auditoria
import auth
import backup as backups_mod
import dados
import seguranca
import ciclo
import dicas
import entrega
import equipe
import incerteza
import medicao
import pmbok
import guia
import metodos
import pmo
import rotas_partes
import principios as principios_mod
import suprimentos
import trabalho
from db import get_db, init_db
from partes import (DIAS_SEM_INTERACAO, chave_prioridade, gerar_alertas_partes, listar_partes, obter_parte, ordem_sugerida,
                    pontos_grade, resumo_fluxo)
from util import filtro_projetos, inteiro, moeda, obter_projeto, tocar_projeto

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CAMPOS_ABERTURA = [
    "proposito", "objetivos", "criterios_sucesso", "requisitos_alto_nivel", "premissas",
    "restricoes", "riscos_alto_nivel", "marcos", "orcamento", "patrocinador", "gerente",
    "autoridade_gerente", "status", "aprovado_por", "aprovado_em",
    "visao_publico", "visao_necessidade", "visao_produto", "visao_categoria",
    "visao_beneficio", "visao_alternativa", "visao_diferencial", "visao_texto",
]
CAMPOS_TERMO_ESSENCIAIS = ["proposito", "objetivos", "criterios_sucesso", "patrocinador", "gerente"]
CAMPOS_VISAO = ["visao_publico", "visao_necessidade", "visao_produto", "visao_categoria", "visao_beneficio"]


def create_app(test_config=None):
    seguranca.configurar_fuso()
    app = Flask(__name__)
    app.extensions["ao_conectar"] = [auditoria.ao_conectar]
    app.extensions["ao_iniciar_banco"] = [auditoria.preparar]
    producao = os.environ.get("GESTOR_PRODUCAO") == "1"
    app.config.update(
        DATABASE=os.path.join(BASE_DIR, "instance", "gestor.db"),
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=producao,  # na internet o app roda em HTTPS
        PERMANENT_SESSION_LIFETIME=timedelta(hours=12),
    )
    if test_config:
        app.config.update(test_config)
    # Login: obrigatório sempre, exceto nos testes antigos (que podem ligá-lo com LOGIN_OBRIGATORIO=True).
    app.config.setdefault("LOGIN_OBRIGATORIO", not app.config.get("TESTING", False))
    app.config.setdefault("BACKUP_AUTOMATICO", not app.config.get("TESTING", False))
    # Antes de atualizar a estrutura do banco, guarda uma cópia verificada (se houver dados).
    app.config.setdefault("ANTES_DE_MIGRAR", lambda caminho, conn: backups_mod.fazer(caminho, "antes-de-migrar", conn=conn))
    init_db(app)
    if not app.config.get("SECRET_KEY"):
        app.config["SECRET_KEY"] = carregar_chave_secreta(os.path.dirname(app.config["DATABASE"]))
    app.register_blueprint(auth.bp)
    app.register_blueprint(dados.bp)
    app.register_blueprint(pmo.bp)
    app.register_blueprint(metodos.bp)
    seguranca.registrar(app)
    registrar_rotas(app)
    app.register_blueprint(incerteza.bp)
    app.register_blueprint(trabalho.bp)
    app.register_blueprint(entrega.bp)
    app.register_blueprint(medicao.bp)
    app.register_blueprint(equipe.bp)
    app.register_blueprint(ciclo.bp)
    app.register_blueprint(principios_mod.bp)
    app.register_blueprint(suprimentos.bp)

    @app.before_request
    def bloquear_post_de_outra_origem():
        """Proteção simples contra CSRF: o app só aceita formulários enviados por ele mesmo."""
        if request.method != "POST":
            return None
        origem = request.headers.get("Origin") or request.headers.get("Referer")
        if origem and origem != "null" and urlparse(origem).netloc != request.host:
            abort(403)
        return None

    @app.before_request
    def projeto_encerrado_somente_leitura():
        """Regra de negócio: projeto encerrado ou cancelado não recebe alterações (só reabrir, no encerramento)."""
        if request.method != "POST" or not request.view_args or "projeto_id" not in request.view_args:
            return None
        if request.endpoint in ("ciclo.encerramento", "projeto_excluir", "dados.anonimizar"):
            return None
        p = get_db().execute("SELECT situacao FROM projeto WHERE id = ?", (request.view_args["projeto_id"],)).fetchone()
        if p and p["situacao"] != "ativo":
            flash("Este projeto está encerrado e só pode ser consultado. Para alterar, reabra-o na tela de encerramento.", "erro")
            return redirect(request.referrer if request.referrer and urlparse(request.referrer).netloc == request.host
                            else url_for("projeto", projeto_id=request.view_args["projeto_id"]))
        return None

    @app.context_processor
    def contexto_global():
        return {"pmbok": pmbok, "hoje": date.today().isoformat(),
                "ajuda_pagina": guia.AJUDA_PAGINA.get(request.endpoint), "dicas_json": _dicas_json(request.endpoint)}

    @app.template_filter("data_br")
    def data_br(valor):
        if not valor:
            return ""
        try:
            return datetime.fromisoformat(str(valor)[:19]).strftime("%d/%m/%Y")
        except ValueError:
            return valor

    app.add_template_filter(moeda, "moeda")

    @app.template_filter("nivel")
    def nivel(valor):
        return pmbok.NIVEIS_ENGAJAMENTO_DICT.get(valor, "—")

    return app


# --------------------------------------------------------------------------
# Utilidades
# --------------------------------------------------------------------------
def carregar_chave_secreta(pasta):
    caminho = os.path.join(pasta, "secret_key")
    if os.path.exists(caminho):
        with open(caminho, encoding="utf-8") as f:
            chave = f.read().strip()
        if chave:
            return chave
    chave = secrets.token_hex(32)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(chave)
    return chave


def obter_abertura(projeto_id):
    db = get_db()
    a = db.execute("SELECT * FROM abertura WHERE projeto_id = ?", (projeto_id,)).fetchone()
    if a is None:
        db.execute("INSERT INTO abertura (projeto_id) VALUES (?)", (projeto_id,))
        db.commit()
        a = db.execute("SELECT * FROM abertura WHERE projeto_id = ?", (projeto_id,)).fetchone()
    return a


def gerar_alertas(projeto, partes, abertura):
    alertas = []
    pid = projeto["id"]
    if not projeto["abordagem"]:
        alertas.append(("medio", "A abordagem de desenvolvimento ainda não foi definida.",
                        url_for("abordagem", projeto_id=pid)))
    if abertura is not None:
        if projeto["abordagem"] == "preditiva" and abertura["status"] != "aprovado":
            alertas.append(("medio", "Abordagem preditiva: o termo de abertura ainda não foi aprovado.",
                            url_for("abertura", projeto_id=pid)))
        if projeto["abordagem"] in ("adaptativa", "hibrida") and not abertura["visao_texto"]:
            alertas.append(("medio", "A declaração de visão ainda não foi escrita.",
                            url_for("abertura", projeto_id=pid) + "#visao"))
    alertas = [{"nivel": n, "texto": t, "link": l} for n, t, l in alertas] + gerar_alertas_partes(projeto, partes)
    alertas.sort(key=lambda a: {"alto": 0, "medio": 1, "info": 2}[a["nivel"]])
    return alertas


def alertas_do_projeto(projeto, sem=None):
    """Todos os pontos de atenção do projeto, de todos os domínios, do mais grave ao informativo."""
    pid = projeto["id"]
    alertas = (gerar_alertas(projeto, listar_partes(pid), obter_abertura(pid))
               + incerteza.gerar_alertas_incerteza(projeto, incerteza.listar_riscos(projeto))
               + trabalho.gerar_alertas_trabalho(projeto) + entrega.gerar_alertas_entrega(projeto)
               + medicao.gerar_alertas_medicao(projeto, sem) + equipe.gerar_alertas_equipe(projeto)
               + ciclo.gerar_alertas_ciclo(projeto) + principios_mod.gerar_alertas_principios(projeto) + suprimentos.gerar_alertas_suprimentos(projeto))
    alertas.sort(key=lambda a: {"alto": 0, "medio": 1, "info": 2}[a["nivel"]])
    return alertas


def verificacoes_do_projeto(projeto_id):
    rows = get_db().execute("SELECT * FROM verificacao WHERE projeto_id = ?", (projeto_id,)).fetchall()
    return {(r["dominio"], r["indice"]): r for r in rows}


@functools.lru_cache(maxsize=None)
def _dicas_json(endpoint):
    """JSON das dicas da página (calculado uma vez por endpoint)."""
    return json.dumps(dicas.dicas_da_pagina(endpoint), ensure_ascii=False).replace("</", "<\\/")


def progresso_dominios(projeto_id):
    verifs = verificacoes_do_projeto(projeto_id)
    resultado = []
    for d in pmbok.DOMINIOS:
        contagem = {"atendido": 0, "parcial": 0, "nao_atendido": 0, "nao_avaliado": 0}
        for i in range(len(d["resultados"])):
            v = verifs.get((d["chave"], i))
            contagem[v["status"] if v else "nao_avaliado"] += 1
        total = len(d["resultados"])
        resultado.append({**d, "contagem": contagem, "total": total,
                          "pct": round(100 * (contagem["atendido"] + 0.5 * contagem["parcial"]) / total)})
    return resultado


def indicadores_dominio(chave, projeto, partes, abertura):
    """Evidências calculadas pelo app para apoiar a verificação de resultados."""
    ind = []
    if chave == "partes-interessadas" and partes:
        com_plano = [s for s in partes if s["lacuna"] is not None]
        no_alvo = sum(1 for s in com_plano if s["lacuna"] <= 0)
        sats = [s["ultima_satisfacao"] for s in partes if s["ultima_satisfacao"]]
        ind.append(f"{len(partes)} partes interessadas ativas; {sum(s['analisada'] for s in partes)} analisadas.")
        if com_plano:
            ind.append(f"{no_alvo} de {len(com_plano)} com engajamento atual no nível desejado ou acima.")
        if sats:
            ind.append(f"Satisfação média mais recente: {sum(sats) / len(sats):.1f}/5 ({len(sats)} partes avaliadas).")
        opos = [s["nome"] for s in partes if s["atitude"] == "opositor"]
        if opos:
            ind.append("Opositoras: " + ", ".join(opos) + ".")
        por_parte = trabalho.mudancas_por_parte(projeto["id"])
        if por_parte:
            ind.append("Mudanças solicitadas por parte interessada (muitas podem indicar desalinhamento com os objetivos): "
                       + ", ".join(f"{r['nome']} ({r['n']})" for r in por_parte) + ".")
    elif chave == "abordagem":
        nomes = dict(pmbok.ABORDAGENS)
        ind.append("Abordagem: " + (nomes.get(projeto["abordagem"]) or "não definida") + ".")
        ind.append("Cadência: " + (dict(pmbok.CADENCIAS).get(projeto["cadencia"]) or "não definida") + ".")
        fatores = json.loads(projeto["fatores_json"] or "{}")
        ind.append(f"Fatores de seleção avaliados: {len(fatores)} de {len(pmbok.FATORES_ABORDAGEM)}.")
        fases = ciclo.listar_fases(projeto["id"])
        if fases:
            ind.append(f"Ciclo de vida: {len(fases)} fases, {sum(1 for f in fases if f['status'] == 'concluida')} concluídas com revisão de fase; "
                       f"{sum(1 for f in fases if not f['criterios'])} sem critérios de saída.")
        n_dec = get_db().execute("SELECT COUNT(*) FROM decisao_tailoring WHERE projeto_id = ?", (projeto["id"],)).fetchone()[0]
        ind.append(f"{n_dec} decisão(ões) de tailoring registradas.")
    elif chave == "equipe":
        ind.extend(equipe.indicadores(projeto))
    elif chave == "medicao":
        ind.extend(medicao.indicadores_dominio(projeto))
    elif chave == "entrega":
        ind.extend(entrega.indicadores(projeto))
    elif chave == "trabalho":
        ind.extend(trabalho.indicadores(projeto))
        ind.extend(suprimentos.indicadores(projeto))
    elif chave == "incerteza":
        ind.extend(incerteza.indicadores(projeto))
    elif chave == "planejamento" and abertura is not None:
        status = {"rascunho": "rascunho", "em_revisao": "em revisão", "aprovado": "aprovado"}
        preenchidos = sum(1 for c in CAMPOS_TERMO_ESSENCIAIS if abertura[c])
        ind.append(f"Termo de abertura: {status.get(abertura['status'], abertura['status'])}; {preenchidos} de {len(CAMPOS_TERMO_ESSENCIAIS)} campos essenciais preenchidos.")
        ind.append("Declaração de visão: " + ("escrita." if abertura["visao_texto"] else "não escrita."))
    return ind


# --------------------------------------------------------------------------
# Rotas
# --------------------------------------------------------------------------
def registrar_rotas(app):

    @app.route("/")
    def inicio():
        db = get_db()
        onde, args = filtro_projetos()
        projetos = db.execute(
            f"""SELECT p.*, (SELECT COUNT(*) FROM parte_interessada s WHERE s.projeto_id = p.id AND s.ativa = 1) AS n_partes
               FROM projeto p WHERE {onde} ORDER BY p.atualizado_em DESC""", args
        ).fetchall()
        return render_template("inicio.html", projetos=projetos)

    @app.route("/exemplo", methods=["POST"])
    def criar_exemplo():
        db = get_db()
        existente = db.execute("SELECT id FROM projeto WHERE nome LIKE '%AgendaFácil%' ORDER BY id LIMIT 1").fetchone()
        if existente:
            pid = existente["id"]
        else:
            import exemplo
            pid = exemplo.criar(current_app._get_current_object())
        if g.get("usuario") is not None and not g.usuario["admin"]:  # quem pediu passa a ver o exemplo
            db.execute("INSERT OR IGNORE INTO usuario_projeto (usuario_id, projeto_id) VALUES (?, ?)", (g.usuario["id"], pid))
            db.commit()
        if existente:
            return redirect(url_for("fluxo", projeto_id=pid))
        flash("Projeto de exemplo criado. Explore à vontade: ele mostra cada tela preenchida.", "ok")
        return redirect(url_for("fluxo", projeto_id=pid))

    @app.route("/backup")
    def backup():
        """Cópia consistente do banco (API de backup do SQLite) para download. Só administradores."""
        auth.exigir_admin()
        fd, caminho = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        destino = sqlite3.connect(caminho)
        with destino:
            get_db().backup(destino)
        destino.close()
        nome = f"gestor-pmbok7-backup-{datetime.now():%Y-%m-%d-%H%M}.db"
        resposta = send_file(caminho, as_attachment=True, download_name=nome, mimetype="application/x-sqlite3")
        resposta.call_on_close(lambda: os.remove(caminho))
        return resposta

    @app.route("/principios")
    def principios():
        return render_template("principios.html")

    # ---------------- Projetos ----------------
    @app.route("/projetos/novo", methods=["GET", "POST"])
    def projeto_novo():
        if request.method == "POST":
            nome = request.form.get("nome", "").strip()
            if not nome:
                flash("Informe o nome do projeto.", "erro")
                return render_template("projeto_form.html", novo=True, modelos=pmo.MODELOS)
            db = get_db()
            cur = db.execute(
                "INSERT INTO projeto (nome, descricao, cadencia) VALUES (?, ?, ?)",
                (nome, request.form.get("descricao", "").strip(), request.form.get("cadencia") or None),
            )
            db.execute("INSERT INTO abertura (projeto_id) VALUES (?)", (cur.lastrowid,))
            pmo.aplicar_modelo(db, cur.lastrowid, request.form.get("modelo", ""))
            if g.get("usuario") is not None and not g.usuario["admin"]:
                db.execute("INSERT OR IGNORE INTO usuario_projeto (usuario_id, projeto_id) VALUES (?, ?)", (g.usuario["id"], cur.lastrowid))
            db.commit()
            flash("Projeto criado! Este é o fluxo do projeto: siga as etapas na ordem, começando por “Como vamos trabalhar”.", "ok")
            return redirect(url_for("fluxo", projeto_id=cur.lastrowid))
        return render_template("projeto_form.html", novo=True, modelos=pmo.MODELOS)

    @app.route("/p/<int:projeto_id>")
    def projeto(projeto_id):
        p = obter_projeto(projeto_id)
        partes = listar_partes(projeto_id)
        ab = obter_abertura(projeto_id)
        riscos = incerteza.listar_riscos(p)
        sem = medicao.semaforo(p)
        _fases = guia.fluxo_do_projeto(p, partes, ab)
        alertas = alertas_do_projeto(p, sem)
        # Painéis completos aparecem quando o básico da fase Iniciar está preenchido (o termo pode ainda estar em revisão).
        iniciado = bool(p["abordagem"] and ab["proposito"] and ab["objetivos"] and partes)
        if not iniciado:
            # Projeto recém-criado: a lista dos 12 princípios "fracos" só assusta; ela volta depois da fase Iniciar.
            alertas = [a for a in alertas if not a["texto"].startswith("Princípios com pouca evidência")]
        return render_template(
            "projeto.html", projeto=p, partes=partes, abertura=ab, semaforo=sem,
            fluxo=resumo_fluxo(partes), alertas=alertas, resumo_riscos=incerteza.resumo_riscos(p, riscos),
            resumo_trabalho=trabalho.resumo_trabalho(p), resumo_entrega=entrega.resumo_entrega(p),
            dominios=progresso_dominios(projeto_id), principios=principios_mod.avaliar_principios(p), secao="visao",
            fases=_fases, iniciado=iniciado,
        )

    @app.route("/p/<int:projeto_id>/fluxo")
    def fluxo(projeto_id):
        p = obter_projeto(projeto_id)
        partes = listar_partes(projeto_id)
        return render_template("fluxo.html", projeto=p, fases=guia.fluxo_do_projeto(p, partes, obter_abertura(projeto_id)), secao="fluxo")

    @app.route("/p/<int:projeto_id>/glossario")
    def glossario(projeto_id):
        return render_template("glossario.html", projeto=obter_projeto(projeto_id), termos=sorted(guia.GLOSSARIO, key=lambda t: t[0].lower()), secao="glossario")

    @app.route("/p/<int:projeto_id>/editar", methods=["GET", "POST"])
    def projeto_editar(projeto_id):
        p = obter_projeto(projeto_id)
        if request.method == "POST":
            nome = request.form.get("nome", "").strip()
            if not nome:
                flash("Informe o nome do projeto.", "erro")
                return render_template("projeto_form.html", projeto=p, novo=False, p=p, secao="visao")
            db = get_db()
            db.execute(
                "UPDATE projeto SET nome = ?, descricao = ?, cadencia = ?, atualizado_em = datetime('now','localtime') WHERE id = ?",
                (nome, request.form.get("descricao", "").strip(), request.form.get("cadencia") or None, projeto_id),
            )
            if request.form.get("acesso_enviado") and g.get("usuario") is not None and g.usuario["admin"]:
                db.execute("DELETE FROM usuario_projeto WHERE projeto_id = ?", (projeto_id,))
                for uid in request.form.getlist("acesso"):
                    if uid.isdigit():
                        db.execute("INSERT OR IGNORE INTO usuario_projeto (usuario_id, projeto_id) SELECT id, ? FROM usuario WHERE id = ? AND admin = 0",
                                   (projeto_id, int(uid)))
            db.commit()
            flash("Projeto atualizado.", "ok")
            return redirect(url_for("projeto", projeto_id=projeto_id))
        usuarios = get_db().execute("""SELECT u.*, EXISTS(SELECT 1 FROM usuario_projeto x WHERE x.usuario_id = u.id AND x.projeto_id = ?) AS tem
                                       FROM usuario u WHERE u.ativo = 1 AND u.admin = 0 ORDER BY u.nome""", (projeto_id,)).fetchall()
        return render_template("projeto_form.html", projeto=p, novo=False, p=p, secao="visao", usuarios=usuarios)

    @app.route("/p/<int:projeto_id>/excluir", methods=["POST"])
    def projeto_excluir(projeto_id):
        obter_projeto(projeto_id)
        auth.exigir_admin()
        if request.form.get("confirmar") != "sim":
            flash("Marque a confirmação para excluir o projeto.", "erro")
            return redirect(url_for("projeto_editar", projeto_id=projeto_id))
        db = get_db()
        db.execute("DELETE FROM projeto WHERE id = ?", (projeto_id,))
        db.commit()
        flash("Projeto excluído. Um administrador pode restaurá-lo em Dados → Lixeira.", "ok")
        return redirect(url_for("inicio"))

    # ---------------- Abordagem (domínio 2.3 + tailoring) ----------------
    @app.route("/p/<int:projeto_id>/abordagem", methods=["GET", "POST"])
    def abordagem(projeto_id):
        p = obter_projeto(projeto_id)
        respostas = json.loads(p["fatores_json"] or "{}")
        if request.method == "POST":
            respostas = {}
            for chave, *_ in pmbok.FATORES_ABORDAGEM:
                v = inteiro(request.form.get(chave))
                if v:
                    respostas[chave] = v
            escolha = request.form.get("abordagem") or None
            if escolha not in dict(pmbok.ABORDAGENS):
                escolha = None
            db = get_db()
            db.execute(
                """UPDATE projeto SET fatores_json = ?, abordagem = ?, abordagem_justificativa = ?, cadencia = ?,
                   atualizado_em = datetime('now','localtime') WHERE id = ?""",
                (json.dumps(respostas), escolha, request.form.get("justificativa", "").strip(),
                 request.form.get("cadencia") or None, projeto_id),
            )
            db.commit()
            if request.form.get("acao") == "calcular":
                flash("Sugestão recalculada. Revise e confirme a abordagem.", "ok")
                return redirect(url_for("abordagem", projeto_id=projeto_id) + "#decisao")
            flash("Abordagem salva." if escolha else "Respostas salvas. Escolha uma abordagem para concluir.", "ok")
            return redirect(url_for("projeto", projeto_id=projeto_id) if escolha else url_for("abordagem", projeto_id=projeto_id))
        media, sugestao, medias_cat = pmbok.recomendar_abordagem(respostas)
        return render_template(
            "abordagem.html", projeto=p, respostas=respostas, media=media,
            sugestao=sugestao, medias_cat=medias_cat, secao="abordagem", sub="abordagem",
        )

    # ---------------- Abertura (termo + visão) ----------------
    @app.route("/p/<int:projeto_id>/abertura", methods=["GET", "POST"])
    def abertura(projeto_id):
        p = obter_projeto(projeto_id)
        ab = obter_abertura(projeto_id)
        if request.method == "POST":
            valores = {c: request.form.get(c, "").strip() for c in CAMPOS_ABERTURA}
            if valores["status"] not in ("rascunho", "em_revisao", "aprovado"):
                valores["status"] = "rascunho"
            exigencia = pmo.exigir("abertura", valores) if valores["status"] != "rascunho" else None
            if exigencia:  # salva o que foi digitado, mas como rascunho
                flash(exigencia + " O termo foi salvo como rascunho.", "erro")
                valores["status"] = "rascunho"
            if valores["status"] == "aprovado":
                faltando = [c for c in CAMPOS_TERMO_ESSENCIAIS if not valores[c]] + ([] if valores["aprovado_por"] else ["aprovado_por"])
                if faltando:
                    flash("Para aprovar, preencha propósito, objetivos, critérios de sucesso, patrocinador, gerente e quem aprovou.", "erro")
                    valores["status"] = ab["status"] if ab["status"] != "aprovado" else "em_revisao"
                elif not valores["aprovado_em"]:
                    valores["aprovado_em"] = date.today().isoformat()
            campos_termo = [c for c in CAMPOS_ABERTURA if not c.startswith("visao_") and c not in ("status", "aprovado_por", "aprovado_em")]
            if ab["status"] == "aprovado" and valores["status"] == "aprovado" and any(valores[c] != (ab[c] or "") for c in campos_termo):
                flash("O termo de abertura já estava aprovado e foi alterado. Registre a alteração no registro de mudanças "
                      "para que ela passe pela decisão do patrocinador.", "aviso")
            if request.form.get("gerar_visao") == "1" or (not valores["visao_texto"] and all(valores[c] for c in CAMPOS_VISAO)):
                valores["visao_texto"] = montar_visao(valores)
            db = get_db()
            db.execute(
                "UPDATE abertura SET " + ", ".join(f"{c} = ?" for c in CAMPOS_ABERTURA)
                + ", atualizado_em = datetime('now','localtime') WHERE projeto_id = ?",
                [valores[c] for c in CAMPOS_ABERTURA] + [projeto_id],
            )
            tocar_projeto(projeto_id)
            db.commit()
            flash("Abertura salva.", "ok")
            ancora = "#visao" if request.form.get("gerar_visao") == "1" else ""
            return redirect(url_for("abertura", projeto_id=projeto_id) + ancora)
        return render_template("abertura.html", projeto=p, ab=ab, secao="abertura",
                               essenciais=CAMPOS_TERMO_ESSENCIAIS)

    rotas_partes.registrar(app)

    # ---------------- Domínios de desempenho ----------------
    @app.route("/p/<int:projeto_id>/dominios")
    def dominios(projeto_id):
        p = obter_projeto(projeto_id)
        return render_template("dominios.html", projeto=p, dominios=progresso_dominios(projeto_id), secao="dominios")

    @app.route("/p/<int:projeto_id>/dominios/<chave>", methods=["GET", "POST"])
    def dominio(projeto_id, chave):
        p = obter_projeto(projeto_id)
        d = pmbok.DOMINIOS_POR_CHAVE.get(chave)
        if d is None:
            abort(404)
        db = get_db()
        if request.method == "POST":
            validos = dict(pmbok.STATUS_VERIFICACAO)
            for i in range(len(d["resultados"])):
                status = request.form.get(f"status_{i}", "nao_avaliado")
                if status not in validos:
                    status = "nao_avaliado"
                db.execute(
                    """INSERT INTO verificacao (projeto_id, dominio, indice, status, evidencia, atualizado_em)
                       VALUES (?, ?, ?, ?, ?, datetime('now','localtime'))
                       ON CONFLICT(projeto_id, dominio, indice) DO UPDATE SET
                       status = excluded.status, evidencia = excluded.evidencia, atualizado_em = excluded.atualizado_em""",
                    (projeto_id, chave, i, status, request.form.get(f"evidencia_{i}", "").strip()),
                )
            tocar_projeto(projeto_id)
            db.commit()
            flash(f"Verificação do domínio {d['nome']} salva.", "ok")
            return redirect(url_for("dominio", projeto_id=projeto_id, chave=chave))
        verifs = verificacoes_do_projeto(projeto_id)
        itens = []
        for i, (resultado, verificacao) in enumerate(d["resultados"]):
            v = verifs.get((chave, i))
            itens.append({"i": i, "resultado": resultado, "verificacao": verificacao,
                          "status": v["status"] if v else "nao_avaliado",
                          "evidencia": v["evidencia"] if v else "",
                          "atualizado_em": v["atualizado_em"] if v else None})
        partes = listar_partes(projeto_id)
        ab = obter_abertura(projeto_id)
        return render_template("dominio.html", projeto=p, d=d, itens=itens, secao="dominios",
                               indicadores=indicadores_dominio(chave, p, partes, ab))

    @app.errorhandler(404)
    def nao_encontrado(_e):
        return render_template("erro.html", mensagem="Página não encontrada."), 404

    @app.errorhandler(403)
    def proibido(_e):
        return render_template("erro.html", mensagem="Você não tem permissão para esta ação. Fale com um administrador."), 403

    @app.errorhandler(413)
    def grande_demais(_e):
        return render_template("erro.html", mensagem="O conteúdo enviado é grande demais."), 413

    @app.errorhandler(500)
    def erro_interno(_e):
        return render_template("erro.html", mensagem="Algo deu errado. Nenhum dado foi perdido: tente de novo e, se continuar, avise o administrador."), 500

    ultimo_teste_backup = {"t": 0.0}

    @app.before_request
    def backup_diario():
        """Backup automático: confere no máximo uma vez por hora se o do dia já foi feito."""
        import time as _t
        if not app.config.get("BACKUP_AUTOMATICO") or request.endpoint == "static":
            return None
        if _t.time() - ultimo_teste_backup["t"] < 3600:
            return None
        ultimo_teste_backup["t"] = _t.time()
        try:
            backups_mod.automatico_se_preciso(app.config["DATABASE"])
        except Exception as e:  # backup nunca derruba o app; o erro fica no log do servidor
            app.logger.error("Falha no backup automático: %s", e)
        return None


def ler_form_parte():
    f = request.form
    atitude = f.get("atitude", "desconhecida")
    return {
        "nome": f.get("nome", "").strip(),
        "papel": f.get("papel", "").strip(),
        "organizacao": f.get("organizacao", "").strip(),
        "categoria": f.get("categoria", ""),
        "interna": 1 if f.get("interna") == "1" else 0,
        "contato": f.get("contato", "").strip(),
        "ativa": 1 if f.get("ativa") else 0,
        "poder": inteiro(f.get("poder")),
        "interesse": inteiro(f.get("interesse")),
        "influencia": inteiro(f.get("influencia")),
        "impacto": inteiro(f.get("impacto")),
        "atitude": atitude if atitude in dict(pmbok.ATITUDES) else "desconhecida",
        "proximidade": f.get("proximidade", ""),
        "crencas": f.get("crencas", "").strip(),
        "expectativas": f.get("expectativas", "").strip(),
        "sal_poder": 1 if f.get("sal_poder") else 0,
        "sal_legitimidade": 1 if f.get("sal_legitimidade") else 0,
        "sal_urgencia": 1 if f.get("sal_urgencia") else 0,
        "engajamento_atual": inteiro(f.get("engajamento_atual")),
        "engajamento_desejado": inteiro(f.get("engajamento_desejado")),
        "metodo_comunicacao": f.get("metodo_comunicacao", ""),
        "tipo_comunicacao": f.get("tipo_comunicacao", ""),
        "frequencia": f.get("frequencia", ""),
        "estrategia": f.get("estrategia", "").strip(),
    }


def registrar_interacao(projeto_id, parte_id):
    obter_parte(projeto_id, parte_id)
    f = request.form
    data = f.get("data") or date.today().isoformat()
    try:
        quando = date.fromisoformat(data)
    except ValueError:
        quando = date.today()
    if quando > date.today():
        flash("A data da interação não pode estar no futuro: o monitoramento registra o que já aconteceu.", "erro")
        return
    data = quando.isoformat()
    db = get_db()
    db.execute(
        "INSERT INTO interacao (parte_id, data, metodo, tipo, resumo, feedback, satisfacao) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (parte_id, data, f.get("metodo", ""), f.get("tipo", ""), f.get("resumo", "").strip(),
         f.get("feedback", "").strip(), inteiro(f.get("satisfacao"))),
    )
    tocar_projeto(projeto_id)
    db.commit()
    flash("Interação registrada.", "ok")


def montar_visao(v):
    """Modelo de declaração de visão (formato 'elevator pitch' de G. Moore — fonte complementar)."""
    partes = [
        f"Para {v['visao_publico']}" if v["visao_publico"] else "",
        f"que {v['visao_necessidade']}," if v["visao_necessidade"] else "",
        f"o {v['visao_produto']}" if v["visao_produto"] else "",
        f"é um(a) {v['visao_categoria']}" if v["visao_categoria"] else "",
        f"que {v['visao_beneficio']}." if v["visao_beneficio"] else "",
        f"Em comparação com {v['visao_alternativa']}," if v["visao_alternativa"] else "",
        f"nosso produto {v['visao_diferencial']}." if v["visao_diferencial"] else "",
    ]
    return " ".join(x for x in partes if x).strip()


def abrir_navegador(endereco):
    """Abre o navegador definido em NAVEGADOR (caminho do executável) ou, se não houver, o navegador padrão."""
    navegador = os.environ.get("NAVEGADOR")
    if navegador and os.path.exists(navegador):
        subprocess.Popen([navegador, endereco])
    else:
        webbrowser.open(endereco)


def principal():
    """Inicia o servidor local e abre o navegador (desligue com SEM_NAVEGADOR=1)."""
    porta = int(os.environ.get("PORTA", "5000"))
    endereco = f"http://localhost:{porta}"
    import socket
    with socket.socket() as teste:
        if teste.connect_ex(("127.0.0.1", porta)) == 0:
            print(f"A porta {porta} já está em uso: o app provavelmente já está aberto em {endereco}.")
            print("Para usar outra porta: defina PORTA=5001 antes de iniciar.")
            if not os.environ.get("SEM_NAVEGADOR"):
                abrir_navegador(endereco)
            sys.exit(0)
    debug = os.environ.get("FLASK_DEBUG") == "1"
    print(f"\nOctante rodando em {endereco}  (Ctrl+C para parar)\n")
    if not os.environ.get("SEM_NAVEGADOR") and not (debug and os.environ.get("WERKZEUG_RUN_MAIN")):
        threading.Timer(1.2, abrir_navegador, args=[endereco]).start()
    # Depurador desligado por padrão; para ativar: FLASK_DEBUG=1 python app.py
    create_app().run(host="127.0.0.1", port=porta, debug=debug)


if __name__ == "__main__":
    principal()
