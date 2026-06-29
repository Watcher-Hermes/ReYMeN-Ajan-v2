
import json
from pathlib import Path

DURUM = Path(__file__).resolve().parent / "durum.json"
with open(DURUM, encoding="utf-8") as f:
    data = json.load(f)

cov = data.get("coverage_durumu", {})
print("coverage_durumu type:", type(cov).__name__)
print("coverage_durumu keys:", list(cov.keys()))

core = cov.get("core_moduller", {})
print("core_moduller type:", type(core).__name__)
print("core_moduller keys:", list(core.keys()))

for mod, info in core.items():
    print("  %s: tamamlandi=%s, simdi=%s" % (mod, info.get("tamamlandi"), info.get("simdi")))

# What does the new script's _sync produce?
data["tamamlanan_moduller"] = {}
for mod, info in core.items():
    if info.get("tamamlandi"):
        data["tamamlanan_moduller"][mod] = {
            "tamamlandi": True,
            "coverage": info.get("simdi", "?"),
            "test_sayisi": info.get("test_sayisi", 0),
        }

print("\nYeni tamamlanan_moduller (%d modul):" % len(data["tamamlanan_moduller"]))
for mod, info in data["tamamlanan_moduller"].items():
    print("  %s: %s" % (mod, info))
