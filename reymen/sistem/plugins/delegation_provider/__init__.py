# -*- coding: utf-8 -*-
"""Delegation Provider - ReYMeN plugin sistemi."""
from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)

PLUGIN_ADI = "Delegation Provider"
PLUGIN_KIND = "provider"


def motor_kaydet(motor: Any) -> None:
    """Motor'a provider araclaini kaydet."""
    if not hasattr(motor, "_plugin_arac_kaydet"):
        logger.warning("[delegation_provider] Motor desteklemiyor")
        return

    try:
        motor._plugin_arac_kaydet("DELEGE_ET", "gorev_devret", "Gorevi alt ajana devreder")
        motor._plugin_arac_kaydet("DELEGE_DURUM", "gorev_durumu", "Alt ajan gorev durumunu sorgular")
        motor._plugin_arac_kaydet("DELEGE_IPTAL", "gorev_iptal", "Alt ajan gorevini iptal eder")
        logger.info("[delegation_provider] Araclar kaydedildi")
    except Exception as e:
        logger.warning("[delegation_provider] Arac kaydi hatasi: %s", e)