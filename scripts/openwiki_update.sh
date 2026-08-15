#!/bin/bash
# OpenWiki 手动维护脚本 — 改完项目文档后跑一次
# 用法: bash scripts/openwiki_update.sh
# 模型配置: ~/.openwiki/.env (opencode zen/go, deepseek-v4-flash)
set -e
cd "$(dirname "$0")/.."   # 仓库根目录

echo "==> 1/4 openwiki --update (deepseek-v4-flash, opencode zen/go)"
OPENWIKI_TELEMETRY_DISABLED=1 openwiki --modelId deepseek-v4-flash --update --print

echo "==> 2/4 重新聚合 ALL.md"
python3 openwiki/merge_all.py

echo "==> 3/4 git 提交"
git add openwiki/ && git commit -q -m "docs: openwiki 更新 $(date '+%Y-%m-%d')" || echo "(无变更,跳过提交)"

echo "==> 4/4 push"
git push -q && echo "PUSHED"

echo "完成。其他 agent 可直接读: https://raw.githubusercontent.com/shawn1905/generation-ship/main/openwiki/ALL.md"
