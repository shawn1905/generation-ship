---
type: skeleton
title: Generation Ship Wiki Skeleton
description: Skeleton structure for the Generation Ship Design project wiki
tags: [project, skeleton]
---
# Generation Ship Design Wiki Skeleton

## Overview
This repository contains the **Generation Ship Design** project - an engineering design project for a 200-year interstellar generation ship to Proxima Centauri b, aiming to produce complete 3D models ready for rendering in Blender/FreeCAD. It also includes a curated sci-fi reference material library.

## Planned Wiki Structure

### Project Overview
- `/openwiki/project/overview.md` - High-level project introduction, principles, goals, and four-phase plan
- `/openwiki/project/design-principles.md` - The three core principles (rigorous sci-fi, reference open source, 200-year constraint)

### Engineering & Design Calculations
- `/openwiki/engineering/budgets.md` - Phase 0 mass budgets, power budgets, population/agriculture area calculations - methodology and results

### Core Design Concepts
- `/openwiki/design/core-constraints.md` - How the 200-year constraint defines the only possible solution (fusion pulse propulsion, two-stage configuration)
- `/openwiki/design/key-parameters.md` - All key ship parameters (size, population, speed, power, shielding) with physical justifications
- `/openwiki/design/ship-configuration.md` - Overall ship layout and configuration (Daedalus-style "train" layout: payload -> habitat -> shielding -> propulsion)
- `/openwiki/design/multi-generational-design.md` - Multi-generational social and organizational design considerations for a 200-year interstellar mission

### Key Subsystems
- `/openwiki/subsystems/propulsion.md` - Two-stage fusion pulse propulsion + magnetic sail braking
- `/openwiki/subsystems/habitat.md` - Rotating twin-ring habitat design, artificial gravity, layout
- `/openwiki/subsystems/radiation-shielding.md` - Combined active magnetic + water/propellant + storm shelter shielding solution to 200-year cumulative radiation problem
- `/openwiki/subsystems/life-support.md` - Closed-loop life support for 200-year mission, BIOS-3/MELiSSA references
- `/openwiki/subsystems/payload.md` - Landing craft and outpost module in the forward section

### Implementation & Code Assets
- `/openwiki/code/parametric-modeling.md` - Blender Python parametric modeling scripts for ship hull and internal layout generation - how they work, how to run them, and what outputs they produce

### Open Source References & Tools
- `/openwiki/references/open-source-projects.md` - Curated list of open source projects used as reference
- `/openwiki/references/literature.md` - Key literature and academic references
- `/openwiki/references/toolchain.md` - Open source toolchain (Blender, FreeCAD, OpenSCAD, etc.)
- `/openwiki/references/engineering-images.md` - Curated NASA public domain reference image collection (including SP-413 Stanford Torus material) organized by ship subsystem

### Sci-Fi Reference Material Library
- `/openwiki/material-library/overview.md` - Overview of the curated 2000+ sci-fi reference collection
- `/openwiki/material-library/gallery.md` - Interactive gallery documentation and usage
- `/openwiki/material-library/generation-pipeline.md` - Documentation for the Python scripts that curate reference data and generate the interactive HTML gallery

## Content Summary
Every major concept and subsystem will be documented with physical justifications, references to source materials, and relationships between different components.
