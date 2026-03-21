#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import tomllib
import xml.etree.ElementTree as ET
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

try:
    from PIL import Image
except ImportError:  # pragma: no cover - local helper fallback
    Image = None


REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_ROOT = REPO_ROOT / "raw"
CURATED_ROOT = REPO_ROOT / "curated"
DEFAULT_CONFIG = Path(__file__).with_name("curation_blacklist.toml")
DEFAULT_PREVIEW_ROOT = REPO_ROOT / "dev" / "curation_migration_preview"
TILED_GID_MASK = 0x1FFF_FFFF

DATASET_DIRS = {
    "undertale": RAW_ROOT / "undertale",
    "deltarune_ch1": RAW_ROOT / "deltarune" / "deltarune_ch1",
    "deltarune_ch2": RAW_ROOT / "deltarune" / "deltarune_ch2",
    "deltarune_ch3": RAW_ROOT / "deltarune" / "deltarune_ch3",
    "deltarune_ch4": RAW_ROOT / "deltarune" / "deltarune_ch4",
}


@dataclass(frozen=True)
class RoomOverrides:
    keep_layer_names_exact: frozenset[str]
    keep_object_types_exact: frozenset[str]
    keep_object_types_prefix: tuple[str, ...]


@dataclass(frozen=True)
class BlacklistConfig:
    layer_names_exact: frozenset[str]
    object_types_exact: frozenset[str]
    object_types_prefix: tuple[str, ...]
    remove_empty_object_layers: bool
    room_overrides: dict[str, RoomOverrides]


@dataclass(frozen=True)
class TilesetInfo:
    source: str
    source_path: Path
    first_gid: int
    name: str
    tile_width: int
    tile_height: int
    tile_count: int
    columns: int
    margin: int
    spacing: int
    image_source: str | None
    image_path: Path | None


@dataclass
class RemovedEntry:
    layer_name: str
    layer_id: str | None
    object_id: str | None
    object_type: str | None
    gid: int | None
    reason: str
    preview_file: str | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Promote a raw room into curated/, with blacklist cleanup and preview output."
    )
    parser.add_argument("--game", choices=sorted(DATASET_DIRS), help="Dataset namespace to migrate")
    parser.add_argument("--room", help="Room name, with or without .tmx")
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG,
        help="Blacklist config TOML path",
    )
    parser.add_argument(
        "--preview-root",
        type=Path,
        default=DEFAULT_PREVIEW_ROOT,
        help="Directory for removed-sprite review output",
    )
    parser.add_argument("--dry-run", action="store_true", help="Do not write curated files")
    parser.add_argument("--force", action="store_true", help="Overwrite curated files without prompting")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    dataset = args.game or prompt_dataset()
    room_name = normalize_room_name(args.room or prompt_room())
    raw_dir = DATASET_DIRS[dataset]
    raw_room = raw_dir / f"{room_name}.tmx"
    if not raw_room.is_file():
        raise SystemExit(f"Room not found: {raw_room}")

    config = load_blacklist_config(args.config)
    room_key = f"{dataset}:{room_name}"
    preview_dir = args.preview_root / dataset / room_name
    curated_dir = curated_dir_for(dataset)
    curated_room = curated_dir / raw_room.name

    if curated_room.exists() and not args.force:
        if args.dry_run:
            print(f"[dry-run] Curated room already exists and would be overwritten: {curated_room}")
        elif sys.stdin.isatty():
            answer = input(f"Overwrite existing curated room {curated_room}? [y/N] ").strip().lower()
            if answer not in {"y", "yes"}:
                raise SystemExit("Aborted.")
        else:
            raise SystemExit(
                f"Curated room already exists: {curated_room}. Re-run with --force to overwrite."
            )

    tree = ET.parse(raw_room)
    root = tree.getroot()
    tilesets = parse_tilesets(root, raw_dir)
    removed_entries = apply_blacklist(root, config, room_key)
    used_sources = collect_used_tileset_sources(root, tilesets)
    prune_unused_tilesets(root, used_sources)

    preview_dir.mkdir(parents=True, exist_ok=True)
    preview_manifest = write_preview_assets(preview_dir, raw_dir, removed_entries, tilesets)
    write_preview_summary(preview_dir, dataset, room_name, removed_entries, preview_manifest)

    copied_files: list[Path] = []
    if args.dry_run:
        print("[dry-run] Curated files were not written.")
    else:
        copied_files = write_curated_room_and_assets(root, raw_dir, curated_dir, curated_room, used_sources, tilesets)

    print_summary(
        dataset=dataset,
        room_name=room_name,
        raw_room=raw_room,
        curated_room=curated_room,
        preview_dir=preview_dir,
        removed_entries=removed_entries,
        copied_files=copied_files,
        dry_run=args.dry_run,
    )
    return 0


