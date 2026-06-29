# -*- coding: utf-8 -*-
"""docker_sandbox.py — Docker tabanli guvenli kod calistirma sandbox'i.

Subprocess sandbox'in otesinde:
  - Docker container'da tam izolasyon
  - Ag erisimi kisitlamasi (--network=none)
  - Dosya sistemi kisitlamasi (read-only root, /sandbox yazilabilir)
  - Kaynak limiti (CPU, memory)
  - Gecici dizin temizligi

Fallback: Docker yoksa subprocess sandbox kullanilir.
"""

import json
import logging
import os
import subprocess
import sys
import tempfile
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)

# ── Varsayilanlar ──────────────────────────────────────────────────────────
VARSAYILAN_IMAGE = "reymen-sandbox:latest"
VARSAYILAN_TIMEOUT = 30
VARSAYILAN_MAX_CHARS = 10000
VARSAYILAN_MEMORY = "256m"       # Docker memory limit
VARSAYILAN_CPU = 0.5             # Docker CPU limit (cores)
VARSAYILAN_TEMP = "/tmp/sandbox"

# Docker mevcut mu?
DOCKER_MEVCUT = False
try:
    r = subprocess.run(["docker", "--version"], capture_output=True, text=True, timeout=5)
    DOCKER_MEVCUT = r.returncode == 0
except Exception:
    pass

# Image mevcut mu?
IMAGE_MEVCUT = False
if DOCKER_MEVCUT:
    try:
        r = subprocess.run(
            ["docker", "images", "-q", VARSAYILAN_IMAGE],
            capture_output=True, text=True, timeout=10
        )
        IMAGE_MEVCUT = bool(r.stdout.strip())
    except Exception:
        pass

# Fallback: subprocess sandbox
try:
    from reymen.guvenlik.guvenli_sandbox import guvenli_calistir as _subprocess_sandbox
    SUBPROCESS_SANDBOX_OK = True
except ImportError:
    SUBPROCESS_SANDBOX_OK = False


# ── Hata Siniflari ─────────────────────────────────────────────────────────

class SandboxError(RuntimeError):
    """Sandbox calistirma hatasi."""


class SandboxTimeout(SandboxError):
    """Zaman asimi."""


class SandboxBuildError(SandboxError):
    """Docker image build hatasi."""


# ── Docker Sandbox ─────────────────────────────────────────────────────────

class DockerSandbox:
    """Docker container'da izole Python kodu calistir.

    Ozellikler:
      - Ag kapali (--network=none)
      - Salt-okunur root (/sandbox haric)
      - CPU/memory limiti
      - Timeout (container kill)
      - Cikti boyut siniri

    Kullanim:
        sb = DockerSandbox()
        sonuc = sb.calistir("print('Merhaba')")
    """

    def __init__(
        self,
        image: str = VARSAYILAN_IMAGE,
        timeout: int = VARSAYILAN_TIMEOUT,
        max_chars: int = VARSAYILAN_MAX_CHARS,
        memory: str = VARSAYILAN_MEMORY,
        cpu: float = VARSAYILAN_CPU,
        network_erisim: bool = False,
    ):
        self.image = image
        self.timeout = timeout
        self.max_chars = max_chars
        self.memory = memory
        self.cpu = cpu
        self.network_erisim = network_erisim
        self._container_id: Optional[str] = None

    def calistir(self, kod: str, baglam: Optional[dict] = None) -> str:
        """Kodu Docker container'da calistir.

        Args:
            kod: Calistirilacak Python kodu.
            baglam: Koda eklenecek degiskenler.

        Returns:
            Stdout ciktisi.
        """
        if not DOCKER_MEVCUT:
            return self._fallback(kod, baglam)

        if not IMAGE_MEVCUT:
            return self._fallback(kod, baglam)

        # Kodu sarmala
        sarmalanmis_kod = self._kod_sarmala(kod, baglam or {})

        # Container argumanlari
        docker_args = [
            "docker", "run", "--rm",
            "--network", "none",                          # ag kapali
            "--read-only",                                 # root salt-okunur
            "--tmpfs", "/sandbox:rw,noexec,nosuid,size=64m",  # yazilabilir tmp
            "--memory", self.memory,
            "--cpus", str(self.cpu),
            "--label", "reymen=sandbox",
        ]

        if not self.network_erisim:
            docker_args.extend(["--network", "none"])

        docker_args.extend([self.image, sarmalanmis_kod])

        try:
            process = subprocess.run(
                docker_args,
                capture_output=True,
                text=True,
                timeout=self.timeout + 5,  # Docker overhead
            )
        except subprocess.TimeoutExpired:
            raise SandboxTimeout(
                f"Kod {self.timeout}s icinde tamamlanamadi (container kill edildi)."
            )

        cikti = process.stdout + process.stderr
        if len(cikti) > self.max_chars:
            cikti = cikti[:self.max_chars] + (
                f"\n... [cikti {len(cikti)} karakter, sinir {self.max_chars}]"
            )
        return cikti

    def _kod_sarmala(self, kod: str, baglam: dict) -> str:
        """Kodu Docker icinde calismasi icin sarmala."""
        baglam_json = json.dumps(baglam, ensure_ascii=False)
        # Kodu tek satirlik bir exec bicimine donustur
        # newline'lari \n olarak escape et
        kod_tek = kod.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n")
        # Stdout buffer'ini flush et
        return (
            "import sys, json; "
            f"_b={baglam_json}; "
            f"exec('{kod_tek}', {{**__builtins__.__dict__, **_b}})"
        )

    def _fallback(self, kod: str, baglam: Optional[dict] = None) -> str:
        """Docker yoksa subprocess sandbox'a dus."""
        if SUBPROCESS_SANDBOX_OK:
            logger.warning("[Sandbox] Docker yok, subprocess sandbox kullaniliyor")
            return _subprocess_sandbox(kod, timeout=self.timeout, max_chars=self.max_chars, baglam=baglam)
        return "[Sandbox] Hicbir sandbox yontemi kullanilamiyor."


