#!/usr/bin/env python3
"""正典确定性修复器 canon_fix.py — 只做安全、可幂等、可验证的机械修复。

修复项:
  [1] front matter 图片路径补 ../../（当 image 以 world/ 开头，缺相对前缀）
  [2] 有 image 字段但正文无嵌图 → 在首个 H1 后插入档案体图注嵌入
  [3] 完全重复段(刷屏)去重：保留首次出现，删除后续「逐字重复」的散文段
      —— 只删完全重复，绝不拼接、不动图片/标题/表格/头块

不触碰（留给工作清单人工处理）: 残句、英雄化、金手指红线、懒canon_check、ASCII框线

用法:
  python3 scripts/canon_fix.py --dry-run    # 只报告将改动的篇数与样例
  python3 scripts/canon_fix.py --apply      # 实际写回
"""
import re, sys, pathlib, collections

ROOT = pathlib.Path(__file__).resolve().parent.parent
WRITING = ROOT / 'artifacts' / 'writing'


def split_fm(raw):
    # 兼容缺陷：闭合 --- 后未换行直接接正文(如 "---# 标题")
    m = re.match(r'^(---\n.*?\n---)[ \t]*(\n?)(.*)$', raw, re.S)
    if m:
        return m.group(1), m.group(3)
    return '', raw


def world_date(datestr):
    m = re.match(r'(\d{4})-(\d{2})-(\d{2})', datestr or '')
    if m:
        y, mo, d = m.groups()
        return f"{int(y)}年{int(mo)}月{int(d)}日"
    return (datestr or '').strip()


def fix_image_path(fm):
    """[1] image: world/... -> image: ../../world/..."""
    changed = False
    def repl(m):
        nonlocal changed
        val = m.group(2).strip()
        if val.startswith('world/') or (val and not val.startswith('../') and not val.startswith('http') and not val.startswith('/')):
            newval = '../../' + val.lstrip('./')
            changed = True
            return f"{m.group(1)}{newval}"
        return m.group(0)
    new_fm = re.sub(r'^(image:\s*)(.+)$', repl, fm, flags=re.M)
    return new_fm, changed


def get_img(fm):
    m = re.search(r'^image:\s*(.+)$', fm, re.M)
    return m.group(1).strip() if m else None


def get_title(fm):
    m = re.search(r'^title:\s*(.+)$', fm, re.M)
    if m:
        return m.group(1).strip()
    return None


def insert_embed(body, img, title, date):
    """[2] 正文无 ![] 时，在首个 H1 后插入档案体嵌入。"""
    if '![' in body or not img:
        return body, False
    cap_title = title or '存档影像'
    wd = world_date(date)
    caption = f"档案影像：{cap_title}" + (f" · {wd}" if wd else "")
    embed = f"![{caption}]({img})"
    lines = body.split('\n')
    # 找首个 H1
    idx = None
    for i, l in enumerate(lines):
        if l.strip().startswith('# '):
            idx = i
            break
    if idx is not None:
        lines.insert(idx + 1, '')
        lines.insert(idx + 2, embed)
    else:
        lines = [embed, ''] + lines
    return '\n'.join(lines), True


def is_prose_block(b):
    s = b.strip()
    if len(re.sub(r'\s', '', s)) < 25:
        return False
    if s.startswith(('#', '!', '|', '>', '```', '---')):
        return False
    if re.match(r'^(\d+[\.、）)]|[-*•])\s', s):  # 列表项
        return False
    # 关键安全约束：只处理「以句末标点收尾的完整散文句」，
    # 排除以冒号收尾的引导句（其后常接表格/列表，删除会造成孤儿内容）
    if s.endswith(('：', ':')):
        return False
    if not re.search(r'[。！？]$', s):
        return False
    if not re.search(r'[\u4e00-\u9fff]', s):
        return False
    return True


