# 交接文档 · 世代飞船设计项目（含科幻素材库分支）

> 最后更新：2026-08-12 ｜ 交接人：AI 助手 ｜ 仓库：`shawn1905/generation-ship`（公开）
> 本文档面向后续接手者：说明项目目标、现状、复现方法、踩坑记录与待办事项。

---

## 1. 项目概览

**主项目**：世代飞船（Generation Ship）设计 —— 三条原则：**严谨科技幻想 / 引用开源 / 200 年尺度**。

**分支收集产出（本仓库主要内容）**：2000+ 科幻作品素材库（后放宽：电影/剧集至 1980+），按**内容与评价**驱动收集，服务于世代飞船设计主线。六类素材共 **391 部**，全部带图片、中文标签、✧ 分级，并配有**交互式画廊**（单文件 HTML，可本地打开 + GitHub Pages 在线）。

### 在线入口（公网）

| 入口 | 地址 |
|---|---|
| 交互式画廊 | https://shawn1905.github.io/generation-ship/branch/gallery.html |
| GitHub 仓库 | https://github.com/shawn1905/generation-ship |
| 汇总文档 | https://github.com/shawn1905/generation-ship/blob/main/docs/科幻素材库-2000后.md |
| 微信读书直达 | https://github.com/shawn1905/generation-ship/blob/main/docs/weread-直达链接.md |

### 素材库规模

| 类别 | 精选数 | 范围 | 数据源 |
|---|---|---|---|
| 🎬 电影 | 157 | 1980+ | IMDb 官方数据集 |
| 📺 剧集 | 62 | 1980+ | IMDb 官方数据集 |
| 🎮 游戏 | 84 | 不限 | steam-insights 快照 |
| 🎌 动漫 | 34 | 边界可到 1988 | AniList GraphQL |
| 📚 漫画 | 29 | 日漫+欧美 | AniList + 维基百科 |
| 📖 小说 | 25 | 经典可到 1961 | Open Library |
| 🖌 原画/设定集 | 103 | 原画 33 + 3D社区 70 | 维基 REST + Goodreads + ArtStation + Sketchfab + Blender 论坛 |
| 🧠 其他-AI精选 | 31 | 未来灵感（AI 主观选品，不限世代飞船，每日可扩） | 维基 REST + Steam CDN + 官网 og:image |

**✧ 分级**：0=无/弱、1=视觉氛围、2=飞船/空间站外形、3=内部结构/工程细节、4=世代飞船直接参考（主线重点）。分布：✧4=42、✧3=65、✧2=121。

---

## 2. 目录结构（branch/）

```
branch/
├── gallery.html            # 交互式画廊（单文件 431KB，六区 Tab + 标签过滤 + ✧筛选 + 搜索）
├── README.md               # 素材库说明 + 统计
├── movies/
│   ├── scifi_movies_raw.csv     # IMDb 过滤：1980+ Sci-Fi 有票（约 9076 部）
│   ├── scifi_movies_curated.csv # 人工精选 157 部（tags/ship_ref/note 列）
│   ├── scifi_tv_raw.csv         # 剧集 4462 部
│   ├── scifi_tv_curated.csv     # 剧集精选 62 部
│   ├── posters/  tv_posters/    # 海报本地缓存（{tconst}.jpg，460px 宽）
│   └── movie_pool.csv  tv_pool.csv  # 全量候选池（.gitignore，不入库，可重新生成）
├── games/
│   ├── scifi_games_raw.csv      # steam-insights 过滤 1775 款
│   ├── scifi_games_curated.csv  # 精选 84 款
│   └── headers/                 # Steam 封面（{appid}.jpg，460×215）
├── anime/  comics/  novels/
│   ├── *_curated.csv            # 精选数据（AniList/维基/Open Library 核验）
│   └── covers/                  # 封面缓存
├── art/
│   ├── scifi_art_curated.csv    # 原画/设定集精选 33 条（type: 原画/设定集）
│   ├── sketchfab_curated.csv    # 3D 社区 40 条（Sketchfab，按♥排序 + ✧4 白名单）
│   ├── blenderartists_curated.csv # 3D 社区 30 条（Blender 论坛 Discourse API）
│   ├── covers/                  # 维基人物图 + Goodreads 书封
│   ├── covers_3d/               # Sketchfab 渲染图（500px）
│   └── covers_forum/            # Blender 论坛渲染图（500px）
├── other/
│   ├── ai_curated.csv           # 🧠 其他-AI精选 24 条（AI 主观选品，科学/自然/工程/哲学/冷门科幻等）
│   ├── covers/                  # 封面本地缓存（维基/Steam/Goodreads/官网）
│   └── README.md                # 每日扩充流程（怎么加）
├── scripts/                     # 完整流水线（见 §3）
├── data/                        # IMDb 原始数据（.gitignore，1.4G 不入库）
└── .venv/                       # Python 3.14（.gitignore）
```

