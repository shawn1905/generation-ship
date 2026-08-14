---
type: design-concept
title: Key Parameters
description: Summary of all key ship parameters with their physical justifications
tags: [design, parameters]
---
# Key Ship Parameters

This page summarizes all key parameters for the generation ship design, with their physical justifications and references.

## Mission Parameters

| Parameter | Value | Justification |
|-----------|-------|---------------|
| Target | Proxima Centauri b | Closest potentially habitable exoplanet, 4.24 ly from Solar System |
| Total mission duration | 200 years | Core project requirement |
| Cruise speed | ~0.03c (9,000 km/s) | 4.24 ly ÷ 200 years ≈ 0.021c average, so cruise ~0.03c to allow for acceleration/deceleration |
| Timeline | 15 yr acceleration + 170 yr cruise + 15 yr deceleration | Matches 200 year total, fusion pulse acceleration rate is manageable |

## Population Parameters

| Parameter | Value | Justification |
|-----------|-------|---------------|
| Initial founding population | 1,000 - 2,000 | Minimum viable population genetics + allows for growth |
| Expected arrival population | 10,000 - 20,000 | Natural growth over 200 years, sufficient for colonization |

## Habitat Parameters

| Parameter | Value | Justification |
|-----------|-------|---------------|
| Habitat configuration | Twin counter-rotating rings | Cancels out net angular momentum for the whole ship |
| Habitat radius | 250 - 500 m | Balances structural mass, radiation shielding mass, and Coriolis effect |
| Artificial gravity | 1g | To maintain human health over multiple generations |
| Rotation rate | 1.2 - 1.9 rpm | At 300-500 m radius, gives 1g, and ≤2 rpm which is the NASA acceptability threshold for Coriolis effects |

## Propulsion Parameters

| Parameter | Value | Justification |
|-----------|-------|---------------|
| Propulsion type | Inertial confinement fusion pulse | Daedalus/Longshot heritage, only feasible option for 0.03c with reasonable mass ratio |
| Specific impulse (Isp) | ~10⁶ s | Inherent to fusion pulse propulsion |
| Configuration | Two-stage (acceleration + deceleration) | Needed to reach cruise speed then stop at destination |
| Final braking | Magnetic sail | Low mass solution for final deceleration |

## Power Parameters

| Parameter | Value | Justification |
|-----------|-------|---------------|
| Cruise power (life support/habitat) | 10 - 100 MW(e) | 5-50 kW per person × 2,000 people |
| Peak propulsion power | GW-TW range | Only needed during acceleration/deceleration phases |
| Power source | Fusion reactor | Leverages same technology as propulsion |

## Radiation Shielding Parameters

| Parameter | Value | Justification |
|-----------|-------|---------------|
| Primary shielding | Superconducting dipole active magnetic shielding | Reduces GCR flux dramatically, lower mass than all-passive |
| Secondary shielding | Water/propellant tanks passive shielding | Already needed for propellant, doubles as shielding |
| Emergency shelter | Central dense storm shelter | For solar particle events (SPE), minimal additional mass |
| Target total dose | <20 Sv over 200 years | Below lethal threshold for cumulative exposure |

## Other Key Parameters

| Parameter | Value | Justification |
|-----------|-------|---------------|
| Front shielding | Whipple double-layer dust shield | Standard solution to interstellar dust erosion at 0.03c |
| Life support closure | 100% for water/oxygen/nitrogen; 90%+ for food | Zero resupply over 200 years requires near-complete closure |

## Related Pages
- [Core Constraints](./core-constraints.md)
- [Ship Configuration](./ship-configuration.md)
- [Budgets](../engineering/budgets.md)
