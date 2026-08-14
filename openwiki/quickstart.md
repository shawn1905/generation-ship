---
type: quickstart
title: OpenWiki Quickstart - Generation Ship Design
description: Quickstart guide to the Generation Ship Design project wiki
tags: [quickstart, introduction, navigation]
---
# Quickstart Guide: Generation Ship Design Project

Welcome to the OpenWiki documentation for the Generation Ship Design project. This wiki documents a project to design a complete generation ship for a 200-year voyage to Proxima Centauri b, with rigorously physically-derived parameters and parametric 3D modeling ready for rendering.

## Project Overview

The project is based on the core insight that **a 200-year voyage to the nearest star uniquely determines the entire design**:
- Target: Proxima Centauri b (4.24 light years)
- Cruise speed: ~0.03c (9000 km/s) to reach the target in 200 years
- Only feasible propulsion: Two-stage fusion pulse propulsion (Daedalus/Longshot lineage)
- The hardest design challenges: **200 years cumulative radiation shielding** and **100% closed-loop life support**

## How to Navigate This Wiki

Start with:
- [Project Overview](./project/overview.md) - High-level introduction and four-phase project plan
- [Core Design Constraints](./design/core-constraints.md) - How the 200-year constraint defines the solution
- [Key Design Parameters](./design/key-parameters.md) - Complete table of all key ship parameters

## Design Documentation

### Core Design Concepts
- [Core Constraints](./design/core-constraints.md)
- [Key Parameters](./design/key-parameters.md)
- [Overall Ship Configuration](./design/ship-configuration.md)
- [Multi-Generational Design](./design/multi-generational-design.md)

### Subsystems
- [Propulsion](./subsystems/propulsion.md) - Two-stage fusion pulse + magnetic sail braking
- [Habitat](./subsystems/habitat.md) - Twin counter-rotating ring habitat with 1g artificial gravity
- [Radiation Shielding](./subsystems/radiation-shielding.md) - Combined active magnetic + water shielding + storm shelter
- [Life Support](./subsystems/life-support.md) - 100% closed-loop recycling of water, oxygen, and nutrients
- [Payload](./subsystems/payload.md) - Landing craft and initial colonization outpost

### Engineering Calculations
- [Mass & Power Budgets](./engineering/budgets.md) - Phase 0 engineering calculations for mass, power, and population

### Code & Implementation
- [Blender Parametric Modeling](./code/parametric-modeling.md) - Python scripts for automatic 3D model generation

### References
- [Open Source Projects](./references/open-source-projects.md) - Open source projects used as reference
- [Literature References](./references/literature.md) - Key academic and engineering literature
- [Toolchain](./references/toolchain.md) - Open source tools used in the project
- [NASA Engineering Reference Images](./references/engineering-images.md) - Curated NASA public domain reference images

### Reference Material Library
- [Overview](./material-library/overview.md) - Overview of the curated sci-fi reference collection (8 categories, 533 entries)
- [Interactive Gallery](./material-library/gallery.md) - Documentation for the interactive reference gallery
- [Generation Pipeline](./material-library/generation-pipeline.md) - How the interactive gallery is generated from curated data

### Creative & AI Concept Art
- [Self-Produced Creation Content](./creative/creation.md) - Original writing, SVG sketches, and the Strudel music experiment (ARK-01 worldbuilding)
- [Future World AI Concept Art](./creative/future-world-images.md) - The "我眼中的未来世界" image series and the Interstellar-style generation methodology

## Common Tasks

| What do you want to do? | Go to these pages... |
|---|---|
| Understand the basic design concept | [Project Overview](./project/overview.md), [Core Constraints](./design/core-constraints.md), [Key Parameters](./design/key-parameters.md) |
| Learn about a specific subsystem | [Propulsion](./subsystems/propulsion.md), [Habitat](./subsystems/habitat.md), [Radiation Shielding](./subsystems/radiation-shielding.md), [Life Support](./subsystems/life-support.md), [Payload](./subsystems/payload.md) |
| Generate the 3D model | [Blender Parametric Modeling](./code/parametric-modeling.md), [Toolchain](./references/toolchain.md) |
| Find sci-fi references for inspiration | [Interactive Gallery](./material-library/gallery.md), [Overview](./material-library/overview.md) |
| Find engineering references | [Open Source Projects](./references/open-source-projects.md), [Literature References](./references/literature.md), [Engineering Images](./references/engineering-images.md) |
| Regenerate the reference gallery | [Generation Pipeline](./material-library/generation-pipeline.md) |
| Read original short stories / music | [Self-Produced Creation Content](./creative/creation.md) |
| Understand the AI image generation method | [Future World AI Concept Art](./creative/future-world-images.md) |

## Task Routing for Changes

The table below routes common change intents to the exact source files, symbols, and validation commands. "Focused checks" are the narrowest evidence-backed validations; broader regeneration steps are marked as conditional.

