#!/usr/bin/env sh
# Abre o Octante (Linux/macOS). Uso: ./iniciar.sh
cd "$(dirname "$0")" || exit 1
PY=$(command -v python3 || command -v python) || { echo "Python não encontrado. Instale o Python 3.10+."; exit 1; }
"$PY" -c "import flask, openpyxl" 2>/dev/null || "$PY" -m pip install --user -r requirements.txt
exec "$PY" app.py
