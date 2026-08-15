#!/usr/bin/env python3
"""产物规范校验器 — 供 GitHub Actions 与主编辑本地使用。
用法: python3 scripts/check_submission.py <file.md> [<file2.md> ...]
校验: front matter 完整性 / 坐标合法性(对照世界大纲坐标系) / 元层词泄漏
退出码: 0=全过, 1=有不合规
"""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

DIMENSIONS = {'工程','人','社会','经济','生态','文化','知识'}
ERAS = {'替代','竞赛','丰裕','离心','启航','落地','双星系'}
ZONES = {'①','②','③','④','⑤','地球','地月系','内太阳系','深空','比邻星'}
# 元层词:世界内文书不应出现的词(允许出现在 front matter / 审核记录段)
# 只保留硬元层词;世界内合理出现的词(生成模型/AI agent/贡献/学派等)不入黑名单
META_WORDS = ['坐标系','空间带','大纲','正典','front matter','canon_check','author_ai','元框架','GitHub']


def parse_front(raw: str) -> dict:
    if not raw.startswith('---'):
        return None
    end = raw.find('\n---', 4)
    if end < 0:
        return None
    fm = {}
    for line in raw[4:end].splitlines():
        m = re.match(r'^([a-z_]+):\s*(.*)$', line.strip())
        if m:
            fm[m.group(1)] = m.group(2).strip()
    return fm


def check_file(path: pathlib.Path) -> list:
    errs = []
    raw = path.read_text(encoding='utf-8')
    fm = parse_front(raw)
    if fm is None:
        return ['front matter 缺失或格式异常(须以 --- 开头且第二段 --- 闭合, 字段: key: value)']

    for k in ('author_ai', 'date', 'coord', 'title'):
        if not fm.get(k):
            errs.append(f'front matter 缺字段: {k}')

    coord = str(fm.get('coord', ''))
    parts = [p.strip() for p in coord.split('×')]
    if len(parts) < 3:
        errs.append(f'coord 应含 维度×纪元×空间带 三段, 现: {coord!r}')
    else:
        dim, era, zone = parts[0], parts[1], parts[2]
        if dim not in DIMENSIONS:
            errs.append(f'维度非法: {dim} (合法: {sorted(DIMENSIONS)})')
        if era not in ERAS:
            errs.append(f'纪元非法: {era} (合法: {sorted(ERAS)})')
        if zone not in ZONES and not zone.isdigit():
            errs.append(f'空间带非法: {zone} (合法: {sorted(ZONES)})')

    if not fm.get('canon_check'):
        errs.append('front matter 缺 canon_check(合法性三问自答, 可用 | 多行)')

    # 元层词泄漏:只查正文, 排除 front matter 与审核记录段
    body = raw[raw.find('\n---', 4) + 5:]
    body = body.split('## 主编辑审核记录')[0] if '## 主编辑审核记录' in body else body
    hit = [w for w in META_WORDS if w in body]
    if hit:
        errs.append(f'元层词泄漏(正文): {", ".join(hit)}')
    return errs


def main():
    files = sys.argv[1:]
    if not files:
        print('用法: check_submission.py <file.md> ...')
        sys.exit(2)
    bad = 0
    for f in files:
        p = pathlib.Path(f)
        # 非产物文档(目录说明/模板)跳过校验
        if p.name in ('README.md', 'TEMPLATE.md'):
            continue
        errs = check_file(p)
        if errs:
            bad += 1
            print(f'✗ {p.name}')
            for e in errs:
                print(f'    - {e}')
        else:
            print(f'✓ {p.name}')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()