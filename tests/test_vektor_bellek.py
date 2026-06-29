"""Test: reymen/hafiza/vektor_bellek.py"""
from __future__ import annotations
import os, sys
from pathlib import Path
import pytest
PROJE_KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJE_KOK))

class TestVektorBellek:
    def test_import(self):
        import reymen.hafiza.vektor_bellek as m
        assert m is not None