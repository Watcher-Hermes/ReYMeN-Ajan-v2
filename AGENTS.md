# ReYMeN — AGENTS.md

> ReYMeN = ReYMeN AI Agent, **tamamen bagimsiz**.
> ReYMeN Agent altyapisi gerektirmez.
> Proje koku: `C:\Users\marko\Desktop\Reymen Proje\ReYMeN-Ajan`

---

## Entry Points

| # | Dosya | Tur | Ne yapar |
|---|-------|-----|----------|
| 1 | `reymen\bin\reymen.cmd` | `.cmd` (batch) | Ana launcher. `python reymen_launcher.py`'yi calistirir. |
| 2 | `venv\Scripts\reymen.cmd` | `.cmd` (batch) | Proje venv'i uzerinden `python reymen_launcher.py`'yi calistirir. |
| 3 | `venv\Scripts\reymen.exe` | `.exe` (PyInstaller) | PyInstaller ile build edilmis dogrudan calistirilabilir. |
| 4 | `~/.local/bin/reymen.exe` | `.exe` (pip zipapp) | pip console_scripts entry point. |

Tum entry point'ler dogrudan `reymen_launcher.py`'yi calistirir.
ReYMeN binary'sine yonlendirme YOK.

---

## Bagimsizlik Beyani

ReYMeN Agent **sifir (0) ReYMeN bagimliligi** ile calisir.
Tum altyapi ReYMeN projesinin kendi modullerinde:

| Bilesen | ReYMeN Modulu | ReYMeN Bagimlisi mi? |
|---------|---------------|:--------------------:|
| LLM Provider / Beyin | `reymen/cereyan/beyin.py` | HAYIR |
| Konusma Dongusu | `reymen/cereyan/conversation_loop.py` | HAYIR |
| Eylem Cozucu (Motor) | `reymen/cereyan/motor.py` | HAYIR |
| Arac Kayit / Calistirma | `reymen/arac/tool_registry.py` + `tool_executor.py` | HAYIR |
| Session DB (SQLite FTS5) | `reymen/hafiza/session_db.py` + `reymen/core/session_db.py` | HAYIR |
| Cron Zamanlayici | `reymen/core/cron_manager.py` + `reymen/sistem/cron_scheduler.py` | HAYIR |
| Hafiza / OnceHafiza | `reymen/sistem/once_hafiza.py` + `reymen/hafiza/` | HAYIR |
| Gateway (Telegram vs.) | `reymen/ag/gateway_yonetici.py` + `platform_gateways.py` | HAYIR |
| Skill Yoneticisi | `reymen/cereyan/skill_activator.py` | HAYIR |
| CLI / Parser | `reymen/cli/__init__.py` (build_parser) | HAYIR |
| CLI Komutlari | `reymen/arac/cli_commands.py` | HAYIR |
| Launcher | `reymen_launcher.py` | HAYIR |
| Config | `config.yaml` | HAYIR |

---

## Test ve Dogrulama (2026-06-30)

- **13/13 ana modul** basariyla import edildi (ReYMeN olmadan)
- **ReYMeN import referansi: 0** (tool/script/yardimci kodlarda)
- **reymen_launcher.py -z "merhaba"** calisiyor (canli API testi)
- **reymen_launcher.py --version** calisiyor
- `reymen/scripts/ReYMeN_tools.py` — ReYMeN import'u temizlendi
- `reymen/arac/cli_commands.py` — ReYMeN binary bagimliligi temizlendi

Kalan ReYMeN metni (bagimli DEGIL):
- `reymen/scripts/fix_01_sessiz_except.py` — "from hermes_tools" string tespiti (kod degil, yorum)
- `reymen/sistem/model_tools.py` — `from hermes_cli` try/except icinde (graceful degrade)

---

## Calistirma

```bash
# Dogrudan
python reymen_launcher.py

# Tek soru (one-shot)
python reymen_launcher.py -z "merhaba"

# REPL
reymen\bin\reymen.cmd

# Versiyon
python reymen_launcher.py --version
```

---

## Veri Lokasyonlari (Bagimsiz)

| Veri | Konum |
|------|-------|
| Config | `ReYMeN-Ajan\config.yaml` |
| API key'ler | `ReYMeN-Ajan\.env` |
| Kisilik/SOUL.md | `ReYMeN-Ajan\SOUL.md` |
| Motor | `reymen\cereyan\conversation_loop.py` |
| Launcher | `reymen_launcher.py` |
| Ana entry point | `reymen\bin\reymen.cmd` |
| PATH stub | `~/.local/bin/reymen.exe` |
| **durum.json (TEK KAYNAK)** | `ReYMeN-Ajan\durum.json` |

---

## KATI KURAL: Bot/Token → durum.json

**Zorunlu kural — asla ihlal edilmez:**

1. **Her yeni bot**, başlangıçta kendini otomatik `durum.json > botlar`'a ekler (`BotProcess._durum_guncelle()`)
2. **Yeni token** geldiğinde: BotFather'dan al → `reymen/.env`'ye yaz → bot yeniden başlatılır → otomatik durum.json'a kaydeder
3. durum.json'a kaydedilmeyen bot TANINMAZ, özellikleri bilinemez
4. **Elle ekleme:** `durum.json > botlar` altına `"bot_adi": { ... }` objesi ekle
5. Bu kural SOUL.md, telegram_bot.py ve conversation_loop.py'de teyit edilmiştir
