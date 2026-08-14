#!/bin/bash
# 我眼中的未来世界 — 一键生图脚本(4K 高清版, 明早 08:00 由 LaunchAgent 自动执行)
# 前提:arkcli 已登录;生图配额 2026-08-13 23:59:59 重置
# 说明:agent-plan 配额内唯一生图模型为 doubao-seedream-5.0-lite;
#       lite 支持 4K(总像素 16.7M),画质显著优于旧版 2K。
cd "$(dirname "$0")"
MODEL=doubao-seedream-5.0-lite
SIZE=4K
OUTDIR="$(cd ../docs/未来世界_生图 && pwd)"
LOG=/tmp/gen_future.log

log() { echo "[$(date '+%H:%M:%S')] $1" | tee -a "$LOG"; }

gen() {
  local name="$1"; local prompt="$2"
  log ">>> 生成: $name ($SIZE)"
  ARKCLI_CALLER_TYPE=ai_agent ARKCLI_CALLER_NAME=pi ARKCLI_SKILL_NAME=arkcli-gen \
  arkcli +gen --model "$MODEL" --modality image --open --size "$SIZE" --save-to "$OUTDIR" --name "$name" "$prompt" 2>&1 | \
    grep -E '"local_path"|"status"|"message"' | tee -a "$LOG"
  sleep 5
}

log "==== 开始 4K 生图(配额重置后) ===="

gen "006_仿生共生城市_树状塔楼_4K" "未来的城市不是被建造的,而是被培育的——巨大的仿生建筑像参天巨树一样从大地生长,外壳覆盖着会发光的苔藓与藤蔓,玻璃穹顶里是垂直森林。无人机像蜂群一样在楼宇间轻柔穿行,维护植物的健康。城市边缘是雾蒙蒙的原始森林,城市与荒野的边界模糊。黄昏时分,建筑表面的生物荧光与夕阳交织,温暖的绿色光点缓缓流动。超写实,电影级光影,宏伟而宁静的尺度感。注意:不要模糊,不要低清晰度,不要塑料感,不要重复图案,不要文字水印"

gen "007_世代飞船_200年环_4K" "深空中一座巨大的环形世代飞船正在缓慢旋转,圆环直径数十公里,环壁表面覆盖着农田的绿色条纹与城市暖光网格,像一颗被精心雕琢的小行星。透过半透明的环壁能看到内部完整的森林、湖泊与旋转的居住区。背景是绚烂的星云与遥远星系,飞船尾部拖曳着聚变引擎的淡蓝色尾焰。冷色调宇宙与飞船内部的暖色生命形成对比,史诗级构图,硬科幻工程美学。注意:不要模糊,不要低清晰度,不要塑料感,不要重复图案,不要文字水印"

gen "008_恒星边缘的文明_戴森云_4K" "一颗即将熄灭的红矮星周围,环绕着人类文明千年的造物——由无数太阳能卫星、居住环与光帆组成的戴森云,像一圈淡金色的薄纱包裹恒星。最近的居住环上,城市灯火如微尘般闪烁。镜头从一颗巨大的布满地标的人造卫星城市拉远,展现整片戴森云的壮阔尺度。极远景构图,恒星光芒被部分遮蔽后形成奇特的光环,硬科幻与宇宙浪漫主义结合,史诗级。注意:不要模糊,不要低清晰度,不要塑料感,不要重复图案,不要文字水印"

log "==== 完成 ===="

# 一次性任务自清理:删除 LaunchAgent
rm -f "$HOME/Library/LaunchAgents/com.generation-ship.gen-future.plist" 2>/dev/null
launchctl remove com.generation-ship.gen-future 2>/dev/null
log "LaunchAgent 已自清理,任务完成。"
