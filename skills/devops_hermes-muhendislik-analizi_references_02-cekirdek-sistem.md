
> **Kategori:** DevOps

---

## 📋 5N1K

| Soru | Cevap |
|:-----|:------|
| **Kim?** | Tüm ajanlar |
| **Ne?** | Devops_Hermes Muhendislik Analizi_References_02 Cekirdek Sistem |
| **Nerede?** | DevOps/ |
| **Ne Zaman?** | İhtiyaç duyulduğunda |
| **Neden?** | Otomatik kategorilendirme |
| **Nasıl?** | Skill referansı ile |

---

# Bölüm 2: Çekirdek Sistem

## Akış Tablosu

| Obsidian Etiketi | Flow | Yaptığı |
|---|---|---|
| #ogren | _flow_learn | YouTube -> SKILL.md |
| #ReYMeN-kaynak | _flow_ingest | Web/GitHub/txt -> SKILL.md |
| #android | _flow_android | Kod -> Gradle -> APK |
| #video-to-app | _flow_video_to_app | URL -> Öğren -> APK |
| #ReYMeN-yayinla | _flow_publish | APK -> GitHub Releases |
| #ReYMeN-plan | _flow_plan | Hedefi alt adımlara böl |
| #ReYMeN-sor | _flow_ask | Vault RAG cevap |
| #ReYMeN-analyze | _flow_analyze | AST statik analiz |

## BrainRouter — LLM Zinciri

Sorgu geldi
  -> _memory_lookup() (ChromaDB veya JSON cache, 60s TTL)
  -> DeepSeek x3 (minimal_fix -> refactor -> alternative)
  -> Claude x3 (advanced mode, "kıdemli mimar" prompt)
  -> Ollama (lokal fallback)
  -> Başarısızlık raporu

Bütçe Durumları: ok -> warn (%80) -> halt (limit aşıldı)

## Görev Durum Makinesi

PENDING -> RUNNING -> VERIFYING -> COMPLETED
                  -> RECOVERING -> QUARANTINED
