---
type: material-library
title: Interactive Reference Gallery
description: Documentation for the interactive HTML reference gallery
tags: [material, gallery, interactive]
---
# Interactive Reference Gallery

The interactive gallery is a pure HTML/JavaScript file that lets you browse the entire curated reference collection. It supports filtering, searching, and sorting by various criteria.

## Opening the Gallery

The gallery is located at `/branch/gallery.html`. Simply open it in any modern web browser. It doesn't require any internet connection or server - it's a pure static file that works completely locally **without any external services**. It is also published online via GitHub Pages at [https://shawn1905.github.io/generation-ship/branch/gallery.html](https://shawn1905.github.io/generation-ship/branch/gallery.html).

## Features

### Filtering Capabilities

The gallery supports multiple ways to filter the entries:

1. **By content category** (8 tabs):
   - Movies
   - TV Shows
   - Games
   - Anime
   - Comics
   - Novels
   - Original Art/Concept Art
   - 🧠 Other/AI-curated (future inspiration; all entries are unrated, `ship_ref` = 0)

   You can select one category at a time to view.

2. **By reference level**:
   - Filter to only show entries at or above a certain reference level
   - For example, you can filter to only show ✧4 and ✧3 level entries to focus on the highest quality references
   - Reference levels: 0 (no reference) to 4 (generation ship level)

3. **By tags**:
   - Multiple tags can be selected simultaneously
   - Tags categorize entries by content themes: "interstellar travel", "hard sci-fi", "space colony", "interior", "exterior", "habitat", "propulsion", etc.
   - Only entries that match all selected tags are displayed

### Searching
- Full-text search across titles, notes, and tags
- Instant results as you type

### Display
- Shows posters/cover images for all entries
- Displays all the metadata for each entry
- Shows notes about why the entry is relevant to generation ship design
- Links to external sources for more information

## Statistics

Current gallery counts (from the `gallery.html` tab headers):

| Category | Curated Entries | ✧4 | ✧3 | ✧2 |
|---|---|---|---|---|
| Movies | 157 | 5 | 7 | 26 |
| TV Shows | 62 | 4 | 8 | 18 |
| Games | 84 | 1 | 13 | 25 |
| Anime | 34 | 1 | 3 | 3 |
| Comics | 29 | 1 | 1 | 8 |
| Novels | 25 | 3 | 4 | 7 |
| Art/Concept | 103 | 27 | 27 | 33 |
| Other/AI-curated | 39 | — | — | — |
| **Total** | **533** | **42** | **63** | **120** |

The ✧4/✧3/✧2 totals cover the seven rated categories only (the Other category is unrated by design). Counts drift as curation continues; the tab headers in `gallery.html` and the per-category `ship_ref` columns in the curated CSVs are the source of truth. Note that `docs/科幻素材库-2000后.md` and `branch/README.md` still show the older 7-category / 495-entry figures.

## Related Pages
- [Overview](./overview.md)
- [Generation Pipeline](./generation-pipeline.md)
