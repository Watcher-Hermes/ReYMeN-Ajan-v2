@echo off
chcp 65001 >nul
title ReYMeN Agent v1.0 - Tam Kurulum

echo ============================================
echo    ReYMeN Agent v1.0 - Tam Kurulum
echo ============================================
echo.
echo NOT: ReYMeN bagimsiz bir ajandir, Hermes gerektirmez.
echo.

:: ---------- GEREKSINIM KONTROLLERI ----------
set ADIM=0

:: 1. PowerShell (Windows'da her zaman var)
set /a ADIM+=1
echo --- %ADIM%/6 PowerShell ---
powershell -Command "exit" >nul 2>&1
if %errorlevel% neq 0 (
    echo [!!] PowerShell bulunamadi! Windows'u guncelleyin.
    pause
    exit /b
) else (
    echo [OK] PowerShell var
)

:: 2. Python
set /a ADIM+=1
echo --- %ADIM%/6 Python ---
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!!] Python bulunamadi! Yukleniyor...
    winget install Python.Python.3.11 --silent --accept-package-agreements
    if %errorlevel% neq 0 (
        echo [!] Otomatik kurulum basarisiz! Suradan indir:
        echo     https://www.python.org/downloads/release/python-3119/
        echo     Kurarken "Add Python to PATH" isaretle
        pause
        exit /b
    )
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

:: 3. Git
set /a ADIM+=1
echo --- %ADIM%/6 Git ---
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!!] Git bulunamadi! Yukleniyor...
    winget install Git.Git --silent --accept-package-agreements
    if %errorlevel% neq 0 (
        echo [!] Otomatik kurulum basarisiz! Suradan indir:
        echo     https://git-scm.com/download/win
        pause
        exit /b
    )
)
for /f "tokens=*" %%i in ('git --version') do set GITVER=%%i
echo [OK] %GITVER%

:: 4. ffmpeg (opsiyonel, video/ses araclari icin)
set /a ADIM+=1
echo --- %ADIM%/6 ffmpeg ---
where ffmpeg >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] ffmpeg bulunamadi! Opsiyonel, video araclari icin gerekli.
    echo     Elle kurmak icin: winget install FFmpeg.FFmpeg
) else (
    echo [OK] ffmpeg var
)

:: 5. Repo + Sanal Ortam + Paketler
set /a ADIM+=1
echo --- %ADIM%/6 Repo ve Python Ortami ---

:: Bu script'in bulundugu dizin
set "SCRIPT_DIR=%~dp0"
echo [INFO] Kurulum dizini: %SCRIPT_DIR%

:: Proje kokunde oldugumuzu varsay, yoksa clone et
if not exist "reymen_launcher.py" (
    if not exist "ReYMeN-Ajan" (
        git clone https://github.com/Watcher-Hermes/ReYMeN-Ajan-v2.git ReYMeN-Ajan
        echo [OK] Repo klonlandi
    )
    cd ReYMeN-Ajan
) else (
    echo [OK] Proje dosyalari mevcut
)

if not exist "reymen_venv" (
    python -m venv reymen_venv
    if !errorlevel! equ 0 (
        echo [OK] Sanal ortam olusturuldu (reymen_venv)
    ) else (
        echo [!!] Sanal ortam olusturulamadi!
        pause
        exit /b
    )
)

call reymen_venv\Scripts\activate

if exist requirements.txt (
    pip install -r requirements.txt
    if !errorlevel! equ 0 (
        echo [OK] Tum paketler yuklendi
    ) else (
        echo [!] Paket hatasi! Elle dene: pip install -r requirements.txt
        pause
        exit /b
    )
) else (
    pip install requests python-dotenv
    echo [OK] Temel paketler yuklendi
)

:: 6. .env olustur
set /a ADIM+=1
echo --- %ADIM%/6 API Anahtarlari ---

if not exist ".env" (
    (
        echo # ReYMeN Agent - API Anahtarlari
        echo # .env dosyasi GITIGNORE'dadir, guvende kalir
        echo.
        echo # ZORUNLU: En az bir provider
        echo DEEPSEEK_API_KEY=buraya_yaz
        echo.
        echo # OPSIYONEL: Diger providerlar
        echo # OPENROUTER_API_KEY=buraya_yaz
        echo # ANTHROPIC_API_KEY=buraya_yaz
        echo # OPENAI_API_KEY=buraya_yaz
        echo # XAI_API_KEY=buraya_yaz
        echo # GROQ_API_KEY=buraya_yaz
        echo # XIAOMI_API_KEY=buraya_yaz
        echo.
        echo # OPSIYONEL: Telegram bot tokeni
        echo # TELEGRAM_BOT_TOKEN=000000_buraya_yaz
        echo.
        echo # OPSIYONEL: Harici servisler
        echo # FIRECRAWL_API_KEY=buraya_yaz
        echo # PERPLEXITY_API_KEY=buraya_yaz
        echo # FAL_KEY=buraya_yaz
    ) > .env
    echo [!!] .env olusturuldu! API anahtarlarini ekle!
    start notepad .env
) else (
    echo [OK] .env zaten var
)

echo.
echo ============================================
echo    KURULUM TAMAMLANDI!
echo ============================================
echo.
echo KULLANIM:
echo    cd ReYMeN-Ajan
echo    reymen_venv\Scripts\activate
echo    python reymen_launcher.py
echo.
echo ONEMLI: .env dosyasina API anahtarlarini ekle!
echo.
echo GitHub: https://github.com/Watcher-Hermes/ReYMeN-Ajan-v2
echo.
pause
