---
type: creative-content
title: Self-Produced Creation Content
description: Original short stories, SVG sketches, and a Strudel music experiment built around the ARK-01 generation ship worldbuilding, fed by the material library and AI image series
tags: [creative, writing, music, svg, ark-01]
openwiki:
  roles: [domain, workflow]
  change_kinds: [content-creation]
  source_paths: [docs/creation/README.md, docs/creation/灵感笔记.md, docs/creation/writing/12-B层.md, docs/creation/writing/C区的曲子.md, docs/creation/music/README.md]
  validation_commands: [npm i @strudel/core then stub SalatRepl to evaluate the music script]
---
# Self-Produced Creation Content

The `docs/creation/` directory is the project's **original-content area** (自产): text written directly, drafts drawn as SVG/Canvas code, and generative audio. It is the counterpart to the `branch/` material library, which collects other people's work. The operating principle, from `docs/creation/README.md`: "平时搜集，随手记录，偶尔展开" - ideas encountered during daily curation, material-library maintenance, and image generation are logged as one-liners in the idea notebook; when an idea grows up, it becomes a finished piece with a back-link.

## Formats

| Form | Practice | Directory |
|---|---|---|
| Original writing (settings/short stories/notes) | Markdown, readable online as soon as committed | `writing/` |
| Drafts / diagrams | Hand-written SVG vector code, rendered directly in the browser | `svg/` |
| Generative art | Single-file HTML + Canvas/p5.js, runs on GitHub Pages | `gen-art/` (planned) |
| AI finished images | Volcengine Ark Seedream / ChatGPT output | `../未来世界_生图/` (see [Future World AI Concept Art](./future-world-images.md)) |

## The Idea Notebook (灵感笔记.md)

`docs/creation/灵感笔记.md` is the intake queue. Each entry follows a light format:

```
### YYYY-MM-DD · 标题
- 来源: (which curation/material/image-generation activity triggered it)
- 灵感: (what to create, one line is enough)
- 状态: 💭 随手记 / 🌱 展开中 / ✅ 已成稿(链接)
```

Notable entries that became finished works:
- **船上考古学** -> short story [writing/12-B层.md](https://github.com/shawn1905/generation-ship/blob/main/docs/creation/writing/12-B层.md) (ARK-01, Year 137: a maintenance worker finds first-generation crew graffiti - "the ship itself is an archaeological site")
- **飞船的声音设计** -> short story [writing/C区的曲子.md](https://github.com/shawn1905/generation-ship/blob/main/docs/creation/writing/C区的曲子.md) + the Strudel piece below
- **方舟号 ARK-01** -> worldbuilding thread (ring ship named ARK-01, Year 137) with a ring cross-section sketch in `svg/ark01_ring_draft.svg`

## Music Experiment: Sector C Suite

`docs/creation/music/` contains a Strudel ([strudel.cc](https://strudel.cc)) composition experiment - "the ship's sound design" from the notebook, made audible. The piece *Sector C Suite (ARK-01, Year 137)* encodes the decay idea from the short story: designers wrote bespoke ambient music per compartment at launch; 137 years later, hardware aging has drifted pitch and loop alignment, and the music is **mutating**.

Four layers:
- **L1 Earth Backup**: the original, clean, aligned (piano chords Am-F-C-G, unadorned)
- **L2 The Decay**: the living Year-137 version - `slow(8.03)` stretches the 8-beat theme to 8.03 beats so it slowly drifts out of phase with the backup (every ~100 loops the songs differ by 3 beats, while each moment sounds almost identical); `add(slow(32, range(-0.05,0.05)))` drifts pitch imperceptibly per note but a full key over decades
- **L3 The Hull**: low drone pads with slow pitch drift simulating metal thermal expansion
- **L4 The Pump**: triangle-wave arpeggio from agricultural ring pump 3, occasionally stuttering like an old pump

Play link and code: `docs/creation/music/播放链接.txt`, `C区曲子_sector_c_suite.js`. Strudel only plays the **last expression**, so multi-layer pieces must be wrapped in `stack(...)`.

## Change Guidance

- **Add an idea**: append a dated entry to `docs/creation/灵感笔记.md` - no format strictness, one line is fine
- **Expand an idea into a piece**: create the file under `writing/` or `svg/` (or `gen-art/` for generative art), update the notebook entry's status, and add a row to the `docs/creation/README.md` index table
- **Music**: Strudel scripts encode to `https://strudel.cc/#` + base64(URL-encoded script). Local verification needs `npm i @strudel/core` with a stub for `@kabelsalat/web`'s `SalatRepl` (the `.mjs` lacks that export under Node), then `evalScope(import('@strudel/core'))`, evaluate via `new Function` returning `stack(...)`, and validate events with `pattern.queryArc(0,2)`
- **No automated tests exist** for this area; validation is the browser rendering for SVG/HTML and the Strudel evaluation steps above for music

## Related Pages
- [Future World AI Concept Art](./future-world-images.md) - the AI image series that shares the ARK-01 worldbuilding and feeds the notebook
- [Sci-Fi Reference Material Library](../material-library/overview.md) - curation activity that generates many notebook ideas
