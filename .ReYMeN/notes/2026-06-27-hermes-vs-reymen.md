# ReYMeN > ReYMeN — Üstünlük Analizi

> ReYMeN ReYMeN'in fork'udur, doğası gereği ReYMeN'in bazı özelliklerini taşımaz.
> İşte ReYMeN'in ReYMeN'den AÇIK ARA üstün olduğu alanlar.

---

## 1. Skill/Tool Ekosistemi (EN BÜYÜK FARK)

| Metrik | ReYMeN | ReYMeN | Fark |
|--------|--------|--------|------|
| Skills | **554** plugin/kategori | **5** SKILL.md | **110x** |
| Tool registry | 50+ hazır tool | ~15 tool | **3x** |
| Web search | Firecrawl MCP + web_extract | DuckDuckGo | Kalite farkı |
| MCP client | Native (config.yaml → otomatik) | Elle yazılmış | **Gömülü vs manuel** |

**ReYMeN:** `hermes_tools` ile 50+ tool tek import. Firecrawl, Perplexity, Playwright MCP config'e yaz → otomatik bağlanır.
**ReYMeN:** Her tool ayrı .py dosyası, manuel import, manuel hata yönetimi.

> **Kazanç:** ReYMeN 2 saatte entegre eder, ReYMeN 2 günde.

---

## 2. Cross-Session Hafıza (FTS5)

| Özellik | ReYMeN | ReYMeN |
|---------|--------|--------|
| Arama motoru | **SQLite FTS5** | OnceHafiza (basit LIKE/ID) |
| Geçmiş sorgu | `session_search("konu")` → 3 sn | OnceHafiza.ara() → keyword eşleşme |
| Puanlama | FTS5 ranking + lineage dedup | Sigmoid güven (basit) |
| Scroll | ±20 mesaj pencere | Yok |
| Profil ayrı | Her profile ayrı DB | 3 bot ortak DB |

**ReYMeN:** "Geçen ayki X konusunu bul" → 3 saniye, doğru sonuç.
**ReYMeN:** "X konusunda ne konuştuk" → keyword gir → belki bulur.

> **Kazanç:** ReYMeN'in hafızası **Google gibi**, ReYMeN'in hafızası **dizin kartı gibi.**

---

## 3. Çoklu Ortam (Multimodal)

| Özellik | ReYMeN | ReYMeN |
|---------|--------|--------|
| Görsel analiz | ✅ `vision_analyze()` — VLM | ❌ Yok (sadece OpenCV OCR) |
| Görsel üretim | ✅ FAL.ai FLUX 2 Klein 9B | ✅ `resim_olustur()` (basit) |
| Ses (TTS) | ✅ OpenAI TTS (doğal) | ✅ pyttsx3 (robotik) |
| Ses tanıma | ✅ Whisper STT | ❌ Yok |
| Video | ✅ HyperFrames, Remotion | ❌ Yok |

**ReYMeN:** Bir resmi analiz eder, üstüne konuşur, sesle yanıt verir.
**ReYMeN:** Metin girer → metin çıkar. Görsel işlemler sınırlı.

> **Kazanç:** ReYMeN **5 duyulu**, ReYMeN **sadece metin.**

---

## 4. Tarayıcı Otomasyonu

| Özellik | ReYMeN | ReYMeN |
|---------|--------|--------|
| Engine | Playwright MCP + Browser-Use | Playwright wrapper |
| Web sayfası okuma | `web_extract()` → markdown | `web_ara()` → DuckDuckGo |
| Form doldurma | Browser-Use AI ajan | Elle kod |
| Ekran görüntüsü | Playwright screenshot | Selenium screenshot |
| Hata yönetimi | Timeout → retry → fallback | try/except basit |

**ReYMeN:** "Şu siteye git, şu formu doldur, sonucu al" — AI karar verir.
**ReYMeN:** "Şu URL'den veri çek" — elle yazılmış selector.

> **Kazanç:** ReYMeN **gözüyle görüp karar verir**, ReYMeN **tarif edileni yapar.**

---

