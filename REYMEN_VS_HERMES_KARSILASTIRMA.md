# ReYMeN Agent vs Hermes Agent — Detaylı Karşılaştırma

**Tarih:** 2026-06-29
**Analiz Kapsamı:** `C:\Users\marko\Desktop\Reymen Proje\ReYMeN-Ajan\reymen/` altındaki tüm .py dosyaları + hermes_legacy referansları

---

## 1. ÖZET TABLOSU

| # | Özellik | ReYMeN | Hermes | Fark |
|---|---------|--------|--------|------|
| 1 | **Gateway Sistemi** (multi-platform) | ⚠️ Kısmi | ✅ Tam | Sadece Telegram+Discord bot; Slack, WhatsApp, SMS, email yok. Gateway "state JSON" basit dosya |
| 2 | **Plugin Sistemi** (discovery/load/hot-reload) | ⚠️ Kısmi | ✅ Tam | PluginManager var ama hot-reload yok, provider plugin (browser/image/video/tts/stt) kavramı yok |
| 3 | **MCP Client** (auto-discovery+background+reconnect) | ⚠️ Kısmi | ✅ Tam | native_mcp_client.py var, exponential backoff var ama auto-reconnect test edilmemiş |
| 4 | **Tool Registry** (check_fn/toolset/HITL) | ✅ Var | ✅ Tam | check_fn TTL cache (30sn), ToolsetManager, schema override, alias var. HITL yok |
| 5 | **Provider Sistemi** (model routing/failover) | ❌ Eksik | ✅ Tam | Provider ABC yok, model routing yok, failover sadece hata sınıflandırma seviyesinde |
| 6 | **Session DB** (FTS5+trigram) | ❌ Eksik | ✅ Tam | conversation_loop `AdvancedSessionStorage` import ediyor ama gerçek FTS5/trigram sistemi yok |
| 7 | **Cron/Scheduler** | ❌ Eksik | ✅ Tam | hermes_legacy/tools/cronjob_tool.py var ama reymen/core'da aktif cron sistemi yok. Sadece CLI handler |
| 8 | **Web UI** (dashboard) | ✅ Var | ✅ Tam | FastAPI+Jinja2+HTMX, auth provider pattern, log stream, process manager, module discovery. Eksik: cron management, kanban dashboard |
| 9 | **A2A/ACP** | ⚠️ Kısmi | ✅ Tam | a2a.py basit in-memory queue broker. A2ADistributed HTTP/WS transport var. ACP yok |
| 10 | **OAuth 2.0** | ❌ Eksik | ✅ Tam | web_ui/auth.py sadece password auth. OAuth provider yok (Google/GitHub/Discord) |
| 11 | **Kanban** | ✅ Var | ✅ Tam | Board+Card+Worker lifecycle. Swarm mode yok |
| 12 | **Context Compression** | ✅ Var | ✅ Tam | ContextCompressor(max_token=4096) var. Otomatik eşik tabanlı compression conversation_loop'da |
| 13 | **Prompt Caching** | ⚠️ Kısmi | ✅ Tam | PromptCache var (LRU+TTL, hash tabanlı). Hermes'te semantic caching (embedding-benzerlik) |
| 14 | **Cost Tracking** | ✅ Var | ✅ Tam | SQLite destekli CostTracker, session_id bazlı, model bazlı özet. Per-session tracking var |
| 15 | **Security** (sandbox/PII/guardrails) | ⚠️ Kısmi | ✅ Tam | Sandbox var (subprocess+module allowlist). PII redaction var ama opsiyonel. Threat pattern yok |
| 16 | **Memory** (vector/hybrid) | ❌ Eksik | ✅ Tam | MemoryManager sadece MEMORY.md+USER.md dosya bazlı. Vector memory, embedding, hybrid retrieval yok |
| 17 | **Skills** (library/activation/sync) | ⚠️ Kısmi | ✅ Tam | skill_utils'de aktivasyon, index, eval var. Hermes'te skill library, sync, evaluation pipeline |
| 18 | **Self-improvement** | ✅ Var | ✅ Tam | SQLite metrik, trend analizi, kod kalite analizi, otomatik hedef. conversation_loop hook |
| 19 | **Config** (YAML profile/env) | ❌ Eksik | ✅ Tam | YAML config sistemi yok. Hard-coded yollar, dict tabanlı config |
| 20 | **CLI** (TUI/slash commands) | ✅ Var | ✅ Tam | Rich TUI, mixin tabanlı CLI, session management |
| 21 | **Delegation** (subagent/ACP) | ❌ Eksik | ✅ Tam | delegate_tool.py sadece hermes_legacy'de. Aktif subagent sistemi yok |
| 22 | **Backup** | ❌ Eksik | ✅ Tam | Otomatik backup sistemi yok |
| 23 | **Code Execution** | ✅ Var | ✅ Tam | guvenli_sandbox.py: timeout, module allowlist, output limit, dangerous keyword blocking |
| 24 | **Image Generation** | ⚠️ Kısmi | ✅ Tam | araclar_goruntu.py var ama FAL/OpenAI/xAI entegrasyonu yok |
| 25 | **Voice/TTS** | ❌ Eksik | ✅ Tam | Edge TTS/OpenAI TTS entegrasyonu yok |
| 26 | **Browser Automation** | ⚠️ Kısmi | ✅ Tam | Browser tools var ama Playwright MCP/Browser Use entegrasyonu yok |
| 27 | **Web Search** | ✅ Var | ✅ Tam | web_search_tool.py var. Multi-backend (Firecrawl/Brave/DDG/Tavily/Exa/xAI) desteği |
| 28 | **MCP Server** (Streamable HTTP) | ✅ Var | ✅ Tam | core/mcp_server.py: tools/list, resources/list, prompts/list, Streamable HTTP, stdio |
| 29 | **Platform Adapter** | ✅ ReYMeN'e özel | ⚠️ | Windows/WSL/Kali adapter — Hermes'te yok |

