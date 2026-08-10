#!/usr/bin/env python3
"""原画/设定集精选：欧美科幻社区(ArtStation/Goodreads/维基)公认知名条目。

人工精选 KNOWN_* 清单 → 来源核验 → 封面下载 → branch/art/scifi_art_curated.csv
- 原画类:  维基百科 REST summary 核验 + 人物图(无词条的新生代 → manual + ArtStation 链接)
- 设定集类: Goodreads search → book/show 页 og:image 拿封面
"""
import csv, json, os, re, sys, time, urllib.request, urllib.parse

ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
OUT = os.path.join(ROOT, 'branch', 'art')
UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Safari/537.36'}

# ── 知名概念艺术家 / 原画 (type=原画) ─────────────────────────
# (姓名, 维基词条或''(无词条), 主页URL, 年代, tags, ship_ref, note)
KNOWN_ARTISTS = [
    ('Ralph McQuarrie', 'Ralph_McQuarrie', 'https://www.artstation.com/ralphmcquarrie', 1975,
     '概念设计|星球大战|飞船|经典', 4, '星战概念设计之父：千年隼/X翼/死星的原点，科幻造型范式开创者'),
    ('Syd Mead', 'Syd_Mead', 'https://www.artstation.com/sydmead', 1982,
     '概念设计|银翼杀手|城市|工业设计', 3, '银翼杀手视觉建筑师：近未来城市+交通工具工业设计标杆'),
    ('Chris Foss', 'Chris_Foss', 'https://www.artstation.com/chrisfoss', 1972,
     '插画|封面艺术|巨舰|经典', 4, '科幻封面插画大师：巨型飞船涂装风格，一代科幻视觉记忆'),
    ('John Berkey', 'John_Berkey', 'https://www.johnberkey.com', 1978,
     '插画|飞船|太空|经典', 4, '美国飞船插画宗师：写实太空巨舰，NASA 海报风格'),
    ('Doug Chiang', 'Doug_Chiang', 'https://www.artstation.com/dougchiang', 1999,
     '概念设计|星球大战|机器人|工业', 3, '星战前传+侠盗一号概念总监：机械细节与东方美学融合'),
    ('Ryan Church', '', 'https://www.artstation.com/ryanchurch', 2000,
     '概念设计|星球大战|工业|飞船', 3, '星战前传/变形金刚概念：AT-TE、圣殿等标志设计'),
    ('Craig Mullins', '', 'https://www.craig-mullins.com', 2000,
     '概念设计|电影|游戏|数字绘画', 2, '影视游戏概念绘画先驱：数字油画风格影响一代人'),
    ('Feng Zhu', '', 'https://www.artstation.com/fengzhu', 2000,
     '概念设计|星球大战|教学|工业', 2, '星战前传概念+知名概念艺术学校 FZD 创始人'),
    ('George Hull', '', 'https://www.artstation.com/georgehull', 2015,
     '概念设计|星球大战|飞船', 3, '星战原力觉醒概念设计：新秩序歼星舰等'),
    ('Ash Thorp', 'Ash_Thorp', 'https://www.artstation.com/ashthorp', 2017,
     '概念设计|银翼杀手2049|赛博朋克|平面', 1, '银翼杀手2049/攻壳机动队视觉：几何未来主义'),
    ('Maciej Kuciara', '', 'https://www.artstation.com/maciejkuciara', 2017,
     '概念设计|电影|赛博朋克|教学', 1, '好莱坞电影概念(美队3/沙丘游戏等)+概念教学社区'),
    ('Sparth', '', 'https://www.artstation.com/sparth', 2010,
     '概念设计|Halo|光环|美术总监', 3, 'Halo 系列艺术总监：光环飞船与建筑视觉'),
    ('Nicolas Bouvier', '', 'https://www.artstation.com/nicolasbouvier', 2015,
     '概念设计|星球大战|飞船|工业', 3, '星战视觉：歼星舰、飞船剖视与工业细节'),
    ('Paul Chadeisson', '', 'https://www.artstation.com/paulchadeisson', 2019,
     '概念设计|沙丘2049|赛博朋克|城市', 2, '沙丘2049/星战/赛博朋克2077概念：巨型城市+巨构'),
    ('Ben Mauro', '', 'https://www.artstation.com/benmauro', 2015,
     '概念设计|光环|星际穿越|机械', 2, '光环/星际穿越概念：机械与装甲设计'),
    ('Ian McQue', '', 'https://www.artstation.com/ianmcque', 2015,
     '概念设计|星际公民|飞船|工业', 4, '星际公民首席概念：锈蚀工业风飞船，世代飞船参考'),
    ('Jama Jurabaev', '', 'https://www.artstation.com/jamajurabaev', 2015,
     '概念设计|星球大战|银翼杀手2049|数字绘画', 2, '星战/银翼杀手2049概念：数字绘画+3D 合成'),
    ('Aaron Beck', '', 'https://www.artstation.com/aaronbeck', 2012,
     '概念设计|星球大战|飞船|机械', 2, '星战概念：共和国/帝国载具与机械细节'),
    ('John Harris', 'John_Harris_(artist)', 'https://www.johnharrisart.com', 1976,
     '插画|封面艺术|宇宙|经典', 2, '英国科幻封面艺术：宇宙奇观风格'),
    ('Wayne Barlowe', 'Wayne_Barlowe', 'https://www.artstation.com/waynebarlowe', 1979,
     '插画|异形星球|生物|经典', 1, '异形星球/地狱景观插画：外星生态想象力'),
]

