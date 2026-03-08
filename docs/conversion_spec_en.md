# Map Conversion Specification

## Conversion Tool

All raw maps are automatically converted from GameMaker `data.win` files using [gm2tiled](https://github.com/Bli-AIk/gm2tiled).

## Conversion Pipeline

```
data.win
  │
  ├─(UTMT extraction)──→ rooms/*.json + textures/*.png
  │                     backgrounds.json
  │
  └─(gm2tiled)──→ raw/{game}/{room}.tmx
                   raw/{game}/tilesets/{bg}.tsx
                   raw/{game}/tilesets/{bg}.png
```

### Step 1: Data Extraction

Using [UndertaleModTool (UTMT)](https://github.com/UnderminersTeam/UndertaleModTool) to extract from `data.win`:

- Room definitions (JSON): tile positions, layer info, object instances
- Background definitions (JSON): tileset properties (size, tile size, GMS2 borders, etc.)
- Texture pages (PNG): raw texture atlases

### Step 2: Map Conversion

`gm2tiled` converts extracted data to Tiled format:

- Each GameMaker room → one `.tmx` file
- Each GameMaker background → one `.tsx` tileset file + corresponding `.png`
- GMS1 LegacyTiles → Tiled tile layers (grouped by depth)
- GMS2 native layers → Tiled tile layers (keep original names)
- GameMaker object instances → Tiled object layers
- GameMaker views → Tiled object layers

## Technical Details

### GMS2 Tileset Borders

GMS2 tilesets have `GMS2OutputBorderX/Y` (typically 2px) surrounding each tile. The TSX file correctly represents this via `margin` and `spacing` attributes.

### Tile Grid Scaling

GMS2 native layers may use different tile sizes than the map grid (e.g., 40×40 tiles on a 20×20 grid). The converter correctly maps tile positions by calculating the effective grid (GCD of all tileset dimensions).

### Tile Flipping

Bits 28-30 of GMS2 tile data contain flip/rotation flags, correctly converted to Tiled's flip flags.

## Validation

Conversion results are validated via visual regression tests:

| Dataset | Pass Rate |
|---------|-----------|
| Undertale | 329/335 (98.2%) |
| Deltarune Ch1 | 147/147 (100%) |
| Deltarune Ch2 | 278/278 (100%) |
| Deltarune Ch3 | 246/246 (100%) |
| Deltarune Ch4 | 327/327 (100%) |

## Conversion Metadata

Conversion parameters for each dataset are recorded in TOML files under the `conversion_info/` directory.
