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
    'som_mars_city':      ('web', 'https://www.som.com/projects/mars-science-city/'),
    'project_hail_mary':  ('goodreads', '54493401'),
    '2001_space_odyssey': ('wiki', '2001: A Space Odyssey (film)'),
    'arrival':            ('wiki', 'Arrival (film)'),
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