# ── 知名设定集 (type=设定集) ──────────────────────────────────
# (书名, 作者/编者, Goodreads搜索词, 出版年, tags, ship_ref, note)
KNOWN_ARTBOOKS = [
    ('The Art and Soul of Blade Runner 2049', 'Tanya Lapointe', 'The Art and Soul of Blade Runner 2049', 2017,
     '设定集|银翼杀手2049|概念设计|电影', 3, '银翼杀手2049官方设定集：完整概念设计+世界观'),
    ('The Art of Star Wars: The Force Awakens', 'Phil Szostak', 'The Art of Star Wars The Force Awakens', 2015,
     '设定集|星球大战|概念设计|电影', 3, '原力觉醒官方设定集：新世代星战视觉'),
    ('Star Wars Art: Ralph McQuarrie', 'Brandon Alinger', 'Star Wars Art Ralph McQuarrie', 2012,
     '设定集|星球大战|经典|概念设计', 4, 'McQuarrie 作品全集：星战造型原点'),
    ('The Art of Star Wars: Rogue One', 'Josh Kushins', 'The Art of Star Wars Rogue One', 2016,
     '设定集|星球大战|概念设计|电影', 3, '侠盗一号设定集：死星与地面战争视觉'),
    ('Halo: The Art of Building Worlds', 'Titan Books', 'Halo The Art of Building Worlds', 2013,
     '设定集|Halo|光环|游戏美术', 3, 'Halo 美术总集：人类/星盟飞船与建筑'),
    ('The Art of Mass Effect', 'BioWare', 'The Art of Mass Effect', 2007,
     '设定集|质量效应|游戏美术|飞船', 3, '质量效应美术集：诺曼底号与银河文明视觉'),
    ('The Making of Star Wars', 'J.W. Rinzler', 'The Making of Star Wars', 2007,
     '设定集|星球大战|幕后|经典', 2, '星战制作内幕：原始概念与拍摄记录'),
    ('The Art of Cyberpunk 2077', 'CD Projekt Red', 'The Art of Cyberpunk 2077', 2020,
     '设定集|赛博朋克|游戏美术|城市', 2, '赛博朋克2077设定集：夜之城视觉圣经'),
    ('The Art of Star Citizen', 'Cloud Imperium', 'The Art of Star Citizen', 2018,
     '设定集|星际公民|飞船|游戏美术', 4, '星际公民艺术设定集：世代尺度飞船工业设计'),
    ('The Art and Making of Dune', 'Tanya Lapointe', 'The Art and Soul of Dune', 2021,
     '设定集|沙丘|概念设计|电影', 3, '沙丘(2021)设定集：厄拉科斯+巨型扑翼机视觉'),
    ('Alien: The Archive', 'Simon Ward', 'Alien The Archive', 2014,
     '设定集|异形|经典|电影', 2, '异形全系列艺术档案：诺斯特罗莫号与异形设计'),
    ('The Art of Star Trek', 'Judith and Garfield Reeves-Stevens', 'The Art of Star Trek', 1995,
     '设定集|星际迷航|经典|飞船', 3, '星际迷航美术集：企业号与联邦视觉体系'),
    ('The Science of Interstellar', 'Kip Thorne', 'The Science of Interstellar', 2014,
     '设定集|星际穿越|物理|科学顾问', 2, '星际穿越科学设定：虫洞/黑洞可视化幕后'),
    ('The Art of The Mandalorian', 'Phil Szostak', 'The Art of The Mandalorian', 2020,
     '设定集|曼达洛人|星战|剧集', 2, '曼达洛人概念设计：星战西部片视觉'),
    ('The Art of Alita: Battle Angel', 'Titan Books', 'The Art of Alita Battle Angel', 2019,
     '设定集|阿丽塔|赛博朋克|电影', 2, '阿丽塔设定集：末世机甲城市视觉'),
]

