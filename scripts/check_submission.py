#!/usr/bin/env python3
"""产物规范校验器 — 供 GitHub Actions 与主编辑本地使用。
用法: python3 scripts/check_submission.py <file.md> [<file2.md> ...] 或 python3 scripts/check_submission.py --all
校验: front matter 完整性 / 坐标合法性(对照世界大纲坐标系) / 元层词泄漏
退出码: 0=全过, 1=有不合规
"""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

# 合法坐标值集合（全库 1220 篇扫描汇总，含旧坐标系与多星纪元新坐标系）
DIMENSIONS = {'事件','人','内太阳系','军事','制度','医','地月系','地球','安全','工程','技术','政治','文化','比邻星','深空','生态','知识','社会','科医','科学','经济','通信'}
ERAS = {'丰裕','丰裕建设期','制度张力期','双星系','启航','多星纪元','多极建设期','拓荒纪元','替代','离心','竞赛','落地','资源重组期','远航纪元','跨星系治理期','文化融合期'}
ZONES = {'ARK01建造带','ARK01航行带','L1拉格朗日带','L5船坞带','①地球','①地球表面','①太阳系','②地月空间','②地月系','②比邻星系','③内太阳系','④外太阳系','④深空','⑤巴纳德星系','⑤比邻星','⑤深空','主小行星带','乘员选拔带','全域','全象限','内太阳系','冥王星轨道带','原乡保护带','地月系','地球','地球带','地表带','城市农业带','太阳系外缘带','日球层顶带','星际航道带','星际轨道带','月背撞击坑带','比邻星','比邻星b地表带','比邻星b海洋带','比邻星b轨道带','比邻星地表带','沙漠修复带','沿海低地带','深空','深空外缘带','火星地表带','火星带','环月带','环月轨道带','第五恒星系带','第五恒星系方向带','第六恒星系方向带','第四恒星系带','联合体带','跨星系带','近地轨道带','金星轨道带','静海地下带','鲸鱼座τ带'}
SCHOOLS = {'互济','亚种医学学派','人事官档学派','传记学派','信息工程学派','公共卫生学派','典礼学派','军事学派','农业学派','制造工程学派','勘探工程学派','医学学派','医学派','历史学派','哲学学派','商贸','国际法学派','土壤学派','城市规划学派','大气工程学派','天体生物学派','子事件','安全工程学派','官档','官档学派','审计学派','射电天文学派','工业经济学派','工技','工技学派','工程学派','建筑学派','微生物学派','推进工程学派','政治学派','教育学派','文化学派','文化工程学派','文学派','文明扩展学派','文物保护学派','星际介质学派','星际客运学派','机器人工程学派','材料工程学派','标准化学派','民防学派','气候学派','法学派','海洋工程学派','海洋生物学派','深时考古学派','深空医学派','灾害管理学派','物流学派','生保工程学派','生态学派','生态工程学派','监察学派','真菌学派','社会学派','私档','科医','科学学派','空间天气学派','空间运输学派','经济学派','能源工程学派','能源经济学派','航天学派','航行安全学派','艺术学派','行政学派','行星地质学派','行星大气学派','行星工程学派','计量学派','身份工程学派','通信工程学派','通信解码学派'}
THREAD_PREFIXES = {'contact','culture','ecology','econ','economy','education','energy','event','festival','incident','industry','law','lineage','mil','military','object','person','public','ritual','security','system','tech','thought'}
# 元层词:世界内文书不应出现的词(允许出现在 front matter / 审核记录段)
# 注: "正典""大纲""空间带""坐标系"常作为世界内合法用词,不列入
META_WORDS = ['front matter','canon_check','author_ai','元框架','GitHub']


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
        # 兼容两种格式: 新式 prefix/identifier (如 system/xxx) 和旧式中文关键词标签 (如 [太空资源, 轨道拍卖])
        thread_items = re.findall(r'([a-zA-Z]+/[\w-]+)', threads_raw)
        if thread_items:
            for t in thread_items:
                pfx = t.split('/')[0]
                if pfx not in THREAD_PREFIXES:
                    errs.append(f'thread 命名空间非法: {t!r} (合法前缀: {sorted(THREAD_PREFIXES)})')
                elif len(t.split('/', 1)[1]) < 2:
                    errs.append(f'thread 标识符过短: {t!r}')
        else:
            # 旧式中文关键词标签: 提取逗号/顿号分隔的非空关键词，有内容即视为合法（存量兼容）
            legacy_tags = [t.strip() for t in re.split(r'[,\u3001\[\]]', threads_raw) if t.strip() and not t.strip().startswith('-')]
            if not legacy_tags:
                errs.append(f'threads 字段无有效线索ID: {threads_raw!r}')


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