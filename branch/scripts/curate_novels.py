#!/usr/bin/env python3
"""小说精选：人工清单 → Open Library search 核验 → ratings 评分 → CSV + 封面"""
import csv, json, os, re, time, urllib.parse, urllib.request

ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
OUT = os.path.join(ROOT, 'branch', 'novels')
UA = {'User-Agent': 'generation-ship/1.0 (by shawn1905)'}
norm = lambda s: re.sub(r'[^a-z0-9]', '', (s or '').lower())

# (搜索词, 作者, 期望年份, tags, ship_ref, note)
KNOWN_NOVELS = [
    ('The Three-Body Problem', 'Liu Cixin', 2008, '硬科幻|外星接触|三体|中国', 2, '三体：舰队+飞船设计（自然选择号等）'),
    ('The Dark Forest', 'Liu Cixin', 2008, '硬科幻|面壁计划|舰队', 2, '三体II 黑暗森林：自然选择号/蓝色空间号'),
    ("Death's End", 'Liu Cixin', 2010, '硬科幻|星际舰队|二向箔', 2, '三体III 死神永生：星舰地球'),
    ('Seveneves', 'Neal Stephenson', 2015, '方舟|轨道工程|末世|硬科幻', 3, '七夏娃：方舟计划+轨道生存工程'),
    ('Aurora', 'Kim Stanley Robinson', 2015, '世代飞船|生态|社会|硬科幻', 4, '极光：世代飞船到达系外后的社会与工程困境，主线直接参考'),
    ('Ark', 'Stephen Baxter', 2009, '世代飞船|方舟|末世', 4, '方舟号：地球灾变下世代飞船启航'),
    ('Leviathan Wakes', 'James S. A. Corey', 2011, '硬科幻|太空歌剧|舰船|地缘政治', 3, 'The Expanse 系列：舰船工程细节标杆'),
    ('Project Hail Mary', 'Andy Weir', 2021, '硬科幻|工程谜题|外星接触', 2, '火星救援作者：飞船工程+谜题'),
    ('The Martian', 'Andy Weir', 2011, '硬科幻|火星|生存', 1, '火星救援：轨道力学+生存工程'),
    ('Blindsight', 'Peter Watts', 2006, '硬科幻|意识|第一接触', 2, '盲视：Theseus 探索舰'),
    ('A Fire Upon the Deep', 'Vernor Vinge', 1992, '太空歌剧|意识|星际网络', 2, '深渊上的火：信息空间科幻经典'),
    ('To Be Taught, If Fortunate', 'Becky Chambers', 2019, '远航|生物|人文', 2, '若幸运即教你：深空远航+生态改造'),
    ("Ender's Game", 'Orson Scott Card', 1985, '太空战|训练|策略', 1, '安德的游戏：舰队战经典'),
    ('Hyperion', 'Dan Simmons', 1989, '太空歌剧|朝圣|AI', 1, '海伯利安：朝圣者叙事+远距传送'),
    ('Dune', 'Frank Herbert', 1965, '生态|政治|沙丘', 1, '沙丘：帝国生态政治经典'),
    ('The Hitchhiker\'s Guide to the Galaxy', 'Douglas Adams', 1979, '喜剧|太空旅行', 1, '银河系漫游指南：黄金之心号'),
    ('Annihilation', 'Jeff VanderMeer', 2014, '南境|未知|生物', 0, '遗落的南境：生物恐怖'),
    ('The Calculating Stars', 'Mary Robinette Kowal', 2018, '航天|历史科幻|方舟', 1, '计算之星：灾变后航天计划'),
    ('A Memory Called Empire', 'Arkady Martine', 2019, '太空歌剧|政治|文化', 1, '记忆名为帝国：文化碰撞'),
    ('Children of Time', 'Adrian Tchaikovsky', 2015, '进化|生态|长时段', 1, '时间之子：蜘蛛文明进化史诗'),
    ('Solaris', 'Stanislaw Lem', 1961, '第一接触|未知|哲学', 0, '索拉里斯：意识海洋经典'),
    ('The Dispossessed', 'Ursula K. Le Guin', 1974, '反乌托邦|无政府|社会学', 0, '一无所有：双世界社会实验'),
    ('Ringworld', 'Larry Niven', 1970, '巨构|工程|探索', 3, '环形世界：巨构工程经典'),
    ('Tau Zero', 'Poul Anderson', 1970, '相对论|世代飞船|近光速', 4, '近光速世代飞船：时间膨胀经典'),
    ('Rendezvous with Rama', 'Arthur C. Clarke', 1973, '巨构|第一接触|探索', 3, '与拉玛相会：外星巨构飞船'),
]

