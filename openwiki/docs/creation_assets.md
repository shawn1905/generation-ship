---
type: 概念
title: 原创创作区
description: 自产内容区（docs/creation/）：灵感笔记机制、方舟号 ARK-01 设定、短篇、SVG 草图与 Strudel 音乐实验
tags: [creation, writing, art, music, ar-k01]
timestamp: 2026-08-13
openwiki:
  roles: [domain, workflow]
  change_kinds: [creation]
  source_paths: [docs/creation/README.md, docs/creation/灵感笔记.md, docs/creation/music/README.md]
---

# 原创创作区（Creation）

源目录 [`docs/creation/`](../../docs/creation/)：pi 自主创作的内容——文字直接写，草稿用 SVG/Canvas 代码手绘。与 branch/ 素材库（收集别人的）相对，这里是**自产**的。

## 运转机制

**平时搜集，随手记录，偶尔展开**——pi 在每日 AI 精选扩充/素材维护/生图等过程中，碰到有趣的东西、想创作点什么，先记进[灵感笔记](../../docs/creation/灵感笔记.md)（一条一行也行）；日后某个灵感长大了，再展开成正式作品并回链。让创作从搜集里自然长出来。

## 实现方式

| 形式 | 做法 | 目录 |
|---|---|---|
| 原创文字（设定/短篇/笔记） | 直接写 markdown，入库即在线可读 | `writing/` |
| 草稿/示意图 | 手写 SVG 矢量代码，浏览器直接渲染 | `svg/` |
| 生成艺术 | 单文件 HTML + Canvas/p5.js，GitHub Pages 直接跑 | `gen-art/` |
| AI 成品图 | 火山方舟 Seedream / ChatGPT 生成 | `../未来世界_生图/`（见 [AI 生图集](./future_world_art.md)） |

## 作品索引

| 日期 | 内容 | 文件 |
|---|---|---|
| 2026-08-13 | 📓 创作灵感笔记（随手记机制） | [`docs/creation/灵感笔记.md`](../../docs/creation/灵感笔记.md) |
| 2026-08-13 | 🛸 方舟号 ARK-01 · 环形剖面概念草图（演示作） | [`docs/creation/svg/ark01_ring_draft.svg`](../../docs/creation/svg/ark01_ring_draft.svg) |
| 2026-08-13 | 📖 《12-B 层》· 短篇（船上考古学，首篇成稿） | [`docs/creation/writing/12-B层.md`](../../docs/creation/writing/12-B层.md) |
| 2026-08-13 | 📖 《C 区的曲子》· 短篇（飞船的声音设计，同题） | [`docs/creation/writing/C区的曲子.md`](../../docs/creation/writing/C区的曲子.md) |
| 2026-08-13 | 🎵 Sector C Suite · Strudel 四层曲 | [`docs/creation/music/`](../../docs/creation/music/) |

## 方舟号 ARK-01 世界观

灵感笔记中的核心创作线：给世代飞船起名字、定参数、写编年史，让生图不再是孤立的图。ARK-01 衍生方向：① 编年史短篇（第 1 年/第 50 年/第 137 年三个切片）② 飞船内部分区详图（居住环一层平面图）③ 「船上的一天」生成艺术（昼夜循环动画）。已落地的代表主题：

- **船上考古学**（《12-B 层》）：第 137 年，船员在维修通道深处发现第 1 代船员的涂鸦与遗物——飞船本身就是考古现场。
- **飞船的声音设计**（《C 区的曲子》）：启航时每个舱段有专属环境音乐，137 年设备老化后音高漂移、循环错位，音乐在变异。

## 音乐实验（Strudel）

《C 区的曲子》· Sector C Suite (ARK-01, Year 137) 为 Strudel（strudel.cc）在线作曲的四层结构：

| 层 | 名称 | 含义 | 技术实现 |
|---|---|---|---|
| L1 | Earth Backup | 地球备份·原曲（干净、对齐） | 钢琴和弦 Am-F-C-G，无修饰 |
| L2 | The Decay | 第 137 年的活版本 | `slow(8.03)` 循环微拉长→与备份永不重合缓慢错位；音高慢漂移；偶发丢音 |
| L3 | The Hull | 船体低鸣 | pads 低音垫，慢漂移模拟金属热胀冷缩 |
| L4 | The Pump | 农业环 3 号水泵 | 三角波琶音，偶发失稳像老水泵喘振 |

核心手法是**循环错位**（时间上的「腐烂」）：8 拍主题被拉成 8.03 拍，与备份每 100 循环差 3 拍——100 年后就是完全不同的歌，但每一刻听起来都几乎一样。技术备忘：Strudel 只播放最后一条表达式，多层必须包 `stack(...)`；链接格式为 `https://strudel.cc/#` + base64 编码的完整脚本。

## 另见

- [AI 生图集](./future_world_art.md) - 生图画面与灵感笔记的联动（ARK-01 设定来源）
- [NASA 真实影像素材](./nasa_reference.md) - SP-413 环内景触发「环里的那座湖」灵感
- [素材库概览](../reference/library_overview.md) - 收集（别人的）与创作（自产）的分工
