# -*- coding: utf-8 -*-
"""
browser_engine.py — Çok back-end'li tarayıcı otomasyon motoru (ABC tabanlı).

BrowserEngine ABC:
  - Soyut calistir(eylem, **kwargs) → str

Engine'ler:
  - PlaywrightMCPEngine  — npx playwright MCP ile (npx + Playwright MCP sunucusu)
  - BrowserUseEngine     — browser-use kütüphanesi ile

BrowserRegistry:
  - engine kaydet / seç (ad ile) / calistir
  - Varsayılan engine: playwright_mcp (npx mevcutsa), yoksa browser_use

Motor tool:
  BROWSER_CALISTIR(eylem, url, backend="playwright_mcp") → str
"""

from __future__ import annotations

import json
import logging
import os
import subprocess
import sys
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional

log = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# Soyut Taban Sınıfı
# ═══════════════════════════════════════════════════════════════════════════════

class BrowserEngine(ABC):
    """Tüm tarayıcı otomasyon engine'leri için soyut taban sınıfı."""

    @property
    @abstractmethod
    def ad(self) -> str:
        """Engine'in benzersiz adı (küçük harf)."""

    @abstractmethod
    def calistir(self, eylem: str, **kwargs: Any) -> str:
        """Tarayıcı eylemini çalıştır.

        Args:
            eylem: Yapilacak islem (ac, screenshot, js, tikla, fill, ...).
            **kwargs: Eyleme ozel parametreler.

        Returns:
            Islem sonucu metin.
        """
        ...

    def __init__(self) -> None:
        self._hazir = self._bagimliliklari_kontrol_et()

    def _bagimliliklari_kontrol_et(self) -> bool:
        return True

    @property
    def hazir(self) -> bool:
        return self._hazir

    @property
    def aciklama(self) -> str:
        """Engine hakkinda kisa aciklama."""
        return f"{self.ad}: {self.__class__.__doc__ or ''}"


# ═══════════════════════════════════════════════════════════════════════════════
# Playwright MCP Engine
# ═══════════════════════════════════════════════════════════════════════════════

