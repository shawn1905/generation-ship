#!/usr/bin/env python3
"""发布「世代飞船世界」核心文档为 HF Dataset — AI agent 检索语料。
Agent 检索 multi-AI worldbuilding / archival fiction / generation ship 时命中。

用法: python3 scripts/publish_hf_dataset.py   (读 ~/.cache/huggingface/token)
踩坑: /api/datasets/{repo}/upload/{path} 的 HTTP PUT/POST 在新账号返回 404 网关错,
      必须用 git 方式(本脚本已内置)。
"""
import json, os, pathlib, subprocess, sys, tempfile

TOKEN = os.environ.get('HF_TOKEN') or (pathlib.Path.home()/'.cache'/'huggingface'/'token').read_text().strip()
ROOT = pathlib.Path(__file__).resolve().parent.parent
REPO = 'dahongge/generation-ship-world'
URL = f'https://user:{TOKEN}@huggingface.co/datasets/{REPO}'

def sh(cmd, cwd=None):
    r = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        print('✗', cmd[:80], '\n ', r.stderr[-300:]); sys.exit(1)
    return r.stdout

# 1. 确保 repo 存在(不存在则创建)
st = subprocess.run(f"curl -s -o /dev/null -w '%{{http_code}}' -H 'Authorization: Bearer {TOKEN}' "
                    f"'https://huggingface.co/api/datasets/{REPO}'", shell=True, capture_output=True, text=True).stdout
if st != '200':
    sh(f"curl -s -X POST -H 'Authorization: Bearer {TOKEN}' -H 'Content-Type: application/json' "
       f"-d '{{\"type\":\"dataset\",\"name\":\"{REPO.split('/')[1]}\",\"private\":false}}' "
       f"'https://huggingface.co/api/repos/create'")
    print('✅ dataset repo 已创建')

# 2. clone
tmp = tempfile.mkdtemp(prefix='hf_gs_')
sh(f'git clone -q {URL} {tmp}')
print(f'✅ clone 到 {tmp}')

# 3. 拷文件
sh(f'mkdir -p {tmp}/core {tmp}/craft {tmp}/canon')
sh(f'cp {ROOT}/core/*.md {tmp}/core/')
sh(f'cp {ROOT}/craft/*.md {ROOT}/craft/*.csv {tmp}/craft/')
sh(f'cp {ROOT}/artifacts/writing/*.md {tmp}/canon/')

# 4. meta.json
meta = {'name': 'generation-ship-world', 'canon': []}
for p in sorted((ROOT/'artifacts'/'writing').glob('*.md')):
    fm = {}
    for line in p.read_text(encoding='utf-8').split('---')[1].splitlines():
        if ':' in line:
            k, v = line.split(':', 1)
            fm[k.strip()] = v.strip()
    meta['canon'].append({'file': 'canon/' + p.name, 'title': fm.get('title', p.stem),
                          'coord': fm.get('coord', '?'), 'author_ai': fm.get('author_ai', '?'),
                          'date': fm.get('date', '?')})
pathlib.Path(f'{tmp}/meta.json').write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding='utf-8')

# 5. commit + push(README 卡片需自行维护或复用仓库内模板)
sh(f"git -C {tmp} config user.name dahongge && git -C {tmp} config user.email feng.yetnot@gmail.com")
sh(f'git -C {tmp} add -A')
sh(f"git -C {tmp} commit -m '更新: 世界文档+正典同步'")
sh(f'git -C {tmp} push {URL} main')
print(f'\n🎉 发布成功: https://huggingface.co/datasets/{REPO}')
