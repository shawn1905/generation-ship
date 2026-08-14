---
type: reference
title: Open Source Toolchain
description: Open source tools used in the generation ship design project
tags: [reference, toolchain, tools]
---
# Open Source Toolchain

All tools used in this project are open source and available free of charge.

## 3D Modeling

### Blender
- **Purpose**: Parametric modeling with Python, Cycles rendering
- **Capabilities**:
  - Python API (bpy) for scripted parametric generation
  - Advanced Cycles path tracing renderer
  - Supports export to glTF, STL, USD and other standard formats
- **Website**: [blender.org](https://www.blender.org/)

### FreeCAD
- **Purpose**: Precise mechanical design, STEP export
- **Capabilities**:
  - Parametric mechanical part design
  - Supports STEP format for precise engineering interchange
  - Good for detailed mechanical components
- **Website**: [freecad.org](https://www.freecad.org/)

### OpenSCAD
- **Purpose**: Procedural CSG modeling
- **Capabilities**:
  - Script-based procedural modeling
  - Good for simple geometric parts
- **Website**: [openscad.org](https://openscad.org/)

## Engineering Calculations

### Python with scientific libraries
- **NumPy**, **SciPy**, **Pandas**: For numerical calculations and data analysis
- **Matplotlib**: For plotting results

### OpenMDAO / dymos
- For multidisciplinary design optimization and trajectory optimization
- See [Open Source Projects](./open-source-projects.md) for more details

## Reference Data Visualization

- **Python**: Data processing for the reference material gallery
- **HTML/CSS/JavaScript**: Interactive gallery (generated from curated data)

## AI Image Generation

- **Volcengine Ark CLI (`arkcli`)**: command-line image generation for the "未来世界" concept-art series. Invocation: `arkcli +gen --model doubao-seedream-5.0-lite --modality image --size 4K --save-to <dir> "<prompt>"` (explicit `--modality image` required on arkcli 1.0.14). Quota: 50 seedream images/month on the agent plan. See [Future World AI Concept Art](../creative/future-world-images.md) for the methodology and scripts.

## Related Pages
- [Parametric Modeling](../code/parametric-modeling.md)
- [Gallery Generation Pipeline](../material-library/generation-pipeline.md)
- [Open Source Projects](./open-source-projects.md)
- [Future World AI Concept Art](../creative/future-world-images.md)