## 5. Zamanlanmış Görevler (Cron)

| Özellik | ReYMeN | ReYMeN |
|---------|--------|--------|
| API | `cronjob(action='create', schedule='30m')` | ❌ Yok |
| Çıktı yönlendirme | Telegram, Discord, SMS | ❌ |
| Zincirleme | `context_from` ile A→B→C | ❌ |
| Tekrarlı/periyodik | interval, cron, one-shot | ❌ |
| Watchdog | script ile threshold → bildirim | ❌ |

**ReYMeN:** "Her saat başı altın fiyatını sorgula, Telegram'a gönder" — tek komut.
**ReYMeN:** Ya elle çalıştır ya da Windows Scheduled Task ile manuel kur.

> **Kazanç:** ReYMeN **otonom**, ReYMeN **bağımlı.**

---

## 6. ACP / Harici AI Entegrasyonu

| Özellik | ReYMeN | ReYMeN |
|---------|--------|--------|
| Claude Code | ACP subprocess | ❌ Yok |
| Codex CLI | ACP subprocess | ❌ Yok |
| Herhangi MCP client | Native MCP server host | ❌ MCP client var, server yok |

**ReYMeN:** Claude Code, Copilot, Codex — hepsi ReYMeN'in tool'larını kullanabilir.
**ReYMeN:** Kendi içinde çalışır, harici ajanlarla konuşamaz.

---

## 7. Topluluk & Güncelleme

| Özellik | ReYMeN | ReYMeN |
|---------|--------|--------|
| Geliştirici | **Nous Research** (ekip) | **Tek kişi** (sen) |
| Güncelleme | Haftalık commit | Sen ne zaman yaparsan |
| Hata raporu | GitHub Issues | Sadece sen |
| PR review | Community | Kendin |
| Dokümantasyon | ReYMeN-agent.nousresearch.com | AGENTS.md + SOUL.md |

**ReYMeN:** Bir hata bulursan 1 haftada fix gelir.
**ReYMeN:** Bir hata bulursan sen fix'lersin.

---

## 8. Web Arama Kalitesi

| Özellik | ReYMeN | ReYMeN |
|---------|--------|--------|
| Engine | Firecrawl + Perplexity MCP | DuckDuckGo (limiti 5 sn) |
| Markdown çıktı | Firecrawl temiz markdown | Ham HTML |
| PDF okuma | Firecrawl PDF → markdown | ❌ Yok |
| 404 yönetimi | Retry → fallback | ❌ Yok |

**ReYMeN:** Wikipedia, arxiv, haber — temiz markdown, kaynak belirtir.
**ReYMeN:** DuckDuckGo — hızlı, sığ, limitsiz değil.

---

## ÖZET: Puan Tablosu

| # | Kategori | ReYMeN | ReYMeN | Fark |
|---|----------|--------|--------|------|
| 1 | Skill ekosistemi | 554 tool | 5 SKILL.md | **110x** |
| 2 | Cross-session hafıza | FTS5 full-text | Keyword LIKE | **10x** |
| 3 | Multimodal | Görsel + Ses + Video | Sadece metin | **5x** |
| 4 | Tarayıcı | AI kararlı Playwright | Elle kod | **3x** |
| 5 | Cron | `cronjob()` API | Yok | **∞** |
| 6 | ACP entegrasyon | Claude Code + Codex | Yok | **∞** |
| 7 | Topluluk | Nous Research | Tek kişi | **∞** |
| 8 | Web arama | Firecrawl + Perplexity | DuckDuckGo | **3x** |

**ReYMeN kazanır:** 8/8 kategoride üstün.

**Ama ReYMeN'in gücü:** ReYMeN'in ihtiyacı olmayan ama senin ihtiyacın olan şeyler:
- Türkçe doğal dil
- OnceHafiza'dan öğrenme + karar ağacı
- 3 bot, 3 profil — Telegram ekosistemi
- Hafıza > Cache > LLM optimizasyonu
- Overengineering yok, pragmatik çözümler

ReYMeN **platform**, ReYMeN **senin aracın.**
