# 🎨 未来世界 · 生图集

> 「我眼中的未来世界」系列 — AI 概念图归档。
> 世界观：**活的城市 / 慢的文明 / 共生的 AI / 恒星级尺度**（拒绝赛博朋克式冰冷，保留真实）。
> **作图方法论（强制）**：见 [生图提示词.md](生图提示词.md) ⭐ 章节 — 星际穿越式 4 条铁律 + 镜头语言锚定 + 干净极繁主义（三篇小红书参考消化）。

## 图集索引（方法论版）

| # | 画面 | 文件名 | 生成时间 | 状态 |
|---|---|---|---|---|
| 009 | 🛸 世代飞船·200年环 | `009_世代飞船_200年环_方法论.jpeg` | 2026-08-14 | ✅ 定稿 |
| 010 | 🌌 恒星边缘的文明（戴森云） | `010_戴森云_方法论.jpeg` | 2026-08-14 | ✅ 定稿 |
| 011 | 🏙 仿生共生城市 | `011_仿生共生城市_方法论.jpeg` | 2026-08-14 | ✅ 定稿 |

> 旧版（001-008，2K/4K 无方法论）已清理，git 历史可恢复。

## 生图命令

```bash
bash scripts/gen_future_v2.sh   # 三张方法论版，4K，输出到本目录
```

## 在线查看

- 目录：https://github.com/shawn1905/generation-ship/tree/main/world/生图集
- 单图直链（jsDelivr）：
  `https://cdn.jsdelivr.net/gh/shawn1905/generation-ship@main/world/生图集/009_世代飞船_200年环_方法论.jpeg`

## 012 · 着陆报告（2026-08-15）

- 配图：《ARK-01 抵达比邻星 b》——seedream-5-0-lite，2048×2048，v2「轨道静置」构图（v1 俯冲感已弃）
- 配套正典：`artifacts/writing/ARK-01抵达处置委员会第001号着陆报告.md`（落地纪元首篇实录）
- 展示页：https://shawn1905.github.io/generation-ship/ecosystem/promotion/landing_report.html
- 提示词：`012_着陆报告/prompt_提示词.txt`（v1 弃稿）与 `prompt_v2_轨道静置.txt`（在用）
- 教训：plan 内仅 seedream-lite 可用（pro/视频模型报「不支持 agent plan」）；「抵达」场景勿用俯冲构图，用轨道静置

## 生图配额备忘

- Agent Plan 内 seedream 免费额度 **50 张/月**（08-13 23:59 重置），方法论版 3 张后余约 42 张
- 文本模型走 AFP（与生图互不占用）
