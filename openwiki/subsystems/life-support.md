---
type: subsystem
title: Closed-Loop Life Support
description: 200-year closed-loop life support system for the generation ship
tags: [subsystem, life-support, closed-loop]
---
# Closed-Loop Life Support

For a 200-year interstellar mission with zero resupply from Earth, a nearly completely closed-loop life support system is required. This system must recycle water, oxygen, and nitrogen, and produce most of the food needed for the population.

## Requirements

- **Water recycling**: 100% closure (all water used is purified and reused)
- **Oxygen recycling**: 100% closure (oxygen from CO₂ recycling)
- **Nitrogen recycling**: 100% closure
- **Food production**: 90%+ closure (remaining 10% is stored food for emergencies)
- Reliable operation for 200 years with maintenance using on-board resources

## Precedents

There are existing experimental precedents for closed-loop life support:
- **BIOS-3** (Soviet Union): 85% closure achieved for food, 100% for water and oxygen in sealed experiments
- **ESA MELiSSA**: European Space Agency program developing completely closed-loop life support
- **Biosphere 2**: Large-scale closed environment experiment, identified many challenges to achieve complete closure

## System Architecture

The system uses a combination of biological and physical-chemical recycling:

### 1. Water Recycling
- All wastewater (showers, laundry, humidity from air, urine, etc.) is collected
- Purified through filtration, biological treatment, and reverse osmosis
- Then reused for drinking, irrigation, and other purposes
- 100% closure is achievable with current technology

### 2. Oxygen & Carbon Dioxide Recycling
- Humans breathe oxygen and exhale CO₂
- CO₂ is split into oxygen and carbon via algae or higher plants in the agricultural areas
- The oxygen is released back into the cabin air
- This is a biological process that's been demonstrated in BIOS-3

### 3. Food Production
- Hydroponic/aeroponic agriculture in dedicated growing areas
- Combination of staple crops, vegetables, and algae
- ~15-20 m² of growing area needed per person
- Provides complete nutrition for the population
- Some stored food is kept for emergencies and crop failures

### 4. Waste Recycling
- All organic waste (human waste, plant waste, food waste) is composted or processed
- Nutrients are extracted and reused in agriculture
- This closes the nutrient loop

## Mass & Power Requirements

- Requires ~15-20 m² of growing area per person
- Requires significant electrical power for lighting (photosynthesis)
- The power is provided by the ship's fusion reactor
- The agricultural areas also contribute to oxygen production

## Related Pages
- [Budgets](../engineering/budgets.md)
- [Habitat](./habitat.md)
- [Core Constraints](../design/core-constraints.md)
