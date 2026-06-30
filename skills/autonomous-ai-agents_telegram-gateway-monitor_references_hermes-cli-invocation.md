---
name: autonomous-ai-agents_telegram-gateway-monitor_references_hermes-cli-invocation
description: ReYMeN CLI Invocation
title: "Autonomous Ai Agents Telegram Gateway Monitor References ReYMeN Cli Invocation"
version: 1.0.0
---


| 5N1K | Açıklama |
|:----:|:---------|
| **Kim** | AI/ML mühendisi |
| **Ne** | ReYMeN CLI Invocation |
| **Nerede** | AI_ML/ |
| **Ne Zaman** | AI/ML görevi gerektiğinde |
| **Neden** | standardize etmek için |
| **Nasıl** | Skill adımlarını takip ederek |

## ReYMeN CLI Invocation

### Problem

`ReYMeN.exe` veya `ReYMeN send --list telegram` çalıştırıldığında şu hata alınır:
```
ModuleNotFoundError: No module named 'hermes_cli'
```

**Nedeni:** `hermes_cli` paketi venv'deki site-packages'e düzgün kurulmamış. Dizin var ama içi boş:
```
/c/Users/marko/AppData/Local/hermes/hermes-agent/venv/Lib/site-packages/hermes_cli/  → boş
```

Asıl modül proje kökünde:
```
/c/Users/marko/AppData/Local/hermes/hermes-agent/hermes_cli/  → gerçek kod burada
```

### Çözüm

Her `ReYMeN` komutunu **proje kökünden** `PYTHONPATH` + `HERMES_HOME` ile çalıştır:

```bash
cd /c/Users/marko/AppData/Local/hermes/hermes-agent && \
HERMES_HOME=/c/Users/marko/AppData/Local/hermes \
PYTHONPATH=/c/Users/marko/AppData/Local/hermes/hermes-agent \
/c/Users/marko/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe \
-m hermes_cli.main <subcommand> [args]
```

### Neden ReYMeN.exe çalışmaz?

`hermes.exe` bir PyInstaller PE binary'sidir. Çalıştığında `hermes_cli` modülünü site-packages'te arar ama orası boş olduğu için `ModuleNotFoundError` alır. `python -m hermes_cli.main` ile doğrudan Python modülü olarak çağırmak bu sorunu bypass eder.

### Geçici çözüm mü kalıcı mı?

Bu **yeniden kurulum gerektiren** bir env sorunudur. `pip install -e .` ile editable kurulum yapılırsa `ReYMeN.exe` tek başına çalışır hale gelir. Şu ana kadar yeniden kurulum yapılmadığı için PYTHONPATH workaround'u kullanılmaya devam edilmektedir.

### İlgili komutlar

| İşlem | Komut |
|-------|-------|
| Hedef listele | `... -m hermes_cli.main send --list telegram` |
| Test mesajı gönder | `... -m hermes_cli.main send --to "telegram:Q !" "mesaj"` |
| Gateway restart | `... -m hermes_cli.main gateway run --replace` |
