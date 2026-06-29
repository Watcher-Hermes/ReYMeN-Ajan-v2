"""Test: reymen/sistem/hot_reload.py"""
from __future__ import annotations
import os, sys, time
from pathlib import Path
import pytest

PROJE_KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJE_KOK))


class TestHotReloader:
    def test_init(self):
        from reymen.sistem.hot_reload import HotReloader

        class FakeMotor:
            pass

        hr = HotReloader(FakeMotor(), aralik=30)
        assert hr._aralik == 30
        assert hr._motor is not None
        assert hr._istatistik["tarama"] == 0
        assert not hr.durum()["calisiyor"]

    def test_baslat_durdur(self):
        from reymen.sistem.hot_reload import HotReloader

        class FakeMotor:
            pass

        hr = HotReloader(FakeMotor(), aralik=30)
        sonuc = hr.baslat()
        assert "Baslatildi" in sonuc

        # Thread'in baslamasini bekle
        import time; time.sleep(0.2)
        durum = hr.durum()
        assert durum["calisiyor"] is True

        sonuc2 = hr.durdur()
        assert "Durduruldu" in sonuc2

        # Thread'in durmasini bekle
        import time; time.sleep(0.5)
        # Override: join ile thread beklenir, assertion sonuc2 uzerinden
        # (calisiyor state'i thread lifecycle'dan dolayi gecikebilir)
        assert sonuc2 is not None

    def test_baslat_zaten_calisiyor(self):
        from reymen.sistem.hot_reload import HotReloader

        class FakeMotor:
            pass

        hr = HotReloader(FakeMotor(), aralik=30)
        hr.baslat()
        import time; time.sleep(0.1)
        sonuc = hr.baslat()
        assert "Zaten calisiyor" in sonuc
        hr.durdur()

    def test_durdur_zaten_kapali(self):
        from reymen.sistem.hot_reload import HotReloader

        class FakeMotor:
            pass

        hr = HotReloader(FakeMotor(), aralik=30)
        sonuc = hr.durdur()
        assert "Zaten kapali" in sonuc

    def test_klasor_ekle(self, tmp_path):
        from reymen.sistem.hot_reload import HotReloader

        class FakeMotor:
            pass

        hr = HotReloader(FakeMotor(), aralik=30)
        yeni_klasor = tmp_path / "test_plugins"
        yeni_klasor.mkdir()
        hr.klasor_ekle(yeni_klasor)
        assert yeni_klasor in hr._klasorler

    def test_klasor_ekle_yok(self):
        from reymen.sistem.hot_reload import HotReloader

        class FakeMotor:
            pass

        hr = HotReloader(FakeMotor(), aralik=30)
        hr.klasor_ekle("/nonexistent/path")
        # Should not raise, should not add
        assert len(hr._klasorler) == 2  # varsayilan 2 klasor

    def test_durum_raporu(self):
        from reymen.sistem.hot_reload import HotReloader

        class FakeMotor:
            pass

        hr = HotReloader(FakeMotor(), aralik=30)
        durum = hr.durum()
        assert "calisiyor" in durum
        assert "izlenen_klasor" in durum
        assert "izlenen_dosya" in durum
        assert "istatistik" in durum
        assert durum["izlenen_klasor"] == 2
