---
type: material-library
title: Gallery Generation Pipeline
description: Documentation for the Python scripts that curate reference data and generate the interactive gallery HTML and human-readable summaries
tags: [material, pipeline, code]
---
# Gallery Generation Pipeline

The interactive gallery is generated automatically from curated CSV data using Python scripts in `/branch/scripts/`. This page documents how the pipeline works, how to reproduce it, and the pitfalls recorded while building it.

## Pipeline Overview

1. Download raw IMDb datasets from https://datasets.imdbws.com/ and place them in `/branch/data/` (git-ignored, ~1.4 GB)
2. Run raw data collection scripts (`make_movies.py`, `make_games.py`) to filter sci-fi candidates
3. Run curation scripts (`curate_*.py`) to merge manual annotations (`KNOWN_*` dictionaries) with raw data
4. Download cover/poster images (`download_images.py`, `download_covers.py`, `fetch_other_covers.py`)
5. Run `make_gallery.py` to produce the single-file `branch/gallery.html`
6. Optionally run `make_docs.py` to regenerate `docs/科幻素材库-2000后.md` (7 rated categories only - the 🧠 Other/AI-curated category is not included; see Backlog)

## Known Issues with IMDb Dataset

The original IMDb dataset has an issue with genre tagging: many sci-fi movies are not tagged as "Sci-Fi" in the dataset, or are mis-classified (Avatar, Blade Runner 2049 and Ad Astra all lack the tag). Automated filtering alone would miss many relevant sci-fi works, so the curation process matches a manual list of known works against the full candidate pool (`*_pool.csv`) by (title, year) instead of relying on genre tags.

## KNOWN_MOVIES Workaround

To address the issue with incomplete genre tagging, the curation process uses a manual list of known sci-fi movies (`KNOWN_MOVIES`, and the analogous `KNOWN_TV` / `KNOWN_GAMES` / etc.) defined directly in the curation scripts. This ensures that all relevant works are included even if they were missed by automated filtering.

- Each manual entry maps `(title, year) -> (tags, ship_ref, note)`
- A `None` value marks a work as **deliberately removed** (e.g. 疯狂的外星人, 独行月球, 上海堡垒); re-running the script will not resurrect it
- Pitfall: matching a year-specified entry must NOT fall back to empty-year matching - a bare `by_norm` fallback once matched Aliens to an unrelated 2014 short film (see `curate_movies.py` / `curate_tv.py`)

## Poster / Cover Image Acquisition

- **Movies & TV**: posters come from the IMDb suggestion JSON API (`v2.sg.media-imdb.com`, no key required). The original plan used the `cinemagoer` library, but its 2026 version has a local-database dependency issue, so it is unused. The suggestion API rate-limits (SSL EOF errors), so the download script sleeps ~2s between requests with 3 retries
- **Games**: Steam CDN `https://cdn.akamai.steamstatic.com/steam/apps/{appid}/header.jpg` (Star Citizen uses an official YouTube trailer thumbnail)
- **Anime/Comics**: AniList cover images; Wikipedia REST for Western comics; Open Library for some (e.g. Letter 44)
- **Novels**: Open Library covers via `ratings.json` lookups
- **Art**: Wikipedia REST person images + Goodreads book-cover scraping (`search` page -> book id -> og:image), with 1s+ intervals because Goodreads rate-limits and occasionally throws SSL EOF
- **Other/AI-curated**: `fetch_other_covers.py` with a `PLAN` dict supporting `wiki` / `url` / `goodreads` / `web` (og:image) sources
- Sketchfab thumbnails are downloaded with `curl` (urllib gets reset by the CDN) and resized to 500px with `sips`; the search API's `thumbnails.images` first item may be 50x50, so the widest image is selected

## End-to-End Reproduction Workflow

### Prerequisites
- Python 3 (the repo uses a `branch/.venv` virtualenv; HANDOVER records Python 3.14)
- IMDb datasets downloaded into `branch/data/` (git-ignored - a new machine must re-download them; the scripts are ready)

### Step 1: Install / Prepare
```bash
python3 -m venv branch/.venv
# The curation/gallery scripts use only the Python standard library (csv, urllib, json).
# The poster download path uses the IMDb suggestion API; cinemagoer is NOT used.
```

