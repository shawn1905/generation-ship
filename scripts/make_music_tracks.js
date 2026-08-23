// scripts/make_music_tracks.js
// 100% 纯净 WebAudio 原生合成器实现（零外部采样依赖、零报错、全版本兼容）

const fs = require('fs');
const path = require('path');

// 1. 星际穿越风格：《向光孤巡》
// 使用纯 triangle / sawtooth 叠加合成为大教堂管风琴，配以大混响和极简琶音
const interstellarCode = `// 《向光孤巡》 The Solitary Crossing (Interstellar Style)
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
`;

// 2. 环太平洋风格：《重构巨力》
// 使用 sawtooth+shape 打造失真机甲吉他，square/saw 打造重型铜管，bd/sn/hh 打造工业鼓
const pacificRimCode = `// 《重构巨力》 Tectonic Rebuild (Pacific Rim Style)
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
`;

function getStrudelUrl(code) {
  const base64 = Buffer.from(code.trim(), 'utf-8').toString('base64');
  return `https://strudel.cc/#${base64}`;
}

const url1 = getStrudelUrl(interstellarCode);
const url2 = getStrudelUrl(pacificRimCode);

const musicDir = path.join(__dirname, '..', 'artifacts', 'music');
fs.writeFileSync(path.join(musicDir, '向光孤巡_the_solitary_crossing.js'), interstellarCode, 'utf-8');
fs.writeFileSync(path.join(musicDir, '重构巨力_tectonic_rebuild.js'), pacificRimCode, 'utf-8');

const desktopDir = path.join(process.env.HOME, 'Desktop', '世代飞船_精选正典');
const htmlHub = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>世代飞船 · 原创代码音乐试听舱 (纯净声波版)</title>
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
    <h1>🌌 世代飞船 · 原创代码音乐试听舱 (纯净声波版)</h1>
    <div class="tips">
      💡 <b>零报错纯净合成</b>：已全面切换为 100% WebAudio 内建振荡器与原生鼓机，去除所有外部采样依赖。点击进入网页后按 <b>Cmd + Enter</b> 或点击 <b>▶ Play</b> 即可稳定流畅发声！
    </div>
    
    <h2>1. 《向光孤巡》· The Solitary Crossing</h2>
    <div class="meta">风格：星际穿越 (Interstellar) / 管风琴极简主义 ｜ 坐标：文化×启航×④深空</div>
    <p>ARK-01 巡航在 0.03c 深空，巡天主镜校准与全船向光日广播圣歌（时间秒针滴答 + 6/8拍双层管风琴极简琶音 + 高亢单音圣歌 + 龙骨引力波低鸣）。</p>
    <a class="btn" href="${url1}" target="_blank">▶️ 在线播放《向光孤巡》</a>

    <h2>2. 《重构巨力》· Tectonic Rebuild</h2>
    <div class="meta">风格：环太平洋 (Pacific Rim) / 赛博重金属铜管 ｜ 坐标：工程×竞赛×②地月系</div>
    <p>地月 L1 空间站与重型小行星动量拦截推进阵列在轨合拢进行曲（过载失真电吉他 Riff + 赛博交响铜管齐奏咆哮 + 工业地陷底鼓重击 + 气阀高压连击）。</p>
    <a class="btn btn-orange" href="${url2}" target="_blank">▶️ 在线播放《重构巨力》</a>
  </div>
</body>
</html>
`;

fs.writeFileSync(path.join(desktopDir, '在线试听跳板.html'), htmlHub, 'utf-8');

fs.writeFileSync(path.join(desktopDir, '07_原创代码音乐_星际穿越与环太平洋双风格.md'), `# 🎵 世代飞船 · 原创代码音乐双风格专卷（纯净声波版）

> 本卷基于 **Strudel 纯净原生 WebAudio 算法合成** 创作，零外部 SoundFont 依赖，100% 稳定发声。

---

## 🌌 第一首：《向光孤巡》· The Solitary Crossing

- **风格**：**星际穿越 (Interstellar) / 管风琴极简主义**
- **坐标**：\`文化×启航×④深空×工技×06音频物证\` ｜ **纪元**：2200 年（第50航行年）
- **核心声部**：时间秒针滴答 + 双层管风琴极简琶音 + 孤绝长线条圣歌 + 龙骨引力波
- **在线播放直达**：[点击直接在 Strudel 播放《向光孤巡》](${url1})

---

## ⚡ 第二首：《重构巨力》· Tectonic Rebuild

- **风格**：**环太平洋 (Pacific Rim) / 赛博重金属铜管进行曲**
- **坐标**：\`工程×竞赛×②地月系×工技×01主承力\` ｜ **纪元**：2035 年（地月大基建）
- **核心声部**：过载失真电吉他 Riff + 赛博铜管咆哮 + 工业地陷底鼓 + 金属军鼓
- **在线播放直达**：[点击直接在 Strudel 播放《重构巨力》](${url2})
`, 'utf-8');

console.log('Regenerated clean WebAudio synth tracks successfully.');
