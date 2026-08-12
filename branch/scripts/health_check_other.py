#!/usr/bin/env python3
"""other/AI精选 健康巡检:CSV 列数 / URL 可达 / 封面存在。每次扩充后必跑。"""
import csv, os, sys, urllib.request, urllib.error

ROOT = os.path.join(os.path.dirname(__file__), '..')

rows = list(csv.reader(open(os.path.join(ROOT, 'other', 'ai_curated.csv'), encoding='utf-8')))
bad_cols, missing, dead = [], [], []
for row in rows[1:]:
    if len(row) != 9:
        bad_cols.append((row[0][:15], len(row)))
        continue
    slug, url = row[8], row[7]
    cov = os.path.join(ROOT, 'other', 'covers', slug + '.jpg')
    if not os.path.exists(cov) or os.path.getsize(cov) < 5000:
        missing.append(slug)
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh) Chrome/126.0'})
        code = urllib.request.urlopen(req, timeout=12).status
    except urllib.error.HTTPError as e:
        code = e.code
    except Exception as e:
        code = type(e).__name__
    if code != 200:
        dead.append((slug, code, url))

print(f'共 {len(rows)-1} 条')
print(f'列错位: {bad_cols or "无"}')
print(f'缺封面: {missing or "无"}')
print(f'不可达: {dead or "无"}')
sys.exit(1 if (bad_cols or missing or dead) else 0)
