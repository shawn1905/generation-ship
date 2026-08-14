---
type: creative-content
title: Future World AI Concept Art
description: The "我眼中的未来世界" AI concept image series, the mandatory Interstellar-style generation methodology (scale reference, single light source, real materials), and the arkcli generation scripts
tags: [creative, ai-images, seedream, methodology]
openwiki:
  roles: [domain, workflow]
  change_kinds: [content-creation]
  source_paths: [docs/未来世界_生图/README.md, docs/未来世界_生图/生图提示词.md, docs/gen_future_v2.sh, docs/gen_my_future.sh]
  symbols: [arkcli +gen, doubao-seedream-5.0-lite]
  validation_commands: [bash docs/gen_future_v2.sh]
---
# Future World AI Concept Art

`docs/未来世界_生图/` archives the **"我眼中的未来世界"** ("The Future World in My Eyes") AI concept-art series. The world view: **living cities / slow civilizations / symbiotic AI / stellar-scale** (rejecting cyberpunk coldness while staying grounded).

Current set (methodology versions, 2026-08-14, 4K, `doubao-seedream-5.0-lite`):
- **009** 世代飞船·200年环 - the main-line ring generation ship
- **010** 恒星边缘的文明（戴森云）- Dyson cloud civilization at a red dwarf's edge
- **011** 仿生共生城市 - biomimetic symbiotic city

Older versions (001-008, 2K/4K, pre-methodology) were cleaned from the tree (recoverable from git history).

## Generation Method (mandatory)

Since 2026-08-14, all image generation must follow the **Interstellar-style methodology** consolidated in `docs/未来世界_生图/生图提示词.md` (sourced from three Xiaohongshu reference notes). The core insight: *scale is communicated by the human-to-universe proportion, not by writing "epic"*.

Seven rules (checklist before every submission):
1. **主体锁死** - lock a single absolute visual subject; other elements are background only
2. **极小尺度参照** - a tiny scale reference (a 3-meter repair craft, an EVA astronaut) nearly vanishing into the frame
3. **巨型天体出画** - the giant body (ship/planet/Dyson cloud) breaks past the frame edges; viewers never see the whole
4. **单一真实光源** - one real light source (star, horizon, engine light); delete colorful nebulae and decorative neon
5. **精准工业细节** - concrete industrial detail words (armor modules, piping, wear scratches, frost, micrometeorite craters) instead of "many details"
6. **镜头语言锚定** - anchor texture to real camera gear + cinematographer style (e.g. `IMAX 70mm, shot in the style of Hoyte van Hoytema` for ship/Dyson scenes; `Arri Alexa Mini, directed in the style of Roger Deakins` for city scenes)
7. **干净极繁** - clean maximalism: 1-2 strong light sources, subject half-lit/half-shadowed, pure-black deep space background, UE5-render/next-gen materials, 8K

Prompt skeleton: `微小参照物＋巨型天体＋明确机位＋单一光源＋真实材质＋大画幅电影镜头`.

## Generation Pipeline

- `docs/gen_future_v2.sh` - the v2 script that generated 009-011 (methodology applied, 4K, output to `docs/未来世界_生图/`)
- `docs/gen_my_future.sh` - the earlier one-shot 4K script (006-008, superseded; also demonstrates the arkcli invocation form)

Both use the Volcengine Ark CLI:
```bash
arkcli +gen --model doubao-seedream-5.0-lite --modality image --size 4K --save-to "$OUTDIR" "$prompt"
```
Notes: `arkcli` 1.0.14 requires explicit `--modality image`; use the dotted raw model id `doubao-seedream-5.0-lite`.

## Quota & Operations

- Seedream free quota inside the agent plan: **50 images/month** (resets monthly); the 3 methodology images left ~42
- Text models run on a separate quota (AFP) and do not share the image budget
- Verification after generation: check the output file appears in `docs/未来世界_生图/` with the planned name; visually verify against the 7-rule checklist

## Related Pages
- [Self-Produced Creation Content](./creation.md) - the idea notebook and short stories that share the ARK-01 worldbuilding with these images
- [Sci-Fi Reference Material Library](../material-library/overview.md) - the curated entries (e.g. Aniara, Silent Running) that inspired ship/ecosystem imagery
- [Open Source Toolchain](../references/toolchain.md) - arkcli and the surrounding open-source stack
