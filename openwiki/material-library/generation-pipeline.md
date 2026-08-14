---
type: material-library
title: Gallery Generation Pipeline
description: Documentation for the Python scripts that generate the interactive gallery from curated CSV data
tags: [material, pipeline, code]
---
# Gallery Generation Pipeline

The interactive gallery is generated automatically from curated CSV data using Python scripts in `/branch/scripts/`. This page documents how the pipeline works.

## Pipeline Overview

1. Download raw IMDb datasets from https://datasets.imdbws.com/
2. Place datasets in `/branch/data/`
3. Run raw data collection scripts to filter sci-fi entries
4. Run curation scripts to merge manual annotations with raw data
5. Download cover/poster images
6. Run gallery generation script to produce the final HTML

## Known Issues with IMDb Dataset

The original IMDb dataset has an issue with genre tagging: many sci-fi movies are not tagged as "Sci-Fi" in the dataset, or miss-classified. This means that automated filtering alone would miss many relevant sci-fi works.

## KNOWN_MOVIES Workaround

To address the issue with incomplete genre tagging, the curation process uses a manual list of known sci-fi movies (KNOWN_MOVIES) defined directly in the curation script. This ensures that all relevant movies are included even if they were missed by automated filtering.

The manual list is matched to raw dataset records by (title, year) combination, and the manual annotations are merged into the final curated output.

## Poster Image Acquisition

The original plan used the cinemagoer library to fetch poster images, but this was replaced with direct downloading from the IMDb website via the OMDB API because:
- cinemagoer didn't provide reliable access to high-quality poster images
- The API approach is more reliable for getting consistent image sizes

## End-to-End Reproduction Workflow

### Prerequisites
- Python 3.7+
- pip

### Step 1: Install Dependencies
```
pip install pandas requests imdbpy aiohttp beautifulsoup4
```

### Step 2: Download Raw Datasets
Download the following files from https://datasets.imdbws.com/:
- title.basics.tsv.gz
- title.ratings.tsv.gz

Place these files in `/branch/data/`

### Step 3: Generate Raw Movie/TV Data
```
cd /branch/scripts
python make_movies.py
python make_games.py
```

### Step 4: Run Curation
```
python curate_movies.py
python curate_tv.py
python curate_games.py
python curate_anime_comics.py
python curate_novels.py
python curate_art.py
```

### Step 5: Download Images
```
python download_images.py
python download_covers.py
python fetch_other_covers.py
```

### Step 6: Generate Gallery
```
python make_gallery.py
```

This will output the final `/branch/gallery.html` file.

## Scripts

All scripts are located in `/branch/scripts/`:

### 1. Data Collection Scripts
- `make_movies.py`: Filter sci-fi movies and TV from the IMDb dataset
- `make_games.py`: Collect game data
- `collect_sketchfab.py`: Scrape 3D models from Sketchfab
- `collect_blenderartists.py`: Scrape 3D art from Blender Artists forum

These scripts collect the basic information (title, year, rating, image URL) for all candidates.

### 2. Curation Scripts
- `curate_movies.py`: Merge manual KNOWN_MOVIES with raw IMDb data
- `curate_tv.py`: Curate TV shows
- `curate_games.py`: Curate games
- `curate_anime_comics.py`: Curate anime and comics
- `curate_novels.py`: Curate novels
- `curate_art.py`: Curate art and concept art

After collection, the raw data is manually curated to:
- Select only relevant entries that are worth including
- Assign tags based on content
- Assign reference level (how useful it is for generation ship design)
- Add notes explaining why the entry is relevant

### 3. Image Download Scripts
- `download_images.py`: Download poster images from IMDb
- `download_covers.py`: Download cover images from various sources
- `fetch_other_covers.py`: Fix missing covers

### 4. Gallery Generation Script
- `make_gallery.py`: Takes the curated CSV files and generates the complete `gallery.html`
- Includes all the data embedded in the HTML file
- Generates the JavaScript for filtering and searching
- Outputs a single self-contained HTML file that works completely offline

## Image Cache Storage

Images are cached locally in these paths:
- `/branch/movies/posters/`: Movie posters
- `/branch/movies/tv_posters/`: TV show posters
- `/branch/games/headers/`: Game header images
- `/branch/anime/covers/`: Anime covers
- `/branch/comics/covers/`: Comic covers
- `/branch/novels/covers/`: Novel covers
- `/branch/art/covers/`: Art covers
- `/branch/art/covers_3d/`: 3D model covers

### Image Path Construction
- For movies: `/{tconst}.jpg` where tconst is the IMDb ID
- For TV shows: Similar to movies, uses the IMDb ID as the filename
- For games: Each game has an ID, and the image path is constructed based on that ID
- For other media: Paths are constructed based on the entry ID in the curated CSV

### Missing Image Handling
- The gallery checks if the local image file exists before displaying it
- If an image is missing, the gallery shows a placeholder "No image available" message instead of a broken image link

### Git Tracking
- Large image cache directories are excluded from git via `.gitignore`
- Only the curated CSV data is tracked in git
- You can regenerate the image cache by running the download scripts

## Data Format

Curated data is stored as CSV files:
- `scifi_movies_curated.csv`: Curated movies
- `scifi_tv_curated.csv`: Curated TV shows
- `scifi_anime_curated.csv`: Curated anime
- `scifi_comics_curated.csv`: Curated comics
- `scifi_novels_curated.csv`: Curated novels
- Various CSV files for art and 3D models

Each CSV includes:
- Title
- Year
- Creator/Director
- Rating
- Tags (comma-separated)
- Reference level
- Notes about relevance
- Path to local poster/cover image

## Related Pages
- [Overview](./overview.md)
- [Interactive Gallery](./gallery.md)
- [Toolchain](../references/toolchain.md)
