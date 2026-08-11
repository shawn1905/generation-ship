#!/usr/bin/env python3
"""第二批:维基 REST API 拿 poster/thumbnail + 修正 SOM 源"""
import json, os, re, urllib.request

ROOT = os.path.join(os.path.dirname(__file__), '..')
COVER_DIR = os.path.join(ROOT, 'other', 'covers')
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'

def fetch(url, binary=False, timeout=30):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read() if binary else r.read().decode('utf-8', errors='replace')

def wiki_rest_thumb(title, size=600):
    api = 'https://en.wikipedia.org/api/rest_v1/page/summary/' + urllib.request.quote(title.replace(' ', '_'))
    try:
        d = json.loads(fetch(api))
        t = d.get('thumbnail') or d.get('originalimage')
        if t:
            return t['source'].replace('/thumb/', '/').split('/')[0] + t['source'].split('/')[0] and t['source'] or t['source']
    except Exception as e:
        print('  REST err:', e)
    return None

def fix_wiki_url(src, size=600):
    # 把维基缩略图 URL 改成指定宽度
    m = re.match(r'(https://upload\.wikimedia\.org/wikipedia/commons/thumb/.*?)/(\d+)px-(.*)$', src)
    if m:
        return f"{m.group(1)}/{size}px-{m.group(3)}"
    m = re.match(r'(https://upload\.wikimedia\.org/wikipedia/(?:commons|en)/[a-z0-9]/[a-z0-9]{2}/)([^/]+)$', src)
    if m:
        return f"{m.group(1)}{m.group(2)}"
    return src

PLAN = {
    'blame':              'Blame!',
    'wandering_earth':    'The Wandering Earth (film)',
    'archigram':          'Archigram',
    'ghost_in_the_shell': 'Ghost in the Shell',
    'the_martian':        'The Martian (film)',
    '2001_space_odyssey': '2001: A Space Odyssey (film)',
    'arrival':            'Arrival (film)',
    'som_mars_city':      'Mars habitat',   # 换维基源兜底
}

for slug, title in PLAN.items():
    out = os.path.join(COVER_DIR, slug + '.jpg')
    if os.path.exists(out) and os.path.getsize(out) > 5000:
        print(f'[skip] {slug}'); continue
    try:
        src = wiki_rest_thumb(title)
        if not src:
            print(f'[FAIL] {slug} REST 无图'); continue
        url = fix_wiki_url(src)
        data = fetch(url, binary=True)
        if len(data) < 5000:
            print(f'[FAIL] {slug} 过小({len(data)}B) src={url}'); continue
        with open(out, 'wb') as f:
            f.write(data)
        print(f'[OK]   {slug} <- {url[:100]} ({len(data)//1024}KB)')
    except Exception as e:
        print(f'[ERR]  {slug}: {e}')
