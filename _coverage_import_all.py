#!/usr/bin/env python3
"""ReYMeN Coverage Importer — tüm modülleri coverage altında içe aktarır."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

for root, dirs, files in os.walk("reymen"):
    if "__pycache__" in root or "venv" in root or "node_modules" in root:
        continue
    for f in files:
        if f.endswith(".py") and f != "__init__.py":
            mod_path = os.path.join(root, f)
            mod_name = mod_path.replace(os.sep, ".")[:-3]
            try:
                __import__(mod_name)
            except Exception:
                pass

print("Coverage import scan complete")
