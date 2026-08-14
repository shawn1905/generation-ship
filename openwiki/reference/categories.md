---
type: 参考
title: 素材库类别摘要
description: 素材库八类内容（电影/剧集/游戏/动漫/漫画/小说/原画设定集/其他-AI精选）的精选数、数据源与世代飞船级（✧4）亮点
tags: [reference, library, categories]
openwiki:
  roles: [domain]
  source_paths: [docs/科幻素材库-2000后.md, branch/README.md]
---

# 素材库类别摘要

素材库按内容分为八类，全部带本地图片、中文标签与 ✧ 分级（0-4）。精选数以当前 `branch/gallery.html` 构建为准；以下 ✧4 亮点为该类别中「世代飞船直接参考」（主线重点）的代表。

## 🎬 电影（157）

- 数据源：IMDb 官方数据集（1980+ 有票），海报走 IMDb suggestion JSON API
- ✧4 亮点：**Interstellar**（环形中继站）、**Passengers**（世代飞船核心参考）、**Pandorum**（内部结构+船员疯癫）、**Voyagers**（社会结构）、**Aniara**（世代飞船社会学，偏离航线的绝望）

## 📺 剧集（62）

- 数据源：IMDb 官方数据集（1980+）
- ✧4 亮点：**The Expanse**（Nauvoo/Behemoth，主线第一参考）、**Battlestar Galactica**（人类流亡舰队）、**Ascension**（60 年代世代飞船计划）、**Nightflyers**（太空恐怖世代飞船）

## 🎮 游戏（84）

- 数据源：steam-insights 快照，Steam 好评率评分，封面走 Steam CDN
- ✧4 亮点：**IXION**（世代飞船城市管理，主线直接参考）

## 🛸 动漫（34）

- 数据源：AniList GraphQL（百分制评分 + 人气），需 UA + 1s 间隔防 403 限流
- ✧4 亮点：**Knights of Sidonia**（希德尼娅号：世代飞船+生态穹顶+重力子炮）

## 📚 漫画（29）

- 数据源：日漫 AniList + 欧美维基 REST
- ✧4 亮点：**Knights of Sidonia**（2009 漫画原作）

## 📖 小说（25）

- 数据源：Open Library 核验/评分/封面；经典可到 1961
- ✧4 亮点：**Aurora**（Kim Stanley Robinson，闭环生态故障与决策困境）、**Ark**（Stephen Baxter）、**Tau Zero**（近光速时间膨胀）
- 微信读书直达链接见 [`docs/weread-直达链接.md`](../../docs/weread-直达链接.md)（5 本未上架：极光、方舟、To Be Taught If Fortunate、计算之星、时间之子）

## 🖌 原画/设定集（103 = 原画 33 + 3D 社区 70）

- 原画/设定集 33：维基 REST 核验艺术家词条 + Goodreads 书封；✧4 亮点：Ralph McQuarrie、Chris Foss、John Berkey、Ian McQue、《The Art of Star Citizen》
- Sketchfab 3D 社区 40：按 ♥ 排序 + ✧4 白名单；✧4 亮点：Venator Prefab、D.S.S. Harbinger、Modular Ring、Icarus Space Station 等
- Blender 论坛 3D 社区 30：Discourse API，23 关键词 + 排除词表 + 人工分级修正；✧4 亮点：Neo-deco space yacht、Skyport Usak、Space colony artwork 等

## 🧠 其他-AI精选（47，独立第 8 区）

- AI 主观选品（不限世代飞船），`ship_ref` 一律 0；每日扩 3-8 条，流程见 `branch/other/README.md`，需跑 `health_check_other.py` 健康巡检。截至 2026-08-14 共三批：8-11 首批 12 条、8-12 两批 15 条、8-14 第三批 8 条。
- 已覆盖维度：巨构/尺度失控、城市形态、人的未来、生态闭环、外星接触、科学前沿、自然生态启发、AI 自身、独立/小众深挖；8-14 第三批按「更深一层」原则扩展：塔比星戴森候选异常、NaissanceE 巨构步行模拟、Kaiba 记忆商品化、与拉玛相会、melodysheep 未来延时、The Line 线性城市、猎户座核脉冲推进、特德·姜《呼吸》

## 分级分布

据交接文档（2026-08-12）与汇总文档：✧4=42、✧3=65、✧2=121（其余为 ✧1/✧0）。确切分布以重新运行 `branch/scripts/make_docs.py` 的生成结果为准。

## 另见

- [素材库概览](./library_overview.md) - 精选标准与标签体系
- [交互式图库](./gallery.md) - 浏览入口
- [整理脚本](./scripts.md) - 数据流水线
