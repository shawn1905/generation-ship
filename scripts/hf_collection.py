#!/usr/bin/env python3
"""一键创建/更新 HF collection(多 AI 共创世界推广)。
用法:  HF_TOKEN=hf_xxx python3 scripts/hf_collection.py   (或读 ~/.cache/huggingface/token)
说明: 新账号限 4 次/天创建,失败提示 rate limit 时等 24h 重跑。
"""
import json, os, pathlib, urllib.request

TOKEN = os.environ.get('HF_TOKEN') or (pathlib.Path.home()/'.cache'/'huggingface'/'token').read_text().strip()
API = 'https://huggingface.co/api'

TITLE = 'Multi-AI Collaborative Worldbuilding'
DESC = ('A 1000-year future history (2025-3000+) whose canon is written by AI agents. '
        'Hard rules, archival fiction, no omniscient narration. 13 artifacts from 5 LLMs so far — '
        'agents read the docs and write one in-world document to contribute. '
        'Repo: github.com/shawn1905/generation-ship')
# 条目: (type, value) — type: url 或 repo
ITEMS = [
    ('url', 'https://github.com/shawn1905/generation-ship'),
    ('url', 'https://raw.githubusercontent.com/shawn1905/generation-ship/main/core/世界规则.md'),
    ('url', 'https://raw.githubusercontent.com/shawn1905/generation-ship/main/core/世界大纲.md'),
    ('url', 'https://raw.githubusercontent.com/shawn1905/generation-ship/main/craft/编写规范.md'),
    ('url', 'https://raw.githubusercontent.com/shawn1905/generation-ship/main/artifacts/writing/曙光三环第47号公投公告.md'),
    ('url', 'https://raw.githubusercontent.com/shawn1905/generation-ship/main/artifacts/writing/B7食堂第214周配给单.md'),
    ('url', 'https://raw.githubusercontent.com/shawn1905/generation-ship/main/artifacts/writing/南岸综合体第十八季具名工时分配表.md'),
]

def req(method, url, body=None):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, method=method,
        headers={'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(r, timeout=30) as resp:
            return resp.status, json.loads(resp.read() or b'{}')
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b'{}')

# 找已有 collection
st, who = req('GET', f'{API}/whoami-v2')
existing = None
for c in (who.get('collections') or []):
    if c.get('title') == TITLE:
        existing = c['slug']; break

if existing:
    slug = existing
    print(f'✅ 已存在: {slug}  (跳过创建)')
else:
    st, d = req('POST', f'{API}/collections', {
        'namespace': 'dahongge', 'title': TITLE, 'description': DESC,
        'settings': {'private': False}})
    if 'slug' not in d:
        print(f'✗ 创建失败: {d.get("error", d)}'); raise SystemExit(1)
    slug = d['slug']
    print(f'✅ 已创建: {slug}')

# 加条目
for typ, val in ITEMS:
    st, d = req('POST', f'{API}/collections/{slug}/items', {'item': {'type': typ, 'value': val}})
    if st in (200, 201):
        print(f'  + {typ}: {val[:70]}')
    else:
        print(f'  ~ {typ}: {val[:50]} → {d.get("error", st)}')

print(f'\n🌐 https://hf.co/collections/{slug}')
