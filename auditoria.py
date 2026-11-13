"""Histórico de alterações, lixeira e recuperação de registros (v13).

Cada conexão do app recebe gatilhos temporários (TEMP TRIGGER) que gravam em `auditoria` toda inclusão,
alteração e exclusão, com o estado antes e depois em JSON, o usuário e um "lote" (a requisição).
Por serem temporários, ferramentas externas que abram o banco não são afetadas.

Como exclusões em cascata também disparam os gatilhos, excluir um projeto registra cada linha removida;
a lixeira restaura o lote inteiro.
"""
import json
import uuid

from flask import g, has_request_context

IGNORAR_TABELAS = {"auditoria", "sqlite_sequence"}
IGNORAR_COLUNAS = {"senha_hash"}          # nunca guardar hash de senha no histórico
COLUNAS_RUIDO = {"atualizado_em"}        # mudar só isto não é alteração relevante
NOMES = {
    "projeto": "Projeto", "abertura": "Termo de abertura", "parte_interessada": "Parte interessada", "interacao": "Contato",
    "historico_engajamento": "Engajamento", "risco": "Risco", "risco_revisao": "Revisão de risco", "incerteza": "Incerteza",
    "questao": "Questão", "mudanca": "Mudança", "licao": "Lição aprendida", "item": "Item de escopo", "linha_base": "Linha de base",
    "qualidade_custo": "Custo da qualidade", "beneficio": "Benefício", "iteracao": "Iteração", "metrica": "Indicador",
    "medicao": "Medição", "relatorio_status": "Relatório de status", "membro": "Membro da equipe", "raci_linha": "Atividade RACI",
    "raci_papel": "Papel RACI", "avaliacao_equipe": "Saúde da equipe", "fase": "Fase", "decisao_tailoring": "Tailoring",
    "verificacao": "Verificação", "conformidade": "Conformidade", "adocao_grupo": "Grupo afetado", "adocao_medicao": "Medição de adoção",
    "decisao": "Decisão", "premissa": "Premissa", "aquisicao": "Aquisição", "recurso_fisico": "Recurso físico", "usuario": "Usuário",
}
ROTULOS = ("titulo", "nome", "item", "descricao", "requisito", "grupo", "elemento", "login", "resumo", "motivo")

_sql_gatilhos = None
_esquema = {}  # tabela -> lista de colunas
_chave = {}    # tabela -> colunas da chave primária


def _json(prefixo, colunas):
    """json_object em blocos de 40 colunas (limite de argumentos de funções do SQLite)."""
    blocos = []
    for i in range(0, len(colunas), 40):
        pares = ", ".join(f"'{c}', {prefixo}.\"{c}\"" for c in colunas[i:i + 40])
        blocos.append(f"json_object({pares})")
    expr = blocos[0]
    for b in blocos[1:]:
        expr = f"json_patch({expr}, {b})"
    return expr


def preparar(conn):
    """Lê o esquema (depois das migrações) e monta o SQL dos gatilhos uma única vez."""
    global _sql_gatilhos
    tabelas = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'") if r[0] not in IGNORAR_TABELAS]
    com_projeto = set()
    for t in tabelas:
        info = conn.execute(f'PRAGMA table_info("{t}")').fetchall()
        _esquema[t] = [r[1] for r in info]
        _chave[t] = [r[1] for r in sorted(info, key=lambda r: r[5]) if r[5]] or ["rowid"]
        if "projeto_id" in _esquema[t]:
            com_projeto.add(t)
    partes = []
    for t in tabelas:
        cols = [c for c in _esquema[t] if c not in IGNORAR_COLUNAS]
        relevantes = [c for c in cols if c not in COLUNAS_RUIDO and c != "id"]
        rid = {k: (f'{k}."{_chave[t][0]}"' if len(_chave[t]) == 1 and _chave[t][0] != "rowid" else f"{k}.rowid") for k in ("NEW", "OLD")}
        if t == "projeto":
            proj = {"NEW": "NEW.id", "OLD": "OLD.id"}
        elif t in com_projeto:
            proj = {"NEW": "NEW.projeto_id", "OLD": "OLD.projeto_id"}
        else:
            fk = next((r for r in conn.execute(f'PRAGMA foreign_key_list("{t}")') if r[2] in com_projeto), None)
            proj = ({k: f"(SELECT projeto_id FROM {fk[2]} WHERE id = {k}.\"{fk[3]}\")" for k in ("NEW", "OLD")} if fk
                    else {"NEW": "NULL", "OLD": "NULL"})
        base = "INSERT INTO main.auditoria (usuario_id, usuario_nome, lote, acao, tabela, registro_id, projeto_id, antes, depois) VALUES (aud_usuario_id(), aud_usuario_nome(), aud_lote(), "
        partes.append(f"CREATE TEMP TRIGGER IF NOT EXISTS aud_{t}_i AFTER INSERT ON main.\"{t}\" BEGIN {base}'I', '{t}', {rid['NEW']}, {proj['NEW']}, NULL, {_json('NEW', cols)}); END;")
        quando = " OR ".join(f'OLD."{c}" IS NOT NEW."{c}"' for c in relevantes) or "0"
        partes.append(f"CREATE TEMP TRIGGER IF NOT EXISTS aud_{t}_u AFTER UPDATE ON main.\"{t}\" WHEN {quando} BEGIN {base}'U', '{t}', {rid['NEW']}, {proj['NEW']}, {_json('OLD', cols)}, {_json('NEW', cols)}); END;")
        partes.append(f"CREATE TEMP TRIGGER IF NOT EXISTS aud_{t}_d AFTER DELETE ON main.\"{t}\" BEGIN {base}'D', '{t}', {rid['OLD']}, {proj['OLD']}, {_json('OLD', cols)}, NULL); END;")
    _sql_gatilhos = "\n".join(partes)


