#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

bash "$SCRIPT_DIR/link_assets.sh"
python3 "$SCRIPT_DIR/generate_manifest.py"
bash "$SCRIPT_DIR/sync_dist_assets.sh"
