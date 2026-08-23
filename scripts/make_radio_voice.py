#!/usr/bin/env python3
"""世代飞船黑匣子语音复原引擎 (Deep Space Radio Telemetry Voice Engine)

使用 macOS 原生多角色 TTS 引擎 + ffmpeg 专业深空无线电 DSP 滤镜链，
为《曙光三环中央垂直中枢第19号降轨进港指令与航行日志》(GS-2096-02)
生成全真深空窄带无线电通信录音（含 Quindar 哔音、带通滤波、电离层杂音与微重力背景嗡鸣）。
"""

import os
import subprocess
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
TMP_DIR = ROOT / "scripts" / "tmp_audio"
TMP_DIR.mkdir(parents=True, exist_ok=True)

OUT_WAV = ROOT / "artifacts" / "music" / "信天翁09进港黑匣子通话录音_2096.wav"
DESKTOP_WAV = pathlib.Path.home() / "Desktop" / "世代飞船_精选正典" / "09_信天翁09进港黑匣子通话录音_2096.wav"

def run_cmd(cmd):
    subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def main():
    print("🎙️ 正在生成深空无线电对话音频 (GS-2096-02)...")

    # 1. 生成 Quindar 开麦音 (2525Hz, 120ms) 与 闭麦音 (2475Hz, 120ms)
    run_cmd(f'ffmpeg -y -f lavfi -i "sine=frequency=2525:duration=0.12" -af "volume=0.3" "{TMP_DIR}/quindar_on.wav"')
    run_cmd(f'ffmpeg -y -f lavfi -i "sine=frequency=2475:duration=0.12" -af "volume=0.25" "{TMP_DIR}/quindar_off.wav"')

    # 2. 生成背景宇宙微波与舱内粉红噪音 (Pink Noise)
    run_cmd(f'ffmpeg -y -f lavfi -i "anoisesrc=c=pink:r=44100:a=0.015:d=25" -af "lowpass=f=2500,volume=0.4" "{TMP_DIR}/noise.wav"')

    # 3. 对话文本与角色分配 (Tingting=管制员, Reed=机长)
    dialogue = [
        ("Tingting", "曙光管制呼叫信天翁零九。你已越过北极减速走廊，主推进已关机。当前轴向距离五百米，请确认切换至中央球核四号泊位进港航线。", "line1"),
        ("Reed", "信天翁零九收到。姿态喷气已接管，轴向相对速度四点七米每秒。重力梯度读数正常，正在通过半径一百七十二米换挡位，请求进入最后系泊走廊。", "line2"),
        ("Tingting", "允许进港。球核四号泊位液压卡爪已加电，请保持相对速度低于零点五米每秒，注意微重力平飞姿态。", "line3"),
        ("Reed", "明白。防撞雷达已锁定四号泊位，硬对接准备就绪。", "line4"),
    ]

    processed_lines = []

    for idx, (voice, text, tag) in enumerate(dialogue):
        raw_aiff = TMP_DIR / f"{tag}_raw.aiff"
        filtered_wav = TMP_DIR / f"{tag}_radio.wav"
        
        # macOS say 合成
        run_cmd(f'say -v "{voice}" "{text}" -o "{raw_aiff}"')
        
        # ffmpeg 施加专业深空窄带无线电 DSP 滤镜：
        # - highpass 350Hz + lowpass 3100Hz (航天窄带对讲机频宽)
        # - acrusher 模拟数字采样失真
        # - aecho 轻微座舱金属反射
        # - compand 压缩动态增加无线电对讲质感
        filter_chain = (
            "highpass=f=350,lowpass=f=3100,"
            "acrusher=bits=10:mode=log:aa=1,"
            "volume=2.2,"
            "aecho=0.8:0.7:15:0.25"
        )
        
        # 拼装：开麦音 -> 语音 -> 闭麦音
        temp_speech_wav = TMP_DIR / f"{tag}_speech.wav"
        run_cmd(f'ffmpeg -y -i "{raw_aiff}" -af "{filter_chain}" "{temp_speech_wav}"')
        
        # 拼接单句无线电片段
        run_cmd(f'ffmpeg -y -i "{TMP_DIR}/quindar_on.wav" -i "{temp_speech_wav}" -i "{TMP_DIR}/quindar_off.wav" -filter_complex "[0:a][1:a][2:a]concat=n=3:v=0:a=1[out]" -map "[out]" "{filtered_wav}"')
        
        processed_lines.append(str(filtered_wav))

    # 4. 串联所有台词并混入背景杂音与静音间隙
    concat_list = TMP_DIR / "concat.txt"
    silence_wav = TMP_DIR / "silence.wav"
    run_cmd(f'ffmpeg -y -f lavfi -i "anullsrc=r=44100:cl=stereo:d=0.8" "{silence_wav}"')

    with open(concat_list, "w", encoding="utf-8") as f:
        for p in processed_lines:
            f.write(f"file '{p}'\n")
            f.write(f"file '{silence_wav}'\n")

    raw_dialogue_wav = TMP_DIR / "dialogue_all.wav"
    run_cmd(f'ffmpeg -y -f concat -safe 0 -i "{concat_list}" -c copy "{raw_dialogue_wav}"')

    # 5. 混音：语音轨 + 背景粉红杂音轨
    run_cmd(f'ffmpeg -y -i "{raw_dialogue_wav}" -i "{TMP_DIR}/noise.wav" -filter_complex "[0:a][1:a]amix=inputs=2:duration=first:dropout_transition=2[out]" -map "[out]" "{OUT_WAV}"')
    
    # 拷贝到桌面
    DESKTOP_WAV.parent.mkdir(parents=True, exist_ok=True)
    import shutil
    shutil.copy(OUT_WAV, DESKTOP_WAV)

    print(f"✅ 深空无线电黑匣子音频生成成功！")
    print(f"📁 仓库路径: {OUT_WAV}")
    print(f"📁 桌面路径: {DESKTOP_WAV}")

if __name__ == "__main__":
    main()
