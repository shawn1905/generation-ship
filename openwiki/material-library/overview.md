---
type: material-library
title: Sci-Fi Reference Material Library
description: Curated collection of 2000+ sci-fi movies, TV shows, games, and art for design inspiration
tags: [material, reference, sci-fi]
---
# Sci-Fi Reference Material Library

The repository includes a comprehensive curated collection of post-2000 science fiction media that serves as inspiration and reference for the generation ship design. This includes movies, TV shows, games, anime, comics, novels, and original art/concept art.

## Overview

- Total curated entries: ~495
- Of these, 42 are classified as "generation ship level" reference (high quality engineering/schematic views of large ships)
- 65 are "engineering details level" reference (good engineering details of space ships)
- 121 are "appearance level" reference (good visual inspiration for ship appearance)

## Organization

The collection is organized by media type:
- `branch/movies/`: Movies and TV shows
- `branch/anime/`: Anime
- `branch/comics/`: Comics
- `branch/games/`: Games
- `branch/novels/`: Novels
- `branch/art/`: Original art, concept art, and 3D models

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

Tags are stored as comma (or pipe) separated values in the curated CSV files. In the interactive gallery, tags are used to filter entries by content themes (e.g. "interstellar travel", "hard sci-fi", "space colony", "interior", "exterior").

## Interactive Gallery

All curated entries are available in an interactive HTML gallery that supports:
- Filtering by category, tag, and reference level
- Full text search
- Viewing posters, covers, and reference images
- Reading notes about each entry

See [Interactive Gallery](./gallery.md) for more details.

## Data Sources

The raw data is collected from:
- IMDb for movies and TV shows
- AniList for anime and manga
- Open Library for novels
- Sketchfab for 3D models
- Blender Artists forum for 3D art
- Wikipedia for general information

## Generation Pipeline

The gallery is generated from curated CSV data using Python scripts. See [Generation Pipeline](./generation-pipeline.md) for how it works.

## Related Pages
- [Interactive Gallery](./gallery.md)
- [Generation Pipeline](./generation-pipeline.md)
