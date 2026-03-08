# open-utdr-maps

<img src="https://img.shields.io/badge/Deltarune-Undertale-black?style=for-the-badge&labelColor=001225&logo=undertale&logoColor=ff0000" /> <img src="https://img.shields.io/badge/Tiled Map Editor-6699FF?style=for-the-badge" /> <br>
<img src="https://img.shields.io/badge/许可证 (地图)-CC_BY--NC_4.0-green?style=for-the-badge" />
<img src="https://img.shields.io/badge/许可证 (代码)-GPLv3-blue?style=for-the-badge" />

> **状态**: 🚧 初始开发阶段 — 地图已全部导入，社区整理工作刚刚开始！

[![](https://dcbadge.limes.pink/api/server/5YXK5DRjPZ)](https://discord.gg/5YXK5DRjPZ)

**open-utdr-maps** 是一个社区驱动的
**[Undertale](https://undertale.com/) / [Deltarune](https://deltarune.com/)** 开放地图仓库，
所有地图采用 [Tiled](https://www.mapeditor.org/) 格式。

| 英语                     | 简体中文 |
|------------------------|------|
| [English](./README.md) | 简体中文 |

## 🤔 这是什么？

想做同人游戏或动画，却对从零开始整理地图素材感到头疼？
或者只是想回顾一下原作某个房间的布局，却不知从何下手？

**open-utdr-maps** 就是为你准备的。

我们将 Undertale 和 Deltarune（第 1–4 章）的所有房间都转换成了
**[Tiled](https://www.mapeditor.org/) TMX/TSX 格式** ——
总计 **1,333 个房间**，全部经过精度验证。

### 为什么选择 Tiled？

[Tiled](https://www.mapeditor.org/) 是一个免费、开源的地图编辑器，在游戏开发社区中被广泛使用。
它的 TMX/TSX 格式已经成为行业标准——几乎所有主流游戏引擎和框架都支持：
GameMaker、Unity、Godot、Bevy、Love2D、MonoGame 等等。

选择 Tiled 作为我们的格式，意味着**无论你用什么工具制作同人游戏**，
这些地图都可以直接导入使用。不管你用的是 GameMaker、Godot、Unity
还是自研引擎——Tiled 地图都能无缝衔接。

即使你不是在做游戏，Tiled 本身也是一个很好的可视化工具，
让你不用写一行代码就能探索和理解房间布局。

## 🌱 这是一个社区项目——我们需要你的参与！

**open-utdr-maps** 不仅仅是一堆数据。这是一个有生命的、社区驱动的项目，它有着清晰的愿景。

### 现在的状态

目前，我们有 **1,333 个房间** 直接从游戏数据转换而来——但它们仍处于原始状态。
许多房间包含遗留的调试对象、未命名的图层和未整理的瓦片数据。
就好比我们已经拥有了所有拼图碎片，但还需要把它们分类、拼好。

### 发展路线

我们采取循序渐进的方式：

1. **🧹 清理地图** *（当前重点！）* — 将原始的自动转换数据整理为结构清晰、显示正确的地图。
   移除调试对象、重命名图层、修复转换问题。这是我们目前最需要帮助的地方！

2. **🌍 世界拼接** — 当单个房间清理完成后，利用 Tiled 的 World 功能将它们连接成完整的区域视图。
   想象一下，把整个遗迹或赛博世界看成一张连贯的大地图。

3. **📐 数据与逻辑图层** — 添加碰撞边界、触发区域、NPC 出生点等游戏逻辑元数据。
   将静态的瓦片地图变成丰富的、可复用的游戏数据。

### 长远目标

- **🎮 赋能创作者** — 为同人游戏开发者和动画创作者提供即用的、精确的地图数据，
  让他们专注于自己热爱的事：创作。
- **📖 保存与记录** — 建立 UT/DR 中每一个房间、每一个瓦片图层、每一个区域布局的全面参考。
- **🖥️ 在线浏览** — 最终实现在浏览器中直接查看和探索所有地图。

### 这对你意味着什么

想象一下这样的场景：
- 在 Tiled 中打开任意一个 Undertale 房间，立即看到每一个瓦片、每一个图层
- 把整个遗迹、雪镇或赛博世界看成一张连贯的世界地图
- 直接把房间布局复制粘贴到你的同人游戏项目中
- 查看某个 NPC 到底在哪里出现，或者某个过场动画在哪里触发

### 参与非常简单！

大部分贡献工作不需要编程经验——只需要
[Tiled 地图编辑器](https://www.mapeditor.org/)（免费！）和对游戏的热爱。
你可以重命名图层、清理房间、添加碰撞数据、拼接世界地图，
甚至只是修复文档中的一个错别字。

👉 查看 [contributing.md](contributing.md) 了解详细的参与步骤。

## ⚖️ 许可证

本仓库采用双许可证：

- **地图文件（TMX/TSX/World）** — [CC BY-NC 4.0](LICENSE-CC-BY-NC-4.0)
  - 你可以自由分享、修改和基于这些地图进行创作
  - 署名时需标注本项目地址和"open-utdr-maps 全体贡献者"
  - 不可用于商业用途
  - 所有贡献均默认以项目整体名义进行，而非个人名义，除非贡献者特别要求
- **代码和脚本** — [GPLv3](LICENSE-GPLv3)
  - 你可以自由使用、修改和分发代码
  - 如果你分发修改后的版本，也必须以 GPLv3 许可证开源

### ⚠️ 贴图版权

本仓库中的贴图（PNG 文件）版权归 **Toby Fox** 及 **Undertale/Deltarune 制作团队** 所有。
仅用于地图预览和社区学习研究，无意侵权，不得商用。侵权删除。

## 📊 已有内容

| 游戏 | 房间数 | 像素精度 |
|------|--------|---------|
| Undertale | 335 | ✅ 98.2% |
| Deltarune Ch1 | 147 | ✅ 100% |
| Deltarune Ch2 | 278 | ✅ 100% |
| Deltarune Ch3 | 246 | ✅ 100% |
| Deltarune Ch4 | 327 | ✅ 100% |

> 全部 **1,333 个房间** 均已自动转换，并通过像素级视觉回归测试验证。

## 🚀 快速开始

### 在 Tiled 中打开地图

1. **克隆本仓库**：
   ```bash
   git clone https://github.com/Bli-AIk/open-utdr-maps.git
   ```
2. **安装 [Tiled 地图编辑器](https://www.mapeditor.org/)**（免费、开源、跨平台）
3. **打开 `raw/` 目录下的任意 `.tmx` 文件** — 比如：
   ```
   raw/undertale/room_ruins1.tmx
   ```
4. 完成！贴图会从相邻的 `tilesets/` 文件夹自动加载。

### 目录浏览

```
raw/
├── undertale/          # 全部 335 个 Undertale 房间
│   ├── room_ruins1.tmx
│   ├── room_ruins2.tmx
│   ├── ...
│   └── tilesets/       # 共享贴图集文件（.tsx + .png）
│
└── deltarune/
    ├── ch1/            # 147 个房间 + tilesets/
    ├── ch2/            # 278 个房间 + tilesets/
    ├── ch3/            # 246 个房间 + tilesets/
    └── ch4/            # 327 个房间 + tilesets/
```

## 📂 仓库结构

```
open-utdr-maps/
├── raw/                    # 自动转换的原始地图（由 gm2tiled 生成，请勿手动修改）
├── curated/                # 社区整理版（清理、标注后的版本）
├── tilesets/               # 标准化贴图集（预留）
├── docs/                   # 文档
│   ├── copyright.md        # 版权与法律声明
│   ├── layer_spec.md       # 图层命名规范
│   └── conversion_spec.md  # 地图转换说明
├── conversion_info/        # 转换元数据（TOML）
└── scripts/                # 自动化脚本
```

## 🔧 技术背景

### 转换工具

`raw/` 中的所有地图由 [gm2tiled](https://github.com/Bli-AIk/gm2tiled) 生成，
这是一个 Rust 命令行工具，将 GameMaker `data.win` 文件转换为 Tiled TMX 格式。

转换处理了以下技术细节：
- GMS1 传统瓦片和 GMS2 原生瓦片图层
- 贴图集边框和间距（GMS2 `OutputBorderX/Y`）
- 瓦片图层网格缩放（如 40×40 瓦片在 20×20 地图网格上的处理）
- 瓦片翻转/旋转标志
- 游戏对象实例和摄像机视图

详见 [docs/conversion_spec.md](docs/conversion_spec.md)。

### 验证体系

每个转换后的房间都通过自动化视觉回归测试验证——
将 TMX 输出（由 `tmxrasterizer` 渲染）与从原始瓦片数据独立渲染的参考图进行逐像素对比。

## 🌟 相关项目

| 项目 | 说明 |
|------|------|
| [gm2tiled](https://github.com/Bli-AIk/gm2tiled) | GameMaker → Tiled 转换器（本仓库背后的工具） |
| [SoupRune](https://github.com/Bli-AIk/souprune) | 独树一帜的现代化同人游戏框架 — SoupRune 非常支持这个旁生项目（本项目）！ |
| [Tiled 地图编辑器](https://www.mapeditor.org/) | 用于打开和编辑这些文件的开源地图编辑器 |
| [UndertaleModTool](https://github.com/UnderminersTeam/UndertaleModTool) | GameMaker 数据提取工具 |

## 💖 致谢

- **[Toby Fox](https://twitter.com/tobyfox)** 和 Undertale/Deltarune 制作团队创造了这些精彩的游戏
- **[Thorbjørn Lindeijer](https://www.mapeditor.org/)** 和贡献者们提供了 Tiled 地图编辑器
- **[UndertaleModTool](https://github.com/UnderminersTeam/UndertaleModTool)** 团队让数据提取成为可能
- UT/DR 社区中每一位保持着决心的人 ❤️
