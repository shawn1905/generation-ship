---
type: 文档
title: 项目交接与待办事项
description: 项目交接信息、已知问题、踩坑记录与当前待办事项清单（同步自 docs/HANDOVER.md）
tags: [documentation, handover, todo, issues]
timestamp: 2026-08-15
openwiki:
  roles: [operations, workflow]
  change_kinds: [maintenance]
  source_paths: [docs/HANDOVER.md]
---

# 项目交接与待办事项

本文档同步自仓库根部的 [`docs/HANDOVER.md`](../../docs/HANDOVER.md)（最后更新 2026-08-12，后续有增量编辑），面向后续接手者：项目目标、现状、复现方法、踩坑记录与待办事项。

## 项目状态

- **主项目**：世代飞船（Generation Ship）设计——三条原则：**严谨科技幻想 / 引用开源 / 200 年尺度**。设计论证见 [概念讨论笔记](./discussion_notes.md)，当前处于阶段 0（需求与预算）：[ARK-01 任务文件](../design/phase0/ark01_phase0.md) v0 已于 2026-08-15 启动，SP-413 万人栖息地预算表锚点数据已固化，质量/功率/人口/农业四大预算表骨架待逐项核算。
- **分支收集产出（本仓库主要内容）**：2000+ 科幻作品素材库（电影/剧集放宽至 1980+），按内容与评价驱动收集，服务于世代飞船设计主线。七类素材共 **494 条**（另「其他-AI精选」53 条为独立第 8 区；见 [素材库概览](../reference/library_overview.md)），全部带图片、中文标签、✧ 分级，配交互式画廊（单文件 HTML，本地 + GitHub Pages 在线）。
- **真实工程参考（2026-08-13 起）**：[NASA 真实影像素材](./nasa_reference.md)——NASA Image Library 免 key 直连，已入库 Ames SP-413 环形栖息地系列等 16 张原图，SP-413 报告全文含万人栖息地预算表，是 Phase 0 人口/质量核算的锚点。

## 在线入口（公开）

| 入口 | URL |
|-------|-----|
| 交互式画廊 | https://shawn1905.github.io/generation-ship/branch/gallery.html |
| GitHub 仓库 | https://github.com/shawn1905/generation-ship |
| 素材库摘要文档 | https://github.com/shawn1905/generation-ship/blob/main/docs/科幻素材库-2000后.md |
| 微信读书直达 | https://github.com/shawn1905/generation-ship/blob/main/docs/weread-直达链接.md |

## 素材库规模（七类合计 494，另有其他-AI精选 53）

| 类别 | 精选数 | 数据源 |
|---|---|---|
| 🎬 电影 | 157 | IMDb 官方数据集 |
| 📺 剧集 | 62 | IMDb 官方数据集 |
| 🎮 游戏 | 84 | steam-insights 快照 |
| 🎌 动漫 | 34 | AniList GraphQL |
| 📚 漫画 | 29 | AniList + 维基百科 |
| 📖 小说 | 25 | Open Library |
| 🖌 原画/设定集 | 103（原画 33 + Sketchfab 40 + Blender 论坛 30） | 维基 REST + Goodreads + Sketchfab + Blender 论坛 |
| 🧠 其他-AI精选 | 53 | 维基 REST + Steam CDN + 官网 og:image |

**✧ 分级**：0=无/弱、1=视觉氛围、2=飞船/空间站外形、3=内部结构/工程细节、4=世代飞船直接参考（主线重点）。分布：✧4=42、✧3=65、✧2=121（据交接文档；条目增删后以 `make_docs.py` 重新生成为准）。

## 数据流水线（可复现）

```bash
cd branch
.venv/bin/python scripts/make_movies.py   # IMDb 数据集 → raw + 候选池
.venv/bin/python scripts/make_games.py    # steam-insights → raw
.venv/bin/python scripts/curate_movies.py # 人工清单 + 核验合并（含 None 剔除标记）
.venv/bin/python scripts/curate_tv.py     # 同上（剧集）
.venv/bin/python scripts/curate_games.py  # 同上（游戏，含 SPECIAL_APPID/NON_STEAM 特判）
.venv/bin/python scripts/curate_anime_comics.py  # 动漫/漫画（AniList + 维基）
.venv/bin/python scripts/fix_anime_comics.py     # 定向修复（灵笼/铁血孤儿/维基词条）
.venv/bin/python scripts/curate_novels.py        # 小说（Open Library 核验/评分/封面）
.venv/bin/python scripts/curate_art.py           # 原画/设定集（维基 REST 核验 + Goodreads 封面）
.venv/bin/python scripts/collect_sketchfab.py    # 3D 社区（Sketchfab API 按♥排序 + 分级配额 + ✧4 白名单）
.venv/bin/python scripts/collect_blenderartists.py # 3D 社区（Blender 论坛，关键词 + 排除词表 + 分级修正）
.venv/bin/python scripts/download_images.py      # 电影/剧集/游戏封面缓存
.venv/bin/python scripts/download_covers.py      # 动漫/漫画封面
.venv/bin/python scripts/make_gallery.py         # → gallery.html
.venv/bin/python scripts/make_docs.py            # → ../docs/科幻素材库-2000后.md
.venv/bin/python scripts/weread_links.py         # 微信读书链接查询（临时工具）
```

