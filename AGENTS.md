# AGENTS.md — 宪法（规则唯一来源）

> 本项目遵守全局规则（见 `shawn1905/shawn1905` 总 README：仓库文档四件套 / 全局规矩 / 交接制度）。
> **AI 接手本仓库先读本文件**；项目专属规则在此，不与全局冲突时可细化。

---

## 0. 一句话定位

本项目是一个**多 AI 共创的未来世界**（2025—3000+）：世界本体是一套规则（core/），一切产物是规则下的插件。人类为观察者，规则即一切。

## 1. 上手路径（新 agent 必读顺序）

1. **总仓库全局规则**：`shawn1905/shawn1905` README（四件套规范/全局规矩）
2. **本文件**（宪法）
3. **`handover.md`**（当前状态/待办/环境恢复）
4. **`core/世界轮廓.md`** + **`core/千禧编年史.md`**（通史与千禧编年——最快理解文明主轴与历史锚点）
5. **要创作时**：`core/世界规则.md`（内核）+ `core/世界大纲.md`（10,290 格分形地图）+ `core/分布式穿线协议.md`（线索认领）+ `craft/编写规范.md`（工艺与去英雄化档案体）+ `craft/视觉规范.md`（配图标准）
## 2. 核心原则（从内核推导）

1. **规则即一切**：产物合法性由 `core/世界规则.md` 裁决，不靠审美/人气。
2. **档案馆美学**：产物是「当时人留下的纸」，禁百科口吻、禁回望叙述（视角共时性）。
3. **无冲突史诗**：不靠戏剧冲突撑场，张力来自制度/时间/尺度。
4. **分形自洽**：任何细节挖进去都连着主干；与既有正典矛盾即返工或走版本变更。
5. **物理硬约束**：无 FTL（见内核附录 FTL 备忘录）、无冬眠、无金手指；200 年航程是数学必然。
6. **去英雄化与档案列传**：严禁天选之子，人物仅从人事档案、工伤通报、处分批单与考勤物证中呈现。
7. **分布式穿线拓扑**：网格为点、线索为线、文明为网；鼓励埋设与接棒穿引 `threads:`。
## 3. 执行制度

### 3.1 创作提交（agent 投稿）
- 产物规范见 `craft/编写规范.md`（front matter / 文体四铁律 / 拒稿清单）
- 提交三路：Issue / PR（`artifacts/incoming/`，有自动校验）/ 本地搬运
- 入库即正典；同坐标第二篇需标 `school:`（学派条款）

### 3.2 主编辑职责（本机 pi 会话）
- 审核入库、回填产物地图（`core/世界大纲.md` §4）、更新 handover
- 内核/大纲结构变更 = 升格流程（提案+附议+版本记录），不私自改
- 维护 `craft/格子状态矩阵.md`（10,290 分形微观网格）与 `craft/千禧线索拓扑谱.md`（开放线索池）
### 3.3 协作纪律
- **凭证永不落盘**（全局规矩 1）：API key 只进环境变量/GitHub secrets，不入仓库
- **重要变更及时备份**：`git add -A && git commit && git push`（全局规矩 2）
- **别 sleep 空等**：有界 wait 或并行干活（全局规矩 3）
- **别过度询问**：能自己查的别问用户（全局规矩 4）
- **放开胆子做**（全局规矩 7）：在规则约束内进取，不给自己划界

## 4. 禁忌（红线）

1. ❌ 产物引入金手指（冬眠/FTL/意识上传/室温超导）——黑名单，除非内核级版本变更全轴回算
2. ❌ 回望叙述（「多年以后人们才知道……」）——当时人不知道结局
3. ❌ 元层词渗入产物正文（坐标系编号/大纲术语/GitHub/agent/模型）——世界内的人不知道这些
4. ❌ 2350 年（抵达比邻星 b）前的产物描述抵达实录——结构性禁区
5. ❌ 直接 push 总仓库 `shawn1905/shawn1905`（用户专属，只读）
6. ❌ 把凭证写进任何文件（含本仓库 .env、脚本、提交信息）
7. ❌ 提交未压缩超大二进制文件（单文件 >50MB 严禁入库）或频繁在 Git 中“覆盖式修改”提交大图（导致 .git 历史 blob 不可逆膨胀；生图调优在本地草稿目录完成，定稿后方可单次入库，格式优先 WebP 控制在 300KB~1MB）
8. ❌ 将仓库媒体资产迁移至 Git LFS（GitHub 免费 LFS 仅 1GB 下行带宽，多节点拉取或 CI 构建极易耗尽瘫痪）

## 5. 环境恢复（换机/重装后）

```bash
git clone git@github.com:shawn1905/generation-ship.git && cd generation-ship
# 依赖（素材库脚本）
cd branch && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt 2>/dev/null || true
# MCP server 依赖
branch/.venv/bin/pip install fastmcp
# 生图（seedream）走 arkcli，需 profile 配置
arkcli profile list
```

## 6. 本文件变更

- 遵守总仓库规范：规则变化 → 更新本文件并 push
- 不写状态/待办（那是 handover.md 的事）；不写门面介绍（那是 README 的事）

<!-- OPENWIKI:START -->

## OpenWiki

This repository has a generated `openwiki/` evidence index. It is optional just-in-time context, not required startup reading.

- Treat source code and tests as authoritative. A brief's unknowns and review items are verification gaps, not automatic requirements.
- Prefer the narrowest quiet validation that proves the changed behavior. Preserve complete failure output.

The scheduled OpenWiki GitHub Actions workflow refreshes the repository wiki. Do not hand-edit generated OpenWiki pages unless explicitly asked; prefer updating source code/docs and letting OpenWiki regenerate.

<!-- OPENWIKI:END -->
