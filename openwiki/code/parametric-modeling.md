---
type: code
title: Blender Parametric Modeling
description: Blender Python scripts for parametric generation of the generation ship 3D model
tags: [code, blender, parametric, modeling]
---
# Blender Parametric Modeling

The project uses Blender Python (bpy) for parametric generation of the complete 3D model of the generation ship. This allows easy parameter changes and automatic generation of the internal and external structure.

## Goals of Parametric Modeling

1. Make it easy to adjust key parameters (habitat radius, mass distribution, etc.) and automatically regenerate the complete model
2. Generate ready-to-render model with proper organization of objects and materials
3. Export the model in standard formats (glTF, STL, USD) that can be used in other 3D tools

## Planned Script Structure

The scripts will be organized into modular components:
1. **Main script**: Reads the parameter file, coordinates generation of all components
2. **Habitat generator**: Generates the twin counter-rotating rings, internal decks, compartments
3. **Propulsion generator**: Generates the fusion propulsion stages, radiators, magnetic sail
4. **Shielding generator**: Generates the propellant/water tanks surrounding the habitat
5. **Payload generator**: Generates the forward payload section and Whipple shield
6. **Export script**: Exports the completed model to various formats

## How to Run

1. Open Blender
2. Run the script from the Blender Python console or use the command-line Blender for batch generation
3. Adjust parameters in the configuration file before running

Parameters are stored in a simple configuration file that includes all the key parameters from this wiki. Changing the radius of the habitat in the config file will automatically change it everywhere in the model when you regenerate.

## Expected Outputs

- Complete Blender scene with all objects properly organized in collections
- Each subsystem is in its own collection for easy visibility control
- Materials are already assigned based on the function of each component
- Model is ready for Cycles rendering with proper lighting setup
- Exported versions in standard formats for use in other 3D software

## Related Pages
- [Key Parameters](../design/key-parameters.md)
- [Overall Ship Configuration](../design/ship-configuration.md)
- [Toolchain](../references/toolchain.md)
