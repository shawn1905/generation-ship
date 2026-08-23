#!/usr/bin/env python3
"""世代飞船全真电影级黑匣子语音与环境音效引擎 (Cinematic Telemetry Soundscape Engine v2.0)

使用 Azure 神经网络真人语音 (edge-tts) + 多轨声效合成 (Foley & DSP)：
  1. 真实真人语调起伏、换气与动态节奏
  2. RCS 姿控高压冷气喷射声 (Pneumatic Thruster Blasts)
  3. 液压卡爪硬对接锁定金属撞击 (Hydraulic Clamp Heavy Metal Impact)
  4. 旋转天井 500 米中枢低频自转共振 (Centrifugal Deep Hull Hum)
  5. 接近率雷达脉冲时钟与多普勒导航信标 (Radar Telemetry & Doppler Ping)
  6. 航天窄带滤波与 Quindar 按键音 (Apollo/Deep Space Radio FX)
"""

import asyncio
import os
import subprocess
import pathlib
import edge_tts

ROOT = pathlib.Path(__file__).resolve().parent.parent
TMP_DIR = ROOT / "scripts" / "tmp_cinematic"
TMP_DIR.mkdir(parents=True, exist_ok=True)

OUT_WAV = ROOT / "artifacts" / "music" / "信天翁09进港黑匣子通话录音_2096.wav"
OUT_MP3 = ROOT / "artifacts" / "music" / "信天翁09进港黑匣子通话录音_2096.mp3"
DESKTOP_DIR = pathlib.Path.home() / "Desktop" / "世代飞船_精选正典"

def run_cmd(cmd):
    subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

async def synthesize_voices():
    print("🎙️ 1. 正在调用神经网络合成真人级航行对话 (Azure Neural TTS)...")
    
    # 增加标点停顿与节奏控制 (通过语速与句间微停顿)
    lines = [
        # 管制员 (Xiaoxiao - 冷静、清晰、标准进港指令)
        ("zh-CN-XiaoxiaoNeural", 
         "曙光管制……呼叫信天翁零九。你已越过北极减速走廊，主推进关机。当前轴向距离五百米，请确认切换至中央球核四号泊位。", 
         "+0%", "+0Hz", "line1"),
        
        # 机长 (Yunxi - 带有呼吸感、现场感与专注沉稳的航天员声调)
        ("zh-CN-YunxiNeural", 
         "信天翁零九收到！姿态喷气已接管……轴向相对速度四点七米每秒。重力梯度读数正常，正在通过一百七十二米换挡位，请求进入最后系泊走廊。", 
         "+5%", "-2Hz", "line2"),
        
        # 管制员 (指令紧凑、雷达核准)
        ("zh-CN-XiaoxiaoNeural", 
         "允许进港。球核四号泊位液压卡爪已加电，请保持相对速度低于零点五米每秒，注意微重力平飞姿态。", 
         "+4%", "+0Hz", "line3"),
        
        # 机长 (收尾决断、硬对接就绪)
        ("zh-CN-YunxiNeural", 
         "明白。防撞雷达已锁定四号泊位……硬对接准备就绪！", 
         "+8%", "+0Hz", "line4")
    ]
    
    for voice, text, rate, pitch, tag in lines:
        out_mp3 = TMP_DIR / f"{tag}_raw.mp3"
        communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
        await communicate.save(str(out_mp3))
        print(f"  ✓ {tag} ({voice}) 神经网络语音合成完成")

def build_foley_effects():
    print("🔊 2. 正在物理合成深空现场环境音效 (Foley Effects)...")
    
    # 1) Quindar 开关麦哔音 (2525Hz / 2475Hz)
    run_cmd(f'ffmpeg -y -f lavfi -i "sine=frequency=2525:duration=0.08" -af "volume=0.25" "{TMP_DIR}/quindar_on.wav"')
    run_cmd(f'ffmpeg -y -f lavfi -i "sine=frequency=2475:duration=0.08" -af "volume=0.2" "{TMP_DIR}/quindar_off.wav"')

    # 2) RCS 姿控高压冷气喷气声 (Pneumatic Thruster Blast, 1.2s 带包络)
    run_cmd(f'ffmpeg -y -f lavfi -i "anoisesrc=c=white:r=44100:a=0.4:d=1.2" -af "highpass=f=800,lowpass=f=4000,afade=t=in:ss=0:d=0.1,afade=t=out:st=0.6:d=0.6,volume=0.8" "{TMP_DIR}/rcs_blast.wav"')

    # 3) 液压卡爪硬对接锁定重击声 (Hydraulic Clamp Heavy Clang + Sub Thud)
    run_cmd(f'ffmpeg -y -f lavfi -i "sine=frequency=55:duration=0.8" -f lavfi -i "anoisesrc=c=pink:r=44100:a=0.5:d=0.8" -filter_complex "[0:a]afade=t=out:st=0.1:d=0.7[a0];[1:a]bandpass=f=1200:w=500,afade=t=out:st=0.05:d=0.7[a1];[a0][a1]amix=inputs=2[out]" -map "[out]" "{TMP_DIR}/hydraulic_lock.wav"')

    # 4) 重力梯度切换状态提示音 (Gravity Gradient Status Chime: E5 -> B4)
    run_cmd(f'ffmpeg -y -f lavfi -i "sine=frequency=659:duration=0.25" -f lavfi -i "sine=frequency=493:duration=0.4" -filter_complex "[0:a]afade=t=out:st=0.1:d=0.15[s1];[1:a]adelay=200|200,afade=t=out:st=0.3:d=0.3[s2];[s1][s2]amix=inputs=2,volume=0.35[out]" -map "[out]" "{TMP_DIR}/gradient_chime.wav"')

    # 5) 雷达接近率打卡脉冲 (Radar Proximity Beeps)
    run_cmd(f'ffmpeg -y -f lavfi -i "sine=frequency=1800:duration=0.04" -af "volume=0.15" "{TMP_DIR}/radar_beep.wav"')

    # 6) 500米天井巨构低频自转共振与深空粉红背景 (Centrifugal Deep Hull Hum: 60Hz + 120Hz + Pink Noise)
    run_cmd(f'ffmpeg -y -f lavfi -i "sine=frequency=60:duration=35" -f lavfi -i "sine=frequency=120:duration=35" -f lavfi -i "anoisesrc=c=pink:r=44100:a=0.015:d=35" -filter_complex "[0:a]volume=0.45[h1];[1:a]volume=0.25[h2];[2:a]lowpass=f=2200,volume=0.35[h3];[h1][h2][h3]amix=inputs=3[out]" -map "[out]" "{TMP_DIR}/ambient_hull_hum.wav"')

