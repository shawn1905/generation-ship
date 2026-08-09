#!/usr/bin/env python3
"""电影侧人工精选：KNOWN_MOVIES 清单 + 与 IMDb raw 数据核验合并。
ship_ref 取值：
  0 = 无/弱参考  1 = 视觉氛围   2 = 飞船/空间站外形   3 = 内部结构/工程细节   4 = 世代飞船直接参考（主线重点）
"""
import csv, os, re

OUT = os.path.join(os.path.dirname(__file__), '..', 'movies')

# (title, year) -> (tags, ship_ref, note)   tags 用 | 分隔中文主题标签
KNOWN_MOVIES = {
    # ---- 硬科幻 / 太空 ----
    ("Interstellar", 2014): ("星际航行|硬科幻|黑洞|环形空间站", 4, "Endurance 与环形中继站设计，主线直接参考"),
    ("The Martian", 2015): ("火星殖民|硬科幻|生存", 1, "火星基地工程细节扎实"),
    ("Gravity", 2013): ("近地轨道|太空灾难|硬科幻", 1, "失重/轨道物理教科书级"),
    ("Arrival", 2016): ("外星接触|语言学|硬科幻", 2, "外星飞船造型经典"),
    ("Ad Astra", 2019): ("深空航行|心理|太空歌剧", 2, "飞船造型克制写实"),
    ("Passengers", 2016): ("世代飞船|休眠|星际移民", 4, "世代飞船核心参考"),
    ("Aniara", 2018): ("世代飞船|悲剧|哲学", 4, "世代飞船社会学，偏离航线的绝望"),
    ("Voyagers", 2021): ("世代飞船|青少年|社会实验", 4, "世代飞船社会结构"),
    ("Stowaway", 2021): ("火星任务|伦理|硬科幻", 2, "任务船内部细节"),
    ("High Life", 2018): ("深空|生育|伦理", 2, "法式黑暗深空美学"),
    ("Europa Report", 2013): ("木卫二|伪纪录片|硬科幻", 1, "科学严谨的探索任务"),
    ("Moon", 2009): ("月球基地|AI|孤独", 2, "月球基地+AI 伦理"),
    ("Sunshine", 2007): ("太阳|硬科幻|心理", 2, "Icarus II 飞船设计值得参考"),
    ("Prospect", 2018): ("外星殖民地|独立科幻|西部", 1, "低成本硬核外星殖民"),
    ("Pandorum", 2009): ("世代飞船|恐怖|失忆", 4, "世代飞船内部结构+船员疯癫"),
    ("The Midnight Sky", 2020): ("末世|太空|父女", 1, "北极站+深空救赎"),
    ("I.S.S.", 2023): ("空间站|政治|悬疑", 1, "近未来空间站冲突"),
    ("Space Sweepers", 2021): ("太空垃圾|韩国|动作", 2, "飞船造型有设计感"),
    ("The Wandering Earth", 2019): ("流浪地球|方舟|中国", 3, "行星级迁徙+地下城，中国科幻里程碑"),
    ("The Wandering Earth II", 2023): ("流浪地球|方舟|中国", 3, "方舟计划+数字生命，前传"),
    ("Moon Man", 2022): ("月球基地|喜剧|中国", 1, "独行月球，基地细节轻松参考"),
    ("Journey to the West: Conquering the Demons", 2013): ("科幻|中国|公路", 0, "宇宙探索编辑部：伪科幻人文片"),
    ("Moonfall", 2022): ("月球|灾难|科幻", 1, "月球坠落脑洞"),
    ("Oblivion", 2013): ("后末日|克隆|无人机|空中塔", 2, "泡泡船+天空塔设计，无人机基地"),
    # ---- AI / 机器人 / 意识 ----
    ("Her", 2013): ("AI|爱情|近未来", 0, "AI 关系哲学"),
    ("Ex Machina", 2014): ("AI|图灵测试|密室", 1, "AI 伦理密室剧"),
    ("I, Robot", 2004): ("AI|机器人三定律|侦探", 0, "阿西莫夫改编"),
    ("Chappie", 2015): ("AI|机器人|南非", 0, "机器人自我意识"),
    ("Upgrade", 2018): ("AI|义体|复仇", 0, "低配硬核爽片"),
    ("Transcendence", 2014): ("意识上传|AI|反噬", 0, "奇点寓言"),
    ("Morgan", 2016): ("AI|生物工程|惊悚", 0, "人造人失控"),
    ("Archive", 2020): ("AI|意识|机器人", 0, "小成本意识拷贝"),
    ("After Yang", 2021): ("AI|家庭|温情", 0, "亚洲未来美学"),
    ("M3GAN", 2022): ("AI|恐怖|玩具", 0, "AI 娃娃"),
    ("Blade Runner 2049", 2017): ("赛博朋克|AI|复制人", 2, "城市+载具设计标杆"),
    ("A.I. Artificial Intelligence", 2001): ("AI|机器人|斯皮尔伯格", 0, "机器人渴望成为人"),
    ("The Creator", 2023): ("AI|战争|视觉", 1, "东南亚未来战争美学"),
    ("Automata", 2014): ("AI|机器人|末世", 0, "废土机器人"),
    ("Ghost in the Shell", 2017): ("赛博朋克|义体|真人版", 1, "攻壳真人版，赛博都市"),
    ("The Matrix Resurrections", 2021): ("虚拟现实|黑客帝国|续集", 0, "母体重启"),
    ("Free Guy", 2021): ("虚拟现实|游戏|喜剧", 0, "NPC 觉醒"),
    ("Ready Player One", 2018): ("虚拟现实|游戏|绿洲", 0, "斯皮尔伯格 VR 狂欢"),
    ("Tron: Legacy", 2010): ("虚拟现实|视觉|电子世界", 0, "光追美学先驱"),
    ("Source Code", 2011): ("时间循环|意识|惊悚", 0, "八分钟循环"),
    # ---- 时间 ----
    ("Inception", 2010): ("梦境|时间|诺兰", 0, "多层梦境结构"),
    ("Tenet", 2020): ("时间倒流|间谍|诺兰", 0, "熵减物理"),
    ("Looper", 2012): ("时间旅行|黑帮|硬核", 0, "环形时间设定"),
    ("Edge of Tomorrow", 2014): ("时间循环|军事|机甲", 1, "外骨骼动力甲设计"),
    ("Predestination", 2014): ("时间悖论|宿命|改编", 0, "闭合因果链"),
    ("Donnie Darko", 2001): ("时间|心理|cult", 0, "兔子人时间线"),
    ("The Butterfly Effect", 2004): ("时间回溯|惊悚", 0, "蝴蝶效应"),
    ("Coherence", 2013): ("平行宇宙|小成本|聚会", 0, "彗星来的那一夜"),
    ("Triangle", 2009): ("时间循环|恐怖|游轮", 0, "游轮循环"),
    ("Palm Springs", 2020): ("时间循环|喜剧|爱情", 0, "婚礼循环"),
    ("The Adam Project", 2022): ("时间旅行|温情|家庭", 0, "穿越见父亲"),
    ("Project Almanac", 2015): ("时间旅行|青少年|纪录片", 0, "高中生发明时光机"),
    ("Primer", 2004): ("时间旅行|硬核|小成本", 0, "最硬核时间旅行"),
    # ---- 反乌托邦 / 近未来 / 殖民 ----
    ("Children of Men", 2006): ("反乌托邦|不育|末世", 0, "人类不育的末世"),
    ("District 9", 2009): ("外星难民|隔离|伪纪录", 2, "外星飞船+贫民窟"),
    ("Elysium", 2013): ("空间站|阶级|义体", 2, "轨道天堂空间站"),
    ("The Hunger Games", 2012): ("反乌托邦|竞技|青少年", 0, "饥饿游戏"),
    ("The Maze Runner", 2014): ("反乌托邦|迷宫|青少年", 0, "移动迷宫"),
    ("In Time", 2011): ("反乌托邦|时间货币", 0, "时间即金钱"),
    ("Never Let Me Go", 2010): ("克隆|伦理|温情", 0, "克隆人捐献人生"),
    ("Dredd", 2012): ("反乌托邦|暴力|城市", 0, "梅加城一号"),
    ("Snowpiercer", 2013): ("方舟列车|阶级|末世", 3, "方舟隐喻+内部结构参考（列车形态）"),
    ("Alita: Battle Angel", 2019): ("赛博朋克|义体|机甲", 1, "废铁城+天空城"),
    ("Cloud Atlas", 2012): ("多线|转世|未来", 1, "六世轮回"),
    ("Valerian and the City of a Thousand Planets", 2017): ("太空歌剧|宇宙都市|视觉", 2, "千星之城空间站设计"),
    ("Jupiter Ascending", 2015): ("太空歌剧|基因|华丽", 1, "沃卓斯基太空歌剧"),
    ("Dune: Part One", 2021): ("太空歌剧|沙丘|生态", 2, "厄拉科斯+香料生态"),
    ("Dune: Part Two", 2024): ("太空歌剧|沙丘|战争", 2, "沙虫战争"),
    ("Avatar", 2009): ("外星生态|潘多拉|殖民", 2, "外星生态+基地设计"),
    ("Avatar: The Way of Water", 2022): ("外星生态|海洋|续集", 1, "潘多拉海洋"),
    ("WALL-E", 2008): ("动画|方舟|地球末日", 3, "Axiom 方舟飞船设计"),
    ("Titan A.E.", 2000): ("动画|方舟|人类幸存", 2, "人类流亡方舟"),
    # ---- 外星接触 / 恐怖 ----
    ("Prometheus", 2012): ("异形前传|外星|工程", 3, "探索舰+星球基地+工程师"),
    ("Alien: Covenant", 2017): ("异形|殖民|AI", 3, "殖民方舟 Covenant 号设计"),
    ("Life", 2017): ("空间站|外星生物|恐怖", 1, "ISS 上发现外星生命"),
    ("Under the Skin", 2013): ("外星|艺术|斯嘉丽", 0, "外星皮囊"),
    ("Nope", 2022): ("UFO|奇观|乔丹皮尔", 0, "UFO 新解读"),
    ("Annihilation", 2018): ("外星区域|变异|心理", 0, "微光区"),
    ("A Quiet Place", 2018): ("末世|怪物|家庭", 0, "声音猎杀"),
    ("A Quiet Place Part II", 2020): ("末世|怪物|续集", 0, "声音猎杀续"),
    ("Cloverfield", 2008): ("怪兽|伪纪录|纽约", 0, "怪兽袭击"),
    ("10 Cloverfield Lane", 2016): ("地堡|悬念|密室", 1, "末日地堡生存"),
    ("Signs", 2002): ("外星|宗教|沙马兰", 0, "麦田圈"),
    ("War of the Worlds", 2005): ("外星入侵|灾难|斯皮尔伯格", 0, "三角机入侵"),
    ("The Tomorrow War", 2021): ("外星|时间|征兵", 1, "未来外星战争"),
    ("Attack the Block", 2011): ("外星|街区|英伦", 0, "伦敦街区打外星人"),
    ("The 5th Wave", 2016): ("外星入侵|青少年", 0, "第五波"),
    ("Battle: Los Angeles", 2011): ("外星入侵|军事|巷战", 0, "洛杉矶滩头"),
    ("Independence Day: Resurgence", 2016): ("外星入侵|续集|灾难", 1, "地球联合舰队"),
    # ---- 末世 / 灾难 ----
    ("28 Days Later", 2002): ("丧尸|末世|病毒", 0, "狂暴病毒"),
    ("I Am Legend", 2007): ("末世|孤独|变异", 0, "纽约孤城"),
    ("The Road", 2009): ("末世|父子|绝望", 0, "灰烬公路"),
    ("Mad Max: Fury Road", 2015): ("末世|废土|追车", 0, "废土美学巅峰"),
    ("World War Z", 2013): ("丧尸|全球|灾难", 0, "丧尸海"),
    ("Contagion", 2011): ("疫情|纪实|科学", 0, "病毒传播纪实"),
    ("Don't Look Up", 2021): ("彗星|讽刺|媒体", 0, "彗星撞地球讽刺剧"),
    ("Geostorm", 2017): ("气象武器|灾难", 1, "空间站气象控制"),
    ("Greenland", 2020): ("彗星|避难所|家庭", 1, "疏散避难所"),
    ("Finch", 2021): ("末世|机器人|温情", 0, "杰夫机器人"),
    ("Love and Monsters", 2020): ("末世|怪兽|冒险", 0, "变异地球"),
    ("The Book of Eli", 2010): ("末世|废土|圣经", 0, "废土送经"),
    ("The Day After Tomorrow", 2004): ("气候灾难|冰河", 0, "极寒末世"),
    ("The Platform", 2019): ("反乌托邦|垂直监狱|西班牙", 0, "垂直食堂"),
    ("2012", 2009): ("末日|方舟船|灾难", 1, "方舟船设计（船舶形态）"),
    # ---- 太空歌剧 / 军事 ----
    ("Star Wars: Episode VII - The Force Awakens", 2015): ("太空歌剧|星战|重启", 2, "星战新三部曲"),
    ("Star Wars: Episode VIII - The Last Jedi", 2017): ("太空歌剧|星战", 2, "星战新三部曲"),
    ("Star Wars: Episode IX - The Rise of Skywalker", 2019): ("太空歌剧|星战|终章", 2, "星战新三部曲"),
    ("Rogue One: A Star Wars Story", 2016): ("太空歌剧|星战|战争", 2, "死星蓝图行动"),
    ("Solo: A Star Wars Story", 2018): ("太空歌剧|星战|外传", 1, "韩索罗起源"),
    ("Star Trek", 2009): ("太空歌剧|星际迷航|重启", 3, "企业号新设计"),
    ("Star Trek Into Darkness", 2013): ("太空歌剧|星际迷航", 2, "可汗"),
    ("Star Trek Beyond", 2016): ("太空歌剧|星际迷航", 2, "约克镇空间站"),
    ("Guardians of the Galaxy", 2014): ("太空歌剧|银河护卫队|喜剧", 2, "宇宙杂耍"),
    ("Guardians of the Galaxy Vol. 2", 2017): ("太空歌剧|银河护卫队", 2, "ego 星球"),
    ("Guardians of the Galaxy Vol. 3", 2023): ("太空歌剧|银河护卫队", 2, "三部曲终章"),
    ("Ender's Game", 2013): ("军事科幻|虫族|训练", 1, "星际军校"),
    ("Pacific Rim", 2013): ("机甲|怪兽|动作", 0, "机甲猎兽"),
    ("Pacific Rim Uprising", 2018): ("机甲|怪兽|续集", 0, "机甲猎兽续"),
    ("Transformers", 2007): ("机甲|外星|爆米花", 1, "变形金刚"),
    ("RoboCop", 2014): ("义体|近未来|翻拍", 0, "机械战警"),
    ("Real Steel", 2011): ("机器人|拳击|温情", 0, "钢铁擂台"),
    ("Battleship", 2012): ("外星|海军|爆米花", 0, "海战打外星人"),
    ("Overlord", 2018): ("二战|超自然|恐怖", 0, "纳粹血清"),
    # ---- 亚洲 / 其它 ----
    ("Shanghai Fortress", 2019): ("中国|科幻|外星|口碑失败", 1, "上海堡垒：可作失败案例分析"),
    ("Crazy Alien", 2019): ("外星|喜剧|中国", 0, "疯狂的外星人"),
    ("Okja", 2017): ("生物工程|韩美|伦理", 0, "超级猪"),
    ("The Host", 2006): ("怪兽|韩国|灾难", 0, "汉江怪物"),
}

