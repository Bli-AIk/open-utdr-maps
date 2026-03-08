#!/usr/bin/env bash
# Creates symlinks from viewer/assets/ to the raw map data.
# Run from the repository root (open-utdr-maps/).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VIEWER_DIR="$(dirname "$SCRIPT_DIR")"
REPO_ROOT="$(dirname "$VIEWER_DIR")"
ASSETS_DIR="$VIEWER_DIR/assets"

mkdir -p "$ASSETS_DIR"

ln -sfn "$REPO_ROOT/raw/undertale"              "$ASSETS_DIR/undertale"
ln -sfn "$REPO_ROOT/raw/deltarune/deltarune_ch1" "$ASSETS_DIR/deltarune_ch1"
ln -sfn "$REPO_ROOT/raw/deltarune/deltarune_ch2" "$ASSETS_DIR/deltarune_ch2"
ln -sfn "$REPO_ROOT/raw/deltarune/deltarune_ch3" "$ASSETS_DIR/deltarune_ch3"
ln -sfn "$REPO_ROOT/raw/deltarune/deltarune_ch4" "$ASSETS_DIR/deltarune_ch4"

echo "Asset symlinks created in $ASSETS_DIR"