### Step 2: Download Raw Datasets
Download the following files from https://datasets.imdbws.com/ into `branch/data/`:
- title.basics.tsv.gz
- title.ratings.tsv.gz
Plus the steam-insights snapshot for games.

### Step 3: Generate Raw Data
```bash
cd branch
.venv/bin/python scripts/make_movies.py   # IMDb -> raw + candidate pool (1980+, Sci-Fi with votes)
.venv/bin/python scripts/make_games.py    # steam-insights -> raw
```

### Step 4: Run Curation
```bash
.venv/bin/python scripts/curate_movies.py
.venv/bin/python scripts/curate_tv.py
.venv/bin/python scripts/curate_games.py    # SPECIAL_APPID / NON_STEAM special-cases
.venv/bin/python scripts/curate_anime_comics.py  # AniList + Wikipedia verification
.venv/bin/python scripts/fix_anime_comics.py     # targeted fixes (灵笼 / 铁血孤儿 / Wikipedia disambiguation)
.venv/bin/python scripts/curate_novels.py        # Open Library verification / ratings / covers
.venv/bin/python scripts/curate_art.py           # art books: Wikipedia REST verify + Goodreads covers
.venv/bin/python scripts/collect_sketchfab.py    # 3D community: Sketchfab API, like-count sort, ✧4 whitelist
.venv/bin/python scripts/collect_blenderartists.py # 3D community: Blender forum Discourse API
```

### Step 5: Download Images
```bash
.venv/bin/python scripts/download_images.py      # movies/TV/games
.venv/bin/python scripts/download_covers.py      # anime/comics/novels
.venv/bin/python scripts/fetch_other_covers.py   # 🧠 Other/AI-curated covers
.venv/bin/python scripts/fix_art_covers.py       # art covers with source_id slug mismatches
```

### Step 6: Generate Gallery + Summary
```bash
.venv/bin/python scripts/make_gallery.py   # -> branch/gallery.html
.venv/bin/python scripts/make_docs.py      # -> docs/科幻素材库-2000后.md (7 categories only)
.venv/bin/python scripts/health_check_other.py  # must pass after every Other-category expansion
```

## Scripts

All scripts are located in `/branch/scripts/`:

### 1. Data Collection Scripts
- `make_movies.py`: Filter sci-fi movies/TV from the IMDb dataset -> raw CSVs + candidate pools
- `make_games.py`: Filter games from the steam-insights snapshot -> raw CSV
- `collect_sketchfab.py`: Collect 3D models from Sketchfab API (like-count sort, rating quotas, ✧4 whitelist)
- `collect_blenderartists.py`: Collect 3D art from the Blender forum Discourse API (23 keywords + exclusion list + rating fixes)

These scripts collect the basic information (title, year, rating, image URL) for all candidates.

### 2. Curation Scripts
- `curate_movies.py` / `curate_tv.py` / `curate_games.py`: Merge manual `KNOWN_*` lists with raw data
- `curate_anime_comics.py`: Anime/comics curation with AniList + Wikipedia verification
- `curate_novels.py`: Novels with Open Library verification/ratings/covers
- `curate_art.py`: Art books and concept artists (Wikipedia REST verify + Goodreads covers)
- `fix_anime_comics.py` / `fix_art_covers.py`: Targeted fixes for specific titles and cover mismatches

After collection, the raw data is manually curated to:
- Select only relevant entries that are worth including
- Assign tags based on content
- Assign reference level (how useful it is for generation ship design)
- Add notes explaining why the entry is relevant

### 3. Image Download Scripts
- `download_images.py`: Movie/TV posters and game headers (IMDb suggestion API + Steam CDN)
- `download_covers.py`: Anime/comics/novels covers
- `fetch_other_covers.py`: 🧠 Other/AI-curated covers (wiki/url/goodreads/web sources)
- `fix_art_covers.py`: Repair art covers whose files don't match `source_id` slugs

### 4. Output Generation Scripts
- `make_gallery.py`: Takes the curated CSV files and generates the complete `gallery.html`
  - Includes all the data embedded in the HTML file (JSON blobs per category)
  - Generates the JavaScript for filtering and searching
  - Outputs a single self-contained HTML file that works completely offline
