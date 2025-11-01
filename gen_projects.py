#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, json, re

ROOT = "assets/projects"
OUT = os.path.join(ROOT, "projects.json")
IMG_EXTS = (".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp")

def titleize(s: str) -> str:
    s = s.replace("-", " ").replace("_", " ").strip()
    return " ".join(w.capitalize() for w in s.split())

def natural_key(s: str):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", s)]

CATEGORY_MAP = {
    "F": "Fencing & gates",
    "P": "Patios & decking",
    "B": "Inside tiling & interior renovations",
    "G": "Garden & landscaping",
}

items = []
if not os.path.isdir(ROOT):
    raise SystemExit(f"Missing {ROOT}")

for name in sorted(os.listdir(ROOT), key=natural_key):
    path = os.path.join(ROOT, name)
    if not os.path.isdir(path): 
        continue
    if name.startswith(".") or name in ("assets_full", "projects.json"):
        continue

    files = [f for f in os.listdir(path) if f.lower().endswith(IMG_EXTS)]
    if not files:
        continue

    # preferuj cover.*
    cover_candidates = [f for f in files if os.path.splitext(f)[0].lower() == "cover"]
    cover = sorted(cover_candidates, key=str.lower)[0] if cover_candidates else sorted(files, key=str.lower)[0]

    cat = CATEGORY_MAP.get(name[0].upper(), "Uncategorized")
    images = [f"{ROOT}/{name}/{fn}" for fn in sorted(files, key=str.lower)]

    items.append({
        "id": name,
        "title": titleize(name),
        "category": cat,
        "coverImage": f"{ROOT}/{name}/{cover}",
        "images": images
    })

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=2)

print(f"Saved {len(items)} entries -> {OUT}")