---

## 2. REYMeN'DE TAMAMEN EKSİK OLAN ÖZELLİKLER

### ❌ 2.1 Provider Sistemi (Model Routing + Failover)

**Durum:** Tamamen eksik

Hermes'te `AbstractProvider` ABC, model routing, failover zinciri, provider switching, cost-per-model tracking vardır. ReYMeN'de:
- Model routing yok — LLM çağrıları doğrudan OpenAI/Anthropic client'larına gider
- Provider failover yok (sadece `hata_siniflandirici` ile hata tespiti var, otomatik switch yok)
- `_HATA_SINIFLANDIRICI_AKTIF` var ama sonrası otomatik geçiş yok

**Çözüm:** `AbstractProvider` ABC + `ProviderRegistry` singleton + model routing tablosu + failover zinciri

### ❌ 2.2 Gateway Sistemi (Multi-Platform)

**Durum:** Sadece Telegram bot var, gateway mimarisi yok

Hermes'te `Gateway` ABC ile Telegram, Discord, CLI, Slack, WhatsApp, SMS, email tek bir interface altında toplanır. ReYMeN'de:
- `reymen/telegram_bot/` — sadece Telegram
- `reymen/ag/discord_bot.py` — ayrı bir Discord bot
- Unified gateway interface (start/stop/routing/message queue) yok
- `gateway_state.json` basit bir durum dosyası

**Çözüm:** `PlatformAdapter` seviyesinde Gateway ABC + platform registry + mesaj routing

### ❌ 2.3 Session DB (FTS5 + Trigram Arama)

**Durum:** Tamamen eksik

Hermes'te SQLite FTS5 + trigram arama ile session geçmişinde tam metin arama vardır. ReYMeN'de:
- `conversation_loop.py` `AdvancedSessionStorage` import ediyor ama bu modül `reymen/hafiza/session_db.py` olarak mevcut değil
- Session yönetimi bellek içi (in-memory), kalıcı değil
- Session search/resume/management yok

