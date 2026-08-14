---
type: design-concept
title: Overall Ship Configuration
description: Overall layout and configuration of the generation ship
tags: [design, configuration, layout]
---
# Overall Ship Configuration

The generation ship follows a Daedalus-style "train" layout, which is the logical arrangement given the propulsion system, habitat requirements, and shielding needs.

## Overall Layout Diagram

<!-- openwiki: mermaid parse failed and this diagram was converted to a text fence so it does not break rendering. Fix the diagram source and restore the mermaid fence. Parser error: Heuristic: an unescaped angle bracket inside a label breaks rendering; rephrase the label. -->
```text
flowchart LR
    A[Payload<br>Landing craft<br>Outpost module] --> B[Whipple Shield]
    B --> C[Rotating Twin-Ring Habitat<br>Residential / Agricultural / Industrial]
    C --> D[Water / Propellant Tanks<br>(also serve as radiation shielding)]
    D --> E[Fusion Propulsion System<br>First Stage (jettisoned after acceleration)]
    D --> F[Fusion Propulsion System<br>Second Stage (carries habitat to destination)]
    F --> G[Large Radiators<br>for fusion heat rejection]
    F --> H[Magnetic Sail<br>for final braking]
```

## Front to Back Arrangement

### 1. Front: Payload & Whipple Shield

**Whipple Shield**:
- Double-layer dust shield located at the very front of the ship
- Protects the rest of the ship from interstellar dust erosion at 0.03c
- This was already studied and used in the Daedalus design

**Payload Section**:
- Located directly behind the Whipple shield
- Contains landing craft for the destination planet
- Contains outpost module for initial surface colonization
- Has its own additional radiation shielding since it's at the front

### 2. Middle: Rotating Twin-Ring Habitat

**Position**: Located in the middle of the ship, behind the payload and before the propellant tanks
**Configuration**: Two counter-rotating rings
- Each ring rotates in opposite direction to cancel out net angular momentum
- Precesses so that the entire ship doesn't start rotating

**Content**:
- Residential areas for the population
- Agricultural areas for closed-loop food production
- Industrial areas for maintenance and manufacturing
- Life support system equipment
- Central radiation storm shelter

### 3. Mid-Rear: Water / Propellant Tanks (Radiation Shielding)

The propellant and water tanks form a large cylindrical shell *around* the habitat section:
- This arrangement maximizes the radiation shielding effect - the propellant/water absorbs and blocks cosmic radiation before it reaches the habitat
- It's a mass-efficient solution because we already need to carry the propellant/water anyway, so it doubles as shielding without adding extra mass

### 4. Rear: Propulsion System & Radiators & Magnetic Sail

**Two-stage propulsion**:
- First stage (larger, more propellant): Jettisoned after acceleration to cruise speed
- Second stage (smaller): Remains attached to the habitat for deceleration at destination

**Large Radiators**:
- Fusion propulsion produces a lot of waste heat
- Large radiators radiate the heat into space
- Required because you can't dump heat anywhere else in space

**Magnetic Sail**:
- Deployed at the rear for final deceleration after the second stage fusion braking is complete
- Uses the interstellar medium for braking with minimal additional mass
- Reduces the amount of propellant needed for deceleration

## Overall Mass Distribution

- The largest mass fraction is radiation shielding (propellant/water tanks)
- Next is propulsion system and propellant
- Then habitat structure
- Then life support equipment
- Then payload

## Why This Configuration?

This layout is the natural result of the requirements:
1. Whipple shield needs to be at the front to stop interstellar dust
2. Propellant tanks around the habitat provide the most mass-efficient radiation shielding
3. Propulsion needs to be at the rear to push the ship
4. Two counter-rotating rings cancel angular momentum so the ship doesn't spin

## Related Pages
- [Key Parameters](./key-parameters.md)
- [Habitat](../subsystems/habitat.md)
- [Radiation Shielding](../subsystems/radiation-shielding.md)
- [Propulsion](../subsystems/propulsion.md)