# ── Image Builder ──────────────────────────────────────────────────────────

class SandboxImageBuilder:
    """Docker sandbox image'ini olusturur ve yonetir."""

    def __init__(self, image: str = VARSAYILAN_IMAGE):
        self.image = image
        self.dockerfile = str(
            Path(__file__).parent / "Dockerfile.sandbox"
        )

    def build(self) -> bool:
        """Sandbox Docker image'ini build et."""
        if not DOCKER_MEVCUT:
            logger.error("[Sandbox] Docker yuklu degil")
            return False

        dockerfile_dir = str(Path(self.dockerfile).parent)
        try:
            r = subprocess.run(
                ["docker", "build", "-t", self.image,
                 "-f", self.dockerfile, dockerfile_dir],
                capture_output=True, text=True, timeout=120,
            )
            if r.returncode == 0:
                global IMAGE_MEVCUT
                IMAGE_MEVCUT = True
                logger.info("[Sandbox] Image build edildi: %s", self.image)
                return True
            logger.error("[Sandbox] Build hatasi: %s", r.stderr[:500])
            return False
        except subprocess.TimeoutExpired:
            logger.error("[Sandbox] Build zamani asimi")
            return False
        except Exception as e:
            logger.error("[Sandbox] Build hatasi: %s", e)
            return False

    def durum(self) -> dict:
        """Image durumunu kontrol et."""
        return {
            "docker_mevcut": DOCKER_MEVCUT,
            "image_mevcut": IMAGE_MEVCUT,
            "image": self.image,
        }


# ── Guvenlik Denetleyici ───────────────────────────────────────────────────