- `make_docs.py`: Generates the human-readable `docs/科幻素材库-2000后.md` (7 rated categories; the Other/AI-curated category is not loaded - see Backlog)
- `weread_links.py`: One-off utility that queries the WeChat Reading (weread) search API to produce `docs/weread-直达链接.md` deep links (`book-detail?type=1&v={hash}`; do not hand-build `web/bookDetail/{id}` - 404)
- `health_check_other.py`: Health check for `other/ai_curated.csv` - verifies column count (9), cover files exist and are >5KB, and URLs return 200. **Must be run after every Other-category expansion**

## Image Cache Storage

Images are cached locally in these paths:
- `/branch/movies/posters/`: Movie posters (`{tconst}.jpg`, 460px wide)
- `/branch/movies/tv_posters/`: TV show posters
- `/branch/games/headers/`: Game header images (`{appid}.jpg`)
- `/branch/anime/covers/`: Anime covers
- `/branch/comics/covers/`: Comic covers
- `/branch/novels/covers/`: Novel covers
- `/branch/art/covers/`: Art covers (Wikipedia/Goodreads)
- `/branch/art/covers_3d/`: Sketchfab renders (500px)
- `/branch/art/covers_forum/`: Blender forum renders (500px)
- `/branch/other/covers/`: Other/AI-curated covers

### Git Tracking
- Curated CSVs, scripts, gallery.html and the local image caches **are all committed to git** (posters/covers regenerate only when needed)
- Only these paths are ignored (see `.gitignore`): `branch/data/` (raw IMDb datasets), `branch/movies/movie_pool.csv` and `tv_pool.csv` (candidate pools, regenerable), `scifi_movies_curated_auto.csv` (intermediate), `branch/.venv/`, `__pycache__/`

## Data Format

Curated data is stored as CSV files:
- `scifi_movies_curated.csv`: Curated movies
- `scifi_tv_curated.csv`: Curated TV shows
- `scifi_games_curated.csv`: Curated games
- `scifi_anime_curated.csv`: Curated anime
- `scifi_comics_curated.csv`: Curated comics
- `scifi_novels_curated.csv`: Curated novels
- `scifi_art_curated.csv` / `sketchfab_curated.csv` / `blenderartists_curated.csv`: Art and 3D models
- `other/ai_curated.csv`: 🧠 Other/AI-curated future inspiration (9 columns)

Each CSV includes:
- Title, year, creator/author/director, rating (IMDb / Steam positive % / AniList score / Open Library stars / type·artist for art)
- Tags (pipe-separated)
- Reference level (`ship_ref`: 0-4)
- Notes about relevance
- URL and cover source
- Path to local poster/cover image (derived from `source_id`/`tconst`/`app_id` slug at gallery build time)

## Recorded Pitfalls (from HANDOVER.md)

1. **AniList 403 rate limiting**: batch requests trigger IP-level throttling; fix is a standard UA + 1s interval + 30s sleep-and-retry on 403
2. **同名不同年份误配**: a year-specified manual entry must never fall back to empty-year matching (see KNOWN_MOVIES above)
3. **Gallery image path double prefix**: `anime/anime/covers/...` breaks all anime/comics covers - the `img` variable already contains the prefix; don't re-concatenate
4. **中文标题 norm 陷阱**: 「三体」 normalizes to an empty string and can match the Norwegian series "Ø"; match IMDb English titles instead
5. **Wikipedia REST 404/no-thumbnail**: missing articles (Letter 44, Aama) get hand-written entries with honest notes; disambiguation pages need suffixes like `(comics)`
6. **IMDb poster throttling**: SSL EOF -> 2s interval + 3 retries
7. **Sketchfab thumbnails**: first `thumbnails.images` item may be 50x50; take the widest; download with curl (browser UA) not urllib; `sips` downscale to 500px
8. **Blender forum images**: exclude-list accumulates (40+ keywords) to filter plugin announcements; some topic images are `.png` so size-parsing (`_WxH`) selects the largest image instead of excluding by extension; if the first post has no image, scan the first 3 posts; `SHIP_OVERRIDE` corrects ratings (e.g. Skyport 天空港 -> ✧4)

## Related Pages
- [Overview](./overview.md)
- [Interactive Gallery](./gallery.md)
- [Toolchain](../references/toolchain.md)
