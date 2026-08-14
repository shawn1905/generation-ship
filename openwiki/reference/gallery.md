---
type: 参考
title: 交互式图库
description: branch/gallery.html 单文件交互式画廊：八区 Tab、标签过滤、✧ 分级筛选、搜索，本地与 GitHub Pages 双入口
tags: [reference, gallery, frontend]
openwiki:
  roles: [integration, operations]
  change_kinds: [data-pipeline]
  source_paths: [branch/gallery.html, branch/scripts/make_gallery.py]
---

# 交互式图库（gallery.html）

`branch/gallery.html` 是素材库的交互式浏览入口：**单文件 HTML（纯 HTML+CSS+JS，无外部依赖）**，图片走相对路径，`file://` 双击即可打开；推送后 GitHub Pages 自动部署在线版。

- 在线版：https://shawn1905.github.io/generation-ship/branch/gallery.html
- 本地版：浏览器直接打开 `branch/gallery.html`

## 功能

- **八区 Tab**：🎬 电影 157 / 📺 剧集 62 / 🎮 游戏 84 / 🛸 动漫 34 / 📚 漫画 29 / 📖 小说 25 / 🖌 原画·设定集 103 / 🧠 其他-AI精选 39
- **标签过滤**：按条目 `tags`（内容主题标签）过滤
- **✧ 分级筛选**：按 `ship_ref`（0-4）筛选，✧4=世代飞船直接参考（主线重点）
- **搜索**：标题/说明全文搜索
- **卡片**：封面图 → 标题+年份 → 评分（按分类格式：IMDb 评分、Steam 好评率、AniList 百分制、Open Library ★）→ 标签 → ✧ 分级 → note，点击封面跳转原始页面（IMDb/Steam/AniList/维基/Goodreads/Sketchfab/Blender Artists）

## 生成与数据流

- 生成命令：`branch/.venv/bin/python branch/scripts/make_gallery.py`（无外部依赖）
- 数据源：各分类 `*_curated.csv`（见 [数据结构](./data_structure.md)）
- 图片路径约定（相对 gallery.html）：`movies/posters/{tconst}.jpg`、`movies/tv_posters/{tconst}.jpg`、`games/headers/{app_id}.jpg`、`{anime|comics|novels}/covers/{slug}.jpg`、`art/covers*/`、`other/covers/`；缺失时卡片显示「无图」占位
- 分级颜色与文案定义在 `make_gallery.py` 的 `SHIP_LABEL`/`SHIP_COLOR`

## 部署（GitHub Pages）

- push 后约 1-2 分钟自动重建；状态查询：`gh api repos/shawn1905/generation-ship/pages --jq '.status'`
- 画廊与 wiki 的同步关系见 [项目交接与待办](../docs/handover.md) 的「双视图架构」：改 CSV → 跑 `make_gallery.py`（+ 规模级变化再跑 `docs/openwiki_update.sh`）

## 已知注意点

- **图片路径前缀坑**：cards 模板中 img 变量已含前缀（如 `anime/covers/`），不要再硬拼一层，否则封面 404（历史事故）。
- 封面缺失时显示「无图」而非报错，新条目需保证封面已下载（`download_*.py`/`fetch_other_covers.py`）。
- 条目继续增多时可考虑懒加载/分页（当前为一次性渲染全部卡片）。

## 另见

- [素材库概览](./library_overview.md) - 精选标准、标签与分级体系
- [类别摘要](./categories.md) - 各分类的精选数与 ✧4 亮点
- [整理脚本](./scripts.md) - 生成画廊的流水线
- [数据结构](./data_structure.md) - CSV 字段与图片路径
