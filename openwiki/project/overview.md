---
type: project-overview
title: Project Overview
description: High-level introduction to the Generation Ship Design project, its goals and four-phase development plan
tags: [project, overview]
---
# Generation Ship Design Project Overview

The Generation Ship Design project is an engineering design effort to create a complete, physically plausible design for a generation ship capable of traveling for 200 years to reach Proxima Centauri b, with the final output being full 3D models that can be rendered in Blender or FreeCAD.

## Project Mission

Design a **200-year interstellar generation ship** that follows three core principles:
1. **Rigorous scientific fantasy** - every design number comes from physical derivation or verifiable research, no unscientific "magic" solutions
2. **Reference existing open source** - maximize use of existing open source projects and public research, avoid arbitrary invention
3. **200-year scale constraint** - the entire design is driven by the requirement of reaching a nearby star within 200 years

## Core Design Conclusion

The 200-year mission constraint uniquely determines the ship architecture:
- Target: Proxima Centauri b (4.24 light years away)
- Required cruise speed: ~0.03c (9,000 km/s) to reach the destination within 200 years
- Chemical/nuclear thermal/nuclear electric propulsion all lack sufficient specific impulse (Isp)
- The only feasible solution: **fusion pulse propulsion** (Daedalus/Longshot design lineage) with Isp ~10⁶ seconds
- Two-stage configuration: acceleration stage + deceleration stage, with magnetic sail for final braking
- Mission timeline: ~15 years acceleration + ~170 years cruise + ~15 years deceleration = 200 years

The hardest design challenges are not propulsion, but:
1. **200-year cumulative radiation dose** that requires combined shielding strategies
2. **200-year closed-loop life support** with zero resupply from Earth

## Four-Phase Development Plan

The project is organized in four phases:

### Phase 0: Requirements & Budgeting
- Mass budget calculation
- Power budget calculation
- Population and agriculture area accounting
- Core constraint validation

### Phase 1: Concept Architecture & Parametric Hull
- Overall concept architecture definition
- Parametric hull modeling with Blender Python scripts
- Key parameter trade-off analysis

### Phase 2: Internal Structure
- Deck compartmentalization
- Twin-ring rotating habitat layout
- Cross-section drawings
- Subsystem placement

### Phase 3: Rendering
- Material and texture application
- Lighting setup
- Final rendering with Cycles

## Repository Structure

- `/README.md` - Project introduction and summary
- `/docs/` - Project documentation and discussion documents
  - `讨论稿-概念与待决问题.md` - Concept discussion and physical derivation notes
- `/branch/` - Sci-fi reference material collection with interactive gallery
  - `gallery.html` - Interactive reference gallery (local HTML file)
  - `scripts/` - Python scripts for data curation and gallery generation
- `/skills/` - OpenWiki skills (not part of the generation ship project itself)

## Related Pages
- [Design Principles](./design-principles.md)
- [Core Constraints](../design/core-constraints.md)
- [Key Parameters](../design/key-parameters.md)
