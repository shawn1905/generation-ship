#!/usr/bin/env python3
"""修补动漫/漫画数据：灵笼、铁血孤儿主TV、Prophet/Letter 44/Aama 维基词条直取"""
import csv, json, os, re, urllib.parse, urllib.request

ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
UA = {'User-Agent': 'generation-ship/1.0 (by shawn1905)'}
norm = lambda s: re.sub(r'[^a-z0-9]', '', s.lower())

def anilist_id(mid):
    q = '''query($id:Int){Media(id:$id){id title{romaji english} averageScore popularity startDate{year} coverImage{large} genres format siteUrl}}'''
    body = json.dumps({'query': q, 'variables': {'id': mid}}).encode()
    req = urllib.request.Request('https://graphql.anilist.co', data=body,
        headers={'Content-Type': 'application/json', **UA})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)['data']['Media']

def wiki_titles(title):
    api = 'https://en.wikipedia.org/w/api.php'
    params = urllib.parse.urlencode({'action': 'query', 'titles': title,
        'prop': 'pageimages|extracts', 'exintro': 1, 'explaintext': 1,
        'pithumbsize': 460, 'format': 'json'})
    req = urllib.request.Request(f'{api}?{params}', headers=UA)
    with urllib.request.urlopen(req, timeout=20) as r:
        d = json.load(r)
    pages = (d.get('query') or {}).get('pages') or {}
    for p in pages.values():
        if 'missing' in p:
            return None
        return {'title': p.get('title', title),
                'cover': (p.get('thumbnail') or {}).get('source') or '',
                'desc': (p.get('extract') or '')[:120],
                'url': f"https://en.wikipedia.org/wiki/{urllib.parse.quote(p['title'].replace(' ', '_'))}"}

def to_row(m, name, tags, ship, note, kind):
    return {'title': m['title'].get('english') or m['title'].get('romaji') or name,
            'search_name': name, 'year': (m.get('startDate') or {}).get('year') or '',
            'source': 'anilist', 'source_id': m.get('id', ''), 'score': m.get('averageScore') or '',
            'popularity': m.get('popularity') or '', 'genres': ','.join(m.get('genres') or []),
            'format': m.get('format') or '', 'cover_img': (m.get('coverImage') or {}).get('large') or '',
            'url': m.get('siteUrl') or '', 'tags': tags, 'ship_ref': ship, 'note': note,
            'desc': '', 'kind': kind}

FIELDS = ['title', 'search_name', 'year', 'source', 'source_id', 'score', 'popularity',
          'genres', 'format', 'cover_img', 'url', 'tags', 'ship_ref', 'note', 'desc', 'kind']

def load(p):
    return list(csv.DictReader(open(p)))

def save(p, rows):
    with open(p, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)

def main():
    ap = os.path.join(ROOT, 'branch', 'anime', 'scifi_anime_curated.csv')
    cp = os.path.join(ROOT, 'branch', 'comics', 'scifi_comics_curated.csv')

    # 1) 灵笼：AniList Ling Long (id 110459)
    m = anilist_id(110459)
    linglong = to_row(m, 'Ling Long', '末世|方舟|中国', 3, '灵笼：灯塔方舟+生态循环', 'anime')
    linglong['title'] = '灵笼 (Ling Long)'

    # 2) 铁血孤儿：主 TV（2015，format TV）
    import time
    q = '''query($s:String){Page(perPage:8){media(search:$s,type:ANIME){id title{romaji english} averageScore popularity startDate{year} coverImage{large} genres format siteUrl}}}'''
    body = json.dumps({'query': q, 'variables': {'s': 'Mobile Suit Gundam: Iron-Blooded Orphans'}}).encode()
    req = urllib.request.Request('https://graphilist.co'.replace('graphilist', 'graphql.anilist'), data=body,
        headers={'Content-Type': 'application/json', **UA})
    with urllib.request.urlopen(req, timeout=20) as r:
        cands = json.load(r)['data']['Page']['media']
    tv = [c for c in cands if c.get('format') == 'TV' and (c.get('startDate') or {}).get('year') == 2015]
    ibo = to_row(tv[0], 'Mobile Suit Gundam: Iron-Blooded Orphans', '军事科幻|机甲|战争', 1, '高达铁血孤儿（主TV）', 'anime') if tv else None

    # 3-5) 维基词条直取（Prophet 有词条；Letter 44 / Aâma 英文维基无词条 → 手写）
    fixes = {
        'Prophet (comics)': ('生物朋克|太空|史诗', 2, 'Prophet：超时空生物朋克'),
    }
    wiki_rows = {}
    for t, (tags, ship, note) in fixes.items():
        w = wiki_titles(t)
        if w:
            wiki_rows[t] = {'title': w['title'], 'search_name': t, 'year': '', 'source': 'wikipedia',
                'source_id': '', 'score': '', 'popularity': '', 'genres': '', 'format': 'Graphic Novel',
                'cover_img': w['cover'], 'url': w['url'], 'tags': tags, 'ship_ref': ship,
                'note': note, 'desc': w['desc'], 'kind': 'comic'}
        else:
            print(f'  wiki missing: {t}')

    # 手写条目（英文维基无词条，诚实标注无外部数据）
    manual = {
        'Letter 44': ('硬科幻|太空政治|近未来', 3, 'Letter 44：小行星带飞船+白宫双线（英文维基无词条，数据手写）'),
        'Aama': ('硬科幻|记忆|太空', 1, 'Aama：法式硬科幻（英文维基无词条，数据手写）'),
    }
    for t, (tags, ship, note) in manual.items():
        wiki_rows[t] = {'title': t, 'search_name': t, 'year': '', 'source': 'manual',
            'source_id': '', 'score': '', 'popularity': '', 'genres': '', 'format': 'Graphic Novel',
            'cover_img': '', 'url': '', 'tags': tags, 'ship_ref': ship, 'note': note,
            'desc': '', 'kind': 'comic'}

    # ---- 更新 anime CSV：去 Urdr 错配，补灵笼 + IBO 主TV ----
    arows = load(ap)
    arows = [r for r in arows if 'Urdr' not in r['title']]
    if linglong:
        arows.append(linglong)
    if ibo:
        arows.append(ibo)
    save(ap, arows)
    print(f'anime updated: {len(arows)}')

    # ---- 更新 comics CSV：替换 Prophet/Letter 44/Aama ----
    crows = load(cp)
    drop = {'Prophet (character)', 'DC Comics', 'Frederik Peeters', 'Private Eye'}
    crows = [r for r in crows if r['title'] not in drop]
    for r in wiki_rows.values():
        # 若已存在同 search_name 则替换
        crows = [x for x in crows if x.get('search_name') != r['search_name']]
        crows.append(r)
    save(cp, crows)
    print(f'comics updated: {len(crows)}')
    for r in crows:
        print(f"  {r['year'] or '--':>4}  {str(r['score']):>4}  {r['title'][:46]} [{r['source']}]")

if __name__ == '__main__':
    main()
