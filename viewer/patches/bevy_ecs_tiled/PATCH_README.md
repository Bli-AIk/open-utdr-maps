# bevy_ecs_tiled WASM Patch

This is a local patch of [bevy_ecs_tiled](https://github.com/adrien-bon/bevy_ecs_tiled) v0.11.2
to fix WASM compatibility.

## Problem

The original `BytesResourceReader::read_from()` uses `futures_lite::future::block_on()` to
synchronously load `.tsx`/`.tx` files within the `tiled::ResourceReader` trait implementation.

On WASM (single-threaded), `block_on` calls `parking::Parker::park()` → `Condvar::wait()`,
which panics with "condvar wait not supported".

**Upstream issue**: https://github.com/adrien-bon/bevy_ecs_tiled/issues/6

## Fix

Instead of using `block_on` at read time, we pre-load all external resources **asynchronously**
before tiled parsing begins:

1. **`reader.rs`**: `BytesResourceReader` now takes a `HashMap<PathBuf, Vec<u8>>` cache instead
   of a `LoadContext`. The `read_from()` method serves files from this cache (no async needed).

2. **`preload_external_resources()`**: New async function that scans XML for `source="*.tsx"`
   and `template="*.tx"` attributes, recursively loads all referenced files via
   `load_context.read_asset_bytes().await`, and returns the populated cache.

3. **`map/loader.rs`** and **`world/loader.rs`**: Call `preload_external_resources()` before
   constructing the `tiled::Loader`.

4. **Removed** `futures-lite` dependency (no longer needed).

## References

- Upstream issue: https://github.com/adrien-bon/bevy_ecs_tiled/issues/6
- Community patch (v0.10.0): https://github.com/j-white/bevy_ecs_tiled (inspiration for approach)
