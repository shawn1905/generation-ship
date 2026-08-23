// scripts/make_music_tracks.js
// 世代飞船双风格大型 Strudel 音乐生成与 URL 编码器

const fs = require('fs');
const path = require('path');

// 1. 星际穿越风格：向光孤巡 (The Solitary Crossing)
const interstellarCode = `// ============================================================
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
`;

// 2. 环太平洋风格：重构巨力 (Tectonic Rebuild)
const pacificRimCode = `// ============================================================
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
`;

function generateUrl(code) {
  const base64 = Buffer.from(code.trim()).toString('base64');
  return `https://strudel.cc/#${base64}`;
}

const url1 = generateUrl(interstellarCode);
const url2 = generateUrl(pacificRimCode);

console.log('=== 曲目 1：星际穿越风格 ===');
console.log(url1);
console.log('\n=== 曲目 2：环太平洋风格 ===');
console.log(url2);

// 保存到 artifacts/music/
const musicDir = path.join(__dirname, '..', 'artifacts', 'music');

fs.writeFileSync(path.join(musicDir, '向光孤巡_the_solitary_crossing.js'), interstellarCode, 'utf-8');
fs.writeFileSync(path.join(musicDir, '重构巨力_tectonic_rebuild.js'), pacificRimCode, 'utf-8');

const linksContent = `世代飞船 · 原创代码音乐播放链接（点开即听）：

1. 《向光孤巡》· The Solitary Crossing (星际穿越 / 管风琴极简主义)
坐标：文化×启航×④深空×工技×06音频物证
播放链接：${url1}

2. 《重构巨力》· Tectonic Rebuild (环太平洋 / 工业金属赛博铜管)
坐标：工程×竞赛×②地月系×工技×01主承力
播放链接：${url2}

3. 《C 区的曲子》· Sector C Suite (深空声音设计与衰变)
坐标：文化×启航×④深空×私档×06音频物证
播放链接：https://strudel.cc/#...
`;

fs.writeFileSync(path.join(musicDir, '播放链接.txt'), linksContent, 'utf-8');
console.log('\n✅ 音乐文件与播放链接已成功更新！');
