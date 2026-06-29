"""Test: reymen/sistem/durum.py"""
from __future__ import annotations
import os, sys, json, tempfile
from pathlib import Path
import pytest

PROJE_KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJE_KOK))


@pytest.fixture(autouse=True)
def _reset_durum_yolu(monkeypatch):
    """Her test öncesi durum.json'u geçici bir dosyaya yönlendir."""
    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, encoding="utf-8"
    )
    json.dump({
        "son_guncelleme": "2025-01-15 10:00",
        "guncelleyen_bot": "test_bot",
        "toplam_ozellik": 10,
        "tamam": 5,
        "isleniyor": 3,
        "cozulen_8_onceki": {
            "toplam": 8, "tamam": 4,
            "maddeler": {
                "test_madde_1": {"detay": "ilk test maddesi"},
                "test_madde_2": {"detay": "ikinci test maddesi"},
            }
        },
        "cozulen_10_ikinci_dalga": {
            "toplam": 10, "tamam": 6,
            "maddeler": {
                "gorev_a": {"detay": "gorev a detay", "oncelik": "yuksek"},
                "gorev_b": {"detay": "gorev b detay", "oncelik": "dusuk"},
            }
        },
        "cozulen_4_kismen": {
            "toplam": 4, "tamam": 2,
            "maddeler": {
                "kismen_1": {"detay": "kismen cozuldu", "oncelik": "orta"},
            }
        },
        "mevcut_eksikler": {
            "toplam": 5, "tamam": 1,
            "maddeler": {
                "eksik_a": {"durum": "tamam", "detay": "tamamlandi", "oncelik": "yuksek"},
                "eksik_b": {"durum": "eksik", "detay": "hala eksik", "oncelik": "dusuk", "cozuluyor": True},
                "eksik_c": {"durum": "kismen", "detay": "kismen", "oncelik": "orta"},
                "eksik_d": {"durum": "stub", "detay": "taslak", "oncelik": "dusuk"},
            }
        },
        "_meta": {"bot_yanlis_liste_var": True},
        "tahmini_seviye": "A2",
    }, tmp)
    tmp.close()
    import reymen.sistem.durum as m
    monkeypatch.setattr(m, "DURUM_DOSYASI", Path(tmp.name))
    yield
    os.unlink(tmp.name)


class TestDurumYukle:
    def test_yukle_basarili(self):
        from reymen.sistem.durum import _yukle
        veri = _yukle()
        assert isinstance(veri, dict)
        assert veri["toplam_ozellik"] == 10
        assert veri["tamam"] == 5

    def test_yukle_dosya_yok(self, monkeypatch):
        import reymen.sistem.durum as m
        monkeypatch.setattr(m, "DURUM_DOSYASI", Path("/nonexistent/durum.json"))
        veri = m._yukle()
        assert "hata" in veri
        assert "bulunamadi" in veri["hata"]

    def test_yukle_bozuk_json(self, monkeypatch):
        tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        )
        tmp.write("Bu gecerli bir json degil{")
        tmp.close()
        import reymen.sistem.durum as m
        monkeypatch.setattr(m, "DURUM_DOSYASI", Path(tmp.name))
        veri = m._yukle()
        assert "hata" in veri
        os.unlink(tmp.name)


class TestDurumOzet:
    def test_ozet_basic(self):
        from reymen.sistem.durum import _yukle, _ozet
        veri = _yukle()
        ozet = _ozet(veri)
        assert "ReYMeN Durum Raporu" in ozet
        assert "test_bot" in ozet
        assert "10" in ozet
        assert "5" in ozet

    def test_ozet_eksikler_tamam_emoji(self):
        from reymen.sistem.durum import _yukle, _ozet
        veri = _yukle()
        ozet = _ozet(veri)
        assert "✅" in ozet
        assert "🔶" in ozet
        assert "📦" in ozet

    def test_ozet_cozulen_diger(self, monkeypatch):
        from reymen.sistem.durum import _ozet
        veri = {"cozulen_diger": {"maddeler": ["item1", "item2"]}}
        ozet = _ozet(veri)
        assert "Diger Cozulenler" in ozet
        assert "item1" in ozet

    def test_ozet_uyari_var(self, monkeypatch):
        from reymen.sistem.durum import _ozet
        veri = {"_meta": {"bot_yanlis_liste_var": True}}
        ozet = _ozet(veri)
        assert "⚠️" in ozet

    def test_ozet_pasa_karsilastirma(self, monkeypatch):
        from reymen.sistem.durum import _ozet
        veri = {
            "pasa_38_karsilastirmasi": {
                "aciklama": "38. pasanin karsilastirmasi",
                "maddeler": [
                    {"eksik": "eksik1", "cozuldu_mu": "evet", "hermes": "var"},
                    {"eksik": "eksik2", "cozuldu_mu": "hayir", "hermes": "yok"},
                ]
            },
            "tahmini_seviye": "B1"
        }
        ozet = _ozet(veri)
        assert "Pasa_38" in ozet
        assert "B1" in ozet
        assert "✅" in ozet
        assert "❌" in ozet


class TestDurumDetayli:
    def test_detayli_json(self):
        from reymen.sistem.durum import _yukle, _detayli
        veri = _yukle()
        detay = _detayli(veri)
        assert "son_guncelleme" in detay
        assert "test_bot" in detay

    def test_detayli_ham(self):
        from reymen.sistem.durum import _yukle, _detayli
        veri = _yukle()
        detay = _detayli(veri)
        parsed = json.loads(detay)
        assert parsed["tamam"] == 5


class TestDurumOku:
    def test_durum_oku_ozet(self):
        from reymen.sistem.durum import durum_oku
        sonuc = durum_oku("0")
        assert "ReYMeN Durum Raporu" in sonuc

    def test_durum_oku_detayli(self):
        from reymen.sistem.durum import durum_oku
        sonuc = durum_oku("1")
        assert "son_guncelleme" in sonuc

    def test_durum_oku_json(self):
        from reymen.sistem.durum import durum_oku
        sonuc = durum_oku("json")
        parsed = json.loads(sonuc)
        assert parsed["tamam"] == 5

    def test_durum_oku_raw(self):
        from reymen.sistem.durum import durum_oku
        sonuc = durum_oku("raw")
        parsed = json.loads(sonuc)
        assert parsed["toplam_ozellik"] == 10

    def test_durum_oku_detay_string(self):
        from reymen.sistem.durum import durum_oku
        sonuc = durum_oku("detay")
        assert "son_guncelleme" in sonuc

    def test_durum_oku_detayli_string(self):
        from reymen.sistem.durum import durum_oku
        sonuc = durum_oku("detayli")
        assert "son_guncelleme" in sonuc


class TestMotorKaydet:
    def test_motor_kaydet_hasattr(self):
        from reymen.sistem.durum import motor_kaydet

        class FakeMotor:
            _tools = {}

            def _plugin_arac_kaydet(self, ad, fn, desc):
                FakeMotor._tools[ad] = fn

        motor = FakeMotor()
        motor_kaydet(motor)
        assert "DURUM_OKU" in FakeMotor._tools
        # Test the registered lambda
        assert "ReYMeN" in FakeMotor._tools["DURUM_OKU"]()

    def test_motor_kaydet_no_attr(self):
        from reymen.sistem.durum import motor_kaydet

        class FakeMotor:
            pass

        # Should not raise
        motor_kaydet(FakeMotor())
