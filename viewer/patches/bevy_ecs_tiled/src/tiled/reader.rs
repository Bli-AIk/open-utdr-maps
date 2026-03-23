//! Implementation of a custom [tiled::ResourceReader] for asset loading in Bevy.
//!
//! This module provides an implementation of the [`tiled::ResourceReader`] trait,
//! allowing Tiled assets (such as maps and tilesets) to be loaded from Bevy's asset system.
//!
//! For WASM compatibility, external resources (.tsx/.tx) are pre-loaded asynchronously
//! before tiled parsing begins, avoiding the need for `block_on` which panics on WASM.

use bevy::asset::LoadContext;
use std::{
    collections::HashMap,
    io::{Cursor, Error as IoError, ErrorKind, Read},
    path::{Path, PathBuf},
    sync::Arc,
};

/// A [`tiled::ResourceReader`] that serves pre-loaded resources from an in-memory cache.
///
/// External .tsx/.tx files must be pre-loaded via [`preload_external_resources`] before
/// constructing a `tiled::Loader` with this reader.
pub(crate) struct BytesResourceReader<'a> {
    /// The bytes of the main resource (e.g., the Tiled map file).
    bytes: Arc<[u8]>,
    /// Pre-loaded external resources keyed by their path.
    cache: &'a HashMap<PathBuf, Vec<u8>>,
}

impl<'a> BytesResourceReader<'a> {
    /// Creates a new [`BytesResourceReader`] from the given bytes and pre-loaded cache.
    pub(crate) fn new(bytes: &[u8], cache: &'a HashMap<PathBuf, Vec<u8>>) -> Self {
        Self {
            bytes: Arc::from(bytes),
            cache,
        }
    }
}

impl<'a> tiled::ResourceReader for BytesResourceReader<'a> {
    type Resource = Box<dyn Read + 'a>;
    type Error = IoError;

    fn read_from(&mut self, path: &Path) -> std::result::Result<Self::Resource, Self::Error> {
        if let Some(extension) = path.extension() {
            if extension == "tsx" || extension == "tx" {
                // Normalize path to resolve `..` components (e.g. `maps/../tilesets/x.tsx` → `tilesets/x.tsx`)
                // so it matches the keys stored during pre-loading.
                let normalized = normalize_path(path);
                let data = self.cache.get(&normalized).ok_or_else(|| {
                    IoError::new(
                        ErrorKind::NotFound,
                        format!("Resource not pre-loaded: {}", path.display()),
                    )
                })?;
                return Ok(Box::new(Cursor::new(data.clone())));
            }
        }
        Ok(Box::new(Cursor::new(self.bytes.clone())))
    }
}

/// Extracts external resource paths (.tsx/.tx) from XML content by scanning for
/// `source="..."` and `template="..."` attributes.
fn extract_external_paths(xml: &str, base_dir: &Path) -> Vec<PathBuf> {
    let mut paths = Vec::new();
    for attr in ["source", "template"] {
        let pattern = format!("{attr}=\"");
        let mut search_from = 0;
        while let Some(start) = xml[search_from..].find(&pattern) {
            let abs_start = search_from + start + pattern.len();
            if let Some(end) = xml[abs_start..].find('"') {
                let value = &xml[abs_start..abs_start + end];
                if value.ends_with(".tsx") || value.ends_with(".tx") {
                    let resolved = resolve_relative_path(base_dir, Path::new(value));
                    paths.push(resolved);
                }
                search_from = abs_start + end;
            } else {
                break;
            }
        }
    }
    paths
}

/// Normalizes a path by resolving `.` and `..` components in place,
/// e.g. `maps/../tilesets/collision.tsx` → `tilesets/collision.tsx`.
fn normalize_path(path: &Path) -> PathBuf {
    let mut result = PathBuf::new();
    for component in path.components() {
        match component {
            std::path::Component::ParentDir => {
                result.pop();
            }
            std::path::Component::CurDir => {}
            std::path::Component::Normal(s) => {
                result.push(s);
            }
            _ => {
                result.push(component);
            }
        }
    }
    result
}

/// Resolves a potentially relative path against a base directory,
/// normalizing `..` components.
fn resolve_relative_path(base: &Path, relative: &Path) -> PathBuf {
    let mut result = base.to_path_buf();
    for component in relative.components() {
        match component {
            std::path::Component::ParentDir => {
                result.pop();
            }
            std::path::Component::Normal(s) => {
                result.push(s);
            }
            _ => {}
        }
    }
    result
}

/// Pre-loads all external .tsx/.tx resources referenced by the given XML content.
///
/// Recursively scans loaded files for nested references (e.g., a .tsx referencing
/// another .tsx via object templates).
pub(crate) async fn preload_external_resources(
    bytes: &[u8],
    load_context: &mut LoadContext<'_>,
) -> HashMap<PathBuf, Vec<u8>> {
    let mut cache = HashMap::new();
    let base_dir = load_context
        .path()
        .path()
        .parent()
        .unwrap_or(Path::new(""))
        .to_path_buf();

    let xml = String::from_utf8_lossy(bytes);
    let initial_paths = extract_external_paths(&xml, &base_dir);

    let mut queue: Vec<PathBuf> = initial_paths;

    while let Some(path) = queue.pop() {
        if cache.contains_key(&path) {
            continue;
        }
        match load_context.read_asset_bytes(path.clone()).await {
            Ok(data) => {
                // Scan loaded file for nested references
                let nested_xml = String::from_utf8_lossy(&data);
                let nested_dir = path.parent().unwrap_or(Path::new("")).to_path_buf();
                let nested_paths = extract_external_paths(&nested_xml, &nested_dir);
                for np in nested_paths {
                    if !cache.contains_key(&np) {
                        queue.push(np);
                    }
                }
                cache.insert(path, data);
            }
            Err(e) => {
                log::warn!("Failed to pre-load resource {}: {}", path.display(), e);
            }
        }
    }

    cache
}
