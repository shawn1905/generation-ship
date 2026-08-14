---
type: 计划
title: OpenWiki 维护更新计划（2026-08-14 后）
description: 基于仓库变更证据的文档影响计划：ALL.md/merge_all.py 已恢复、其他-AI精选 39→47、创作区新增文明天顶与文明扩散时间轴
tags: [plan, maintenance, openwiki]
timestamp: 2026-08-14
---

# 文档影响计划（维护更新）

上次成功更新：`gitHead b35fc5366ee66d732194d77c39feb0e71539849e`（2026-08-14T05:37Z，zh-CN）。Shell 受限，无法执行 git；以下变更通过「当前源码/CSV/文档 vs 现有 wiki 页面」逐项比对得出。

## 受影响系统清单与处置

### 1. OpenWiki 维护链路（ALL.md / merge_all.py / openwiki_update.sh）
- 证据：仓库现存 `/openwiki/ALL.md`（85KB 聚合全文）与 `/openwiki/merge_all.py`；`docs/HANDOVER.md` §8 与 §10、`README.md` 顶部均声称 ALL.md 存在；`docs/openwiki_update.sh` 第 2 步运行 `python3 openwiki/merge_all.py`。
- 现状：wiki `docs/handover.md` 的「文档与现状的出入」仍声称「ALL.md 与 merge_all.py 均不存在，update.sh 第 2 步会失败」——已过时。
- 处置：更新 `/openwiki/docs/handover.md`（更正该条 + 补充 OpenWiki 中文版 26 篇/ALL.md 聚合说明）；同步修正 `/openwiki/ALL.md` 中镜像的同一段落及其 front matter（移除 `openwiki_generated` 回退标记）。

### 2. 素材库「其他-AI精选」规模 39 → 47
- 证据：`branch/other/ai_curated.csv` 数据行 47 条（8-11：12 条、8-12 两批 15 条、8-14 第三批 8 条，见 `branch/other/README.md`「已收录（47 条，2026-08-14）」）。
- 影响页：`quickstart.md`（导航条目）、`docs/handover.md`（素材库规模表 + 项目状态行）、`reference/categories.md`（🧠 章节标题 + 已覆盖维度）、`reference/library_overview.md`（统计段）、`reference/gallery.md`（八区 Tab 行），以及 `ALL.md` 中对应镜像段落。
- 处置：全部更新为 47；categories.md 补充 8-14 第三批新维度（塔比星/NaissanceE/Kaiba/与拉玛相会/melodysheep/The Line/猎户座核脉冲/特德·姜）。

### 3. 创作区新增：文明扩散时间轴（母题）+ 文明天顶（工程）
- 证据：`docs/creation/README.md` 新增「创作母题:文明扩散时间轴」段；`docs/creation/文明扩散时间轴_梗概.md`（五时代 + 四大奇点）；`docs/creation/svg/文明扩散时间轴_2025-2200.svg`；`docs/creation/文明天顶/`（README + compose_ceiling.py + 9 格装帧 v1 SVG）；`docs/creation/文明天顶_构思.md`；`docs/creation/svg/文明天顶_构图稿.svg`、`文明天顶_风格小样.svg`；`docs/HANDOVER.md` §10「创作区进展（2026-08-14 大更新）」。
- 现状：wiki `docs/creation_assets.md`（timestamp 2026-08-13）作品索引止于 08-13，完全未覆盖上述内容。
- 处置：扩展 `creation_assets.md`——新增「文明扩散时间轴（创作母题）」与「文明天顶（教堂穹顶×版画）」两节、更新作品索引表、补充 ARK-01 任务文件与三体关联线索；同步更新 ALL.md 镜像段。

### 4. 生图配额细节（HANDOVER §10）
- 证据：`docs/HANDOVER.md` §10「本月已用约 20 张（006-011+天顶 9 格+测试），还剩约 30 张，08-13 23:59 重置」。
- 现状：wiki `docs/handover.md` 生图待办仅记「配额 50 张/月」。
- 处置：在 handover.md 创作/生图待办中补充 HANDOVER §10 的配额用量口径（与 future_world_art.md 的「方法论版 3 张后余约 42 张」口径并存，注明来源差异）。

### 5. 未受影响（证据核实后保持不动）
- 设计/物理/任务架构/需求/人口农业（讨论稿 v0.1 未变）；NASA 影像（16 张未变）；灵感来源地图（2026-08-11 未变）；七类素材规模 494/103（CSV 实测 33+40+30=103，与 wiki 一致；`branch/README.md` 与 `docs/科幻素材库-2000后.md` 的 104/495 为旧值，wiki 已如实标注）。
- 路由关系：quickstart 变更路由表各入口与现源码一致，无需改动。

## 关系建模（概念链接）
- docs/handover.md <-- 维护/生成 --> openwiki 聚合链路（ALL.md、merge_all.py、docs/openwiki_update.sh）——在同一页内说明，不需要新概念页。
- docs/creation_assets.md <-- 母题支撑 --> 文明扩散时间轴；<-- 子工程 --> 文明天顶；<-- 联动 --> future_world_art.md（天顶底稿走生图方法论）、nasa_reference.md（环内景触发「环里的那座湖」）、reference/library_overview.md（收集 vs 自产分工）。全部在同一页展开，无需新建页面。
