import json
#!/usr/bin/env python3
"""图片收集：电影/剧集海报（IMDb cover，cinemagoer）+ 游戏封面（Steam CDN）。
输出：movies/posters/{tconst}.jpg  movies/tv_posters/{tconst}.jpg  games/headers/{appid}.jpg
"""
import csv, os, sys, time, urllib.request

ROOT = os.path.join(os.path.dirname(__file__), '..')
UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Safari/537.36'}

def fetch(url, dest, timeout=30):
    if os.path.exists(dest) and os.path.getsize(dest) > 2000:
        return 'cached'
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read()
        if len(data) < 2000:
            return 'too-small'
        with open(dest, 'wb') as f:
            f.write(data)
        return 'ok'
    except Exception as e:
        return f'err:{e}'

def imdb_cover(tconst):
    """IMDb suggestion JSON API 取海报 URL（免 key 免登录）"""
    url = f'https://v2.sg.media-imdb.com/suggestion/t/{tconst}.json'
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.load(resp)
        img = data['d'][0]['i']['imageUrl']
        # 换成 460px 宽海报，省空间
        return img.replace('._V1_.jpg', '._V1_QL75_UX460_.jpg')
    except Exception:
        return None

def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None  # 测试用：只处理指定 tconst

    # 电影
    mdir = os.path.join(ROOT, 'movies', 'posters')
    os.makedirs(mdir, exist_ok=True)
    mrows = [r for r in csv.DictReader(open(os.path.join(ROOT, 'movies', 'scifi_movies_curated.csv')))]
    if only:
        mrows = [r for r in mrows if r['tconst'] == only]

    ok = fail = 0
    for i, r in enumerate(mrows):
        dest = os.path.join(mdir, r['tconst'] + '.jpg')
        if os.path.exists(dest) and os.path.getsize(dest) > 2000:
            ok += 1
            continue
        url = imdb_cover(r['tconst'])
        if not url:
            fail += 1
            print(f'  [{i+1}/{len(mrows)}] no cover: {r["title"]}')
            time.sleep(0.4)
            continue
        st = fetch(url, dest)
        if st == 'ok':
            ok += 1
        else:
            fail += 1
            print(f'  [{i+1}/{len(mrows)}] {st}: {r["title"]}')
        time.sleep(0.4)
    print(f'movies: ok={ok} fail={fail}')

    # 剧集
    tdir = os.path.join(ROOT, 'movies', 'tv_posters')
    os.makedirs(tdir, exist_ok=True)
    trows = [r for r in csv.DictReader(open(os.path.join(ROOT, 'movies', 'scifi_tv_curated.csv')))]
    if only:
        trows = [r for r in trows if r['tconst'] == only]
    ok = fail = 0
    for i, r in enumerate(trows):
        dest = os.path.join(tdir, r['tconst'] + '.jpg')
        if os.path.exists(dest) and os.path.getsize(dest) > 2000:
            ok += 1
            continue
        url = imdb_cover(r['tconst'])
        if not url:
            fail += 1
            print(f'  [{i+1}/{len(trows)}] no cover: {r["title"]}')
            time.sleep(0.4)
            continue
        st = fetch(url, dest)
        if st == 'ok':
            ok += 1
        else:
            fail += 1
            print(f'  [{i+1}/{len(trows)}] {st}: {r["title"]}')
        time.sleep(0.4)
    print(f'tv: ok={ok} fail={fail}')

    # 游戏（Steam CDN 免限速）
    gdir = os.path.join(ROOT, 'games', 'headers')
    os.makedirs(gdir, exist_ok=True)
    grows = [r for r in csv.DictReader(open(os.path.join(ROOT, 'games', 'scifi_games_curated.csv'))) if r['app_id']]
    ok = fail = 0
    for i, r in enumerate(grows):
        dest = os.path.join(gdir, r['app_id'] + '.jpg')
        st = fetch(r['header_img'], dest)
        if st in ('ok', 'cached'):
            ok += 1
        else:
            fail += 1
            print(f'  [{i+1}/{len(grows)}] {st}: {r["name"]}')
        time.sleep(0.15)
    print(f'games: ok={ok} fail={fail}')

if __name__ == '__main__':
    main()
