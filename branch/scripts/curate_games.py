#!/usr/bin/env python3
"""游戏侧人工精选：KNOWN_GAMES 清单 + Steam 全量数据核验。
匹配顺序：raw(sci-fi 标签) → 全量 games.csv → Steam 官方搜索 API 补 appid。
ship_ref：0=无/弱 1=视觉氛围 2=飞船/空间站外形 3=内部结构/工程细节 4=世代飞船直接参考
"""
import csv, json, os, re, subprocess, sys, urllib.parse, urllib.request

DATA = os.path.join(os.path.dirname(__file__), '..', 'data', 'steam')
OUT = os.path.join(os.path.dirname(__file__), '..', 'games')

KNOWN_GAMES = {
    # ---- 太空 / 模拟 / 建造 ----
    "EVE Online": ("太空|MMO|经济", 3, "舰船/空间站设计海量参考"),
    "Elite Dangerous": ("太空模拟|银河|探索", 3, "舰船内部+星系尺度假想"),
    "Star Citizen": ("太空模拟|众筹|飞船", 3, "飞船细节顶级（EA 中）"),
    "No Man's Sky": ("太空探索|程序生成|生存", 2, "程序星球+货船"),
    "X4: Foundations": ("太空模拟|经济|舰队", 3, "模块化飞船+空间站建造"),
    "Kerbal Space Program": ("火箭|物理|工程", 3, "轨道力学教科书"),
    "Kerbal Space Program 2": ("火箭|物理|工程", 2, "续作（EA 评价一般）"),
    "Outer Wilds": ("太空探索|时间循环|解密", 2, "小飞船+奇异星球"),
    "The Outer Worlds": ("太空歌剧|RPG|黑色幽默", 2, "殖民边疆宇宙"),
    "Starfield": ("太空RPG|探索|B社", 2, "千行星+飞船建造"),
    "Mass Effect Legendary Edition": ("太空歌剧|RPG|三部曲", 3, "诺曼底号内部结构"),
    "Mass Effect: Andromeda": ("殖民|方舟|RPG", 3, "方舟级殖民船+异星建设（Steam 名带 Deluxe）"),
    "Dead Space": ("太空恐怖|生存", 3, "石村号内部结构标杆"),
    "Dead Space Remake": ("太空恐怖|生存|重制", 3, "石村号重制版"),
    "Alien: Isolation": ("太空恐怖|潜行|异形", 3, "Sevastopol 空间站"),
    "Prey": ("空间站|恐怖|模拟", 3, "Talos I 空间站内部"),
    "Subnautica": ("水下|外星|生存", 1, "异星海洋基地"),
    "Dyson Sphere Program": ("建造|戴森球|自动化", 1, "行星级工程"),
    "Factorio": ("自动化|工厂|硬核", 1, "船内工业系统参考"),
    "Satisfactory": ("自动化|工厂|3D", 0, "工厂自动化"),
    "Space Engineers": ("太空建造|物理|生存", 2, "自由飞船建造"),
    "Avorion": ("飞船建造|程序生成", 2, "模块化飞船设计"),
    "Cosmoteer: Starship Architect & Commander": ("飞船建造|模块|物理", 2, "龙骨+模块化结构"),
    "Starbound": ("沙盒|星球|探索", 1, "2D 星际沙盒"),
    "Astroneer": ("星球基地|可爱|探索", 1, "异星基地美化"),
    "The Planet Crafter": ("行星改造|生存", 1, "火星改造"),
    "Surviving Mars": ("火星殖民|模拟", 2, "火星穹顶城市"),
    "RimWorld": ("殖民模拟|故事生成", 2, "太空殖民社会学"),
    "Oxygen Not Included": ("殖民地|气体物理|生存", 1, "闭环生命支持参考"),
    "Endless Space 2": ("4X|太空策略", 2, "文明级太空策略"),
    "Stellaris": ("4X|银河帝国", 2, "银河尺度文明"),
    "Sins of a Solar Empire®: Rebellion": ("RTS|太空", 2, "舰队战"),
    "Homeworld 3": ("RTS|母舰|史诗", 3, "母舰美学+舰队"),
    "FTL: Faster Than Light": ("roguelike|飞船管理", 2, "飞船内舱室管理"),
    "Hardspace: Shipbreaker": ("拆船|模拟|太空", 3, "飞船结构解剖——绝佳参考"),
    "Void Bastards": ("roguelike|飞船|漫画", 1, "随机飞船探索"),
    "Everspace 2": ("太空射击|roguelike", 2, "开放太空"),
    "Rebel Galaxy": ("太空|贸易|牛仔", 1, "大舰对轰"),
    "Breathedge": ("太空生存|幽默", 1, "太空事故求生"),
    "Deliver Us The Moon": ("月球|叙事|解谜", 2, "月球基地细节"),
    "Observation": ("空间站|AI|叙事", 2, "空间站 AI 视角"),
    "Tacoma": ("空间站|叙事|沉浸", 2, "空间站全息回放"),
    "The Invincible": ("硬科幻|莱姆|叙事", 2, "莱姆原著改编"),
    "Ixion": ("世代飞船|城市管理", 4, "世代飞船城市管理——主线直接参考"),
    "Frostpunk": ("末世|城市管理|蒸汽朋克", 1, "方舟隐喻"),
    "Frostpunk 2": ("末世|城市管理", 1, "续作"),
    "Empyrion - Galactic Survival": ("太空生存|建造", 1, "自由建造"),
    "Aven Colony": ("殖民模拟", 1, "异星殖民地"),
    "Planetbase": ("殖民模拟|小体量", 1, "基地资源闭环"),
    "Stranded: Alien Dawn": ("生存|外星|殖民", 1, "异星求生"),
    "Nimbatus - The Space Drone Constructor": ("飞船建造|物理", 1, "无人机船体设计"),
    # ---- FPS / 军事 / 机甲 ----
    "Halo: The Master Chief Collection": ("军事科幻|FPS|士官长", 2, "星盟战争"),
    "Halo Infinite": ("军事科幻|FPS|开放世界", 1, "环带开放世界"),
    "Crysis": ("军事|纳米服|沙盒", 0, "纳米服"),
    "Titanfall 2": ("机甲|FPS|跑酷", 0, "泰坦战斗"),
    "MechWarrior 5: Mercenaries": ("机甲|模拟", 1, "机甲舱内视角"),
    "Armored Core VI: Fires of Rubicon": ("机甲|宫崎英高", 1, "机甲组装"),
    "BATTLETECH": ("机甲|回合|策略", 0, "回合制机甲"),
    "XCOM 2": ("战术|外星|策略", 1, "外星占领地球"),
    "Half-Life 2": ("反乌托邦|FPS|物理", 0, "17号城"),
    "Portal 2": ("解谜|AI|传送门", 1, "光圈科技设施"),
    "BioShock": ("蒸汽朋克|水下都市|反乌托邦", 2, "销魂城"),
    "BioShock Infinite": ("天空之城|蒸汽朋克", 1, "哥伦比亚"),
    "System Shock": ("空间站|AI|恐怖", 2, "SHODAN 空间站"),
    "SOMA": ("水下|意识|恐怖", 1, "意识拷贝"),
    "DEATH STRANDING DIRECTOR'S CUT": ("送快递|科幻|小岛秀夫", 1, "美国重建（导演剪辑版）"),
    "Detroit: Become Human": ("AI|叙事|仿生人", 0, "仿生人觉醒"),
    "NieR:Automata": ("AI|哲学|动作", 0, "人造人末日"),
    "Horizon Zero Dawn": ("后末日|机械兽|开放世界", 1, "机械生物生态"),
    # ---- 赛博朋克 / 近未来 ----
    "Cyberpunk 2077": ("赛博朋克|夜之城|RPG", 1, "赛博都市标杆"),
    "Deus Ex: Mankind Divided": ("赛博朋克|义体|潜行", 1, "增强人社会"),
    "Shadowrun Returns": ("赛博朋克|奇幻|回合", 0, "影遁"),
    "Observer": ("赛博朋克|恐怖|侦探", 0, "潜入他人记忆"),
    "Cloudpunk": ("赛博朋克|飞行车|叙事", 1, "垂直都市飞行"),
    "Ghostrunner": ("赛博朋克|跑酷|动作", 0, "一刀流"),
    "Stray": ("机器人城市|猫|冒险", 0, "猫视角赛博城"),
    "Signalis": ("太空恐怖|生存|复古", 2, "复古太空恐怖"),
    "Scorn": ("生物朋克|恐怖|艺术", 0, "吉格尔美学"),
    "Returnal": ("外星|循环|roguelike", 2, "异星生态+飞船残骸"),
    "The Talos Principle": ("AI|哲学|解谜", 0, "仿生人解谜"),
    "Sable": ("开放世界|艺术|探索", 1, "荒漠废船美学"),
    # ---- 星战 / 太空歌剧 ----
    "STAR WARS Jedi: Fallen Order": ("星战|动作|冒险", 1, "绝地武士"),
    "STAR WARS™: Squadrons": ("星战|空战|VR", 2, "X翼/TIE 座舱"),
    "STAR WARS™: Knights of the Old Republic": ("星战|RPG|经典", 1, "旧共和国"),
    "Everspace 2": ("太空射击|roguelike", 2, "开放太空"),
}

