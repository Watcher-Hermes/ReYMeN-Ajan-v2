@echo off
chcp 65001 >nul
title ReYMeN Agent v2.0 - Tam Kurulum

echo ============================================
echo    ReYMeN Agent v2.0 - Tam Kurulum
echo ============================================
echo.

:: ---------- GEREKSINIM KONTROLLERI ----------
set ADIM=0

:: 1. PowerShell
set /a ADIM+=1
echo --- %ADIM%/8 PowerShell ---
powershell -Command "exit" >nul 2>&1
if %errorlevel% neq 0 (
    echo [!!] PowerShell bulunamadi! Windows'u guncelleyin.
    pause
    exit /b
) else (
    echo [OK] PowerShell var
)

:: 2. winget (paket yoneticisi)
set /a ADIM+=1
echo --- %ADIM%/8 winget ---
winget --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!!] winget bulunamadi! Microsoft Store'dan "App Installer" yukleyin.
    pause
    exit /b
) else (
    echo [OK] winget var
)

:: 3. Python
set /a ADIM+=1
echo --- %ADIM%/8 Python ---
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

:: 4. Git
set /a ADIM+=1
echo --- %ADIM%/8 Git ---
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

:: 5. VS Code
set /a ADIM+=1
echo --- %ADIM%/8 VS Code ---
code --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!!] VS Code bulunamadi! Yukleniyor...
    winget install Microsoft.VisualStudioCode --silent --accept-package-agreements
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

:: 6. WSL + Ubuntu
set /a ADIM+=1
echo --- %ADIM%/8 WSL (Linux) ---
wsl --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!!] WSL bulunamadi! Yukleniyor...
    dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /quiet
    dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /quiet
    wsl --update
    wsl --install -d Ubuntu --quiet
    echo [OK] WSL + Ubuntu kuruldu (bilgisayar yeniden baslatilabilir)
) else (
    echo [OK] WSL var
)

:: 7. ffmpeg + yt-dlp
set /a ADIM+=1
echo --- %ADIM%/8 Ek Araclar (ffmpeg, yt-dlp) ---

where ffmpeg >nul 2>&1
if %errorlevel% neq 0 (
    echo [!!] ffmpeg bulunamadi! Yukleniyor...
    winget install ffmpeg --silent --accept-package-agreements
    if %errorlevel% equ 0 (
        echo [OK] ffmpeg kuruldu
    ) else (
        echo [!] ffmpeg kurulamadi! Elle kur: winget install ffmpeg
    )
) else (
    echo [OK] ffmpeg var
)

pip show yt-dlp >nul 2>&1
if %errorlevel% neq 0 (
    echo [!!] yt-dlp bulunamadi! Yukleniyor...
    pip install yt-dlp
    if %errorlevel% equ 0 (
        echo [OK] yt-dlp kuruldu
    ) else (
        echo [!] yt-dlp kurulamadi
    )
) else (
    echo [OK] yt-dlp var
)

:: 8. Repo + Sanal Ortam + Paketler
set /a ADIM+=1
echo --- %ADIM%/8 Repo ve Python Ortami ---

if not exist "ReYMeN-Ajan-v2" (
    git clone https://github.com/Watcher-Hermes/ReYMeN-Ajan-v2.git
) else (
    echo ReYMeN-Ajan-v2 zaten var, guncelleniyor...
)
cd ReYMeN-Ajan-v2

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