**Çözüm:** SQLite FTS5 tabanlı session storage + trigram arama + session resume

### ❌ 2.4 Cron/Scheduler Sistemi

**Durum:** Tamamen eksik

Hermes'te per-job model override, no_agent mode, context_from chain, workdir, script runner, watchdog pattern ile cron vardır. ReYMeN'de:
- `hermes_legacy/tools/cronjob_tool.py` var ama anakoda entegre değil
- `reymen/sistem/cli_commands/handlers/tools/cron_handler.py` CLI handler var ama arka plan scheduler yok
- `self_improve_cron.py` sadece self-improvement için

**Çözüm:** APScheduler/arq tabanlı cron sistemi + per-job model override + workdir

### ❌ 2.5 OAuth 2.0

**Durum:** Tamamen eksik

Hermes'te Google, GitHub, Discord OAuth provider'ları vardır. ReYMeN'de:
- `web_ui/auth.py` sadece `PasswordAuthProvider` — kullanıcı adı/şifre
- `ROLE_PERMISSIONS` var ama OAuth akışı yok
- `hermes_legacy/tools/mcp_oauth.py` var ama entegre değil

**Çözüm:** OAuth provider registry + Google/GitHub/Discord provider'ları + JWT token refresh

### ❌ 2.6 Vector Memory / Embedding

**Durum:** Tamamen eksik

Hermes'te ChromaDB/Qdrant tabanlı vector memory + hybrid search + embedding generation vardır. ReYMeN'de:
- `hafiza/memory_manager.py` sadece dosya tabanlı (MEMORY.md + USER.md)
- Vector embedding yok
- Semantic search yok
- `hermes_legacy/tools/memory_providers/chromadb_provider.py` var ama anakoda entegre değil

**Çözüm:** ChromaDB/Qdrant entegrasyonu + embedding pipeline + hybrid retrieval (vector + keyword)

### ❌ 2.7 Delegation / Subagent Sistemi

**Durum:** Tamamen eksik

Hermes'te ACP/Copilot protokolü ile subagent task delegation vardır. ReYMeN'de:
- `hermes_legacy/tools/delegate_tool.py` var ama anakoda entegre değil
- A2A agent mesajlaşma var ama subagent lifecycle yok
- Task decomposition + parallel execution yok

**Çözüm:** A2A üzerine subagent manager + task decomposition + sonuç toplama

### ❌ 2.8 Backup Sistemi

**Durum:** Tamamen eksik

Hermes'te otomatik, periyodik backup sistemi vardır. ReYMeN'de:
- Otomatik backup yok
- Konfigürasyon/veritabanı yedekleme yok
- Disaster recovery planı yok

**Çözüm:** Schedule-based backup + incremental backup + restore command

### ❌ 2.9 Guardrails / Threat Pattern Detection

**Durum:** Tamamen eksik

Hermes'te built-in threat patterns, PII redaction, request/response guardrails vardır. ReYMeN'de:
- `reymen/guvenlik/redact.py` var ama opsiyonel
- `hermes_legacy/tools/tool_guardrails.py` var ama anakoda entegre değil
- Aktif guardrail pipeline yok

**Çözüm:** Guardrail pipeline (input/output) + threat pattern DB + PII detection + rate limiting

### ❌ 2.10 YAML Config / Profile Sistemi

**Durum:** Tamamen eksik

Hermes'te profile-based YAML config + env passthrough + config merge vardır. ReYMeN'de:
- Hard-coded yollar (`ROOT = Path(__file__).parent`)
- `config.yaml` okunur ama yapılandırılmış profile sistemi yok
- Environment variable passthrough yok
- Config validation yok

**Çözüm:** YAML config loader + profile inheritance + env variable expansion + schema validation

---

