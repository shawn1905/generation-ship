#!/usr/bin/env python3
"""下载 other/AI精选 封面：维基 API / Steam CDN / Goodreads / 官网 og:image"""
import json, os, re, subprocess, sys, urllib.request

ROOT = os.path.join(os.path.dirname(__file__), '..')
COVER_DIR = os.path.join(ROOT, 'other', 'covers')
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'

def fetch(url, binary=False, timeout=30):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read() if binary else r.read().decode('utf-8', errors='replace')

def wiki_thumb(title, size=600):
    api = 'https://en.wikipedia.org/w/api.php?action=query&titles=' + urllib.request.quote(title) \
        + f'&prop=pageimages&piprop=thumbnail&pithumbsize={size}&format=json&formatversion=2'
    d = json.loads(fetch(api))
    for p in d['query']['pages']:
        if 'thumbnail' in p:
            return p['thumbnail']['source']
    return None

def og_image(url):
    html = fetch(url)
    m = re.search(r'<meta[^>]*property=["\']og:image["\'][^>]*content=["\']([^"\']+)["\']', html, re.I)
    if not m:
        m = re.search(r'<meta[^>]*content=["\']([^"\']+)["\'][^>]*property=["\']og:image["\']', html, re.I)
    return m.group(1) if m else None

def goodreads_og(book_id):
    return og_image(f'https://www.goodreads.com/book/show/{book_id}')

# slug -> 来源定义
PLAN = {
    'blame':              ('wiki', 'Blame!'),
    'dyson_sphere_program': ('url', 'https://cdn.akamai.steamstatic.com/steam/apps/1366540/header.jpg'),
    'wandering_earth':    ('wiki', 'The Wandering Earth (film)'),
    'syd_mead':           ('wiki', 'Syd Mead'),
    'archigram':          ('wiki', 'Archigram'),
    'ghost_in_the_shell': ('wiki', 'Ghost in the Shell'),
    'soma':               ('url', 'https://cdn.akamai.steamstatic.com/steam/apps/282140/header.jpg'),
    'the_martian':        ('wiki', 'The Martian (film)'),
    'mars_science_city':  ('url', 'https://images.adsttc.com/media/images/59cb/ba4b/b22e/383c/4000/0035/newsletter/Mars_Science_City2.jpg?1506523718'),
    'project_hail_mary':  ('goodreads', '54493401'),
    '2001_space_odyssey': ('wiki', '2001: A Space Odyssey (film)'),
    'arrival':            ('wiki', 'Arrival (film)'),
    'de_extinction':      ('wiki', 'De-extinction'),
    'ocean_spiral':       ('url', 'https://www.shimz.co.jp/topics/dream/images/img_list_01.jpg'),
    'ligo':               ('wiki', 'LIGO'),
    'music_for_airports': ('wiki', 'Brian Eno'),
    'ex_machina':         ('url', 'https://upload.wikimedia.org/wikipedia/en/b/ba/Ex-machina-uk-poster.jpg'),
    'james_webb':         ('wiki', 'James Webb Space Telescope'),
    'svalbard_seed_vault': ('wiki', 'Svalbard Global Seed Vault'),
    # 社区深挖 · 小众独立
    'voices_of_the_void': ('web', 'https://mrdrnose.itch.io/votv'),
    'citizen_sleeper':    ('url', 'https://cdn.akamai.steamstatic.com/steam/apps/1134650/header.jpg'),
    'in_other_waters':    ('url', 'https://cdn.akamai.steamstatic.com/steam/apps/1140500/header.jpg'),
    'signalis':           ('url', 'https://cdn.akamai.steamstatic.com/steam/apps/1542350/header.jpg'),
    'outer_wilds':        ('url', 'https://cdn.akamai.steamstatic.com/steam/apps/753640/header.jpg'),
    'sable':              ('url', 'https://cdn.akamai.steamstatic.com/steam/apps/1150690/header.jpg'),
    'world_of_tomorrow':  ('url', 'https://upload.wikimedia.org/wikipedia/en/c/c1/World_of_Tomorrow_%28film%29_POSTER.jpg'),
    'scavengers_reign':   ('url', 'https://upload.wikimedia.org/wikipedia/en/0/0c/Scavengers_Reign.png'),
    # 8-14 第三批 · 更深一层
    'tabbys_star':        ('wiki', "Tabby's Star"),
    'naissancee':         ('url', 'https://cdn.akamai.steamstatic.com/steam/apps/265690/header.jpg'),
    'kaiba':              ('url', 'https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx3701-ooD3N9dD2rqa.jpg'),
    'rendezvous_with_rama': ('web', 'https://en.wikipedia.org/wiki/Rendezvous_with_Rama'),
    'melodysheep_timelapse': ('url', 'https://i.ytimg.com/vi/uD4izuDMUQA/maxresdefault.jpg'),
    'the_line':           ('url', 'https://www.neom.com/content/dam/neom/theline/hero/line-hero-thumbnail-new.jpg'),
    'project_orion':      ('wiki', 'Project Orion (nuclear propulsion)'),
    'exhalation':         ('goodreads', '41160292'),
}

os.makedirs(COVER_DIR, exist_ok=True)
for slug, (kind, val) in PLAN.items():
    out = os.path.join(COVER_DIR, slug + '.jpg')
    if os.path.exists(out) and os.path.getsize(out) > 5000:
        print(f'[skip] {slug} 已有'); continue
    try:
        if kind == 'wiki':
            src = wiki_thumb(val)
        elif kind == 'url':
            src = val
        elif kind == 'goodreads':
            src = goodreads_og(val)
        else:
            src = og_image(val)
        if not src:
            print(f'[FAIL] {slug} 未找到图片源'); continue
        data = fetch(src, binary=True)
        if len(data) < 5000:
            print(f'[FAIL] {slug} 图片过小({len(data)}B)'); continue
        with open(out, 'wb') as f:
            f.write(data)
        print(f'[OK]   {slug} <- {src[:90]} ({len(data)//1024}KB)')
    except Exception as e:
        print(f'[ERR]  {slug}: {e}')
