#!/usr/bin/env python3
"""事实锚点守卫 fact_anchor.py — 返工前后比对，确保正典事实锚点不丢失。

文学返工（注入物证钩子/留白/破模板/声音）允许改写文字，但**不得丢失或篡改
正典事实锚点**：档案互引编号(GS-XXXX-NN)、数字统计、年份日期。本工具在返工前
快照每篇的锚点集合，返工后比对，报告「丢失的锚点」，作为分形自洽的自动护栏。

用法:
  python3 scripts/fact_anchor.py snapshot --list FILELIST --out /tmp/anchor.json
  python3 scripts/fact_anchor.py verify   --list FILELIST --before /tmp/anchor.json
退出码(verify): 0=无锚点丢失, 1=有丢失
"""
import re, sys, json, os, glob

WRITING = 'artifacts/writing'


def body_of(raw):
    m = re.match(r'^---\n.*?\n---', raw, re.S)
    return raw[m.end():] if m else raw


def anchors(path):
    """提取一篇的事实锚点集合。"""
    if not os.path.exists(path):
        return None
    raw = open(path, encoding='utf-8', errors='replace').read()
    body = body_of(raw)
    a = set()
    # 档案互引编号
    a |= {'REF:' + m for m in re.findall(r'GS-\d{4}-\d{2}', body)}
    # 年份/日期（公元年、front matter date）
    a |= {'YR:' + m for m in re.findall(r'\b(\d{3,4})\b', body)}
    # 数字统计（含小数/百分号/千分位），归一化去逗号
    for m in re.findall(r'\d[\d,]*\.?\d*\s*%?', body):
        norm = m.replace(',', '').replace(' ', '')
        if norm.rstrip('%').replace('.', '').isdigit() and len(norm.rstrip('%')) >= 1:
            a.add('NUM:' + norm)
    return a


def resolve(name):
    if os.path.exists(name):
        return name
    g = glob.glob(f'{WRITING}/{name}')
    if g:
        return g[0]
    g = glob.glob(f'{WRITING}/*{name}*')
    return g[0] if g else None


def load_list(arg):
    if arg.endswith('.txt'):
        return [l.strip() for l in open(arg, encoding='utf-8') if l.strip()]
    return [arg]


def main():
    cmd = sys.argv[1]
    lst = sys.argv[sys.argv.index('--list') + 1]
    names = load_list(lst)
    if cmd == 'snapshot':
        out = sys.argv[sys.argv.index('--out') + 1]
        snap = {}
        for n in names:
            p = resolve(n)
            if p:
                snap[os.path.basename(p)] = sorted(anchors(p))
        json.dump(snap, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(f"快照 {len(snap)} 篇 → {out}")
    elif cmd == 'verify':
        before = sys.argv[sys.argv.index('--before') + 1]
        snap = json.load(open(before, encoding='utf-8'))
        lost_files = 0
        total_lost = 0
        for base, old in snap.items():
            p = resolve(base)
            if not p:
                print(f"  ✗ 文件消失: {base}")
                lost_files += 1
                continue
            new = anchors(p)
            missing = set(old) - set(new)
            # 只关注 REF 与 NUM/YR 丢失（锚点）
            missing = {m for m in missing if m.startswith(('REF:', 'NUM:', 'YR:'))}
            if missing:
                lost_files += 1
                total_lost += len(missing)
                show = sorted(missing)[:8]
                print(f"  ⚠ {base[:46]} 丢失{len(missing)}锚点: {show}")
        print(f"\n锚点守卫: {lost_files} 篇有丢失, 共 {total_lost} 个锚点。")
        sys.exit(1 if lost_files else 0)


if __name__ == '__main__':
    main()
