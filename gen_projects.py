#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Generator assets/projects/projects.json
# Skanuje foldery w assets/projects/* i tworzy listę obiektów dla strony

import os, json, re

ROOT = "assets/projects"
OUT_PATH = os.path.join(ROOT, "projects.json")
IMG_EXTS = (".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp")

def titleize(s: str) -> str:
    s = s.replace("-", " ").replace("_", " ").strip()
    return " ".join(w.capitalize() for w in s.split())

def natural_key(s: str):
    # sortowanie naturalne: G1, G2, G10...
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", s)]

items = []

if not os.path.isdir(ROOT):
    raise SystemExit(f"Brak katalogu: {ROOT}")

for name in sorted(os.listdir(ROOT), key=natural_key):
    path = os.path.join(ROOT, name)
    if not os.path.isdir(path):
        continue
    if name.startswith(".") or name == "assets_full" or name == "projects.json":
        continue

    files = sorted([f for f in os.listdir(path) if f.lower().endswith(IMG_EXTS)])
    if not files:
        continue

    cover = files[0]
    items.append({
        "id": name,
        "title": titleize(name),
        "category": "Uncategorized",
        "coverImage": f"{ROOT}/{name}/{cover}"
    })

with open(OUT_PATH, "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=2)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Generator assets/projects/projects.json
# Skanuje foldery w assets/projects/* i tworzy listę obiektów dla strony

import os, json, re

ROOT = "assets/projects"
OUT_PATH = os.path.join(ROOT, "projects.json")
IMG_EXTS = (".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp")

def titleize(s: str) -> str:
    s = s.replace("-", " ").replace("_", " ").strip()
    return " ".join(w.capitalize() for w in s.split())

def natural_key(s: str):
    # sortowanie naturalne: G1, G2, G10...
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", s)]

items = []

if not os.path.isdir(ROOT):
    raise SystemExit(f"Brak katalogu: {ROOT}")

for name in sorted(os.listdir(ROOT), key=natural_key):
    path = os.path.join(ROOT, name)
    if not os.path.isdir(path):
        continue
    if name.startswith(".") or name == "assets_full" or name == "projects.json":
        continue

    files = sorted([f for f in os.listdir(path) if f.lower().endswith(IMG_EXTS)])
    if not files:
        continue

    cover = files[0]
    items.append({
        "id": name,
        "title": titleize(name),
        "category": "Uncategorized",
        "coverImage": f"{ROOT}/{name}/{cover}"
    })

with open(OUT_PATH, "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=2)

print(f"Wygenerowano {len(items)} wpisów -> {OUT_PATH}")
