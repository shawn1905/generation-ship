// ============================================================
// 《C 区的曲子》— Sector C Suite (ARK-01, Year 137)
// 世代飞船「方舟号 ARK-01」· C 区环境音乐
// 概念:启航时设计师给每个舱段写了专属环境音乐;137 年后
// 设备老化、音高漂移、循环错位,音乐在变异。船员习以为常的
// "C 区的脾气",其实是一首正在腐烂的曲子。
// 有一天有人从地球备份里听到"原版"——和现在的版本已完全不同。
// 哪一个才是这艘船真正的声音?
//
// 结构(四层,同时发声):
//   L1  Earth Backup 地球备份:干净、对齐、完整的原曲(钢琴和弦)
//   L2  The Decay    船上活版本:同一主题,音高漂移 + 回声漂移 + 偶发丢音,
//                     循环被拉长 0.375%——与备份永不重合,缓慢错位
//   L3  The Hull     船体低鸣:低音垫,缓慢漂移像金属热胀冷缩
//   L4  The Pump     农业环水泵:三角波琶音,偶发失稳,像老水泵喘振
// ============================================================

const ratchet = register('ratchet', (pat) => pat.sometimes(ply(2)))

stack(
  // L1 · 地球备份(原曲,干净版)— 和弦 Am - F - C - G
  note("<[a4 e5] [b4 e5] [c5 e5] [b4 e5]>*2")
    .s("piano")
    .velocity(0.4)
    .attack(0.01).release(0.5)
    .room(0.6)
    .gain(0.8),

  // L2 · 第 137 年的活版本(同一首曲子,正在腐烂)
  note("<[a4 e5] [b4 e5] [c5 e5] [b4 e5]>*2")
    .slow(8.03)
    .s("piano")
    .velocity(0.4)
    .attack(0.01).release(0.5)
    .add(slow(32, range(-0.05, 0.05)))          // 音高慢漂移(半音级)
    .delay(0.5).delaytime(slow(8, range(0.35, 0.42))).delayfeedback(0.45) // 回声被拉扯
    .sometimes(x => x.degradeBy(0.125))         // 继电器老化,偶发丢音
    .room(0.7)
    .gain(0.8),

  // L3 · 船体自身的低鸣(推进段骨架共振)
  note("<[a1,a2,e3] [f1,f2,c3] [c2,c3,g3] [g1,g2,d3]>")
    .slow(2)
    .s("pads")
    .velocity(0.6)
    .sustain(4)
    .add(slow(16, range(-0.03, 0.03)))
    .room(0.9)
    .gain(0.4),

  // L4 · 农业环 3 号循环水泵(第 137 年,已更换 4 次)
  note("[a4 c5 e5 c5]*4")
    .slow(8.03)
    .s("triangle")
    .attack(0.01).release(0.1)
    .velocity(0.3)
    .jux(rev)
    .lpf(1200)
    .sometimes(x => x.degradeBy(0.08))
    .room(0.3)
    .gain(0.5)
)
