#!/usr/bin/env python3
"""正典文字质感诊断器 canon_texture.py — P2 文学层定位工具（只读，不改文件）。

目标：在「合规但扁平」的多数篇章里，量化定位最该做文学优化的方阵，把有限的
返工精力投到刀刃上。不评判合法性（那是 check_submission/canon_health 的事），
只评判「文字质感」——是否物证侧写、是否留白、是否破模板、是否有声音。

四个维度（各 0—25 分，合 100；分越低越扁平）:
  物证钩子 EVIDENCE：具体可触的档案物证词密度（签名/涂改/考勤/工单/台账/存根/封条/磨损/手书/签认…）
  留白      RESTRAINT：过度解释标记（因为/所以/这意味着/旨在/目的是/也就是说）越少越好
  破模板    ANTIFORM ：开篇骨架是否落入通用模板（## 一、系统概述/建档缘由/事件概况/立法缘由/总则…）
  声音      VOICE    ：句长变化 + 世界内第一人称/署名/口语残留 + 非匀质节奏

用法:
  python3 scripts/canon_texture.py            # 汇总 + 最扁平方阵 Top N
  python3 scripts/canon_texture.py --top 40   # 指定数量
  python3 scripts/canon_texture.py --csv OUT  # 导出全量评分
"""
import re, sys, glob, os, statistics, collections

WRITING = 'artifacts/writing'

# 具体物证词（越具体越好：一张纸、一个签名、一处磨损）
EVIDENCE = r'(签名|签认|签章|签字|涂改|描红|指纹|手印|考勤|打卡|值班表|排班|工单|台账|存根|回执|批注|批文|封条|火漆|骑缝|编号|手书|亲笔|勾选|划痕|磨损|污渍|油渍|咖啡|折痕|装订|归档号|卷宗|名册|清册|登记簿|体检|处方|病历|化验|读数|仪表|计数|磅单|过秤|领用|交接单|钥匙|门禁|工牌|饭票|配给券)'
# 过度解释标记（讲满讲透=不留白）
OVEREXPLAIN = r'(因为|所以|因此|从而|这意味着|也就是说|换言之|旨在|目的是|为了表明|由此可见|不难看出|众所周知|值得一提的是|需要指出的是|综上所述|总而言之)'
# 通用模板开篇骨架
TEMPLATE_HEADS = ('一、系统概述', '一、建档缘由', '一、事件概况', '一、事件概述', '一、事件概要',
                  '一、立法缘由', '一、设立缘由', '一、决算范围', '一、决算概况', '一、基本登记',
                  '一、总则', '第一章 总则', '一、背景', '一、概述', '一、概况', '一、缘起')
# 世界内声音痕迹（第一人称/署名/口语/岗位腔）
VOICE = r'(本人|我方|我处|兹|谨|查|奉|窃|职|卑职|经办人|值班员|记录人|签名略|（略）|照准|准此|此令|此复|合行|为荷|勿此|特此)'


def body_of(raw):
    m = re.match(r'^---\n.*?\n---', raw, re.S)
    return raw[m.end():] if m else raw


def score(path):
    raw = open(path, encoding='utf-8', errors='replace').read()
    body = body_of(raw)
    text = re.sub(r'\s+', '', body)
    n = max(len(text), 1)

    # 物证钩子：密度（每千字命中数），封顶 25
    ev = len(re.findall(EVIDENCE, body))
    ev_score = min(25, round(ev / n * 1000 * 2.2))

    # 留白：过度解释密度越低越好
    ox = len(re.findall(OVEREXPLAIN, body))
    ox_rate = ox / n * 1000
    re_score = max(0, round(25 - ox_rate * 6))

    # 破模板：首个标题是否落入通用模板
    heads = [l.strip() for l in body.splitlines() if l.strip().startswith('#')]
    first = heads[0].lstrip('#').strip() if heads else ''
    af_score = 8 if any(first.startswith(t.split('、')[-1]) or t in first for t in TEMPLATE_HEADS) else 25
    # 若通篇章节标题高度雷同（一二三…+概述类），再扣
    if len(heads) >= 6 and sum(1 for h in heads if re.search(r'概述|概况|缘起|背景|总则|说明|附则', h)) >= max(3, len(heads) // 2):
        af_score = max(4, af_score - 8)

    # 声音：句长方差 + 世界内腔调命中
    sents = [s for s in re.split(r'[。；！？]', body) if 4 < len(s.strip()) < 200]
    if len(sents) >= 4:
        lens = [len(re.sub(r'\s', '', s)) for s in sents]
        cv = statistics.pstdev(lens) / (statistics.mean(lens) or 1)  # 变异系数
        var_score = min(13, round(cv * 22))
    else:
        var_score = 4
    vc = len(re.findall(VOICE, body))
    voice_score = min(12, vc * 2) + var_score
    voice_score = min(25, voice_score)

    total = ev_score + re_score + af_score + voice_score
    return {'file': os.path.basename(path), 'total': total,
            'ev': ev_score, 're': re_score, 'af': af_score, 'vo': voice_score,
            'chars': n, 'heads': len(heads)}


def main():
    files = sorted(glob.glob(f'{WRITING}/*.md'))
    rows = [score(f) for f in files]
    rows = [r for r in rows if r['chars'] >= 300]
    rows.sort(key=lambda r: r['total'])

    top = 25
    if '--top' in sys.argv:
        top = int(sys.argv[sys.argv.index('--top') + 1])

    totals = [r['total'] for r in rows]
    print(f"文字质感诊断 · 有效 {len(rows)} 篇")
    print('=' * 66)
    print(f"  总分 中位 {statistics.median(totals):.0f} / 均值 {statistics.mean(totals):.1f} / 最低 {min(totals)} / 最高 {max(totals)}")
    band = collections.Counter()
    for t in totals:
        band['<40 极扁平' if t < 40 else '40-59 偏平' if t < 60 else '60-74 尚可' if t < 75 else '≥75 有质感'] += 1
    for k in ['<40 极扁平', '40-59 偏平', '60-74 尚可', '≥75 有质感']:
        print(f"    {band.get(k,0):5d}  {k}")
    # 维度均值
    for dim, lab in [('ev', '物证钩子'), ('re', '留白'), ('af', '破模板'), ('vo', '声音')]:
        print(f"  维度均值 {lab}: {statistics.mean([r[dim] for r in rows]):.1f}/25")

    print('=' * 66)
    print(f"最扁平方阵 Top {top}（优先做文学优化）：")
    print(f"  {'分':>3} {'证':>2}{'白':>3}{'模':>3}{'声':>3}  文件")
    for r in rows[:top]:
        print(f"  {r['total']:>3} {r['ev']:>2}{r['re']:>3}{r['af']:>3}{r['vo']:>3}  {r['file'][:52]}")

    if '--csv' in sys.argv:
        out = sys.argv[sys.argv.index('--csv') + 1]
        import csv
        with open(out, 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=['file', 'total', 'ev', 're', 'af', 'vo', 'chars', 'heads'])
            w.writeheader()
            for r in sorted(rows, key=lambda x: x['total']):
                w.writerow(r)
        print(f"\nCSV 已导出: {out}")


if __name__ == '__main__':
    main()