## 3. REYMeN'DE KISMEN VAR OLAN ÖZELLİKLER

### ⚠️ 3.1 MCP Client (Native)

**Mevcut:** `reymen/mcp/mcp_manager.py` + `reymen/arac/native_mcp_client.py`
**Eksik:**
- auto-discovery sadece motor başlangıcında, runtime'da değil
- background reconnect var ama test edilmemiş (exponential backoff docker)
- Tool caching/refresh sistemi yok
- Notification handler yok

### ⚠️ 3.2 Plugin Sistemi

**Mevcut:** `reymen/sistem/plugin_manager.py` + `PluginYukleyici`
**Eksik:**
- Hot-reload yok (plugin değişikliklerini runtime'da algılama)
- Provider plugin kavramı yok (browser, image_gen, video_gen, tts, stt)
- Plugin dependency graph yok
- Plugin sandbox yok

### ⚠️ 3.3 Skills Sistemi

**Mevcut:** `skill_utils` (aktivasyon, index, eval, kategori)
**Eksik:**
- Skill library (centralized repo sync) yok
- Auto-activation mechanics yok
- Skill evaluation pipeline zayıf
- Cross-session skill state yok

### ⚠️ 3.4 Web Search

**Mevcut:** `reymen/arac/web_search_tool.py`
**Eksik:**
- Multi-backend abstraction yok (Firecrawl/Brave/DDG/Tavily/Exa/xAI)
- Sadece tek backend
- Search history/caching yok

### ⚠️ 3.5 Image Generation

**Mevcut:** `reymen/arac/araclar_goruntu.py`
**Eksik:**
- FAL/OpenAI/xAI entegrasyonu yok
- Provider-agnostik image gen API yok
- Image generation bir tool olarak kayıtlı değil (motor.py import listesinde)

### ⚠️ 3.6 Browser Automation

**Mevcut:** Browser CLI handler + `araclar_tarayici` modülleri
**Eksik:**
- Playwright MCP entegrasyonu yok
- Browser Use entegrasyonu yok
- Headless browser session management yok

### ⚠️ 3.7 Security / Sandbox

**Mevcut:** `reymen/guvenlik/guvenli_sandbox.py`
**Eksik:**
- Subprocess tabanlı (Docker sandbox değil)
- Module allowlist çok kısıtlı
- File system restriction yok
- Network restriction yok

---

## 4. REYMeN'DE FAZLA OLAN ÖZELLİKLER (Hermes'te yok)

| # | Özellik | Açıklama |
|---|---------|----------|
| 1 | **Platform Adapter** (WSL/Kali/Windows) | platform_adapter.py — Windows/WSL arası yol çevirisi, Kali adapter. Hermes sadece native çalışır |
| 2 | **CUA (Computer Use Agent)** | Bilgisayar kullanımı için CUA motor aracı |
| 3 | **Hook Dispatcher Sistemi** | Async event-driven hook sistemi (TOOL_CALLED, TOOL_ERROR gibi olaylar) |
| 4 | **Iteration Budget** | conversation_loop'da adım limiti + bütçe takibi |
| 5 | **Hata Sınıflandırıcı + Mesaj Tamirci** | API hatalarını sınıflandırma, tool call argüman temizleme, mesaj sırası tamiri |
| 6 | **MessageBroker** | queue.Queue tabanlı, pipeline görev çözümü (GÖREV -> PLAN -> KOD -> TEST -> İNCELE -> KAYDET) |
| 7 | **Self-improvement Script** | Kod kalite analizi + metrik takibi + otomatik iyileştirme hedefi |
| 8 | **Türkçe Dil Desteği** | Tüm kod tabanı Türkçe değişken/fonksiyon isimleri, Türkçe dokümantasyon |

---

## 5. KOD KALİTESİ FARKLARI

| Kriter | ReYMeN | Hermes |
|--------|--------|--------|
| **Type Hints** | ⚠️ Kısmen (bazı dosyalarda yok, `Optional` eski stil) | ✅ Tam (modern typing, `| None` syntax) |
| **Error Handling** | ⚠️ Zayıf (`try/except: pass` çok yaygın, sessiz hata yutma) | ✅ Sağlam (specific exception handling, logging) |
| **Test Coverage** | ⚠️ Çok az test (`test/` dizininde 7-8 test dosyası) | ✅ Yüksek (pytest, conftest, GitHub Actions) |
| **Logging** | ⚠️ Tutarsız (bazı yerde `print()`, bazı yerde `logging`) | ✅ Tutarlı (yapılandırılmış logging pipeline) |
| **Async Kullanımı** | ⚠️ Kısmen (sync+async karışık, `run_in_executor`) | ✅ Tam async (asyncio native) |
| **Dependency Management** | ❌ Zayıf (her modül kendi import'ını try/except ile dener) | ✅ Güçlü (dependency injection, lazy loading) |
| **Config Yönetimi** | ❌ Dağınık (hard-coded path'ler, ROOT = Path(__file__).parent) | ✅ Merkezi (YAML config, profile inheritance) |
| **Dockerization** | ❌ Yok | ✅ Docker support |

---

## 6. MİMARİ FARKLAR

| Kriter | ReYMeN | Hermes |
|--------|--------|--------|
| **Modülerlik** | ⚠️ Orta — büyük dosyalar var (motor.py 1983 satır, conversation_loop.py 2230 satır) | ✅ Yüksek — her özellik ayrı modül/plugin |
| **Bağımlılık Yönetimi** | ❌ Gevşek — her modül kendi import'larını try/except ile dener | ✅ Sıkı — dependency injection, explicit registration |
| **Config Akışı** | ❌ Dağınık — her modül kendi yollarını tanımlar | ✅ Merkezi — tek config noktasından dağıtım |
| **Genişletilebilirlik** | ⚠️ Orta — plugin sistemi var ama hot-reload yok | ✅ Yüksek — plugin, provider, gateway extension points |
| **Test Edilebilirlik** | ❌ Düşük — singleton'lar, global state, import-time side effects | ✅ Yüksek — dependency injection, test fixtures |

---

## 7. ÖNCELİKLİ EKSİKLER (Hangi Sırayla Tamamlanmalı)

### P0 — Kritik (Temel İşlevsellik)
1. **Provider Sistemi** — Model routing + failover olmadan agent güvenilir çalışmaz
2. **YAML Config** — Hard-coded yollar ve dağınık config sürdürülemez
3. **Error Handling İyileştirme** — `try/except: pass` kalıpları hata ayıklamayı imkansız kılıyor

### P1 — Yüksek Öncelik
4. **Cron/Scheduler** — Zamanlanmış görevler için kritik
5. **Session DB (FTS5)** — Session yönetimi ve geri yükleme için
6. **Gateway Sistemi** — Multi-platform desteği için temel

### P2 — Orta Öncelik
7. **Vector Memory** — Anlamsal bellek ve arama için
8. **OAuth** — Web UI güvenliği için
9. **Backup Sistemi** — Veri koruması için
10. **Delegation** — Paralel görev çözümü için

### P3 — Düşük Öncelik
11. **Guardrails** — Güvenlik katmanı
12. **Skills Library** — Skill paylaşımı
13. **Image/Video Generation** — Multimodal yetenekler
14. **Voice/TTS** — Sesli etkileşim

---

## 8. İSTATİSTİKLER

- **Toplam Python dosyası (reymen/):** ~100
- **Hermes'te olan ama ReYMeN'de tamamen eksik:** ~10 özellik
- **Hermes'te olan ama ReYMeN'de kısmen var:** ~7 özellik
- **ReYMeN'de olup Hermes'te olmayan:** ~8 özellik
- **Kod kalitesi farkı:** Orta (ReYMeN'de çok sayıda `try/except: pass` ve print-based logging)
