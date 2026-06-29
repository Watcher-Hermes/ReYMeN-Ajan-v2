# -*- coding: utf-8 -*-
"""schema_manager.py — ReYMeN Schema Versionlama Yoneticisi.

Alembic + SQLite PRAGMA user_version ile tum veritabanlarinin
schema versiyonlarini takip eder, migrate eder ve raporlar.

Desteklenen DB'ler:
  - session.db (ana konusma DB) — Alembic ile
  - self_improve.db — PRAGMA user_version ile
  - hata_toplama.db — PRAGMA user_version ile
  - ogrenmeler.db — PRAGMA user_version ile
"""

import json
import logging
import sqlite3
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)

PROJE_KOK = Path(__file__).parent.parent.parent  # ReYMeN-Ajan/

# Tum veritabanlari
VERITABANLARI = {
    "session": {
        "yol": PROJE_KOK / ".ReYMeN" / "session.db",
        "alembic": True,
        "aciklama": "Konusma oturumlari ve mesajlar",
        "versiyon": 1,
    },
    "self_improve": {
        "yol": PROJE_KOK / "reymen" / "sistem" / "self_improve.db",
        "alembic": False,
        "aciklama": "Kendini-gelistirme metrikleri",
        "versiyon": 1,
    },
    "hata_toplama": {
        "yol": PROJE_KOK / "reymen" / "sistem" / "hata_toplama.db",
        "alembic": False,
        "aciklama": "Merkezi hata kayitlari",
        "versiyon": 1,
    },
    "ogrenmeler": {
        "yol": PROJE_KOK / "reymen" / "cereyan" / "ogrenmeler.db",
        "alembic": False,
        "aciklama": "Ogrenme hafizasi",
        "versiyon": 1,
    },
    "karar": {
        "yol": PROJE_KOK / "reymen" / "cereyan" / ".ReYMeN" / "karar.db",
        "alembic": False,
        "aciklama": "Karar kayitlari",
        "versiyon": 1,
    },
}


