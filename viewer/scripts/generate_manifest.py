#!/usr/bin/env python3
"""Generate a structured viewer manifest from repository root map directories."""

from __future__ import annotations

import json
from pathlib import Path
import xml.etree.ElementTree as ET


SCRIPT_DIR = Path(__file__).resolve().parent
VIEWER_DIR = SCRIPT_DIR.parent
REPO_ROOT = VIEWER_DIR.parent
ASSETS_DIR = VIEWER_DIR / "assets"
OUTPUT_JSON = ASSETS_DIR / "manifest.json"
OUTPUT_TXT = ASSETS_DIR / "manifest.txt"

PROPERTY_MAP = {
    "open_utdr_visual_status": "visual_status",
    "open_utdr_logic_status": "logic_status",
    "open_utdr_scope": "scope",
    "open_utdr_notes": "notes",
}


def dataset_for_path(path: Path) -> str:
    parts = path.parts
    if len(parts) >= 2 and parts[0] in {"raw", "curated"} and parts[1] == "undertale":
        return "undertale"
    if len(parts) >= 3 and parts[0] in {"raw", "curated"} and parts[1] == "deltarune":
        return parts[2]
    return "other"


def parse_map_properties(tmx_path: Path) -> dict[str, str]:
    try:
        root = ET.parse(tmx_path).getroot()
    except ET.ParseError:
        return {}

    properties: dict[str, str] = {}
    properties_elem = root.find("properties")
    if properties_elem is None:
        return properties

    for prop in properties_elem.findall("property"):
        name = prop.get("name")
        if not name or name not in PROPERTY_MAP:
            continue
        value = prop.get("value")
        if value is None:
            value = (prop.text or "").strip()
        if value:
            properties[PROPERTY_MAP[name]] = value
    return properties


def collect_entries() -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    for source_dir in ("raw", "curated"):
        root = REPO_ROOT / source_dir
        if not root.exists():
            continue
        for tmx_path in sorted(root.rglob("*.tmx")):
            rel_path = tmx_path.relative_to(REPO_ROOT).as_posix()
            entry = {
                "path": rel_path,
                "source": source_dir,
                "dataset": dataset_for_path(Path(rel_path)),
                "room_name": tmx_path.stem,
                "visual_status": None,
                "logic_status": None,
                "scope": None,
                "notes": None,
            }
            entry.update(parse_map_properties(tmx_path))
            entries.append(entry)
    return entries


def main() -> None:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    entries = collect_entries()
    payload = {"maps": entries}

    OUTPUT_JSON.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    OUTPUT_TXT.write_text(
        "\n".join(entry["path"] for entry in entries) + "\n",
        encoding="utf-8",
    )
    print(f"Generated {OUTPUT_JSON} with {len(entries)} maps")


if __name__ == "__main__":
    main()