---

## 3. 数据流水线（可复现）

```bash
cd branch
.venv/bin/python scripts/make_movies.py   # IMDb 数据集 → raw + 候选池（1980+）
.venv/bin/python scripts/make_games.py    # steam-insights → raw
.venv/bin/python scripts/curate_movies.py # 人工清单 + 核验合并（含 None 剔除标记）
.venv/bin/python scripts/curate_tv.py     # 同上（剧集）
.venv/bin/python scripts/curate_games.py  # 同上（游戏，含 SPECIAL_APPID/NON_STEAM 特判）
.venv/bin/python scripts/curate_anime_comics.py  # 动漫/漫画（AniList + 维基）
.venv/bin/python scripts/fix_anime_comics.py     # 定向修复（灵笼/铁血孤儿/维基词条）
.venv/bin/python scripts/curate_novels.py        # 小说（Open Library 核验/评分/封面）
.venv/bin/python scripts/curate_art.py           # 原画/设定集（维基 REST 核验 + Goodreads 封面）
.venv/bin/python scripts/collect_sketchfab.py    # 3D 社区（Sketchfab API 按♥排序 + 分级配额 + ✧4 白名单）
.venv/bin/python scripts/collect_blenderartists.py # 3D 社区（Blender 论坛，23 关键词 + 排除词表 + 分级修正）
.venv/bin/python scripts/download_images.py      # 电影/剧集/游戏封面缓存
.venv/bin/python scripts/download_covers.py      # 动漫/漫画封面
.venv/bin/python scripts/make_gallery.py         # → gallery.html
.venv/bin/python scripts/make_docs.py            # → ../docs/科幻素材库-2000后.md
.venv/bin/python scripts/weread_links.py         # 微信读书链接查询（临时工具）
```

**关键设计**：
- 人工精选清单硬编码在各 `curate_*.py` 的 `KNOWN_*` 字典里（title, year → tags, ship_ref, note）；`None` 值表示"已剔除"（如疯狂的外星人/独行月球/上海堡垒），重跑不会复活。
- IMDb 类型标签不可靠（Avatar/BR2049/Ad Astra 都没标 Sci-Fi）→ 输出全量 `*_pool.csv` 供人工清单回退匹配。
- 评分：电影/剧集用 IMDb rating+票数、游戏用 Steam 好评率、动漫/漫画用 AniList 百分制、小说用 Open Library 评分。

---

## 4. 数据源与图片

| 数据源 | 用途 | 备注 |
|---|---|---|
| IMDb datasets (datasets.imdbws.com) | 电影/剧集核验 | 12.7M 行本地缓存于 branch/data/ |
| steam-insights (NewbieIndieGameDev) | 游戏 | 5 个 zip 快照 |
| IMDb suggestion API (v2.sg.media-imdb.com) | 海报 | 限流 → 间隔 2s + 重试 3 次 |
| Steam CDN (cdn.akamai.steamstatic.com) | 游戏封面 | appid/header.jpg |
| AniList GraphQL (graphql.anilist.co) | 动漫/漫画 | **403 限流**：需 UA + 1s 间隔 + 等待重试 |
| 维基百科 REST summary | 欧美漫画封面 | 有 429 限流，需退避重试 |
| Open Library API | 小说核验/评分/封面 | 免费无 key，ratings.json 拿评分 |
| 维基百科 REST summary | 原画类：概念艺术家词条核验 + 人物图 | summary 端点，无图词条 → manual + ArtStation 链接 |
| Goodreads search + book/show | 设定集封面 | search 页解析 book id → 书页 og:image（需间隔 1s+，偶发 SSL EOF 重试即可） |
| Sketchfab API (api.sketchfab.com/v3/search) | 3D 社区高人气作品 | 免 key；按 -likeCount 排序；缩略图需取 images 中 width 最大项（首项可能是 50x50），下载用 curl（urllib 被 CDN 重置），sips 压 500px；✧4 用白名单控制贴题 + 星战复刻 ≤2 |
| Blender Artists (Discourse JSON) | 民间 3D 论坛作品 | search.json?q=关键词 order:likes 拿 topic id → /t/{id}.json 拿 like_count/首帖图/作者；坑1: order:likes 混入插件公告/硬件讨论/UI 吐槽等论坛高赞帖(排除词表已积累 40+);坑2: 作品图可能是 .png,排除 png 会误杀——改按 _WxH 解析尺寸选最大图(emoji 小图自动排除);坑3: 首帖无图时遍历前 3 帖找图;SHIP_OVERRIDE 人工分级修正(如 Skyport 天空港→✧4) |
| 微信读书搜索 API (weread.qq.com/web/search/global) | 直达链接 | 返回 deepLink，格式 `book-detail?type=1&v={hash}`（**勿拼 web/bookDetail/{id}，404**） |

