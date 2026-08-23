// ============================================================
// 《向光孤巡》· The Solitary Crossing (ARK-01, Year 50 / 2200 CE)
// 坐标：文化×启航×④深空×工技×06音频物证
// 风格：星际穿越 (Interstellar) / 管风琴极简主义 / 深空时间膨胀
// 概念：ARK-01 巡航在 0.03c 深空，巡天主镜校准与全船向光日广播曲。
// ============================================================

setCpm(36) // 极慢的深空呼吸周期 (每分钟 36 个大循环周期)

stack(
  // 声部 1：时间滴答 (Ticking Clock of Deep Time) - 恒星际秒针
  sound("wood:2*16")
    .gain(0.4)
    .pan(0.3)
    .hpf(1200)
    .room(0.4),

  // 声部 2：管风琴极简主义快速琶音 (Minimalist Pipe Organ Arpeggios)
  // 6/8 拍经典和弦进行：Am -> F -> C -> Em
  note("<[a4 c5 e5 c5 a4 e5]*2 [f4 a4 c5 a4 f4 c5]*2 [c4 e4 g4 e4 c4 g4]*2 [e4 g4 b4 g4 e4 b4]*2>")
    .s("piano,gm_church_organ")
    .velocity(slow(8, range(0.35, 0.7)))
    .attack(0.01).release(0.4)
    .lpf(slow(16, range(800, 4800))) // 滤波器缓慢开合，模拟星际极光呼啸
    .room(0.85)
    .sz(0.9)
    .gain(0.75),

  // 声部 3：主旋律长线条管风琴圣歌 (The Solitary Organ Anthem)
  // 跨越八度的高亢单音线条，充满孤绝与敬畏
  note("<[~ a5] [b5 c6] [~ g5] [e5 d5] [~ f5] [g5 a5] [~ e5] [b4 a4]>")
    .slow(2)
    .s("gm_church_organ,sawtooth")
    .attack(0.3).sustain(1.2).release(0.8)
    .vibrato(2).vibdepth(0.02)
    .room(0.95)
    .sz(0.95)
    .gain(0.85),

  // 声部 4：低频重力波与龙骨共鸣 (Hull Sub-Bass Resonance)
  note("<[a1,a2] [f1,f2] [c1,c2] [e1,e2]>")
    .slow(2)
    .s("sawtooth,triangle")
    .lpf(slow(16, range(150, 450)))
    .attack(0.2).release(1.5)
    .room(0.7)
    .gain(0.9),

  // 声部 5：高维虚空弦乐垫 (Interstellar Strings Pad)
  note("<[e5,a5,c6] [c5,f5,a5] [g5,c6,e6] [b4,e5,g5]>")
    .slow(4)
    .s("pads")
    .attack(1.5).release(2.0)
    .jux(rev)
    .pan(0.7)
    .room(0.9)
    .gain(0.5)
)
