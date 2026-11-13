@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Octante
where python >nul 2>nul
if errorlevel 1 (
  echo Python nao encontrado. Instale o "Python 3.13" pela Microsoft Store e tente de novo.
  pause
  exit /b 1
)
python -c "import flask, openpyxl" >nul 2>nul
if errorlevel 1 (
  echo Instalando o Flask (so na primeira vez)...
  python -m pip install --user -r requirements.txt
)
python app.py
pause
