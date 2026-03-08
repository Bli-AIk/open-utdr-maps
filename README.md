# open-utdr-maps

社区驱动的 Undertale / Deltarune 开放地图仓库。

所有地图使用 [Tiled](https://www.mapeditor.org/) TMX/TSX 格式——跨引擎、跨语言的行业标准地图编辑器格式。

## 目标

- 提供标准化、可复用的 UT/DR 地图数据
- 建立社区整理和贡献的工作流
- 支持在线地图浏览器预览

## 数据集

| 游戏 | 房间数 | 状态 |
|------|--------|------|
| Undertale | 335 | ✅ 已导入 |
| Deltarune Ch1 | 147 | ✅ 已导入 |
| Deltarune Ch2 | 278 | ✅ 已导入 |
| Deltarune Ch3 | 246 | ✅ 已导入 |
| Deltarune Ch4 | 327 | ✅ 已导入 |

## 目录结构

```
open-utdr-maps/
├── raw/                    # 自动转换的原始地图（由 gm2tiled 生成）
│   ├── undertale/          # Undertale 全部房间 + tilesets/
│   └── deltarune/          # Deltarune ch1-ch4 + 各章节 tilesets/
├── curated/                # 社区整理版（图层重命名、碰撞标注等）
├── tilesets/               # 标准化贴图集（预留）
├── docs/                   # 文档
├── conversion_info/        # 转换元数据（TOML）
└── scripts/                # 自动化脚本
```

## 快速开始

### 在 Tiled 中打开地图

1. 克隆本仓库：`git clone https://github.com/<owner>/open-utdr-maps.git`
2. 使用 [Tiled 编辑器](https://www.mapeditor.org/) 打开 `raw/` 目录下的任意 `.tmx` 文件
3. 贴图会自动从同目录的 `tilesets/` 加载

### 贡献

请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解贡献流程。

## 转换工具

地图由 [gm2tiled](https://github.com/<owner>/gm2tiled) 从 GameMaker `data.win` 文件自动转换生成。转换细节见 [docs/conversion_spec.md](docs/conversion_spec.md)。

## 许可证

- **Tiled 地图文件（TMX/TSX/World）** — [CC BY-NC 4.0](LICENSE-CC-BY-NC-4.0)
- **代码和脚本** — [GPLv3](LICENSE-GPLv3)
- **原作贴图** — 版权归 Toby Fox 及 Undertale/Deltarune 制作团队所有。详见 [docs/copyright.md](docs/copyright.md)。