def fetch(url, timeout=20):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()

def wiki_summary(page):
    """维基 REST summary：返回 (title, thumbnail, desc, url) 或 None"""
    try:
        data = json.loads(fetch(f'https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(page)}'))
        if data.get('type') == 'standard':
            return (data.get('title'), (data.get('thumbnail') or {}).get('source'), data.get('description') or '',
                    data.get('content_urls', {}).get('desktop', {}).get('page'))
    except Exception:
        pass
    return None

def goodreads_cover(title):
    """Goodreads 搜索 → 第一本书 → 书页 og:image"""
    try:
        q = urllib.parse.quote_plus(title)
        html = fetch(f'https://www.goodreads.com/search?q={q}', 20).decode('utf-8', 'ignore')
        m = re.search(r'/book/show/(\d+)-[a-z0-9-]+', html)
        if not m:
            return None
        bid = m.group(1)
        page = fetch(f'https://www.goodreads.com/book/show/{bid}', 20).decode('utf-8', 'ignore')
        m2 = re.search(r'<meta property="og:image" content="([^"]+)"', page)
        return m2.group(1) if m2 else None
    except Exception:
        return None

def slug(s):
    return re.sub(r'[^a-z0-9]+', '_', str(s).lower()).strip('_') or 'x'

def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(os.path.join(OUT, 'covers'), exist_ok=True)
    rows = []

    # ── 原画 / 艺术家 ──
    print('== 原画/艺术家 ==')
    for name, wiki, home, year, tags, ship, note in KNOWN_ARTISTS:
        info = wiki_summary(wiki) if wiki else None
        if info:
            title, thumb, desc, url = info
            row = {'title': name, 'type': '原画', 'artist': name, 'year': year, 'source': 'wikipedia',
                   'source_id': wiki, 'tags': tags, 'ship_ref': ship, 'note': note,
                   'url': url, 'cover_img': thumb or '', 'img_note': '维基词条图' if thumb else ''}
            print(f'  OK  {name}: {desc[:40]}')
        else:
            row = {'title': name, 'type': '原画', 'artist': name, 'year': year, 'source': 'manual',
                   'source_id': '', 'tags': tags, 'ship_ref': ship, 'note': note,
                   'url': home, 'cover_img': '', 'img_note': ''}
            print(f'  MAN {name}: 无维基词条 → ArtStation/官网链接')
        rows.append(row)
        time.sleep(0.25)

    # ── 设定集 ──
    print('== 设定集 ==')
    for title, author, gq, year, tags, ship, note in KNOWN_ARTBOOKS:
        cover = goodreads_cover(gq)
        rows.append({'title': title, 'type': '设定集', 'artist': author, 'year': year, 'source': 'goodreads',
                     'source_id': '', 'tags': tags, 'ship_ref': ship, 'note': note,
                     'url': f'https://www.goodreads.com/search?q={urllib.parse.quote_plus(gq)}',
                     'cover_img': cover or '', 'img_note': 'Goodreads 封面' if cover else ''})
        print(f"  {'OK ' if cover else 'NO '} {title[:44]}")
        time.sleep(1.2)  # Goodreads 需慢一点

    with open(os.path.join(OUT, 'scifi_art_curated.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f'art curated: {len(rows)}')

    # ── 封面下载 ──
    print('== 封面下载 ==')
    ok = fail = 0
    for r in rows:
        if not r['cover_img']:
            fail += 1
            continue
        dest = os.path.join(OUT, 'covers', slug(r['source_id'] or r['title']) + '.jpg')
        try:
            data = fetch(r['cover_img'], 30)
            if len(data) < 2000:
                raise ValueError('too small')
            with open(dest, 'wb') as f:
                f.write(data)
            ok += 1
        except Exception as e:
            fail += 1
            print(f'  cover fail {r["title"]}: {e}')
        time.sleep(0.3)
    print(f'covers: ok={ok} fail={fail}')

if __name__ == '__main__':
    main()