SPECIAL_APPID = {  # 同名重载/需要精确 appid：清单名 -> appid
    'Dead Space Remake': '1693980',
    'Mass Effect: Andromeda': '1238000',  # Steam 名带 Deluxe 后缀
}
NON_STEAM = {  # 不在 Steam 的知名科幻游戏
    'Star Citizen': ("太空模拟|众筹|飞船", 3, "非 Steam（独立启动器）；飞船细节顶级，EA 中"),
}

def norm(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())

def main():
    games = {r['app_id']: r for r in csv.DictReader(open(os.path.join(DATA, 'games.csv')))}
    reviews = {r['app_id']: r for r in csv.DictReader(open(os.path.join(DATA, 'reviews.csv')))}
    spy = {r['app_id']: r for r in csv.DictReader(open(os.path.join(DATA, 'steamspy_insights.csv')))}
    raw = list(csv.DictReader(open(os.path.join(OUT, 'scifi_games_raw.csv'))))
    raw_by_name = {}
    for r in raw:
        raw_by_name.setdefault(norm(r['name']), r)

    def steam_search(term):
        """Steam 官方搜索 API 补 appid"""
        url = 'https://store.steampowered.com/api/storesearch/?term=' + urllib.parse.quote(term) + '&l=english&cc=us'
        try:
            with urllib.request.urlopen(url, timeout=15) as resp:
                data = json.load(resp)
            for item in data.get('items', []):
                if norm(item.get('name')) == norm(term):
                    return str(item['id']), item.get('name')
        except Exception as e:
            print(f'  search error for {term}: {e}')
        return None, None

    rows, missing = [], []
    for name, (tags, ship, note) in KNOWN_GAMES.items():
        n = norm(name)
        if name in NON_STEAM:  # 非 Steam 作品：手写记录
            rows.append({'app_id': '', 'name': name, 'release_year': '', 'release_date': '',
                         'review_score_desc': '非 Steam', 'positive': 0, 'total_reviews': 0,
                         'positive_pct': 0.0, 'steamspy_owners': 0, 'price_overview': '',
                         'steam_url': 'https://robertsspaceindustries.com/',
                         'header_img': '', 'tags': tags, 'ship_ref': ship, 'note': note,
                         'match_source': 'non-steam'})
            continue
        if name in SPECIAL_APPID:  # 同名重载：按 appid 精确取
            appid = SPECIAL_APPID[name]
            g = games.get(appid)
            r = {'app_id': appid, 'name': (g or {}).get('name') or name,
                 'release_year': ((g or {}).get('release_date') or '')[:4],
                 'release_date': (g or {}).get('release_date') or '',
                 'review_score_desc': '', 'positive': 0, 'total_reviews': 0,
                 'positive_pct': 0.0, 'steamspy_owners': 0,
                 'price_overview': ((g or {}).get('price_overview') or '')[:80],
                 'steam_url': f'https://store.steampowered.com/app/{appid}/',
                 'header_img': f'https://cdn.akamai.steamstatic.com/steam/apps/{appid}/header.jpg'}
            source = 'appid'
        else:
            r = raw_by_name.get(n)
            source = 'raw'
            if not r:
                # 前缀匹配（处理 ™/Complete Edition/Director's Cut 等后缀变体）
                cands = [rn for rn in raw_by_name if rn.startswith(n)]
                if cands:
                    r = raw_by_name[sorted(cands, key=len)[0]]
                    source = 'raw-prefix'
            if not r:
                # 全量 games.csv 找
                hit = None
                for appid, g in games.items():
                    if norm(g.get('name')) == n:
                        hit = g
                        break
                if hit:
                    source = 'games.csv'
                else:
                    appid, api_name = steam_search(name)
                    if appid:
                        hit = games.get(appid)
                        source = 'api'
                    else:
                        missing.append(name)
                        continue
                r = {
                    'app_id': hit['app_id'], 'name': hit.get('name') or name,
                    'release_year': (hit.get('release_date') or '')[:4],
                    'release_date': hit.get('release_date') or '',
                    'review_score_desc': '', 'positive': 0, 'total_reviews': 0,
                    'positive_pct': 0.0, 'steamspy_owners': 0,
                    'price_overview': (hit.get('price_overview') or '')[:80],
                    'steam_url': f"https://store.steampowered.com/app/{hit['app_id']}/",
                    'header_img': f"https://cdn.akamai.steamstatic.com/steam/apps/{hit['app_id']}/header.jpg",
                }
        rv = reviews.get(r['app_id'], {})
        sp = spy.get(r['app_id'], {})
        try:
            total = int(rv.get('total') or 0)
            pos = int(rv.get('positive') or 0)
        except ValueError:
            total = pos = 0
        try:
            owners = int(sp.get('owners') or 0)
        except ValueError:
            owners = 0
        rows.append({
            **r,
            'review_score_desc': rv.get('review_score_description') or r.get('review_score_desc') or '',
            'positive': pos, 'total_reviews': total,
            'positive_pct': round(pos / total * 100, 1) if total else 0.0,
            'steamspy_owners': owners,
            'tags': tags, 'ship_ref': ship, 'note': note,
            'match_source': source,
        })
    rows.sort(key=lambda r: r['total_reviews'], reverse=True)

    fields = ['app_id', 'name', 'release_year', 'release_date', 'review_score_desc',
              'positive', 'total_reviews', 'positive_pct', 'steamspy_owners',
              'price_overview', 'steam_url', 'header_img', 'tags', 'ship_ref', 'note', 'match_source']
    with open(os.path.join(OUT, 'scifi_games_curated.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f'curated games: {len(rows)}  (known={len(KNOWN_GAMES)})')
    if missing:
        print('NOT FOUND:')
        for m in missing:
            print(f'  {m}')

if __name__ == '__main__':
    main()
