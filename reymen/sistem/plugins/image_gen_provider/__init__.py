# -*- coding: utf-8 -*-
"""Image Gen Provider - ReYMeN plugin sistemi."""
from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)

PLUGIN_ADI = "Image Gen Provider"
PLUGIN_KIND = "provider"


def motor_kaydet(motor: Any) -> None:
    """Motor'a provider araclaini kaydet."""
    if not hasattr(motor, "_plugin_arac_kaydet"):
        logger.warning("[image_gen_provider] Motor desteklemiyor")
        return

    try:
        motor._plugin_arac_kaydet("GORUNTU_OLUSTUR", "goruntu_olustur", "Prompt'tan goruntu olusturur")
        motor._plugin_arac_kaydet("GORUNTU_DUZENLE", "goruntu_duzenle", "Varolan goruntuyu duzenler")
        logger.info("[image_gen_provider] Araclar kaydedildi")
    except Exception as e:
        logger.warning("[image_gen_provider] Arac kaydi hatasi: %s", e)