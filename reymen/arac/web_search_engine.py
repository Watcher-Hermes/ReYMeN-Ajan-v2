# -*- coding: utf-8 -*-
"""
web_search_engine.py — Çok back-end'li web arama motoru (ABC tabanlı).

WebSearchEngine ABC:
  - Soyut calistir(sorgu, max_sonuc) → str

Engine'ler:
  - DuckDuckGoEngine  — duckduckgo-search kütüphanesi (öncelikli) / DDG Lite HTML (fallback)
  - GoogleEngine      — stub (GOOGLE_API_KEY gerektirir, NotImplementedError)
  - BingEngine        — stub (BING_API_KEY gerektirir, NotImplementedError)

WebSearchRegistry:
  - engine kaydet / seç (ad ile) / calistir (engine adı + sorgu ile)
  - Varsayılan engine: duckduckgo

Motor tool:
  WEB_ARAMA(sorgu, backend="duckduckgo") → str
"""

from __future__ import annotations

import json
import logging
import os
import time
import urllib.parse
import urllib.request
from abc import ABC, abstractmethod
from html.parser import HTMLParser
from typing import Optional

log = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# Soyut Taban Sınıfı
# ═══════════════════════════════════════════════════════════════════════════════

class WebSearchEngine(ABC):
    """Tüm web arama engine'leri için soyut taban sınıfı."""

    @property
    @abstractmethod
    def ad(self) -> str:
        """Engine'in benzersiz adı (küçük harf)."""

    @abstractmethod
    def calistir(self, sorgu: str, max_sonuc: int = 5) -> str:
        """Web araması yap, formatlı metin döndür."""
        ...

    def __init__(self) -> None:
        self._hazir = self._bagimliliklari_kontrol_et()

    def _bagimliliklari_kontrol_et(self) -> bool:
        """Alt sınıflar override edebilir. Varsayılan: True."""
        return True

    @property
    def hazir(self) -> bool:
        """Engine kullanıma hazır mı?"""
        return self._hazir


# ═══════════════════════════════════════════════════════════════════════════════
# DuckDuckGo Engine
# ═══════════════════════════════════════════════════════════════════════════════

class DuckDuckGoEngine(WebSearchEngine):
    """DuckDuckGo arama engine'i. API key gerekmez.

    Öncelik: duckduckgo-search kütüphanesi
    Fallback: DDG Lite HTML scraping
    """

    @property
    def ad(self) -> str:
        return "duckduckgo"

    def _bagimliliklari_kontrol_et(self) -> bool:
        # duckduckgo-search isteğe bağlı — hiçbiri yoksa Lite HTML fallback çalışır
        return True

    def _ddgs_library_ara(self, sorgu: str, max_sonuc: int = 5) -> Optional[list[dict]]:
        try:
            # duckduckgo_search -> ddgs (yeni paket adi)
            try:
                from ddgs import DDGS
            except ImportError:
                from duckduckgo_search import DDGS
            ddgs = DDGS()
            results = list(ddgs.text(sorgu, max_results=max_sonuc))
            if hasattr(ddgs, "close"):
                ddgs.close()
            if results:
                return [
                    {"href": r.get("href", ""), "title": r.get("title", ""), "body": r.get("body", "")}
                    for r in results
                ]
        except Exception as e:
            log.debug("duckduckgo-search kutuphanesi calismadi: %s", e)
        return None

    def _ddg_lite_ara(self, sorgu: str, max_sonuc: int = 5) -> list[dict]:
        class _Parser(HTMLParser):
            def __init__(self):
                super().__init__()
                self.results: list[dict] = []
                self._current: Optional[dict] = None
                self._in_link = False
                self._skip_domains = {"duckduckgo.com", "wikipedia.org"}

            def handle_starttag(self, tag, attrs):
                ad = dict(attrs)
                if tag == "a" and "href" in ad:
                    href = ad["href"]
                    if href.startswith("http") and not any(d in href for d in self._skip_domains):
                        self._in_link = True
                        self._current = {"href": href, "title": "", "body": ""}

            def handle_data(self, data):
                if self._in_link and self._current is not None:
                    self._current["title"] += data.strip()

            def handle_endtag(self, tag):
                if tag == "a" and self._current is not None and self._current.get("title", "").strip():
                    self.results.append(self._current)
                    self._current = None
                    self._in_link = False

        try:
            url = "https://lite.duckduckgo.com/lite/"
            data = urllib.parse.urlencode({"q": sorgu}).encode()
            req = urllib.request.Request(url, data=data)
            req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
            req.add_header("Accept", "text/html")
            resp = urllib.request.urlopen(req, timeout=15)
            html = resp.read().decode("utf-8", errors="replace")
            parser = _Parser()
            parser.feed(html)
            return parser.results[:max_sonuc]
        except Exception as e:
            log.debug("DDG Lite scraping hatasi: %s", e)
            return []

    def calistir(self, sorgu: str, max_sonuc: int = 5) -> str:
        results = self._ddgs_library_ara(sorgu, max_sonuc)
        if results is None:
            results = self._ddg_lite_ara(sorgu, max_sonuc)

        if not results:
            return "Sonuc bulunamadi."

        satirlar = []
        for i, r in enumerate(results, 1):
            title = (r.get("title") or "").strip()
            href = (r.get("href") or "").strip()
            body = (r.get("body") or "").strip()[:200]
            satirlar.append(f"[{i}] {title}")
            if href:
                satirlar.append(f"     {href}")
            if body:
                satirlar.append(f"     {body}")
        return "\n".join(satirlar)


