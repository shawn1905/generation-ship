#!/usr/bin/env python3
"""Blender Artists 论坛高人气科幻作品收集(民间 3D 社区第二源)。

Discourse JSON API:
  1. search.json?q={kw} order:likes → 候选 topic ids
  2. /t/{id}.json → like_count / 首帖渲染图 / 作者 / 年份
按点赞门槛过滤 → 分级配额 → 封面下载(500px) → branch/art/blenderartists_curated.csv
"""
import csv, json, os, re, subprocess, time, urllib.request, urllib.parse

ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
OUT = os.path.join(ROOT, 'branch', 'art')
BASE = 'https://blenderartists.org'
UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/125 Safari/537.36'}

# (关键词, ship_ref, 标签)  与 Sketchfab 同分级
QUERIES = [
    ('generation ship', '4', '世代飞船|巨构'),
    ('space habitat', '4', '栖息地|生态'),
    ('space colony', '4', '殖民地|栖息地'),
    ('battle cruiser', '4', '主力舰|巨构'),
    ('colony ship', '4', '殖民船|巨构'),
    ('mothership', '4', '母舰|巨构'),
    ('orbital station', '4', '轨道站|巨构'),
    ('space station', '3', '空间站|巨构'),
    ('starship interior', '3', '内部结构|甲板'),
    ('spaceship cockpit', '3', '驾驶舱|内部'),
    ('spaceship', '2', '飞船|外形'),
    ('sci-fi corridor', '1', '走廊|环境'),
]

MIN_LIKES = 60         # 论坛点赞门槛
PER_QUERY = 12         # 每关键词候选数
MAX_TOTAL = 30         # 总条数上限

EXCLUDE_WORDS = ['car', 'motorcycle', 'airplane', 'train', 'tank', 'gun', 'robot',
                 'character', 'portrait', 'city', 'subway', 'speedbike',
                 'addon', 'add-on', 'add on', 'geo-scatter', 'flip fluids', 'bonsai', 'blenderbim',
                 'proxify', 'clarification', 'challenge', 'sketchbook', 'best of', 'get ready',
                 'ai generated', 'a.n.t', 'texture based version', 'dino', 'skeleton', 'proxy',
                 'sinektronaut', 'zbrush', 'random flow']

def search(q, n):
    url = f'{BASE}/search.json?' + urllib.parse.urlencode({'q': f'{q} order:likes'})
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r).get('topics', [])[:n]

def get_topic(tid):
    url = f'{BASE}/t/{tid}.json'
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)

def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(os.path.join(OUT, 'covers_forum'), exist_ok=True)

    by_ship = {'4': {}, '3': {}, '2': {}, '1': {}}
    seen = set()
    for q, ship, tagbase in QUERIES:
        try:
            topics = search(q, PER_QUERY)
        except Exception as e:
            print(f'  ERR search [{q}]: {e}')
            time.sleep(1)
            continue
        for t in topics:
            tid = str(t.get('id'))
            if not tid or tid in seen:
                continue
            title = t.get('title') or ''
            if any(w in title.lower() for w in EXCLUDE_WORDS):
                continue
            try:
                d = get_topic(tid)
            except Exception as e:
                continue
            likes = d.get('like_count') or 0
            if likes < MIN_LIKES:
                continue
            posts = d.get('post_stream', {}).get('posts', [])
            p0 = posts[0] if posts else {}
            imgs = re.findall(r'<img[^>]+src="([^"]+)"', p0.get('cooked') or '')
            img = ''
            for u in imgs:  # 优先非 emoji 的大图
                if '/uploads/' in u and not u.endswith('.png'):
                    img = u.replace('/optimized/', '/original/').split('_2_')[0] + '.jpeg' if '_2_' in u else u
                    break
            desc = re.sub(r'<[^>]+>', ' ', p0.get('cooked') or '')
            desc = re.sub(r'\s+', ' ', desc).strip()
            if len(desc) > 60:
                desc = desc[:60] + '…'
            by_ship[ship][tid] = {
                'title': title, 'type': '3D社区', 'artist': p0.get('username') or '?',
                'year': (d.get('created_at') or '')[:4], 'source': 'blenderartists', 'source_id': tid,
                'tags': f'{tagbase}|Blender|社区论坛', 'ship_ref': ship,
                'note': f'♥{likes} 赞 · 回复{d.get("posts_count") or 0}。{desc}',
                'url': f'{BASE}/t/{tid}', 'cover_img': img, 'img_note': 'Blender 论坛渲染图',
            }
            seen.add(tid)
        print(f'  [{q}] 累计 {len(by_ship["4"])}/{len(by_ship["3"])}/{len(by_ship["2"])}/{len(by_ship["1"])}')
        time.sleep(0.6)

    rows = []
    for ship in ['4', '3', '2', '1']:
        pool = sorted(by_ship[ship].values(), key=lambda r: -int(re.search(r'♥(\d+)', r['note']).group(1)))
        rows.extend(pool)
        print(f'  ship{ship}: {len(pool)} 条')
    rows = sorted(rows, key=lambda r: -int(re.search(r'♥(\d+)', r['note']).group(1)))
    if len(rows) > MAX_TOTAL:
        rows = rows[:MAX_TOTAL]

    with open(os.path.join(OUT, 'blenderartists_curated.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f'blenderartists curated: {len(rows)} 条')

    print('== 封面下载 ==')
    ok = fail = 0
    for r in rows:
        dest = os.path.join(OUT, 'covers_forum', r['source_id'] + '.jpg')
        if os.path.exists(dest) and os.path.getsize(dest) > 2000:
            ok += 1
            continue
        if not r['cover_img']:
            fail += 1
            continue
        tmp = dest + '.tmp'
        try:
            subprocess.run(['curl', '-s', '-L', '-m', '30', '-A', UA['User-Agent'], r['cover_img'], '-o', tmp],
                           check=True, capture_output=True)
            if not os.path.exists(tmp) or os.path.getsize(tmp) < 2000:
                raise ValueError('download fail')
            subprocess.run(['sips', '-Z', '500', tmp, '--out', dest], check=True, capture_output=True)
            os.remove(tmp)
            ok += 1
        except Exception as e:
            fail += 1
            print(f'  cover fail {r["title"][:36]}: {e}')
        time.sleep(0.3)
    print(f'covers_forum: ok={ok} fail={fail}')

if __name__ == '__main__':
    main()