def prompt_dataset() -> str:
    print("Available datasets:")
    for name in sorted(DATASET_DIRS):
        print(f"  - {name}")
    value = input("Game namespace: ").strip()
    if value not in DATASET_DIRS:
        raise SystemExit(f"Unknown dataset: {value}")
    return value


def prompt_room() -> str:
    value = input("Room name: ").strip()
    if not value:
        raise SystemExit("Room name is required.")
    return value


def normalize_room_name(value: str) -> str:
    value = value.strip()
    return value[:-4] if value.endswith(".tmx") else value


def curated_dir_for(dataset: str) -> Path:
    if dataset == "undertale":
        return CURATED_ROOT / "undertale"
    return CURATED_ROOT / "deltarune" / dataset


def load_blacklist_config(path: Path) -> BlacklistConfig:
    with path.open("rb") as fh:
        raw = tomllib.load(fh)

    room_overrides: dict[str, RoomOverrides] = {}
    for room_key, room_cfg in raw.get("rooms", {}).items():
        room_overrides[room_key] = RoomOverrides(
            keep_layer_names_exact=frozenset(room_cfg.get("keep_layer_names_exact", [])),
            keep_object_types_exact=frozenset(room_cfg.get("keep_object_types_exact", [])),
            keep_object_types_prefix=tuple(room_cfg.get("keep_object_types_prefix", [])),
        )

    return BlacklistConfig(
        layer_names_exact=frozenset(raw.get("layer_names", {}).get("exact", [])),
        object_types_exact=frozenset(raw.get("object_types", {}).get("exact", [])),
        object_types_prefix=tuple(raw.get("object_types", {}).get("prefix", [])),
        remove_empty_object_layers=bool(raw.get("cleanup", {}).get("remove_empty_object_layers", True)),
        room_overrides=room_overrides,
    )


def parse_tilesets(root: ET.Element, raw_dir: Path) -> list[TilesetInfo]:
    tilesets: list[TilesetInfo] = []
    for element in root.findall("tileset"):
        source = element.get("source")
        first_gid = int(element.get("firstgid", "0"))
        if not source:
            continue
        source_path = raw_dir / source
        ts_root = ET.parse(source_path).getroot()
        image = ts_root.find("image")
        image_source = image.get("source") if image is not None else None
        image_path = (source_path.parent / image_source).resolve() if image_source else None
        tilesets.append(
            TilesetInfo(
                source=source,
                source_path=source_path,
                first_gid=first_gid,
                name=ts_root.get("name", source_path.stem),
                tile_width=int(ts_root.get("tilewidth", "0")),
                tile_height=int(ts_root.get("tileheight", "0")),
                tile_count=int(ts_root.get("tilecount", "0")),
                columns=int(ts_root.get("columns", "0")),
                margin=int(ts_root.get("margin", "0")),
                spacing=int(ts_root.get("spacing", "0")),
                image_source=image_source,
                image_path=image_path,
            )
        )
    tilesets.sort(key=lambda item: item.first_gid)
    return tilesets


def apply_blacklist(root: ET.Element, config: BlacklistConfig, room_key: str) -> list[RemovedEntry]:
    removed: list[RemovedEntry] = []
    overrides = config.room_overrides.get(
        room_key,
        RoomOverrides(frozenset(), frozenset(), tuple()),
    )

    for layer in list(root.findall("objectgroup")):
        layer_name = layer.get("name", "")
        layer_reason = match_layer_rule(layer_name, config, overrides)
        if layer_reason:
            for obj in layer.findall("object"):
                removed.append(build_removed_entry(layer, obj, layer_reason))
            root.remove(layer)
            continue

        for obj in list(layer.findall("object")):
            obj_type = obj.get("type", "")
            object_reason = match_object_rule(obj_type, config, overrides)
            if object_reason:
                removed.append(build_removed_entry(layer, obj, object_reason))
                layer.remove(obj)

        if config.remove_empty_object_layers and not layer.findall("object"):
            root.remove(layer)

    return removed


