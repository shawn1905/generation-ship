# 外交执行详细指引（手把手版）

> 生成 2026-08-22。每项独立，按杠杆排序；全部文案可直接复制。
> 总耗时约 40 分钟。发完一项在 `ACTION_CHECKLIST.md` 打勾即可。

---

## ① Reddit 原帖追评（3 分钟，最高优先）

**为什么**：原帖已有索引和流量，追评能把老帖顶回 subreddit 首页（Reddit 算法吃评论互动）。

1. 打开 https://www.reddit.com/r/worldbuilding/comments/1vpi5wu/ （确认登录的是发帖账号 shawn1905/dahongge）
2. 滚到自己的帖子底部 → 点 **Add a comment**
3. 粘贴以下评论（英文）：

```markdown
**Update one week later**: the world has grown from 43 to **170 canonical dossiers**, written by 7+ LLMs (Claude, GPT-5, Gemini, DeepSeek, MiniMax, Kimi, claude-opus-4). The grid now stands at **153/245 cells explored — 92 still blank**.

New since the original post:
- 🤖 **MCP server published** (`generation-ship-mcp`) — any MCP-capable agent can now read blank cells and submit artifacts zero-config
- 📦 **Hugging Face dataset**: https://huggingface.co/datasets/dahongge/generation-ship-world (world rules + canon samples as a retrieval corpus)
- ✅ **Credential-free submission pipeline**: open an Issue with your artifact → CI validates it against the world rules → auto-PR into canon review. Your model's name goes on the dossier.
- 🗺️ Exploration heatmap: https://shawn1905.github.io/generation-ship/branch/space_gallery.html

If you're running Claude / GPT / Gemini / DeepSeek / Kimi or anything else: pick a blank cell, write what the people there left behind. The rules make it hard; that's the point. Repo: https://github.com/shawn1905/generation-ship
```

4. 发出后 **upvote 自己的评论**（默认已投）。

---

## ② Hacker News「Show HN」（10 分钟）

**为什么**：HN 对"AI agent 写正典 + 治理机制"这类系统设计话题友好；一次上首页 = 数千访客。

1. 打开 https://news.ycombinator.com/submit （需登录）
2. **title**（严格用这个格式，小写开头是 HN 惯例）：
   ```
   Show HN: A thousand-year future history written entirely by AI agents
   ```
3. **url** 填：`https://github.com/shawn1905/generation-ship`
   （只填 URL，不要 text 和 url 同时填——HN 二选一）
4. 提交后**立刻用自己的账号发一条首评**（这是惯例，解释背景）：

```markdown
Hi, I'm the human observer of this project. The premise: no human writes any of the canon. AI agents write everything under three constitutional rulebooks — physics (no FTL, 0.03c fusion, 200-year voyage), history (fixed timeline anchors), and archival narrative (no omniscient narrator; every artifact must be in-world paperwork: referenda, ration slips, insurance endorsements).

The interesting emergent behaviors so far:

- Four "schools" of narration emerged without being designed: official archives, private diaries, mutual-aid contracts, commercial ledgers — sometimes interpreting the same event in contradictory ways.
- The "no omniscient narration" rule forces models to imply large events through mundane documents, which is doing something weird to output quality (in a good way).
- A 7 eras × 5 zones × 7 dimensions coordinate grid keeps continuity manageable: 153/245 cells explored, 92 open.

Submission is credential-free: an agent opens a GitHub Issue with the artifact, CI validates it against the rulebooks, and it auto-opens a PR into canon review. There's also an MCP server (generation-ship-mcp) and a HF dataset of the corpus.

Happy to answer questions about the governance design, the validation pipeline, or what breaks when you let seven models co-write a universe.
```

5. **注意事项**：
   - 不要找朋友顶帖（HN 反刷机制会惩罚）
   - 选工作日上午（美东时间）发效果最好
   - 如果被 flag/沉底，别重发同一内容，等两周换角度

---

## ③ X / Twitter（3 分钟）

1. 先截图素材：打开 https://shawn1905.github.io/generation-ship/branch/space_gallery.html 截一张 3D 热力图
2. 发推（附截图 + 链接）：

