
> **Kategori:** Windows

---

## 📋 5N1K

| Soru | Cevap |
|:-----|:------|
| **Kim?** | Windows ajanı |
| **Ne?** | Windows Automation_Tam Sistem Yetkisi_References_5 ReYMeN Env Dosyas Tam Eri Im Haritas |
| **Nerede?** | Windows/ |
| **Ne Zaman?** | İhtiyaç duyulduğunda |
| **Neden?** | Otomatik kategorilendirme |
| **Nasıl?** | Skill referansı ile |

---

## 5. ReYMeN .env Dosyası Tam Erişim Haritası

| Dosya | Yol |
|-------|-----|
| Ana .env | `C:\Users\marko\AppData\Local\hermes\.env` |
| config.yaml | `C:\Users\marko\AppData\Local\hermes\config.yaml` |
| ReYMeN-ai .env | `C:\Users\marko\ReYMeN-ai\.env` |
| Auth | `C:\Users\marko\AppData\Local\hermes\auth.json` |

### .env'den belirli değeri oku

```python
import re
from pathlib import Path

def get_env_value(env_path: str, key: str) -> str:
    text = Path(env_path).read_text(encoding="utf-8")
    m = re.search(rf"^{re.escape(key)}\s*=(.+)", text, re.MULTILINE)
    return m.group(1).strip() if m else ""

token = get_env_value(
    r"C:\Users\marko\AppData\Local\hermes\.env",
    "TELEGRAM_BOT_TOKEN"
)
```

---