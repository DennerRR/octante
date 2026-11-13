"""Telas de segurança dos dados (v13): histórico, lixeira, backups e anonimização (LGPD)."""
import os
import tempfile

from flask import Blueprint, abort, current_app, flash, redirect, render_template, request, send_file, url_for

import auditoria
import auth
import backup
from db import VERSAO_ATUAL, get_db, migrar
from util import obter_projeto

bp = Blueprint("dados", __name__)


@bp.route("/p/<int:projeto_id>/historico")
def historico(projeto_id):
    p = obter_projeto(projeto_id)
    tipo = request.args.get("tipo", "")
    sql, args = "SELECT * FROM auditoria WHERE projeto_id = ?", [projeto_id]
    if tipo in auditoria.NOMES:
        sql += " AND tabela = ?"
        args.append(tipo)
    linhas = get_db().execute(sql + " ORDER BY id DESC LIMIT 300", args).fetchall()
    tipos = [r[0] for r in get_db().execute("SELECT DISTINCT tabela FROM auditoria WHERE projeto_id = ?", (projeto_id,))]
    return render_template("historico.html", projeto=p, eventos=[auditoria.descrever(l) for l in linhas],
                           tipos=sorted((t, auditoria.NOMES.get(t, t)) for t in tipos), tipo=tipo, secao="historico")


@bp.route("/admin/dados", methods=["GET", "POST"])
def painel():
    auth.exigir_admin()
    db = get_db()
    banco = current_app.config["DATABASE"]
    if request.method == "POST":
        acao = request.form.get("acao")
        try:
            if acao == "backup_agora":
                feito = backup.fazer(banco, "manual", conn=db)
                flash("Backup criado e verificado." if feito else "Ainda não há dados para copiar.", "ok")
            elif acao == "restaurar_lote":
                r, i = auditoria.restaurar_lote(db, request.form.get("lote", ""))
                flash(f"{r} registro(s) restaurado(s)." + (f" {i} ignorado(s) porque já existiam." if i else ""), "ok")
            elif acao == "restaurar_registro":
                r, i = auditoria.restaurar_registro(db, request.form.get("auditoria_id", type=int))
                flash("Registro restaurado." if r else "Não foi possível restaurar: o registro já existe.", "ok" if r else "erro")
            elif acao == "restaurar_backup":
                origem = backup.caminho_seguro(banco, request.form.get("nome"))
                if not origem:
                    abort(404)
                _restaurar(banco, origem)
            elif acao == "enviar_backup":
                arquivo = request.files.get("arquivo")
                if not arquivo or not arquivo.filename:
                    flash("Escolha o arquivo .db do backup.", "erro")
                else:
                    fd, tmp = tempfile.mkstemp(suffix=".db")
                    os.close(fd)
                    try:
                        arquivo.save(tmp)
                        _restaurar(banco, tmp)
                    finally:
                        os.remove(tmp)
        except ValueError as e:
            try:
                db.rollback()
            except Exception:  # a conexão pode ter sido fechada para restaurar
                pass
            flash(str(e), "erro")
        return redirect(url_for("dados.painel"))
    lixeira = db.execute(
        """SELECT a.*, (SELECT COUNT(*) FROM auditoria b WHERE b.lote = a.lote AND b.acao = 'D') AS n
           FROM auditoria a WHERE a.acao = 'D' AND a.tabela = 'projeto' ORDER BY a.id DESC LIMIT 50""").fetchall()
    avulsos = db.execute(
        """SELECT * FROM auditoria a WHERE a.acao = 'D' AND a.tabela NOT IN ('projeto', 'usuario')
           AND NOT EXISTS (SELECT 1 FROM auditoria p WHERE p.lote = a.lote AND p.acao = 'D' AND p.tabela = 'projeto')
           ORDER BY a.id DESC LIMIT 60""").fetchall()
    return render_template("dados.html", backups=backup.listar(banco),
                           projetos_excluidos=[{**auditoria.descrever(l), "n": l["n"]} for l in lixeira],
                           registros_excluidos=[auditoria.descrever(l) for l in avulsos])


def _restaurar(banco, origem):
    from flask import g
    ok, msg, _ = backup.verificar(origem, VERSAO_ATUAL)
    if not ok:
        raise ValueError(msg)
    db = g.pop("db", None)
    if db is not None:
        db.close()
    info = backup.restaurar(banco, origem, VERSAO_ATUAL, migrar)
    flash(f"Backup restaurado ({info['projetos']} projeto(s)). Uma cópia do estado anterior foi guardada em “antes de restaurar”.", "ok")


@bp.route("/admin/dados/backup/<nome>")
def baixar_backup(nome):
    auth.exigir_admin()
    cam = backup.caminho_seguro(current_app.config["DATABASE"], nome)
    if not cam:
        abort(404)
    return send_file(cam, as_attachment=True, download_name=nome, mimetype="application/x-sqlite3")


@bp.route("/p/<int:projeto_id>/anonimizar", methods=["POST"])
def anonimizar(projeto_id):
    """LGPD: apaga contatos e opiniões pessoais das partes interessadas de um projeto encerrado."""
    auth.exigir_admin()
    p = obter_projeto(projeto_id)
    if p["situacao"] == "ativo":
        flash("Só projetos encerrados ou cancelados podem ser anonimizados.", "erro")
    else:
        db = get_db()
        n = db.execute("""UPDATE parte_interessada SET contato = '', crencas = '', expectativas = ''
                          WHERE projeto_id = ? AND (contato != '' OR crencas != '' OR expectativas != '')""", (projeto_id,)).rowcount
        db.commit()
        flash(f"Dados pessoais de {n} parte(s) interessada(s) apagados (contato, crenças e expectativas).", "ok")
    return redirect(url_for("ciclo.encerramento", projeto_id=projeto_id))