def norm(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())

def load_pool():
    pool = {}
    for fn in ('movie_pool.csv',):
        path = os.path.join(OUT, fn)
        if os.path.exists(path):
            for r in csv.DictReader(open(path)):
                pool.setdefault((norm(r['title']), r['year']), r)
                pool.setdefault((norm(r['title']), ''), r)
    return pool

def main():
    raw = list(csv.DictReader(open(os.path.join(OUT, 'scifi_movies_raw.csv'))))
    by_norm = {}
    for r in raw:
        by_norm.setdefault((norm(r['title']), r['year']), r)
        by_norm.setdefault((norm(r['title']), ''), r)
    pool = load_pool()

    rows, missing = [], []
    for (title, year), (tags, ship, note) in KNOWN_MOVIES.items():
        r = by_norm.get((norm(title), str(year))) or by_norm.get((norm(title), ''))
        if not r:  # 回退到全量候选池（IMDb 类型标签不可靠）
            r = pool.get((norm(title), str(year))) or pool.get((norm(title), ''))
        if not r:
            missing.append((title, year))
            continue
        rows.append({**r, 'tags': tags, 'ship_ref': ship, 'note': note})
    rows.sort(key=lambda r: int(r['num_votes']), reverse=True)

    fields = ['tconst', 'title', 'year', 'runtime_min', 'imdb_rating', 'num_votes', 'genres',
              'tags', 'ship_ref', 'note', 'imdb_url']
    with open(os.path.join(OUT, 'scifi_movies_curated.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f'curated movies: {len(rows)}  (known={len(KNOWN_MOVIES)})')
    if missing:
        print('NOT MATCHED:')
        for t, y in missing:
            print(f'  {t} ({y})')

if __name__ == '__main__':
    main()
