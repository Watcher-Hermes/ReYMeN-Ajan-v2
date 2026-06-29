"""Test: reymen/hafiza/ modulleri"""
from __future__ import annotations
import os,sys
from pathlib import Path
import pytest
PROJE_KOK=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(PROJE_KOK))
class TestHafiza:
    def test_memory_manager(self):
        import reymen.hafiza.memory_manager
        assert reymen.hafiza.memory_manager is not None
    def test_vektorel_hafiza(self):
        import reymen.hafiza.vektorel_hafiza
        assert reymen.hafiza.vektorel_hafiza is not None
    def test_bounded_memory(self):
        import reymen.hafiza.bounded_memory
        assert reymen.hafiza.bounded_memory is not None