# ═══════════════════════════════════════════════════════════════════════════════
# Google Engine (Stub)
# ═══════════════════════════════════════════════════════════════════════════════

class GoogleEngine(WebSearchEngine):
    """Google Custom Search JSON API stub.

    GOOGLE_API_KEY + GOOGLE_CX ortam değişkenleri gerekli.
    Mevcut değilse NotImplementedError fırlatır.
    """

    @property
    def ad(self) -> str:
        return "google"

    def _bagimliliklari_kontrol_et(self) -> bool:
        api_key = os.environ.get("GOOGLE_API_KEY", "").strip()
        cx = os.environ.get("GOOGLE_CX", "").strip()
        return bool(api_key and cx)

    def calistir(self, sorgu: str, max_sonuc: int = 5) -> str:
        api_key = os.environ.get("GOOGLE_API_KEY", "").strip()
        cx = os.environ.get("GOOGLE_CX", "").strip()
        if not api_key or not cx:
            raise NotImplementedError(
                "GoogleEngine: GOOGLE_API_KEY ve GOOGLE_CX ortam değişkenleri gerekli."
            )
        raise NotImplementedError(
            "GoogleEngine henüz implemente edilmedi. "
            "GOOGLE_API_KEY ve GOOGLE_CX ayarlandı ancak HTTP istemcisi eksik."
        )


# ═══════════════════════════════════════════════════════════════════════════════
# Bing Engine (Stub)
# ═══════════════════════════════════════════════════════════════════════════════

class BingEngine(WebSearchEngine):
    """Bing Web Search API stub.

    BING_API_KEY ortam değişkeni gerekli.
    Mevcut değilse NotImplementedError fırlatır.
    """

    @property
    def ad(self) -> str:
        return "bing"

    def _bagimliliklari_kontrol_et(self) -> bool:
        return bool(os.environ.get("BING_API_KEY", "").strip())

    def calistir(self, sorgu: str, max_sonuc: int = 5) -> str:
        api_key = os.environ.get("BING_API_KEY", "").strip()
        if not api_key:
            raise NotImplementedError(
                "BingEngine: BING_API_KEY ortam değişkeni gerekli."
            )
        raise NotImplementedError(
            "BingEngine henüz implemente edilmedi. "
            "BING_API_KEY ayarlandı ancak HTTP istemcisi eksik."
        )


# ═══════════════════════════════════════════════════════════════════════════════
# Web Search Registry
# ═══════════════════════════════════════════════════════════════════════════════

class WebSearchRegistry:
    """Web arama engine'lerini kaydet, seç ve çalıştır."""

    def __init__(self) -> None:
        self._engines: dict[str, WebSearchEngine] = {}
        self._varsayilan: Optional[str] = None

    def kaydet(self, engine: WebSearchEngine) -> None:
        """Bir engine kaydet."""
        adi = engine.ad
        self._engines[adi] = engine
        if self._varsayilan is None:
            self._varsayilan = adi
        log.info("[WebSearchRegistry] Engine kaydedildi: %s", adi)

    def sec(self, ad: str) -> Optional[WebSearchEngine]:
        """Ada göre engine seç. Varsayılana düş."""
        eng = self._engines.get(ad)
        if eng is None and self._varsayilan:
            log.warning("[WebSearchRegistry] '%s' bulunamadi, varsayilana dusuluyor: %s", ad, self._varsayilan)
            return self._engines.get(self._varsayilan)
        return eng

    @property
    def varsayilan(self) -> Optional[WebSearchEngine]:
        return self._engines.get(self._varsayilan) if self._varsayilan else None

    def calistir(self, engin_adi: str, sorgu: str, max_sonuc: int = 5) -> str:
        """Belirtilen engine ile arama yap."""
        eng = self.sec(engin_adi)
        if eng is None:
            return f"[WEB_ARAMA] '{engin_adi}' engine'i bulunamadi ve varsayilan engine yok."
        if not eng.hazir:
            return f"[WEB_ARAMA] '{engin_adi}' engine'i hazir degil (bagimlilik eksik)."
        try:
            return eng.calistir(sorgu, max_sonuc)
        except NotImplementedError as e:
            return f"[WEB_ARAMA] '{engin_adi}' henuz implemente edilmemis: {e}"
        except Exception as e:
            log.exception("[WebSearchRegistry] '%s' calistirma hatasi:", engin_adi)
            return f"[WEB_ARAMA] '{engin_adi}' hatasi: {e}"


