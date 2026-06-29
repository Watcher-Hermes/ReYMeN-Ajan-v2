"""Test: reymen/core/oauth_manager.py - kapsamli coverage testi"""
from __future__ import annotations
import os, sys, time, json, tempfile
from pathlib import Path
import pytest

PROJE_KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJE_KOK))


class TestOAuthToken:
    def test_olusum(self):
        from reymen.core.oauth_manager import OAuthToken
        t = OAuthToken(access_token="test_token", provider="test", expires_in=3600)
        assert t.access_token == "test_token"
        assert t.provider == "test"

    def test_is_expired_false(self):
        from reymen.core.oauth_manager import OAuthToken
        t = OAuthToken(access_token="t", provider="p", expires_in=3600)
        assert not t.is_expired

    def test_expires_at_str(self):
        from reymen.core.oauth_manager import OAuthToken
        t = OAuthToken(access_token="t", provider="p", expires_in=3600)
        assert isinstance(t.expires_at, str)


class TestOAuthError:
    def test_olusum(self):
        from reymen.core.oauth_manager import OAuthError
        e = OAuthError("test error", provider="google", status_code=401)
        assert str(e) == "test error"
        assert e.provider == "google"
        assert e.status_code == 401

    def test_varsayilan(self):
        from reymen.core.oauth_manager import OAuthError
        e = OAuthError("hata")
        assert e.provider == ""
        assert e.status_code == 0


class TestOAuthTokenDeposu:
    def test_olusum(self):
        from reymen.core.oauth_manager import OAuthTokenDeposu, OAuthToken
        with tempfile.TemporaryDirectory() as td:
            depo = OAuthTokenDeposu(base_path=Path(td))
            assert depo is not None

    def test_kaydet_yukle(self):
        from reymen.core.oauth_manager import OAuthTokenDeposu, OAuthToken
        with tempfile.TemporaryDirectory() as td:
            depo = OAuthTokenDeposu(base_path=Path(td))
            t = OAuthToken(access_token="at", provider="test_prov", expires_in=3600, refresh_token="rt")
            depo.kaydet(t)
            yuklenen = depo.yukle("test_prov")
            assert yuklenen is not None
            assert yuklenen.access_token == "at"

    def test_sil(self):
        from reymen.core.oauth_manager import OAuthTokenDeposu, OAuthToken
        with tempfile.TemporaryDirectory() as td:
            depo = OAuthTokenDeposu(base_path=Path(td))
            t = OAuthToken(access_token="a", provider="sil_test", expires_in=3600)
            depo.kaydet(t)
            assert depo.var_mi("sil_test") is True
            depo.sil("sil_test")
            assert depo.var_mi("sil_test") is False

    def test_listele(self):
        from reymen.core.oauth_manager import OAuthTokenDeposu, OAuthToken
        with tempfile.TemporaryDirectory() as td:
            depo = OAuthTokenDeposu(base_path=Path(td))
            t1 = OAuthToken(access_token="a1", provider="p1", expires_in=3600)
            t2 = OAuthToken(access_token="a2", provider="p2", expires_in=3600)
            depo.kaydet(t1)
            depo.kaydet(t2)
            liste = depo.listele()
            assert len(liste) >= 2

    def test_var_mi_yok(self):
        from reymen.core.oauth_manager import OAuthTokenDeposu
        with tempfile.TemporaryDirectory() as td:
            depo = OAuthTokenDeposu(base_path=Path(td))
            assert depo.var_mi("olmayan") is False


class TestOAuthManager:
    def test_olusum(self):
        from reymen.core.oauth_manager import OAuthManager
        om = OAuthManager()
        assert om is not None

    def test_provider_listesi(self):
        from reymen.core.oauth_manager import OAuthManager
        om = OAuthManager()
        providers = om.provider_listesi()
        assert isinstance(providers, list)

    def test_listele_bos(self):
        from reymen.core.oauth_manager import OAuthManager
        with tempfile.TemporaryDirectory() as td:
            from reymen.core.oauth_manager import OAuthTokenDeposu
            depo = OAuthTokenDeposu(base_path=Path(td))
            om = OAuthManager(deposu=depo)
            liste = om.listele()
            assert isinstance(liste, list)

    def test_login_olmayan_provider(self):
        from reymen.core.oauth_manager import OAuthManager
        om = OAuthManager()
        with pytest.raises(Exception):
            om.login("olmayan_provider_xyz")

    def test_durum_olmayan_provider(self):
        from reymen.core.oauth_manager import OAuthManager
        om = OAuthManager()
        durum = om.durum("olmayan_provider")
        assert "bulunamadi" in str(durum).lower() or "error" in str(durum).lower()

    def test_singleton(self):
        from reymen.core.oauth_manager import oauth_manager_al
        o1 = oauth_manager_al()
        o2 = oauth_manager_al()
        assert o1 is o2

    def test_motor_kaydet(self):
        from reymen.core.oauth_manager import motor_kaydet
        class M:
            tools = {}
            def _plugin_arac_kaydet(self, a, f, d=""):
                self.tools[a] = f
        m = M()
        motor_kaydet(m)
        assert len(m.tools) > 0