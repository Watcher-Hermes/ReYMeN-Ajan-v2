"""Test: reymen/arac/web_search_engine.py"""
from __future__ import annotations
import os, sys
from pathlib import Path
import pytest
PROJE_KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJE_KOK))

class TestWebSearch:
    def test_module_import(self):
        import reymen.arac.web_search_engine
        assert reymen.arac.web_search_engine is not None
