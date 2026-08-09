#!/usr/bin/env python3
"""剧集侧人工精选：KNOWN_TV 清单 + 与 IMDb raw 数据核验合并。
ship_ref 取值：0=无/弱 1=视觉氛围 2=飞船/空间站外形 3=内部结构/工程 4=世代飞船直接参考（主线重点）
"""
import csv, os, re, sys

OUT = os.path.join(os.path.dirname(__file__), '..', 'movies')

# (title, year) -> (tags, ship_ref, note)
KNOWN_TV = {
    # ---- 世代飞船 / 方舟（主线核心）----
    ("The Expanse", 2015): ("世代飞船|硬科幻|太空歌剧|地缘政治", 4, "Nauvoo/Behemoth 世代飞船+舰船细节标杆，主线第一参考"),
    ("Battlestar Galactica", 2004): ("方舟舰队|末世|太空歌剧|宗教", 4, "人类流亡舰队，社会+工程双重参考"),
    ("Nightflyers", 2018): ("世代飞船|太空恐怖|心理", 4, "飞向恒星的世代飞船恐怖剧"),
    ("Lost in Space", 2018): ("方舟殖民|太空家庭|冒险", 3, "殖民方舟 Resolute 号+行星基地"),
    ("The 100", 2014): ("方舟空间站|末世|青少年", 3, "方舟空间站坠落地球"),
    ("1899", 2022): ("方舟船|迷案|悬疑", 3, "船上方舟隐喻（船舶形态）"),
    ("Ascension", 2014): ("世代飞船|阴谋|迷你剧", 4, "60年代世代飞船计划"),
    # ---- 硬科幻 / 近未来 ----
    ("For All Mankind", 2019): ("架空历史|太空竞赛|硬科幻|火星", 3, "NASA 工程细节教科书"),
    ("3 Body Problem", 2024): ("硬科幻|外星|三体|物理学", 3, "三体问题+星际舰队计划"),
    ("Three-Body", 2023): ("硬科幻|中国|三体", 3, "腾讯剧版三体"),
    ("Devs", 2020): ("量子计算|宿命论|悬疑", 1, "预测未来公司"),
    ("Severance", 2022): ("意识分割|反乌托邦|职场", 0, "工作/生活记忆分离"),
    ("Silo", 2023): ("反乌托邦|末世|地窖", 1, "地下巨窖社会"),
    ("Station Eleven", 2021): ("末世|流感|人文", 0, "疫情后的剧团"),
    ("Tales from the Loop", 2020): ("近未来|温情|艺术", 0, "环状机器小镇"),
    ("The Peripheral", 2022): ("近未来|VR|时间线", 1, "威廉吉布森改编"),
    ("Away", 2020): ("火星任务|宇航员|家庭", 2, "国际火星任务"),
    ("Another Life", 2019): ("深空|外星|冒险", 2, "外星信标任务"),
    # ---- AI / 意识 / 赛博朋克 ----
    ("Black Mirror", 2011): ("反乌托邦|AI|近未来|单元剧", 0, "科技寓言集"),
    ("Westworld", 2016): ("AI|乐园|西部|觉醒", 0, "接待员觉醒"),
    ("Altered Carbon", 2018): ("赛博朋克|意识|义体", 1, "意识数字化"),
    ("Upload", 2020): ("意识上传|喜剧|近未来", 0, "数字来世"),
    ("Pantheon", 2022): ("意识上传|动画|阴谋", 0, "上传大脑战争"),
    ("Love, Death & Robots", 2019): ("短片集|动画|多元", 1, "风格试验田"),
    ("Person of Interest", 2011): ("AI|监视|犯罪", 0, "机器先知"),
    ("Orphan Black", 2013): ("克隆|惊悚|身份", 0, "克隆姐妹"),
    ("Electric Dreams", 2017): ("菲利普迪克|单元剧", 0, "PKD 短篇改编"),
    ("Raised by Wolves", 2020): ("人造人|殖民|宗教|异星", 2, "开普勒-22b 殖民+人造人抚养"),
    # ---- 时间 / 平行世界 ----
    ("Dark", 2017): ("时间旅行|德语|悬疑|循环", 0, "温登时间网"),
    ("Fringe", 2008): ("平行世界|边缘科学|FBI", 0, "边缘档案"),
    ("The Man in the High Castle", 2015): ("架空历史|平行世界|轴心国", 0, "轴心国获胜世界"),
    ("Doctor Who", 2005): ("时间旅行|太空歌剧|英剧", 1, "TARDIS 与飞船设计多样"),
    # ---- 太空歌剧 / 军事 ----
    ("Foundation", 2021): ("太空歌剧|帝国|心理史学|视觉", 2, "银河帝国+殖民舰设计"),
    ("The Mandalorian", 2019): ("星战|西部|赏金猎人", 2, "星战宇宙细节"),
    ("Andor", 2022): ("星战|谍战|政治", 2, "星战最扎实剧集"),
    ("Star Trek: Discovery", 2017): ("星际迷航|探索", 2, "星联新舰"),
    ("Star Trek: Picard", 2020): ("星际迷航|续作", 2, "皮卡德晚年"),
    ("Star Trek: Strange New Worlds", 2022): ("星际迷航|经典回归", 2, "企业号新纪元"),
    ("The Orville", 2017): ("太空歌剧|喜剧|致敬", 1, "迷航喜剧版"),
    ("Firefly", 2002): ("太空歌剧|西部|独立舰", 2, "Serenity 号内部设计参考"),
    ("Stargate Atlantis", 2004): ("星际门|探险|军事", 1, "飞马座远征"),
    ("Stargate Universe", 2009): ("深空|世代飞船感|生存", 3, "命运号深空漂流，资源管理"),
    ("Halo", 2022): ("军事科幻|游戏改编", 1, "士官长"),
    # ---- 末世 / 灾难 ----
    ("The Last of Us", 2023): ("末世|真菌|父女", 0, "真菌末世"),
    ("Fallout", 2024): ("末世|废土|核战", 1, "避难所+废土"),
    ("Snowpiercer", 2020): ("方舟列车|阶级|末世", 3, "永动列车社会（剧版）"),
    ("Y: The Last Man", 2021): ("末世|性别|改编", 0, "男性灭绝"),
    ("The Stand", 2020): ("末世|超自然|斯蒂芬金", 0, "瘟疫后善恶之战"),
    ("Scavengers Reign", 2023): ("异星生态|动画|生存", 2, "异星生态艺术标杆"),

    # ---- 经典扩充：1980-2000（用户放宽范围） ----
    ("Star Trek: The Next Generation", 1987): ("太空歌剧|星际迷航|联邦", 2, "企业号 D：全息甲板+联邦理想"),
    ("Red Dwarf", 1988): ("太空喜剧|孤独|克隆", 2, "红矮星号：孤独远航喜剧"),
    ("Quantum Leap", 1989): ("穿越|科学实验|单元剧", 0, "量子跳跃实验"),
    ("Star Trek: Deep Space Nine", 1993): ("空间站|政治|战争", 2, "深空九号：空间站+战争弧线"),
    ("Babylon 5", 1993): ("空间站|政治|长弧线", 2, "巴别五号：空间站地缘政治史诗"),
    ("The X-Files", 1993): ("外星|阴谋|单元剧", 0, "X档案：外星阴谋论"),
    ("SeaQuest 2032", 1993): ("海底|科幻|探险", 0, "海下探索舰"),
    ("Earth 2", 1994): ("殖民|生态|远征", 1, "地球2号：异星殖民远征"),
    ("Star Trek: Voyager", 1995): ("远航|星际迷航|生存", 2, "航海家号：被抛到银河彼岸的归途"),
    ("Space: Above and Beyond", 1995): ("太空战|军事|克隆", 2, "深海太空战+克隆士兵"),
    ("Lexx", 1996): ("活体飞船|黑色幽默|异星", 1, "活体飞船 Lexx：异色经典"),
    ("Stargate SG-1", 1997): ("星门|远征|单元剧", 1, "星门远征队"),
    ("Farscape", 1999): ("活体飞船|外星|冒险", 2, "活体飞船莫亚+外星生物设计"),
}

