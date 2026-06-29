"""Test: reymen/core/mcp_server.py"""
from __future__ import annotations
import os,sys
from pathlib import Path
import pytest
PROJE_KOK=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(PROJE_KOK))
class TestMCPServer:
    def test_import(self):
        import reymen.core.mcp_server
        assert reymen.core.mcp_server is not None