class GuvenlikDenetleyici:
    """Kod guvenlik denetleyicisi: threat pattern + PII + yasakli ifade.

    Subprocess sandbox'in keyword kontrolunun otesinde:
      - Regex tabanli threat pattern tespiti
      - PII (TC kimlik, telefon, email, kredi karti) taramasi
      - URL/IP adresi taramasi
      - Dosya yolu taramasi
    """

    # Threat pattern'ler
    THREAT_PATTERNS = {
        "base64_encoded": r"(?:base64|b64decode|b64encode)\s*\(",
        "reverse_shell": r"(?:reverse_shell|bind_shell|backconnect)",
        "crypto_miner": r"(?:cryptominer|miner|monero|xmrig)",
        "credential_steal": r"(?:credential|password|token|apikey|secret)\s*(?:=|:)\s*['\"][^'\"]{20,}['\"]",
        "suspicious_eval": r"(?:exec|eval|compile)\s*\(\s*(?:request|response|input|data)",
    }

    # PII pattern'leri
    PII_PATTERNS = {
        "tc_kimlik": r"\b[1-9]\d{10}\b",
        "telefon": r"\b(?:0|\+90)?5\d{2}\s?\d{3}\s?\d{4}\b",
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "kredi_karti": r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
    }

    def __init__(self):
        import re
        self.re = re
        self._threat_re = {
            k: self.re.compile(v, self.re.IGNORECASE)
            for k, v in self.THREAT_PATTERNS.items()
        }
        self._pii_re = {
            k: self.re.compile(v)
            for k, v in self.PII_PATTERNS.items()
        }

    def kod_kontrol(self, kod: str) -> list[dict]:
        """Kodu threat pattern'lerle tara.

        Returns:
            [{"tip": "threat", "kategori": "base64_encoded", "eslesme": "...", "konum": (bas, son)}, ...]
        """
        sonuclar = []
        for kategori, regex in self._threat_re.items():
            for m in regex.finditer(kod):
                sonuclar.append({
                    "tip": "threat",
                    "kategori": kategori,
                    "eslesme": kod[m.start():m.end()][:80],
                    "konum": (m.start(), m.end()),
                })
        return sonuclar

    def pii_kontrol(self, metin: str) -> list[dict]:
        """Metinde PII tara.

        Returns:
            [{"tip": "pii", "kategori": "tc_kimlik", "eslesme": "***", "konum": (bas, son)}, ...]
        """
        sonuclar = []
        for kategori, regex in self._pii_re.items():
            for m in regex.finditer(metin):
                sonuclar.append({
                    "tip": "pii",
                    "kategori": kategori,
                    "eslesme": metin[m.start():m.end()][:20],
                    "konum": (m.start(), m.end()),
                })
        return sonuclar

    def tam_kontrol(self, kod: str) -> dict:
        """Kod + PII kontrolu tek seferde.

        Returns:
            {"guvenli": bool, "threats": [...], "pii": [...], "ozet": str}
        """
        threats = self.kod_kontrol(kod)
        pii = self.pii_kontrol(kod)
        guvenli = len(threats) == 0
        if guvenli and len(pii) > 0:
            # PII var ama threat yok -> uyari seviyesinde
            pass

        parcalar = []
        if threats:
            parcalar.append(f"{len(threats)} threat pattern")
        if pii:
            parcalar.append(f"{len(pii)} PII")
        ozet = "✅ Guvenli" if not threats else f"⚠️ {', '.join(parcalar)}"

        return {
            "guvenli": guvenli,
            "threats": threats,
            "pii": pii,
            "ozet": ozet,
        }


# ── Entegre Sandbox API ────────────────────────────────────────────────────

_VARSAYILAN_DOCKER = DockerSandbox()
_VARSAYILAN_DENETLEYICI = GuvenlikDenetleyici()


def guvenli_calistir(
    kod: str,
    timeout: int = VARSAYILAN_TIMEOUT,
    max_chars: int = VARSAYILAN_MAX_CHARS,
    baglam: Optional[dict] = None,
    docker_oncelikli: bool = True,
) -> str:
    """Kodu guvenli sandbox'ta calistir (docker oncelikli).

    Args:
        kod: Calistirilacak Python kodu.
        timeout: Zaman asimi (saniye).
        max_chars: Maksimum cikti karakteri.
        baglam: Kod degiskenleri.
        docker_oncelikli: True=Docker dene, yoksa subprocess.

    Returns:
        Cikti metni.
    """
    # Once threat kontrol
    denetleyici = _VARSAYILAN_DENETLEYICI
    kontrol = denetleyici.tam_kontrol(kod)
    if not kontrol["guvenli"]:
        threat_list = ", ".join(
            f"{t['kategori']}" for t in kontrol["threats"]
        )
        kodu = kod[:200].replace("\n", " ")
        return (
            f"[GUVENLIK] Kod bloke edildi - threat pattern tespit edildi: {threat_list}\n"
            f"[KOD] {kodu}"
        )

    # Docker dene
    if docker_oncelikli and DOCKER_MEVCUT and IMAGE_MEVCUT:
        try:
            return _VARSAYILAN_DOCKER.calistir(kod, baglam)
        except SandboxTimeout as e:
            return f"[TIMEOUT] {e}"
        except Exception as e:
            logger.warning("[Sandbox] Docker hatasi, subprocess fallback: %s", e)

    # Subprocess fallback
    if SUBPROCESS_SANDBOX_OK:
        from reymen.guvenlik.guvenli_sandbox import guvenli_calistir as _sp_calistir
        try:
            return _sp_calistir(kod, timeout=timeout, max_chars=max_chars, baglam=baglam)
        except Exception as e:
            return f"[GUVENLIK] {e}"

    return "[Sandbox] Hicbir sandbox yontemi kullanilamiyor."


