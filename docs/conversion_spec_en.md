# Map Conversion Specification

## Conversion Tool

All raw maps are automatically converted from GameMaker `data.win` files using [gm2tiled](https://github.com/Bli-AIk/gm2tiled).

## Conversion Pipeline

```
data.win
  │
  ├─(UTMT extraction)──→ extracted/rooms/*.json + extracted/textures/*.png
  │                     backgrounds.json + sprites.json
  │
  └─(gm2tiled)──→ raw/{game}/{room}.tmx
                   raw/{game}/tilesets/{name}.tsx
                   raw/{game}/textures/{background}.png
                   raw/{game}/sprites/{sprite}.png
                   raw/{game}/tile_objects/{free_tile}.png
```

### Step 1: Data Extraction

Using [UndertaleModTool (UTMT)](https://github.com/UnderminersTeam/UndertaleModTool) to extract from `data.win`:

- Room definitions (JSON): tile positions, layer info, object instances
- Background definitions (JSON): tileset properties (size, tile size, GMS2 borders, etc.)
- Sprite definitions (JSON): default object sprites and frame crop data
- Texture pages (PNG): raw texture atlases

### Step 2: Map Conversion

`gm2tiled` converts extracted data to Tiled format:

- Each GameMaker room → one `.tmx` file
- Each GameMaker background → one `.tsx` tileset file referencing `textures/`
- Object default sprites → TSX/PNG assets in `sprites/`
- Non-grid-aligned or mixed-size loose tiles → generated TSX entries referencing `tile_objects/`
- GMS1 LegacyTiles → Tiled tile layers, plus free-tile object layers when needed
- GMS2 native layers → Tiled tile layers, plus free-tile object layers when needed
- GameMaker object instances → Tiled object layers
- GameMaker views → Tiled object layers

## Technical Details

### GMS2 Tileset Borders

GMS2 tilesets have `GMS2OutputBorderX/Y` (typically 2px) surrounding each tile. The TSX file correctly represents this via `margin` and `spacing` attributes.

### Room Tile Grid Detection

`gm2tiled` detects the effective room grid from GMS2 native tile layers first, then falls back to aligned GMS1 tile sizes. This avoids forcing every room onto a single global grid guess.

### Tile Grid Scaling

GMS2 native layers may use different tile sizes than the map grid (for example 40×40 tiles on a 20×20 or 40×40 room grid). The converter preserves those layouts and emits free-tile object layers when a room mixes incompatible tile sizes.

### Tile Flipping

Bits 28-30 of GMS2 tile data contain mirror/flip/rotation flags, correctly converted to Tiled's flip flags.

## Validation

Conversion results are validated via automated pixel-diff regression using `gm2tiled_regress`.
`PASS` means the room's static map content matched an independent reference renderer at pixel level.
`NO_STATIC_MAP` means the room converted successfully, but it does not currently have a meaningful static-map baseline because the visible result is driven mainly by objects, scripts, or runtime drawing.

| Dataset | PASS | NO_STATIC_MAP | FAIL |
|---------|------|---------------|------|
| Undertale | 265 | 70 | 0 |
| Deltarune Ch1 | 111 | 36 | 0 |
| Deltarune Ch2 | 204 | 74 | 0 |
| Deltarune Ch3 | 160 | 86 | 0 |
| Deltarune Ch4 | 231 | 96 | 0 |

## Conversion Metadata

Conversion parameters for each dataset are recorded in TOML files under the `conversion_info/` directory.
