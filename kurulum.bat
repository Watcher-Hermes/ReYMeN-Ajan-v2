@echo off
chcp 65001 >nul
title ReYMeN Agent v2.0 - Tam Kurulum

echo ============================================
echo    ReYMeN Agent v2.0 - Tam Kurulum
echo ============================================
echo.

:: ---------- GEREKSINIM KONTROLLERI ----------
echo --- 1/6 Python ---
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!!] Python bulunamadi! Yukleniyor...
    echo      Python 3.11.9 indiriliyor...
    winget install Python.Python.3.11 --silent --accept-package-agreements >nul 2>&1
    if %errorlevel% neq 0 (
        echo [!] Otomatik kurulum basarisiz! Suradan indir:
        echo     https://www.python.org/downloads/release/python-3119/
        pause
        exit /b
    )
    echo [OK] Python kuruldu
)

python -c "import sys; v=sys.version_info; exit(0) if v.major==3 and v.minor>=11 else exit(1)" >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python 3.11+ gerekli! 
    python --version
    pause
    exit /b
)
for /f "tokens=*" %%i in ('python --version 2^>nul') do set PYVER=%%i
echo [OK] %PYVER%

echo.
echo --- 2/6 Git ---
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!!] Git bulunamadi! Yukleniyor...
    winget install Git.Git --silent --accept-package-agreements >nul 2>&1
    if %errorlevel% neq 0 (
        echo [!] Otomatik kurulum basarisiz! Suradan indir:
        echo     https://git-scm.com/download/win
        pause
        exit /b
    )
    echo [OK] Git kuruldu
)
for /f "tokens=*" %%i in ('git --version') do set GITVER=%%i
echo [OK] %GITVER%

echo.
echo --- 3/6 VS Code ---
code --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!!] VS Code bulunamadi! Yukleniyor...
    winget install Microsoft.VisualStudioCode --silent --accept-package-agreements >nul 2>&1
    if %errorlevel% neq 0 (
        echo [!] Otomatik kurulum basarisiz! Suradan indir:
        echo     https://code.visualstudio.com/download
        pause
        exit /b
    )
    echo [OK] VS Code kuruldu
) else (
    echo [OK] VS Code var
)

echo.
echo --- 4/6 WSL (Linux) ---
wsl --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!!] WSL bulunamadi! Yukleniyor...
    dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /quiet >nul 2>&1
    dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /quiet >nul 2>&1
    wsl --update >nul 2>&1
    wsl --install -d Ubuntu --quiet >nul 2>&1
    echo [OK] WSL + Ubuntu kuruldu (bilgisayar yeniden baslatilabilir)
) else (
    echo [OK] WSL var
)

echo.
echo --- 5/6 Repo Klonlama ---
if not exist "ReYMeN-Ajan-v2" (
    git clone https://github.com/Watcher-Hermes/ReYMeN-Ajan-v2.git
) else (
    echo ReYMeN-Ajan-v2 zaten var, guncelleniyor...
    cd ReYMeN-Ajan-v2
    git pull
    cd ..
)
cd ReYMeN-Ajan-v2

echo.
echo --- 6/6 Python Ortami ---
if not exist "venv" (
    python -m venv venv
    echo [OK] Sanal ortam olusturuldu
)
call venv\Scripts\activate

if exist requirements.txt (
    pip install -r requirements.txt
    if %errorlevel% equ 0 (
        echo [OK] Tum paketler yuklendi
    ) else (
        echo [!] Paket hatasi! Elle dene: pip install -r requirements.txt
        pause
        exit /b
    )
)

:: .env
if not exist .env (
    echo # ReYMeN - API Anahtarlari > .env
    echo. >> .env
    echo # DEEPSEEK_API_KEY=*** >> .env
    echo # TELEGRAM_BOT_TOKEN=*** >> .env
    echo [!!] .env olusturuldu! API anahtarlarini ekle!
)

echo.
echo ============================================
echo    KURULUM TAMAMLANDI!
echo ============================================
echo.
echo KULLANIM:
echo    cd ReYMeN-Ajan-v2
echo    venv\Scripts\activate
echo    python reymen_launcher.py
echo.
echo ONEMLI: .env dosyasina API anahtarlarini ekle!
echo.
pause
