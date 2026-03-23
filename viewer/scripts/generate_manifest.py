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
    if len(parts) >= 3 and parts[0] in {"raw", "curated"} and parts[1] == "worlds":
        if parts[2] == "undertale":
            return "undertale"
        if len(parts) >= 4 and parts[2] == "deltarune":
            return parts[3]
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


def tone_for_badge(label: str, *, kind: str) -> str:
    if kind == "section":
        return "success" if label == "curated" else "muted"
    if kind == "visual_status":
        return {
            "curated": "success",
            "reviewed_clean": "info",
            "seeded": "warning",
            "needs_work": "danger",
            "unreviewed": "muted",
        }.get(label, "accent")
    if kind == "scope":
        return {
            "normal": "info",
            "system": "muted",
            "archival": "warning",
        }.get(label, "muted")
    return "muted"


def build_details(source: str, dataset: str, props: dict[str, str]) -> list[dict[str, str]]:
    details: list[dict[str, str]] = [
        {"label": "Source", "value": source},
        {"label": "Dataset", "value": dataset},
    ]
    if visual := props.get("visual_status"):
        details.append({"label": "Visual Status", "value": visual})
    if logic := props.get("logic_status"):
        details.append({"label": "Logic Status", "value": logic})
    if scope := props.get("scope"):
        details.append({"label": "Scope", "value": scope})
    if notes := props.get("notes"):
        details.append({"label": "Notes", "value": notes})
    return details


def collect_entries() -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    for source_dir in ("raw", "curated"):
        root = REPO_ROOT / source_dir
        if not root.exists():
            continue
        for map_path in sorted(
            path for path in root.rglob("*") if path.suffix in {".tmx", ".world"}
        ):
            rel_path = map_path.relative_to(REPO_ROOT).as_posix()
            dataset = dataset_for_path(Path(rel_path))
            category = "worlds" if map_path.suffix == ".world" else dataset
            props = parse_map_properties(map_path) if map_path.suffix == ".tmx" else {}
            badges = [
                {
                    "label": source_dir,
                    "tone": tone_for_badge(source_dir, kind="section"),
                }
            ]
            if visual := props.get("visual_status"):
                badges.append(
                    {
                        "label": visual,
                        "tone": tone_for_badge(visual, kind="visual_status"),
                    }
                )
            elif source_dir == "curated":
                badges.append({"label": "metadata missing", "tone": "danger"})

            if scope := props.get("scope"):
                badges.append(
                    {
                        "label": scope,
                        "tone": tone_for_badge(scope, kind="scope"),
                    }
                )

            entry = {
                "path": rel_path,
                "title": map_path.stem,
                "section": source_dir,
                "category": category,
                "badges": badges,
                "details": build_details(source_dir, dataset, props),
            }
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
