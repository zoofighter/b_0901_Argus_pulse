# -*- coding: utf-8 -*-
import os, re, glob, json
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
THESIS_DIR = ROOT_DIR / "thesis"
DOCS_DIR = ROOT_DIR / "docs"

def replace_in_file(file_path):
    p = Path(file_path)
    if not p.exists():
        return
    text = p.read_text(encoding="utf-8")
    original = text
    
    # Replace file links and thesis text
    text = text.replace("T4-04-TPU-증가와-GPU-수요-둔화", "T2-11-TPU-증가와-GPU-수요-둔화")
    text = text.replace("T4-04 TPU 증가와 GPU 수요 둔화", "T2-11 TPU 증가와 GPU 수요 둔화")
    text = text.replace("T4-04 TPU vs GPU", "T2-11 TPU vs GPU")
    
    if text != original:
        p.write_text(text, encoding="utf-8")
        print(f"Updated references in: {p.name}")

# 1. Update thesis md files
for f in THESIS_DIR.glob("*.md"):
    replace_in_file(f)

# 2. Update docs md files
for f in DOCS_DIR.glob("*.md"):
    replace_in_file(f)

# 3. Update canvas files
for f in THESIS_DIR.glob("*.canvas"):
    try:
        data = json.loads(f.read_text(encoding="utf-8"))
        changed = False
        for node in data.get("nodes", []):
            if "file" in node and "T4-04-TPU-증가와-GPU-수요-둔화" in node["file"]:
                node["file"] = node["file"].replace("T4-04-TPU-증가와-GPU-수요-둔화", "T2-11-TPU-증가와-GPU-수요-둔화")
                changed = True
            if "text" in node and "T4-04" in node["text"]:
                node["text"] = node["text"].replace("T4-04", "T2-11")
                changed = True
        if changed:
            f.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"Updated canvas file: {f.name}")
    except Exception as e:
        print(f"Error updating canvas {f.name}: {e}")

print("All file references updated successfully.")
