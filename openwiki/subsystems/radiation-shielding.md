---
type: subsystem
title: Radiation Shielding
description: Combined radiation shielding solution for 200-year interstellar travel
tags: [subsystem, radiation, shielding]
---
# Radiation Shielding

Radiation shielding is the biggest technical challenge for a 200-year interstellar mission. Cumulative radiation dose over 200 years would be lethal without effective shielding. The design uses a combined approach of multiple shielding strategies to keep the total dose within safe limits.

## The Radiation Problem

- **Galactic Cosmic Rays (GCR)**: Constant low-intensity high-energy radiation from outside the Solar System
- **Solar Particle Events (SPE)**: Occasional bursts of high-energy particles from solar activity
- Without shielding: ~0.5 Sv/year inside the ship → 100 Sv over 200 years → 100 Sv is lethal for humans
- Safe limit: The goal is to keep total cumulative dose below 20 Sv over 200 years

## Combined Shielding Strategy

The solution combines three different shielding approaches for maximum effectiveness with minimum mass:

### 1. Active Superconducting Dipole Magnetic Shielding

This is the first line of defense:
- A large superconducting magnetic dipole creates a magnetic field that deflects most charged cosmic rays
- Reduces the GCR flux reaching the habitat by a factor of 3-5
- This is the most mass-efficient approach for primary shielding
- Requires superconducting technology that's actively being developed today
- Needs cryogenic cooling for the superconductors

### 2. Passive Shielding: Water / Propellant Tanks

The second layer is passive shielding:
- The water and propellant tanks that we already need to carry anyway are arranged around the habitat
- Water is very effective at absorbing radiation
- Any cosmic rays that get past the magnetic shield are absorbed or scattered by the water
- This is mass-efficient because we don't need to carry extra mass just for shielding - we use what we already need

### 3. Emergency Storm Shelter

The third layer is for solar particle events (SPE):
- A central, heavily shielded storm shelter located in the core of the habitat
- Dense material (like lead or water) provides additional shielding during large SPE events
- Crew stays in the shelter for the duration of the event (days to a week)
- Minimal additional mass is needed because it's only a small area

## Mass Implications

Radiation shielding is the single largest mass component of the entire ship:
- Approximately 40-50% of the total ship mass is associated with radiation shielding
- This is why the combined approach is important - it minimizes the total mass needed

## Current Research Status

Active magnetic shielding for space missions is an active area of research:
- Multiple concepts have been studied by NASA and other space agencies
- The main challenges are maintaining the superconducting magnets and handling the cryogenics over 200 years
- This project assumes that this technology will be available when the ship is built

## Related Pages
- [Core Constraints](../design/core-constraints.md)
- [Overall Ship Configuration](../design/ship-configuration.md)
- [Budgets](../engineering/budgets.md)
- [Habitat](./habitat.md)
