#!/usr/bin/env bash
# Creates a generated asset tree for the viewer without manually maintaining
# duplicated map files. Files are hardlinked from the repository roots so the
# viewer can build against regular directories while avoiding redundant storage.
# Run from the repository root (open-utdr-maps/).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VIEWER_DIR="$(dirname "$SCRIPT_DIR")"
REPO_ROOT="$(dirname "$VIEWER_DIR")"
ASSETS_DIR="$VIEWER_DIR/assets"

mkdir -p "$ASSETS_DIR"

rm -rf \
  "$ASSETS_DIR/raw" \
  "$ASSETS_DIR/curated" \
  "$ASSETS_DIR/undertale" \
  "$ASSETS_DIR/deltarune_ch1" \
  "$ASSETS_DIR/deltarune_ch2" \
  "$ASSETS_DIR/deltarune_ch3" \
  "$ASSETS_DIR/deltarune_ch4"

cp -al "$REPO_ROOT/raw" "$ASSETS_DIR/raw"
cp -al "$REPO_ROOT/curated" "$ASSETS_DIR/curated"

mkdir -p "$ASSETS_DIR"
touch "$ASSETS_DIR/manifest.json" "$ASSETS_DIR/manifest.txt"

echo "Prepared viewer assets using hardlinked trees:"
echo "  $ASSETS_DIR/raw <= $REPO_ROOT/raw"
echo "  $ASSETS_DIR/curated <= $REPO_ROOT/curated"
