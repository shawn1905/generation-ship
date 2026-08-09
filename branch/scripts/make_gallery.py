#!/usr/bin/env python3
"""生成 branch/gallery.html：本地科幻素材画廊（电影/剧集/游戏）。
无外部依赖：纯 HTML+CSS+JS，图片走相对路径，可 file:// 直接打开。
"""
import csv, html, json, os, re

ROOT = os.path.join(os.path.dirname(__file__), '..')

SHIP_LABEL = {0: '无参考', 1: '氛围参考', 2: '外形参考', 3: '工程细节', 4: '世代飞船'}
SHIP_COLOR = {0: '#666', 1: '#8aa', 2: '#5bd', 3: '#7cf', 4: '#fd5'}

def load(csvf):
    with open(os.path.join(ROOT, csvf), newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def esc(s):
    return html.escape(str(s or ''))

def poster_path(r, sub):
    tconst = r['tconst']
    p = f'{sub}/{tconst}.jpg'
    return p if os.path.exists(os.path.join(ROOT, 'movies', sub, tconst + '.jpg')) else ''

def game_img(r):
    p = f"headers/{r['app_id']}.jpg"
    return p if (r['app_id'] and os.path.exists(os.path.join(ROOT, 'games', p))) else ''

def cover_img(r, sub):
    """动漫/漫画封面：source_id（AniList）或 title（维基/手动）"""
    key = r.get('source_id') or r.get('title')
    slug = re.sub(r'[^a-z0-9]+', '_', str(key).lower()).strip('_')
    p = f'{sub}/covers/{slug}.jpg'
    return p if os.path.exists(os.path.join(ROOT, sub, 'covers', slug + '.jpg')) else ''

ANISCORE = lambda s: 3 if (s or 0) >= 75 else (2 if (s or 0) >= 65 else (1 if (s or 0) >= 55 else 0))

def cards_novels(rows):
    out = []
    for r in rows:
        ship = int(r.get('ship_ref') or 0)
        key = re.sub(r'[^a-z0-9]+', '_', (r.get('source_id') or r['title']).lower()).strip('_')
        img = f'novels/covers/{key}.jpg'
        img = img if os.path.exists(os.path.join(ROOT, img)) else ''
        tags = ''.join(f'<span class="tag">{esc(t)}</span>' for t in r['tags'].split('|') if t)
        rating = r.get('rating') or ''
        score_txt = f"OL ★{rating}" if rating else '—'
        cnt = r.get('rating_count') or ''
        out.append(f'''<div class="card" data-tags="{esc(r['tags'])}" data-ship="{ship}">
  <a href="{esc(r['url'])}" target="_blank"><div class="imgwrap">{"<img loading='lazy' src='" + img + "' alt=''>" if img else '<div class="noimg">无图</div>'}</div></a>
  <div class="meta">
    <div class="title">{esc(r['title'])} <span class="year">{r['year']}</span></div>
    <div class="ratings">{score_txt}<span class="score">{f'（{cnt}人评）' if cnt else '作者：' + esc(r['author'])}</span></div>
    <div class="tags">{tags}</div>
    <div class="ship ship-{ship}">✧ {SHIP_LABEL[ship]}</div>
    <div class="note">{esc(r.get('note', ''))}</div>
  </div>
</div>''')
    return out

def cards_anime(rows):
    out = []
    for r in rows:
        ship = int(r.get('ship_ref') or 0)
        img = cover_img(r, 'anime')
        tags = ''.join(f'<span class="tag">{esc(t)}</span>' for t in r['tags'].split('|') if t)
        try:
            score = int(r.get('score') or 0)
        except ValueError:
            score = 0
        score_txt = f"{r['score']}/100" if r.get('score') else '—'
        out.append(f'''<div class="card" data-tags="{esc(r['tags'])}" data-ship="{ship}">
  <a href="{esc(r['url'])}" target="_blank"><div class="imgwrap">{"<img loading='lazy' src='" + img + "' alt=''>" if img else '<div class="noimg">无图</div>'}</div></a>
  <div class="meta">
    <div class="title">{esc(r['title'])} <span class="year">{r['year']}</span></div>
    <div class="ratings">{"★" * ANISCORE(score)}<span class="score">{score_txt}</span><span class="votes">人气{r['popularity']}</span></div>
    <div class="tags">{tags}</div>
    <div class="ship ship-{ship}">✧ {SHIP_LABEL[ship]}</div>
    <div class="note">{esc(r.get('note', ''))}</div>
  </div>
</div>''')
    return out

def cards_comics(rows):
    out = []
    for r in rows:
        ship = int(r.get('ship_ref') or 0)
        img = cover_img(r, 'comics')
        tags = ''.join(f'<span class="tag">{esc(t)}</span>' for t in r['tags'].split('|') if t)
        try:
            score = int(r.get('score') or 0)
        except ValueError:
            score = 0
        score_txt = f"{r['score']}/100" if r.get('score') else ('维基' if r.get('source') == 'wikipedia' else '手写')
        out.append(f'''<div class="card" data-tags="{esc(r['tags'])}" data-ship="{ship}">
  <a href="{esc(r['url'])}" target="_blank"><div class="imgwrap">{"<img loading='lazy' src='" + img + "' alt=''>" if img else '<div class="noimg">无图</div>'}</div></a>
  <div class="meta">
    <div class="title">{esc(r['title'])} <span class="year">{r['year']}</span></div>
    <div class="ratings">{"★" * ANISCORE(score)}<span class="score">{score_txt}</span></div>
    <div class="tags">{tags}</div>
    <div class="ship ship-{ship}">✧ {SHIP_LABEL[ship]}</div>
    <div class="note">{esc(r.get('note', ''))}</div>
  </div>
</div>''')
    return out

def star(rating):
    """IMDb 评分 → ★"""
    try:
        v = float(rating)
    except (TypeError, ValueError):
        return 0
    if v >= 8.3: return 3
    if v >= 7.5: return 2
    if v >= 6.5: return 1
    return 0

def cards_movie(rows, sub):
    out = []
    for r in rows:
        ship = int(r.get('ship_ref') or 0)
        img = poster_path(r, sub)
        tags = ''.join(f'<span class="tag">{esc(t)}</span>' for t in r['tags'].split('|') if t)
        out.append(f'''<div class="card" data-tags="{esc(r['tags'])}" data-ship="{ship}">
  <a href="{esc(r['imdb_url'])}" target="_blank"><div class="imgwrap">{"<img loading='lazy' src='movies/" + img + "' alt=''>" if img else '<div class="noimg">无图</div>'}</div></a>
  <div class="meta">
    <div class="title">{esc(r['title'])} <span class="year">{r['year']}</span></div>
    <div class="ratings">{"★" * star(r['imdb_rating'])}<span class="score">{r['imdb_rating']}</span><span class="votes">({r['num_votes']}票)</span></div>
    <div class="tags">{tags}</div>
    <div class="ship ship-{ship}">✧ {SHIP_LABEL[ship]}</div>
    <div class="note">{esc(r.get('note', ''))}</div>
  </div>
</div>''')
    return out  # 返回数组

def cards_games(rows):
    out = []
    for r in rows:
        ship = int(r.get('ship_ref') or 0)
        img = game_img(r)
        pct = r.get('positive_pct') or '0'
        try:
            pctf = float(pct)
            pstars = 3 if pctf >= 95 else (2 if pctf >= 88 else (1 if pctf >= 80 else 0))
        except ValueError:
            pstars = 0
        tags = ''.join(f'<span class="tag">{esc(t)}</span>' for t in r['tags'].split('|') if t)
        rev = f"{r['total_reviews']}评·{pct}%" if r.get('total_reviews') else (r.get('review_score_desc') or '')
        out.append(f'''<div class="card" data-tags="{esc(r['tags'])}" data-ship="{ship}">
  <a href="{esc(r['steam_url'])}" target="_blank"><div class="imgwrap wide">{"<img loading='lazy' src='games/" + img + "' alt=''>" if img else '<div class="noimg">无图</div>'}</div></a>
  <div class="meta">
    <div class="title">{esc(r['name'])} <span class="year">{r['release_year']}</span></div>
    <div class="ratings">{"★" * pstars}<span class="score">{rev}</span></div>
    <div class="tags">{tags}</div>
    <div class="ship ship-{ship}">✧ {SHIP_LABEL[ship]}</div>
    <div class="note">{esc(r.get('note', ''))}</div>
  </div>
</div>''')
    return out  # 返回数组

def main():
    movies = load('movies/scifi_movies_curated.csv')
    tv = load('movies/scifi_tv_curated.csv')
    games = load('games/scifi_games_curated.csv')
    anime = load('anime/scifi_anime_curated.csv')
    comics = load('comics/scifi_comics_curated.csv')
    novels = load('novels/scifi_novels_curated.csv')

    html_doc = f'''<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>2000+ 科幻素材库 · 世代飞船设计参考</title>
<style>
:root {{ color-scheme: dark; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ background: radial-gradient(ellipse at 20% 0%, #131a2e 0%, #0a0d18 55%, #05060c 100%); color: #d8def0; font: 14px/1.5 -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif; min-height: 100vh; }}
header {{ padding: 28px 32px 10px; }}
h1 {{ font-size: 22px; letter-spacing: 1px; }}
h1 small {{ color: #7a86a8; font-weight: 400; font-size: 13px; margin-left: 10px; }}
.sub {{ color: #8b96b8; margin: 6px 0 0; font-size: 13px; }}
.tabs {{ display: flex; gap: 8px; margin: 16px 32px; }}
.tab {{ background: #1a2240; border: 1px solid #2c3860; color: #9fb0d8; padding: 8px 18px; border-radius: 20px; cursor: pointer; font-size: 14px; }}
.tab.active {{ background: #2b3a6e; color: #fff; border-color: #4a5f9e; }}
.tab b {{ color: #ffd75e; }}
.controls {{ margin: 0 32px 14px; display: flex; gap: 10px; flex-wrap: wrap; align-items: center; }}
#search {{ background: #12182c; border: 1px solid #2c3860; color: #e8ecf8; padding: 8px 14px; border-radius: 8px; width: 240px; font-size: 14px; }}
.chip {{ background: #151d36; border: 1px solid #2c3860; color: #9fb0d8; padding: 4px 12px; border-radius: 14px; cursor: pointer; font-size: 12px; }}
.chip.on {{ background: #35477f; color: #fff; border-color: #5a74bd; }}
.chip.ship {{ border-color: #7a5c1e; color: #e8c36a; }}
#grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(210px, 1fr)); gap: 16px; padding: 0 32px 40px; }}
.card {{ background: #10162a; border: 1px solid #223052; border-radius: 10px; overflow: hidden; transition: transform .15s, border-color .15s; }}
.card:hover {{ transform: translateY(-3px); border-color: #3c5090; }}
.imgwrap {{ aspect-ratio: 2/3; background: #0a0f1e; overflow: hidden; }}
.imgwrap.wide {{ aspect-ratio: 460/215; }}
.card img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
.noimg {{ display: flex; align-items: center; justify-content: center; height: 100%; color: #4a5578; font-size: 13px; }}
.meta {{ padding: 10px 12px 12px; }}
.title {{ font-weight: 600; font-size: 14px; }}
.year {{ color: #6b77a0; font-weight: 400; font-size: 12px; margin-left: 4px; }}
.ratings {{ color: #ffd75e; font-size: 13px; margin: 3px 0; }}
.score {{ color: #c8d2f0; margin-left: 6px; }}
.votes {{ color: #6b77a0; font-size: 11px; }}
.tags {{ margin: 5px 0; display: flex; flex-wrap: wrap; gap: 4px; }}
.tag {{ background: #1c2547; color: #9fb0d8; font-size: 11px; padding: 1px 8px; border-radius: 10px; }}
.ship {{ font-size: 12px; margin-top: 4px; }}
.note {{ color: #7a86a8; font-size: 12px; margin-top: 5px; line-height: 1.4; }}
.legend {{ color: #8b96b8; font-size: 12px; margin: 0 32px 18px; }}
.legend span {{ margin-right: 14px; }}
.hide {{ display: none !important; }}
footer {{ color: #4a5578; font-size: 12px; padding: 0 32px 30px; }}
</style></head><body>
<header><h1>🚀 2000+ 科幻素材库<small>Generation Ship Design · 参考收集</small></h1>
<div class="sub">电影 / 剧集 / 游戏 · 内容+评价驱动 · ✧ 标注飞船设计参考价值（世代飞船级 = 主线直接参考）</div></header>
<div class="tabs">
  <div class="tab active" data-tab="movies">🎬 电影 <b>{len(movies)}</b></div>
  <div class="tab" data-tab="tv">📺 剧集 <b>{len(tv)}</b></div>
  <div class="tab" data-tab="games">🎮 游戏 <b>{len(games)}</b></div>
  <div class="tab" data-tab="anime">🛸 动漫 <b>{len(anime)}</b></div>
  <div class="tab" data-tab="comics">📚 漫画 <b>{len(comics)}</b></div>
  <div class="tab" data-tab="novels">📖 小说 <b>{len(novels)}</b></div>
</div>
<div class="controls">
  <input id="search" placeholder="搜索标题…">
  <span class="chip ship" data-filter="4">✧ 世代飞船级(4)</span>
  <span class="chip ship" data-filter="3">✧ 工程细节(3)</span>
  <span class="chip ship" data-filter="2">✧ 外形参考(2)</span>
  <span id="tagbox"></span>
  <span class="chip" data-filter="clear" style="display:none" id="clearBtn">✕ 清除</span>
</div>
<div class="legend"><span>✧✧✧✧ 世代飞船直接参考</span><span>✧✧✧ 内部结构/工程细节</span><span>✧✧ 飞船/空间站外形</span><span>✧ 视觉氛围</span><span>无 ✧ 设定/主题参考</span><span>★ 评价分级</span></div>
<div id="grid" data-which="movies"></div>
<footer>数据：IMDb 官方数据集（电影/剧集）+ Steam 2024-10 全量快照（steam-insights）· 人工精选 + 数据核验 · 图片本地缓存</footer>
<script>
const DATA = {{
  movies: {json.dumps(movies, ensure_ascii=False)},
  tv: {json.dumps(tv, ensure_ascii=False)},
  games: {json.dumps(games, ensure_ascii=False)},
  anime: {json.dumps(anime, ensure_ascii=False)},
  comics: {json.dumps(comics, ensure_ascii=False)},
  novels: {json.dumps(novels, ensure_ascii=False)}
}};
const CARD = {{ movies: {json.dumps(cards_movie(movies, 'posters'), ensure_ascii=False)},
  tv: {json.dumps(cards_movie(tv, 'tv_posters'), ensure_ascii=False)},
  games: {json.dumps(cards_games(games), ensure_ascii=False)},
  anime: {json.dumps(cards_anime(anime), ensure_ascii=False)},
  comics: {json.dumps(cards_comics(comics), ensure_ascii=False)},
  novels: {json.dumps(cards_novels(novels), ensure_ascii=False)} }};
let which = 'movies', search = '', tagF = new Set(), shipF = null;
const grid = document.getElementById('grid');
function allTags() {{
  const s = new Set();
  DATA[which].forEach(r => (r.tags||'').split('|').filter(Boolean).forEach(t => s.add(t)));
  return [...s].sort();
}}
function renderTags() {{
  const box = document.getElementById('tagbox');
  box.innerHTML = allTags().map(t => `<span class="chip ${{tagF.has(t)?'on':''}}" data-tag="${{t}}">${{t}}</span>`).join('');
  document.getElementById('clearBtn').style.display = (tagF.size || shipF || search) ? '' : 'none';
}}
function render() {{
  const cards = CARD[which];
  const shown = [];
  cards.forEach((c, i) => {{
    const r = DATA[which][i];
    const t = (r.tags||'').toLowerCase();
    const okTag = tagF.size === 0 || [...tagF].every(x => t.includes(x.toLowerCase()));
    const okShip = shipF === null || String(r.ship_ref) === shipF;
    const okSearch = !search || (r.title||r.name||'').toLowerCase().includes(search);
    shown.push(okTag && okShip && okSearch);
  }});
  grid.innerHTML = cards.map((c, i) => `<div class="${{shown[i]?'':'hide'}}">${{c}}</div>`).join('');
}}
document.querySelectorAll('.tab').forEach(t => t.onclick = () => {{
  document.querySelectorAll('.tab').forEach(x => x.classList.remove('active'));
  t.classList.add('active'); which = t.dataset.tab; tagF.clear(); shipF = null; renderTags(); render();
}});
document.getElementById('search').oninput = e => {{ search = e.target.value.trim().toLowerCase(); render(); }};
document.getElementById('tagbox').onclick = e => {{
  const c = e.target.closest('.chip'); if (!c) return;
  const t = c.dataset.tag; tagF.has(t) ? tagF.delete(t) : tagF.add(t);
  c.classList.toggle('on'); renderTags(); render();
}};
document.querySelectorAll('.chip[data-filter]').forEach(c => c.onclick = () => {{
  const v = c.dataset.filter;
  if (v === 'clear') {{ tagF.clear(); shipF = null; search = ''; document.getElementById('search').value=''; renderTags(); render(); return; }}
  shipF = (shipF === v) ? null : v;
  document.querySelectorAll('.chip[data-filter]').forEach(x => x.classList.toggle('on', x.dataset.filter === shipF));
  render();
}});
renderTags(); render();
</script></body></html>'''
    with open(os.path.join(ROOT, 'gallery.html'), 'w', encoding='utf-8') as f:
        f.write(html_doc)
    print('gallery.html written:', os.path.getsize(os.path.join(ROOT, 'gallery.html')) // 1024, 'KB')

if __name__ == '__main__':
    main()
