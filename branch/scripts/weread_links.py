#!/usr/bin/env python3
"""批量查微信读书地址：素材库小说清单 → weread search → 输出链接表"""
import csv, json, re, time, urllib.parse, urllib.request

ROOT = '/Users/dahongge/generation-ship/branch'
UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126.0 Safari/537.36'}
norm = lambda s: re.sub(r'[^a-z0-9\u4e00-\u9fff]', '', (s or '').lower())

def search(kw, count=10):
    url = 'https://weread.qq.com/web/search/global?' + urllib.parse.urlencode(
        {'keyword': kw, 'maxIdx': 0, 'count': count})
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)

def book_url(book_id):
    return f'https://weread.qq.com/web/bookDetail/{book_id}'

# 排除：三体×3、Dune 沙丘
SKIP = {'The Three-Body Problem', 'The Dark Forest', "Death's End", 'Dune'}
rows = [r for r in csv.DictReader(open(f'{ROOT}/novels/scifi_novels_curated.csv')) if r['title'] not in SKIP]

# 中文别名优先搜索（微信读书以中译本为主）
ALIAS = {
    'Seveneves': '七夏娃', 'Aurora': '极光 罗宾逊', 'Ark': '方舟 巴克斯特',
    'Leviathan Wakes': '苍穹浩瀚 利维坦', 'Project Hail Mary': '挽救计划',
    'The Martian': '火星救援', 'Blindsight': '盲视 瓦茨', 'A Fire upon the Deep': '深渊上的火',
    'To Be Taught, If Fortunate': '幸存的巡游', "Ender's Game": '安德的游戏',
    'Hyperion': '海伯利安', "The Hitchhiker's Guide to the Galaxy": '银河系漫游指南',
    'Annihilation': '湮灭 杰夫·范德米尔', 'The Calculating Stars': '计算之星',
    'A Memory Called Empire': '名为帝国的记忆', 'Children of Time': '时间之子 柴纳',
    'Solaris': '索拉里斯', 'The Dispossessed': '一无所有 勒古恩',
    'Ringworld': '环形世界 尼文', 'Tau Zero': '零时 安德森', 'Rendezvous with Rama': '与拉玛相会',
}

results = []
for r in rows:
    title = r['title']
    kw = ALIAS.get(title, title)
    best = None
    for attempt, query in enumerate([kw, title, r['search_name']]):
        try:
            d = search(query)
        except Exception as e:
            print(f'  ERR {title}: {e}')
            time.sleep(1)
            continue
        books = d.get('books') or []
        for b in books:
            bi = b.get('bookInfo') or {}
            bt = bi.get('title') or ''
            # 书名匹配：norm 包含或互相包含
            if norm(title) in norm(bt) or norm(bt) in norm(title) or norm(query) in norm(bt):
                best = bi
                break
        if best:
            break
        time.sleep(0.4)
    if best:
        results.append((title, best.get('title'), best.get('author'), book_url(best['bookId'])))
        print(f"  ✓ {title[:28]:28} → 《{best.get('title')}》 {best.get('author')}  {book_url(best['bookId'])}")
    else:
        results.append((title, '', '', ''))
        print(f"  ✗ {title}: 未找到")
    time.sleep(0.5)

print('\n=== 汇总 ===')
with open('/tmp/weread_links.md', 'w', encoding='utf-8') as f:
    f.write('| 素材库书目 | 微信读书书名 | 作者 | 链接 |\n|---|---|---|---|\n')
    for t, wt, au, url in results:
        if url:
            f.write(f'| {t} | {wt} | {au} | [{url}]({url}) |\n')
        else:
            f.write(f'| {t} | — | — | 未上架 |\n')
print('written /tmp/weread_links.md')
