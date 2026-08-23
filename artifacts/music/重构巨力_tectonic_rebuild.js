// ============================================================
// 《重构巨力》 Tectonic Rebuild (3-Minute Industrial Cyber March)
// Pacific Rim Style / Heavy Distorted Metal Riff & Cyber Brass
// Coordinate: Engineering x Contest x Earth-Moon (L1 Gantry 2035)
// ============================================================

setBpm(132)

// 6-Section 3-Minute Industrial Heavy March (180s)
stack(
  // [Layer 1] Heavy Distorted Metal Cyber Guitar Riff
  // Theme: D -> F -> G -> Ab -> G -> F -> D (Heavy Syncopation)
  note("<[d2 d2 f2 g2] [ab2 g2 f2 d2] [d2 d2 c2 d2] [f2 d2 g2 f2]>*2")
    .s("sawtooth,gm_electric_guitar_clean")
    .shape(0.7) // High overdrive distortion
    .gain(0.9)
    .attack(0.01).release(0.16)
    .room(0.4),

  // [Layer 2] Epic Cyber Brass Section (Heroic Anthem)
  note("<[~ d4] [~ f4] [g4 ab4] [g4 ~] [~ d4] [~ c4] [f4 g4] [d4 ~]>")
    .slow(4)
    .s("gm_brass_section,gm_synth_brass_1")
    .attack(0.05).release(0.4)
    .lpf(3400)
    .room(0.8).sz(0.85)
    .gain(slow(16, range(0.5, 1.0))),

  // [Layer 3] Heavy Industrial Taiko & Sub Kick (132 BPM Impact)
  sound("<[bd:4 bd:4] [bd:4 ~] [bd:4 bd:4] [bd:4 [bd:4*2]]>")
    .gain(1.15)
    .shape(0.45)
    .room(0.35),

  // [Layer 4] Metallic Clang Snare & Industrial Hits
  sound("<[~ sn:2] [~ [sn:2,metal:3]] [~ sn:2] [[~ sn:2] [sn:2*2]]>")
    .gain(0.95)
    .room(0.5),

  // [Layer 5] High-Speed Hi-Hat Ratchets & Pneumatic Exhaust
  sound("hh*8")
    .sometimes(x => x.ply(2))
    .pan(range(0.2, 0.8))
    .gain(0.55),

  // [Layer 6] Sub-Bass Gantry Foundation (200Hz Low End)
  note("<d1 f1 g1 ab1 g1 f1 d1 c1>")
    .slow(4)
    .s("sine,sawtooth")
    .lpf(220)
    .attack(0.02).release(0.35)
    .gain(1.05)
)
