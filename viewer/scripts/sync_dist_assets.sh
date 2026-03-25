#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VIEWER_DIR="$(dirname "$SCRIPT_DIR")"
ASSETS_DIR="$VIEWER_DIR/assets"
DIST_ASSETS_DIR="$VIEWER_DIR/dist/assets"

mkdir -p "$DIST_ASSETS_DIR"

rsync -a --delete "$ASSETS_DIR/" "$DIST_ASSETS_DIR/"

echo "Synced viewer assets into dist/assets:"
echo "  $DIST_ASSETS_DIR <= $ASSETS_DIR"