def dedup_paragraphs(body):
    """[3] 删除逐字重复的散文段，保留首次出现——但绝不抽空任何章节。
    安全约束：仅当某重复段所在「章节」(上一个标题到下一个标题之间)删除后
    仍保留至少一个其它内容块(散文/列表/表格/图片)时，才删除该重复段。"""
    units = re.split(r'(\n\s*\n)', body)  # 奇数下标为分隔符
    # 第一遍：给每个内容块标注所属章节序号（按标题行递增）
    section_of = []
    sec = -1
    for u in units:
        if re.fullmatch(r'\n\s*\n', u):
            section_of.append(None)
            continue
        if u.strip().startswith('#'):
            sec += 1
        section_of.append(sec)
    # 统计每章节的内容块数量（非分隔符、非纯标题）
    sec_content = collections.Counter()
    for u, s in zip(units, section_of):
        if s is None:
            continue
        if u.strip() and not u.strip().startswith('#'):
            sec_content[s] += 1
    # 第二遍：删除逐字重复的散文段（受章节余量约束）
    seen = set()
    removed = []
    out = []
    for u, s in zip(units, section_of):
        if s is None:  # 分隔符原样保留
            out.append(u)
            continue
        key = re.sub(r'\s+', '', u)
        if is_prose_block(u):
            dup = key in seen
            if not dup:
                seen.add(key)
            # 仅当确属重复、且删除后本章节仍有其它内容时，才删
            if dup and sec_content[s] >= 2:
                sec_content[s] -= 1
                removed.append(u.strip()[:40])
                continue
        else:
            if len(key) >= 25:
                seen.add(key)
        out.append(u)
    new = ''.join(out)
    new = re.sub(r'\n{3,}', '\n\n', new)
    return new, removed


def main():
    apply = '--apply' in sys.argv
    files = sorted(WRITING.glob('*.md'))
    c_path = c_embed = c_dedup = c_delim = 0
    dedup_total = 0
    samples = {'path': [], 'embed': [], 'dedup': []}

    for p in files:
        if p.name in ('README.md', 'TEMPLATE.md'):
            continue
        raw = p.read_text(encoding='utf-8', errors='replace')
        fm, body = split_fm(raw)
        if not fm:
            continue
        orig_fm, orig_body = fm, body
        touched = False

        # [4] front matter 闭合 --- 与正文粘连(缺换行)规范化
        if fm and not raw[len(fm):].startswith('\n'):
            c_delim += 1; touched = True

        fm, ch = fix_image_path(fm)
        if ch:
            c_path += 1; touched = True
            if len(samples['path']) < 3:
                samples['path'].append((p.name, get_img(orig_fm), get_img(fm)))

        img = get_img(fm)
        title = get_title(fm)
        date = re.search(r'^date:\s*(.+)$', fm, re.M)
        date = date.group(1).strip() if date else ''
        body, ch = insert_embed(body, img, title, date)
        if ch:
            c_embed += 1; touched = True
            if len(samples['embed']) < 3:
                samples['embed'].append((p.name, img))

        body, removed = dedup_paragraphs(body)
        if removed:
            c_dedup += 1; dedup_total += len(removed); touched = True
            if len(samples['dedup']) < 5:
                samples['dedup'].append((p.name, removed))

        if touched and apply:
            out = (fm + '\n\n' + body.lstrip('\n')).rstrip('\n') + '\n'
            p.write_text(out, encoding='utf-8')

    mode = '已写回' if apply else 'DRY-RUN(未写回)'
    print(f"canon_fix {mode} · 扫描 {len(files)} 篇")
    print('=' * 56)
    print(f"  [1] 图片路径补 ../../ : {c_path} 篇")
    print(f"  [2] 补正文图注嵌入     : {c_embed} 篇")
    print(f"  [3] 去重复段(刷屏)     : {c_dedup} 篇 / 删 {dedup_total} 段")
    print(f"  [4] front matter 分隔符规范化: {c_delim} 篇")
    print('=' * 56)
    print("样例[1] 路径修复:")
    for n, a, b in samples['path']:
        print(f"   {n[:38]}\n      {a}  ->  {b}")
    print("样例[2] 嵌入:")
    for n, i in samples['embed']:
        print(f"   {n[:44]}  += ![..]({i})")
    print("样例[3] 去重:")
    for n, r in samples['dedup']:
        print(f"   {n[:40]}  删{len(r)}段: {r[0]!r}")


if __name__ == '__main__':
    main()
