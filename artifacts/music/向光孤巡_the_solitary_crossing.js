// ============================================================
// 《向光孤巡》 The Solitary Crossing (3-Minute Deep Space Epic)
// Interstellar Style / Minimalist Pipe Organ & Relativistic Time
// Coordinate: Culture x Launch x Deep-Space (ARK-01 Year 50)
// ============================================================

setBpm(120)

// 6-Section 3-Minute Grand Deep Space Evolution (180s)
stack(
  // [Layer 1] Relativistic Ticking Clock (0:00 - 3:00)
  sound("wood:2*16")
    .gain(0.4)
    .pan(0.3)
    .hpf(1200)
    .room(0.4),

  // [Layer 2] Minimalist Organ Arpeggio Engine (Gradual Swell)
  // Progression: Am -> F -> C -> Em with dynamic LPF filter opening
  note("<[a4 c5 e5 c5 a4 e5]*2 [f4 a4 c5 a4 f4 c5]*2 [c4 e4 g4 e4 c4 g4]*2 [e4 g4 b4 g4 e4 b4]*2>")
    .s("piano,gm_church_organ")
    .velocity(slow(16, range(0.3, 0.85)))
    .attack(0.01).release(0.35)
    .lpf(slow(32, range(400, 5200))) // 32-bar slow filter sweep (3-min breathing)
    .room(0.85).sz(0.9)
    .gain(0.75),

  // [Layer 3] Grand Pipe Organ Solitary Theme (Enters at Bar 8)
  note("<[~ a5] [b5 c6] [~ g5] [e5 d5] [~ f5] [g5 a5] [~ e5] [b4 a4]>")
    .slow(4)
    .s("gm_church_organ,sawtooth")
    .attack(0.4).sustain(2.0).release(1.2)
    .vibrato(2.5).vibdepth(0.02)
    .room(0.95).sz(0.95)
    .gain(slow(16, range(0.4, 0.95))),

  // [Layer 4] 5.2km Hull Sub-Bass Gravitational Wave
  note("<[a1,a2] [f1,f2] [c1,c2] [e1,e2]>")
    .slow(4)
    .s("sawtooth,triangle")
    .lpf(slow(32, range(120, 500)))
    .attack(0.3).release(2.0)
    .room(0.7)
    .gain(0.9),

  // [Layer 5] Deep Space Shimmering Strings Pad
  note("<[e5,a5,c6] [c5,f5,a5] [g5,c6,e6] [b4,e5,g5]>")
    .slow(8)
    .s("pads")
    .attack(2.0).release(3.0)
    .jux(rev)
    .pan(0.7)
    .room(0.92)
    .gain(slow(24, range(0.2, 0.65)))
)
