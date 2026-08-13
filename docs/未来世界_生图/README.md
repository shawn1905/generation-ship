# 🎨 未来世界 · 生图集

> 「我眼中的未来世界」系列 — AI 概念图归档。用 [生图提示词.md](生图提示词.md) 生成。
> 世界观：**活的城市 / 慢的文明 / 共生的 AI / 恒星级尺度**（拒绝赛博朋克式冰冷，保留真实）。

## ⚠️ 生图模型现状（2026-08-13）

- **配额内（agent-plan）唯一生图模型**：`doubao-seedream-5.0-lite`。模型目录里存在更强的 `doubao-seedream-5.0-pro`（编辑可控/更自然），但 agent-plan 配额**不支持**（实测 `+gen` 返回 `does not support the agent plan feature`）；需走 platform 按量付费 + 自建 EP 才能用。
- **配额**：每月 08-13 23:59:59 重置；本月已用完则等重置后跑 `bash gen_my_future.sh`。
- **画质提升点**：lite 支持 **4K**（总像素 16.7M）——旧图全用 2K，这是明显差距；脚本已改 4K + 提示词内嵌负面描述（lite 不支持 negative_prompt 参数）。
- 若想上 5.0-pro（按量付费），需确认余额并 `+deploy` 创建 EP，见 [arkcli-deploy](../../.agents/skills/arkcli-deploy/SKILL.md)。

## 图集索引

| # | 画面 | 文件名 | 生成时间 | 状态 |
|---|---|---|---|---|
| 001 | 🏙 仿生共生城市（树状塔楼） | `001_仿生共生城市_树状塔楼.png` | 2026-08-12 | ✅ 定稿（2K） |
| 002 | 🏙 仿生共生城市（树状塔楼 v2） | `002_仿生共生城市_树状塔楼_v2.png` | 2026-08-12 | ✅ 备选（2K） |
| 003 | 🛸 世代飞船·200年环 | `003_世代飞船_200年环.png` | 2026-08-12 | ✅ 已归档（2K） |
| 005 | 🌌 恒星边缘的文明（戴森云） | `005_恒星边缘的文明_戴森云_v1.png` / `v2.png` | 2026-08-12 | ✅ 两版归档（2K） |

> ~~004 人机共生日常~~ — 用户放弃，系列定格为三画面。
> **4K 重制待跑**：配额重置后 `bash gen_my_future.sh` 出 4K 版（命名 006-008）覆盖对比。

## 在线查看

- 目录浏览：https://github.com/shawn1905/generation-ship/tree/main/docs/未来世界_生图
- 单图直链示例（jsDelivr CDN）：
  `https://cdn.jsdelivr.net/gh/shawn1905/generation-ship@main/docs/未来世界_生图/001_仿生共生城市_树状塔楼.png`

## 提示词

- [生图提示词.md](生图提示词.md) — 4 画面完整中英双语提示词 + Negative + 各家工具用法