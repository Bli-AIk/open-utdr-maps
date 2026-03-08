# 地图转换说明

## 转换工具

所有原始地图由 [gm2tiled](https://github.com/<owner>/gm2tiled) 从 GameMaker `data.win` 文件自动转换生成。

## 转换流程

```
data.win
  │
  ├─(UTMT 提取)──→ rooms/*.json + textures/*.png
  │                 backgrounds.json
  │
  └─(gm2tiled 转换)──→ raw/{game}/{room}.tmx
                        raw/{game}/tilesets/{bg}.tsx
                        raw/{game}/tilesets/{bg}.png
```

### 步骤 1：数据提取

使用 [UndertaleModTool (UTMT)](https://github.com/UnderminersTeam/UndertaleModTool) 从 `data.win` 中提取：

- 房间定义（JSON）：瓦片位置、图层信息、对象实例
- 背景定义（JSON）：贴图集属性（尺寸、瓦片大小、GMS2 边框等）
- 贴图页（PNG）：原始纹理图集

### 步骤 2：地图转换

`gm2tiled` 将提取的数据转换为 Tiled 格式：

- 每个 GameMaker 房间 → 一个 `.tmx` 文件
- 每个 GameMaker 背景 → 一个 `.tsx` 贴图集文件 + 对应 `.png`
- GMS1 LegacyTiles → Tiled 瓦片图层（按 depth 分组）
- GMS2 原生图层 → Tiled 瓦片图层（保留原名）
- GameMaker 对象实例 → Tiled 对象图层
- GameMaker 视图 → Tiled 对象图层

## 技术细节

### GMS2 贴图集边框

GMS2 贴图集有 `GMS2OutputBorderX/Y`（通常 2px）环绕每个瓦片。TSX 文件中通过 `margin` 和 `spacing` 属性正确表示。

### 瓦片网格缩放

GMS2 原生图层可能使用与地图网格不同的瓦片尺寸（如 40×40 瓦片在 20×20 网格上）。转换器通过计算有效网格（所有贴图集尺寸的 GCD）来正确映射瓦片位置。

### 瓦片翻转

GMS2 瓦片数据的 28-30 位包含翻转/旋转标志，已正确转换为 Tiled 的翻转标志。

## 验证

转换结果通过视觉回归测试验证：

| 数据集 | 通过率 |
|--------|--------|
| Undertale | 329/335 (98.2%) |
| Deltarune Ch1 | 147/147 (100%) |
| Deltarune Ch2 | 278/278 (100%) |
| Deltarune Ch3 | 246/246 (100%) |
| Deltarune Ch4 | 327/327 (100%) |

## 转换元数据

每个数据集的转换参数记录在 `conversion_info/` 目录下的 TOML 文件中。