class SchemaManager:
    """Schema versiyonlama yoneticisi."""

    def __init__(self):
        self._alembic_ini = str(PROJE_KOK / "alembic.ini")

    # ── Versiyon Sorgulama ────────────────────────────────────────────

    def versiyon_al(self, db_adi: str) -> str:
        """Bir DB'nin mevcut schema versiyonunu al.

        Alembic DB'ler icin revision hash,
        digerleri icin PRAGMA user_version kullanilir.
        """
        bilgi = VERITABANLARI.get(db_adi)
        if not bilgi:
            return "0"

        yol = bilgi["yol"]
        if not yol.exists():
            return "0"

        try:
            conn = sqlite3.connect(str(yol))
            if bilgi["alembic"]:
                cur = conn.execute(
                    "SELECT version_num FROM alembic_version_session ORDER BY rowid DESC LIMIT 1"
                )
                row = cur.fetchone()
                conn.close()
                return str(row[0]) if row else "0"
            else:
                cur = conn.execute("PRAGMA user_version")
                versiyon = cur.fetchone()[0]
                conn.close()
                return str(versiyon)
        except Exception as e:
            logger.error("[Schema] %s versiyon okuma hatasi: %s", db_adi, e)
            return "-1"

    def versiyon_beklenen(self, db_adi: str) -> str:
        """Bir DB icin beklenen (guncel) versiyon."""
        bilgi = VERITABANLARI.get(db_adi)
        return str(bilgi["versiyon"]) if bilgi else "0"

    def guncel_mi(self, db_adi: str) -> bool:
        """DB guncel versiyonda mi?

        Alembic DB'ler: version_num varsa gunceldir (hash bazli).
        PRAGMA DB'ler: user_version >= beklenen versiyon.
        """
        bilgi = VERITABANLARI.get(db_adi)
        if not bilgi:
            return False

        mevcut = self.versiyon_al(db_adi)

        if bilgi["alembic"]:
            # Alembic: hash varsa guncel (v0 degilse)
            return mevcut not in ("0", "-1", "")
        try:
            return int(mevcut) >= int(self.versiyon_beklenen(db_adi))
        except (ValueError, TypeError):
            return False

    # ── Migration ─────────────────────────────────────────────────────

    def migrate(self, db_adi: str) -> dict:
        """Bir DB'yi en son versiyona migrate et.

        Returns:
            dict: {"basarili": bool, "mesaj": str, "onceki": int, "sonra": int}
        """
        bilgi = VERITABANLARI.get(db_adi)
        if not bilgi:
            return {"basarili": False, "mesaj": f"Bilinmeyen DB: {db_adi}"}

        onceki = self.versiyon_al(db_adi)

        if bilgi["alembic"]:
            return self._alembic_migrate(db_adi, onceki)
        else:
            return self._pragma_migrate(db_adi, onceki, bilgi)

    def _alembic_migrate(self, db_adi: str, onceki: int) -> dict:
        """Alembik ile migrate et (session.db)."""
        try:
            sonuc = subprocess.run(
                [sys.executable, "-m", "alembic", "-c", self._alembic_ini, "upgrade", "head"],
                capture_output=True, text=True, timeout=60,
                cwd=str(PROJE_KOK),
            )
            sonra = self.versiyon_al(db_adi)
            if sonuc.returncode == 0:
                return {
                    "basarili": True,
                    "mesaj": f"Alembic migration basarili",
                    "onceki": onceki,
                    "sonra": sonra,
                    "cikti": sonuc.stdout.strip(),
                }
            return {
                "basarili": False,
                "mesaj": f"Alembic migration basarisiz: {sonuc.stderr[:500]}",
                "onceki": onceki,
                "sonra": sonra,
            }
        except Exception as e:
            return {"basarili": False, "mesaj": f"Alembic hatasi: {e}", "onceki": onceki, "sonra": onceki}

    def _pragma_migrate(self, db_adi: str, onceki_str: str, bilgi: dict) -> dict:
        """PRAGMA user_version ile migrate et.

        Basit schema guncellemeleri icin SQL script calistirir.
        """
        yol = bilgi["yol"]
        hedef = bilgi["versiyon"]

        try:
            onceki = int(onceki_str)
        except (ValueError, TypeError):
            onceki = 0

        if onceki >= hedef:
            return {
                "basarili": True,
                "mesaj": f"Zaten guncel (v{onceki})",
                "onceki": onceki,
                "sonra": onceki,
            }

        try:
            conn = sqlite3.connect(str(yol))
            for v in range(onceki + 1, hedef + 1):
                script = self._migration_script(db_adi, v)
                if script:
                    conn.executescript(script)
                conn.execute(f"PRAGMA user_version = {v}")
            conn.commit()
            conn.close()

            sonra = self.versiyon_al(db_adi)
            return {
                "basarili": True,
                "mesaj": f"v{onceki} -> v{sonra} migrate edildi",
                "onceki": onceki,
                "sonra": sonra,
            }
        except Exception as e:
            return {"basarili": False, "mesaj": f"PRAGMA migrate hatasi: {e}", "onceki": onceki, "sonra": onceki}

    def _migration_script(self, db_adi: str, versiyon: int) -> str:
        """Belirli bir versiyon guncellemesi icin SQL script.

        Yeni tablo/sutun eklemeleri buraya eklenir.
        """
        scripts = {
            "self_improve": {
                1: """
                    CREATE TABLE IF NOT EXISTS metrics (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        metric_name TEXT NOT NULL,
                        metric_value REAL NOT NULL,
                        category TEXT DEFAULT '',
                        metadata TEXT DEFAULT '{}'
                    );
                    CREATE TABLE IF NOT EXISTS improvement_goals (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        created_at TEXT NOT NULL,
                        goal TEXT NOT NULL,
                        status TEXT DEFAULT 'active',
                        progress REAL DEFAULT 0.0,
                        completed_at TEXT
                    );
                    CREATE TABLE IF NOT EXISTS code_quality_snapshots (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        total_files INTEGER DEFAULT 0,
                        total_lines INTEGER DEFAULT 0,
                        test_count INTEGER DEFAULT 0,
                        coverage REAL DEFAULT 0.0,
                        details TEXT DEFAULT '{}'
                    );
                """,
            },
            "hata_toplama": {
                1: """
                    CREATE TABLE IF NOT EXISTS hata_kayitlari (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        zaman TEXT NOT NULL,
                        modul TEXT NOT NULL DEFAULT '',
                        arac TEXT NOT NULL DEFAULT '',
                        hata_tipi TEXT NOT NULL DEFAULT '',
                        hata_mesaji TEXT NOT NULL DEFAULT '',
                        seviye TEXT NOT NULL DEFAULT 'UYARI',
                        frekans_imzasi TEXT NOT NULL DEFAULT '',
                        ek_bilgi TEXT NOT NULL DEFAULT '{}',
                        cozuldu_mu INTEGER NOT NULL DEFAULT 0,
                        bildirim_gonderildi_mi INTEGER NOT NULL DEFAULT 0
                    );
                    CREATE INDEX IF NOT EXISTS idx_hata_zaman ON hata_kayitlari(zaman);
                    CREATE INDEX IF NOT EXISTS idx_hata_imza ON hata_kayitlari(frekans_imzasi);
                """,
            },
            "ogrenmeler": {
                1: """
                    CREATE TABLE IF NOT EXISTS ogrenmeler (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        hedef TEXT NOT NULL,
                        cozum TEXT NOT NULL,
                        kategori TEXT DEFAULT 'genel',
                        basari INTEGER DEFAULT 0,
                        hata INTEGER DEFAULT 0,
                        guven_skoru FLOAT DEFAULT 0.5,
                        son_kullanim DATE DEFAULT (date('now')),
                        kaynak_url TEXT DEFAULT '',
                        gecerlilik_tarihi DATE DEFAULT (date('now', '+180 days')),
                        olusturma DATE DEFAULT (date('now'))
                    );
                """,
            },
            "karar": {
                1: """
                    CREATE TABLE IF NOT EXISTS kararlar (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        zaman TEXT NOT NULL,
                        karar TEXT NOT NULL,
                        gerekce TEXT DEFAULT '',
                        sonuc TEXT DEFAULT '',
                        session_id TEXT DEFAULT ''
                    );
                """,
            },
        }
        return scripts.get(db_adi, {}).get(versiyon, "")

    # ── Tum DB'leri Migrate Et ────────────────────────────────────────

    def tumunu_migrate(self) -> list[dict]:
        """Tum veritabanlarini migrate et.

        Returns:
            list[dict]: Her DB icin sonuc
        """
        sonuclar = []
        for db_adi in VERITABANLARI:
            sonuc = self.migrate(db_adi)
            sonuclar.append({"db": db_adi, **sonuc})
            if sonuc["basarili"]:
                logger.info("[Schema] %s: %s", db_adi, sonuc["mesaj"])
            else:
                logger.warning("[Schema] %s: %s", db_adi, sonuc["mesaj"])
        return sonuclar

    # ── Durum Raporu ──────────────────────────────────────────────────

    def durum(self) -> dict[str, Any]:
        """Tum DB'lerin versiyon durumu."""
        return {
            db_adi: {
                "mevcut": self.versiyon_al(db_adi),
                "beklenen": self.versiyon_beklenen(db_adi),
                "guncel": self.guncel_mi(db_adi),
                "yol": str(bilgi["yol"]),
                "aciklama": bilgi["aciklama"],
                "var_mi": bilgi["yol"].exists(),
            }
            for db_adi, bilgi in VERITABANLARI.items()
        }

    def durum_text(self) -> str:
        """Insan-okunabilir durum raporu."""
        satirlar = ["[SchemaManager] Veritabani Versiyon Durumu:", "=" * 50]
        for db_adi, d in self.durum().items():
            # Versiyonu formatla
            mevcut = d["mevcut"]
            beklenen = d["beklenen"]
            if mevcut is None or mevcut == -1:
                mevcut_str = "HATA"
            else:
                mevcut_str = f"v{mevcut}"
            guncel = "🟢" if d["guncel"] else ("🟡" if mevcut is None else "🔴")
            var = "✅" if d["var_mi"] else "❌"
            satirlar.append(
                f"  {guncel} {db_adi:<16} {mevcut_str:>5} / v{beklenen}  {var}  {d['aciklama']}"
            )
        return "\n".join(satirlar)