详细脚本职责与顺序见 [整理脚本](../reference/scripts.md)，CSV 字段见 [数据结构](../reference/data_structure.md)。

**关键设计**：人工精选清单硬编码在各 `curate_*.py` 的 `KNOWN_*` 字典里（title, year → tags, ship_ref, note）；`None` 值表示「已剔除」，重跑不会复活。IMDb 类型标签不可靠（Avatar/BR2049/Ad Astra 都没标 Sci-Fi）→ 输出全量 `*_pool.csv` 供人工清单回退匹配。

## 踩坑记录（重要）

1. **AniList 403**：批量请求触发 IP 级限流。解决：标准 UA + 间隔 1s + 403 时 sleep 30s 重试。手动单测 UA 全通过，是频率问题不是 UA 格式问题。
2. **同名不同年份误配**：Aliens 匹配到 2014 同名短片 → 指定年份的清单条目禁用空年份兜底。
3. **画廊图片路径重复前缀**：`anime/anime/covers/...` → cards 模板里 img 变量已含前缀，别再硬拼。
4. **中文标题 norm 陷阱**：「三体」norm 后为空串 → 改用 IMDb 英文标题 Three-Body 匹配。
5. **维基 REST summary 404/无图**：部分词条不存在（Letter 44/Aama）→ 手写条目 + 诚实标注；消歧义页需后缀（Black Science 用 `(comics)`）。
6. **微信读书链接**：正确格式是搜索 API 返回的 deepLink（`book-detail?type=1&v=...`）；`web/bookDetail/{id}` 是 404。
7. **IMDb 海报限流**：SSL EOF → 间隔 2s + 重试 3 次。
8. **Sketchfab 缩略图坑**：search API 的 `thumbnails.images` 首项可能是 50×50，须取 width 最大项；media.sketchfab.com 用 urllib 会被 CDN 重置，要用 curl + 浏览器 UA；封面统一 sips 压 500px。
9. **其他-AI 精选 CSV**：note 里不能用英文逗号（会列错位导致画廊死链），用 health_check_other.py 巡检。

## 待办事项

### 主项目：世代飞船

- [ ] **阶段 0（进行中）**：[ARK-01 任务文件](../design/phase0/ark01_phase0.md) v0 已启动（2026-08-15）——SP-413 锚点已固化（Table 4-1 / 67 m²/人 / 屏蔽论证 / Colin Clark 下限）+ 四大预算表骨架；下一步 = 任务文件 §5 五项待办（屏蔽三方案对比 / 农业光照功率 / 结构缩放 / 人口-工业联动 / 预算 CSV）
- [ ] 阶段 1：Blender Python 参数化建模脚本、两段式架构定尺寸、轨道与推进验证
- [ ] 阶段 2（未来）：辐射屏蔽质量分配优化、闭环生命保障系统框图、双居住环甲板分区、剖视图
- [ ] 阶段 3（未来）：材质与光照、Cycles 最终渲染图

### 素材库与周边

- [ ] **每日例行**：🧠 其他-AI 精选扩 3-8 条（流程见 `branch/other/README.md`；维基 REST 有 429 限流需退避）
- [ ] 全站链接健康巡检脚本（playwright 批量验证 AS/Goodreads/维基链接）— 未做
- [ ] 原画类部分艺术家无封面可后续从 Commons/电影词条补
- [ ] 微信读书 5 本未上架：极光 Aurora、方舟 Ark、To Be Taught If Fortunate、计算之星、时间之子
- [ ] `branch/data/`（IMDb 原始数据 1.4G）与 pool CSV 不入库（.gitignore），换机器复现需重新下载
- [ ] gallery 若条目继续增多可考虑懒加载/分页

### 创作与生图

- [ ] 未来世界生图集：方法论已固化（见 [AI 生图集](./future_world_art.md)），009-011 已按方法论定稿；生图配额 seedream 50 张/月（08-13 23:59 重置），据 HANDOVER §10 已用约 20 张（006-011 + 天顶 9 格 + 测试），剩约 30 张——**注意**：HANDOVER.md 中「006-008 4K 已归档、待按方法论重做」的描述已过时，`docs/未来世界_生图/README.md` 显示旧版 001-008 已清理，009-011 为当前定稿。

## 创作区进展（2026-08-14 大更新）

来自 HANDOVER §10，详情见 [原创创作区](./creation_assets.md)：

