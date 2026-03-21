# 地图转换说明

## 转换工具

所有原始地图由 [gm2tiled](https://github.com/Bli-AIk/gm2tiled) 从 GameMaker `data.win` 文件自动转换生成。

## 转换流程

```
data.win
  │
  ├─(UTMT 提取)──→ extracted/rooms/*.json + extracted/textures/*.png
  │                 backgrounds.json + sprites.json
  │
  └─(gm2tiled 转换)──→ raw/{game}/{room}.tmx
                        raw/{game}/tilesets/{name}.tsx
                        raw/{game}/textures/{background}.png
                        raw/{game}/sprites/{sprite}.png
                        raw/{game}/tile_objects/{free_tile}.png
```

### 步骤 1：数据提取

使用 [UndertaleModTool (UTMT)](https://github.com/UnderminersTeam/UndertaleModTool) 从 `data.win` 中提取：

- 房间定义（JSON）：瓦片位置、图层信息、对象实例
- 背景定义（JSON）：贴图集属性（尺寸、瓦片大小、GMS2 边框等）
- Sprite 定义（JSON）：对象默认 sprite 和帧裁切数据
- 贴图页（PNG）：原始纹理图集

### 步骤 2：地图转换

`gm2tiled` 将提取的数据转换为 Tiled 格式：

- 每个 GameMaker 房间 → 一个 `.tmx` 文件
- 每个 GameMaker 背景 → 一个引用 `textures/` 的 `.tsx` 贴图集文件
- 对象默认 sprite → 输出到 `sprites/` 的 TSX/PNG 资源
- 非网格对齐或混合尺寸的零散瓦片 → 输出为引用 `tile_objects/` 的 TSX 资源
- GMS1 LegacyTiles → Tiled 瓦片图层；必要时补充 free-tile 对象图层
- GMS2 原生图层 → Tiled 瓦片图层；必要时补充 free-tile 对象图层
- GameMaker 对象实例 → Tiled 对象图层
- GameMaker 视图 → Tiled 对象图层

## 技术细节

### GMS2 贴图集边框

GMS2 贴图集有 `GMS2OutputBorderX/Y`（通常 2px）环绕每个瓦片。TSX 文件中通过 `margin` 和 `spacing` 属性正确表示。

### 房间 Tile Grid 检测

`gm2tiled` 会优先根据 GMS2 原生瓦片图层推断房间使用的有效网格，再回退到对齐良好的 GMS1 瓦片尺寸，避免用单一的全局默认值去硬套所有房间。

### 瓦片网格缩放

GMS2 原生图层可能使用与地图网格不同的瓦片尺寸（例如 40×40 瓦片运行在 20×20 或 40×40 的房间网格上）。转换器会保留这些布局；当一个房间混用了不兼容的尺寸时，会补充 free-tile 对象图层而不是强行压扁。

### 瓦片翻转

GMS2 瓦片数据的 28-30 位包含镜像/翻转/旋转标志，已正确转换为 Tiled 的翻转标志。

## 验证

转换结果通过 `gm2tiled_regress` 的自动化逐像素回归进行验证。
`PASS` 表示房间中的静态地图内容已经与独立参考渲染器逐像素匹配。
`NO_STATIC_MAP` 表示房间虽然转换成功，但它当前没有适合做静态地图逐像素阻塞判定的稳定基线，因为其可见结果主要依赖对象、脚本或运行时绘制。

| 数据集 | PASS | NO_STATIC_MAP | FAIL |
|--------|------|---------------|------|
| Undertale | 265 | 70 | 0 |
| Deltarune Ch1 | 111 | 36 | 0 |
| Deltarune Ch2 | 204 | 74 | 0 |
| Deltarune Ch3 | 160 | 86 | 0 |
| Deltarune Ch4 | 231 | 96 | 0 |

## 转换元数据

每个数据集的转换参数记录在 `conversion_info/` 目录下的 TOML 文件中。
