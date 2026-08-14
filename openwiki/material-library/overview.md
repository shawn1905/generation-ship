---
type: material-library
title: Sci-Fi Reference Material Library
description: Curated collection of 1980+ sci-fi movies, TV shows, games, anime, comics, novels, art, and AI-curated future inspiration for the generation ship design
tags: [material, reference, sci-fi]
---
# Sci-Fi Reference Material Library

The repository includes a comprehensive curated collection of science fiction media that serves as inspiration and reference for the generation ship design. This includes movies, TV shows, games, anime, comics, novels, original art/concept art, and an "Other / AI-curated" category for future inspiration beyond the ship-design rating scale.

## Overview

- Total curated entries: **533** (as shown by the current `gallery.html` tabs)
- Media scope: movies/TV span **1980+**, games span **2000+**, plus classic-boundary entries in anime/comics/novels
- Of the seven rated categories, 42 are classified as "generation ship level" reference (✧4), 63 as "engineering details level" (✧3), and 120 as "appearance level" (✧2). The 🧠 Other/AI-curated category is deliberately unrated (all `ship_ref` = 0)
- Note: `branch/README.md` and `docs/科幻素材库-2000后.md` still show the earlier 7-category / 495-entry numbers; the gallery (8 tabs, 533) is the current artifact

## Organization

The collection is organized by media type:
- `branch/movies/`: Movies and TV shows (curated + raw CSVs)
- `branch/anime/`: Anime
- `branch/comics/`: Comics
- `branch/games/`: Games
- `branch/novels/`: Novels
- `branch/art/`: Original art, concept art, and 3D models (Wikipedia/Goodreads art + Sketchfab + Blender Artists forum)
- `branch/other/`: 🧠 Other/AI-curated future inspiration (39 entries; see below)

### 🧠 Other / AI-curated (每日扩充)

A separate category added for "future inspiration" that does not fit the ship-design rating scale: megastructures, future cities, post-human concepts, science frontiers, music, and niche indie/underground finds. Every entry carries `ship_ref` = 0 by rule.

- Data: `branch/other/ai_curated.csv` (9 columns: `title,type,artist,year,tags,ship_ref,note,url,source_id`)
- Covers: `branch/other/covers/{source_id}.jpg`, fetched via `branch/scripts/fetch_other_covers.py` (`PLAN` dict supports `wiki`/`url`/`goodreads`/`web` sources)
- Expansion flow and selection criteria live in `branch/other/README.md` (deep-dive-first selection principle, ~3-8 entries per day)
- Every expansion must pass `branch/scripts/health_check_other.py` (column alignment, cover existence, URL reachability) before pushing

## Reference Level Classification

Each reference is classified by how useful it is for generation ship design (0-4 scale):
- ✧4: **Generation ship level**: Direct depiction of large generation ships or space colonies with detailed engineering views
- ✧3: **Engineering details level**: Detailed engineering views of large space ships
- ✧2: **Appearance level**: Good visual inspiration for ship appearance
- ✧1: **General sci-fi inspiration**: Interesting sci-fi concepts, but not detailed ship design
- ✧0: **No/weak reference**: Interesting sci-fi concept but not useful for ship design reference

## Raw vs Curated Data

The curation process combines automated raw dataset collection with manual selection:

- **Raw CSV files**: These contain all sci-fi entries automatically filtered from large datasets (IMDb for movies/TV, etc.). They include all basic metadata but no manual curation.
- **Curated CSV files**: These are manually processed files that include:
  - Only entries selected as relevant to generation ship design inspiration
  - Manual assignment of reference levels
  - Manual assignment of content tags
  - Manual notes explaining relevance to generation ship design

## Manual Curation Process

Manual entries (KNOWN_MOVIES, etc.) defined in the curation scripts are matched to raw dataset records by (title, year) combination. When a match is found, the manual information (tags, reference level, notes) is merged with the raw metadata to create the final curated CSV.

## Tags

Tags are stored as pipe-separated Chinese values in the curated CSV files (e.g. `世代飞船|硬科幻|黑洞|环形空间站`). In the interactive gallery, tags are used to filter entries by content themes (e.g. "interstellar travel", "hard sci-fi", "space colony", "interior", "exterior"). Note for editors: never use ASCII commas inside `note` values - they shift the CSV columns and break the gallery (detected by `health_check_other.py`).

## Interactive Gallery

All curated entries are available in an interactive HTML gallery that supports:
- Filtering by category (8 tabs), tag, and reference level
- Full text search
- Viewing posters, covers, and reference images
- Reading notes about each entry

See [Interactive Gallery](./gallery.md) for more details.

## Data Sources

The raw data is collected from:
- IMDb (official datasets + suggestion JSON API for posters) for movies and TV shows
- steam-insights snapshot (NewbieIndieGameDev) for games
- AniList GraphQL for anime and manga
- Open Library for novels
- Wikipedia REST summary for art/artist verification and covers
- Goodreads search for art-book covers
- Sketchfab API and Blender Artists forum (Discourse JSON) for 3D community works

The curated list in `docs/灵感来源地图_20260811.md` tracks further candidate sources (Erik Wernquist's *Wanderers*, NASA 3D Resources, Poly Haven, generation-ship novels, etc.) with link-verification status; it feeds future curation rounds.

## Generation Pipeline

The gallery is generated from curated CSV data using Python scripts. See [Generation Pipeline](./generation-pipeline.md) for how it works.

## Relationship to Original Creation

The curation process also feeds the project's own creative output: ideas encountered while curating the AI-selected entries are logged in [Self-Produced Creation Content](../creative/creation.md) (灵感笔记), and several finished works (short stories, music, AI concept art) grew out of material-library entries.

## Related Pages
- [Interactive Gallery](./gallery.md)
- [Generation Pipeline](./generation-pipeline.md)
- [Self-Produced Creation Content](../creative/creation.md)
