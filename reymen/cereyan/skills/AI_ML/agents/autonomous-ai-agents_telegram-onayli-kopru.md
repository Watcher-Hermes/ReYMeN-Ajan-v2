---
name: telegram-onayli-kopru
title: Telegram Onayli Kopru
description: Claude + Ollama koprusu, dosya tabanli Telegram onayi ile
tags:
- agents
- ai
- telegram
category: agents
audience: user
---
| 5N1K | Açıklama |
|:----:|:---------|
| **Kim** | AI gelistiricisi |
| **Ne** | Claude + Ollama koprusu, dosya tabanli Telegram onayi ile |
| **Nerede** | `autonomous-ai-agents\autonomous-ai-agents_telegram-onayli-kopru.md` |
| **Ne Zaman** | Ilgili gorev gerektiginde |
| **Neden** | Autonomous Ai Agents Telegram Onayli Kopru islemini standartlastirmak icin |
| **Nasıl** | Skill dosyasindaki adimlari takip ederek |


## 📋 5N1K

| Soru | Cevap |
|:-----|:------|
| **Kim?** | Tüm ajanlar |
| **Ne?** | Claude + Ollama koprusu, dosya tabanli Telegram onayi ile |
| **Nerede?** | autonomous-ai-agents/ |
| **Ne Zaman?** | İhtiyaç duyulduğunda |
| **Neden?** | Otomatik kategorilendirme |
| **Nasıl?** | Skill referansı ile |

Kim: Otonom ajan gelistiricisi
Ne: Claude + Ollama koprusu, dosya tabanli Telegram onayi ile
Nerede: `autonomous-ai-agents\autonomous-ai-agents_telegram-onayli-kopru.md`
Ne Zaman: Ilgili gorev gerektiginde
Neden: Autonomous Ai Agents Telegram Onayli Kopru islemini standartlastirmak ve tekrarlanabilir kilmak icin
Nasil: Skill dosyasindaki adimlari takip ederek


# Telegram Onaylı Köprü

Claude + Ollama (Dolphin) arasında dosya tabanlı köprü. Telegram üzerinden onay mekanizması ile çalışır.

## Kullanım

1. `python bridge_tg.py` çalıştır
2. ReYMeN `bridge_status.txt` okur, Telegram'a aktarır
3. Kullanıcı `devam` / `dur` der, ReYMeN `bridge_signal.txt`'e yazar

## Güvenlik

- `MAX_TURN=5` — maksimum 5 tur
- `300sn timeout` — otomatik durma
- Dosya tabanlı sinyalizasyon

## Akış

1. Kullanıcı Telegram'dan komut gönderir
2. ReYMeN köprü script'ini çalıştırır
3. Script Claude + Ollama arasında gidiş-geliş yapar
4. Her turda durumu `bridge_status.txt`'ye yazar
5. ReYMeN durumu okur ve Telegram'a iletir
6. Kullanıcı onay verene kadar veya timeout'a kadar devam eder

## Log Örneği

```
# Tur 1 Claude
def tek_sayilari_topla(liste):
    return sum(x for x in liste if x % 2 != 0)

# Tur 1 Ollama (Dolphin)
Dolphin: Hello Claude! I'm here to help you...
```