def ol_search(q, author, year):
    api = 'https://openlibrary.org/search.json?' + urllib.parse.urlencode({'q': q, 'limit': 8})
    req = urllib.request.Request(api, headers=UA)
    with urllib.request.urlopen(req, timeout=20) as r:
        docs = json.load(r).get('docs', [])
    best = None
    for d in docs:
        authors = d.get('author_name') or []
        if not any(norm(author) in norm(a) for a in authors):
            continue
        if d.get('first_publish_year') and year and abs(d['first_publish_year'] - year) > 8:
            continue
        best = d
        break
    if best is None and docs:
        best = docs[0]  # 兜底
    return best

def ol_ratings(wkey):
    try:
        api = f'https://openlibrary.org/works/{wkey}/ratings.json'
        req = urllib.request.Request(api, headers=UA)
        with urllib.request.urlopen(req, timeout=20) as r:
            s = json.load(r).get('summary', {})
        return s.get('average') or '', s.get('count') or ''
    except Exception:
        return '', ''

def main():
    os.makedirs(OUT, exist_ok=True)
    rows = []
    for q, author, year, tags, ship, note in KNOWN_NOVELS:
        d = ol_search(q, author, year)
        if not d:
            print(f'  NOT FOUND: {q}')
            continue
        wkey = (d.get('key') or '').rsplit('/', 1)[-1]
        avg, cnt = ol_ratings(wkey) if wkey else ('', '')
        title = d.get('title') or q
        rows.append({
            'title': title, 'search_name': q, 'author': author,
            'year': d.get('first_publish_year') or year, 'source': 'openlibrary',
            'source_id': d.get('key') or '', 'rating': f'{float(avg):.1f}' if avg else '',
            'rating_count': cnt, 'cover_img': f"https://covers.openlibrary.org/b/id/{d['cover_i']}-L.jpg" if d.get('cover_i') else '',
            'url': f"https://openlibrary.org{d['key']}" if d.get('key') else '',
            'tags': tags, 'ship_ref': ship, 'note': note, 'desc': ''})
        print(f"  {str(d.get('first_publish_year')):>4}  {title[:36]:36} {avg or '--':>4} ({cnt})")
        time.sleep(0.4)

    with open(os.path.join(OUT, 'scifi_novels_curated.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f'novels curated: {len(rows)}')

    # 封面下载
    ok = fail = 0
    for r in rows:
        if not r['cover_img']:
            fail += 1
            continue
        key = re.sub(r'[^a-z0-9]+', '_', (r['source_id'] or r['title']).lower()).strip('_')
        dest = os.path.join(OUT, 'covers', key + '.jpg')
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        try:
            req = urllib.request.Request(r['cover_img'], headers=UA)
            with urllib.request.urlopen(req, timeout=25) as resp:
                data = resp.read()
            if len(data) < 2000:
                raise ValueError('too small')
            open(dest, 'wb').write(data)
            ok += 1
        except Exception as e:
            fail += 1
            print(f'  cover fail {r["title"]}: {e}')
        time.sleep(0.3)
    print(f'covers: ok={ok} fail={fail}')

if __name__ == '__main__':
    main()
