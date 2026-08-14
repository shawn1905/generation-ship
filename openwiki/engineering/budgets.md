---
type: engineering-calculations
title: Mass, Power & Population Budgets
description: Phase 0 engineering budget calculations for the generation ship
tags: [engineering, budget, mass, power, population]
---
# Mass, Power & Population Budgets

Phase 0 of the project focuses on establishing the key engineering budgets that bound all subsequent design work. This page documents the methodology and preliminary results.

## Population Budget

The population budget determines the minimum number of people needed for a healthy multi-generational colony that can successfully colonize the destination planet after 200 years of travel.

Key considerations:
- **Minimum viable population**: Genetics studies suggest 100-160 founding individuals as the minimum to maintain genetic diversity
- **Colonization requirement**: To successfully colonize a new planet, at least 500 individuals are needed upon arrival
- **Growth over 200 years**: Starting with 1000-2000 initial population, the population is expected to grow to 10,000-20,000 by arrival

**Current budget:**
- Initial founding population: 1,000 - 2,000 people
- Target arrival population: 10,000 - 20,000 people
- Habitat area allocation: ~50 m² per person (including living space, agriculture, and industry)

> **Phase 0 anchor**: NASA SP-413 (*Space Settlements: A Design Study*, 1975) contains a full mass/area budget table for a **10,000-person** rotating habitat - the most credible historical anchor for this population accounting. The original images and the report link are collected in [NASA Engineering Reference Images](../references/engineering-images.md).

## Agriculture & Food Budget

For 200-year closed-loop life support, food production must be entirely on-board:

Based on BIOS-3 experience:
- ~15-20 m² of growing area per person is needed to provide complete nutrition
- This includes both crops for food and algae for oxygen production
- Using higher-yield hydroponic/aeroponic systems can reduce this area somewhat

**Current budget:**
- Total agricultural area: ~15-20 m² per person × 2,000 people = 30,000 - 40,000 m²
- This translates to a significant portion of the rotating habitat space
- Food closure target: 90%+ (the remaining 10% is stored food for emergencies)

## Power Budget

Power is needed for:
- Life support systems (lighting for agriculture, air handling, water recycling)
- Habitat systems (temperature control, lighting, communications)
- Industrial systems (3D printing, maintenance, repairs)
- Radiation shielding (power for active magnetic shielding)

**Current budget estimates:**
- Per person power consumption: 5-50 kW(e)
- Total power for life support + habitat + industry: **10-100 MW(e)**
- Propulsion power: GW-TW range (only during acceleration/deceleration phases, not during cruise)
- Power source: Fusion reactor (same technology that powers propulsion)

## Mass Budget

The total ship mass is dominated by:
1. **Radiation shielding**: The single largest mass component (water/propellant used as passive shielding)
2. **Propulsion system**: Fusion pulse engines and fuel
3. **Habitat structure**: The rotating habitat ring structure
4. **Propellant**: For acceleration and deceleration

Based on Daedalus/Longshot heritage:
- Daedalus total mass: 54,000 tonnes (unmanned probe)
- This design is larger (carries 1000-2000 people + habitat)
- Estimated total mass is in the **hundreds of thousands to millions of tonnes** range

Key mass allocations (preliminary):
- Radiation shielding: ~40-50% of total mass
- Propulsion and propellant: ~25-35% of total mass
- Habitat and structure: ~10-15% of total mass
- Life support and equipment: ~5-10% of total mass
- Payload (landers, outpost): ~5% of total mass

## Trade-offs Being Considered

1. **Smaller habitat vs. radiation mass**: Reducing habitat radius reduces radiation shielding mass but increases Coriolis effect issues
2. **Higher speed vs. mass fraction**: Higher speed requires more propellant but reduces travel time (fixed at 200 years by requirement)
3. **More redundancy vs. mass**: More redundant systems increase reliability but add mass

## Related Pages
- [Project Overview](../project/overview.md)
- [Key Parameters](../design/key-parameters.md)
- [Radiation Shielding](../subsystems/radiation-shielding.md)
- [Life Support](../subsystems/life-support.md)