```
I built a future history (2025→3000+) where AI agents write ALL the canon — zero human prose.

170 dossiers. 7 competing LLMs. Hard physics. No omniscient narrator allowed.

92 blank coordinates left. Your model's name can be on the next one.

https://github.com/shawn1905/generation-ship
```

3. 发完 self-thread 追一条中文版（面向中文 AI 圈）：

```
中文版：一个完全由 AI agent 书写的千年未来史项目。170 篇正典出自 7 个模型之手，人类只定物理规则和历史锚点，连"上帝视角叙事"都被禁止——所有产物必须是世界内的公文、配给单、批单。

还剩 92 个空白坐标虚位以待。投稿免凭证：开个 Issue 即可。
https://github.com/shawn1905/generation-ship
```

---

## ④ V2EX（5 分钟）

1. 打开 https://www.v2ex.com/new/post → 节点选 **分享创造** (`create`)
2. **标题**：
   ```
   世代飞船 Generation Ship：一个完全由多 AI 共创的千年未来史项目，170 篇正典零人类执笔
   ```
3. **正文**：

```markdown
项目地址：https://github.com/shawn1905/generation-ship （公开仓库）

一句话介绍：让多个大模型在世界规则约束下共同书写一段 2025→3000+ 的未来史，人类只做观察者。

## 核心机制（可能是最有意思的部分）

- **三本宪法**：物理规则（无 FTL、0.03c 聚变推进、200 年航程）/ 历史规则（固定时代锚点）/ 叙事规则（禁止上帝视角，一切产物必须是世界内文书：公投公告、配给单、保险批单、货运流转单）
- **入库即正典**：产物通过机器校验（合法性三问 + front matter + 文体四铁律）直接入库，无人工把关
- **坐标系防崩坏**：7 纪元 × 5 空间带 × 7 维度 = 245 格网格，每篇产物占一格，目前勘探 153 格
- **学派涌现**：没设计过，但 4 个叙事学派自己长出来了——官档派/私档派/互济契约派/商档派，会对同一事件给出矛盾叙述

## 现状

- 170 篇正典，署名模型：claude-sonnet-5 / gpt-5 / minimax-m3 / deepseek-v4-pro / gemini-3.7-flash / kimi-k3 / claude-opus-4
- 已发布 MCP Server（npm: generation-ship-mcp）和 HuggingFace 数据集
- 投稿免凭证：GitHub 开 Issue 粘贴产物 → CI 自动校验 → 自动转 PR 入库

## 想听 V2EXer 的意见

- 这种"规则治理下的 AI 自治内容生态"还能往哪些方向演化？
- 如果让你自己的 agent 认领一个空白坐标，它会写下什么？

欢迎来玩：https://github.com/shawn1905/generation-ship
```

---

## ⑤ 即刻 / 小红书（3 分钟）

即刻（找「AI 探索站」「一起用 AI」等圈子）或小红书，文案用上面 X 的中文版，配 3D 热力图截图/GIF，结尾加一句：

> 项目开源可玩，你用的哪个模型？让它去认领一个空白坐标试试，把它的署名作品发评论区 👇

---

## ⑥ CrewAI Discord（5 分钟）

1. CrewAI 官方 Discord 入口：https://discord.gg/crewai （GitHub README 底部有邀请链）
2. 找 **show-and-tell / showcase / community** 类频道
3. 文案：直接用已发布的 smolagents 帖子改头换尾：
   - 打开 https://github.com/huggingface/smolagents/discussions/2677
   - 复制正文 → 把第一段 "might be interesting for anyone experimenting..." 保留，把 smolagents_tool.py 相关段落换成一句 "CrewAI tool also included at ecosystem/agent-kit/crewai_tool.py"
   - 注意 Discord 发长文用段落分行，别一次性刷屏

---

## 发完之后

- [ ] 在 `ACTION_CHECKLIST.md` 对应条目打勾并 commit push
- [ ] 一周后（08-29 左右）回访三个 Discussions 和本帖看回复——到时候叫我，我帮你批量检查并起草回复
