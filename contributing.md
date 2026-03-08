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

## 🚀 Step-by-step: Your first contribution

### 0. Open an Issue

Go to [Issues](../../issues) and create a new one. Describe what you'd like to work on
(e.g., "Clean up room_ruins1 layers"). Check that no one else has claimed it yet!

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

When creating or renaming layers, please follow [docs/layer_spec.md](docs/layer_spec.md).

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
- [ ] I followed the [layer naming conventions](docs/layer_spec.md)
- [ ] I included screenshots for visual changes
- [ ] I described my changes in the PR description

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
