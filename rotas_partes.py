"""Rotas das partes interessadas (domínio 2.1), separadas do app.py na v14. Os nomes das rotas não mudaram."""


def registrar(app):
    from app import (DIAS_SEM_INTERACAO, abort, chave_prioridade, datetime, flash, gerar_alertas, get_db, incerteza, inteiro, ler_form_parte, listar_partes, obter_abertura, obter_parte, obter_projeto, ordem_sugerida, pmbok, pmo, pontos_grade, redirect, registrar_interacao, render_template, request, resumo_fluxo, tocar_projeto, url_for)  # noqa: F401  (importado na hora do registro: evita import circular)

    # ---------------- Partes interessadas ----------------
    @app.route("/p/<int:projeto_id>/partes")
    def partes_registro(projeto_id):
        p = obter_projeto(projeto_id)
        partes = listar_partes(projeto_id, incluir_inativas=True)
        return render_template("partes_registro.html", projeto=p, partes=partes,
                               fluxo=resumo_fluxo([s for s in partes if s["ativa"]]),
                               etapa="identificar", secao="partes")

    @app.route("/p/<int:projeto_id>/partes/nova", methods=["GET", "POST"])
    def parte_nova(projeto_id):
        p = obter_projeto(projeto_id)
        if request.method == "POST":
            dados = ler_form_parte()
            db = get_db()
            erro = None if dados["nome"] else "Informe o nome da parte interessada."
            erro = erro or pmo.exigir("parte", dados)
            if not erro and db.execute("SELECT 1 FROM parte_interessada WHERE projeto_id = ? AND lower(nome) = lower(?)",
                                       (projeto_id, dados["nome"])).fetchone():
                erro = f"“{dados['nome']}” já está no registro. Edite a parte existente em vez de cadastrar de novo."
            if erro:
                flash(erro, "erro")
                return render_template("parte_form.html", projeto=p, s=dados, novo=True, secao="partes")
            cols = list(dados.keys())
            cur = db.execute(
                f"INSERT INTO parte_interessada (projeto_id, {', '.join(cols)}) VALUES (?, {', '.join('?' for _ in cols)})",
                [projeto_id] + [dados[c] for c in cols],
            )
            if dados["engajamento_atual"]:
                db.execute("INSERT INTO historico_engajamento (parte_id, nivel_anterior, nivel_novo) VALUES (?, NULL, ?)",
                           (cur.lastrowid, dados["engajamento_atual"]))
            tocar_projeto(projeto_id)
            db.commit()
            flash(f"{dados['nome']} adicionada ao registro.", "ok")
            if request.form.get("acao") == "outra":
                return redirect(url_for("parte_nova", projeto_id=projeto_id))
            return redirect(url_for("parte_detalhe", projeto_id=projeto_id, parte_id=cur.lastrowid))
        return render_template("parte_form.html", projeto=p, s={"interna": 1, "ativa": 1, "atitude": "desconhecida"},
                               novo=True, secao="partes")

    @app.route("/p/<int:projeto_id>/partes/<int:parte_id>")
    def parte_detalhe(projeto_id, parte_id):
        p = obter_projeto(projeto_id)
        obter_parte(projeto_id, parte_id)
        partes = listar_partes(projeto_id, incluir_inativas=True)
        s = next(x for x in partes if x["id"] == parte_id)
        db = get_db()
        interacoes = db.execute("SELECT * FROM interacao WHERE parte_id = ? ORDER BY data DESC, id DESC", (parte_id,)).fetchall()
        historico = db.execute("SELECT * FROM historico_engajamento WHERE parte_id = ? ORDER BY data DESC, id DESC", (parte_id,)).fetchall()
        riscos = [r for r in incerteza.listar_riscos(p) if r["parte_id"] == parte_id]
        return render_template("parte_detalhe.html", projeto=p, s=s, interacoes=interacoes,
                               historico=historico, riscos=riscos, secao="partes")

    @app.route("/p/<int:projeto_id>/partes/<int:parte_id>/editar", methods=["GET", "POST"])
    def parte_editar(projeto_id, parte_id):
        p = obter_projeto(projeto_id)
        atual = obter_parte(projeto_id, parte_id)
        if request.method == "POST":
            dados = ler_form_parte()
            erro_p = "Informe o nome da parte interessada." if not dados["nome"] else pmo.exigir("parte", dados)
            if erro_p:
                flash(erro_p, "erro")
                return render_template("parte_form.html", projeto=p, s={**dados, "id": parte_id}, novo=False, secao="partes")
            db = get_db()
            db.execute(
                "UPDATE parte_interessada SET " + ", ".join(f"{c} = ?" for c in dados)
                + ", atualizado_em = datetime('now','localtime') WHERE id = ?",
                list(dados.values()) + [parte_id],
            )
            if dados["engajamento_atual"] != atual["engajamento_atual"] and dados["engajamento_atual"]:
                db.execute("INSERT INTO historico_engajamento (parte_id, nivel_anterior, nivel_novo) VALUES (?, ?, ?)",
                           (parte_id, atual["engajamento_atual"], dados["engajamento_atual"]))
            tocar_projeto(projeto_id)
            db.commit()
            flash("Parte interessada atualizada.", "ok")
            return redirect(url_for("parte_detalhe", projeto_id=projeto_id, parte_id=parte_id))
        return render_template("parte_form.html", projeto=p, s=atual, novo=False, secao="partes")

    @app.route("/p/<int:projeto_id>/partes/<int:parte_id>/excluir", methods=["POST"])
    def parte_excluir(projeto_id, parte_id):
        s = obter_parte(projeto_id, parte_id)
        db = get_db()
        db.execute("DELETE FROM parte_interessada WHERE id = ?", (parte_id,))
        tocar_projeto(projeto_id)
        db.commit()
        flash(f"{s['nome']} removida do registro.", "ok")
        return redirect(url_for("partes_registro", projeto_id=projeto_id))

    @app.route("/p/<int:projeto_id>/partes/analise", methods=["GET", "POST"])
    def partes_analise(projeto_id):
        p = obter_projeto(projeto_id)
        if request.method == "POST":
            db = get_db()
            for s in listar_partes(projeto_id):
                sid = s["id"]
                if f"poder_{sid}" not in request.form:
                    continue
                atitude = request.form.get(f"atitude_{sid}")
                db.execute(
                    """UPDATE parte_interessada SET poder = ?, interesse = ?, influencia = ?, impacto = ?, atitude = ?,
                       sal_poder = ?, sal_legitimidade = ?, sal_urgencia = ?, atualizado_em = datetime('now','localtime')
                       WHERE id = ? AND projeto_id = ?""",
                    (inteiro(request.form.get(f"poder_{sid}")), inteiro(request.form.get(f"interesse_{sid}")),
                     inteiro(request.form.get(f"influencia_{sid}")), inteiro(request.form.get(f"impacto_{sid}")),
                     atitude if atitude in dict(pmbok.ATITUDES) else "desconhecida",
                     1 if request.form.get(f"sal_poder_{sid}") else 0,
                     1 if request.form.get(f"sal_legitimidade_{sid}") else 0,
                     1 if request.form.get(f"sal_urgencia_{sid}") else 0, sid, projeto_id),
                )
            tocar_projeto(projeto_id)
            db.commit()
            flash("Análise salva.", "ok")
            return redirect(url_for("partes_analise", projeto_id=projeto_id))
        partes = listar_partes(projeto_id)
        return render_template("partes_analise.html", projeto=p, partes=partes, fluxo=resumo_fluxo(partes),
                               etapa="analisar", secao="partes")

    @app.route("/p/<int:projeto_id>/partes/priorizacao", methods=["GET", "POST"])
    def partes_priorizacao(projeto_id):
        p = obter_projeto(projeto_id)
        partes = listar_partes(projeto_id)
        if request.method == "POST":
            db = get_db()
            acao = request.form.get("acao")
            if acao == "sugerida":
                ordem = [s["id"] for s in ordem_sugerida(partes)]
            elif acao == "limpar":
                ordem = None
            else:
                pares = []
                for s in partes:
                    v = inteiro(request.form.get(f"ordem_{s['id']}"), 1, 10**6)
                    pares.append((v if v is not None else 10**6, chave_prioridade(s), s["id"]))
                ordem = [sid for *_, sid in sorted(pares)]
            if ordem is None:
                db.execute("UPDATE parte_interessada SET prioridade_manual = NULL WHERE projeto_id = ?", (projeto_id,))
                flash("Priorização removida.", "ok")
            else:
                for pos, sid in enumerate(ordem, start=1):
                    db.execute("UPDATE parte_interessada SET prioridade_manual = ? WHERE id = ? AND projeto_id = ?",
                               (pos, sid, projeto_id))
                flash("Priorização confirmada.", "ok")
            tocar_projeto(projeto_id)
            db.commit()
            return redirect(url_for("partes_priorizacao", projeto_id=projeto_id))
        return render_template("partes_priorizacao.html", projeto=p, partes=partes, fluxo=resumo_fluxo(partes),
                               sugerida=ordem_sugerida(partes), pontos=pontos_grade(partes), etapa="priorizar", secao="partes")

    @app.route("/p/<int:projeto_id>/partes/engajamento", methods=["GET", "POST"])
    def partes_engajamento(projeto_id):
        p = obter_projeto(projeto_id)
        if request.method == "POST":
            db = get_db()
            for s in listar_partes(projeto_id):
                sid = s["id"]
                if f"atual_{sid}" not in request.form:
                    continue
                novo_atual = inteiro(request.form.get(f"atual_{sid}"))
                db.execute(
                    """UPDATE parte_interessada SET engajamento_atual = ?, engajamento_desejado = ?, metodo_comunicacao = ?,
                       tipo_comunicacao = ?, frequencia = ?, estrategia = ?, info_necessaria = ?, info_responsavel = ?,
                       atualizado_em = datetime('now','localtime')
                       WHERE id = ? AND projeto_id = ?""",
                    (novo_atual, inteiro(request.form.get(f"desejado_{sid}")),
                     request.form.get(f"metodo_{sid}", ""), request.form.get(f"tipo_{sid}", ""),
                     request.form.get(f"frequencia_{sid}", ""), request.form.get(f"estrategia_{sid}", "").strip(),
                     request.form.get(f"info_{sid}", "").strip(), request.form.get(f"quem_{sid}", "").strip(),
                     sid, projeto_id),
                )
                if novo_atual and novo_atual != s["engajamento_atual"]:
                    db.execute("INSERT INTO historico_engajamento (parte_id, nivel_anterior, nivel_novo) VALUES (?, ?, ?)",
                               (sid, s["engajamento_atual"], novo_atual))
            tocar_projeto(projeto_id)
            db.commit()
            flash("Plano de engajamento salvo.", "ok")
            return redirect(url_for("partes_engajamento", projeto_id=projeto_id))
        partes = listar_partes(projeto_id)
        return render_template("partes_engajamento.html", projeto=p, partes=partes, fluxo=resumo_fluxo(partes),
                               etapa="engajar", secao="partes")

    @app.route("/p/<int:projeto_id>/partes/monitoramento", methods=["GET", "POST"])
    def partes_monitoramento(projeto_id):
        p = obter_projeto(projeto_id)
        if request.method == "POST":
            parte_id = inteiro(request.form.get("parte_id"), 1, 10**9)
            if parte_id is None:
                flash("Escolha a parte interessada.", "erro")
                return redirect(url_for("partes_monitoramento", projeto_id=projeto_id))
            registrar_interacao(projeto_id, parte_id)
            destino = request.form.get("voltar")
            if destino == "detalhe":
                return redirect(url_for("parte_detalhe", projeto_id=projeto_id, parte_id=parte_id))
            return redirect(url_for("partes_monitoramento", projeto_id=projeto_id))
        partes = listar_partes(projeto_id)
        db = get_db()
        interacoes = db.execute(
            """SELECT i.*, s.nome FROM interacao i JOIN parte_interessada s ON s.id = i.parte_id
               WHERE s.projeto_id = ? ORDER BY i.data DESC, i.id DESC LIMIT 50""", (projeto_id,)
        ).fetchall()
        historico = db.execute(
            """SELECT h.*, s.nome FROM historico_engajamento h JOIN parte_interessada s ON s.id = h.parte_id
               WHERE s.projeto_id = ? AND h.nivel_anterior IS NOT NULL ORDER BY h.data DESC, h.id DESC LIMIT 20""",
            (projeto_id,),
        ).fetchall()
        ab = obter_abertura(projeto_id)
        alertas = [a for a in gerar_alertas(p, partes, ab) if "/partes/" in a["link"]]
        return render_template("partes_monitoramento.html", projeto=p, partes=partes, fluxo=resumo_fluxo(partes),
                               interacoes=interacoes, historico=historico, alertas=alertas,
                               etapa="monitorar", secao="partes", dias=DIAS_SEM_INTERACAO)

    @app.route("/p/<int:projeto_id>/interacoes/<int:interacao_id>/excluir", methods=["POST"])
    def interacao_excluir(projeto_id, interacao_id):
        db = get_db()
        row = db.execute(
            """SELECT i.id, i.parte_id FROM interacao i JOIN parte_interessada s ON s.id = i.parte_id
               WHERE i.id = ? AND s.projeto_id = ?""", (interacao_id, projeto_id)
        ).fetchone()
        if row is None:
            abort(404)
        db.execute("DELETE FROM interacao WHERE id = ?", (interacao_id,))
        db.commit()
        flash("Interação removida.", "ok")
        if request.form.get("voltar") == "detalhe":
            return redirect(url_for("parte_detalhe", projeto_id=projeto_id, parte_id=row["parte_id"]))
        return redirect(url_for("partes_monitoramento", projeto_id=projeto_id))
