---
type: subsystem
title: Propulsion System
description: Two-stage fusion pulse propulsion system with magnetic sail braking
tags: [subsystem, propulsion, fusion]
---
# Propulsion System

The propulsion system is a two-stage fusion pulse propulsion design based on the Project Daedalus and Project Longshot lineage, which is the only feasible solution for a 200-year mission to Proxima Centauri.

## Design Heritage

- **Project Daedalus** (British Interplanetary Society, 1978): Original fusion pulse propulsion design for an uncrewed 50-year flyby mission to Barnard's Star
- **Project Longshot** (US Naval Academy, 1988): Fission-initiated fusion design for a 100-year uncrewed mission to Alpha Centauri
- This project adapts this approach for a crewed generation ship with 200-year mission duration

## Why Fusion Pulse Propulsion?

- Provides specific impulse (Isp) ~10⁶ seconds, which is the only way to reach 0.03c with a reasonable mass ratio
- Inertial confinement fusion is a known approach that's being actively researched today
- Scales well to the large power levels needed for this mission

## Two-Stage Configuration

### Stage 1: Acceleration Stage
- Larger stage with more fusion fuel
- Provides all the initial acceleration to bring the entire ship up to cruise speed of ~0.03c
- After acceleration is complete (about 15 years), this stage is jettisoned to reduce mass during cruise
- Jettisoning the empty stage improves overall mission efficiency

### Stage 2: Deceleration Stage
- Smaller stage that remains attached to the habitat and payload for the entire mission
- Carries enough fusion fuel to decelerate the habitat and payload at the destination
- After deceleration, it remains attached to the habitat as a power source for the colonization effort

## Fusion Pulse Operation

The basic operating principle:
1. Small fusion pellets are injected into the combustion chamber
2. Each pellet is ignited (inertial confinement using laser or particle beams)
3. The fusion explosion creates a plasma pulse that pushes against the pusher plate
4. The momentum from the pulse accelerates the ship forward
5. This repeats at a certain rate to provide continuous thrust

Benefits of this approach:
- High specific impulse
- Proven design concept that has been studied in depth
- Scales well to large thrust levels

## Magnetic Sail Final Braking

After the second stage fusion deceleration, a magnetic sail is deployed for final braking:
- Large superconducting magnetic loop deployed behind the ship
- The magnetic field interacts with the interstellar medium to provide additional drag
- This reduces the amount of fuel that needs to be carried for deceleration
- Minimal mass penalty compared to carrying extra fusion fuel

## Power Generation

The fusion reactor that powers propulsion also provides electrical power for the entire ship during cruise:
- 10-100 MW(e) needed for life support, habitat systems, and active shielding
- The same fusion technology used for propulsion can generate electricity

## Related Pages
- [Core Constraints](../design/core-constraints.md)
- [Key Parameters](../design/key-parameters.md)
- [Overall Ship Configuration](../design/ship-configuration.md)
- [Radiation Shielding](./radiation-shielding.md)