def norm(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())

def load_pool():
    pool = {}
    for fn in ('tv_pool.csv',):
        path = os.path.join(OUT, fn)
        if os.path.exists(path):
            for r in csv.DictReader(open(path)):
                pool.setdefault((norm(r['title']), r['year']), r)
                pool.setdefault((norm(r['title']), ''), r)
    return pool

def main():
    raw = list(csv.DictReader(open(os.path.join(OUT, 'scifi_tv_raw.csv'))))
    by_norm = {}
    for r in raw:
        by_norm.setdefault((norm(r['title']), r['year']), r)
        by_norm.setdefault((norm(r['title']), ''), r)
    pool = load_pool()

    rows, missing = [], []
    for (title, year), (tags, ship, note) in KNOWN_TV.items():
        # 指定年份时禁用空年份兜底（避免同名不同年份作品误配）
        r = by_norm.get((norm(title), str(year)))
        if not r and not year:
            r = by_norm.get((norm(title), ''))
        if not r:  # 回退到全量候选池（IMDb 类型标签不可靠）
            r = pool.get((norm(title), str(year)))
            if not r and not year:
                r = pool.get((norm(title), ''))
        if not r:
            missing.append((title, year))
            continue
        rows.append({**r, 'tags': tags, 'ship_ref': ship, 'note': note})
    rows.sort(key=lambda r: int(r['num_votes']), reverse=True)

    fields = ['tconst', 'title', 'year', 'runtime_min', 'imdb_rating', 'num_votes', 'genres',
              'tags', 'ship_ref', 'note', 'imdb_url']
    with open(os.path.join(OUT, 'scifi_tv_curated.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f'curated TV: {len(rows)}  (known={len(KNOWN_TV)})')
    if missing:
        print('NOT MATCHED:')
        for t, y in missing:
            print(f'  {t} ({y})')

if __name__ == '__main__':
    main()
