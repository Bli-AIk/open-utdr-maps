# open-utdr-maps 贡献指南

首先——**感谢你的关注！** ❤️

无论你是来修复一个瓦片、标注一个房间，还是只是来浏览——你已经是这个社区的一份子了。
这份指南会带你了解参与贡献所需的一切。

[![](https://dcbadge.limes.pink/api/server/5YXK5DRjPZ)](https://discord.gg/5YXK5DRjPZ)

**有问题？加入我们的 Discord！** 我们很乐意帮你入门。

## 📚 开始之前

参与贡献需要了解以下工具。这里是一些入门资源：

### Tiled 地图编辑器

[Tiled](https://www.mapeditor.org/) 是我们使用的免费、开源地图编辑器。

- [下载 Tiled](https://www.mapeditor.org/download.html)
- [Tiled 文档](https://doc.mapeditor.org/en/stable/)
- [Tiled 入门视频](https://www.bilibili.com/video/BV17HAZeREjH)

### Git 和 GitHub

我们使用 Git 进行版本控制，使用 GitHub 进行协作（Issue、Pull Request）。

- [Git 手册（GitHub 官方）](https://docs.github.com/zh/get-started/using-git/about-git)
- [GitHub 快速入门](https://docs.github.com/zh/get-started/quickstart)
- [如何创建 Issue](https://docs.github.com/zh/issues/tracking-your-work-with-issues/creating-an-issue)
- [如何创建 Pull Request](https://docs.github.com/zh/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request)

> 💡 别担心你是新手——每个人都是从零开始的！
> 遇到困难随时来 [Discord](https://discord.gg/5YXK5DRjPZ) 问我们。

## 🌟 不需要编程经验！

本项目的大部分贡献工作都是在
[Tiled 地图编辑器](https://www.mapeditor.org/) 中编辑地图文件——这是一个免费的可视化工具。
如果你能拖放瓦片，你就能做出贡献！

## 📋 贡献类型

下面列出了一些贡献方式——**选择你感兴趣的任意一种即可！**
这些不是需要按顺序完成的步骤，而是各自独立的贡献类型。

目前，**数据整理（第 1 种）** 是我们最优先的工作，也是最需要帮助的地方。
如果你不知道从哪里开始，那就从这里开始吧！🧹

### 🧹 1. 数据整理（最简单！）

`raw/` 中的地图是自动生成的，可能存在：
- 未命名或命名奇怪的图层
- 遗留的调试对象
- 轻微的瓦片错位

**你可以这样做：**
1. 在 Tiled 中打开 `raw/` 下的地图
2. 清理它（重命名图层、移除调试对象等）
3. 将清理后的版本保存到 `curated/` 的对应路径下

> ⚠️ **永远不要修改 `raw/` 中的文件** — 那些是原始的自动生成地图。
> 请将你的工作成果保存到 `curated/`。

### 📐 2. 逻辑图层 *（未来工作）*

> 💡 这**不是当前的工作重点**。你可以暂时跳过，或等待社区通过讨论建立统一规范后再参与。

通过创建对象图层，为地图添加有用的元数据：

| 图层名 | 添加内容 |
|--------|---------|
| `collision` | 画出玩家不能行走的矩形/多边形区域 |
| `trigger` | 标记触发事件的区域（门、过场动画等） |
| `npc_spawn` | 放置 NPC 出现的位置点 |
| `interaction` | 标记玩家可以互动的物体 |

**操作方法：** 打开一个整理版地图（或从原始地图创建一个），添加新的对象图层，
按上表命名，然后开始绘制！

### 🌍 3. 世界拼接

Tiled 支持 `.world` 文件，可以将多个地图连接在一起。
这样你就可以把整个区域（比如废墟或雪镇）看成一个完整的视图。

**操作方法：** 在 Tiled 中，点击 *世界 → 新建世界*，然后添加房间并设置它们之间的相对位置。

### 📝 4. 文档完善

- 编写各区域的介绍指南
- 为房间添加描述
- 翻译文档
- 修复错别字！

### 🔧 5. 工具改进

如果你懂 Rust 或脚本编程：
- 改进 [gm2tiled](https://github.com/Bli-AIk/gm2tiled) 转换器
- 编写自动化脚本
- 增强在线地图浏览器

## 🔄 工作流程：先提 Issue，再提 PR

我们的工作流程很简单：

1. **先提 Issue** — 在开始任何工作之前，先创建一个 Issue 描述你打算做什么。
   这样可以确保没有其他人在做相同的事情，也方便我们提供指导。

2. **进行修改** — Fork 仓库、创建分支、编辑地图。

3. **准备好后提交 PR** — 把 PR 关联到你的 Issue。不需要一次做完——
   有阶段性进展时随时都可以提交！

> 💡 **不知道怎么提 PR？** 完全没关系！
> 只需要提一个 Issue 描述你的工作内容，我们会帮你完成后续流程。
> 你也可以直接在 Issue 中分享修改后的文件，这样也行。
> 我们在这里是为了帮助你，而不是设置门槛。

## 🚀 手把手教程：你的第一次贡献

### 0. 提 Issue

前往 [Issues](../../issues) 创建一个新的 Issue。描述你想做的事情
（比如"清理 room_ruins1 的图层"）。先检查一下有没有人已经在做了！

### 1. Fork 并克隆

```bash
# 先在 GitHub 上 Fork 这个仓库，然后：
git clone https://github.com/你的用户名/open-utdr-maps.git
cd open-utdr-maps
```

### 2. 创建分支

```bash
git checkout -b my-contribution
```

### 3. 进行修改

- 在 Tiled 中打开地图，编辑，保存
- 将整理后的地图放到正确的 `curated/` 子目录

### 4. 提交并推送

```bash
git add .
git commit -m "curate: 清理 room_ruins1 图层"
git push origin my-contribution
```

### 5. 发起 Pull Request

到 GitHub 上的原始仓库，点击 "New Pull Request"。
填写模板——描述你做了什么改动以及原因。

## 📏 图层命名规范

创建或重命名图层时，请遵循 [docs/layer_spec.md](docs/layer_spec.md)。

快速参考：

| 图层名 | 类型 | 说明 |
|--------|------|------|
| `ground` | tile | 基础地形 |
| `decoration` | tile | 装饰覆盖物 |
| `collision` | object | 玩家不能行走的区域 |
| `trigger` | object | 事件触发区域 |
| `npc_spawn` | object | NPC 出生点 |
| `interaction` | object | 可互动的物体 |

## ✅ PR 检查清单

提交前请确认：

- [ ] 我**没有**修改 `raw/` 中的任何文件
- [ ] 我的整理版地图在正确的 `curated/` 子目录中
- [ ] 我的 TMX 文件在 Tiled 中可以正常打开
- [ ] 我遵循了 [图层命名规范](docs/layer_spec.md)
- [ ] 视觉变更已附截图
- [ ] 我在 PR 描述中说明了修改内容

## 📜 署名政策

所有贡献均默认以 **open-utdr-maps 项目整体** 名义进行，而非个人名义，
除非贡献者特别要求。

使用这些地图时，请标注：
**open-utdr-maps 全体贡献者** + 本仓库链接。

## 💬 有问题？

- 加入 [Discord](https://discord.gg/5YXK5DRjPZ) — 最快的获取帮助方式！
- 在 [GitHub Issues](../../issues) 报告 Bug 或提出功能需求
- 在 [Discussions](../../discussions) 提问或分享想法
- 不要害羞——没有愚蠢的问题！😊

**让我们一起创造精彩的东西吧！** 🎔