def _usuario():
    if has_request_context():
        return g.get("usuario")
    return None


def _lote():
    if not has_request_context():
        return "sistema"
    if "lote_auditoria" not in g:
        g.lote_auditoria = uuid.uuid4().hex[:12]
    return g.lote_auditoria


def ao_conectar(conn):
    """Registra as funções de contexto e os gatilhos temporários numa conexão do app."""
    conn.create_function("aud_usuario_id", 0, lambda: (_usuario() or {"id": None})["id"], deterministic=False)
    conn.create_function("aud_usuario_nome", 0, lambda: (_usuario() or {"nome": ""})["nome"], deterministic=False)
    conn.create_function("aud_lote", 0, _lote, deterministic=False)
    if _sql_gatilhos:
        conn.executescript(_sql_gatilhos)


# ------------------------------------------------------------------ leitura
def rotulo(tabela, dados):
    dados = dados or {}
    cod = dados.get("codigo")
    prefixo = {"risco": "R", "questao": "Q", "mudanca": "M", "item": "I", "aquisicao": "A"}.get(tabela)
    nome = next((str(dados[c]) for c in ROTULOS if dados.get(c)), "")
    if prefixo and cod:
        nome = f"{prefixo}-{cod} {nome}"
    return (nome[:90] + "…") if len(nome) > 90 else nome


def descrever(linha):
    antes = json.loads(linha["antes"]) if linha["antes"] else None
    depois = json.loads(linha["depois"]) if linha["depois"] else None
    mudou = []
    if antes and depois:
        mudou = [c for c in depois if c not in COLUNAS_RUIDO and antes.get(c) != depois.get(c)]
    return {
        "id": linha["id"], "quando": linha["quando"], "quem": linha["usuario_nome"] or "sistema", "acao": linha["acao"],
        "acao_texto": {"I": "criou", "U": "alterou", "D": "excluiu"}[linha["acao"]],
        "tabela": linha["tabela"], "tipo": NOMES.get(linha["tabela"], linha["tabela"]),
        "registro": rotulo(linha["tabela"], depois or antes), "campos": mudou, "lote": linha["lote"],
        "antes": antes, "depois": depois, "projeto_id": linha["projeto_id"], "registro_id": linha["registro_id"],
    }


# ------------------------------------------------------------------ recuperação
def restaurar_lote(db, lote):
    """Recria tudo o que foi excluído num lote (ex.: um projeto e todos os seus registros). Devolve (restaurados, ignorados)."""
    linhas = db.execute("SELECT * FROM auditoria WHERE lote = ? AND acao = 'D' ORDER BY id DESC", (lote,)).fetchall()
    return _reinserir(db, linhas)


def restaurar_registro(db, auditoria_id):
    linhas = db.execute("SELECT * FROM auditoria WHERE id = ? AND acao = 'D'", (auditoria_id,)).fetchall()
    return _reinserir(db, linhas)


def _reinserir(db, linhas):
    restaurados = ignorados = 0
    db.execute("PRAGMA defer_foreign_keys = ON")  # pais e filhos voltam na mesma transação
    try:
        for l in linhas:
            t = l["tabela"]
            if t not in _esquema or t == "usuario":
                ignorados += 1
                continue
            dados = {c: v for c, v in json.loads(l["antes"]).items() if c in _esquema[t]}
            chave = [c for c in _chave[t] if c in dados]
            if chave and db.execute(f'SELECT 1 FROM "{t}" WHERE ' + " AND ".join(f'"{c}" = ?' for c in chave),
                                    [dados[c] for c in chave]).fetchone():
                ignorados += 1  # já existe (foi recriado ou restaurado antes)
                continue
            cols = list(dados)
            db.execute(f'INSERT INTO "{t}" ({", ".join(chr(34) + c + chr(34) for c in cols)}) VALUES ({", ".join("?" for _ in cols)})',
                       [dados[c] for c in cols])
            restaurados += 1
        if db.execute("PRAGMA foreign_key_check").fetchone():
            raise ValueError("a restauração deixaria registros sem o registro pai")
        db.commit()
    except Exception:
        db.rollback()
        raise
    return restaurados, ignorados
