"""Test: reymen/core/config_manager.py"""
from __future__ import annotations
import os, sys
from pathlib import Path
import pytest
PROJE_KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJE_KOK))

class TestConfigManager:
    def test_import(self):
        import reymen.core.config_manager as m
        assert m is not None