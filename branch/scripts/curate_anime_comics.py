#!/usr/bin/env python3
"""动漫 + 漫画收集：人工清单 + 数据核验。
- 动漫：AniList GraphQL（评分/人气/封面）
- 日漫：AniList MANGA；欧美漫画：Wikipedia REST（封面+简介）
ship_ref：0=无/弱 1=视觉氛围 2=外形/设定 3=工程细节 4=世代飞船直接参考（主线重点）
"""
import csv, json, os, re, sys, time, urllib.parse, urllib.request

ROOT = os.path.join(os.path.dirname(__file__), '..', '..')  # generation-ship
UA = {'User-Agent': 'generation-ship/1.0 (by shawn1905)'}
ANILIST = 'https://graphql.anilist.co'

def norm(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())

def anilist_search(name, mtype):
    q = '''query($s:String,$t:MediaType){Media(search:$s,type:$t){
      id title{romaji english} averageScore popularity startDate{year}
      coverImage{large} genres format siteUrl }}'''
    body = json.dumps({'query': q, 'variables': {'s': name, 't': mtype}}).encode()
    for attempt in range(4):
        try:
            req = urllib.request.Request(ANILIST, data=body, headers={'Content-Type': 'application/json', 'User-Agent': UA['User-Agent']})
            with urllib.request.urlopen(req, timeout=20) as r:
                d = json.load(r)
            return d.get('data', {}).get('Media')
        except Exception as e:
            if attempt == 3:
                print(f'  anilist err {name}: {e}')
                return None
            time.sleep(30 if '403' in str(e) else 3 + attempt * 3)  # 403 等待限流窗口

def wiki_lookup(name):
    """维基百科：搜索 + 封面 + 摘要"""
    api = 'https://en.wikipedia.org/w/api.php'
    params = urllib.parse.urlencode({
        'action': 'query', 'generator': 'search', 'gsrsearch': name,
        'gsrlimit': 1, 'prop': 'pageimages|extracts', 'exintro': 1,
        'explaintext': 1, 'pithumbsize': 460, 'format': 'json'})
    try:
        req = urllib.request.Request(f'{api}?{params}', headers=UA)
        with urllib.request.urlopen(req, timeout=20) as r:
            d = json.load(r)
        pages = (d.get('query') or {}).get('pages') or {}
        for pid, p in pages.items():
            return {
                'title': p.get('title', name),
                'cover': (p.get('thumbnail') or {}).get('source') or '',
                'desc': (p.get('extract') or '')[:120],
                'url': f"https://en.wikipedia.org/wiki/{urllib.parse.quote(p.get('title', '').replace(' ', '_'))}",
                'year': '',
            }
    except Exception as e:
        print(f'  wiki err {name}: {e}')
    return None

