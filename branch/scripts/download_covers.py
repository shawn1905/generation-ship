import json
#!/usr/bin/env python3
"""下载动漫/漫画封面：AniList cover + 维基 REST summary thumbnail"""
import csv, os, re, time, urllib.request, urllib.parse

ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
UA = {'User-Agent': 'generation-ship/1.0 (by shawn1905)'}

def wiki_thumb(title):
    """REST summary 拿条目图（处理 429）"""
    t = title.replace(' ', '_')
    for attempt in range(4):
        try:
            req = urllib.request.Request('https://en.wikipedia.org/api/rest_v1/page/summary/' + urllib.parse.quote(t), headers=UA)
            with urllib.request.urlopen(req, timeout=15) as r:
                d = json.load(r)
            return (d.get('thumbnail') or {}).get('source', '')
        except Exception as e:
            if '429' in str(e) and attempt < 3:
                time.sleep(20 + attempt * 15)
            elif '404' in str(e):
                return ''
            else:
                time.sleep(5)
    return ''

def fetch(url, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 2000:
        return 'cached'
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=25) as r:
        data = r.read()
    if len(data) < 2000:
        return 'too-small'
    open(dest, 'wb').write(data)
    return 'ok'

def run(csvf, outdir):
    d = os.path.join(ROOT, outdir)
    os.makedirs(d, exist_ok=True)
    rows = list(csv.DictReader(open(os.path.join(ROOT, csvf))))
    ok = fail = 0
    for r in rows:
        url = r.get('cover_img') or ''
        if not url and r.get('source') == 'wikipedia':
            url = wiki_thumb(r['title'])
            if url:
                r['cover_img'] = url  # 回写
        if not url:
            fail += 1
            print(f'  no url: {r["title"]}')
            continue
        key = r.get('source_id') or r.get('title')
        slug = re.sub(r'[^a-z0-9]+', '_', str(key).lower()).strip('_') + '.jpg'
        dest = os.path.join(d, slug)
        try:
            st = fetch(url, dest)
        except Exception as e:
            st = f'err:{e}'
        if st in ('ok', 'cached'):
            ok += 1
        else:
            fail += 1
            print(f'  fail {r["title"]}: {st}')
        time.sleep(0.5)
    print(f'{outdir}: ok={ok} fail={fail}')
    # 回写 cover_img（维基补图）
    with open(os.path.join(ROOT, csvf), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)

if __name__ == '__main__':
    run('branch/comics/scifi_comics_curated.csv', 'branch/comics/covers')
