# -*- coding: utf-8 -*-
"""Mcp Provider - ReYMeN plugin sistemi."""
from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)

PLUGIN_ADI = "Mcp Provider"
PLUGIN_KIND = "provider"


def motor_kaydet(motor: Any) -> None:
    """Motor'a provider araclaini kaydet."""
    if not hasattr(motor, "_plugin_arac_kaydet"):
        logger.warning("[mcp_provider] Motor desteklemiyor")
        return

    try:
        motor._plugin_arac_kaydet("MCP_SUNUCU_BASLAT", "sunucu_baslat", "MCP sunucusu baslatir")
        motor._plugin_arac_kaydet("MCP_ARAC_CALISTIR", "arac_calistir", "MCP aracini calistirir")
        motor._plugin_arac_kaydet("MCP_BAGLAN", "baglan", "MCP sunucusuna baglanir")
        logger.info("[mcp_provider] Araclar kaydedildi")
    except Exception as e:
        logger.warning("[mcp_provider] Arac kaydi hatasi: %s", e)