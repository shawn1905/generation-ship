#!/usr/bin/env python3
"""3D 社区作品收集(Sketchfab)：欧美 3D 艺术家社区高人气民间科幻作品。

按 likeCount 排序抓取飞船/空间站/内部结构/世代飞船等关键词,精选高人气条目,
输出 branch/art/sketchfab_curated.csv + covers_3d/{uid}.jpg(500px 封面)。

数据源: https://api.sketchfab.com/v3/search (公开免 key)
"""
import csv, json, os, re, subprocess, time, urllib.request, urllib.parse

ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
OUT = os.path.join(ROOT, 'branch', 'art')
UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/125 Safari/537.36'}

# (关键词, ship_ref, 备注标签)  ship_ref: 4=世代飞船 3=内部工程 2=外形 1=氛围
QUERIES = [
    ('generation ship', '4', '世代飞船|巨构'),
    ('space habitat', '4', '栖息地|生态'),
    ('space station', '3', '空间站|巨构'),
    ('orbital ring', '4', '轨道环|巨构'),
    ('sci-fi spaceship', '2', '飞船|外形'),
    ('starship', '2', '飞船|外形'),
    ('starship interior', '3', '内部结构|甲板'),
    ('spaceship cockpit', '3', '驾驶舱|内部'),
    ('spaceship engine', '3', '引擎|推进'),
    ('sci-fi corridor', '1', '走廊|环境'),
    ('space colony', '4', '殖民地|栖息地'),
    ('sci-fi city', '1', '城市|氛围'),
]

MIN_LIKES = 150       # 人气门槛(分级覆盖)
PER_QUERY = 8         # 每关键词取 top N
MAX_TOTAL = 36        # 最终条数上限

# 分级门槛与配额: ship_ref → (最少like, 目标条数)
RULES = {
    '4': (80, 9),    # 世代飞船/栖息地/巨构: 放宽人气,保证覆盖
    '3': (120, 11),  # 内部/工程
    '2': (150, 11),  # 飞船外形
    '1': (250, 7),   # 氛围: 高门槛,只留真正人气作品
}

# 明显不相关的名字关键词(人工剔除规则)
EXCLUDE_WORDS = ['subway', 'train', 'airport', 'airplane', 'aircraft', 'fighter jet', 'tank', 'motorcycle',
                 'drone', 'robot', 'mech', 'gun', 'rifle', 'soldier', 'character', 'portrait', 'human',
                 'speeder bike', 'watermelon', 'spaceman', 'osaka', 'police chase', 'future car',
                 'monitor', 'city pop', '80s', 'styliized', '80 ']

# 精确标题排除(收集后人工核对清单)
EXCLUDE_TITLES = ['Future Car', 'Sci fi Monitor', 'Stylized City View', 'Police Chase',
                  'Osaka downtown', 'Watermelone', 'Spaceman Model', 'StarWars Speeder Bike',
                  'city', 'Sci Fi Wall Bridge With Monitor', 'Sci-Fi Corridor - Revisited 2019',
                  'Cuban Macaw', 'Urban Concrete Dwellings', 'Project Eden']

def search(q, n):
    url = 'https://api.sketchfab.com/v3/search?' + urllib.parse.urlencode({
        'type': 'models', 'q': q, 'sort_by': '-likeCount', 'count': n})
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r).get('results', [])