def process_and_mix():
    print("🎛️ 3. 正在施加航天无线电 DSP 滤镜并执行多轨电影级混音...")
    
    # 对每句真人语音施加【深空航天无线电滤镜】
    # - 300Hz ~ 3400Hz 航空带通
    # - 温暖过载压缩 (compand + soft clipping)
    # - 微弱座舱反射 (aecho)
    radio_filter = (
        "highpass=f=320,lowpass=f=3300,"
        "compand=attacks=0.02:decays=0.1:points=-40/-40|-15/-5|0/-1,"
        "volume=1.8,"
        "aecho=0.8:0.6:12:0.2"
    )
    
    dialogue_segments = []
    for tag in ["line1", "line2", "line3", "line4"]:
        raw_mp3 = TMP_DIR / f"{tag}_raw.mp3"
        radio_wav = TMP_DIR / f"{tag}_radio.wav"
        combined_wav = TMP_DIR / f"{tag}_with_quindar.wav"
        
        # 施加滤镜
        run_cmd(f'ffmpeg -y -i "{raw_mp3}" -af "{radio_filter}" "{radio_wav}"')
        
        # 拼接 Quindar 开关麦音
        run_cmd(f'ffmpeg -y -i "{TMP_DIR}/quindar_on.wav" -i "{radio_wav}" -i "{TMP_DIR}/quindar_off.wav" -filter_complex "[0:a][1:a][2:a]concat=n=3:v=0:a=1[out]" -map "[out]" "{combined_wav}"')
        dialogue_segments.append(combined_wav)

    # 4. 构建时间轴编排 (Timeline Sequencing)
    # 0s: 进港环境音开始
    # 1.5s: 调度员 Line 1 ("曙光管制呼叫信天翁零九...")
    # 9.0s: 机长 Line 2 ("信天翁零九收到...")
    # 11.5s: 伴随 RCS 喷气爆发 + 重力换挡提示音
    # 20.0s: 调度员 Line 3 ("允许进港...")
    # 27.5s: 机长 Line 4 ("明白...硬对接准备就绪！")
    # 32.0s: 液压卡爪锁定金属撞击 (Clang) + 减压泄气
    
    mix_script = (
        f'ffmpeg -y '
        f'-i "{TMP_DIR}/ambient_hull_hum.wav" '            # [0] 背景共鸣
        f'-i "{dialogue_segments[0]}" '                   # [1] Line 1
        f'-i "{dialogue_segments[1]}" '                   # [2] Line 2
        f'-i "{dialogue_segments[2]}" '                   # [3] Line 3
        f'-i "{dialogue_segments[3]}" '                   # [4] Line 4
        f'-i "{TMP_DIR}/rcs_blast.wav" '                  # [5] RCS 喷气
        f'-i "{TMP_DIR}/gradient_chime.wav" '             # [6] 换挡音
        f'-i "{TMP_DIR}/hydraulic_lock.wav" '             # [7] 液压锁定
        f'-filter_complex "'
        f'[1:a]adelay=1500|1500[v1];'
        f'[2:a]adelay=9200|9200[v2];'
        f'[5:a]adelay=11800|11800,volume=0.9[rcs];'
        f'[6:a]adelay=15500|15500[chime];'
        f'[3:a]adelay=20000|20000[v3];'
        f'[4:a]adelay=27500|27500[v4];'
        f'[7:a]adelay=31800|31800,volume=1.4[lock];'
        f'[0:a][v1][v2][rcs][chime][v3][v4][lock]amix=inputs=8:duration=first:dropout_transition=3[out]" '
        f'-map "[out]" -t 35 "{OUT_WAV}"'
    )
    run_cmd(mix_script)
    
    # 转换 MP3
    run_cmd(f'ffmpeg -y -i "{OUT_WAV}" -b:a 192k "{OUT_MP3}"')
    
    # 拷贝到桌面
    DESKTOP_DIR.mkdir(parents=True, exist_ok=True)
    import shutil
    shutil.copy(OUT_WAV, DESKTOP_DIR / "09_信天翁09进港黑匣子通话录音_2096.wav")
    shutil.copy(OUT_MP3, DESKTOP_DIR / "09_信天翁09进港黑匣子通话录音_2096.mp3")

    print("\n" + "="*65)
    print("🎬 电影级深空黑匣子航行录音生成完毕！")
    print("="*65)
    print(f"📁 仓库输出: {OUT_WAV}")
    print(f"📁 桌面输出: {DESKTOP_DIR / '09_信天翁09进港黑匣子通话录音_2096.wav'}")
    print("="*65)

def main():
    asyncio.run(synthesize_voices())
    build_foley_effects()
    process_and_mix()

if __name__ == "__main__":
    main()