**图片现状**：电影 157/157、剧集 62/62、游戏 84/84（Star Citizen 用官方 YouTube 宣传片缩略图）、动漫 34/34、漫画 29/29（Letter 44 走 Open Library、Aama 走法语维基、Black Science 用 (comics) 词条）、小说 25/25。**原画/设定集 103/103 全部有图**（John Harris 封面文件与 source_id slug 不匹配已修复；Feng Zhu 因无图已整体删除（CSV/curate_art/fix_art_covers 三处），删后 art 103 条零缺图）。**其他-AI精选 24/24 有图**。

---

## 5. 踩坑记录（重要）

1. **AniList 403**：脚本批量请求触发限流（IP 级）。解决：标准 UA + 请求间隔 1s + 403 时 sleep 30s 重试。**首次排查时手动单测 UA 全通过，是频率问题不是 UA 格式问题。**
2. **同名不同年份误配**：Aliens 匹配到 2014 同名短片 → `by_norm` 空年份兜底有坑。修复：**指定年份的清单条目禁用空年份兜底**（curate_movies.py / curate_tv.py 已改）。
3. **画廊图片路径重复前缀**：`anime/anime/covers/...` → cards 模板里 img 变量已含前缀，别再硬拼。曾致全部动漫/漫画封面 404。
4. **中文标题 norm 陷阱**：「三体」norm 后为空串 → 误匹配挪威剧「Ø」。改用 IMDb 英文标题 Three-Body 匹配。
5. **维基 REST summary 404/无图**：部分词条不存在（Letter 44/Aama 英文维基无词条）→ 手写条目 + 诚实标注；词条存在但无缩略图（Black Science 是消歧义页，需 `(comics)` 后缀）。
6. **微信读书链接**：正确格式是搜索 API 返回的 deepLink（`book-detail?type=1&v=...`）；`web/bookDetail/{id}` 是 404。
7. **IMDb 海报限流**：SSL EOF → 间隔 2s + 重试 3 次；个别 tconst（Quantum Leap）suggestion API 偶发无图，重跑即可。
8. **Pages 部署**：push 后约 1-2 分钟自动重建；验证 `gh api repos/shawn1905/generation-ship/pages --jq '.status'`。
9. **Sketchfab 缩略图坑**：search API 的 `thumbnails.images` 首项可能是 50×50 小图（尺寸不统一），须取 width 最大项；media.sketchfab.com 用 urllib 下载会被 CDN 重置（TLS 指纹），要用 curl + 浏览器 UA；封面统一 sips 压 500px 控仓库体积。

---

## 6. 待办 / 已知限制

- [ ] **每日例行**：🧠 其他-AI精选扩 3-8 条（AI 主观选品，不限世代飞船；流程见 `branch/other/README.md`；维基 REST 有 429 限流需退避）
- [ ] **未来世界生图集**（docs/未来世界_生图/）：三画面已定格归档（仿生城市×2、世代飞船、戴森云×2；ChatGPT 渠道生成，GitHub 在线可看）；火山方舟 seedream 配额 08-13 23:59 重置后可跑 `docs/gen_my_future.sh` 出同款（同一世界观提示词）
- [ ] 全站链接健康巡检脚本（playwright 批量验证 AS/Goodreads/维基链接）— 未做
- [ ] 原画类部分艺术家无封面可后续从 Commons/电影词条补
- [ ] Goodreads 封面抓取偶发 SSL EOF（重试即可）；限流敏感，脚本已内置 1.2s 间隔
- [ ] 微信读书 5 本未上架：极光 Aurora、方舟 Ark、To Be Taught If Fortunate、计算之星、时间之子
- [ ] `branch/data/`（IMDb 原始数据 1.4G）与 pool CSV 不入库（.gitignore），**换机器复现需重新下载**（脚本已就绪）
- [ ] gallery 若条目继续增多可考虑懒加载/分页
- [ ] 主项目（世代飞船本体设计）尚未在本仓库体现——素材库是配套产出，主线设计文档见 `docs/讨论稿-概念与待决问题.md`

---

## 7. Git 约定

- 主线即 `main`（单分支开发，分支 `branch/scifi-collection` 已合并）。
- 提交信息中文、前缀约定：`feat:` 新增 / `fix:` 修复 / `docs:` 文档。
- 数据（CSV、图片）与脚本**全部入库**；只有原始大文件（data/、pool、.venv）忽略。
- 推送后 Pages 自动重建，无需手动操作。
