---
name: agent-project-bootstrap_references_hermes-entegrasyonu
description: ReYMeN Agent Entegrasyon Deseni
title: "Agent Project Bootstrap References ReYMeN Entegrasyonu"
version: 1.0.0
---


| 5N1K | Açıklama |
|:----:|:---------|
| **Kim** | AI/ML mühendisi |
| **Ne** | ReYMeN Agent Entegrasyon Deseni |
| **Nerede** | AI_ML/ |
| **Ne Zaman** | AI/ML görevi gerektiğinde |
| **Neden** | standardize etmek için |
| **Nasıl** | Skill adımlarını takip ederek |

# ReYMeN Agent Entegrasyon Deseni

Reymen Proje'de Nous Research ReYMeN Agent'ı entegre etmek için kullanılan desen.

## Mimari

```
C:\hermes\                         ← Hermes Agent (bağımsız repo)
  cli.py (731KB)                   ← Ana CLI
  agent/                           ← Agent runtime modülleri
  skills/                          ← 100+ skill
  apps/                            ← Uygulamalar
  cron/                            ← Zamanlanmış görevler
  .env                             ← ReYMeN config (Reymen'den senkronize)
  cli-config.yaml                  ← ReYMeN ayarları

Reymen Proje/
  hermes_cli.py                    ← Wrapper: env sync + ReYMeN CLI çağırma
  reyemen.bat                      ← "reyemen.bat ReYMeN ..." ile erişim
```

## Wrapper (hermes_cli.py) İşleyişi

1. **Env senkronizasyonu**: Reymen .env'deki anahtarları ReYMeN .env'ye kopyala (boş/*** olanları doldur)
2. **Subprocess çağrısı**: `python C:\hermes\cli.py <args>` çalıştır
3. **Çıktı yönlendirme**: stdout/stderr kullanıcıya göster

```python
def env_aktar():
    reymen = {}  # Reymen .env'den oku
    ReYMeN = []  # ReYMeN .env'yi güncelle
    # ... senkronizasyon mantığı

def hermes_cagir(args):
    subprocess.run([sys.executable, HERMES_CLI, *args])
```

## .bat Entegrasyonu

```
reyemen.bat ReYMeN doctor         # ReYMeN sağlık kontrolü
reyemen.bat ReYMeN gateway start  # Gateway başlat
reyemen.bat ReYMeN skills list    # Skill listele
```

## Önemli

- ReYMeN Agent kendi reposunda kalır (taşınmaz)
- Yalnızca wrapper (hermes_cli.py) ve .bat referansı Reymen Proje'de
- Çift yönlü env senkronizasyonu: Reymen'de değişiklik → ReYMeN'e yansır
- ReYMeN .git (280MB) korunur — kendi git geçmişi bozulmaz