class PlaywrightMCPEngine(BrowserEngine):
    """npx playwright MCP ile tarayıcı otomasyonu. Node.js + Playwright gerekli."""

    @property
    def ad(self) -> str:
        return "playwright_mcp"

    def _bagimliliklari_kontrol_et(self) -> bool:
        """npx ve playwright'in varlığını kontrol et."""
        try:
            result = subprocess.run(
                ["npx", "--yes", "@playwright/mcp", "--help"],
                capture_output=True, text=True, timeout=15,
                env={**os.environ, "NODE_OPTIONS": "--no-warnings"},
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired, Exception) as e:
            log.debug("[PlaywrightMCPEngine] npx playwright kontrolu basarisiz: %s", e)
            return False

    def calistir(self, eylem: str, **kwargs: Any) -> str:
        """Playwright MCP subprocess ile çalıştır.

        Desteklenen eylemler: ac, screenshot, js, tikla, fill, html, snapshot
        """
        url = kwargs.get("url", "")
        secici = kwargs.get("secici", "")
        deger = kwargs.get("deger", "")
        js_kod = kwargs.get("js", "document.title")
        dosya = kwargs.get("dosya", "browser_screenshot.png")

        try:
            if eylem == "ac":
                # Playwright MCP ile sayfa açma için npx playwright open kullan
                if not url:
                    return "[Browser/PlaywrightMCP] Hata: 'url' parametresi gerekli."
                result = subprocess.run(
                    ["npx", "--yes", "@playwright/mcp", "open", url],
                    capture_output=True, text=True, timeout=30,
                    env={**os.environ, "NODE_OPTIONS": "--no-warnings"},
                )
                stdout = result.stdout.strip()
                stderr = result.stderr.strip()
                if result.returncode != 0:
                    return f"[Browser/PlaywrightMCP] Sayfa acma hatasi: {stderr[:500]}"
                return f"[Browser/PlaywrightMCP] Sayfa acildi: {url}\n{stdout[:1000]}"

            elif eylem == "screenshot":
                result = subprocess.run(
                    ["npx", "--yes", "@playwright/mcp", "screenshot", url or "about:blank", "--output", dosya],
                    capture_output=True, text=True, timeout=30,
                    env={**os.environ, "NODE_OPTIONS": "--no-warnings"},
                )
                if result.returncode != 0:
                    return f"[Browser/PlaywrightMCP] Screenshot hatasi: {result.stderr.strip()[:500]}"
                return f"[Browser/PlaywrightMCP] Screenshot alindi: {dosya}"

            elif eylem == "html":
                result = subprocess.run(
                    ["npx", "--yes", "@playwright/mcp", "html", url or "about:blank"],
                    capture_output=True, text=True, timeout=30,
                    env={**os.environ, "NODE_OPTIONS": "--no-warnings"},
                )
                if result.returncode != 0:
                    return f"[Browser/PlaywrightMCP] HTML hatasi: {result.stderr.strip()[:500]}"
                html_icerik = result.stdout.strip()[:3000]
                return f"[Browser/PlaywrightMCP] HTML ({len(result.stdout)} char):\n{html_icerik}"

            elif eylem in ("js", "evaluate"):
                result = subprocess.run(
                    ["npx", "--yes", "@playwright/mcp", "evaluate", js_kod, url or "about:blank"],
                    capture_output=True, text=True, timeout=30,
                    env={**os.environ, "NODE_OPTIONS": "--no-warnings"},
                )
                if result.returncode != 0:
                    return f"[Browser/PlaywrightMCP] JS hatasi: {result.stderr.strip()[:500]}"
                return f"[Browser/PlaywrightMCP] JS sonucu: {result.stdout.strip()[:1000]}"

            elif eylem == "tikla":
                if not secici:
                    return "[Browser/PlaywrightMCP] Hata: 'secici' parametresi gerekli."
                result = subprocess.run(
                    ["npx", "--yes", "@playwright/mcp", "click", secici, url or "about:blank"],
                    capture_output=True, text=True, timeout=30,
                    env={**os.environ, "NODE_OPTIONS": "--no-warnings"},
                )
                if result.returncode != 0:
                    return f"[Browser/PlaywrightMCP] Tiklama hatasi: {result.stderr.strip()[:500]}"
                return f"[Browser/PlaywrightMCP] Tiklandi: {secici}"

            elif eylem == "fill":
                if not secici or not deger:
                    return "[Browser/PlaywrightMCP] Hata: 'secici' ve 'deger' parametreleri gerekli."
                result = subprocess.run(
                    ["npx", "--yes", "@playwright/mcp", "fill", secici, deger, url or "about:blank"],
                    capture_output=True, text=True, timeout=30,
                    env={**os.environ, "NODE_OPTIONS": "--no-warnings"},
                )
                if result.returncode != 0:
                    return f"[Browser/PlaywrightMCP] Fill hatasi: {result.stderr.strip()[:500]}"
                return f"[Browser/PlaywrightMCP] Dolduruldu: {secici} = {deger[:50]}"

            elif eylem == "snapshot":
                result = subprocess.run(
                    ["npx", "--yes", "@playwright/mcp", "content", url or "about:blank"],
                    capture_output=True, text=True, timeout=30,
                    env={**os.environ, "NODE_OPTIONS": "--no-warnings"},
                )
                if result.returncode != 0:
                    return f"[Browser/PlaywrightMCP] Snapshot hatasi: {result.stderr.strip()[:500]}"
                metin = result.stdout.strip()[:3000]
                return f"[Browser/PlaywrightMCP] Sayfa ({len(result.stdout)} char):\n{metin}"

            elif eylem == "durum":
                return (
                    "[Browser/PlaywrightMCP] Durum: hazir.\n"
                    "  Eylemler: ac, screenshot, js/evaluate, tikla, fill, html, snapshot, durum"
                )

            else:
                return (
                    f"[Browser/PlaywrightMCP] Bilinmeyen eylem: '{eylem}'.\n"
                    f"  Desteklenen: ac, screenshot, js, tikla, fill, html, snapshot, durum"
                )

        except FileNotFoundError:
            return "[Browser/PlaywrightMCP] Hata: Node.js/npx bulunamadi. Node.js kurulu mu?"
        except subprocess.TimeoutExpired:
            return "[Browser/PlaywrightMCP] Hata: Zaman asimi (30sn)."
        except Exception as e:
            log.exception("[PlaywrightMCPEngine] Hata:")
            return f"[Browser/PlaywrightMCP] Hata: {e}"


# ═══════════════════════════════════════════════════════════════════════════════
# Browser Use Engine
# ═══════════════════════════════════════════════════════════════════════════════

