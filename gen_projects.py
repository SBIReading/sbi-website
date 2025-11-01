#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Generator assets/projects/projects.json
# Skanuje katalogi w assets/projects/* i tworzy listę obiektów na stronę

import os, json, re

ROOT = "assets/projects"
OUT_PATH = os.path.join(ROOT, "projects.json")
IMG_EXTS = (".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp")

def nice_title(pid: str) -> str:
    """
    G1 -> Garden 1, F3 -> Fence 3, P12 -> Patio 12, B7 -> Bathroom 7
    Inaczej: zamiana - i _ na spacje + kapitalizacja.
    """
    m = re.fullmatch(r"([A-Za-z])(\d+)", pid)
    if m:
        letter, num = m.group(1).upper(), m.group(2)
        prefix = {"G": "Garden", "F": "Fence", "P": "Patio", "B": "Bathroom"}.get(letter, letter)
        return f"{prefix} {num}"
    s = pid.replace("-", " ").replace("_", " ").strip()
    return " ".join(w.capitalize() for w in s.split())

def category_from_prefix(pid: str) -> str:
    letter = pid[:1].upper() if pid else ""
    return {
        "F": "Fencing & gates",
        "P": "Patios & decking",
        "B": "Inside tiling & interior renovations",
        "G": "Garden",
    }.get(letter, "Uncategorized")

def natural_key(s: str):
    # sortowanie naturalne: G1,G2,G10…; dla plików również
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", s)]

items = []

if not os.path.isdir(ROOT):
    raise SystemExit(f"Brak katalogu: {ROOT}")

for name in sorted(os.listdir(ROOT), key=natural_key):
    path = os.path.join(ROOT, name)
    if not os.path.isdir(path):
        continue
    if name.startswith(".") or name in ("assets_full", "projects.json"):
        continue

    # zbierz obrazki w projekcie (pełna galeria)
    imgs = [f for f in os.listdir(path) if f.lower().endswith(IMG_EXTS)]
    imgs.sort(key=natural_key)
    if not imgs:
        continue

    cover = f"{ROOT}/{name}/{imgs[0]}"
    images = [f"{ROOT}/{name}/{f}" for f in imgs]

    items.append({
        "id": name,
        "title": nice_title(name),
        "category": category_from_prefix(name),
        "coverImage": cover,
        "images": images,
        "tags": []
    })

with open(OUT_PATH, "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=2)

print(f"Wygenerowano {len(items)} wpisów -> {OUT_PATH}")
