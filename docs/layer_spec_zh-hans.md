# 图层命名规范

所有整理版地图应遵循以下图层命名标准。原始地图（`raw/`）保留自动生成的图层名称。

## 瓦片图层（Tile Layers）

| 图层名 | 说明 |
|--------|------|
| `ground` | 基础地形瓦片 |
| `decoration` | 装饰性覆盖瓦片 |

如有多个同类图层，使用数字后缀：`ground_1`、`ground_2` 等。

## 对象图层（Object Layers）

| 图层名 | 说明 |
|--------|------|
| `collision` | 碰撞边界 |
| `interaction` | 可交互区域 |
| `npc_spawn` | NPC 出生点 |
| `trigger` | 事件触发器 |
| `event` | 剧情/过场标记 |

## 自动生成图层

以下图层由 `gm2tiled` 自动生成，整理时可保留或重命名：

| 图层名 | 说明 |
|--------|------|
| `views` | 摄像机视图区域 |
| `instances` | GameMaker 游戏对象实例 |
| `Tiles_<depth>` | 按 depth 值命名的瓦片图层（GMS1） |
| 原始图层名 | GMS2 原生图层保留原名 |

## 图层顺序

从上到下（前景到背景）：

1. 对象图层（collision、trigger 等）
2. 前景装饰（decoration）
3. 基础地形（ground）
4. 视图（views）
