"""Backups automáticos, verificação e restauração do banco (v13).

- Um backup automático por dia (no primeiro acesso do dia), mais um antes de cada migração e antes de cada restauração.
- Cada cópia é feita pela API de backup do SQLite (consistente mesmo com o app em uso), conferida com integrity_check
  e acompanhada de um arquivo .sha256 que detecta corrupção ou adulteração antes de restaurar.
- Rotação: mantém os 14 automáticos mais recentes e os 5 mais recentes de cada outro motivo.
"""
import hashlib
import os
import re
import sqlite3
import time
from datetime import datetime

CABECALHO_SQLITE = b"SQLite format 3\x00"
NOME_VALIDO = re.compile(r"^gestor-\d{8}-\d{6}-[a-z-]+\.db$")
MANTER = {"automatico": 14}
MANTER_OUTROS = 5


def pasta(caminho_banco):
    p = os.path.join(os.path.dirname(os.path.abspath(caminho_banco)), "backups")
    os.makedirs(p, exist_ok=True)
    return p


def _sha256(caminho):
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 16), b""):
            h.update(bloco)
    return h.hexdigest()


def verificar(caminho, versao_max=None):
    """Confere se o arquivo é um banco válido deste app. Devolve (ok, mensagem, info)."""
    try:
        with open(caminho, "rb") as f:
            if f.read(16) != CABECALHO_SQLITE:
                return False, "O arquivo não é um banco SQLite.", {}
        conn = sqlite3.connect(f"file:{caminho}?mode=ro", uri=True)
        try:
            if conn.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
                return False, "O banco está corrompido (falhou na verificação de integridade).", {}
            tabelas = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            if "projeto" not in tabelas:
                return False, "O arquivo não é um banco do Octante.", {}
            versao = conn.execute("PRAGMA user_version").fetchone()[0]
            if versao_max is not None and versao > versao_max:
                return False, f"O backup é de uma versão mais nova do app (banco v{versao}). Atualize o app antes.", {}
            info = {"versao": versao, "projetos": conn.execute("SELECT COUNT(*) FROM projeto").fetchone()[0]}
        finally:
            conn.close()
    except sqlite3.DatabaseError as e:
        return False, f"Não foi possível ler o arquivo ({e}).", {}
    sidecar = caminho + ".sha256"
    if os.path.exists(sidecar):
        with open(sidecar, encoding="ascii") as f:
            if f.read().strip() != _sha256(caminho):
                return False, "A assinatura (SHA-256) não confere: o arquivo foi alterado ou corrompido depois do backup.", {}
    return True, "ok", info


def fazer(caminho_banco, motivo, conn=None):
    """Copia o banco para a pasta de backups. Devolve o caminho do backup (ou None se não há dados)."""
    destino_dir = pasta(caminho_banco)
    proprio = conn is None
    origem = conn or sqlite3.connect(caminho_banco, timeout=10)
    try:
        if not origem.execute("SELECT name FROM sqlite_master WHERE name = 'projeto'").fetchone():
            return None
        if not origem.execute("SELECT 1 FROM projeto LIMIT 1").fetchone() and motivo != "manual":
            return None  # banco sem projetos: nada a proteger
        nome = f"gestor-{datetime.now():%Y%m%d-%H%M%S}-{motivo}.db"
        final = os.path.join(destino_dir, nome)
        tmp = final + ".tmp"
        copia = sqlite3.connect(tmp)
        with copia:
            origem.backup(copia)
        copia.close()
        ok, msg, _ = verificar(tmp)
        if not ok:
            os.remove(tmp)
            raise RuntimeError(f"Backup descartado: {msg}")
        os.replace(tmp, final)
        with open(final + ".sha256", "w", encoding="ascii") as f:
            f.write(_sha256(final))
        rotacionar(destino_dir)
        return final
    finally:
        if proprio:
            origem.close()


def listar(caminho_banco):
    itens = []
    for nome in sorted(os.listdir(pasta(caminho_banco)), reverse=True):
        if not NOME_VALIDO.match(nome):
            continue
        cam = os.path.join(pasta(caminho_banco), nome)
        partes = nome[:-3].split("-", 3)
        itens.append({"nome": nome, "motivo": partes[3].replace("-", " "), "tamanho_kb": round(os.path.getsize(cam) / 1024),
                      "quando": datetime.strptime(partes[1] + partes[2], "%Y%m%d%H%M%S"), "assinado": os.path.exists(cam + ".sha256")})
    return itens


def rotacionar(destino_dir):
    por_motivo = {}
    for nome in sorted(os.listdir(destino_dir), reverse=True):
        if NOME_VALIDO.match(nome):
            por_motivo.setdefault(nome[:-3].split("-", 3)[3], []).append(nome)
    for motivo, nomes in por_motivo.items():
        for velho in nomes[MANTER.get(motivo, MANTER_OUTROS):]:
            for cam in (os.path.join(destino_dir, velho), os.path.join(destino_dir, velho + ".sha256")):
                if os.path.exists(cam):
                    os.remove(cam)


def automatico_se_preciso(caminho_banco, intervalo_horas=20):
    """Faz o backup diário se o último automático tem mais de `intervalo_horas`."""
    autos = [b for b in listar(caminho_banco) if b["motivo"] == "automatico"]
    if autos and (datetime.now() - autos[0]["quando"]).total_seconds() < intervalo_horas * 3600:
        return None
    return fazer(caminho_banco, "automatico")


def caminho_seguro(caminho_banco, nome):
    if not NOME_VALIDO.match(nome or ""):
        return None
    cam = os.path.join(pasta(caminho_banco), nome)
    return cam if os.path.exists(cam) else None


def restaurar(caminho_banco, origem, versao_atual, migrar):
    """Substitui o banco atual pelo backup `origem`, guardando antes uma cópia do estado atual."""
    ok, msg, info = verificar(origem, versao_atual)
    if not ok:
        raise ValueError(msg)
    fazer(caminho_banco, "antes-de-restaurar")
    src = sqlite3.connect(f"file:{origem}?mode=ro", uri=True)
    dst = sqlite3.connect(caminho_banco, timeout=30, isolation_level=None)
    try:
        src.backup(dst)
        migrar(dst)
    finally:
        src.close()
        dst.close()
    time.sleep(0)  # libera o arquivo no Windows
    return info
