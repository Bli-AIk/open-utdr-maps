#!/usr/bin/env python3
"""Generates assets/manifest.txt listing all .tmx files for WASM discovery."""
import os

ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
OUTPUT = os.path.join(ASSETS_DIR, "manifest.txt")

maps = []
for root, _dirs, files in os.walk(ASSETS_DIR):
    for f in files:
        if f.endswith(".tmx"):
            rel = os.path.relpath(os.path.join(root, f), ASSETS_DIR)
            maps.append(rel)

maps.sort()
with open(OUTPUT, "w") as fh:
    fh.write("\n".join(maps) + "\n")

print(f"Generated {OUTPUT} with {len(maps)} maps")
