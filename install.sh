#!/usr/bin/env bash
# ReYMeN — Tek komut kurulum
# Kullanim: curl -fsSL https://raw.githubusercontent.com/Watcher-Hermes/ReYMeN-Ajan-v2/main/install.sh | bash
set -euo pipefail

REPO="Watcher-Hermes/ReYMeN-Ajan-v2"
BRANCH="main"
REPO_URL="https://github.com/$REPO.git"

BOLD='\033[1m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

info()  { printf "${GREEN}==>${NC} %s\n" "$*"; }
warn()  { printf "${YELLOW}==>${NC} %s\n" "$*"; }
error() { printf "${RED}==>${NC} %s\n" "$*"; }
header(){ printf "\n${CYAN}════════════════════════════════════════${NC}\n${BOLD} %s${NC}\n${CYAN}════════════════════════════════════════${NC}\n" "$*"; }

# Platform tespiti
detect_platform() {
    case "$(uname -s)" in
        Linux*)  echo "linux" ;;
        Darwin*) echo "macos" ;;
        CYGWIN*|MINGW*|MSYS*) echo "windows" ;;
        *)       echo "unknown" ;;
    esac
}

PLATFORM=$(detect_platform)
HEDEF_DIZIN="$HOME/reymen"

header "ReYMeN Kurulumu"
info "Platform: $PLATFORM"
info "Hedef: $HEDEF_DIZIN"

# Bagimlilik kontrolu
check_deps() {
    local eksik=0
    if ! command -v python3 &>/dev/null; then
        error "python3 bulunamadi! Python 3.11+ kurun"
        eksik=1
    else
        local pyver
        pyver=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d. -f1-2)
        info "Python $pyver"
    fi
    if ! command -v git &>/dev/null; then
        error "git bulunamadi!"
        eksik=1
    else
        info "Git ok"
    fi
    if [ "$eksik" = "1" ]; then
        error "Eksik bagimliliklar. Once kurun."
        exit 1
    fi
}

check_deps

# Klonla
if [ -d "$HEDEF_DIZIN" ]; then
    warn "$HEDEF_DIZIN zaten var. Uzerine yazilsin mi? [y/N]"
    read -r cevap
    if [ "$cevap" != "y" ] && [ "$cevap" != "Y" ]; then
        info "Iptal."
        exit 0
    fi
    rm -rf "$HEDEF_DIZIN"
fi

info "Depo klonlaniyor: $REPO"
git clone --depth 1 --branch "$BRANCH" "$REPO_URL" "$HEDEF_DIZIN"
cd "$HEDEF_DIZIN"

# Sanal ortam
info "Sanal ortam olusturuluyor..."
python3 -m venv venv

if [ "$PLATFORM" = "windows" ]; then
    . venv/Scripts/activate 2>/dev/null || source venv/Scripts/activate
else
    . venv/bin/activate
fi

info "Bagimliliklar yukleniyor..."
pip install --upgrade pip -q
pip install -e . -q

# .env
if [ ! -f .env ]; then
    info "Ornek .env olusturuluyor..."
    cat > .env << 'ENVEOF'
# ReYMeN Cevre Degiskenleri
# En az bir API key ekleyin (DeepSeek onerilen)
DEEPSEEK_API_KEY=
OPEN...OKEN=
ENVEOF
    warn "API key'lerinizi .env dosyasina ekleyin: $HEDEF_DIZIN/.env"
fi

# Bitis
header "Kurulum Tamamlandi!"
echo ""
echo "Kullanmak icin:"
echo "  cd $HEDEF_DIZIN"
echo "  source venv/bin/activate  # Windows: venv\\Scripts\\activate"
echo "  reymen chat"
echo ""
echo "Web UI:"
echo "  reymen web"
echo ""
echo "Dokumantasyon:"
echo "  https://github.com/$REPO#readme"
