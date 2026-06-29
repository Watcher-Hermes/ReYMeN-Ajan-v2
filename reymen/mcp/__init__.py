# -*- coding: utf-8 -*-
"""
reymen/mcp/__init__.py — ReYMeN MCP İstemci Paketi.

Model Context Protocol (MCP) sunucularına bağlanma, tool keşfetme ve çağırma.

Alt Modüller:
  mcp_manager      — Async MCP yöneticisi (singleton)
  mcp_tool         — Motor araç kaydı (MCP_TOOL_LISTELE / MCP_TOOL_CAGIR)
  mcp_catalog      — Önceden tanımlı MCP sunucu kataloğu
  mcp_discovery    — config.yaml + .env'den otomatik keşif (MCP_DISCOVERY)
  mcp_reconnect    — Heartbeat + otomatik yeniden bağlanma (MCP_RECONNECT_*)

Kullanım:
    from reymen.mcp.mcp_manager import mcp_manager
    from reymen.mcp.mcp_discovery import mcp_kesfet
    from reymen.mcp.mcp_reconnect import mcp_reconnect_baslat

    # Otomatik keşif
    yeni = mcp_kesfet()

    # Başlat ve keşfet
    await mcp_manager().baslat()

    # Heartbeat + reconnect başlat
    await mcp_reconnect_baslat()

    # Tool çağır
    sonuc = await mcp_manager().cagir("github", "issues/list", {"repo": "user/repo"})

    # Tüm tool'ları listele
    tools = mcp_manager().tum_araclari_getir()
"""

from reymen.mcp.mcp_tool import motor_kaydet as mcp_tool_kaydet
from reymen.mcp.mcp_discovery import motor_kaydet as mcp_discovery_kaydet
from reymen.mcp.mcp_reconnect import motor_kaydet as mcp_reconnect_kaydet

__all__ = [
    "mcp_tool_kaydet",
    "mcp_discovery_kaydet",
    "mcp_reconnect_kaydet",
]


def motor_kaydet(motor) -> None:
    """Tüm MCP araçlarını Motor'a kaydet.

    Motor başlatılırken çağrılır. Sırasıyla:
      1. MCP_TOOL_LISTELE / MCP_TOOL_CAGIR (mcp_tool)
      2. MCP_DISCOVERY / MCP_DISCOVERY_DURUM (mcp_discovery)
      3. MCP_RECONNECT_BASLAT / MCP_RECONNECT_DURDUR / MCP_RECONNECT_DURUM (mcp_reconnect)
    """
    mcp_tool_kaydet(motor)
    mcp_discovery_kaydet(motor)
    mcp_reconnect_kaydet(motor)
