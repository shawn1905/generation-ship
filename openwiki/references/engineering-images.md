---
type: reference
title: NASA Engineering Reference Images
description: Curated NASA Image and Video Library downloads organized by ship subsystem, with API quick reference and usage notes for the generation ship design
tags: [reference, images, nasa]
---
# NASA Engineering Reference Images

The repository contains a curated collection of NASA public-domain reference images in `/docs/nasa_参考影像/`, downloaded from the [NASA Image and Video Library](https://images.nasa.gov/) (official, keyless, mostly public domain). 16 core images (43 MB) are cached in `images/`, named by NASA ID. The collection documentation (`README.md` in that directory) is organized by design need rather than by generic subsystem folders.

## API Quick Reference (keyless)

```
搜索:  https://images-api.nasa.gov/search?q={关键词}&media_type=image
详情:  https://images-api.nasa.gov/asset/{nasa_id}      -> lists all resolution variants
直链:  https://images-assets.nasa.gov/image/{id}/{id}~{orig|large|medium|small|thumb}.jpg
网页:  https://images.nasa.gov/details/{nasa_id}
```

Note: some old scans only have `orig`/`small` (no `large`); `orig` can reach 30 MB, so prefer `large` for local storage.

## Collection Sections

### 1. Rotating Habitat (closest to the main design thread - ✧4 reference)

The **1975 NASA Ames + Stanford summer study (NASA SP-413, *Space Settlements: A Design Study*)**, artists Don Davis / Rick Guidice. This is the most serious engineering concept design of rotating habitats ever produced and directly anchors the twin-ring habitat layout (Phase 2). Local images include:
- `ARC-1975-AC75-2621` - Don Davis ring-habitat interior (farmland, homes along the ring)
- `ARC-1975-AC75-1920` - Don Davis L-5 ring interior
- `ARC-1976-AC76-1267` - Rick Guidice full ring wheel view (SP-413 cover-class)
- `ARC-1975-AC75-1086` - Rick Guidice living area (recumbent view)
- `ARC-1975-AC75-1886` - Don Davis ring wheel construction/assembly
- `ARC-1976-AC76-0525` - ring colony exterior (multiple adjacent colonies)
- Plus **Bernal Sphere** alternates (the O'Neill-lineage comparison): `ARC-1975-AC75-1924`, `ARC-1976-AC76-1089`, `AC76-0628` (sphere cross-section showing gravity strongest at the equator)

### 2. Propulsion (real-world anchors for fusion pulse)

- `9902054` / `9902053` - **NERVA nuclear thermal rocket** 1963 concept art - the real engineering start of nuclear propulsion
- `9906395` / `9906382` - **Project Orion** nuclear pulse propulsion - same lineage as Daedalus fusion pulse; the disc-shaped pulse units + shock absorbers are the most credible shape reference for the fusion pulse stage
- `ACS3_SolarPanels_001` - **ACS3 advanced composite solar sail** (in orbit 2024) - real-world reference for the final magnetic-sail/light-sail braking

### 3. Closed-Loop Life Support / Space Agriculture (200-year zero-resupply)

- `KSC-20190613-PH_KLS01_0084` and the APH series - **Advanced Plant Habitat** radish harvest - realistic space-planting module texture
- Veggie series (`KSC-20170808-PH_CSH01_0080` etc., online only) - lettuce/mustard growing in "plant pillows"
- Search terms: `Advanced Plant Habitat`, `Veggie plant`, `plant growth chamber`

### 4. Real On-Orbit Interiors (modeling materials/piping reference)

- `iss017e015059` - ISS Zvezda service module interior (piping/equipment density reference)
- Online only: more module interiors, `S99-00157` TransHab inflatable habitat full-scale model, NextSTEP deep-space habitat prototypes (Lockheed/Boeing etc.), `jsc2024e041788` Gateway lunar space station configuration

### 5. Deep-Space Backgrounds (rendering environment maps / atmosphere)

- `carina_nebula` - JWST Carina "Cosmic Cliffs" - cruise-phase window background
- `GSFC_20171208_Archive_e000214` - Hubble's Alpha Centauri A/B - the destination star system (Proxima Centauri's triple system), a real photo
- Online only: terrestrial exoplanet art concepts (arrival-phase target planet references)

## Usage Suggestions (from the collection README)

1. **Phase 2 internal structure**: the ring-habitat series maps directly to deck compartmentalization and twin-ring layout; the full SP-413 report ([PDF, NTRS](https://ntrs.nasa.gov/citations/19770076862)) contains a **10,000-person population mass/area budget table** - the anchor for [Phase 0 population accounting](../engineering/budgets.md)
2. **Materials/textures**: the ring-interior paintings' "white skeleton + green farmland + blue sky windows" is the classic paradigm; the 200-year ship may deliberately deviate (darker, more industrial), and ISS real photos provide the true piping-density baseline
3. **Propulsion shape**: Orion's disc-shaped pulse units + shock absorbers are the most credible external shape reference for the fusion-pulse stage
4. The search API is long-lived; find more images in the same series with the keywords above

## Licensing

NASA imagery is public domain by default (minor non-commercial restrictions); credit "Image credit: NASA". Ames concept art: "NASA Ames Research Center / Don Davis / Rick Guidice". JWST/Hubble images note STScI credit.

## Related Pages
- [Habitat Subsystem](../subsystems/habitat.md) - the rotating twin-ring design this collection anchors
- [Mass, Power & Population Budgets](../engineering/budgets.md) - Phase 0 budget methodology referencing SP-413
- [Literature References](./literature.md)
