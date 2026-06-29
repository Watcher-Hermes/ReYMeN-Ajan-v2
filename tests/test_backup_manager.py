"""Test: reymen/core/backup_manager.py - kapsamli coverage testi"""
from __future__ import annotations
import os, sys, tempfile, json
from pathlib import Path
import pytest

PROJE_KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJE_KOK))


class TestBackupManager:
    def test_olusum(self):
        from reymen.core.backup_manager import BackupManager
        with tempfile.TemporaryDirectory() as td:
            bm = BackupManager(yedek_dizini=Path(td))
            assert bm is not None

    def test_durum_bos(self):
        from reymen.core.backup_manager import BackupManager
        with tempfile.TemporaryDirectory() as td:
            bm = BackupManager(yedek_dizini=Path(td))
            d = bm.durum()
            assert isinstance(d, dict)

    def test_yedek_listele_bos(self):
        from reymen.core.backup_manager import BackupManager
        with tempfile.TemporaryDirectory() as td:
            bm = BackupManager(yedek_dizini=Path(td))
            liste = bm.yedek_listele()
            assert isinstance(liste, list)

    def test_geri_yukle_gecersiz(self):
        from reymen.core.backup_manager import BackupManager
        with tempfile.TemporaryDirectory() as td:
            bm = BackupManager(yedek_dizini=Path(td))
            sonuc = bm.geri_yukle("/olmayan/dizin")
            assert sonuc is not None

    def test_singleton(self):
        from reymen.core.backup_manager import backup_manager_al
        b1 = backup_manager_al()
        b2 = backup_manager_al()
        assert b1 is b2

    def test_motor_kaydet(self):
        from reymen.core.backup_manager import motor_kaydet
        class M:
            tools = {}
            def _plugin_arac_kaydet(self, a, f, d=""):
                self.tools[a] = f
        m = M()
        motor_kaydet(m)
        assert "YEDEK_AL" in m.tools
        assert "YEDEK_LISTE" in m.tools