- **文明扩散时间轴（创作母题，已固化）**——五时代（2025-35 白领的冬天 → 2150+ 星际尺度）+ 技术奇点点状点缀 + 四大奇点索引；梗概文档 `docs/creation/文明扩散时间轴_梗概.md`，DK 范长卷 `docs/creation/svg/文明扩散时间轴_2025-2200.svg`。**创作约定**：以后短篇/图/音乐沿时间轴时代切片展开。
- **《文明天顶》（教堂穹顶×版画巨幅画布）**——九格正稿 v1 全部完成（seedream 4K 浮世绘底稿 + SVG 装帧：金框/朱印/题跋），总图 `文明天顶_总图v1.png` 由 `compose_ceiling.py` 复现拼合；**v2 方向已定**：改中国风（敦煌经变画「异时同图」× 青绿山水），用户反馈浮世绘「太小气」。
- **创作总纲（2026-08-14 用户定调，纲领级）**：无冲突的未来史诗——不写激烈矛盾/伟大道德观/闪耀人格，只做未来世界的局部观察；质量标尺=世界密度（分形自洽）；「未来博物馆」档案馆美学。全文见灵感笔记 8-14 条目。
- **三体关联**：①《文明纪年法》✅ 成稿（地球五纪元+船上双轨纪年）②蓝色空间号对照已砍 ③天顶 v2 只取结构不取符号。新参照系：辐射避难所实验（程序化冷静+终端拼图叙事）。
- **新作品（08-14）**：《乘员心理学档案·137 年》（伪学术档案袋，纲领首作，与 12-B 层/C 区曲子互文）、《文明纪年法》设定文档 v1。

## Git 约定与 OpenWiki 维护

- 主线即 `main`（单分支开发，分支 `branch/scifi-collection` 已合并）；提交信息中文，前缀 `feat:` / `fix:` / `docs:`；数据与脚本全部入库，仅原始大文件（data/、pool、.venv）忽略。
- 推送后 Pages 自动重建（1-2 分钟），验证 `gh api repos/shawn1905/generation-ship/pages --jq '.status'`。
- OpenWiki wiki 由 `bash docs/openwiki_update.sh` 手动维护（openwiki --update → 聚合 → commit + push），模型配置在 `~/.openwiki/.env`。
- **另有定时自动更新**：GitHub Actions `.github/workflows/openwiki-update.yml`（cron 每日 08:00 UTC，可手动 dispatch）运行 `openwiki code --update` 并自动开 PR（分支 `openwiki/update`，提交信息 `docs: update OpenWiki`）；PR 合并后 Pages/wiki 同步生效。手动维护与定时 PR 两条链路并存，避免同时跑造成冲突。
- **OpenWiki 聚合链路已恢复**：`openwiki/ALL.md` 聚合全文（约 85KB，26 篇中文页）与 `openwiki/merge_all.py` 聚合器均已在库；`docs/openwiki_update.sh` 第 2 步（`python3 openwiki/merge_all.py`）可正常执行。注意：ALL.md 由 merge_all.py 从 openwiki/ 各页自动拼接，**不要手改内容**，改完任一 wiki 页后重跑脚本重新聚合（或在本页维护流程中一并提交）。

## 双视图架构（画廊 + wiki 怎么同步改）

项目对外的两个视图，源是同一份仓库数据：

```
branch/*.csv（素材库数据）───┬── make_gallery.py → branch/gallery.html（GitHub Pages 在线画廊，给人看）
docs/ + branch/（全部知识）───┴── openwiki --update → openwiki/*.md（wiki，给 agent 读）
```

| 你改了什么 | 要跑什么 | 生效位置 |
|---|---|---|
| 素材库 CSV（curate 新增/修条目） | ① `curate_*.py`（数据）→ ② `make_gallery.py`（画廊重建） | 画廊 Pages 自动部署；若规模/分类变化大，再跑 ③ `docs/openwiki_update.sh` 刷新 wiki |
| docs/ 文档（灵感笔记、创作、方法论、NASA 参考） | `bash docs/openwiki_update.sh` | openwiki/ 重新聚合 |
| 只改画廊样式/搜索逻辑 | `make_gallery.py` 即可 | 画廊 |
| 只改 wiki 结构/模型 | `bash docs/openwiki_update.sh` | wiki |

要点：画廊 Pages 是自动的；wiki 是手动的（跑 openwiki_update.sh）。两边不是严格 1:1 同步——wiki 只关心「知识/结构变化」。

## 另请参阅

- [概念讨论笔记](./discussion_notes.md) - 原始概念讨论与物理推导
- [项目阶段](../project/phases.md) - 阶段说明与退出标准
- [素材库概览](../reference/library_overview.md) - 素材库文档
- [NASA 真实影像素材](./nasa_reference.md) - 真实工程参考影像
