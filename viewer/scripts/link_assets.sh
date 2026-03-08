#!/usr/bin/env bash
# Copies raw map data into viewer/assets/ (dereferencing symlinks).
# Uses rsync for fast incremental updates.
# Run from the repository root (open-utdr-maps/).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VIEWER_DIR="$(dirname "$SCRIPT_DIR")"
REPO_ROOT="$(dirname "$VIEWER_DIR")"
ASSETS_DIR="$VIEWER_DIR/assets"

mkdir -p "$ASSETS_DIR"

# Remove stale symlinks from old approach
for name in undertale deltarune_ch1 deltarune_ch2 deltarune_ch3 deltarune_ch4; do
    [ -L "$ASSETS_DIR/$name" ] && rm "$ASSETS_DIR/$name"
done

DIRS=(
    "undertale:$REPO_ROOT/raw/undertale"
    "deltarune_ch1:$REPO_ROOT/raw/deltarune/deltarune_ch1"
    "deltarune_ch2:$REPO_ROOT/raw/deltarune/deltarune_ch2"
    "deltarune_ch3:$REPO_ROOT/raw/deltarune/deltarune_ch3"
    "deltarune_ch4:$REPO_ROOT/raw/deltarune/deltarune_ch4"
)

for entry in "${DIRS[@]}"; do
    name="${entry%%:*}"
    src="${entry#*:}"
    if [ -d "$src" ]; then
        rsync -a --delete "$src/" "$ASSETS_DIR/$name/"
    else
        echo "WARNING: source not found: $src"
    fi
done

echo "Assets synced to $ASSETS_DIR"

# Ensure manifest.txt exists (trunk watch needs it for ignore path)
touch "$ASSETS_DIR/manifest.txt"