| Change area / intent | Wiki page | Source entry points | Key symbols / types | Focused checks | Minimal validation |
|---|---|---|---|---|---|
| Regenerate `branch/gallery.html` after any CSV edit | [Generation Pipeline](./material-library/generation-pipeline.md) | `branch/scripts/make_gallery.py` | `load()` (reads all `*_curated.csv` + `other/ai_curated.csv`), per-category `cards_*()` builders | Tabs in `gallery.html` must show current per-category counts | `branch/.venv/bin/python branch/scripts/make_gallery.py` |
| Add an entry to 🧠 Other/AI-curated | [Material Library Overview](./material-library/overview.md) | `branch/other/ai_curated.csv`, `branch/other/README.md`, `branch/scripts/fetch_other_covers.py` (`PLAN` dict) | 9-column CSV row; `source_id` slug; note must avoid ASCII commas | `health_check_other.py` checks column count, cover existence, URL reachability | `branch/.venv/bin/python branch/scripts/health_check_other.py` |
| Curate movies/TV/games (add/remove entries) | [Generation Pipeline](./material-library/generation-pipeline.md) | `branch/scripts/curate_movies.py`, `curate_tv.py`, `curate_games.py` | `KNOWN_MOVIES` / `KNOWN_*` dicts (`(title, year) -> (tags, ship_ref, note)`); `None` marks removals | Year-specified entries must not fall back to empty-year matching (同名不同年份 pitfall) | Re-run the `curate_*.py` script; verify `*_curated.csv` row count |
| Generate new AI concept images | [Future World AI Concept Art](./creative/future-world-images.md) | `docs/gen_future_v2.sh`, `docs/未来世界_生图/生图提示词.md` | `arkcli +gen --model doubao-seedream-5.0-lite --modality image --size 4K` | Methodology checklist (7 rules) in `生图提示词.md` before submitting | `bash docs/gen_future_v2.sh` (quota-bounded, see page) |
| Add NASA reference images | [Engineering Images](./references/engineering-images.md) | `docs/nasa_参考影像/README.md` (API quick ref), `images/` dir | `images-api.nasa.gov` search/asset endpoints; NASA ID filenames | Image file name must equal NASA ID; prefer `large` variant | None (manual download; verify file opens) |
| Regenerate human-readable summary | [Generation Pipeline](./material-library/generation-pipeline.md) | `branch/scripts/make_docs.py` | `load()` for 7 categories only; `row()` formatters | Known gap: `other` category not included in output | `branch/.venv/bin/python branch/scripts/make_docs.py` (conditional; see Backlog) |
| Write original content (stories/SVG/music) | [Self-Produced Creation Content](./creative/creation.md) | `docs/creation/灵感笔记.md`, `writing/`, `svg/`, `music/` | Notebook format (`### YYYY-MM-DD · 标题` with 来源/灵感/状态) | Keep `note` values free of ASCII commas in CSVs; Strudel: only last expression plays, wrap layers in `stack(...)` | None (markdown); `npm i @strudel/core` + stub `SalatRepl` to validate music code |

## Project Phases

1. **Phase 0** - Complete mass, power, population, and agriculture budgets ✅ (in progress)
2. **Phase 1** - Concept architecture + parametric shell (Blender Python scripts)
3. **Phase 2** - Complete internal structure, deck layout, sectional views
4. **Phase 3** - Materials, lighting, Cycles rendering

## Related Resources

- Original project README: [https://github.com/shawn1905/generation-ship/blob/main/README.md](https://github.com/shawn1905/generation-ship/blob/main/README.md)
- Concept discussion document: [https://github.com/shawn1905/generation-ship/blob/main/docs/讨论稿-概念与待决问题.md](https://github.com/shawn1905/generation-ship/blob/main/docs/讨论稿-概念与待决问题.md)
- Online interactive gallery (GitHub Pages): [https://shawn1905.github.io/generation-ship/branch/gallery.html](https://shawn1905.github.io/generation-ship/branch/gallery.html)
- Handover document (project status + pitfalls): [https://github.com/shawn1905/generation-ship/blob/main/docs/HANDOVER.md](https://github.com/shawn1905/generation-ship/blob/main/docs/HANDOVER.md)

## Backlog

The following items are outside the current documentation scope:
- Detailed step-by-step rendering workflow (will be added during Phase 3)
- Detailed mechanical engineering of individual components (will be added as they are designed)
- `docs/科幻素材库-2000后.md` omits the 🧠 Other/AI-curated category: `make_docs.py` loads only the 7 rated categories, so the generated summary lags the gallery (source: `branch/scripts/make_docs.py` `load()` list; not documented in detail until the script is updated)
- `branch/README.md` statistics are stale vs. the gallery (7 tabs / 495 entries vs. 8 tabs / 533): the README is not regenerated automatically (source: `branch/README.md` vs. `branch/gallery.html`)
