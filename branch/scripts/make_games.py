#!/usr/bin/env python3
"""游戏侧：从 steam-insights (2024-10 Steam 全量快照) 过滤科幻游戏。
输出：
  branch/games/scifi_games_raw.csv     全量（含 Sci-fi / Space 相关标签）
  branch/games/scifi_games_curated.csv 精选（好评率>=80% 且评价数>=500，或 SteamSpy 玩家数足够）
数据源：https://github.com/NewbieIndieGameDev/steam-insights
"""
import csv, os

DATA = os.path.join(os.path.dirname(__file__), '..', 'data', 'steam')
OUT = os.path.join(os.path.dirname(__file__), '..', 'games')
os.makedirs(OUT, exist_ok=True)

SCI_TAGS = {'sci-fi', 'space', 'spaceships', 'space sim', 'mars', 'sci-fi rpg',
            'cyberpunk', 'mechs', 'spacesim', 'scifi'}

def load_csv(name):
    with open(os.path.join(DATA, name), newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def clean(v):
    return (v or '').strip()

def main():
    games = {r['app_id']: r for r in load_csv('games.csv')}
    tags = load_csv('tags.csv')
    reviews = {r['app_id']: r for r in load_csv('reviews.csv')}
    spy = {r['app_id']: r for r in load_csv('steamspy_insights.csv')}
    print(f'games={len(games)} tags={len(tags)} reviews={len(reviews)}')

    # app 集合：带 sci-fi 相关标签
    sci_apps = set()
    for r in tags:
        if clean(r['tag']).lower() in SCI_TAGS:
            sci_apps.add(r['app_id'])
    print(f'games with sci-fi-ish tags: {len(sci_apps)}')

    rows = []
    for appid in sci_apps:
        g = games.get(appid)
        if not g or clean(g.get('type')) != 'game':
            continue
        rd = clean(g.get('release_date'))
        if not rd or not rd[:4].isdigit() or int(rd[:4]) < 2000:
            continue
        rv = reviews.get(appid, {})
        try:
            total = int(clean(rv.get('total')) or 0)
            pos = int(clean(rv.get('positive')) or 0)
        except ValueError:
            total = pos = 0
        pct = (pos / total * 100) if total else 0.0
        sp = spy.get(appid, {})
        try:
            owners = int(clean(sp.get('owners')) or 0)
        except ValueError:
            owners = 0
        rows.append({
            'app_id': appid,
            'name': clean(g.get('name')),
            'release_year': rd[:4],
            'release_date': rd,
            'review_score_desc': clean(rv.get('review_score_description')),
            'positive': pos, 'total_reviews': total,
            'positive_pct': round(pct, 1),
            'steamspy_owners': owners,
            'price_overview': clean(g.get('price_overview'))[:80],
            'steam_url': f'https://store.steampowered.com/app/{appid}/',
            'header_img': f'https://cdn.akamai.steamstatic.com/steam/apps/{appid}/header.jpg',
        })
    rows.sort(key=lambda r: r['total_reviews'], reverse=True)
    print(f'games 2000+ with sci-fi tag: {len(rows)}')

    fields = ['app_id', 'name', 'release_year', 'release_date', 'review_score_desc',
              'positive', 'total_reviews', 'positive_pct', 'steamspy_owners',
              'price_overview', 'steam_url', 'header_img']
    with open(os.path.join(OUT, 'scifi_games_raw.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    # 精选：好评率>=80% 且 (评价数>=1000 或 玩家数>=200000)
    curated = [r for r in rows if r['positive_pct'] >= 80 and
               (r['total_reviews'] >= 1000 or r['steamspy_owners'] >= 200000)]
    cfields = fields + ['tags', 'ship_design_ref', 'note']
    with open(os.path.join(OUT, 'scifi_games_curated.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=cfields)
        w.writeheader()
        for r in curated:
            r['tags'] = ''
            r['ship_design_ref'] = ''
            r['note'] = ''
            w.writerow(r)
    print(f'curated: {len(curated)}')
    for r in curated[:20]:
        print(f"  {r['release_year']}  {r['positive_pct']:>5}%  {r['total_reviews']:>7}r  {r['name'][:45]}")

if __name__ == '__main__':
    main()