# ── Singleton ──────────────────────────────────────────────────────────────

_SCHEMA: Optional[SchemaManager] = None


def schema_manager() -> SchemaManager:
    global _SCHEMA
    if _SCHEMA is None:
        _SCHEMA = SchemaManager()
    return _SCHEMA


def motor_kaydet(motor):
    """Motor'a schema yonetim araclarini kaydet."""
    yonetici = schema_manager()

    if hasattr(motor, "_plugin_arac_kaydet"):
        motor._plugin_arac_kaydet(
            "SCHEMA_DURUM",
            lambda: schema_manager().durum_text(),
            "Veritabani schema versiyon durumu",
        )
        motor._plugin_arac_kaydet(
            "SCHEMA_MIGRATE",
            lambda db="": _schema_migrate_arac(db),
            "Veritabanini migrate et. Parametre: db_adi (bos=batch: tumu). "
            "DB'ler: session, self_improve, hata_toplama, ogrenmeler, karar",
        )
        logger.info("[Schema] Motor'a 2 arac kaydedildi")


def _schema_migrate_arac(db_adi: str) -> str:
    """Schema migrate arac wrapper."""
    yonetici = schema_manager()
    if not db_adi or db_adi.strip() == "":
        sonuclar = yonetici.tumunu_migrate()
        satirlar = ["[Schema] Tum DB migrate edildi:"]
        for s in sonuclar:
            ikon = "✅" if s["basarili"] else "❌"
            satirlar.append(f"  {ikon} {s['db']}: {s['mesaj']}")
        return "\n".join(satirlar)
    sonuc = yonetici.migrate(db_adi.strip())
    ikon = "✅" if sonuc["basarili"] else "❌"
    return f"{ikon} {db_adi}: {sonuc['mesaj']}"


# ── CLI Test ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    yonetici = schema_manager()
    print(yonetici.durum_text())
    print()
    print("Migrate ediliyor...")
    sonuclar = yonetici.tumunu_migrate()
    for s in sonuclar:
        print(f"  {s['db']}: {s['mesaj']}")
    print()
    print(yonetici.durum_text())
