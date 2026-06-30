# -*- coding: utf-8 -*-
"""
telegram_bot/ai_bot.py — ReYMeN AI Agent Botu (Wrapper).
=========================================================

Bu dosya, birlesik telegram_bot.py'ye yonlendirme yapar.
Tum ozellikler: reymen/ag/telegram_bot.py

Kullanim:
    HERMES_GATEWAY=ai python telegram_bot/ai_bot.py
    veya python -c "from telegram_bot.ai_bot import BotProcess; ..."
"""

from reymen.ag.telegram_bot import (
    # Ana siniflar
    BotProcess,
    UnifiedBot,
    CronManager,
    _cron_manager,
    # Yardimcilar
    _api,
    gonder,
    gonder_requests,
    # AI yardimcilari
    BEYIN_CLS,
    ONCE_HAFIZA_ARA,
    ONCE_HAFIZA_KAYDET,
    CONVERSATION_LOOP_CLS,
    # Sabitler
    TOKEN,
    CHAT_ID,
    API_BASE,
    GATEWAY_MOD,
    _PROJE_KOK,
)

# BotProcess icin kolay erisim
def main():
    """BotProcess AI modu baslat."""
    if not TOKEN or TOKEN.startswith("***"):
        import sys
        print("[ai_bot] TELEGRAM_BOT_TOKEN ayarli degil!")
        sys.exit(1)
    bot = BotProcess(TOKEN)
    bot.poll()

if __name__ == "__main__":
    main()
