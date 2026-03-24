#[cfg(all(not(target_arch = "wasm32"), feature = "viewer-brp"))]
use bevy_brp_extras::BrpExtrasPlugin;
use tiled_map_web_viewer::{MapCategory, MapListView, ViewerConfig};

fn main() {
    let asset_root = if cfg!(target_arch = "wasm32") {
        None
    } else {
        Some(
            std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
                .join("assets")
                .to_string_lossy()
                .into_owned(),
        )
    };
    let manifest_path = if cfg!(target_arch = "wasm32") {
        "assets/manifest.json".into()
    } else {
        std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
            .join("assets/manifest.json")
            .to_string_lossy()
            .into_owned()
    };

    let config = ViewerConfig {
        title: "Open UTDR Maps Viewer".into(),
        resolution: (1280, 720),
        map_lists: vec![
            MapListView {
                id: "map_list".into(),
                title: "Map List".into(),
                default_visible: true,
                section_filter: Some("curated".into()),
            },
            MapListView {
                id: "raw_map_list".into(),
                title: "Raw Map List".into(),
                default_visible: false,
                section_filter: Some("raw".into()),
            },
        ],
        sections: vec![],
        categories: vec![
            MapCategory {
                name: "Worlds".into(),
                key: "worlds".into(),
            },
            MapCategory {
                name: "Undertale".into(),
                key: "undertale".into(),
            },
            MapCategory {
                name: "Deltarune Ch1".into(),
                key: "deltarune_ch1".into(),
            },
            MapCategory {
                name: "Deltarune Ch2".into(),
                key: "deltarune_ch2".into(),
            },
            MapCategory {
                name: "Deltarune Ch3".into(),
                key: "deltarune_ch3".into(),
            },
            MapCategory {
                name: "Deltarune Ch4".into(),
                key: "deltarune_ch4".into(),
            },
        ],
        asset_root,
        manifest_path,
        locale_sources: vec![],
    };

    #[cfg(all(not(target_arch = "wasm32"), feature = "viewer-brp"))]
    {
        tiled_map_web_viewer::run_with_app_hook(config, |app| {
            app.add_plugins(BrpExtrasPlugin::default());
        });
    }

    #[cfg(not(all(not(target_arch = "wasm32"), feature = "viewer-brp")))]
    {
        tiled_map_web_viewer::run(config);
    }
}
