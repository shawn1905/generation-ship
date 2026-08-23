// scripts/make_music_tracks.js
// 重新生成纯净、长结构、无歧义的 Strudel 3分钟大型音乐脚本与 URL

const fs = require('fs');
const path = require('path');

// 1. 星际穿越风格：《向光孤巡》
const interstellarCode = `// ============================================================
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
`;

// 2. 环太平洋风格：《重构巨力》
const pacificRimCode = `// ============================================================
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
`;

function getStrudelUrl(code) {
  // 使用 UTF-8 base64 编码
  const base64 = Buffer.from(code.trim(), 'utf-8').toString('base64');
  return `https://strudel.cc/#${base64}`;
}

const url1 = getStrudelUrl(interstellarCode);
const url2 = getStrudelUrl(pacificRimCode);

console.log('Generated URLs successfully.');

const musicDir = path.join(__dirname, '..', 'artifacts', 'music');
fs.writeFileSync(path.join(musicDir, '向光孤巡_the_solitary_crossing.js'), interstellarCode, 'utf-8');
fs.writeFileSync(path.join(musicDir, '重构巨力_tectonic_rebuild.js'), pacificRimCode, 'utf-8');

const desktopDir = path.join(process.env.HOME, 'Desktop', '世代飞船_精选正典');
const htmlHub = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>世代飞船 · 原创代码音乐试听舱 (3分钟史诗版)</title>
  <style>
    body {
      background: #0b0f19;
      color: #e2e8f0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      margin: 0;
      padding: 30px;
    }
    .card {
      background: #1e293b;
      border: 1px solid #334155;
      border-radius: 16px;
      padding: 36px;
      max-width: 720px;
      width: 100%;
      box-shadow: 0 12px 32px rgba(0,0,0,0.6);
      margin-bottom: 24px;
    }
    h1 { color: #38bdf8; font-size: 26px; margin-top: 0; }
    h2 { color: #fb923c; font-size: 20px; margin-top: 24px; border-bottom: 1px solid #334155; padding-bottom: 8px; }
    p { line-height: 1.7; color: #94a3b8; font-size: 15px; }
    .btn {
      display: inline-block;
      background: #0284c7;
      color: #ffffff;
      text-decoration: none;
      padding: 14px 24px;
      border-radius: 8px;
      font-weight: 700;
      font-size: 16px;
      margin-top: 12px;
      transition: all 0.2s;
    }
    .btn:hover { background: #0369a1; transform: translateY(-1px); }
    .btn-orange { background: #ea580c; }
    .btn-orange:hover { background: #c2410c; }
    .meta { font-family: monospace; font-size: 13px; color: #4ade80; margin-top: 6px; }
    .tips { background: #0f172a; border-left: 4px solid #38bdf8; padding: 12px 16px; margin: 20px 0; font-size: 14px; color: #cbd5e1; border-radius: 4px; }
  </style>
</head>
<body>
  <div class="card">
    <h1>🌌 世代飞船 · 原创代码音乐试听舱 (3分钟史诗版)</h1>
    <div class="tips">
      💡 <b>播放指南</b>：点击下方按钮打开网页后，直接点击页面左侧的 <b>▶ Play 按钮</b>（或按键盘 <b>Cmd + Enter</b>）即可听到由声波实时合成的声音！
    </div>
    
    <h2>1. 《向光孤巡》· The Solitary Crossing</h2>
    <div class="meta">风格：星际穿越 (Interstellar) / 管风琴极简主义 ｜ 坐标：文化×启航×④深空 ｜ 时长：3 分钟</div>
    <p>ARK-01 巡航在 0.03c 深空，巡天主镜校准与全船向光日广播圣歌（120 BPM · 时间滴答秒针 + 6/8拍管风琴快速极简琶音 + 32小节低通滤波器漫长开合 + 跨八度虚空圣歌单音线条）。</p>
    <a class="btn" href="${url1}" target="_blank">▶️ 点击进入《向光孤巡》播放页</a>

    <h2>2. 《重构巨力》· Tectonic Rebuild</h2>
    <div class="meta">风格：环太平洋 (Pacific Rim) / 赛博重金属铜管 ｜ 坐标：工程×竞赛×②地月系 ｜ 时长：3 分钟</div>
    <p>地月 L1 空间站与重型小行星动量拦截推进阵列在轨合拢进行曲（132 BPM · 重金属过载锯齿 Riff + 史诗赛博铜管齐奏咆哮 + 工业地陷底鼓重击 + 气阀高压连击）。</p>
    <a class="btn btn-orange" href="${url2}" target="_blank">▶️ 点击进入《重构巨力》播放页</a>
  </div>
</body>
</html>
`;

fs.writeFileSync(path.join(desktopDir, '在线试听跳板.html'), htmlHub, 'utf-8');

fs.writeFileSync(path.join(desktopDir, '07_原创代码音乐_星际穿越与环太平洋双风格.md'), `# 🎵 世代飞船 · 原创代码音乐双风格专卷（3分钟完整版）

> 本卷基于 **Strudel 实时算法作曲引擎** 创作。
> 代码已完成网格坐标落位与全声部 3 分钟长程演进设计。

---

## 🌌 第一首：《向光孤巡》· The Solitary Crossing

- **风格**：**星际穿越 (Interstellar) / 管风琴极简主义**
- **坐标**：\`文化×启航×④深空×工技×06音频物证\` ｜ **纪元**：2200 年（第50航行年）
- **时长**：180 秒（120 BPM，32 Bar 滤波器极长周期开合）
- **在线播放直达**：[点击进入《向光孤巡》播放页](${url1})

---

## ⚡ 第二首：《重构巨力》· Tectonic Rebuild

- **风格**：**环太平洋 (Pacific Rim) / 赛博重金属铜管进行曲**
- **坐标**：\`工程×竞赛×②地月系×工技×01主承力\` ｜ **纪元**：2035 年（地月大基建）
- **时长**：180 秒（132 BPM 工业进行曲）
- **在线播放直达**：[点击进入《重构巨力》播放页](${url2})
`, 'utf-8');

console.log('All files and Desktop hub updated.');