class BrowserUseEngine(BrowserEngine):
    """browser-use kütüphanesi ile tarayıcı otomasyonu.

    pip install browser-use gerektirir.
    """

    @property
    def ad(self) -> str:
        return "browser_use"

    def _bagimliliklari_kontrol_et(self) -> bool:
        try:
            import browser_use  # noqa: F401
            return True
        except ImportError:
            return False

    def calistir(self, eylem: str, **kwargs: Any) -> str:
        """Browser-use ile tarayıcı eylemi.

        Desteklenen eylemler: ac, screenshot, tikla, fill, js, durum
        """
        url = kwargs.get("url", "")
        secici = kwargs.get("secici", "")
        deger = kwargs.get("deger", "")
        js_kod = kwargs.get("js", "document.title")
        dosya = kwargs.get("dosya", "browser_screenshot.png")

        if not self.hazir:
            return "[Browser/BrowserUse] Hata: browser-use kutuphanesi yuklu degil. 'pip install browser-use'"

        try:
            # browser-use'ün async yapısı nedeniyle asyncio.run ile çalıştır
            import asyncio

            if eylem == "ac":
                return asyncio.run(self._browser_use_ac(url))
            elif eylem == "screenshot":
                return asyncio.run(self._browser_use_screenshot(url, dosya))
            elif eylem == "js":
                return asyncio.run(self._browser_use_js(url, js_kod))
            elif eylem == "tikla":
                return asyncio.run(self._browser_use_tikla(url, secici))
            elif eylem == "fill":
                return asyncio.run(self._browser_use_fill(url, secici, deger))
            elif eylem == "snapshot":
                return asyncio.run(self._browser_use_snapshot(url))
            elif eylem == "durum":
                return (
                    "[Browser/BrowserUse] Durum: hazir.\n"
                    "  Eylemler: ac, screenshot, js, tikla, fill, snapshot, durum\n"
                    "  Not: browser-use async tabanlidir, her eylem ayri bir oturum acar."
                )
            else:
                return (
                    f"[Browser/BrowserUse] Bilinmeyen eylem: '{eylem}'.\n"
                    f"  Desteklenen: ac, screenshot, js, tikla, fill, snapshot, durum"
                )

        except ImportError as e:
            return f"[Browser/BrowserUse] Hata: {e}"
        except Exception as e:
            log.exception("[BrowserUseEngine] Hata:")
            return f"[Browser/BrowserUse] Hata: {e}"

    # ── Async helpers ──────────────────────────────────────────────────────────

    async def _browser_use_ac(self, url: str) -> str:
        if not url:
            return "[Browser/BrowserUse] Hata: 'url' parametresi gerekli."
        try:
            from browser_use import Agent
            agent = Agent(
                task=f"Navigate to {url} and tell me the page title",
                llm=None,  # LLM gerekmez, sadece gezinme
            )
            history = await agent.run(max_steps=5)
            return f"[Browser/BrowserUse] Sayfa acildi: {url}\n{str(history)[:1000]}"
        except Exception as e:
            return f"[Browser/BrowserUse] Acma hatasi: {e}"

    async def _browser_use_screenshot(self, url: str, dosya: str) -> str:
        try:
            from browser_use import Agent
            agent = Agent(
                task=f"Go to {url or 'about:blank'} and take a screenshot, save to {dosya}",
                llm=None,
            )
            history = await agent.run(max_steps=5)
            if os.path.exists(dosya):
                return f"[Browser/BrowserUse] Screenshot alindi: {dosya}"
            return f"[Browser/BrowserUse] Screenshot denendi. Agent ciktisi:\n{str(history)[:500]}"
        except Exception as e:
            return f"[Browser/BrowserUse] Screenshot hatasi: {e}"

    async def _browser_use_js(self, url: str, js_kod: str) -> str:
        try:
            from browser_use import Agent
            agent = Agent(
                task=f"Go to {url or 'about:blank'}, execute JavaScript: {js_kod}, return the result",
                llm=None,
            )
            history = await agent.run(max_steps=5)
            return f"[Browser/BrowserUse] JS sonucu:\n{str(history)[:1000]}"
        except Exception as e:
            return f"[Browser/BrowserUse] JS hatasi: {e}"

    async def _browser_use_tikla(self, url: str, secici: str) -> str:
        if not secici:
            return "[Browser/BrowserUse] Hata: 'secici' parametresi gerekli."
        try:
            from browser_use import Agent
            agent = Agent(
                task=f"Go to {url or 'about:blank'}, click on element matching '{secici}'",
                llm=None,
            )
            history = await agent.run(max_steps=10)
            return f"[Browser/BrowserUse] Tiklandi: {secici}\n{str(history)[:500]}"
        except Exception as e:
            return f"[Browser/BrowserUse] Tiklama hatasi: {e}"

    async def _browser_use_fill(self, url: str, secici: str, deger: str) -> str:
        if not secici or not deger:
            return "[Browser/BrowserUse] Hata: 'secici' ve 'deger' gerekli."
        try:
            from browser_use import Agent
            agent = Agent(
                task=f"Go to {url or 'about:blank'}, fill in '{secici}' with '{deger}'",
                llm=None,
            )
            history = await agent.run(max_steps=10)
            return f"[Browser/BrowserUse] Dolduruldu: {secici} = {deger[:50]}\n{str(history)[:500]}"
        except Exception as e:
            return f"[Browser/BrowserUse] Fill hatasi: {e}"

    async def _browser_use_snapshot(self, url: str) -> str:
        try:
            from browser_use import Agent
            agent = Agent(
                task=f"Go to {url or 'about:blank'} and extract the page text content",
                llm=None,
            )
            history = await agent.run(max_steps=5)
            return f"[Browser/BrowserUse] Sayfa icerigi:\n{str(history)[:3000]}"
        except Exception as e:
            return f"[Browser/BrowserUse] Snapshot hatasi: {e}"


