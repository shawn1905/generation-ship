#!/usr/bin/env python3
"""电影侧：从 IMDb 官方数据集过滤 2000+ 科幻电影。
输出：
  branch/movies/scifi_movies_raw.csv     全量（type=movie, sci-fi, 2000+, 有票数）
  branch/movies/scifi_movies_curated.csv 精选（numVotes >= 5000），留人工标签列
数据源：https://datasets.imdbws.com/  (IMDb 非商业数据集)
"""
import csv, gzip, os, sys

DATA = os.path.join(os.path.dirname(__file__), '..', 'data')
OUT = os.path.join(os.path.dirname(__file__), '..', 'movies')
os.makedirs(OUT, exist_ok=True)

def read_basics(ttype_filter, genres_req=('Sci-Fi',)):
    """tconst -> (title, year, runtime, genres)。genres_req=None 表示不限类型"""
    hits = {}
    with gzip.open(os.path.join(DATA, 'title.basics.tsv.gz'), 'rt', encoding='utf-8') as f:
        r = csv.reader(f, delimiter='\t')
        next(r)
        for row in r:
            if len(row) < 9:
                continue
            tconst, ttype, ptitle, otitle, adult, syear, eyear, runtime, genres = row[:9]
            if ttype not in ttype_filter or adult == '1':
                continue
            if not (syear.isdigit() and 2000 <= int(syear) <= 2025):
                continue
            if genres == r'\N':
                if genres_req is not None:
                    continue
            elif genres_req is not None and 'Sci-Fi' not in genres.split(','):
                continue
            hits[tconst] = (ptitle, int(syear), runtime, genres)
    return hits

def read_ratings():
    out = {}
    with gzip.open(os.path.join(DATA, 'title.ratings.tsv.gz'), 'rt', encoding='utf-8') as f:
        r = csv.reader(f, delimiter='\t')
        next(r)
        for tconst, rating, votes in r:
            out[tconst] = (float(rating), int(votes))
    return out

def main():
    ratings = read_ratings()

    def build(ttype, outname, label):
        print(f'reading basics ({label})...')
        basics = read_basics(ttype)
        print(f'  sci-fi {label} 2000+: {len(basics)}')
        rows = []
        for tc, (title, year, runtime, genres) in basics.items():
            rating, votes = ratings.get(tc, (0.0, 0))
            if votes == 0:
                continue
            rows.append({'tconst': tc, 'title': title, 'year': year,
                         'runtime_min': runtime, 'genres': genres,
                         'imdb_rating': rating, 'num_votes': votes,
                         'imdb_url': f'https://www.imdb.com/title/{tc}/'})
        rows.sort(key=lambda r: r['num_votes'], reverse=True)
        print(f'  with votes: {len(rows)}')
        with open(os.path.join(OUT, outname), 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)
        return rows

    def build_pool(ttype, outname, label):
        """全量候选池：2000+ 有票，不限类型（IMDb 类型标签不可靠，Avatar/BR2049 都没标 Sci-Fi）"""
        print(f'reading basics pool ({label})...')
        basics = read_basics(ttype, genres_req=None)
        print(f'  all {label} 2000+: {len(basics)}')
        rows = []
        for tc, (title, year, runtime, genres) in basics.items():
            rating, votes = ratings.get(tc, (0.0, 0))
            if votes == 0:
                continue
            rows.append({'tconst': tc, 'title': title, 'year': year,
                         'runtime_min': runtime, 'genres': genres,
                         'imdb_rating': rating, 'num_votes': votes,
                         'imdb_url': f'https://www.imdb.com/title/{tc}/'})
        rows.sort(key=lambda r: r['num_votes'], reverse=True)
        print(f'  pool with votes: {len(rows)}')
        with open(os.path.join(OUT, outname), 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)
        return rows

    fields = ['tconst', 'title', 'year', 'runtime_min', 'genres',
              'imdb_rating', 'num_votes', 'imdb_url']
    rows = build(('movie',), 'scifi_movies_raw.csv', 'movies')
    build_pool(('movie',), 'movie_pool.csv', 'movies')

    curated = [r for r in rows if r['num_votes'] >= 5000]
    cfields = fields + ['tags', 'ship_ref', 'note']
    with open(os.path.join(OUT, 'scifi_movies_curated_auto.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=cfields)
        w.writeheader()
        for r in curated:
            r['tags'] = ''
            r['ship_ref'] = ''
            r['note'] = ''
            w.writerow(r)
    print(f'auto-curated movies (votes>=5000): {len(curated)}')

    build(('tvSeries', 'tvMiniSeries'), 'scifi_tv_raw.csv', 'TV series')
    build_pool(('tvSeries', 'tvMiniSeries'), 'tv_pool.csv', 'TV series')

if __name__ == '__main__':
    main()
