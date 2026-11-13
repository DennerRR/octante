"""Ponto de entrada para hospedagem (PythonAnywhere, Gunicorn etc.). Veja DEPLOY.md."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("GESTOR_PRODUCAO", "1")

from app import create_app  # noqa: E402

application = create_app()
app = application
