# -*- coding: utf-8 -*-
"""Guardrails Provider - ReYMeN plugin sistemi."""
from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)

PLUGIN_ADI = "Guardrails Provider"
PLUGIN_KIND = "provider"


def motor_kaydet(motor: Any) -> None:
    """Motor'a provider araclaini kaydet."""
    if not hasattr(motor, "_plugin_arac_kaydet"):
        logger.warning("[guardrails_provider] Motor desteklemiyor")
        return

    try:
        motor._plugin_arac_kaydet("GUARDRAIL_DENETLE", "denetle", "Metni guvenlik filtrelerinden gecirir")
        motor._plugin_arac_kaydet("GUARDRAIL_DURUM", "durum", "Guardrails sistem durumunu gosterir")
        motor._plugin_arac_kaydet("GUARDRAIL_EKLE", "kural_ekle", "Yeni guvenlik kurali ekler")
        logger.info("[guardrails_provider] Araclar kaydedildi")
    except Exception as e:
        logger.warning("[guardrails_provider] Arac kaydi hatasi: %s", e)