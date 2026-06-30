@echo off
REM ============================================================================
REM  reymen.cmd — ReYMeN Agent Bagimsiz Launcher
REM  Hermes'siz, direkt ReYMeN venv'i ile calisir
REM ============================================================================
setlocal

set "REYMEN_PROJE=%~dp0.."
set "REYMEN_VENV_PY=%REYMEN_PROJE%\venv\Scripts\python.exe"

if not exist "%REYMEN_VENV_PY%" (
    echo [HATA] ReYMeN venv bulunamadi: %REYMEN_VENV_PY%
    pause
    exit /b 1
)

cd /d "%REYMEN_PROJE%"

REM PYTHONPATH'i temizle (Hermes kalintilari)
set "PYTHONPATH="

"%REYMEN_VENV_PY%" reymen_launcher.py %*
