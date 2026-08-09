# 科幻素材库分支收集（2000+ 电影/剧集/游戏）

面向世代飞船设计主线的**支线素材收集**：2000 年以后的科幻电影、剧集、游戏，按内容与评价整理，附带本地图片缓存与交互式画廊。

## 快速上手

1. **交互式画廊**：浏览器打开 `gallery.html`（纯本地文件，三区 Tab：电影 130 / 剧集 49 / 游戏 84，标签过滤 + 搜索 + 飞船参考分级筛选）
2. **人读汇总**：`../docs/科幻素材库-2000后.md`（数据源、标签体系、世代飞船级参考清单、主题速览）
3. **机器数据**：`movies/`、`games/` 下的 CSV（raw 全量 + curated 精选）

## 精选统计

| 类别 | 精选数 | 世代飞船级(✧4) | 工程细节级(✧3) | 外形级(✧2) |
|---|---|---|---|---|
| 电影 | 157 | 5 | 7 | 26 |
| 剧集 | 62 | 4 | 8 | 18 |
| 游戏 | 84 | 1 | 13 | 25 |
| 动漫 | 34 | 1 | 3 | 3 |
| 漫画 | 29 | 1 | 1 | 8 |
| 小说 | 25 | 3 | 4 | 7 |
| **合计** | **391** | **15** | **36** | **87** |

## 目录

```
branch/
├── gallery.html            # 交互式画廊（本地打开，六区：电影/剧集/游戏/动漫/漫画/小说）
├── movies/
│   ├── scifi_movies_raw.csv      # IMDb 数据集过滤：5491 部（Sci-Fi 标签 2000+ 有票）
│   ├── scifi_movies_curated.csv  # 人工精选 131 部（含 tags/ship_ref/note）
│   ├── scifi_tv_raw.csv          # 剧集 1978 部
│   ├── scifi_tv_curated.csv      # 剧集精选 49 部
│   ├── posters/  tv_posters/     # 本地海报缓存（tt开头.jpg）
│   └── movie_pool.csv  tv_pool.csv  # 全量候选池（.gitignore，可重新生成）
├── anime/
│   ├── scifi_anime_curated.csv   # 精选 36 部（AniList 核验：评分/人气/封面）
│   └── covers/                   # 封面缓存
├── comics/
│   ├── scifi_comics_curated.csv  # 精选 29 部（日漫 AniList + 欧美维基）
│   └── covers/
├── novels/
│   ├── scifi_novels_curated.csv  # 精选 25 部（Open Library 核验+评分）
│   └── covers/
├── games/
│   ├── scifi_games_raw.csv       # steam-insights 过滤：1775 款
│   ├── scifi_games_curated.csv   # 精选 84 款
│   └── headers/                  # Steam 封面缓存（appid.jpg）
├── scripts/
│   ├── make_movies.py      # IMDb 数据集 → raw + 候选池
│   ├── make_games.py       # steam-insights → raw
│   ├── curate_movies.py    # 电影人工清单 + 核验合并
│   ├── curate_tv.py        # 剧集人工清单 + 核验合并
│   ├── curate_games.py     # 游戏人工清单 + 核验合并（含非 Steam 特判）
│   ├── curate_anime_comics.py  # 动漫/漫画清单 + AniList/维基核验
│   ├── curate_novels.py        # 小说清单 + Open Library 核验/评分/封面
│   ├── fix_anime_comics.py     # 定向修复（灵笼/铁血孤儿/维基词条）
│   ├── download_images.py  # 海报/封面本地缓存
│   ├── download_covers.py  # 动漫/漫画封面
│   ├── make_gallery.py     # 生成 gallery.html
│   └── make_docs.py        # 生成 ../docs/ 汇总文档
└── .venv/                  # Python 环境（.gitignore）
```

## 复现

```bash
python3 -m venv branch/.venv
branch/.venv/bin/pip install cinemagoer   # 实际海报走 suggestion API，cinemagoer 未使用
# 下载 IMDb 数据集到 branch/data/（见 docs 数据源）
branch/.venv/bin/python scripts/make_movies.py
branch/.venv/bin/python scripts/make_games.py
branch/.venv/bin/python scripts/curate_movies.py   # + curate_tv.py + curate_games.py
branch/.venv/bin/python scripts/download_images.py
branch/.venv/bin/python scripts/make_gallery.py && branch/.venv/bin/python scripts/make_docs.py
```

## 已知发现

- IMDb 类型标签不可靠（Avatar、Blade Runner 2049、Ad Astra 未标 Sci-Fi）→ 人工清单从**全量候选池**匹配
- cinemagoer 2026 版有本地数据库依赖坑 → 海报改用 IMDb suggestion JSON API（免 key）
- 游戏侧 Sci-Fi 标签过宽（混入 Crab Game/BLEACH）→ 精选以人工清单为准
