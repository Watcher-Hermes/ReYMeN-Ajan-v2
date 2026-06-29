# -*- coding: utf-8 -*-
"""Web Search Provider - ReYMeN plugin sistemi."""
from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)

PLUGIN_ADI = "Web Search Provider"
PLUGIN_KIND = "provider"


def motor_kaydet(motor: Any) -> None:
    """Motor'a provider araclaini kaydet."""
    if not hasattr(motor, "_plugin_arac_kaydet"):
        logger.warning("[web_search_provider] Motor desteklemiyor")
        return

    try:
        motor._plugin_arac_kaydet("WEB_ARA", "ara", "Web'de arama yapar")
        motor._plugin_arac_kaydet("WEB_GETIR", "sayfa_getir", "Web sayfasi icerigini getirir")
        logger.info("[web_search_provider] Araclar kaydedildi")
    except Exception as e:
        logger.warning("[web_search_provider] Arac kaydi hatasi: %s", e)