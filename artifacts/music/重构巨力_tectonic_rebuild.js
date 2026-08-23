// 《重构巨力》 Tectonic Rebuild (Pacific Rim Style)
// 坐标：工程×竞赛×②地月系×工技×01主承力 (L1 Gantry 2035)

stack(
  // 1. 重型失真赛博电吉他 Riff (Heavy Distorted Cyber Riff)
  // 核心动机：D -> F -> G -> Ab -> G -> F -> D (重切分音型)
  note("<[d2 d2 f2 g2] [ab2 g2 f2 d2] [d2 d2 c2 d2] [f2 d2 g2 f2]>*2")
    .s("sawtooth")
    .shape(0.75) // 强力失真过载
    .lpf(2200)
    .attack(0.01).release(0.14)
    .room(0.3)
    .gain(0.9),

  // 2. 史诗赛博铜管咆哮主旋律 (Epic Cyber Brass Anthem)
  note("<[~ d4] [~ f4] [g4 ab4] [g4 ~] [~ d4] [~ c4] [f4 g4] [d4 ~]>")
    .slow(2)
    .s("sawtooth")
    .lpf(3200)
    .attack(0.05).decay(0.3).sustain(0.7).release(0.3)
    .room(0.7)
    .gain(0.95),

  // 3. 铜管低八度加重 (Brass Low Octave Double)
  note("<[~ d3] [~ f3] [g3 ab3] [g3 ~] [~ d3] [~ c3] [f3 g3] [d3 ~]>")
    .slow(2)
    .s("square")
    .lpf(1800)
    .attack(0.05).release(0.3)
    .room(0.6)
    .gain(0.75),

  // 4. 重型工业底鼓 (Heavy Industrial Kick)
  sound("<[bd bd] [bd ~] [bd bd] [bd [bd*2]]>")
    .shape(0.4)
    .gain(1.1)
    .room(0.2),

  // 5. 金属撞击军鼓 (Metallic Industrial Snare)
  sound("<[~ sn] [~ sn] [~ sn] [[~ sn] [sn*2]]>")
    .gain(0.95)
    .room(0.4),

  // 6. 高速切分金属踩镲与高压排气 (Hi-Hat Ratchets)
  sound("hh*8")
    .sometimes(x => x.ply(2))
    .pan(range(0.2, 0.8))
    .gain(0.5),

  // 7. 200Hz 地陷超重低音 (Sub-Bass Foundation)
  note("<d1 f1 g1 ab1 g1 f1 d1 c1>")
    .slow(2)
    .s("sine")
    .lpf(220)
    .attack(0.02).release(0.3)
    .gain(1.1)
).fast(1.1)
