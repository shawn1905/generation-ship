#!/usr/bin/env python3
"""正典体检器 canon_health.py — 文学/红线/工艺卫生维度（补足 check_submission.py 的结构校验）。

用法:
    python3 scripts/canon_health.py            # 全库体检，打印汇总 + 写报告
    python3 scripts/canon_health.py --json OUT # 额外输出机器可读工作清单

检查维度（非破坏性，只读）:
  红线  金手指(冬眠/室温超导/超光速-正面/意识上传/FTL) · 英雄化叙事 · 回望叙述 · 纪元名渗入正文
  工艺  front matter 图片路径断裂 · 有image字段但正文未嵌图 · 图片目标不存在 · 懒canon_check · ASCII框线字符画
  文本  完全重复段(刷屏) · 行内自我重复句(残句)
退出码: 0=无红线, 1=存在红线级问题(工艺/文本问题只报告不置错)
"""
import re, sys, os, json, pathlib, collections, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
WRITING = ROOT / 'artifacts' / 'writing'

# 金手指黑名单：命中即红线，但排除否定/辟谣语境
GOLDFINGER = {
    '冬眠': r'冬眠|冷冻睡眠|低温休眠',
    '室温超导': r'室温超导',
    '意识上传': r'意识上传|心智上传|数字永生',
    'FTL/超光速': r'超光速|曲率引擎|曲率驱动|跃迁引擎| faster-than-light|\bFTL\b',
}
# 否定/辟谣前缀语境：出现这些词视为合规（明确声明不存在/辟谣）
NEG_CTX = r'(无|禁|非|没有|不|取消|废除|辟谣|误解|传言|误传|谣言|否定|不存在|尚无|未实现|拒绝|反对)'

HERO = r'传奇|英雄称号|名人堂|最伟大|天选|救世主|扬名立万|封神|力挽狂澜|凭一己之力'
RETRO = r'多年以后|多年后人们|后来人们才|后世才知道|事后回看|回过头来看才'
ERA_LEAK = r'(替代|竞赛|丰裕|离心|启航|落地|双星系)纪元'
ASCII_BOX = r'[┌┐└┘├┤┬┴─│═╔╗╚╝║╠╣╦╩╬]'


def parse(raw):
    m = re.match(r'^---\n(.*?)\n---', raw, re.S)
    if not m:
        return '', raw
    return m.group(1), raw[m.end():]


def fm_get(fm, key):
    m = re.search(rf'^{key}:\s*(.+)$', fm, re.M)
    return m.group(1).strip() if m else None


def goldfinger_hits(body):
    out = []
    for name, rx in GOLDFINGER.items():
        for m in re.finditer(rx, body):
            s = max(0, m.start() - 12)
            ctx = body[s:m.end() + 8]
            # 否定语境过滤
            pre = body[max(0, m.start() - 6):m.start()]
            if re.search(NEG_CTX, pre) or re.search(NEG_CTX + r'[^。；\n]{0,4}$', ctx[:len(ctx)]):
                continue
            # 明确辟谣句过滤
            if re.search(NEG_CTX, ctx):
                continue
            out.append((name, ctx.replace('\n', ' ')))
    return out


def dup_paragraphs(body):
    paras = [re.sub(r'\s+', '', p) for p in re.split(r'\n\s*\n', body)]
    paras = [p for p in paras if len(p) >= 20 and not p.startswith('![') and not p.startswith('#')]
    c = collections.Counter(paras)
    return [(p[:40], n) for p, n in c.items() if n >= 2]


def selfdup_line(body):
    hits = []
    for line in body.splitlines():
        for m in re.finditer(r'([^。；，\n]{10,24})[。；，][^。；，\n]*?\1', line):
            hits.append(m.group(1)[:24])
    return hits


