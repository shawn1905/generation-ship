// scripts/make_flight_log_audio.js
// 世代飞船航行日志声学复原 (Flight Log Acoustic Telemetry Synthesis)
// 专为《曙光三环中央垂直中枢第19号降轨进港指令与航行日志》(GS-2096-02) 定制

const fs = require('fs');
const path = require('path');

const flightLogAudioCode = `// ============================================================
// 《信天翁-09降轨进港黑匣子遥测声学复原》
// Albatross-09 Inbound Telemetry Acoustic Log (GS-2096-02)
// 坐标：工程×离心×③内太阳系×工技×01主承力 (三环历7年第203日)
// 场景：重型穿梭机从北极天井降轨至中央离心球核4号泊位全过程声学记录
// ============================================================

setBpm(96) // 航行进港管制基准节奏

stack(
  // 1. 主轴向导航多普勒信标 (Navigation Doppler Carrier Beacon)
  // 模拟天井入口 500m 激光测距脉冲，带有微弱频率漂移
  note("<[b5 ~] [e6 ~] [b5 b5] [e6 [b5*2]]>")
    .s("sine")
    .attack(0.005).release(0.08)
    .gain(0.4)
    .pan(0.4)
    .room(0.35),

  // 2. RCS 姿态微调喷气脉冲 (RCS Thruster Bursts)
  // 模拟穿梭机进入减速走廊时的离散高压气体点动
  sound("<[~ hh:2] [hh:2 ~] [~ [hh:2*2]] [hh:2 [~ hh:2]]>")
    .gain(0.45)
    .hpf(2000)
    .pan(range(0.2, 0.8)),

  // 3. 旋转主环低频自转惯性共鸣 (Centrifugal Hull Hum: 1.56 rpm)
  // 286米地板自转产生的 0.78g 环面机械低频嗡鸣
  note("<[d1,a1] [e1,b1] [d1,a1] [g1,d2]>")
    .slow(4)
    .s("sawtooth")
    .lpf(slow(8, range(90, 220)))
    .attack(0.4).release(2.0)
    .room(0.7)
    .gain(0.85),

  // 4. 重力梯度换挡状态提示音 (Gravity Gradient Status Chime)
  // 穿梭机在 r=172m (0.47g) 与 r=57m (0.16g) 换挡位时座舱语音终端提示音
  note("<[~ e5] [~ b4] [~ a4] [e5 ~]>")
    .slow(2)
    .s("triangle")
    .attack(0.02).decay(0.4).sustain(0.3).release(0.6)
    .room(0.8)
    .gain(0.6),

  // 5. 泊位雷达接近率脉冲时钟 (Proximity Radar Telemetry Clock)
  // 随着靠近球核 4 号泊位，16 分音符脉冲持续打卡
  note("a6*8")
    .s("triangle")
    .attack(0.002).release(0.02)
    .gain(0.2)
    .pan(0.6),

  // 6. 液压卡爪硬对接锁定准备 (Hydraulic Clamp Arming Bass Impact)
  // 每 4 拍一次的沉重机械就位重音
  sound("<bd:2 ~ [~ bd:2] ~>")
    .shape(0.3)
    .gain(0.8)
    .room(0.4)
)
`;

function getStrudelUrl(code) {
  const base64 = Buffer.from(code.trim(), 'utf-8').toString('base64');
  return `https://strudel.cc/#${base64}`;
}

const url = getStrudelUrl(flightLogAudioCode);

// 写入 artifacts/music/
const musicDir = path.join(__dirname, '..', 'artifacts', 'music');
fs.writeFileSync(path.join(musicDir, '航行日志_信天翁09进港遥测_flight_log_telemetry.js'), flightLogAudioCode, 'utf-8');

// 写入桌面
const desktopDir = path.join(process.env.HOME, 'Desktop', '世代飞船_精选正典');
fs.writeFileSync(path.join(desktopDir, '08_航行日志声学复原_信天翁09进港黑匣子.md'), `# 📡 航行日志声学复原物证（Flight Log Telemetry Audio）

> 本音频为正典公文 **《曙光三环中央垂直中枢第19号降轨进港指令与航行日志》（GS-2096-02）** 的配属黑匣子遥测声学复原物证。

---

## 🚀 航行日志背景

- **对应公文**：\`artifacts/writing/曙光三环中央垂直中枢第19号降轨进港指令与航行日志.md\`
- **工单批号**：航-管-2096-19A
- **进港载具**：环带货运自治公会 重型穿梭机「信天翁-09」（机长 48 米）
- **进港航线**：北极轴向天井 ➔ 中央离心球核 4 号泊位（轴向 500 米减速走廊）
- **时间锚点**：三环历 7 年第 203 日（公元 2096 年 8 月下旬）

---

## 🎧 声音物理剖面（六层遥测信号）

1. **导航激光多普勒信标（Doppler Carrier Beacon）**：高频多普勒脉冲，带有向轴心靠近时的频移；
2. **RCS 姿态喷气微调（RCS Thruster Bursts）**：高压冷气姿控喷射，控制穿梭机进入管制走廊；
3. **主环自转低频惯性共振（Centrifugal Hull Hum）**：286 米地板自转（1.56 rpm，0.78g）产生的巨构机械低鸣；
4. **重力梯度换挡提示音（Gravity Gradient Chime）**：穿过 0.47g（r=172m）与 0.16g（r=57m）换挡参照位时的座舱状态音；
5. **雷达接近率脉冲时钟（Proximity Radar Clock）**：高频数据打卡脉冲；
6. **液压卡爪对接锁定准备（Hydraulic Clamp Impact）**：低沉的泊位卡爪机械重音。

---

## ▶️ 在线试听直达

👉 **[点击直接在 Strudel 播放《信天翁-09进港遥测音频》](${url})**

*(打开页面后点击左上角 ▶ Play 按钮，或按 Cmd + Enter 即可实时合成收听！)*
`, 'utf-8');

console.log('Flight log telemetry audio generated successfully.');
console.log('URL:', url);
