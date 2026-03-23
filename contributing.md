# Contributing to open-utdr-maps

First off — **thank you for your interest!** ❤️

Whether you're here to fix a tile, annotate a room, or just browse — you're already part of this community.
This guide will walk you through everything you need to know to contribute.

[![](https://dcbadge.limes.pink/api/server/5YXK5DRjPZ)](https://discord.gg/5YXK5DRjPZ)

**Have questions? Join our Discord!** We're happy to help you get started.

## 📚 Before you start

To contribute, you'll need to be familiar with a few tools. Here are some resources to get started:

### Tiled Map Editor

[Tiled](https://www.mapeditor.org/) is the free, open-source map editor we use for all our map files.

- [Download Tiled](https://www.mapeditor.org/download.html)
- [Tiled Documentation](https://doc.mapeditor.org/en/stable/)
- [Tiled Introduction Video](https://www.youtube.com/watch?v=ZwaomOYGuYo)

### Git & GitHub

We use Git for version control and GitHub for collaboration (Issues, Pull Requests).

- [Git Handbook (GitHub)](https://docs.github.com/en/get-started/using-git/about-git)
- [GitHub Quickstart](https://docs.github.com/en/get-started/quickstart)
- [How to create an Issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/creating-an-issue)
- [How to create a Pull Request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request)

> 💡 Don't worry if you're new to these tools — everyone starts somewhere!
> If you get stuck, ask in our [Discord](https://discord.gg/5YXK5DRjPZ).

## 🌟 No programming required!

Most contributions to this project involve editing map files in
[Tiled Map Editor](https://www.mapeditor.org/) — a free, visual tool.
If you can drag and drop tiles, you can contribute!

## 📋 Types of contributions

Below are some ways you can contribute — **pick whichever interests you!**
These aren't sequential steps; they're independent types of contributions.

Right now, **data curation (#1)** is our top priority and where we need the most help.
If you're not sure where to start, that's the best place! 🧹

### 🧹 1. Data curation (easiest!)

The maps in `raw/` are auto-generated and may have:
- Unnamed or oddly named layers
- Debug objects left behind
- Slight tile misalignment

**What you can do:**
1. Open a map from `raw/` in Tiled
2. Clean it up (rename layers, remove debug objects, etc.)
3. Save your cleaned version to the matching path under `curated/`

> ⚠️ **Never modify files in `raw/`** — those are the original auto-generated maps.
> Always save your work to `curated/`.

### Helper script: raw -> curated promotion

If you do not want to copy dependencies by hand, use the local helper:

```bash
# Preview one room first
just migrate-dry-run dataset=undertale room=room_fire2

# Promote one room into curated/
just migrate dataset=undertale room=room_fire2
```

What it does:

1. Parses the selected `raw/.../<room>.tmx`
2. Collects referenced `.tsx` files
3. Collects referenced `.png` files from those `.tsx`
4. Applies the blacklist from `scripts/curation_blacklist.toml`
5. Writes a review folder under `dev/curation_migration_preview/...`
6. Copies the cleaned room plus dependencies into the matching `curated/` subtree

Before changing blacklist rules, build the global review folder:

```bash
just blacklist-audit
```

That command writes all blacklist-matched sprite previews to `dev/curation_blacklist_audit/`.
Use it to catch false positives before promoting rooms.

### Curated metadata

For files under `curated/`, use different metadata depending on whether the file is a single map (`.tmx`) or a stitched world (`.world`).

If a field is left blank, treat it as "not filled yet".

#### TMX metadata

Use these fields on `curated/**/*.tmx`:

| Field | Meaning | Allowed values / format |
|-------|---------|-------------------------|
| `open_utdr_visual_status` | Visual curation state | blank / `needs_work` / `reviewed_clean` / `pass` |
| `open_utdr_logic_status` | Logic-layer curation state | blank / `needs_work` / `reviewed_clean` / `pass` |
| `open_utdr_scope` | Whether the map is part of the main usable map set or mainly archival | `normal` / `archival` |
| `open_utdr_visual_notes` | Notes about visual cleanup | English text, prefixed with name and date |
| `open_utdr_logic_notes` | Notes about logic-layer work | English text, prefixed with name and date |
| `open_utdr_contributor` | Main contributor identifier for the current curated version | Free-form name / handle / ID |

Status guidance:

- `needs_work`: reviewed and confirmed to still need more work
- `reviewed_clean`: reviewed and currently clean enough to use
- `pass`: curated to the current standard

Scope guidance:

- `normal`: this is part of the main map set. Contributors can use it directly, keep improving it, and use it for future world stitching or logic-layer work.
- `archival`: this map is mainly kept for reference, research, or completeness. Typical examples include menu rooms, initialization rooms, test rooms, placeholder rooms, or other rooms that are not useful as part of the finished public map collection.

#### WORLD metadata

Use these fields on `curated/**/*.world`:

| Field | Meaning | Allowed values / format |
|-------|---------|-------------------------|
| `open_utdr_world_status` | World stitching state | blank / `needs_work` / `pass` |
| `open_utdr_world_notes` | Notes about world stitching | English text, prefixed with name and date |
| `open_utdr_contributor` | Main contributor identifier for the current curated version | Free-form name / handle / ID |

World guidance:

- `needs_work`: the world file exists, but map placement or inclusion still needs work
- `pass`: the world is organized well enough for current use

Use world metadata for the stitched world itself. Do not copy the full TMX visual/logic status model onto `.world` files.

Notes format:

- Use English
- Prefix each note with the contributor name and date
- Example: `[aik | 2026-03-23] bridge trigger objects still need cleanup`
- When a note is replaced, the new note must keep the previous commit hash for traceability
- Example: `[aik | 2026-03-23 | replaces 1a2b3c4] visual pass for community use`

Contributor format:

- You may use a GitHub username, Discord name, or another stable contributor identifier

### 📐 2. Logic layers *(future work)*

> 💡 This is **not a current priority**. You can skip this for now, or wait until the
> community establishes unified standards through discussion.

Add useful metadata to maps by creating object layers:

| Layer name | What to add |
|-----------|-------------|
| `collision` | Draw rectangles/polygons where the player can't walk |
| `trigger` | Mark areas that trigger events (doors, cutscenes, etc.) |
| `npc_spawn` | Place points where NPCs appear |
| `interaction` | Mark objects the player can interact with |

**How:** Open a curated map (or create one from raw), add a new Object Layer,
name it according to the table above, and start drawing!

### 🌍 3. World stitching

Tiled supports `.world` files that connect multiple maps together.
This lets you see an entire area (like the Ruins or Snowdin) as one seamless view.

**How:** In Tiled, go to *World → New World*, then add rooms and position them
relative to each other.

### 📝 4. Documentation

- Write guides explaining what each area looks like
- Add descriptions to rooms
- Translate documentation
- Fix typos!

### 🔧 5. Tool improvements

If you know Rust or scripting:
- Improve the [gm2tiled](https://github.com/Bli-AIk/gm2tiled) converter
- Write automation scripts
- Enhance the web map viewer

## 🔄 Workflow: Issue first, then PR

Our workflow is simple:

1. **Open an Issue first** — Before starting any work, create an Issue describing
   what you plan to do. This ensures no one else is already working on the same task,
   and lets us provide guidance if needed.

2. **Work on your changes** — Fork the repo, create a branch, and make your edits.

3. **Submit a PR when ready** — Link your PR to the Issue. You don't have to finish
   everything at once — partial progress is welcome too!

> 💡 **Not sure how to create a PR?** That's totally fine!
> Just open an Issue describing your work, and we'll help you through the process.
> You can also share your edited files directly in the Issue if that's easier.
> We're here to help — not to gatekeep.

### Issue language, titles, and labels

Please keep Issues in **English**, even if discussion later happens in multiple languages.

Use this title format:

```text
[Type | GAME | EMOJI] Description
```

Examples:

```text
[Curation | UNDERTALE | 🧹] Garbage Dump cleanup
[Bug | DELTARUNE CH2 | 📐] Missing collision rectangles in room_dw_city_big_2
```

Choose the emoji based on the primary work type:

| Emoji | Meaning | Label |
|-------|---------|-------|
| `🧹` | Data curation | `data-curation` |
| `📐` | Logic layers | `logic-layers` |
| `🌍` | World stitching | `world-stitching` |
| `📝` | Documentation | `documentation` |
| `🔧` | Tool improvements | `tooling` |

Issue templates apply the base labels automatically. Maintainers may add or adjust labels after triage.

## 🚀 Step-by-step: Your first contribution

### 0. Open an Issue

Go to [Issues](../../issues) and create a new one. Describe what you'd like to work on
(e.g., `[Curation | UNDERTALE | 🧹] room_ruins1 cleanup`). Check that no one else has claimed it yet!

### 1. Fork and clone

```bash
# Fork this repo on GitHub, then:
git clone https://github.com/YOUR_USERNAME/open-utdr-maps.git
cd open-utdr-maps
```

### 2. Create a branch

```bash
git checkout -b my-contribution
```

### 3. Make your changes

- Open maps in Tiled, make edits, save
- Put curated maps in the right `curated/` subdirectory
- Or start from the helper script above, then continue cleanup in Tiled

### 4. Commit and push

```bash
git add .
git commit -m "curate: clean up room_ruins1 layers"
git push origin my-contribution
```

### 5. Open a Pull Request

Go to the original repo on GitHub and click "New Pull Request".
Fill in the template — describe what you changed and why.

## 📏 Layer naming conventions

When creating or renaming layers, please follow [docs/layer_spec_en.md](docs/layer_spec_en.md).

Quick reference:

| Layer | Type | Description |
|-------|------|-------------|
| `ground` | tile | Base terrain |
| `decoration` | tile | Decorative overlays |
| `collision` | object | Where players can't walk |
| `trigger` | object | Event trigger zones |
| `npc_spawn` | object | NPC spawn points |
| `interaction` | object | Interactable objects |

## ✅ PR checklist

Before submitting, please check:

- [ ] I did **not** modify any files in `raw/`
- [ ] My curated maps are in the correct `curated/` subdirectory
- [ ] My TMX files open correctly in Tiled
- [ ] I followed the [layer naming conventions](docs/layer_spec_en.md)
- [ ] I included screenshots for visual changes
- [ ] I described my changes in the PR description

## 🤖 Automated CI checks

When you open a PR, several automated checks will run. If your PR shows as **Blocked**, don't panic — here's what each check does and how to fix it:

| Check | What it does | How to fix |
|-------|-------------|-----------|
| **Raw files protection** | Blocks PRs that modify files in `raw/`. These are auto-generated and should not be edited. | Move your changes to `curated/` instead. If this is an authorized data update, a maintainer will add the `raw-update` label. |
| **Curated path check** | Verifies that curated maps are in the correct subdirectory (e.g., `curated/undertale/`, `curated/deltarune/deltarune_ch1/`). | Make sure your file paths match the `raw/` directory structure. |
| **TMX/TSX XML validation** | Checks that all `.tmx` and `.tsx` files are valid XML. | Open the file in Tiled and re-save it — Tiled always outputs valid XML. |
| **Layer naming check** | Warns if curated maps use non-standard layer names (per [layer_spec.md](docs/layer_spec_en.md)). | Rename layers to follow the spec, or explain in your PR why a custom name is needed. |
| **File size check** | Blocks files larger than 5MB (10MB for PNGs). | Check if you accidentally committed unnecessary large files. |
| **PR description check** | Warns if your PR description is missing key sections from the template. | Fill in the PR template completely. |

In addition, all PRs require **at least 1 approving review** from a maintainer before merging.

## 📜 Attribution policy

All contributions are made on behalf of the **open-utdr-maps project** as a whole, not under individual names,
unless a contributor specifically requests otherwise.

When using these maps in your work, please credit:
**open-utdr-maps contributors** + a link to this repository.

## 💬 Questions?

- Join our [Discord](https://discord.gg/5YXK5DRjPZ) — the fastest way to get help!
- Open a [GitHub Issue](../../issues) for bugs or feature requests
- Start a [Discussion](../../discussions) for ideas or proposals
- Don't be shy — there are no stupid questions! 😊

**Let's build something amazing together!** 🎔