# ---- 动漫清单 ----
KNOWN_ANIME = {
    "Knights of Sidonia": ("世代飞船|硬科幻|机甲|生态穹顶", 4, "希德尼娅号：世代飞船+生态穹顶+重力子炮，主线第一参考"),
    "Planetes": ("硬科幻|太空作业|轨道工程", 3, "星空清理者：近地轨道作业硬核细节"),
    "Infinite Ryvius": ("太空|青少年|封闭社会", 3, "无限的未知：船内社会崩溃实验"),
    "Legend of the Galactic Heroes: Die Neue These": ("太空歌剧|政治|舰队战", 2, "银河英雄传说重制，舰队战美学"),
    "Cowboy Bebop": ("太空歌剧|西部|爵士", 2, "星际牛仔：1998 边界作，Bebop 号内部"),
    "Ghost in the Shell: Stand Alone Complex": ("赛博朋克|AI|义体", 1, "攻壳 SAC：赛博都市"),
    "Psycho-Pass": ("反乌托邦|AI|近未来", 0, "心理测量者：西比拉系统"),
    "Steins;Gate": ("时间旅行|悬疑|科学", 0, "命运石之门"),
    "Space Dandy": ("太空歌剧|喜剧|单元", 1, "太空丹迪：宇宙奇观"),
    "Eureka Seven": ("机甲|成长|滑空", 1, "交响诗篇"),
    "Macross Frontier": ("太空歌剧|歌|机甲", 1, "超时空要塞F"),
    "Fafner Exodus": ("机甲|外星|悲剧", 1, "苍穹之法芙娜"),
    "Expelled from Paradise": ("赛博朋克|AI|剧场版", 0, "乐园追放"),
    "Cyberpunk: Edgerunners": ("赛博朋克|义体|夜之城", 1, "边缘行者：赛博都市视觉"),
    "Ling Cage: Incarnation": ("末世|方舟|中国", 3, "灵笼：灯塔方舟+生态循环"),
    "Swallowed Star": ("科幻|中国|进化", 1, "吞噬星空"),
    "Vivy: Fluorite Eye's Song": ("AI|歌|科幻", 0, "Vivy：AI 百年旅程"),
    "86 Eighty-Six": ("军事科幻|机甲|战争", 1, "86 不存在的战区"),
    "Dr. Stone": ("科学|文明重建|近未来", 0, "石纪元：科学复现"),
    "RahXephon": ("机甲|心理|平行世界", 0, "翼神传说"),
    "Vandread": ("太空|性别|机甲", 1, "银河冒险战记"),
    "Yukikaze": ("军事科幻|AI|空战", 1, "战斗妖精雪风"),
    "Godzilla Singular Point": ("硬科幻|怪兽|科学", 0, "哥斯拉奇点：理论物理"),
    "Three-Body (2022)": ("硬科幻|中国|三体", 2, "艺画开天动画版三体"),
    "My Three Body": ("硬科幻|中国|方块动画", 1, "我的三体：MC 动画"),
    "Gargantia on the Verdurous Planet": ("太空|海洋|哲学", 2, "翠星加尔刚蒂亚"),
    "Kabaneri of the Iron Fortress": ("蒸汽朋克|末世|列车", 0, "甲铁城：蒸汽方舟列车"),
    "Ghost in the Shell: SAC_2045": ("赛博朋克|AI|续作", 1, "攻壳 SAC 2045"),
    "Paprika": ("梦境|赛博朋克|剧场版", 0, "红辣椒：今敏"),
    "Steamboy": ("蒸汽朋克|剧场版", 0, "蒸汽男孩"),
    "Appleseed": ("赛博朋克|义体|剧场版", 1, "苹果核战记"),
    "Ghost in the Shell 2: Innocence": ("赛博朋克|AI|剧场版", 0, "攻壳无罪"),
    "Mobile Suit Gundam 00": ("军事科幻|机甲|地缘", 1, "高达00"),
    "Mobile Suit Gundam: Iron-Blooded Orphans": ("军事科幻|机甲|战争", 1, "高达铁血孤儿"),
    "Mobile Suit Gundam Unicorn": ("军事科幻|机甲|UC", 1, "高达独角兽"),
    "Eighty-Six": ("军事科幻|机甲|战争", 1, "86（同 86 Eighty-Six）"),
}
# 重复条目清理：删除 Eighty-Six（与 86 Eighty-Six 重复）
KNOWN_ANIME.pop("Eighty-Six", None)

# ---- 漫画清单 ----
KNOWN_MANGA = {  # 日漫（AniList MANGA）
    "Sidonia no Kishi": ("世代飞船|硬科幻|机甲", 4, "希德尼娅的骑士（漫画原作，动画 2014）"),
    "Blame!": ("赛博朋克|巨构|末世", 2, "BLAME!：超巨构城市美学"),
    "Gunnm Last Order": ("赛博朋克|义体|火星", 1, "铳梦 Last Order"),
    "Gantz": ("科幻|惊悚|死亡游戏", 0, "Gantz"),
    "Pluto": ("AI|机器人|悬疑", 0, "PLUTO：浦泽直树"),
    "Terra Formars": ("火星|基因改造|殖民", 2, "火星异种"),
    "Girls' Last Tour": ("末世|温情|废土", 0, "少女终末旅行"),
    "Ajin": ("生物|不死|惊悚", 0, "亚人"),
    "Inuyashiki": ("机器人|改造|伦理", 0, "犬屋敷"),
    "20th Century Boys": ("悬疑|末世|阴谋", 0, "20世纪少年：99 边界作"),
    "Mobile Suit Gundam Thunderbolt": ("军事科幻|机甲|宇宙", 1, "高达雷霆宙域"),
    "Eden: It's an Endless World!": ("末世|生物|科幻", 0, "EDEN：97 边界作"),
    "Yokohama Kaidashi Kikou": ("末世|温情|机器", 0, "横滨购物纪行：98 边界作"),
    "Ghost in the Shell 2: Man-Machine Interface": ("赛博朋克|AI", 1, "攻壳 MMI"),
    "Blame! and So On": ("赛博朋克|设定集", 2, "BLAME! 设定集：巨构图纸"),
}
KNOWN_COMICS = {  # 欧美漫画（Wikipedia）
    "Saga (comics)": ("太空歌剧|战争|家庭", 2, "Saga：太空歌剧杰作"),
    "Descender (comics)": ("AI|太空|机器人", 2, "Descender：机器人少年寻主"),
    "Paper Girls": ("时间旅行|80年代|冒险", 0, "Paper Girls"),
    "Black Science": ("维度跳跃|硬科幻|家庭", 1, "Black Science"),
    "East of West": ("末世|西部|启示录", 0, "East of West"),
    "The Private Eye (comics)": ("赛博朋克|隐私|近未来", 0, "The Private Eye：无隐私世界"),
    "Low (comics)": ("深海|末世|探索", 1, "Low：深海遗孤"),
    "Fear Agent": ("太空牛仔|战争|硬核", 2, "Fear Agent：太空流浪汉"),
    "Prophet (comics)": ("生物朋克|太空|史诗", 2, "Prophet：超时空生物朋克"),
    "Letter 44 (comics)": ("硬科幻|太空政治|近未来", 3, "Letter 44：小行星带飞船+白宫双线"),
    "Injection (comics)": ("科幻|悬疑|英国", 0, "Injection"),
    "Aama (comics)": ("硬科幻|记忆|太空", 1, "Aama：法式硬科幻"),
    "Universal War One": ("太空歌剧|法国|军事", 2, "UW1：98 边界作，硬核太空战争"),
    "Star Wars (2015 comic)": ("星战|正史|绝地", 1, "星战正史漫画"),
}