def main():
    files = sorted(WRITING.glob('*.md'))
    report = collections.defaultdict(list)
    stats = collections.Counter()
    json_rows = []

    for p in files:
        if p.name in ('README.md', 'TEMPLATE.md'):
            continue
        raw = p.read_text(encoding='utf-8', errors='replace')
        fm, body = parse(raw)
        base = p.name

        # --- 红线 ---
        gf = goldfinger_hits(body)
        if gf:
            report['红线·金手指'].append((base, gf[:3]))
            stats['红线·金手指'] += 1
        if re.search(HERO, body) or re.search(HERO, base):
            report['红线·英雄化(需复核)'].append((base, re.findall(HERO, body + base)[:4]))
            stats['红线·英雄化(需复核)'] += 1
        if re.search(RETRO, body):
            report['红线·回望叙述'].append((base, re.findall(RETRO, body)[:2]))
            stats['红线·回望叙述'] += 1
        if re.search(ERA_LEAK, body):
            report['红线·纪元名渗入正文'].append((base, re.findall(ERA_LEAK, body)[:2]))
            stats['红线·纪元名渗入正文'] += 1

        # --- 工艺 ---
        img = fm_get(fm, 'image')
        if img:
            if img.startswith('world/') or (not img.startswith('../') and not img.startswith('http')):
                report['工艺·图片路径断裂(缺../../)'].append((base, img))
                stats['工艺·图片路径断裂(缺../../)'] += 1
            # 目标是否存在
            tgt = (p.parent / img).resolve() if not img.startswith('http') else None
            if tgt is not None and not tgt.exists():
                # 尝试 ../../ 修正后再判
                alt = (p.parent / ('../../' + img if img.startswith('world/') else img)).resolve()
                if not alt.exists():
                    report['工艺·图片目标不存在'].append((base, img))
                    stats['工艺·图片目标不存在'] += 1
            if '![' not in body:
                report['工艺·有image字段但正文未嵌图'].append((base, img))
                stats['工艺·有image字段但正文未嵌图'] += 1
        cc = fm_get(fm, 'canon_check')
        if cc and len(cc) <= 6:
            report['工艺·懒canon_check(<=6字)'].append((base, cc))
            stats['工艺·懒canon_check(<=6字)'] += 1
        if re.search(ASCII_BOX, body):
            report['工艺·ASCII框线字符画'].append((base, ''))
            stats['工艺·ASCII框线字符画'] += 1

        # --- 文本 ---
        dp = dup_paragraphs(body)
        if dp:
            report['文本·完全重复段(刷屏)'].append((base, dp[:3]))
            stats['文本·完全重复段(刷屏)'] += 1
        sd = selfdup_line(body)
        if sd:
            report['文本·行内自我重复句(残句)'].append((base, sd[:3]))
            stats['文本·行内自我重复句(残句)'] += 1

        row = {'file': base}
        for k in report:
            if report[k] and report[k][-1][0] == base:
                row[k] = report[k][-1][1]
        if len(row) > 1:
            json_rows.append(row)

    # --- 汇总 ---
    print(f"正典体检 · {len(files)} 篇 · {datetime.date.today()}")
    print('=' * 60)
    order = ['红线·金手指', '红线·英雄化(需复核)', '红线·回望叙述', '红线·纪元名渗入正文',
             '工艺·图片路径断裂(缺../../)', '工艺·图片目标不存在', '工艺·有image字段但正文未嵌图',
             '工艺·懒canon_check(<=6字)', '工艺·ASCII框线字符画',
             '文本·完全重复段(刷屏)', '文本·行内自我重复句(残句)']
    redline = 0
    for k in order:
        n = stats.get(k, 0)
        tag = '🔴' if k.startswith('红线') else ('🟠' if k.startswith('工艺') else '🟡')
        print(f"  {tag} {n:5d}  {k}")
        if k.startswith('红线'):
            redline += n

    # 写 markdown 报告
    outdir = ROOT / 'artifacts'
    md = outdir / f'正典体检报告_{datetime.date.today():%Y%m%d}.md'
    with md.open('w', encoding='utf-8') as f:
        f.write(f"# 正典体检报告 · {datetime.date.today()}\n\n")
        f.write(f"扫描 {len(files)} 篇正典。红线级问题合计 {redline} 处。\n\n")
        for k in order:
            items = report.get(k, [])
            if not items:
                continue
            f.write(f"## {k}（{len(items)} 篇）\n\n")
            for base, detail in items:
                f.write(f"- `{base}` — {detail}\n")
            f.write('\n')
    print('=' * 60)
    print(f"报告已写入: {md.relative_to(ROOT)}")

    if '--json' in sys.argv:
        out = sys.argv[sys.argv.index('--json') + 1]
        pathlib.Path(out).write_text(json.dumps(json_rows, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f"工作清单(JSON): {out}  共 {len(json_rows)} 篇待处理")

    sys.exit(1 if redline else 0)


if __name__ == '__main__':
    main()