def docker_image_build(zorla: bool = False) -> str:
    """Sandbox Docker image'ini build et.

    Args:
        zorla: True olsa bile image varsa yeniden build et.

    Returns:
        Durum mesaji.
    """
    builder = SandboxImageBuilder()
    if IMAGE_MEVCUT and not zorla:
        return f"[Sandbox] Image zaten mevcut: {VARSAYILAN_IMAGE}"
    if builder.build():
        return f"[Sandbox] Image build edildi: {VARSAYILAN_IMAGE}"
    return "[Sandbox] Image build basarisiz."


def sandbox_durum() -> dict:
    """Sandbox durum raporu."""
    builder = SandboxImageBuilder()
    return {
        "docker": builder.durum(),
        "subprocess": SUBPROCESS_SANDBOX_OK,
        "denetleyici": True,
    }


def sandbox_durum_text() -> str:
    """Insan-okunabilir durum."""
    d = sandbox_durum()
    docker_ikon = "🟢" if d["docker"]["docker_mevcut"] else "🔴"
    image_ikon = "🟢" if d["docker"]["image_mevcut"] else "🟡"
    sp_ikon = "🟢" if d["subprocess"] else "🔴"
    return (
        f"[Sandbox] Guvenlik Durumu:\n"
        f"  {docker_ikon} Docker: {'mevcut' if d['docker']['docker_mevcut'] else 'yok'}\n"
        f"  {image_ikon} Image: {'build edilmis' if d['docker']['image_mevcut'] else 'build edilmemis'}\n"
        f"  {sp_ikon} Subprocess: {'hazir' if d['subprocess'] else 'yok'}\n"
        f"  🟢 Threat Denetleyici: aktif"
    )


# ── Motor Plugin API ───────────────────────────────────────────────────────

def motor_kaydet(motor):
    """Motor'a guvenlik araclarini kaydet."""
    if hasattr(motor, "_plugin_arac_kaydet"):
        motor._plugin_arac_kaydet(
            "SANDOX_DURUM",
            lambda: sandbox_durum_text(),
            "Sandbox ve guvenlik durum raporu",
        )
        motor._plugin_arac_kaydet(
            "SANDOX_IMAGE_BUILD",
            lambda zorla="": docker_image_build(zorla=bool(zorla.strip())),
            "Docker sandbox image'ini build et. Parametre: zorla=True (opsiyonel)",
        )
        motor._plugin_arac_kaydet(
            "SANDOX_KOD_KONTROL",
            lambda kod="": _VARSAYILAN_DENETLEYICI.tam_kontrol(kod)["ozet"],
            "Bir kod parcacigini threat/PII icin kontrol et. Parametre: kod",
        )
        logger.info("[Sandbox] Motor'a 3 arac kaydedildi")


# ── CLI Test ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s [%(levelname)s] %(message)s")

    print("=== ReYMeN Docker Sandbox Test ===\n")

    # 1. Durum
    print(sandbox_durum_text())
    print()

    # 2. Threat kontrol
    denetleyici = GuvenlikDenetleyici()
    test_kodlari = [
        ("Basit kod", "print('Merhaba')"),
        ("Threat: base64", "__import__('base64').b64decode('dGVzdA==')"),
        ("Threat: eval", "eval(request.form['data'])"),
        ("PII: TC kimlik", "# tc: 12345678901"),
    ]
    for ad, kod in test_kodlari:
        sonuc = denetleyici.tam_kontrol(kod)
        print(f"  {sonuc['ozet']} | {ad}")

    print()

    # 3. Docker ile calistir (varsa)
    if DOCKER_MEVCUT and IMAGE_MEVCUT:
        sonuc = guvenli_calistir("print('Docker sandbox calisiyor!')")
        print(f"Docker test: {sonuc.strip()}")
    else:
        print("Docker image build ediliyor...")
        print(docker_image_build())
        if IMAGE_MEVCUT:
            sonuc = guvenli_calistir("print('Docker sandbox calisiyor!')")
            print(f"Docker test: {sonuc.strip()}")
