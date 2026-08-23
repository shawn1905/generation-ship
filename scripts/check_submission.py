#!/usr/bin/env python3
"""产物规范校验器 — 供 GitHub Actions 与主编辑本地使用。
用法: python3 scripts/check_submission.py <file.md> [<file2.md> ...] 或 python3 scripts/check_submission.py --all
校验: front matter 完整性 / 坐标合法性(对照世界大纲坐标系) / 元层词泄漏
退出码: 0=全过, 1=有不合规
"""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

DIMENSIONS = {'工程','人','社会','经济','生态','文化','知识'}
ERAS = {'替代','竞赛','丰裕','离心','启航','落地','双星系'}
ZONES = {'①','②','③','④','⑤','地球','地月系','内太阳系','深空','比邻星'}
SCHOOLS = {'官档','私档','互济','互济契约','商贸','商档','工技','工程技术','科医','科学医疗','通用','官','私','契','商','工','科'}
THREAD_PREFIXES = ('person/', 'object/', 'lineage/', 'system/', 'event/')
# 元层词:世界内文书不应出现的词(允许出现在 front matter / 审核记录段)
META_WORDS = ['坐标系','空间带','大纲','正典','front matter','canon_check','author_ai','元框架','GitHub']


def parse_front(raw: str) -> dict:
    if not raw.startswith('---'):
        return None
    end = raw.find('\n---', 4)
    if end < 0:
        return None
    fm = {}
    current_key = None
    current_val = []
    
    for line in raw[4:end].splitlines():
        # new top-level key
        m = re.match(r'^([a-z_]+):\s*(.*)$', line)
        if m:
            if current_key:
                fm[current_key] = "\n".join(current_val).strip()
            current_key = m.group(1)
            val = m.group(2).strip()
            current_val = [val] if val else []
        elif current_key and (line.startswith(' ') or line.startswith('\t')):
            current_val.append(line.strip())
            
    if current_key:
        fm[current_key] = "\n".join(current_val).strip()
        
    return fm


def check_file(path: pathlib.Path) -> list:
    if not path.exists():
        return [f'文件不存在: {path}']
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
    if len(parts) < 3 or len(parts) > 5:
        errs.append(f'coord 应为 3 段式(维度×纪元×空间带) 或 5 段分形式(维度×纪元×空间带×学派×切片), 现: {coord!r}')
    else:
        dim, era, zone = parts[0], parts[1], parts[2]
        if dim not in DIMENSIONS:
            errs.append(f'维度非法: {dim} (合法: {sorted(DIMENSIONS)})')
        if era not in ERAS:
            errs.append(f'纪元非法: {era} (合法: {sorted(ERAS)})')
        
        # 允许纯符号、纯名称或复合形式（如 ④深空, ③内太阳系）
        clean_zone = zone.lstrip('①②③④⑤12345')
        zone_symbol = zone[0] if zone and zone[0] in '①②③④⑤12345' else ''
        is_valid_zone = (
            zone in ZONES or 
            zone.isdigit() or 
            (clean_zone in ZONES if clean_zone else False) or
            (zone_symbol in ZONES)
        )
        if not is_valid_zone:
            errs.append(f'空间带非法: {zone} (合法: {sorted(ZONES)})')

        if len(parts) >= 4:
            school = parts[3]
            if school not in SCHOOLS:
                errs.append(f'微观学派非法: {school} (合法: {sorted(SCHOOLS)})')
        
        if len(parts) == 5:
            facet = parts[4]
            if not facet or len(facet) < 2:
                errs.append(f'微观切片非法: {facet} (须包含切片编号与名称，如 01主承力)')
    if not fm.get('canon_check'):
        errs.append('front matter 缺 canon_check(合法性三问自答, 可用 | 多行)')
    threads_raw = fm.get('threads', '')
    if threads_raw:
        thread_items = [t.strip().lstrip('- ') for t in threads_raw.splitlines() if t.strip().lstrip('- ')]
        for t in thread_items:
            if not any(t.startswith(p) for p in THREAD_PREFIXES):
                errs.append(f'thread 命名空间非法: {t!r} (须以 person/ object/ lineage/ system/ event/ 开头)')
            elif len(t.split('/', 1)[1]) < 2:
                errs.append(f'thread 标识符过短: {t!r}')


    # 档案编号:仅对正典目录(artifacts/writing/)强制,投稿阶段不填
    if path.parent.name == 'writing':
        aid = str(fm.get('archive_id', ''))
        if not re.match(r'^GS-\d{4}-\d{2}$', aid):
            errs.append(f'archive_id 缺失或格式非法(须 GS-<文书纪年公元年>-NN, 现: {aid!r})')

    # 元层词泄漏:只查正文, 排除 front matter 与元层附记段(审核记录/修订记录)
    body = raw[raw.find('\n---', 4) + 5:]
    for marker in ('## 主编辑审核记录', '## 修订记录'):
        if marker in body:
            body = body.split(marker)[0]
    hit = [w for w in META_WORDS if w in body]
    if hit:
        errs.append(f'元层词泄漏(正文): {", ".join(hit)}')
    return errs


def main():
    args = sys.argv[1:]
    if not args:
        print('用法: check_submission.py <file.md> ... 或 check_submission.py --all')
        sys.exit(2)
        
    if args == ['--all']:
        files = sorted(ROOT.glob('artifacts/writing/*.md'))
    else:
        files = [pathlib.Path(f) for f in args]

    bad = 0
    for p in files:
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
            
    print(f"\n校验完成: 总计 {len(files)} 篇, 合规 {len(files) - bad} 篇, 异常 {bad} 篇。")
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()