# Justfile for open-utdr-maps viewer
# Run from repository root (open-utdr-maps/)

# Prerequisites:
#   cargo install trunk
#   rustup target add wasm32-unknown-unknown

default: serve

# Create asset symlinks (run once after clone)
setup:
    bash viewer/scripts/link_assets.sh

# Serve WASM version locally (http://127.0.0.1:8080)
serve: setup
    cd viewer && trunk serve

# Build WASM version (release, output in viewer/dist/)
build-wasm: setup
    cd viewer && trunk build --release

# Run desktop version
run: setup
    cd viewer && cargo run

# Check compilation (native + WASM)
check:
    cd viewer && cargo check
    cd viewer && cargo check --target wasm32-unknown-unknown

# Run clippy lints
lint:
    cd viewer && cargo clippy --all-targets -- -D warnings

# Format code
fmt:
    cd viewer && cargo fmt

# Check formatting (CI-style)
fmt-check:
    cd viewer && cargo fmt -- --check

# Run all CI checks locally
ci: fmt-check lint check

# Clean build artifacts
clean:
    cd viewer && cargo clean
    rm -rf viewer/dist

# Dry-run a raw -> curated room promotion and generate blacklist previews in dev/
migrate-dry-run dataset="undertale" room="room_fire2":
    python3 scripts/curation_migrate.py --game {{dataset}} --room {{room}} --dry-run

# Build a global preview catalog for all blacklist-matched sprites
blacklist-audit:
    python3 scripts/curation_migrate.py --audit-blacklist

# Promote a raw room into curated/ using the blacklist config
migrate dataset="undertale" room="room_fire2":
    python3 scripts/curation_migrate.py --game {{dataset}} --room {{room}}
