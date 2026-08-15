#!/bin/bash
# 一次性定时重试 HF collection 创建 — 由 crontab 每 15 分钟触发,成功后自动移除 cron 条目
# 用法: crontab 加  */15 8-20 * * * /Users/dahongge/generation-ship/scripts/retry_hf_once.sh
LOG=/Users/dahongge/generation-ship/scripts/hf_retry.log
OUT=$(cd /Users/dahongge/generation-ship && python3 scripts/hf_collection.py 2>&1)
echo "$(date '+%F %T') $OUT" >> "$LOG"
if echo "$OUT" | grep -q "创建失败"; then
  exit 0   # 仍限速,等下一次 cron 触发
else
  crontab -l 2>/dev/null | grep -v "retry_hf_once" | crontab -   # 成功,移除定时任务
fi
