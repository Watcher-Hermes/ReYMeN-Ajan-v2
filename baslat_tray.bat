@echo off
title ReYMeN Tray
cd /d "%~dp0"
echo ReYMeN Desktop (sistem tepsisi) baslatiliyor...
call venv\Scripts\python.bat -m reymen.desktop.launcher tray
