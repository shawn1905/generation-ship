// 《向光孤巡》 The Solitary Crossing (Interstellar Style)
// 坐标：文化×启航×④深空×工技×06音频物证 (ARK-01 Year 50)

stack(
  // 1. 恒星际时间滴答 (Ticking Clock of Deep Time)
  note("c7*16")
    .s("triangle")
    .attack(0.005).release(0.03)
    .gain(0.25)
    .pan(0.3)
    .room(0.2),

  // 2. 管风琴快速极简琶音 (Minimalist Pipe Organ Arpeggio)
  // 和弦进行：Am -> F -> C -> Em (6/8拍)
  note("<[a4 c5 e5 c5 a4 e5]*2 [f4 a4 c5 a4 f4 c5]*2 [c4 e4 g4 e4 c4 g4]*2 [e4 g4 b4 g4 e4 b4]*2>")
    .s("triangle")
    .attack(0.01).release(0.25)
    .velocity(slow(8, range(0.4, 0.9)))
    .lpf(slow(16, range(600, 4500)))
    .room(0.8)
    .gain(0.7),

  // 3. 管风琴琶音声部中音增厚 (Organ Mid Harmonics)
  note("<[a3 c4 e4 c4 a3 e4]*2 [f3 a3 c4 a3 f3 c4]*2 [c3 e3 g3 e3 c3 g3]*2 [e3 g3 b3 g3 e3 b3]*2>")
    .s("sawtooth")
    .attack(0.02).release(0.2)
    .lpf(1200)
    .room(0.8)
    .gain(0.4),

  // 4. 孤绝长线条管风琴主旋律圣歌 (The Solitary Organ Anthem)
  note("<[~ a5] [b5 c6] [~ g5] [e5 d5] [~ f5] [g5 a5] [~ e5] [b4 a4]>")
    .slow(2)
    .s("triangle")
    .attack(0.2).decay(0.8).sustain(0.8).release(0.8)
    .room(0.95)
    .gain(0.85),

  // 5. 主旋律高八度光辉 (Theme Octave Shimmer)
  note("<[~ a6] [b6 c7] [~ g6] [e6 d6] [~ f6] [g6 a6] [~ e6] [b5 a5]>")
    .slow(2)
    .s("sine")
    .attack(0.3).release(1.0)
    .room(0.9)
    .gain(0.3),

  // 6. 5.2公里龙骨超低频重力波 (Sub-Bass Resonance)
  note("<[a1,a2] [f1,f2] [c1,c2] [e1,e2]>")
    .slow(2)
    .s("sawtooth")
    .lpf(slow(8, range(120, 380)))
    .attack(0.1).release(1.5)
    .room(0.6)
    .gain(0.9),

  // 7. 高维深空弦乐长垫 (Cosmic Strings Pad)
  note("<[e5,a5,c6] [c5,f5,a5] [g5,c6,e6] [b4,e5,g5]>")
    .slow(4)
    .s("sawtooth")
    .lpf(1600)
    .attack(1.2).release(2.0)
    .pan(0.7)
    .room(0.9)
    .gain(0.35)
).slow(1.2)
