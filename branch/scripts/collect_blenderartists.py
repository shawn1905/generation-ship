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
    ('space ark', '4', '方舟飞船|巨构'),
    ('interstellar ship', '4', '星际飞船|巨构'),
    ('spaceport', '4', '太空港|巨构'),
    ('space elevator', '4', '太空电梯|巨构'),
    ('space station', '3', '空间站|巨构'),
    ('starship interior', '3', '内部结构|甲板'),
    ('spaceship cockpit', '3', '驾驶舱|内部'),
    ('spaceship bridge', '3', '舰桥|内部'),
    ('spaceship hangar', '3', '机库|内部'),
    ('spaceship', '2', '飞船|外形'),
    ('spacecraft', '2', '航天器|外形'),
    ('starfighter', '2', '战斗机|外形'),
    ('sci-fi ship', '2', '飞船|外形'),
    ('sci-fi corridor', '1', '走廊|环境'),
    ('alien world', '1', '外星世界|环境'),
    ('futuristic architecture', '1', '未来建筑|环境'),
]

MIN_LIKES = 55         # 论坛点赞门槛
PER_QUERY = 12         # 每关键词候选数
MAX_TOTAL = 50         # 总条数上限

EXCLUDE_WORDS = ['car', 'motorcycle', 'airplane', 'train', 'tank', 'gun', 'robot',
                 'character', 'portrait', 'city', 'subway', 'speedbike',
                 'addon', 'add-on', 'add on', 'geo-scatter', 'flip fluids', 'bonsai', 'blenderbim',
                 'proxify', 'clarification', 'challenge', 'sketchbook', 'best of', 'get ready',
                 'ai generated', 'a.n.t', 'texture based version', 'dino', 'skeleton', 'proxy',
                 'sinektronaut', 'zbrush', 'random flow',
                 'batmobile', 'vanity', 'grease', 'iphone', '36 days', 'letter t', 'mmos',
                 'spacesuit', 'study', 'mmo', 'tutorial', 'how to', 'course', 'job',
                 'm3 ', 'sdf thread', 'filmic', 'progress and practice', 'flexi bezier',
                 '3d-coat', 'large and complex', 'battle arena', "blender's ui", 'treehead',
                 'vehicle concept', 'hardware accelerated', 'hardware']

# 人工分级修正: 标题关键词 → ship_ref(覆盖自动映射)
SHIP_OVERRIDE = {
    'Skyport Usak': '4',   # 天空港 = 巨构,世代飞船直接参考
}

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
            imgs = []
            for p in posts[:3]:  # 首帖无图时往后找
                imgs += re.findall(r'<img[^>]+src="([^"]+)"', p.get('cooked') or '')
            img = ''
            best_w = 0
            for u in imgs:  # 选尺寸最大的作品图(排除 emoji 小图,兼容 jpg/png/webp)
                if '/uploads/' not in u:
                    continue
                m = re.search(r'_(\d+)x\d+\.(?:jpe?g|png|webp)$', u)
                w = int(m.group(1)) if m else (2000 if '/original/' in u else 0)
                if w > best_w:
                    img, best_w = u, w
            desc = re.sub(r'<[^>]+>', ' ', p0.get('cooked') or '')
            desc = re.sub(r'\s+', ' ', desc).strip()
            if len(desc) > 60:
                desc = desc[:60] + '…'
            row = {
                'title': title, 'type': '3D社区', 'artist': p0.get('username') or '?',
                'year': (d.get('created_at') or '')[:4], 'source': 'blenderartists', 'source_id': tid,
                'tags': f'{tagbase}|Blender|社区论坛', 'ship_ref': ship,
                'note': f'♥{likes} 赞 · 回复{d.get("posts_count") or 0}。{desc}',
                'url': f'{BASE}/t/{tid}', 'cover_img': img, 'img_note': 'Blender 论坛渲染图',
            }
            by_ship[ship][tid] = row
            for k, v in SHIP_OVERRIDE.items():  # 分级修正
                if k.lower() in title.lower():
                    by_ship[ship].pop(tid, None)
                    row['ship_ref'] = v
                    by_ship[v][tid] = row
                    break
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