def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(os.path.join(OUT, 'covers_3d'), exist_ok=True)

    by_ship = {'4': {}, '3': {}, '2': {}, '1': {}}  # ship_ref -> uid -> row
    seen_uids = set()  # 全局去重(跨级)
    for q, ship, tagbase in QUERIES:
        try:
            results = search(q, PER_QUERY)
        except Exception as e:
            print(f'  ERR [{q}]: {e}')
            time.sleep(1)
            continue
        for m in results:
            uid = m.get('uid')
            if not uid or uid in seen_uids:
                continue
            name = m.get('name') or ''
            if any(w in name.lower() for w in EXCLUDE_WORDS):
                continue
            if any(t in name for t in EXCLUDE_TITLES):
                continue
            likes = m.get('likeCount') or 0
            min_like, _ = RULES[ship]
            if likes < min_like:
                continue
            user = m.get('user') or {}
            thumbs = (m.get('thumbnails') or {}).get('images') or []
            # 选最大尺寸缩略图(search API 尺寸不统一,可能首项是 50x50 小图)
            thumb = max(thumbs, key=lambda t: t.get('width') or 0).get('url', '') if thumbs else ''
            desc = (m.get('description') or '').strip().replace('\n', ' ')
            if len(desc) > 70:
                desc = desc[:70] + '…'
            by_ship[ship][uid] = {
                'title': name, 'type': '3D社区', 'artist': user.get('displayName') or user.get('username') or '?',
                'year': (m.get('publishedAt') or '')[:4], 'source': 'sketchfab', 'source_id': uid,
                'tags': f'{tagbase}|3D模型|社区人气', 'ship_ref': ship,
                'note': f'♥{likes} 赞 · {m.get("viewCount") or 0} 浏览。{desc}',
                'url': m.get('viewerUrl') or f'https://sketchfab.com/3d-models/{uid}',
                'cover_img': thumb, 'img_note': 'Sketchfab 渲染图',
            }
            seen_uids.add(uid)
        print(f'  [{q}] 累计 4级:{len(by_ship["4"])} 3级:{len(by_ship["3"])} 2级:{len(by_ship["2"])} 1级:{len(by_ship["1"])}')
        time.sleep(0.5)

    # 按级配额截取
    rows = []
    for ship in ['4', '3', '2', '1']:
        _, quota = RULES[ship]
        pool = sorted(by_ship[ship].values(), key=lambda r: -int(re.search(r'♥(\d+)', r['note']).group(1)))
        rows.extend(pool[:quota])
        print(f'  ship{ship}: 候选{len(pool)} → 取{min(len(pool), quota)}')

    rows = sorted(rows, key=lambda r: -int(re.search(r'♥(\d+)', r['note']).group(1)))
    with open(os.path.join(OUT, 'sketchfab_curated.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f'sketchfab curated: {len(rows)} 条')

    # 封面下载(curl + sips 压 500px)
    print('== 封面下载 ==')
    ok = fail = 0
    for r in rows:
        dest = os.path.join(OUT, 'covers_3d', r['source_id'] + '.jpg')
        if os.path.exists(dest) and os.path.getsize(dest) > 2000:
            ok += 1
            continue
        url = r['cover_img']
        if not url:
            fail += 1
            continue
        tmp = dest + '.tmp'
        try:
            subprocess.run(['curl', '-s', '-m', '30', '-A', UA['User-Agent'], url, '-o', tmp], check=True, capture_output=True)
            if not os.path.exists(tmp) or os.path.getsize(tmp) < 2000:
                raise ValueError('download fail')
            subprocess.run(['sips', '-Z', '500', tmp, '--out', dest], check=True, capture_output=True)
            os.remove(tmp)
            ok += 1
        except Exception as e:
            fail += 1
            # 兜底: search 缩略图小/失效时,查详情接口取最大图
            try:
                url = 'https://api.sketchfab.com/v3/models/' + r['source_id']
                d = json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=20))
                thumbs = (d.get('thumbnails') or {}).get('images') or []
                big = max(thumbs, key=lambda t: t.get('width') or 0).get('url', '') if thumbs else ''
                if big:
                    subprocess.run(['curl', '-s', '-m', '40', '-A', UA['User-Agent'], big, '-o', tmp], check=True, capture_output=True)
                    if os.path.exists(tmp) and os.path.getsize(tmp) > 2000:
                        subprocess.run(['sips', '-Z', '500', tmp, '--out', dest], check=True, capture_output=True)
                        os.remove(tmp)
                        ok += 1
                        continue
            except Exception as e2:
                pass
            print(f'  cover fail {r["title"][:36]}: {e}')
        time.sleep(0.3)
    print(f'covers_3d: ok={ok} fail={fail}')

if __name__ == '__main__':
    main()
