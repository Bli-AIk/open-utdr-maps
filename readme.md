# open-utdr-maps

<img src="https://img.shields.io/badge/Deltarune-Undertale-black?style=for-the-badge&labelColor=001225&logo=undertale&logoColor=ff0000" /> <img src="https://img.shields.io/badge/Tiled Map Editor-6699FF?style=for-the-badge" /> <br>
<img src="https://img.shields.io/badge/License (Maps)-CC_BY--NC_4.0-green?style=for-the-badge" />
<img src="https://img.shields.io/badge/License (Code)-GPLv3-blue?style=for-the-badge" />

> **Status**: 🚧 Initial development — maps are imported, community curation is just getting started!

[![](https://dcbadge.limes.pink/api/server/5YXK5DRjPZ)](https://discord.gg/5YXK5DRjPZ)

**open-utdr-maps** is a community-driven open repository of
**[Undertale](https://undertale.com/) / [Deltarune](https://deltarune.com/)** map data
in [Tiled](https://www.mapeditor.org/) format.

| English | Simplified Chinese          |
|---------|-----------------------------|
| English | [简体中文](./readme_zh-hans.md) |

## 🤔 What is this?

Ever wanted to make a fangame or animation/comic, but dreaded the thought of
manually piecing together map assets from scratch?
Or maybe you just wanted to revisit the layout of a favorite room
but didn't know where to start?

**open-utdr-maps** is here to help.

We've converted every room from Undertale and Deltarune (chapters 1–4) into
the **[Tiled](https://www.mapeditor.org/) TMX/TSX format** —
that's **1,333 rooms** in total.
These maps were auto-converted from game data, and while many are structurally accurate,
**some rooms may still contain rendering artifacts, missing object-backed details, or incorrect layering**.
Quality varies — see the verification notes below.

### Why Tiled?

[Tiled](https://www.mapeditor.org/) is a free, open-source map editor used across the game development community.
Its TMX/TSX format has become an industry standard — supported by virtually every game engine and framework:
GameMaker, Unity, Godot, Bevy, Love2D, MonoGame, and many more.

By choosing Tiled as our format, we ensure that **no matter what tool you use to create your fangame**,
these maps are ready to plug in. Whether you're building in GameMaker, Godot, Unity,
or a custom engine — Tiled maps just work.

And even if you're not making a game, Tiled itself is a great way to visually explore and
understand room layouts without writing a single line of code.

## 🌱 A community project — and we need you!

**open-utdr-maps** isn't just a data dump. It's a living, community-driven project with a vision.

### Where we are now

Right now, we have **1,333 rooms** directly converted from game data — but they're still in a raw state.
Many rooms contain leftover debug objects, unnamed layers, and unorganized tile data.
Think of it like having all the puzzle pieces, but still needing to sort and assemble them.

### The roadmap

We're taking a step-by-step approach:

1. **🧹 Clean maps** *(current priority!)* — Turn raw auto-converted data into properly
   organized, accurately displayed maps. Remove debug artifacts, rename layers, fix any
   conversion quirks. This is where we need the most help right now!

2. **🌍 World stitching** — Once individual rooms are clean, connect them into seamless
   area views using Tiled's World feature. Imagine seeing the entire Ruins or Cyber World
   as one connected map.

3. **📐 Data & logic layers** — Add collision boundaries, trigger zones, NPC spawn points,
   and other gameplay metadata. This turns static tile maps into rich, reusable game data.

### Our long-term goals

- **🎮 Empower creators** — Give fangame developers and animators ready-to-use,
  accurate map data so they can focus on what they love: creating.
- **📖 Preserve and document** — Build a comprehensive reference of every room,
  every tile layer, every area layout in UT/DR.
- **🖥️ Browse online** — Eventually, view and explore all maps right in your browser.

### What this means for you

Imagine being able to:
- Open any Undertale room in Tiled and immediately see every tile, every layer
- See the entire Ruins, Snowdin, or Cyber World as a connected world map
- Copy-paste room layouts directly into your fangame project
- Look up where exactly an NPC spawns or where a cutscene triggers

### Getting involved is easy!

Most contributions don't require any programming — just
[Tiled Map Editor](https://www.mapeditor.org/) (free!) and a love for the games.
You can rename layers, clean up rooms, add collision data, stitch worlds together,
or even just fix a typo in the docs.

👉 See [contributing.md](contributing.md) for a step-by-step guide.

## ⚖️ Licensing

This repository uses a dual license:

- **Map files (TMX/TSX/World)** — [CC BY-NC 4.0](LICENSE-CC-BY-NC-4.0)
  - You're free to share, remix, and build upon these maps
  - Attribution: credit this project's URL and "open-utdr-maps contributors"
  - Not for commercial use
  - All contributions are made on behalf of the project, not individuals, unless specifically requested
- **Code and scripts** — [GPLv3](LICENSE-GPLv3)
  - You can use, modify, and distribute the code freely
  - If you distribute modified versions, you must also share the source code under GPLv3

### ⚠️ Texture copyright

The texture images (PNG files) in this repository are the property of
**Toby Fox** and the **Undertale/Deltarune development team**.
They are included solely for map preview and community research.
No copyright infringement is intended. Not for commercial use.
Infringing content will be removed upon request.

## 📊 What's already here

| Game | Rooms | Current regression status |
|------|-------|---------------------------|
| Undertale | 335 | 265 `PASS` / 70 `NO_STATIC_MAP` / 0 `FAIL` |
| Deltarune Ch1 | 147 | 111 `PASS` / 36 `NO_STATIC_MAP` / 0 `FAIL` |
| Deltarune Ch2 | 278 | 204 `PASS` / 74 `NO_STATIC_MAP` / 0 `FAIL` |
| Deltarune Ch3 | 246 | 160 `PASS` / 86 `NO_STATIC_MAP` / 0 `FAIL` |
| Deltarune Ch4 | 327 | 231 `PASS` / 96 `NO_STATIC_MAP` / 0 `FAIL` |

> All **1,333 rooms** have been auto-converted.
> `PASS` means the room's static map content matched an independent reference renderer at pixel level.
> `NO_STATIC_MAP` means the room converted successfully, but its visible result is driven mainly by objects,
> scripts, or runtime drawing rather than a stable static tile map, so it still needs manual review.

## 🚀 Quick Start

### Open maps in Tiled

1. **Clone this repository**:
   ```bash
   git clone https://github.com/Bli-AIk/open-utdr-maps.git
   ```
2. **Install [Tiled Map Editor](https://www.mapeditor.org/)** (free, open-source, cross-platform)
3. **Open any `.tmx` file** from the `raw/` directory — for example:
   ```
   raw/undertale/room_ruins1.tmx
   ```
4. That's it! Referenced assets load automatically from the adjacent `tilesets/`, `textures/`, `sprites/`, and `tile_objects/` folders.

### Browse the directory

```
raw/
├── undertale/
│   ├── room_ruins1.tmx
│   ├── sprites/
│   ├── textures/
│   ├── tile_objects/
│   └── tilesets/
│
└── deltarune/
    ├── deltarune_ch1/
    ├── deltarune_ch2/
    ├── deltarune_ch3/
    └── deltarune_ch4/
```

### Promote raw maps into curated/

This repo also ships a local helper for promoting one room from `raw/` to `curated/` without manually chasing every `.tsx` and `.png` dependency.

Quick examples:

```bash
# Preview what would be removed and copied
just migrate-dry-run dataset=undertale room=room_fire2

# Build a global review folder for all blacklist-matched sprites
just blacklist-audit

# Actually copy one room and its dependencies into curated/
just migrate dataset=deltarune_ch2 room=room_dw_city_big_2
```

Key files:

- `scripts/curation_migrate.py` — promotion helper
- `scripts/curation_blacklist.toml` — blacklist / allowlist config
- `dev/curation_migration_preview/` — per-room local preview output
- `dev/curation_blacklist_audit/` — global blacklist review output

The `dev/` directory is intentionally git-ignored. Use it to review blacklist hits before deciding whether a rule is safe.

## 📂 Repository Structure

```
open-utdr-maps/
├── raw/                    # Auto-converted maps (generated by gm2tiled, do not edit)
├── curated/                # Community-curated versions (cleaned up, annotated)
├── tilesets/               # Standardized tilesets (reserved for future use)
├── docs/
│   ├── conversion_spec_en.md
│   ├── conversion_spec_zh-hans.md
│   ├── copyright_en.md
│   ├── copyright_zh-hans.md
│   ├── layer_spec_en.md
│   └── layer_spec_zh-hans.md
├── conversion_info/        # Conversion metadata (TOML)
├── scripts/                # Automation scripts, including raw -> curated helpers
└── dev/                    # Local review output (ignored by git)
```

## 🔧 Technical Background

### Conversion Tool

All maps in `raw/` are generated by [gm2tiled](https://github.com/Bli-AIk/gm2tiled),
a Rust CLI tool that converts GameMaker `data.win` files to Tiled TMX format.

The conversion handles:
- GMS1 legacy tiles and GMS2 native tile layers
- Non-grid-aligned or mixed-size loose tiles via generated `tile_objects/` assets
- Tileset borders and spacing (GMS2 `OutputBorderX/Y`)
- Room-level tile grid detection
- Tile flip/rotation flags
- Game object instances and camera views

See [docs/conversion_spec_en.md](docs/conversion_spec_en.md) for full details.

### Verification

Every converted room is checked through automated pixel-diff regression using `gm2tiled_regress`.
The tool renders the original static map data and the converted Tiled model with independent renderers,
then compares the results pixel by pixel. Rooms without a meaningful static-map baseline are reported as
`NO_STATIC_MAP` instead of `FAIL` and still require manual review.

## 🌟 Related Projects

| Project | Description |
|---------|-------------|
| [gm2tiled](https://github.com/Bli-AIk/gm2tiled) | GameMaker → Tiled converter (the tool behind this repo) |
| [SoupRune](https://github.com/Bli-AIk/souprune) | A distinctive modern fangame framework — SoupRune is a strong supporter of this project! |
| [Tiled Map Editor](https://www.mapeditor.org/) | The open-source map editor for these files |
| [UndertaleModTool](https://github.com/UnderminersTeam/UndertaleModTool) | GameMaker data extraction tool |

## 💖 Acknowledgments

- **[Toby Fox](https://twitter.com/tobyfox)** and the Undertale/Deltarune team for creating these wonderful games
- **[Thorbjørn Lindeijer](https://www.mapeditor.org/)** and contributors for the Tiled Map Editor
- **[UndertaleModTool](https://github.com/UnderminersTeam/UndertaleModTool)** team for making data extraction possible
- Everyone in the UT/DR community who keeps the determination alive ❤️
