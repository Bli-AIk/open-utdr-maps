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
These maps were auto-converted from game data, and while many are visually accurate,
**some rooms may contain rendering artifacts, missing layers, or incorrect tile placements**.
Quality varies — see the accuracy notes below.

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

| Game | Rooms | Auto-conversion quality |
|------|-------|------------------------|
| Undertale | 335 | ⚠️ Main rooms render well; some edge cases remain |
| Deltarune Ch1 | 147 | ⚠️ Main rooms render well; quality varies for minor rooms |
| Deltarune Ch2 | 278 | ⚠️ Main rooms render well; quality varies for minor rooms |
| Deltarune Ch3 | 246 | ⚠️ Main rooms render well; quality varies for minor rooms |
| Deltarune Ch4 | 327 | ⚠️ Main rooms render well; quality varies for minor rooms |

> All **1,333 rooms** have been auto-converted. Automated pixel-level tests catch many issues,
> but **some maps may still contain visual inaccuracies** — missing tiles, incorrect layering,
> or conversion artifacts. Contributions to identify and fix these are very welcome!

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
4. That's it! Tilesets load automatically from the adjacent `tilesets/` folder.

### Browse the directory

```
raw/
├── undertale/          # All 335 Undertale rooms
│   ├── room_ruins1.tmx
│   ├── room_ruins2.tmx
│   ├── ...
│   └── tilesets/       # Shared tileset files (.tsx + .png)
│
└── deltarune/
    ├── ch1/            # 147 rooms + tilesets/
    ├── ch2/            # 278 rooms + tilesets/
    ├── ch3/            # 246 rooms + tilesets/
    └── ch4/            # 327 rooms + tilesets/
```

## 📂 Repository Structure

```
open-utdr-maps/
├── raw/                    # Auto-converted maps (generated by gm2tiled, do not edit)
├── curated/                # Community-curated versions (cleaned up, annotated)
├── tilesets/               # Standardized tilesets (reserved for future use)
├── docs/                   # Documentation
│   ├── copyright.md        # Copyright & legal notice
│   ├── layer_spec.md       # Layer naming conventions
│   └── conversion_spec.md  # How maps were converted
├── conversion_info/        # Conversion metadata (TOML)
└── scripts/                # Automation scripts
```

## 🔧 Technical Background

### Conversion Tool

All maps in `raw/` are generated by [gm2tiled](https://github.com/Bli-AIk/gm2tiled),
a Rust CLI tool that converts GameMaker `data.win` files to Tiled TMX format.

The conversion handles:
- GMS1 legacy tiles and GMS2 native tile layers
- Tileset borders and spacing (GMS2 `OutputBorderX/Y`)
- Tile layer grid scaling (e.g., 40×40 tiles on 20×20 map grids)
- Tile flip/rotation flags
- Game object instances and camera views

See [docs/conversion_spec.md](docs/conversion_spec.md) for full details.

### Verification

Every converted room is checked through automated visual regression tests
that compare the TMX output (rendered by `tmxrasterizer`) against an independent
reference rendering of the original tile data. However, **these tests do not catch all issues** —
some rooms may still have visual artifacts that require manual review.

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