def match_layer_rule(layer_name: str, config: BlacklistConfig, overrides: RoomOverrides) -> str | None:
    if layer_name in config.layer_names_exact and layer_name not in overrides.keep_layer_names_exact:
        return f"layer-exact:{layer_name}"
    return None


def match_object_rule(object_type: str, config: BlacklistConfig, overrides: RoomOverrides) -> str | None:
    if not object_type:
        return None
    if object_type in config.object_types_exact and object_type not in overrides.keep_object_types_exact:
        return f"object-exact:{object_type}"
    for prefix in config.object_types_prefix:
        if object_type.startswith(prefix) and prefix not in overrides.keep_object_types_prefix:
            return f"object-prefix:{prefix}"
    return None


def build_removed_entry(layer: ET.Element, obj: ET.Element, reason: str) -> RemovedEntry:
    gid = obj.get("gid")
    return RemovedEntry(
        layer_name=layer.get("name", ""),
        layer_id=layer.get("id"),
        object_id=obj.get("id"),
        object_type=obj.get("type"),
        gid=int(gid) if gid is not None else None,
        reason=reason,
    )


def collect_used_tileset_sources(root: ET.Element, tilesets: list[TilesetInfo]) -> set[str]:
    used_sources: set[str] = set()
    sorted_tilesets = sorted(tilesets, key=lambda item: item.first_gid)

    for layer in root.findall("layer"):
        data = layer.find("data")
        if data is None or data.text is None:
            continue
        for gid in parse_csv_gids(data.text):
            source = resolve_tileset_source(mask_gid(gid), sorted_tilesets)
            if source:
                used_sources.add(source)

    for obj in root.findall(".//objectgroup/object[@gid]"):
        gid = int(obj.get("gid", "0"))
        source = resolve_tileset_source(mask_gid(gid), sorted_tilesets)
        if source:
            used_sources.add(source)

    return used_sources


def prune_unused_tilesets(root: ET.Element, used_sources: set[str]) -> None:
    for element in list(root.findall("tileset")):
        source = element.get("source")
        if source and source not in used_sources:
            root.remove(element)


def parse_csv_gids(csv_text: str) -> Iterable[int]:
    for token in csv_text.replace("\n", "").split(","):
        token = token.strip()
        if token and token != "0":
            yield int(token)


def mask_gid(gid: int) -> int:
    return gid & TILED_GID_MASK


def resolve_tileset_source(gid: int, tilesets: list[TilesetInfo]) -> str | None:
    match: TilesetInfo | None = None
    for tileset in tilesets:
        if gid >= tileset.first_gid:
            match = tileset
        else:
            break
    return match.source if match else None


def resolve_tileset(gid: int, tilesets: list[TilesetInfo]) -> TilesetInfo | None:
    match: TilesetInfo | None = None
    for tileset in tilesets:
        if gid >= tileset.first_gid:
            match = tileset
        else:
            break
    return match


def write_preview_assets(
    preview_dir: Path,
    raw_dir: Path,
    removed_entries: list[RemovedEntry],
    tilesets: list[TilesetInfo],
) -> list[dict[str, object]]:
    removed_sprites_dir = preview_dir / "removed_sprites"
    if removed_sprites_dir.exists():
        shutil.rmtree(removed_sprites_dir)
    removed_sprites_dir.mkdir(parents=True, exist_ok=True)

    manifest: list[dict[str, object]] = []
    for index, entry in enumerate(removed_entries, start=1):
        preview_name = None
        if entry.gid is not None:
            preview_name = maybe_write_preview_sprite(removed_sprites_dir, index, entry, tilesets)
            entry.preview_file = preview_name

        manifest.append(
            {
                "layer_name": entry.layer_name,
                "layer_id": entry.layer_id,
                "object_id": entry.object_id,
                "object_type": entry.object_type,
                "gid": entry.gid,
                "reason": entry.reason,
                "preview_file": preview_name,
            }
        )

    manifest_path = preview_dir / "removed_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    return manifest


