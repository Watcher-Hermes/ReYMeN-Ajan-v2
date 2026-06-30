---
name: autonomous-ai-agents_hermes-telegram-sync
title: ReYMeN Telegram Sync
description: ''
tags:
- agents
category: agents
audience: agent
---
| 5N1K | Açıklama |
|:----:|:---------|
| **Kim** | AI gelistiricisi |
| **Ne** | "ReYMeN Agent ile Telegram bot arasinda kopru kurar. Iki yonlu senkronizasyon saglar: Telegram'dan mesaj geldiginde ReYMeN Agent'a iletilir, ReYMeN Agent'in cevabi Telegram'a gonderilir. Skill kutupha |
| **Nerede** | `autonomous-ai-agents\autonomous-ai-agents_hermes-telegram-sync.md` |
| **Ne Zaman** | Ilgili gorev gerektiginde |
| **Neden** | Autonomous Ai Agents ReYMeN Telegram Sync islemini standartlastirmak icin |
| **Nasıl** | Skill dosyasindaki adimlari takip ederek |


## 📋 5N1K

| Soru | Cevap |
|:-----|:------|
| **Kim?** | Tüm ajanlar |
| **Ne?** | ReYMeN Agent ile Telegram bot arasinda kopru kurar. Iki yonlu senkronizasyon saglar: Telegram'dan mesaj geldiginde ReYMeN Agent'a iletilir, ReYMeN Agent'in cevabi Telegram'a gonderilir. Skill kutuphanesi, .env ayarlari ve vault verisi her iki tarafta da ayni kalir. |
| **Nerede?** | autonomous-ai-agents/ |
| **Ne Zaman?** | İhtiyaç duyulduğunda |
| **Neden?** | Otomatik kategorilendirme |
| **Nasıl?** | Skill referansı ile |

Kim: Otonom ajan gelistiricisi
Ne: "ReYMeN Agent ile Telegram bot arasinda kopru kurar. Iki yonlu senkronizasyon saglar: Telegram'dan mesaj geldiginde ReYMeN Agent'a iletilir, ReYMeN Agent'in cevabi Telegram'a gonderilir. Skill kutupha
Nerede: `autonomous-ai-agents\autonomous-ai-agents_hermes-telegram-sync.md`
Ne Zaman: Ilgili gorev gerektiginde
Neden: Autonomous Ai Agents ReYMeN Telegram Sync islemini standartlastirmak ve tekrarlanabilir kilmak icin
Nasil: Skill dosyasindaki adimlari takip ederek


## Alternatif: Dosya Bazlı Kurtarma (n8n'siz)

Eğer n8n kapalıysa veya kurulum istemiyorsan, **dosya bazlı kurtarma** yöntemi kullanılabilir. Bu yöntem n8n gerektirmez.

### Mimari Farkı
| Yöntem | Araç | Karmaşıklık |
|--------|------|------------|
| n8n köprüsü | n8n + router.py | Yüksek |
| **Dosya bazlı kurtarma** | Cron job + takildi.txt | **Düşük** |

### Nasıl Çalışır
```
Local ReYMeN takılır → C:\Users\marko\takildi.txt oluşturur
Telegram ReYMeN cron job'u (her 15 dk) → dosyayı bulur
→ Tor'da araştırma yapar → çözümü Telegram'a bildirir
→ takildi.txt silinir
```

### Cron Job Detayı
- **Job adı:** Takilma-Izleyici
- **Çalıştığı yer:** Telegram ReYMeN (bu session)
- **Kontrol sıklığı:** 15 dakikada bir
- **Yüklü skill:** tor-browser-arama
- **Local ReYMeN'te gereken:** takili-kalma skill'i aktif olmalı (5. kural: Telegram Kurtarma Sinyali)

### ÖNEMLİ Kısıt
Local ReYMeN'in kendi başına web'de arama (Tor Browser, web_search, web_extract) yeteneği YOKTUR. Bu nedenle araştırma her zaman Telegram ReYMeN tarafından yapılır.

### Referans
Detaylı akış için: `takili-kalma` skill'indeki `references/kurtarma-akisi.md`