# -*- coding: utf-8 -*-
"""Browser Provider - ReYMeN plugin sistemi."""
from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)

PLUGIN_ADI = "Browser Provider"
PLUGIN_KIND = "provider"


def motor_kaydet(motor: Any) -> None:
    """Motor'a provider araclaini kaydet."""
    if not hasattr(motor, "_plugin_arac_kaydet"):
        logger.warning("[browser_provider] Motor desteklemiyor")
        return

    try:
        motor._plugin_arac_kaydet("BROWSER_AC", "sayfa_ac", "Tarayici sayfasi acar")
        motor._plugin_arac_kaydet("BROWSER_TIKLA", "tikla", "Sayfada elemente tiklar")
        motor._plugin_arac_kaydet("BROWSER_YAZ", "yaz", "Sayfada elemente metin yazar")
        motor._plugin_arac_kaydet("BROWSER_EKRAN", "ekran_goruntusu_al", "Sayfanin ekran goruntusunu alir")
        motor._plugin_arac_kaydet("BROWSER_KAPAT", "kapat", "Tarayiciyi kapatir")
        logger.info("[browser_provider] Araclar kaydedildi")
    except Exception as e:
        logger.warning("[browser_provider] Arac kaydi hatasi: %s", e)