# ── Global registry singleton ──────────────────────────────────────────────────

_registry: Optional[WebSearchRegistry] = None


def _get_registry() -> WebSearchRegistry:
    global _registry
    if _registry is None:
        _registry = WebSearchRegistry()
        _registry.kaydet(DuckDuckGoEngine())
        _registry.kaydet(GoogleEngine())
        _registry.kaydet(BingEngine())
    return _registry


# ═══════════════════════════════════════════════════════════════════════════════
# Tool Fonksiyonu
# ═══════════════════════════════════════════════════════════════════════════════

def web_arama(sorgu: str, backend: str = "duckduckgo", max_sonuc: int = 5) -> str:
    """WEB_ARAMA tool'u — backend parametresi ile çoklu arama motoru.

    Args:
        sorgu: Arama sorgusu.
        backend: Kullanilacak engine adi (duckduckgo, google, bing).
        max_sonuc: Maksimum sonuc sayisi.

    Returns:
        Formatli arama sonuclari veya hata mesaji.
    """
    reg = _get_registry()
    return reg.calistir(backend, sorgu, max_sonuc)


def web_search_engine_listele() -> str:
    """Kayitli engine'leri listele."""
    reg = _get_registry()
    satirlar = ["[WEB_ARAMA] Kayitli engine'ler:"]
    for ad, eng in reg._engines.items():
        durum = "hazir" if eng.hazir else "bagimlilik eksik"
        isaret = " >" if ad == reg._varsayilan else "  "
        satirlar.append(f"  {isaret} {ad} ({durum})")
    return "\n".join(satirlar)


# ═══════════════════════════════════════════════════════════════════════════════
# Motor Kayit
# ═══════════════════════════════════════════════════════════════════════════════

def motor_kaydet(motor) -> None:
    """Motor tarafindan otomatik cagrilir. WEB_ARAMA tool'unu kaydeder."""
    if not hasattr(motor, "_plugin_arac_kaydet"):
        return
    try:
        motor._plugin_arac_kaydet(
            "WEB_ARAMA",
            lambda ham="": (
                # Parametre: sorgu, backend
                _web_arama_ayristir_ve_calistir(ham)
            ),
            "Web aramasi yapar (coklu back-end)."
            " Kullanim: WEB_ARAMA(sorgu=\"...\", backend=\"duckduckgo|google|bing\")\n"
            "Varsayilan backend: duckduckgo (API key gerekmez).\n"
            "Google icin GOOGLE_API_KEY+GOOGLE_CX, Bing icin BING_API_KEY gerekli.",
        )
        motor._plugin_arac_kaydet(
            "WEB_ARAMA_BACKEND_LISTELE",
            lambda: web_search_engine_listele(),
            "Kullanilabilir web arama engine'lerini listeler.",
        )
    except Exception as e:
        log.warning("[WebSearchEngine] Motor kayit hatasi: %s", e)


def _web_arama_ayristir_ve_calistir(ham: str) -> str:
    """WEB_ARAMA(ham) -> sorgu, backend ayristir."""
    import re as _re
    # Pattern: WEB_ARAMA(sorgu="...", backend="...")
    sorgu = ""
    backend = "duckduckgo"
    s_match = _re.search(r'sorgu\s*=\s*"([^"]*)"', ham)
    if s_match:
        sorgu = s_match.group(1)
    b_match = _re.search(r'backend\s*=\s*"([^"]*)"', ham)
    if b_match:
        backend = b_match.group(1)
    if not sorgu:
        # Fallback: tüm string'i sorgu olarak al
        sorgu = ham.strip().strip('"').strip("'")
    return web_arama(sorgu, backend)


# ═══════════════════════════════════════════════════════════════════════════════
# Test
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys
    print(web_search_engine_listele())
    sorgu = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "python asyncio nedir"
    print("\n--- DuckDuckGo ---")
    print(web_arama(sorgu, backend="duckduckgo"))
    print("\n--- Google (stub) ---")
    print(web_arama(sorgu, backend="google"))
