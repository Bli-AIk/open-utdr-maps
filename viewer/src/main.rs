use tiled_map_web_viewer::{MapCategory, MapSection, ViewerConfig};

fn main() {
    tiled_map_web_viewer::run(ViewerConfig {
        title: "Open UTDR Maps Viewer".into(),
        resolution: (1280, 720),
        sections: vec![
            MapSection {
                name: "Curated Map List".into(),
                key: "curated".into(),
                default_visible: true,
            },
            MapSection {
                name: "Raw Map List".into(),
                key: "raw".into(),
                default_visible: false,
            },
        ],
        categories: vec![
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
        manifest_path: "assets/manifest.json".into(),
        locale_sources: vec![],
    });
}
