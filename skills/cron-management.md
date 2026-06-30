
> **Kategori:** references

---

## 📋 5N1K

| Soru | Cevap |
|:-----|:------|
| **Kim?** | Tüm ajanlar |
| **Ne?** | Cron Management |
| **Nerede?** | references/ |
| **Ne Zaman?** | İhtiyaç duyulduğunda |
| **Neden?** | Otomatik kategorilendirme |
| **Nasıl?** | Skill referansı ile |

---

# Cron Job Yönetimi — ReYMeN

## Mevcut Cron Jobs

| Job ID | Adı | Zaman | Durum |
|:-------|:----|:------|:------|
| 88fd9b2df0dc | reymen-daily-full-push | 03:00 günlük | ✅ aktif |
| 077f588e8372 | reymen-daily-memory-push | 00:30 günlük | ✅ aktif |
| dc37c9cb8a6a | reymen-weekly-report | 28.06.2026 12:00 | ✅ aktif |
| 3e4395759774 | reymen-test-runner | Her 15dk | ✅ aktif (sonradan açıldı) |
| c3f0e4d6d424 | reymen-hourly-check | Her saat | ⚠️ devre dışı |

## Proje Remote'ları

```
origin  → https://github.com/Watcher-ReYMeN/ReYMeN-Ajan.git
backup  → https://github.com/Watcher-Hermes/hermes-memory-backup.git
full-backup → https://github.com/Watcher-ReYMeN/ReYMeN-full-backup.git
```

## Push Script'leri

- `daily_memory_push.py` — `.ReYMeN/` + `AGENTS.md` + `decisions.md` → `backup master`
- `daily_full_push.py` — tüm proje → `full-backup master`

## Sorun Giderme

### Terminal Bloke Oldu
```
# Önceki komut asılı kaldıysa:
process kill <session_id>

# Gateway'i yeniden başlat:
ReYMeN -p reymen gateway stop
ReYMeN -p reymen gateway start

# Cron tick'i canlandır:
ReYMeN cron tick
```

### Cron Job Ateşlenmiyor
1. `ReYMeN cron status` ile scheduler'ı kontrol et
2. Gateway çalışıyorsa `ReYMeN cron tick` ile manuel tetikle
3. Çalışmıyorsa gateway'i yeniden başlat

### Test Runner Çalışmıyor
```
ReYMeN cron run 3e4395759774  # Job ID ile manuel çalıştır
```
