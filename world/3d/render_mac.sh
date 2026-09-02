#!/usr/bin/env bash
# ==============================================================================
# 世代飞船 (Generation Ship) - macOS (Apple Silicon / Metal) 渲染加速脚本
# ==============================================================================
# 用法:
#   ./world/3d/render_mac.sh [blend_file_path] [samples] [resolution_percentage]
#
# 示例:
#   ./world/3d/render_mac.sh world/3d/gargantua/Gargantua.blend
#   ./world/3d/render_mac.sh world/3d/gargantua/Gargantua.blend 200 100
# ==============================================================================

set -e

# 1. 查找 macOS 下的 Blender 可执行路径
BLENDER_BIN=""
if command -v blender &> /dev/null; then
    BLENDER_BIN="blender"
elif [ -x "/Applications/Blender.app/Contents/MacOS/Blender" ]; then
    BLENDER_BIN="/Applications/Blender.app/Contents/MacOS/Blender"
elif [ -x "$HOME/Applications/Blender.app/Contents/MacOS/Blender" ]; then
    BLENDER_BIN="$HOME/Applications/Blender.app/Contents/MacOS/Blender"
else
    echo "❌ 未找到 Blender！请确保已安装 Blender 并放置在 /Applications 中。"
    echo "下载地址: https://www.blender.org/download/"
    exit 1
fi

BLEND_FILE="${1:-world/3d/gargantua/Gargantua.blend}"
SAMPLES="${2:-100}"
RES_SCALE="${3:-100}"

if [ ! -f "$BLEND_FILE" ]; then
    echo "❌ 找不到工程文件: $BLEND_FILE"
    exit 1
fi

DIR=$(dirname "$BLEND_FILE")
BASENAME=$(basename "$BLEND_FILE" .blend)

echo "=================================================="
echo "🚀 启动 Generation Ship 3D 渲染 (Mac Metal 加速)"
echo "--------------------------------------------------"
echo "📂 工程文件: $BLEND_FILE"
echo "🎯 采样率:   $SAMPLES samples"
echo "📐 分辨率:   ${RES_SCALE}%"
echo "💻 Blender:  $BLENDER_BIN"
echo "=================================================="

# 生成动态 Python 配置脚本（强制开启 Metal GPU 并设置参数）
SETUP_PY=$(mktemp /tmp/blender_metal_setup_XXXXXX.py)
cat <<EOF > "$SETUP_PY"
import bpy

# 开启 Cycles 与 Metal GPU
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
prefs = bpy.context.preferences
cycles_prefs = prefs.addons.get('cycles')

if cycles_prefs:
    cprefs = cycles_prefs.preferences
    cprefs.compute_device_type = 'METAL'
    cprefs.get_devices()
    metal_found = False
    for device in cprefs.devices:
        if device.type == 'METAL':
            device.use = True
            metal_found = True
            print(f"[Mac Metal] 启用 GPU 设备: {device.name}")
    if metal_found:
        scene.cycles.device = 'GPU'
    else:
        print("[Mac Metal] 未检测到 Metal GPU，降级到 CPU")
        scene.cycles.device = 'CPU'

# 设置自定义采样与分辨率百分比
scene.cycles.samples = int("$SAMPLES")
scene.render.resolution_percentage = int("$RES_SCALE")
EOF

# 执行渲染
START_TIME=$(date +%s)
"$BLENDER_BIN" -b "$BLEND_FILE" -P "$SETUP_PY" -o "$DIR/render_mac_" -f 1
END_TIME=$(date +%s)
ELAPSED=$((END_TIME - START_TIME))

rm -f "$SETUP_PY"

echo "=================================================="
echo "✅ 渲染完成！"
echo "⏱️ 渲染总耗时: ${ELAPSED} 秒"
echo "🖼️ 输出产物:   $DIR/render_mac_0001.png"
echo "=================================================="
