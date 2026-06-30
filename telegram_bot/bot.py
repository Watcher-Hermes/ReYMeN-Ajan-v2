# -*- coding: utf-8 -*-
"""
telegram_bot/bot.py — ReYMeN Cron Botu (Wrapper).
=================================================

Bu dosya, birlesik telegram_bot.py'ye yonlendirme yapar.
Tum ozellikler: reymen/ag/telegram_bot.py

Kullanim:
    python -m telegram_bot.bot
    veya HERMES_GATEWAY=ptb python telegram_bot/bot.py
"""

from reymen.ag.telegram_bot import (
    # Ana siniflar
    UnifiedBot,
    BotProcess,
    CronManager,
    _cron_manager,
    # Yardimcilar
    _api,
    gonder,
    gonder_requests,
    # Komut handler'lari (HTTP modu)
    polling,
    main,
    _cmd_start,
    _cmd_help,
    _cmd_run,
    _cmd_status,
    _cmd_logs,
    _cmd_cancel,
    _cmd_clarify,
    _cmd_exec,
    _cmd_beceriler,
    _cmd_cron,
    # Motor entegrasyonu
    motor_bildirim_gonder,
    telegram_araclari_kaydet,
    motor_kaydet,
    # Sabitler
    TOKEN,
    CHAT_ID,
    API_BASE,
    GATEWAY_MOD,
    PTB_AVAILABLE,
)

if __name__ == "__main__":
    main()
