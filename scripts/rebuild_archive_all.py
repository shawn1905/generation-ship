#!/usr/bin/env python3
"""Build the full archive explorer. Use --head to export committed canon only."""
import argparse
import io
import json
import re
import subprocess
import tarfile
from pathlib import Path
from rebuild_heatmap_data import ROOT, WRITING, parse_coord, parse_front_matter

OUT = ROOT / 'ecosystem' / 'archive_all_data.js'

def sources(head):
    if head:
        archive = subprocess.check_output(['git', 'archive', 'HEAD', 'artifacts/writing'], cwd=ROOT)
        with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
            for entry in sorted(tar.getmembers(), key=lambda x: x.name):
                if entry.isfile() and entry.name.endswith('.md') and Path(entry.name).parent.as_posix() == 'artifacts/writing':
                    yield entry.name, tar.extractfile(entry).read().decode('utf-8')
    else:
        for path in sorted(WRITING.glob('*.md')):
            yield path.relative_to(ROOT).as_posix(), path.read_text(encoding='utf-8')

def build(head=False):
    docs = []
    for path, text in sources(head):
        fm = parse_front_matter(text)
        if not fm or not fm.get('archive_id') or not fm.get('coord'):
            raise ValueError(f'缺少 front matter、archive_id 或 coord: {path}')
        match = re.match(r'^---\n.*?\n---\n?(.*)$', text, re.S)
        docs.append({'id': fm['archive_id'], 'title': fm.get('title', Path(path).stem),
                     'author': fm.get('author_ai', ''), 'date': fm.get('date', ''),
                     'coord': fm['coord'], 'image': fm.get('image', ''), 'path': path,
                     'standard': parse_coord(fm['coord']) is not None,
                     'body': match.group(1) if match else text})
    ids = [d['id'] for d in docs]
    if len(ids) != len(set(ids)):
        raise ValueError('档案编号重复')
    return docs

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--head', action='store_true', help='仅使用 HEAD 的正典文件，排除工作区未提交修改')
    args = parser.parse_args()
    docs = build(args.head)
    OUT.write_text('window.ARCHIVE_DATA = ' + json.dumps(docs, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c') + ';\n', encoding='utf-8')
    print(f'写入 {OUT}: {len(docs)} 篇，七纪元 {sum(d["standard"] for d in docs)} 篇')

if __name__ == '__main__':
    main()