def maybe_write_preview_sprite(
    removed_sprites_dir: Path,
    index: int,
    entry: RemovedEntry,
    tilesets: list[TilesetInfo],
) -> str | None:
    if Image is None:
        return None
    gid = mask_gid(entry.gid or 0)
    tileset = resolve_tileset(gid, tilesets)
    if tileset is None or tileset.image_path is None or not tileset.image_path.is_file():
        return None
    if gid < tileset.first_gid:
        return None

    local_id = gid - tileset.first_gid
    if tileset.columns <= 0 or tileset.tile_width <= 0 or tileset.tile_height <= 0:
        return None

    column = local_id % tileset.columns
    row = local_id // tileset.columns
    crop_x = tileset.margin + column * (tileset.tile_width + tileset.spacing)
    crop_y = tileset.margin + row * (tileset.tile_height + tileset.spacing)
    crop_box = (
        crop_x,
        crop_y,
        crop_x + tileset.tile_width,
        crop_y + tileset.tile_height,
    )

    filename = (
        f"{index:03d}_{slugify(entry.object_type or 'layer')}"
        f"__obj{entry.object_id or 'na'}__gid{gid}.png"
    )
    out_path = removed_sprites_dir / filename
    with Image.open(tileset.image_path) as image:
        image.crop(crop_box).save(out_path)
    return filename


def slugify(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9._-]+", "_", value).strip("_") or "item"


def write_preview_summary(
    preview_dir: Path,
    dataset: str,
    room_name: str,
    removed_entries: list[RemovedEntry],
    preview_manifest: list[dict[str, object]],
) -> None:
    by_reason = Counter(entry.reason for entry in removed_entries)
    lines = [
        f"dataset: {dataset}",
        f"room: {room_name}",
        f"removed_total: {len(removed_entries)}",
        f"preview_total: {sum(1 for item in preview_manifest if item['preview_file'])}",
        "",
        "removed_by_rule:",
    ]
    for reason, count in sorted(by_reason.items()):
        lines.append(f"  - {reason}: {count}")
    (preview_dir / "summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_curated_room_and_assets(
    root: ET.Element,
    raw_dir: Path,
    curated_dir: Path,
    curated_room: Path,
    used_sources: set[str],
    tilesets: list[TilesetInfo],
) -> list[Path]:
    copied: list[Path] = []
    curated_dir.mkdir(parents=True, exist_ok=True)
    tree = ET.ElementTree(root)
    indent_xml(root)
    tree.write(curated_room, encoding="utf-8", xml_declaration=True)
    copied.append(curated_room)

    tileset_index = {item.source: item for item in tilesets}
    for source in sorted(used_sources):
        tileset = tileset_index[source]
        destination_tsx = curated_dir / source
        destination_tsx.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(tileset.source_path, destination_tsx)
        copied.append(destination_tsx)

        if tileset.image_source and tileset.image_path is not None:
            destination_image = destination_tsx.parent / tileset.image_source
            destination_image.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(tileset.image_path, destination_image)
            copied.append(destination_image)

    return copied


def indent_xml(elem: ET.Element, level: int = 0) -> None:
    indent = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = indent + "  "
        for child in elem:
            indent_xml(child, level + 1)
        if not child.tail or not child.tail.strip():
            child.tail = indent
    if level and (not elem.tail or not elem.tail.strip()):
        elem.tail = indent


def print_summary(
    *,
    dataset: str,
    room_name: str,
    raw_room: Path,
    curated_room: Path,
    preview_dir: Path,
    removed_entries: list[RemovedEntry],
    copied_files: list[Path],
    dry_run: bool,
) -> None:
    preview_count = sum(1 for entry in removed_entries if entry.preview_file)
    print(f"Dataset: {dataset}")
    print(f"Room: {room_name}")
    print(f"Raw room: {raw_room}")
    if dry_run:
        print(f"Curated room: {curated_room} [dry-run, not written]")
    else:
        print(f"Curated room: {curated_room}")
    print(f"Preview dir: {preview_dir}")
    print(f"Removed blacklist entries: {len(removed_entries)}")
    print(f"Removed sprite previews: {preview_count}")
    if not dry_run:
        print(f"Copied files: {len(copied_files)}")


if __name__ == "__main__":
    raise SystemExit(main())
