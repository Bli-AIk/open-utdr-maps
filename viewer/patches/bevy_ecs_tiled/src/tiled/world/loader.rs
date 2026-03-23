//! Asset loader for Tiled worlds.
//!
//! This module defines the asset loader implementation for importing Tiled worlds into Bevy's asset system.

use crate::{
    prelude::*,
    tiled::{
        cache::TiledResourceCache,
        reader::{preload_external_resources, BytesResourceReader},
    },
};
use bevy::{
    asset::{io::Reader, AssetLoader, AssetPath, LoadContext},
    prelude::*,
};
use std::path::Path;

/// [`TiledWorldAsset`] loading error.
#[derive(Debug, thiserror::Error)]
pub enum TiledWorldLoaderError {
    /// An [`IO`](std::io) Error
    #[error("Could not load Tiled file: {0}")]
    Io(#[from] std::io::Error),
    /// No map was found in this world
    #[error("No map found in this world")]
    EmptyWorld,
    /// Found an infinite map in this world which is not supported
    #[error("Infinite map found in this world (not supported)")]
    WorldWithInfiniteMap,
    /// Could not determine the size of a map referenced by a world
    #[error("Could not determine size for world map '{0}'")]
    MissingWorldMapSize(String),
}

#[derive(TypePath)]
pub(crate) struct TiledWorldLoader {
    cache: TiledResourceCache,
}

impl FromWorld for TiledWorldLoader {
    fn from_world(world: &mut World) -> Self {
        Self {
            cache: world.resource::<TiledResourceCache>().clone(),
        }
    }
}

impl AssetLoader for TiledWorldLoader {
    type Asset = TiledWorldAsset;
    type Settings = ();
    type Error = TiledWorldLoaderError;

    async fn load(
        &self,
        reader: &mut dyn Reader,
        _settings: &Self::Settings,
        load_context: &mut LoadContext<'_>,
    ) -> Result<Self::Asset, Self::Error> {
        let mut bytes = Vec::new();
        reader.read_to_end(&mut bytes).await?;

        debug!("Start loading world '{}'", load_context.path());

        let world_path = load_context.path().path().to_path_buf();
        let cache = preload_external_resources(&bytes, load_context).await;

        let world = {
            let mut loader = tiled::Loader::with_cache_and_reader(
                self.cache.clone(),
                BytesResourceReader::new(&bytes, &cache),
            );
            loader
                .load_world(&world_path)
                .map_err(|e| std::io::Error::other(format!("Could not load Tiled world: {e}")))?
        };

        if world.maps.is_empty() {
            return Err(TiledWorldLoaderError::EmptyWorld);
        }

        let world_dir = world_path.parent().unwrap_or(Path::new(""));
        let mut world_maps = Vec::new();
        let mut world_rect = Rect::new(0.0, 0.0, 0.0, 0.0);
        for map in world.maps.iter() {
            let map_path = world_dir.join(map.filename.clone());
            let (map_width, map_height) =
                world_map_pixel_size(load_context, &map_path, map.width, map.height).await?;
            let map_rect = Rect::new(
                map.x as f32,
                map.y as f32, // Invert for Tiled to Bevy Y axis
                map.x as f32 + map_width,
                map.y as f32 + map_height,
            );

            world_rect = world_rect.union(map_rect);
            world_maps.push((map_rect, map_path));
        }

        // Load all maps
        let mut maps = Vec::new();
        for (map_rect, map_path) in world_maps {
            maps.push((
                Rect::new(
                    map_rect.min.x,
                    world_rect.max.y - map_rect.max.y, // Invert for Tiled to Bevy Y axis
                    map_rect.max.x,
                    world_rect.max.y - map_rect.min.y,
                ),
                load_context.load(AssetPath::from(map_path)),
            ));
        }

        trace!(?maps, "maps");

        let world = TiledWorldAsset {
            world,
            rect: world_rect,
            maps,
        };
        debug!("Loaded world '{}': {:?}", load_context.path(), world);
        Ok(world)
    }

    fn extensions(&self) -> &[&str] {
        static EXTENSIONS: &[&str] = &["world"];
        EXTENSIONS
    }
}

async fn world_map_pixel_size(
    load_context: &mut LoadContext<'_>,
    map_path: &Path,
    embedded_width: Option<i32>,
    embedded_height: Option<i32>,
) -> Result<(f32, f32), TiledWorldLoaderError> {
    if let (Some(width), Some(height)) = (embedded_width, embedded_height) {
        return Ok((width as f32, height as f32));
    }

    let bytes = load_context
        .read_asset_bytes(map_path.to_path_buf())
        .await
        .map_err(|e| std::io::Error::other(format!("Could not read world map: {e}")))?;
    parse_map_pixel_size_from_tmx(map_path, &bytes)
}

fn parse_map_pixel_size_from_tmx(
    map_path: &Path,
    bytes: &[u8],
) -> Result<(f32, f32), TiledWorldLoaderError> {
    let text = std::str::from_utf8(bytes)
        .map_err(|_| TiledWorldLoaderError::MissingWorldMapSize(map_path.display().to_string()))?;
    let Some(tag_start) = text.find("<map") else {
        return Err(TiledWorldLoaderError::MissingWorldMapSize(
            map_path.display().to_string(),
        ));
    };
    let Some(tag_end) = text[tag_start..].find('>') else {
        return Err(TiledWorldLoaderError::MissingWorldMapSize(
            map_path.display().to_string(),
        ));
    };
    let attrs = &text[tag_start..tag_start + tag_end];

    if matches!(xml_attr(attrs, "infinite").as_deref(), Some("1" | "true")) {
        return Err(TiledWorldLoaderError::WorldWithInfiniteMap);
    }

    let width = xml_attr(attrs, "width")
        .and_then(|v| v.parse::<f32>().ok())
        .ok_or_else(|| TiledWorldLoaderError::MissingWorldMapSize(map_path.display().to_string()))?;
    let height = xml_attr(attrs, "height")
        .and_then(|v| v.parse::<f32>().ok())
        .ok_or_else(|| TiledWorldLoaderError::MissingWorldMapSize(map_path.display().to_string()))?;
    let tile_width = xml_attr(attrs, "tilewidth")
        .and_then(|v| v.parse::<f32>().ok())
        .ok_or_else(|| TiledWorldLoaderError::MissingWorldMapSize(map_path.display().to_string()))?;
    let tile_height = xml_attr(attrs, "tileheight")
        .and_then(|v| v.parse::<f32>().ok())
        .ok_or_else(|| TiledWorldLoaderError::MissingWorldMapSize(map_path.display().to_string()))?;

    Ok((width * tile_width, height * tile_height))
}

fn xml_attr(text: &str, name: &str) -> Option<String> {
    let needle = format!("{name}=\"");
    let start = text.find(&needle)? + needle.len();
    let end = start + text[start..].find('"')?;
    Some(text[start..end].to_string())
}

pub(crate) fn plugin(app: &mut App) {
    app.init_asset_loader::<TiledWorldLoader>();
}
