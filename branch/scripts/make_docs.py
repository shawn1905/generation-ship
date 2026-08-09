#!/usr/bin/env python3
"""生成 docs/科幻素材库-1980后.md：人读汇总（表格由数据自动生成）"""
import csv, os
from collections import defaultdict

ROOT = os.path.join(os.path.dirname(__file__), '..', '..')  # generation-ship

def load(csvf):
    with open(os.path.join(ROOT, csvf), newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

movies = load('branch/movies/scifi_movies_curated.csv')
tv = load('branch/movies/scifi_tv_curated.csv')
games = load('branch/games/scifi_games_curated.csv')
anime = load('branch/anime/scifi_anime_curated.csv')
comics = load('branch/comics/scifi_comics_curated.csv')
novels = load('branch/novels/scifi_novels_curated.csv')

def rating_str(r, kind):
    if kind == 'game':
        return f"{r['positive_pct']}%（{r['total_reviews']}评）" if r.get('total_reviews') else r.get('review_score_desc') or '—'
    if kind in ('anime', 'comic'):
        return (f"{r['score']}/100" if r.get('score') else ('维基' if r.get('source') == 'wikipedia' else '手写'))
    if kind == 'novel':
        return f"OL ★{r['rating']}（{r['rating_count']}人）" if r.get('rating') else '—'
    return f"{r['imdb_rating']}（{r['num_votes']}票）"

def row(r, kind, tag=''):
    if kind == 'game':
        name, year = r['name'], r['release_year']
    elif kind == 'novel':
        name, year = f"{r['title']}（{r['author']}）", r['year']
    else:
        name, year = r['title'], r['year']
    tags = tag or r.get('tags', '')
    note = r.get('note', '')
    return f"| {name} | {year} | {rating_str(r, kind)} | {tags} | {note} |"

# ---- 分组 ----
ship4 = [(r, k) for k, rs in (('movie', movies), ('tv', tv), ('game', games), ('anime', anime), ('comic', comics), ('novel', novels)) for r in rs if r.get('ship_ref') == '4']
ship3 = [(r, k) for k, rs in (('movie', movies), ('tv', tv), ('game', games), ('anime', anime), ('comic', comics), ('novel', novels)) for r in rs if r.get('ship_ref') == '3']
ship2 = [(r, k) for k, rs in (('movie', movies), ('tv', tv), ('game', games), ('anime', anime), ('comic', comics), ('novel', novels)) for r in rs if r.get('ship_ref') == '2']

tag_index = defaultdict(list)
for k, rs in (('movie', movies), ('tv', tv), ('game', games), ('anime', anime), ('comic', comics), ('novel', novels)):
    for r in rs:
        for t in (r.get('tags') or '').split('|'):
            if t:
                tag_index[t].append((r, k))
# 只保留有意义的主题标签（去掉泛标签）
CORE_TAGS = ['世代飞船', '硬科幻', '太空歌剧', '赛博朋克', '反乌托邦', 'AI', '外星接触',
             '时间循环', '末世', '机甲', '太空恐怖', '殖民', '方舟', '星际航行', '火星']

lines = []
lines.append('# 科幻素材库（1980+）· 世代飞船设计参考\n')
lines.append('> **分支收集工作产出**：1980 年以后的科幻电影 / 剧集 / 游戏，按内容与评价整理，服务于世代飞船设计主线。\n')
lines.append('> **交互式画廊**：`branch/gallery.html`（双击本地打开，六区 Tab + 标签过滤 + 图片；在线版见 GitHub Pages）\n')
lines.append('---\n')
lines.append('## 0. 收集方法与数据源（可复现）\n')
lines.append('| 步骤 | 说明 | 数据源 |')
lines.append('|---|---|---|')
lines.append('| 电影/剧集原始数据 | IMDb 官方非商业数据集（title.basics + title.ratings，2025-08 快照） | https://datasets.imdbws.com/ |')
lines.append('| 游戏原始数据 | Steam 2024-10 全量快照（games/genres/tags/reviews/steamspy） | https://github.com/NewbieIndieGameDev/steam-insights |')
lines.append('| 精选策略 | 人工代表作清单 + 数据核验（评分/票数/好评率），非自动全量 | — |')
lines.append('| 海报/封面 | IMDb suggestion JSON API + Steam CDN，本地缓存 | https://v2.sg.media-imdb.com/ |')
lines.append('| 复现脚本 | `branch/scripts/`（make_* 原始过滤 → curate_* 人工精选 → download_images → make_gallery/docs） | 本仓库 |\n')
lines.append('> **重要发现**：IMDb 类型标签不可靠（Avatar/Blade Runner 2049/Ad Astra 均未标 Sci-Fi），故精选用"人工清单 + 全量候选池匹配"而非纯标签过滤。\n')
lines.append('---\n')
lines.append('## 1. 标签体系\n')
lines.append('每条目按**内容**打主题标签（可多选），独立于 IMDb/Steam 自带类型。核心主题：')
lines.append('`世代飞船` `方舟` `星际航行` `硬科幻` `太空歌剧` `殖民` `火星` `外星接触` `AI` `赛博朋克` `反乌托邦` `时间循环` `末世` `机甲` `太空恐怖` 等。\n')
lines.append('---\n')
lines.append('## 2. ship_ref 分级（飞船设计参考价值）\n')
lines.append('| 级别 | 含义 | 示例 |')
lines.append('|---|---|---|')
lines.append('| ✧✧✧✧ 4 | **世代飞船直接参考**（主线重点） | The Expanse Nauvoo、BSG 方舟舰队、Passengers、Aniara、Pandorum、Ixion |')
lines.append('| ✧✧✧ 3 | 内部结构 / 工程细节 | 石村号、Talos I、诺曼底号、Hardspace: Shipbreaker、流浪地球 |')
lines.append("| ✧✧ 2 | 飞船 / 空间站外形设计 | Dune、BR2049 载具、Stellaris、No Man's Sky |")
lines.append('| ✧ 1 | 视觉氛围 / 基地细节 | Gravity 轨道物理、For All Mankind 工程细节 |')
lines.append('| 0 | 设定 / 主题参考（无飞船设计价值） | 黑镜、时间循环类 |\n')
lines.append('---\n')
lines.append('## 3. 统计\n')
lines.append('| 类别 | 精选数 | 原始池 |')
lines.append('|---|---|---|')
lines.append(f'| 电影 | {len(movies)} | {9076} 部（Sci-Fi 标签 1980+ 有票） |')
lines.append(f'| 剧集 | {len(tv)} | {4462} 部 |')
lines.append(f'| 游戏 | {len(games)} | {1775} 款（Sci-Fi 相关标签 2000+） |')
lines.append(f'| 动漫 | {len(anime)} | AniList 人工清单+核验 |')
lines.append(f'| 漫画 | {len(comics)} | AniList(日漫)+维基(欧美) |')
lines.append(f'| 小说 | {len(novels)} | Open Library 核验+评分 |')
lines.append(f'| **合计** | **{len(movies)+len(tv)+len(games)+len(anime)+len(comics)+len(novels)}** | — |\n')
lines.append('---\n')

lines.append('## 4. ✧✧✧✧ 世代飞船级参考（主线重点）\n')
lines.append('| 作品 | 年份 | 评价 | 标签 | 说明 |')
lines.append('|---|---|---|---|---|')
for r, k in ship4:
    lines.append(row(r, k))
lines.append('')
lines.append('---\n')
lines.append('## 5. ✧✧✧ 工程细节级参考\n')
lines.append('| 作品 | 年份 | 评价 | 标签 | 说明 |')
lines.append('|---|---|---|---|---|')
for r, k in ship3:
    lines.append(row(r, k))
lines.append('')
lines.append('---\n')
lines.append('## 6. 主题速览（每主题 Top 6）\n')
for t in CORE_TAGS:
    items = tag_index.get(t, [])
    if not items:
        continue
    lines.append(f'### {t}（{len(items)} 部/款）\n')
    lines.append('| 作品 | 年份 | 评价 | 说明 |')
    lines.append('|---|---|---|---|')
    for r, k in items[:6]:
        name = r['title'] if k != 'game' else r['name']
        year = r['year'] if k != 'game' else r['release_year']
        note = (r.get('note') or '')[:40]
        lines.append(f"| {name} | {year} | {rating_str(r, k)} | {note} |")
    lines.append('')
lines.append('---\n')
lines.append('## 7. 评价指标说明\n')
lines.append('- **电影/剧集**：IMDb 评分 + 投票数（数据集中 `title.ratings`）')
lines.append('- **游戏**：Steam 好评率 + 评价总数（steam-insights `reviews.csv`），另有 SteamSpy 估算玩家数')
lines.append('- **精选门槛**：人工清单为主；自动档参考阈值 电影≥5000 票、游戏好评率≥80% 且评价≥1000 或玩家≥20 万\n')
lines.append('---\n')
lines.append('*生成：branch/scripts/make_docs.py · 数据快照 2025-08 · 世代飞船设计项目*')

out = os.path.join(ROOT, 'docs', '科幻素材库-2000后.md')
with open(out, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines) + '\n')
print('written:', out, os.path.getsize(out) // 1024, 'KB')
print(f'ship4={len(ship4)} ship3={len(ship3)} ship2={len(ship2)}')