# ═══════════════════════════════════════════════════════════════════════════════
# Browser Registry
# ═══════════════════════════════════════════════════════════════════════════════

class BrowserRegistry:
    """Tarayıcı otomasyon engine'lerini kaydet, seç ve çalıştır."""

    def __init__(self) -> None:
        self._engines: dict[str, BrowserEngine] = {}
        self._varsayilan: Optional[str] = None

    def kaydet(self, engine: BrowserEngine) -> None:
        adi = engine.ad
        self._engines[adi] = engine
        if self._varsayilan is None:
            self._varsayilan = adi
        # Varsayılan: hazır olanı tercih et
        if engine.hazir:
            self._varsayilan = adi
        log.info("[BrowserRegistry] Engine kaydedildi: %s (hazir=%s, varsayilan=%s)",
                 adi, engine.hazir, self._varsayilan)

    def sec(self, ad: str) -> Optional[BrowserEngine]:
        eng = self._engines.get(ad)
        if eng is None and self._varsayilan:
            log.warning("[BrowserRegistry] '%s' bulunamadi, varsayilana dusuluyor: %s", ad, self._varsayilan)
            return self._engines.get(self._varsayilan)
        return eng

    @property
    def varsayilan(self) -> Optional[BrowserEngine]:
        return self._engines.get(self._varsayilan) if self._varsayilan else None

    def calistir(self, engine_adi: str, eylem: str, **kwargs: Any) -> str:
        eng = self.sec(engine_adi)
        if eng is None:
            return f"[BROWSER] '{engine_adi}' engine'i bulunamadi."
        if not eng.hazir:
            return (f"[BROWSER] '{engine_adi}' hazir degil.\n"
                    f"  PlaywrightMCP icin: npm install -g @playwright/mcp && npx playwright install\n"
                    f"  BrowserUse icin: pip install browser-use")
        try:
            return eng.calistir(eylem, **kwargs)
        except Exception as e:
            log.exception("[BrowserRegistry] '%s' calistirma hatasi:", engine_adi)
            return f"[BROWSER] '{engine_adi}' hatasi: {e}"


# ── Global registry singleton ──────────────────────────────────────────────────

_registry: Optional[BrowserRegistry] = None


def _get_registry() -> BrowserRegistry:
    global _registry
    if _registry is None:
        _registry = BrowserRegistry()
        try:
            _registry.kaydet(PlaywrightMCPEngine())
        except Exception as e:
            log.warning("[BrowserRegistry] PlaywrightMCPEngine yuklenemedi: %s", e)
        try:
            _registry.kaydet(BrowserUseEngine())
        except Exception as e:
            log.warning("[BrowserRegistry] BrowserUseEngine yuklenemedi: %s", e)
    return _registry


# ═══════════════════════════════════════════════════════════════════════════════
# Tool Fonksiyonu
# ═══════════════════════════════════════════════════════════════════════════════

