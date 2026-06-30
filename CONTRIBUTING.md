# Katki Rehberi / Contributing Guide

ReYMeN'e katkida bulunmak istediginiz icin tesekkurler!

## Baslarken / Getting Started

1. **Fork** et -> [github.com/Watcher-Hermes/ReYMeN-Ajan](https://github.com/Watcher-Hermes/ReYMeN-Ajan)
2. **Clone**:
   ```bash
   git clone https://github.com/<kullanici>/ReYMeN-Ajan.git
   cd ReYMeN-Ajan
   ```
3. **Ortami kur**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   pip install -e ".[dev]"
   pre-commit install
   ```
4. **Branch ac**:
   ```bash
   git checkout -b feature/ozellik-adi
   # veya
   git checkout -b fix/hata-adi
   ```

## Branch Stratejisi
- `main` — kararli surum
- `feature/xyz` — yeni ozellik
- `fix/xyz` — hata duzeltme
- `docs/xyz` — dokumantasyon

## Test
```bash
# Tum testler
pytest tests/ --ignore=tests/ReYMeN_reference -v

# Tek dosya
pytest tests/test_kanban.py -v

# Coverage
coverage run --source=reymen -m pytest tests/ --ignore=tests/ReYMeN_reference -q
coverage report
```

## Kod Standartlari
| Kural | Aciklama |
|-------|----------|
| Lint | `ruff check reymen/` (on-commit otomatik) |
| Format | `ruff format reymen/` |
| Guvenlik | `bandit -r reymen/ -ll` (on-commit otomatik) |
| `shell=True` | KESINLIKLE KULLANMA |
| `except: pass` | Sessiz except KABUL EDILMEZ, logla |
| Tip ipucu | Mumkunse ekle |
| Test | Her yeni ozellik icin test sart |

## PR Sureci
1. Feature branch'inde kodla
2. Test ekle (happy path + 1 hata senaryosu)
3. `pre-commit` calistir: `pre-commit run --all-files`
4. PR ac, aciklama yaz (`Closes #N` eklemeyi unutma)
5. CI gecip gecmedigini kontrol et
6. Review bekle

## Proje Yapisi
```
reymen/
  core/           # Ana moduller (session_db, config_manager, ...)
  cereyan/        # Ogrene dongusu, self-improvement
  hafiza/         # Memory management
  guvenlik/       # Guvenlik katmani (redact, guardrails, oauth)
  arac/           # Araclar (tool registry, web search, ...)
  ag/             # Gateway, bot, protocol
  sistem/         # CLI, plugin, cron, terminal backends
  reymen_cli/     # CLI komutlari
  scripts/        # Yardimci scriptler
  test/           # Testler
tests/            # Entegrasyon testleri
```

## Iletisim
- Telegram: @Pasa_38
- E-posta: marko@reymen.dev
- GitHub Issues: Hata ve ozellik talepleri
