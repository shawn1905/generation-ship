#!/usr/bin/env python3
"""修复手工清单: 4 个失效 ArtStation 链接换新 + 15 位无图艺术家补封面。

封面来源优先级:
  1. ArtStation projects.json(过 Cloudflare 后)拿第一件作品 cover
  2. 艺术家官网 og:image(craig-mullins / paulchadeisson / waynebarlowe 等)
  3. 第三方介绍页第一张图(CDR 的 Ian McQue 页)
"""
import csv, os, re, subprocess, time, urllib.request, json

ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
OUT = os.path.join(ROOT, 'branch', 'art')
COVERS = os.path.join(OUT, 'covers')
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/125 Safari/537.36'

# (艺术家名, 新链接, 封面来源)  — 链接修复 + 封面来源
FIX = {
    'Jama Jurabaev':  ('https://www.artstation.com/jama', 'as:jama'),
    'Maciej Kuciara': ('https://www.artstation.com/maciej', 'as:maciej'),
    'Ian McQue':      ('https://www.characterdesignreferences.com/artists-of-the-week/ian-mcque', 'og'),
    'Paul Chadeisson':('https://paulchadeisson.com/', 'og'),
}
# 纯补封面(链接不变)
COVER_ONLY = {
    'Ryan Church':    ('https://www.artstation.com/ryanchurch', 'as:ryanchurch'),
    'George Hull':    ('https://www.artstation.com/georgehull', 'as:georgehull'),
    'Sparth':         ('https://www.artstation.com/sparth', 'as:sparth'),
    'Nicolas Bouvier':('https://www.artstation.com/nicolasbouvier', 'as:nicolasbouvier'),
    'Ben Mauro':      ('https://www.artstation.com/benmauro', 'as:benmauro'),
    'Aaron Beck':     ('https://www.artstation.com/aaronbeck', 'as:aaronbeck'),
    'Craig Mullins':  ('https://craig-mullins.com/', 'og'),
    'Ash Thorp':      ('https://ashthorp.com/', 'og'),
    'Wayne Barlowe':  ('https://waynebarlowe.com/', 'og'),
    'John Harris':    ('https://www.johnharrisart.com/', 'og'),
}
ALL = {**FIX, **COVER_ONLY}

def slug(name):
    return re.sub(r'[^a-z0-9]+', '_', name.lower()).strip('_')

def dl(url, dest, retries=2):
    for i in range(retries):
        try:
            subprocess.run(['curl', '-s', '-L', '-m', '30', '-A', UA, url, '-o', dest + '.tmp'],
                           check=True, capture_output=True, timeout=40)
            if os.path.exists(dest + '.tmp') and os.path.getsize(dest + '.tmp') > 3000:
                subprocess.run(['sips', '-Z', '500', dest + '.tmp', '--out', dest], check=True, capture_output=True)
                os.remove(dest + '.tmp')
                return True
        except Exception:
            time.sleep(1)
    return False

def as_cover(username):
    """ArtStation projects.json → 第一件作品 cover(需先过 Cloudflare)"""
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            b = p.chromium.launch(headless=True)
            ctx = b.new_context(user_agent=UA)
            pg = ctx.new_page()
            pg.goto('https://www.artstation.com/', timeout=25000, wait_until='domcontentloaded')
            for _ in range(15):
                pg.wait_for_timeout(1000)
                if 'Just a moment' not in pg.title(): break
            resp = ctx.request.get(f'https://www.artstation.com/users/{username}/projects.json?page=1')
            if resp.status != 200:
                return ''
            data = resp.json()
            for it in data.get('data', []):
                cover = (it.get('cover') or {}).get('small_square_url') or (it.get('cover') or {}).get('medium_url') or ''
                if cover:
                    return cover
            b.close()
            return ''
    except Exception as e:
        print(f'  AS {username} ERR: {str(e)[:50]}')
        return ''

def og_image(url):
    try:
        subprocess.run(['curl', '-s', '-L', '-m', '20', '-A', UA, url, '-o', '/tmp/og.html'], check=True, capture_output=True, timeout=30)
        html = open('/tmp/og.html', encoding='utf-8', errors='ignore').read()
        m = re.search(r'property="og:image" content="([^"]+)"', html)
        return m.group(1) if m else ''
    except Exception:
        return ''

def main():
    os.makedirs(COVERS, exist_ok=True)
    results = {}
    for name, (link, src) in ALL.items():
        dest = os.path.join(COVERS, slug(name) + '.jpg')
        if os.path.exists(dest) and os.path.getsize(dest) > 3000:
            results[name] = '已有图'
            continue
        url = ''
        if src.startswith('as:'):
            url = as_cover(src[3:])
        elif src == 'og':
            url = og_image(link)
        if not url:
            print(f'  ✗ {name}: 无封面源')
            continue
        if dl(url, dest):
            results[name] = f'✓ {url[:60]}'
        else:
            results[name] = '✗ 下载失败'
        time.sleep(0.5)
    for k, v in results.items():
        print(f'{k:18} {v}')

if __name__ == '__main__':
    main()
