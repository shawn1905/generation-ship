// ============================================================
// 《重构巨力》· Tectonic Rebuild (L1 Orbital Gantry March, 2035 CE)
// 坐标：工程×竞赛×②地月系×工技×01主承力
// 风格：环太平洋 (Pacific Rim) / 赛博重工业摇滚 / 机甲与空间站锻造
// 概念：地月 L1 空间站与重型小行星动量拦截推进阵列合拢进行曲。
// ============================================================

setCpm(130) // 130 BPM 强力工业进行曲节奏

stack(
  // 声部 1：重金属失真锯齿吉他 Riff (Heavy Distorted Cyber Riff)
  // 经典主音动机：D -> F -> G -> Ab -> G -> F -> D
  note("<[d2 d2 f2 g2] [ab2 g2 f2 d2] [d2 d2 c2 d2] [f2 d2 g2 f2]>*2")
    .s("sawtooth,gm_electric_guitar_clean")
    .shape(0.65) // 强力失真过载
    .gain(0.9)
    .attack(0.01).release(0.18)
    .room(0.4),

  // 声部 2：史诗赛博铜管咆哮 (Epic Cyber Brass Horns)
  // 宏大管乐齐奏主旋律
  note("<[~ d4] [~ f4] [g4 ab4] [g4 ~] [~ d4] [~ c4] [f4 g4] [d4 ~]>")
    .slow(2)
    .s("gm_brass_section,gm_synth_brass_1")
    .attack(0.05).release(0.4)
    .lpf(3200)
    .room(0.75)
    .sz(0.8)
    .gain(0.95),

  // 声部 3：重型工业底鼓与地陷重击 (Heavy Industrial Kick & Sub)
  sound("<[bd:4 bd:4] [bd:4 ~] [bd:4 bd:4] [bd:4 [bd:4*2]]>")
    .gain(1.1)
    .shape(0.4)
    .room(0.3),

  // 声部 4：金属撞击军鼓与机械切分 (Metallic Snare & Clangs)
  sound("<[~ sn:2] [~ [sn:2,metal:3]] [~ sn:2] [[~ sn:2] [sn:2*2]]>")
    .gain(0.95)
    .room(0.5),

  // 声部 5：高速切分踩镲与气阀连击 (Hi-Hat Ratchets & Valve Exhaust)
  sound("hh*8")
    .sometimes(x => x.ply(2)) // 偶发 16 连音连击
    .pan(range(0.2, 0.8))
    .gain(0.55),

  // 声部 6：超重低音贝斯沉降 (Sub Bass Foundation)
  note("<d1 f1 g1 ab1 g1 f1 d1 c1>")
    .slow(2)
    .s("sine,sawtooth")
    .lpf(200)
    .attack(0.02).release(0.3)
    .gain(1.0)
)