def out_row(m, name, tags, ship, note, kind):
    if m is None:
        return None
    title = m['title'].get('english') or m['title'].get('romaji') or name
    return {
        'title': title, 'search_name': name, 'year': (m.get('startDate') or {}).get('year') or '',
        'source': 'anilist', 'source_id': m.get('id', ''),
        'score': m.get('averageScore') or '', 'popularity': m.get('popularity') or '',
        'genres': ','.join(m.get('genres') or []), 'format': m.get('format') or '',
        'cover_img': (m.get('coverImage') or {}).get('large') or '',
        'url': m.get('siteUrl') or '', 'tags': tags, 'ship_ref': ship, 'note': note,
        'desc': '', 'kind': kind,
    }

def main():
    anime_out = os.path.join(ROOT, 'branch', 'anime')
    comics_out = os.path.join(ROOT, 'branch', 'comics')
    os.makedirs(anime_out, exist_ok=True)
    os.makedirs(comics_out, exist_ok=True)

    # ---- 动漫 ----
    rows = []
    for name, (tags, ship, note) in KNOWN_ANIME.items():
        m = anilist_search(name, 'ANIME')
        r = out_row(m, name, tags, ship, note, 'anime')
        if r is None:
            print(f'  NOT FOUND anime: {name}')
            continue
        rows.append(r)
        time.sleep(1.0)
    fields = ['title', 'search_name', 'year', 'source', 'source_id', 'score', 'popularity',
              'genres', 'format', 'cover_img', 'url', 'tags', 'ship_ref', 'note', 'desc', 'kind']
    with open(os.path.join(anime_out, 'scifi_anime_curated.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f'anime curated: {len(rows)}')
    for r in rows:
        print(f"  {r['year']}  {str(r['score']):>4}  {r['title'][:44]}")

    # ---- 漫画（日漫 AniList + 欧美 Wikipedia）----
    rows = []
    for name, (tags, ship, note) in KNOWN_MANGA.items():
        m = anilist_search(name, 'MANGA')
        r = out_row(m, name, tags, ship, note, 'comic')
        if r is None:
            print(f'  NOT FOUND manga: {name}')
            continue
        rows.append(r)
        time.sleep(1.0)
    print(f'manga (anilist) curated: {len(rows)}')
    for name, (tags, ship, note) in KNOWN_COMICS.items():
        w = wiki_lookup(name)
        if w is None:
            print(f'  NOT FOUND comic: {name}')
            continue
        rows.append({
            'title': w['title'], 'search_name': name, 'year': w['year'],
            'source': 'wikipedia', 'source_id': '', 'score': '', 'popularity': '',
            'genres': '', 'format': 'Graphic Novel', 'cover_img': w['cover'],
            'url': w['url'], 'tags': tags, 'ship_ref': ship, 'note': note,
            'desc': w['desc'], 'kind': 'comic',
        })
        time.sleep(1.0)
    with open(os.path.join(comics_out, 'scifi_comics_curated.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f'comics curated: {len(rows)}')
    for r in rows:
        print(f"  {r['year'] or '--'}  {str(r['score']):>4}  {r['title'][:44]} [{r['source']}]")

if __name__ == '__main__':
    main()
