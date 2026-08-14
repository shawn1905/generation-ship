---
type: 参考
title: 素材库数据结构
description: branch/ 各分类精选 CSV 的字段 schema、标签/分级体系与本地封面路径约定
tags: [reference, data, csv, schema]
openwiki:
  roles: [domain, integration]
  change_kinds: [data-pipeline]
  source_paths: [branch/movies/scifi_movies_curated.csv, branch/games/scifi_games_curated.csv, branch/anime/scifi_anime_curated.csv, branch/novels/scifi_novels_curated.csv, branch/art/sketchfab_curated.csv]
---

# 素材库数据结构

素材库全部精选数据以 CSV 存储于 `branch/` 各分类目录（`*_curated.csv`），配本地缓存封面图。字段按分类略有差异，但共享核心语义：**内容标签（tags）+ 飞船参考分级（ship_ref）+ 策展说明（note）**。

## 公共字段语义

- `tags`：按**内容**打的中文主题标签，多选、`|` 分隔（如 `世代飞船|硬科幻|机甲`），独立于 IMDb/Steam/AniList 自带类型。核心标签：`世代飞船` `方舟` `星际航行` `硬科幻` `太空歌剧` `殖民` `火星` `外星接触` `AI` `赛博朋克` `反乌托邦` `时间循环` `末世` `机甲` `太空恐怖` 等。
- `ship_ref`：飞船设计参考价值分级（整数 0-4）：4=世代飞船直接参考（主线重点）、3=内部结构/工程细节、2=飞船/空间站外形、1=视觉氛围/基地细节、0=设定/主题参考（无飞船设计价值）。
- `note`：策展人说明。**注意：CSV 里不能用英文逗号**（会列错位导致画廊死链），用全角「，」。
- `source_id`：封面文件名 slug（英文小写+下划线），`cover_img` 为原图 URL。

## 各分类 CSV 字段

### 电影 / 剧集（movies/）

```
tconst,title,year,runtime_min,imdb_rating,num_votes,genres,tags,ship_ref,note,imdb_url
```

- 海报路径：`movies/posters/{tconst}.jpg` 与 `movies/tv_posters/{tconst}.jpg`（460px 宽，本地缓存）。

### 游戏（games/）

```
app_id,name,release_year,release_date,review_score_desc,positive,total_reviews,positive_pct,steamspy_owners,price_overview,steam_url,header_img,tags,ship_ref,note,match_source
```

- 封面路径：`games/headers/{app_id}.jpg`（460×215）。评分用 Steam 好评率（`positive_pct`）。

### 动漫 / 漫画（anime/、comics/）

```
title,search_name,year,source,source_id,score,popularity,genres,format,cover_img,url,tags,ship_ref,note,desc,kind
```

- 来源：AniList（`source=anilist`，百分制 `score`）或维基/手写（`source=wikipedia`）。封面本地缓存路径由 `source_id` 或 title 生成 slug：`{分类}/covers/{slug}.jpg`。

### 小说（novels/）

```
title,search_name,author,year,source,source_id,rating,rating_count,cover_img,url,tags,ship_ref,note,desc
```

- 来源：Open Library（`rating` 为 OL ★，`source_id` 形如 `/works/OL...`）。微信读书直达链接见 [`docs/weread-直达链接.md`](../../docs/weread-直达链接.md)（由 `weread_links.py` 生成）。

### 原画/设定集与 3D 社区（art/）

三个 CSV 共用结构（`type` 区分来源）：

```
title,type,artist,year,source,source_id,tags,ship_ref,note,url,cover_img,img_note
```

- `scifi_art_curated.csv`：原画/设定集（`type=原画/设定集`，维基 REST 核验 + Goodreads 封面）
- `sketchfab_curated.csv`：Sketchfab 3D 社区（`type=3D社区`，按♥排序 + ✧4 白名单）
- `blenderartists_curated.csv`：Blender 论坛 3D 社区（`type=3D社区`，Discourse API）
- 封面目录：`art/covers/`（维基人物图 + Goodreads 书封）、`art/covers_3d/`（Sketchfab 渲染图 500px）、`art/covers_forum/`（Blender 论坛渲染图 500px）。

### 其他-AI 精选（other/）

```
title,type,artist,year,tags,ship_ref,note,url,source_id
```

- `type`：动漫/游戏/电影/建筑/小说/原画/科学/音乐/其他；`ship_ref` 一律 0（本分类不用 ✧ 等级）。封面：`other/covers/{source_id}.jpg`。每日扩充流程见 `branch/other/README.md`。

## 原始候选池（不入库）

- `movies/movie_pool.csv`、`movies/tv_pool.csv`（IMDb 全量候选，.gitignore）
- `branch/data/`：IMDb 原始数据集（1.4G，.gitignore，换机器需重新下载）
- `branch/movies/scifi_movies_curated_auto.csv`：自动核验中间产物

## 元数据与画廊的对应

画廊卡片（make_gallery.py）渲染字段：封面图 → title/year → 评分（按分类格式）→ tags → ✧ 分级 → note。评级颜色：✧4 黄、✧3 青、✧2 蓝、✧1/0 灰。人读汇总 `docs/科幻素材库-2000后.md` 由 `make_docs.py` 从同一批 CSV 生成，两者保证一致。

## 另见

- [整理脚本](./scripts.md) - 数据流水线与变更路由
- [交互式画廊](./gallery.md) - 数据的渲染产物
- [素材库概览](./library_overview.md) - 标签体系与分级体系的完整说明
