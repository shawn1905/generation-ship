---
type: design-concept
title: Core Constraints
description: How the 200-year mission constraint defines the only possible ship architecture
tags: [design, constraints, propulsion]
---
# Core Design Constraints

The 200-year interstellar mission requirement is not just a mission duration - it's a hard constraint that uniquely determines the entire ship architecture. This page explains how the constraint leads to the only feasible solution.

## The 200-Year Constraint Logic

```
200 years + reach a new habitable planet
  → Target must be within ~4-5 light years (only Proxima Centauri b fits)
  → Required average speed: ~0.021c, cruise speed ~0.03c (9,000 km/s)
  → This speed requirement eliminates all conventional propulsion options
```

## Why Other Propulsion Options Are Impossible

### 1. Chemical Propulsion
- Specific impulse (Isp): 300-450 seconds
- To reach 9,000 km/s with chemical propulsion would require an enormous mass ratio that's physically impossible
- Eliminated.

### 2. Nuclear Thermal / Nuclear Electric Propulsion
- Specific impulse (Isp): ~10⁴ seconds
- Using the relativistic rocket equation, mass ratio required is e^(v/(Isp×g)) = e^(9000/(10000×9.8)) ≈ e^0.092 ≈ 1.1 - wait that looks okay? Wait no, that's wrong, because Isp units are already in seconds. Let's recalculate correctly:

The rocket equation is Δv = Isp × g × ln(mass_ratio)

For Δv = 9000 km/s = 9,000,000 m/s
Isp = 10,000 s
g = 9.8 m/s²

ln(mr) = Δv/(Isp × g) = 9,000,000/(10000 × 9.8) ≈ 9.18
mr = e^9.18 ≈ 9,700

So for a 50,000 ton final vehicle, you need 485 million tons of propellant - physically impossible to build.

**Conclusion**: Nuclear thermal/electric propulsion also eliminated.

## The Only Feasible Solution: Fusion Pulse Propulsion

Fusion pulse propulsion (from the Daedalus/Longshot design lineage) provides:
- Specific impulse (Isp): ~10⁶ seconds
- Recalculating with Isp = 1,000,000 s:
  - ln(mr) = 9,000,000/(1,000,000 × 9.8) ≈ 0.092
  - mr = e^0.092 ≈ 1.10 - that's manageable!

For deceleration at the end, the mass ratio is e^(v/(Isp × g)) ≈ 2.5, which is still acceptable.

## Two-Stage Configuration

Because we need to both accelerate and then decelerate at the destination, a two-stage configuration is required:
1. **First stage (acceleration stage)**: Provides all the initial acceleration to reach cruise speed, then is jettisoned
2. **Second stage (deceleration stage + habitat)**: Carries the habitat and payload, provides deceleration at the destination
3. **Magnetic sail**: Provides additional final braking with minimal mass cost

**Mission Timeline**:
- Acceleration phase: ~15 years
- Cruise phase: ~170 years
- Deceleration phase: ~15 years
- **Total**: 200 years - exactly meets the requirement

## The Two Hard Challenges

While propulsion is uniquely determined by the constraint, the real difficult problems that this project focuses on are:

### 1. 200-Year Cumulative Radiation Dose
- Galactic Cosmic Rays (GCR) at ~0.5 Sv/year inside an unshielded ship gives 100 Sv over 200 years - which is lethal
- Solution must combine multiple strategies: active magnetic shielding + passive water/propellant shielding + storm shelter for solar particle events

### 2. 200-Year Closed-Loop Life Support
- Zero resupply from Earth - water, oxygen, nitrogen must be nearly 100% recycled
- Food production must be 90%+ closed-loop
- Based on precedent from BIOS-3 (85% closure achieved in experiments) and ESA MELiSSA program

## Key Derived Constraints

The 200-year constraint also leads to other requirements:
- **Redundant systems**: All critical systems must have redundancy, because repairs can't be done from Earth
- **Radiation-hardened electronics**: Electronics must survive 200 years of cumulative radiation damage
- **On-board manufacturing**: Ability to manufacture replacement parts using 3D printing and machining (but note that chip manufacturing cannot be done on board, so system design must account for this)

## Related Pages
- [Design Principles](../project/design-principles.md)
- [Key Parameters](./key-parameters.md)
- [Propulsion](../subsystems/propulsion.md)
- [Radiation Shielding](../subsystems/radiation-shielding.md)
- [Life Support](../subsystems/life-support.md)
