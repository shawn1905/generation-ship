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
- [Overview](./material-library/overview.md) - Overview of the curated sci-fi reference collection
- [Interactive Gallery](./material-library/gallery.md) - Documentation for the interactive reference gallery
- [Generation Pipeline](./material-library/generation-pipeline.md) - How the interactive gallery is generated from curated data

## Common Tasks

| What do you want to do? | Go to these pages... |
|---|---|
| Understand the basic design concept | [Project Overview](./project/overview.md), [Core Constraints](./design/core-constraints.md), [Key Parameters](./design/key-parameters.md) |
<!-- openwiki: broken internal link [#subsystem-documentation] heading anchor "subsystem-documentation" does not exist in /openwiki/quickstart.md. Fix the href or restore the target, then delete this comment. -->
| Learn about a specific subsystem | [Subsystems Index](#subsystem-documentation) above |
| Generate the 3D model | [Blender Parametric Modeling](./code/parametric-modeling.md), [Toolchain](./references/toolchain.md) |
| Find sci-fi references for inspiration | [Interactive Gallery](./material-library/gallery.md), [Overview](./material-library/overview.md) |
| Find engineering references | [Open Source Projects](./references/open-source-projects.md), [Literature References](./references/literature.md), [Engineering Images](./references/engineering-images.md) |
| Regenerate the reference gallery | [Generation Pipeline](./material-library/generation-pipeline.md) |

## Project Phases

1. **Phase 0** - Complete mass, power, population, and agriculture budgets ✅ (in progress)
2. **Phase 1** - Concept architecture + parametric shell (Blender Python scripts)
3. **Phase 2** - Complete internal structure, deck layout, sectional views
4. **Phase 3** - Materials, lighting, Cycles rendering

## Related Resources

- Original project README: [/README.md](https://github.com/.../README.md)
- Concept discussion document: [/docs/讨论稿-概念与待决问题.md](https://github.com/.../docs/讨论稿-概念与待决问题.md)

## Backlog

The following items are outside the current documentation scope:
- Detailed step-by-step rendering workflow (will be added during Phase 3)
- Detailed mechanical engineering of individual components (will be added as they are designed)
