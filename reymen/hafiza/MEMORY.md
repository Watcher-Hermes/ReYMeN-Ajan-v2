# ReYMeN Kalıcı Hafıza

## Proje
- Ana dizin: `C:\Users\marko\Desktop\Reymen Proje\ReYMeN-Ajan`
- GitHub: Watcher-ReYMeN/ReYMeN-Ajan (private)
- Model: deepseek-v4-flash (deepseek) — öncelik 1
- Aktif profil: reymen

## Önemli Bilgiler
- Provider zinciri: deepseek → xiaomi → xai → openrouter → groq → lmstudio
- WEB_ARA: Firecrawl → Brave → DDG (sıralı fallback)
- Cron: `.ReYMeN/cron/` altında JSON tabanlı, CronScheduler ile yönetilir
- Kullanıcı: Marko/Q! — mobil remote desktop, kopyalama yapamaz
- Dil: Türkçe, kısa/direkt, tablo+emoji çıktı

## Aktif Özellikler
- WEB_ARA (Firecrawl + Brave + DDG)
- TARAYICI_AC (Playwright headless)
- GORUNTU_ANALIZ (LLaVA/Ollama)
- RESIM_OLUSTUR (FAL.ai)
- VISION_ANALIZ (FAL.ai vision)
- HAFIZA_OKU / BECERI_BUL
- CronScheduler (yerleşik cron motoru)
- SQLite + Vektör DB + JSON bellek
- ConversationLoop (tam pipeline)
- Plugin Sistemi (15+ plugin)
- Skill Sistemi (FTS5 index, 1114 skill dosyası)

## Eksikler / Yapılacak
- Mail gateway henüz yok
- Self-Improvement cron aktif ama kod eksik
- Dead code oranı %5-10

## Bilinen Pitfall'lar
- Bot restart gerekli: durum.json/SOUL.md/kod değişikliği sonrası bot process restart ZORUNLU
- Dosya varlığı ≠ çalışma durumu: 6 katmanlı pipeline kontrolü yap
- "Yok" demeden önce 3 farklı yöntemle doğrula (dosya sistemi, process, store)

> **Not:** Ana memory kaynağı `.ReYMeN/memories/MEMORY.md`'dir. Bu dosya onunla senkronizedir.
