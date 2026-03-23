use tiled_map_web_viewer::{MapCategory, MapListView, ViewerConfig};

fn main() {
    tiled_map_web_viewer::run(ViewerConfig {
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
        manifest_path: "assets/manifest.json".into(),
        locale_sources: vec![],
    });
}