def browser_calistir(eylem: str, url: str = "", secici: str = "", deger: str = "",
                     js: str = "", dosya: str = "", backend: str = "") -> str:
    """BROWSER_CALISTIR tool'u — backend parametresi ile çoklu tarayıcı otomasyonu.

    Args:
        eylem: Yapilacak islem (ac, screenshot, js, tikla, fill, html, snapshot, durum).
        url: Hedef URL.
        secici: CSS secici (tikla/fill icin).
        deger: Deger (fill icin).
        js: JavaScript kodu.
        dosya: Screenshot cikti dosyasi.
        backend: Kullanilacak engine (playwright_mcp, browser_use).
                Bos birakilirsa varsayilan kullanilir.

    Returns:
        Islem sonucu metin.
    """
    reg = _get_registry()
    engine_adi = backend.strip() if backend.strip() else ""

    # Varsayilan engine bul
    if not engine_adi:
        eng = reg.varsayilan
        if eng is None:
            return "[BROWSER] Hata: hicbir engine kayitli degil."
        engine_adi = eng.ad

    return reg.calistir(engine_adi, eylem, url=url, secici=secici,
                        deger=deger, js=js, dosya=dosya)


def browser_engine_listele() -> str:
    """Kayitli engine'leri listele."""
    reg = _get_registry()
    satirlar = ["[BROWSER] Kayitli engine'ler:"]
    for ad, eng in reg._engines.items():
        durum = "hazir" if eng.hazir else "bagimlilik eksik"
        isaret = " >" if ad == reg._varsayilan else "  "
        satirlar.append(f"  {isaret} {ad} ({durum})")
        satirlar.append(f"       {eng.aciklama}")
    return "\n".join(satirlar)


# ═══════════════════════════════════════════════════════════════════════════════
# Motor Kayit
# ═══════════════════════════════════════════════════════════════════════════════

def motor_kaydet(motor) -> None:
    """Motor tarafindan otomatik cagrilir. BROWSER_CALISTIR tool'unu kaydeder."""
    if not hasattr(motor, "_plugin_arac_kaydet"):
        return
    try:
        motor._plugin_arac_kaydet(
            "BROWSER_CALISTIR",
            lambda ham="": _browser_ayristir_ve_calistir(ham),
            "Tarayici otomasyonu yapar (coklu back-end)."
            " Kullanim: BROWSER_CALISTIR(eylem=\"ac|screenshot|js|tikla|fill|snapshot|durum\", "
            "url=\"...\", secici=\"...\", deger=\"...\", js=\"...\", dosya=\"...\", "
            "backend=\"playwright_mcp|browser_use\")\n"
            "PlaywrightMCP: npx @playwright/mcp gerekli (npm install -g @playwright/mcp)\n"
            "BrowserUse: pip install browser-use gerekli\n"
            "Varsayilan: hazir olan engine.",
        )
        motor._plugin_arac_kaydet(
            "BROWSER_BACKEND_LISTELE",
            lambda: browser_engine_listele(),
            "Kullanilabilir tarayici engine'lerini listeler.",
        )
    except Exception as e:
        log.warning("[BrowserEngine] Motor kayit hatasi: %s", e)


def _browser_ayristir_ve_calistir(ham: str) -> str:
    """BROWSER_CALISTIR(ham) -> parametre ayristir."""
    import re as _re
    eylem = ""
    url = ""
    secici = ""
    deger = ""
    js = ""
    dosya = ""
    backend = ""

    e_match = _re.search(r'eylem\s*=\s*"([^"]*)"', ham)
    if e_match:
        eylem = e_match.group(1)

    u_match = _re.search(r'url\s*=\s*"([^"]*)"', ham)
    if u_match:
        url = u_match.group(1)

    s_match = _re.search(r'secici\s*=\s*"([^"]*)"', ham)
    if s_match:
        secici = s_match.group(1)

    d_match = _re.search(r'deger\s*=\s*"([^"]*)"', ham)
    if d_match:
        deger = d_match.group(1)

    j_match = _re.search(r'js\s*=\s*"([^"]*)"', ham)
    if j_match:
        js = j_match.group(1)

    f_match = _re.search(r'dosya\s*=\s*"([^"]*)"', ham)
    if f_match:
        dosya = f_match.group(1)

    b_match = _re.search(r'backend\s*=\s*"([^"]*)"', ham)
    if b_match:
        backend = b_match.group(1)

    if not eylem:
        eylem = ham.strip().strip('"').strip("'")

    return browser_calistir(eylem, url=url, secici=secici,
                            deger=deger, js=js, dosya=dosya, backend=backend)


# ═══════════════════════════════════════════════════════════════════════════════
# Test
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(browser_engine_listele())
    print("\n--- Durum Test ---")
    print(browser_calistir("durum"))
