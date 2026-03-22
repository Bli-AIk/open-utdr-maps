---
name: Curation Task
about: Propose or claim map curation work
title: '[Curation | <GAME> | 🧹] <area or description>'
labels: curation, help wanted
---

<!--
Please keep issue titles and bodies in English so triage stays consistent.
Use the title prefix for quick scanning in the issue list.
This template applies the base "curation" and "help wanted" labels automatically; maintainers may add more labels after triage.

<GAME>: UNDERTALE, DELTARUNE CH1, DELTARUNE CH2, DELTARUNE CH3, DELTARUNE CH4
<area or description>: e.g., "rm_mausoleum_entrance" or "room_ruins_1"
-->

## Curation Goal

Describe the map area or content to be curated.

## Affected Rooms

List the room names or areas that need curation.

## Scope & Starting Point

- Directory: (curated / raw reference / both)
- Current status: (proposal / claimed / in progress / blocked)
- Starting point: (edit existing curated map / promote from raw / mixed)

## Curation Scope

### 🧹 1. Data Curation
- [ ] Layer renaming (per layer_spec.md)
- [ ] Remove debug objects
- [ ] Fix tile misalignment

### 📐 2. Logic Layers
- [ ] Collision boundary annotation (collision)
- [ ] NPC spawn point annotation (npc_spawn)
- [ ] Event trigger annotation (trigger)
- [ ] Interaction object annotation (interaction)

### 🌍 3. World Stitching
- [ ] Create .world file
- [ ] Connect multiple rooms

### 📝 4. Documentation
- [ ] Area introduction guides
- [ ] Room descriptions
- [ ] Translate documentation
- [ ] Fix typos

### 🔧 5. Tool Improvements
- [ ] gm2tiled converter improvements
- [ ] Automation scripts
- [ ] Web map viewer improvements

### Other
- [ ] Other:

## References

Related game screenshots, wiki links, etc.
