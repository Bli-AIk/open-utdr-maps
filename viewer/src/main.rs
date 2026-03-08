use tiled_map_web_viewer::{MapCategory, ViewerConfig};

fn main() {
    tiled_map_web_viewer::run(ViewerConfig {
        title: "Open UTDR Maps Viewer".into(),
        resolution: (1280, 720),
        categories: vec![
            MapCategory {
                name: "Undertale".into(),
                directory: "undertale".into(),
            },
            MapCategory {
                name: "Deltarune Ch1".into(),
                directory: "deltarune_ch1".into(),
            },
            MapCategory {
                name: "Deltarune Ch2".into(),
                directory: "deltarune_ch2".into(),
            },
            MapCategory {
                name: "Deltarune Ch3".into(),
                directory: "deltarune_ch3".into(),
            },
            MapCategory {
                name: "Deltarune Ch4".into(),
                directory: "deltarune_ch4".into(),
            },
        ],
        locale_sources: vec![],
    });
}
