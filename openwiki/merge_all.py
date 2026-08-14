#!/usr/bin/env python3
"""openwiki/ALL.md 聚合器 — 把 openwiki/ 下所有页面拼成一个 agent 友好的全文文件。"""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'ALL.md')

files = []
for root, _dirs, fs in os.walk(ROOT):
    for f in sorted(fs):
        if f.endswith('.md') and f != 'ALL.md':
            files.append(os.path.join(root, f))
files.sort()

parts = [
    "# Generation Ship Wiki — 聚合全文（Agent 专用）",
    "",
    "> 本文件由 openwiki/ 所有页面聚合而成（openwiki/merge_all.py 生成），供 agent 一次性读取。",
    "> 单页版本见各子目录。入口导航：index.md / quickstart.md",
    "> 维护：跑 `bash docs/openwiki_update.sh` 手动更新并重新聚合",
    "",
]

for fp in files:
    rel = os.path.relpath(fp, ROOT)
    content = open(fp, encoding='utf-8').read()
    parts.append(f"\n\n---\n\n<!-- 来源: {rel} -->\n\n" + content)

with open(OUT, 'w', encoding='utf-8') as f:
    f.write('\n'.join(parts))

print(f"ALL.md 生成: {os.path.getsize(OUT)//1024} KB, {len(files)} 个源文件")
