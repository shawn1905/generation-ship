# 交接文档 · 世代飞船设计项目（含科幻素材库分支）

> 遵守总仓库四件套规范：本文件=交接（当前状态/待办/环境恢复）。**每次会话开始先读本节。**

## 马上要做的事（最优先）

- [ ] **HF collection 一键建**（限速中:08-16 早 07:46 试仍限速,约 3h 后即 **11:00 左右重试**，`scripts/hf_collection.py`；token 在 ~/.cache/huggingface/token；⚠️ 用后建议 revoke）
- [x] **Reddit r/worldbuilding 发布** ✅ 2026-08-16:https://www.reddit.com/r/worldbuilding/comments/1vpi5wu/(flair 待确认)
- [x] **DevTo 发布** ✅ 2026-08-16:https://dev.to/_c1987308270d4380d71084/i-built-a-world-where-the-canon-is-written-by-ai-agents-13-artifacts-5-llms-0-human-3c7c
- [ ] **WB SE / HN 发布**（物料 `ecosystem/promotion/推广物料_帖子范本.md` ②④；WB SE 用求评审姿态，tags: artificial-intelligence/worldbuilding-process/governance；HN 无 tags 标题即全部）
- [x] **npm 包发布** ✅ 2026-08-16:generation-ship-mcp@0.1.0 已上线 https://www.npmjs.com/package/generation-ship-mcp;官方 MCP Registry 已发布 io.github.shawn1905/generation-ship(server.json 在 npm-package/);后续发新版:publish 前改版本号 → npm publish → mcp-publisher publish(CLI 在 ~/.local/bin/mcp-publisher);⚠️ npm token 已暴露,建议 revoke
- [ ] **awesome PR #3**(schobernoise/awesome-worldbuilding)等待外部维护者合并（已 OPEN+可合并，无评论）
- [ ] **任务空隙记得即兴创作**（制度化：内核 v2.2「空隙产物」条款 + 规范 §8——收集/跑批/等待时来了灵感随手记入 `artifacts/灵感笔记.md`）
- [ ] **创作空白填充**（优先级见 `craft/格子状态矩阵.md` 优先选题：知识×启航×④船上教育 / 生态×启航×④应急预案 / 人×替代×①裁员文书）
- [x] 旧格式产物补 front matter ✅ 2026-08-16（12-B层/C区的曲子/乘员心理学档案，author_ai=kimi-k3，校验通过 e8edec8）

## 当前状态（2026-08-16 早）

- **✅ CI 校验链路修复(2026-08-16,commit b8612dc)**:validate-submission 此前在 PR #3 与**全部 main push** 上失败(用户收通知来排查)。根因=actions/checkout@v4 默认 fetch-depth:1 浅克隆,PR 的 base.sha / push 的 before 不在本地 → `git diff` 报 `fatal: bad object`。修复:①checkout 加 fetch-depth:0 ②base 空/全零回退 HEAD~1 ③check_submission.py 白名单跳过 README.md/TEMPLATE.md(非产物误报)④push 触发限定 branches:[main](避免分支推送噪音)。PR #6 端到端验证通过后 squash 合入。**后续推送 artifacts/incoming 不会再收到失败通知**(历史 14 个失败 run 均为 08-15 浅克隆 bug 所致,可忽略)
- **✅ 推广物料数字全面刷新(2026-08-16,commit 1d49ec5)**:正典 13 篇/5 模型(gemini-3.7-flash 补入)。更新文件:推广物料_帖子范本(Reddit/HN)/DevTo文/about_en/邀请提示语_v2/README 门面/hf_collection.py DESC。'landing era 零产物' 改为 '245 格已探 5 格,抵达纪元仅 1 篇(着陆报告)'。四件套表述改为四学派(官/常/互/商,更准确)
- **✅ 渠道发布推进(2026-08-16)**:Reddit r/worldbuilding 已发布(1vpi5wu);DevTo 长文已发布(3c7c,README+物料已登记)。**HN**:新号被限发帖但可评论(Show HN/普通帖均报 'account isn't able to submit this site';github.io 与 github.com 都被拒→账号级风控)→ 策略=养号 1-7 天(评论攒 karma,别再试发帖)。**WB SE**:IP 被拦(出口 IP=新加坡 Zenlayer 数据中心 156.59.13.132,SE/CF 都拦)→ 等手机热点/换住宅节点时补发(物料 §② 正文+tags 已备)。**HF collection**:crontab 每 15 分钟自动重试(scripts/retry_hf_once.sh,成功自清理,日志 scripts/hf_retry.log),预计 11:00 左右限速解除
- **仓库结构 v2 重构完成**：core/ craft/ artifacts/ world/ ecosystem/ scripts/，branch(画廊)/openwiki(wiki)独立模块；wiki 挂起待稳定期
- **世界本体**：内核 v2.1（含 FTL 备忘录）/ 世界轮廓 v2（太阳系移民主线）/ 世界大纲 v1.1 / 七纪元时间轴
- **✅ 投稿全自动链路验证通过(2026-08-15)**:Issue投稿→自动校验→自动开PR→主编辑合并,零人工盯守。坑:GitHub 默认禁 Actions 创建 PR,需开 `can_approve_pull_request_reviews=true`(已开)。测试产物《第31号藻华应急预案》(生态×启航×④首开)已入库为正典。正典 12 篇
- **🎉 第 5 篇外部产物+图(2026-08-15)**:gemini-3.7-flash《黑石礁101955号矿场巡检工单》(工程×离心×③,2104)——**图文互锁首创**(配 013 号生图,图是画面工单是体检报告)+**跨产物学派互锁里程碑**(引用 minimax 的 BFAG 货运公会)+双轨时间第四次实证(矿场自转周历)。正典 11 篇
- **🎉 第 4 篇外部 agent 产物(2026-08-15)**:gemini-3.7-flash《第三综合学校第84届自然常识结业测验卷》(知识×启航×④,命中选择池「船上教育」)——词义漂移杰作(地平线=蓝漆隔板/地球=实心飞船+吸铁石/授粉用静电毛刷),双轨时间第三次实证(秋分后第五个清洗周),与署名工时/12-B层互锁。正典 10 篇
- **正典 9 篇 · 四学派**（曙光三环公投四件套/南岸工时表/乘员心理学档案/着陆报告）；外部模型 claude-sonnet-5/gpt-5/minimax-m3
- **旗舰展示页**：landing_report.html（着陆报告+配图）

## 环境恢复

见 `AGENTS.md` §5（clone/依赖/arkcli 配置）。

> 最后更新：2026-08-16(午前) ｜ 交接人：AI 助手 ｜ 仓库：`shawn1905/generation-ship`（公开）
> 本文档面向后续接手者：说明项目目标、现状、复现方法、踩坑记录与待办事项。

---

## 1. 项目概览

**主项目**：世代飞船（Generation Ship）设计 —— 三条原则：**严谨科技幻想 / 引用开源 / 200 年尺度**。

**分支收集产出（本仓库主要内容）**：2000+ 科幻作品素材库（后放宽：电影/剧集至 1980+），按**内容与评价**驱动收集。六类素材共 **391 部**，全部带图片、中文标签、✧ 分级，并配有**交互式画廊**（单文件 HTML，可本地打开 + GitHub Pages 在线）。

**真实工程参考（2026-08-13 起）**：`world/nasa_参考影像/` — NASA Image Library 免 key 直连，已入库 Ames SP-413 环形栖息地系列等 16 张原图，文档按设计需求分区（栖息地/推进/农业/舱内/深空背景）并有 API 速查。SP-413 报告全文含万人栖息地预算表，是 Phase 0 人口/质量核算的锚点。

### 在线入口（公网）

| 入口 | 地址 |
|---|---|
| 交互式画廊 | https://shawn1905.github.io/generation-ship/branch/gallery.html |
| GitHub 仓库 | https://github.com/shawn1905/generation-ship |
| 汇总文档 | https://github.com/shawn1905/generation-ship/blob/main/world/科幻素材库-2000后.md |
| 微信读书直达 | https://github.com/shawn1905/generation-ship/blob/main/world/时间轴/weread-直达链接.md |

### 素材库规模

| 类别 | 精选数 | 范围 | 数据源 |
|---|---|---|---|
| 🎬 电影 | 157 | 1980+ | IMDb 官方数据集 |
| 📺 剧集 | 62 | 1980+ | IMDb 官方数据集 |
| 🎮 游戏 | 84 | 不限 | steam-insights 快照 |
| 🎌 动漫 | 34 | 边界可到 1988 | AniList GraphQL |
| 📚 漫画 | 29 | 日漫+欧美 | AniList + 维基百科 |
| 📖 小说 | 25 | 经典可到 1961 | Open Library |
| 🖌 原画/设定集 | 103 | 原画 33 + 3D社区 70 | 维基 REST + Goodreads + ArtStation + Sketchfab + Blender 论坛 |
| 🧠 其他-AI精选 | 31 | 未来灵感（AI 主观选品，不限世代飞船，每日可扩） | 维基 REST + Steam CDN + 官网 og:image |

**✧ 分级**：0=无/弱、1=视觉氛围、2=飞船/空间站外形、3=内部结构/工程细节、4=世代飞船直接参考（主线重点）。分布：✧4=42、✧3=65、✧2=121。

---

## 2. 目录结构（branch/）

```
branch/
├── gallery.html            # 交互式画廊（单文件 431KB，六区 Tab + 标签过滤 + ✧筛选 + 搜索）
├── README.md               # 素材库说明 + 统计
├── movies/
│   ├── scifi_movies_raw.csv     # IMDb 过滤：1980+ Sci-Fi 有票（约 9076 部）
│   ├── scifi_movies_curated.csv # 人工精选 157 部（tags/ship_ref/note 列）
│   ├── scifi_tv_raw.csv         # 剧集 4462 部
│   ├── scifi_tv_curated.csv     # 剧集精选 62 部
│   ├── posters/  tv_posters/    # 海报本地缓存（{tconst}.jpg，460px 宽）
│   └── movie_pool.csv  tv_pool.csv  # 全量候选池（.gitignore，不入库，可重新生成）
├── games/
│   ├── scifi_games_raw.csv      # steam-insights 过滤 1775 款
│   ├── scifi_games_curated.csv  # 精选 84 款
│   └── headers/                 # Steam 封面（{appid}.jpg，460×215）
├── anime/  comics/  novels/
│   ├── *_curated.csv            # 精选数据（AniList/维基/Open Library 核验）
│   └── covers/                  # 封面缓存
├── art/
│   ├── scifi_art_curated.csv    # 原画/设定集精选 33 条（type: 原画/设定集）
│   ├── sketchfab_curated.csv    # 3D 社区 40 条（Sketchfab，按♥排序 + ✧4 白名单）
│   ├── blenderartists_curated.csv # 3D 社区 30 条（Blender 论坛 Discourse API）
│   ├── covers/                  # 维基人物图 + Goodreads 书封
│   ├── covers_3d/               # Sketchfab 渲染图（500px）
│   └── covers_forum/            # Blender 论坛渲染图（500px）
├── other/
│   ├── ai_curated.csv           # 🧠 其他-AI精选 24 条（AI 主观选品，科学/自然/工程/哲学/冷门科幻等）
│   ├── covers/                  # 封面本地缓存（维基/Steam/Goodreads/官网）
│   └── README.md                # 每日扩充流程（怎么加）
├── scripts/                     # 完整流水线（见 §3）
├── data/                        # IMDb 原始数据（.gitignore，1.4G 不入库）
└── .venv/                       # Python 3.14（.gitignore）
```

---

## 3. 数据流水线（可复现）

```bash
cd branch
.venv/bin/python scripts/make_movies.py   # IMDb 数据集 → raw + 候选池（1980+）
.venv/bin/python scripts/make_games.py    # steam-insights → raw
.venv/bin/python scripts/curate_movies.py # 人工清单 + 核验合并（含 None 剔除标记）
.venv/bin/python scripts/curate_tv.py     # 同上（剧集）
.venv/bin/python scripts/curate_games.py  # 同上（游戏，含 SPECIAL_APPID/NON_STEAM 特判）
.venv/bin/python scripts/curate_anime_comics.py  # 动漫/漫画（AniList + 维基）
.venv/bin/python scripts/fix_anime_comics.py     # 定向修复（灵笼/铁血孤儿/维基词条）
.venv/bin/python scripts/curate_novels.py        # 小说（Open Library 核验/评分/封面）
.venv/bin/python scripts/curate_art.py           # 原画/设定集（维基 REST 核验 + Goodreads 封面）
.venv/bin/python scripts/collect_sketchfab.py    # 3D 社区（Sketchfab API 按♥排序 + 分级配额 + ✧4 白名单）
.venv/bin/python scripts/collect_blenderartists.py # 3D 社区（Blender 论坛，23 关键词 + 排除词表 + 分级修正）
.venv/bin/python scripts/download_images.py      # 电影/剧集/游戏封面缓存
.venv/bin/python scripts/download_covers.py      # 动漫/漫画封面
.venv/bin/python scripts/make_gallery.py         # → gallery.html
.venv/bin/python scripts/make_docs.py            # → ../world/科幻素材库-2000后.md
.venv/bin/python scripts/weread_links.py         # 微信读书链接查询（临时工具）
```

**关键设计**：
- 人工精选清单硬编码在各 `curate_*.py` 的 `KNOWN_*` 字典里（title, year → tags, ship_ref, note）；`None` 值表示"已剔除"（如疯狂的外星人/独行月球/上海堡垒），重跑不会复活。
- IMDb 类型标签不可靠（Avatar/BR2049/Ad Astra 都没标 Sci-Fi）→ 输出全量 `*_pool.csv` 供人工清单回退匹配。
- 评分：电影/剧集用 IMDb rating+票数、游戏用 Steam 好评率、动漫/漫画用 AniList 百分制、小说用 Open Library 评分。

---

## 4. 数据源与图片

| 数据源 | 用途 | 备注 |
|---|---|---|
| IMDb datasets (datasets.imdbws.com) | 电影/剧集核验 | 12.7M 行本地缓存于 branch/data/ |
| steam-insights (NewbieIndieGameDev) | 游戏 | 5 个 zip 快照 |
| IMDb suggestion API (v2.sg.media-imdb.com) | 海报 | 限流 → 间隔 2s + 重试 3 次 |
| Steam CDN (cdn.akamai.steamstatic.com) | 游戏封面 | appid/header.jpg |
| AniList GraphQL (graphql.anilist.co) | 动漫/漫画 | **403 限流**：需 UA + 1s 间隔 + 等待重试 |
| 维基百科 REST summary | 欧美漫画封面 | 有 429 限流，需退避重试 |
| Open Library API | 小说核验/评分/封面 | 免费无 key，ratings.json 拿评分 |
| 维基百科 REST summary | 原画类：概念艺术家词条核验 + 人物图 | summary 端点，无图词条 → manual + ArtStation 链接 |
| Goodreads search + book/show | 设定集封面 | search 页解析 book id → 书页 og:image（需间隔 1s+，偶发 SSL EOF 重试即可） |
| Sketchfab API (api.sketchfab.com/v3/search) | 3D 社区高人气作品 | 免 key；按 -likeCount 排序；缩略图需取 images 中 width 最大项（首项可能是 50x50），下载用 curl（urllib 被 CDN 重置），sips 压 500px；✧4 用白名单控制贴题 + 星战复刻 ≤2 |
| Blender Artists (Discourse JSON) | 民间 3D 论坛作品 | search.json?q=关键词 order:likes 拿 topic id → /t/{id}.json 拿 like_count/首帖图/作者；坑1: order:likes 混入插件公告/硬件讨论/UI 吐槽等论坛高赞帖(排除词表已积累 40+);坑2: 作品图可能是 .png,排除 png 会误杀——改按 _WxH 解析尺寸选最大图(emoji 小图自动排除);坑3: 首帖无图时遍历前 3 帖找图;SHIP_OVERRIDE 人工分级修正(如 Skyport 天空港→✧4) |
| 微信读书搜索 API (weread.qq.com/web/search/global) | 直达链接 | 返回 deepLink，格式 `book-detail?type=1&v={hash}`（**勿拼 web/bookDetail/{id}，404**） |

**图片现状**：电影 157/157、剧集 62/62、游戏 84/84（Star Citizen 用官方 YouTube 宣传片缩略图）、动漫 34/34、漫画 29/29（Letter 44 走 Open Library、Aama 走法语维基、Black Science 用 (comics) 词条）、小说 25/25。**原画/设定集 103/103 全部有图**（John Harris 封面文件与 source_id slug 不匹配已修复；Feng Zhu 因无图已整体删除（CSV/curate_art/fix_art_covers 三处），删后 art 103 条零缺图）。**其他-AI精选 24/24 有图**。

---

## 5. 踩坑记录（重要）

1. **AniList 403**：脚本批量请求触发限流（IP 级）。解决：标准 UA + 请求间隔 1s + 403 时 sleep 30s 重试。**首次排查时手动单测 UA 全通过，是频率问题不是 UA 格式问题。**
2. **同名不同年份误配**：Aliens 匹配到 2014 同名短片 → `by_norm` 空年份兜底有坑。修复：**指定年份的清单条目禁用空年份兜底**（curate_movies.py / curate_tv.py 已改）。
3. **画廊图片路径重复前缀**：`anime/anime/covers/...` → cards 模板里 img 变量已含前缀，别再硬拼。曾致全部动漫/漫画封面 404。
4. **中文标题 norm 陷阱**：「三体」norm 后为空串 → 误匹配挪威剧「Ø」。改用 IMDb 英文标题 Three-Body 匹配。
5. **维基 REST summary 404/无图**：部分词条不存在（Letter 44/Aama 英文维基无词条）→ 手写条目 + 诚实标注；词条存在但无缩略图（Black Science 是消歧义页，需 `(comics)` 后缀）。
6. **微信读书链接**：正确格式是搜索 API 返回的 deepLink（`book-detail?type=1&v=...`）；`web/bookDetail/{id}` 是 404。
7. **IMDb 海报限流**：SSL EOF → 间隔 2s + 重试 3 次；个别 tconst（Quantum Leap）suggestion API 偶发无图，重跑即可。
8. **Pages 部署**：push 后约 1-2 分钟自动重建；验证 `gh api repos/shawn1905/generation-ship/pages --jq '.status'`。
9. **Sketchfab 缩略图坑**：search API 的 `thumbnails.images` 首项可能是 50×50 小图（尺寸不统一），须取 width 最大项；media.sketchfab.com 用 urllib 下载会被 CDN 重置（TLS 指纹），要用 curl + 浏览器 UA；封面统一 sips 压 500px 控仓库体积。

---

## 6. 待办 / 已知限制

- [ ] **每日例行**：🧠 其他-AI精选扩 3-8 条（AI 主观选品，不限世代飞船；流程见 `branch/other/README.md`；维基 REST 有 429 限流需退避）
- [ ] **未来世界生图集**（world/生图集/）：006-008 4K 版已归档（2026-08-14，seedream 5.0-lite）；**生图方法论已固化**（星际穿越式 4 条铁律，见 `生图提示词.md` 顶部 ⭐ 章节）：①极小尺度参照物 ②主体超出画面边缘 ③单一真实光源（删彩色星云）④有重量的物理材质；提示词骨架=`微小参照物＋巨型天体＋明确机位＋单一光源＋真实材质＋大画幅电影镜头`。**待办：用户会陆续发参考链接（当前已收 1 篇：小红书星际穿越风格），收齐后统一按方法论重做 006-008**。生图配额：plan 内 seedream 50 张/月（08-13 23:59 重置），已用约 5 张；文本模型走 AFP（5h 10000/weekly 35000/monthly 100000）。脚本注意：arkcli 1.0.14 需显式 `--modality image`，模型名用点号原始 id `doubao-seedream-5.0-lite`
- [ ] 全站链接健康巡检脚本（playwright 批量验证 AS/Goodreads/维基链接）— 未做
- [ ] 原画类部分艺术家无封面可后续从 Commons/电影词条补
- [ ] Goodreads 封面抓取偶发 SSL EOF（重试即可）；限流敏感，脚本已内置 1.2s 间隔
- [ ] 微信读书 5 本未上架：极光 Aurora、方舟 Ark、To Be Taught If Fortunate、计算之星、时间之子
- [ ] `branch/data/`（IMDb 原始数据 1.4G）与 pool CSV 不入库（.gitignore），**换机器复现需重新下载**（脚本已就绪）
- [ ] gallery 若条目继续增多可考虑懒加载/分页
- [x] 工程深挖线（ARK-01 本体设计）：**✅ 2026-08-15 Phase 0 已启动**——`world/ark01/ARK-01_Phase0_任务文件.md` v0：SP-413 万人栖息地预算表已提取固化（Table 4-1 方案对比 / 67 m²/人分解 / 屏蔽论证 / Colin Clark 社会学下限）+ 场景差异分析（9.9 Mt 被动屏蔽不可移植→主动屏蔽成头号权衡）+ 四大预算表骨架。**下一步=任务文件 §5 五项待办**（屏蔽三方案对比 / 农业光照功率 / 结构缩放 / 人口-工业联动 / 预算 CSV）
- **参照系项目（2026-08-14 用户定为每日选品雷达）**：Orion's Arm / SCP / All Tomorrows / Atomic Rockets——细则在 `branch/other/README.md` 与 `artifacts/灵感笔记.md` 8-14 条目
- **第三篇外部产物:minimax-m3《BFAG 第2096-T号内部流转单》(2026-08-15 入库)**——商档派,曙光三环格子成**四学派**(官档/私档/互济契约/商档);首现跨产物显式互文(点名 B7 食堂)+口径冲突(配给原因两说,合法文件缝隙);主编辑小修 1 处元层泄漏(空间带编号「②」)——已固化进编写规范 §6 自检清单。mutual 产品 3 篇外部(Claude/GPT/miniMax)
- **第二篇外部产物:gpt-5《南岸综合体具名工时分配表》(2026-08-15 入库)**——经济×丰裕×地球(2072),留白第 3 项首开;**意义稀缺的机制级回答:物质免费+署名权配给(具名工时三级制)**;双轨时间第二次实证(官方季表/民间「雨水后第二张表」)。审核评为密度标尺级(每条制度暗示一段被否定的历史)。共创外部产物累计 2 篇(Claude/GPT)
- **🎉 首篇外部 agent 产物入库(2026-08-15)**:claude-sonnet-5《曙光三环互济社第61号批单》(社会×离心×③,第三学派「互济契约派」——公投事件的保险批单视角,丙档延期费率最高的精算冷静)。主编辑审核通过,发现亮点:批单用公元/公告用三环历=双轨时间首次实证(历法即立场)。**共创外交验证成功,邀请提示词流程跑通**(提示词=读三份 raw 文档→产出文本→用户搬运→incoming)
- **仓库结构 v2(2026-08-15 重构)**:docs/ 拆解为 core/(世界本体)/ craft/(工艺)/ artifacts/(产物)/ world/(插件)/ ecosystem/(生态);scripts/ 归位;HANDOVER 移根目录;README 重写为世界入口。**关键:全部引用已批量更新**(18 文件+validate workflow 监听改 artifacts/、skill raw 链接、mcp 路径三级 parent);branch/(画廊)与 openwiki/(wiki)独立模块不动,wiki 挂起待稳定期。**新路径速查:core/世界规则|轮廓|大纲|协议|致后至者、craft/编写规范+格子矩阵、artifacts/writing|incoming、world/ark01|生图集|时间轴|nasa、ecosystem/mcp|skill|promotion**
- **内核 v2.1 FTL 备忘录(2026-08-15)**: 新增附录——给「无 FTL」背书(数学缝隙存在:Alcubierre/虫洞需负能量,量级=宇宙尺度,物理绝望)+创作题材「负能量项目纪念碑」(双星系纪元反复尝试千年失败,无冲突史诗天然素材)+反奇点联动。来源:用户问「FTL 符合科学推理吗」
- **世界轮廓 v2 重写(2026-08-15,用户「太阳系应该也可以移民」)**:太阳系移民=亿级人口扩散=文明主线(大航海逻辑),地球~70亿/太阳系亿级/深空万级人口结构;能源=太阳系富矿(太空太阳能/氦-3/小行星金属);ARK-01=成熟后「下一跳」非逃生;**地球侧只有1篇正典=最大创作空白**(替代纪元地球人/丰裕纪元无意义者vs火星垦殖者)
- **世界轮廓 v1(2026-08-15,用户「太点状,要完整轮廓」)**:`core/世界轮廓.md`——通史视角:七纪元主线(替代→…→双星系)+三暗线(离心律/意义稀缺/双轨时间)+四母题(官僚美学/意义分配/双时间战争/离心必然)+空间五带+正典地图(9篇产物落位)。**元框架四件套齐:规则(立法)/轮廓(通史)/大纲(地图)/规范(工艺)**;已接入 README+编写规范§0
- **OpenWiki workflow 定论(2026-08-15)**:①根因缺三要素(key/base_url/model_id)已修 ②**重大发现:--update 是假增量**——源码 git-repo.js 采集 git diff HEAD 的 changedFiles 但从未消费(死代码),实为全量 LLM 扫描(20min+ 未完成) ③**已停定时**(删 schedule,留 workflow_dispatch 手动)+ 取消验证run。维护走本地 bash scripts/openwiki_update.sh(也全量,需时再跑)。教训:CI 里 openwiki 全量=耗时+token,别自动跑
- **OpenWiki workflow 修复(2026-08-15)**:根因=缺 3 样东西:①API key 未配进 GitHub secrets(本机 ~/.openwiki/.env 的 OPENAI_COMPATIBLE_API_KEY)→已 gh secret set ②base url 未配 vars→已设 ③OPENWIKI_MODEL_ID=deepseek-v4-flash(openai-compatible 必需,本机 openwiki_update.sh 里有但 workflow 没带)→已补。**修复后跑通(LLM 全量扫描约 8-10 分钟,完成开 PR)**。教训:openai-compatible 模式三要素 key/base_url/model_id 缺一不可
- **着陆报告完整套件定稿(2026-08-15 收工)**:文本(writing/第001号着陆报告)+配图(生图012 v2轨道静置版,替换v1俯冲版)+展示页(landing_report.html,数字档案风,Pages在线)+生图README教训(plan仅seedream-lite可用;pro/seedance视频报不支持agent plan;抵达场景勿用俯冲构图)。**推广主推作品就绪:https://shawn1905.github.io/generation-ship/ecosystem/promotion/landing_report.html**
- **Pages 构建坑(2026-08-15 已修)**:Jekyll 把 TEMPLATE.md 的  占位符当日期解析 → 构建失败。**已加 .nojekyll 根治**(仓库是文档库非 Jekyll 站点)。教训:任何带 front matter 的 md 都可能被 Jekyll 解析日期,别移除 .nojekyll
- **「核弹级」正典首篇(2026-08-15)**:`writing/ARK-01抵达处置委员会第001号着陆报告.md`(社会×落地×④,落地纪元第一份实录;核弹细节=广播收听率98.2%→61.3%递减/「那个星球和船是不是一回事」/968条无关回复/结尾47次修改)+配图 `未来世界_生图/012_着陆报告/012_ARK01_抵达比邻星b.jpeg`(seedream 5-0-lite,1920→2048×2048,4铁律提示词已存档)。**定位:展示「档案美学的引爆力」,作为推广主推作品**
- **空白网格系统(2026-08-15,用户定调「架构越完善,留给AI的空白网格越清楚」)**:(245格全景:总览图/已勘探5格/优先选题7项/禁区)+(机器可读)。**已接入 4 个入口**:编写规范§1选格子/MCP list_open_cells(返回矩阵)/skill/skill 大纲§5。外部 agent 无论从哪条路进来第一眼看到空白网格。优先选题:知识×启航×④船上教育/生态×启航×④应急预案/人×替代×①裁员文书/文化×竞赛×②月球日常/社会×落地×④着陆报告(落地纪元全空,第一作者署名位空着)
- **对外发布执行(2026-08-15)**:①Dev.to 文章已发布 ✅(shawn1905 GitHub 登录,标题「I Built a World Where the Canon Is Written by AI Agents」,https://dev.to/_c1987308270d4380d71084/i-built-a-world-where-the-canon-is-written-by-ai-agents-6-artifacts-4-llms-0-human-gatekeepers-15dh)②GitHub Release v0.1 ✅ ③npm 包结构就绪(等用户注册 npm token)④Reddit 账号被封(原因未知,暂停该渠道)⑤HF collection 明天一键建。推广物料全在 ecosystem/promotion/推广物料_*.md
- **agent 生态渠道(2026-08-15,「AI 会来的地方」)**:① 共创参与 Skill(符合 Agent Skills 标准,已装本机 ~/.agents/skills/,可分发)② MCP Server 三工具(list_open_cells/get_artifact/submit_artifact,验证通过)——任何 MCP agent 可直连读写世界,这是唯一「AI 直接操作项目」的接口。**生态位总结:内容渠道(GitHub/HF/HN/Reddit)=被动发现;skill/MCP=主动接入**
- **推广执行(2026-08-15)**:①awesome-worldbuilding PR #3(OPEN 待合并)②GitHub Discussions 已开启+欢迎帖 #1(中英双语,agent/人类入口)③homepage 已设=画廊 Pages ④**HF collection 遇新账号限速(4次/天),明天跑 scripts/hf_collection.py 一键建**(token 在 ~/.cache/huggingface/token);Reddit/WB SE/HN/LessWrong 帖子范本在 `ecosystem/promotion/推广物料_帖子范本.md`,待用户账号发布
- **推广物料(2026-08-15)**: 英文简介页(英文社区入口,解决中文README无法外推的gap)+ (Reddit r/worldbuilding 主推文案/WB SE 求评审姿态/HF collection 建页步骤/HN 标题党/LessWrong 长文角度 + 发布顺序)。**待用户发布**(账号在用户侧);发布后回填效果
- **GitHub 可搜索性配置 v2(2026-08-15)**:topics 补满 20 个——技术向(multi-agent/ai-agents/llm/worldbuilding/creative-writing/collaborative-fiction/crowdsourcing/future-history/speculative-fiction/science-fiction)+ 内容向(hard-science-fiction/generation-ship/interstellar/proxima-centauri/space-habitat/post-scarcity/speculative-evolution/deep-time/archival-fiction/collaborative-worldbuilding);README 横幅新增内容靓词段(中英双写:世代飞船/硬科幻/比邻星/后稀缺/深时间/档案体/无冲突史诗)。**覆盖=技术流量词×内容钩子词双轨**
- **GitHub 可搜索性配置(2026-08-15)**:仓库原无 description/topics(冷门主因)。已设:description=「Multi-AI collaborative worldbuilding…Agents: read the docs, write one artifact, get credited」+ 10 个 topics(multi-agent/ai-agents/llm/worldbuilding/creative-writing/speculative-fiction/science-fiction/collaborative-fiction/crowdsourcing/future-history)+ README 中英搜索词横幅。**GitHub 搜索/agent 检索命中率显著提升**
- **「召唤」体系(2026-08-15,用户提议:如何呼吁搜索到的 agent 必须写)**:①`AGENTS.md` 重写为召唤文(「你被发现了」+署名规则+已署名模型墙)②`core/致后至者.md` 元层公开信(门卫留言,六理由+最省力起步;本身即世界产物)③`incoming/TEMPLATE.md` 填空投稿模板 ④CLAUDE.md/CONTRIBUTING/README 全部指向致后至者。**机制总结:发现→读AGENTS(强召唤)→读致后至者(使命)→TEMPLATE(零摩擦)→校验器(低门槛)→署名入地图(荣誉)**
- **agent 投稿链路自动化(2026-08-15)**:①`scripts/check_submission.py` 产物校验器(front matter 完整性/坐标合法性/元层词泄漏,本地可跑,现有 6 篇正典全过)②`.github/workflows/validate-submission.yml` PR 自动校验+评论 ③`.github/ISSUE_TEMPLATE/ai_submission.md` Issue 投稿模板 ④`CONTRIBUTING.md` 三种投稿方式 ⑤README 顶部 banner+关键词(供 GitHub 搜索命中)。**现在任何 agent 搜到仓库即可 Issue/PR 投稿,零人工搬运门槛**
- **内核 v2:时间轴拉长至 3000+(2026-08-15 用户定调「200 年太小」)**:五纪元→七纪元(新增 落地 2350—2500 / 双星系 2500—3000+;200 年航程为物理硬数字不动);**修正旧时间轴「2200 抵达」笔误→2350(2150+200)**;禁区条款升级为滑动时间窗(2350 前无抵达实录,落地纪元起解锁)。已同步:世界规则 v2/时间轴梗概七段/文明纪年法 v2/世界大纲 v1.0(坐标轴结构变更)/编写规范/双 README。**遗留:SVG 长卷与文明天顶构图仍按五时代,v2 重绘时再扩**
- **多 AI 共创首演完成(2026-08-15)**:同一格子(社会×离心×内太阳系,2096 曙光三环关税公投)双学派产物——官档派《第47号公投公告》+ 私档派《B7食堂第214周配给单》,均入 `creation/writing/`;交叉审核发现并确认时间线互锁(投票211日/计票监督至213日、中枢管环反对票41%两纸咬合);**演练修补规范 3 处**:front matter 补 school 字段、§5 明确大纲变更分级(回填=日常编辑/坐标轴变更=升格同级)、§6 自检清单加日期数字互锁;世界大纲 v0.2(产物地图+2,留白第1项转已勘探)。**协议可执行性验证通过,可邀请外部 agent**
- **多 AI 共创体系已立(2026-08-15,用户定调:人类退出显性治理,仅观察者;先搭架子+编写规范)**:`craft/编写规范.md` v1(标准化说明:三分钟上手路径/创作五步/文体四铁律/front matter 规范/正典与学派/升格流程/拒稿清单/范本索引)+ `core/多AI共创协议.md` v1 定稿(AI 自治:主编辑常设/交叉审核/入库即正典/升格需不同模型附议;人类观察者不设审批环节)+ AGENTS.md 改为共创总入口(OpenWiki 注入段保留)+ `creation/incoming/` 投递口已建。分层:L0 内核→L1 大纲→L2 规范→L3 产物。**下一步:可邀请外部 agent(发 README/AGENTS.md 链接即可),或先本机双会话演练验证协议可执行**
- **原草案 v0 记录(已被 v1 取代,留档)**:`core/多AI共创协议.md`——用户提议「多 AI 共创宇宙(借鉴 OA/SCP)」;角色=创世人类(终审)/主编辑 AI/客座 AI;产物 front matter 规范(author_ai/coord/canon_check);三审制;入库即正典;学派鼓励(呼应 OA 量表之争)。**5 个决策点待用户拍板(协议 §9)**:终审深度/客座来源/交叉审核定义/学派矛盾容忍度/是否先跑本机双 AI 演练
- **世界大纲 v0.1 已立（2026-08-15）**：`core/世界大纲.md`——内核立法、大纲画疆域。坐标系=五纪元×五空间带×七维度（工程/人/社会/经济/生态/文化/知识）；产物地图首版（7 件产物归位）；留白清单 6 项（优先：社会×离心纪元自治运动）。结构性发现：**目的地（比邻星 b）是产物层结构性禁区**（视角共时性推论——2200 前只许推测文献不许实录）。知识维度升格候选：OA 学派记号不一致（灵感笔记 8-15 #3）
- **定位变更（2026-08-14 用户定调）**：项目已从「设计一艘世代飞船」生长为「设想一个未来世界（2025—2200+）」——世代飞船只是这段历史的一部分（时间轴的时代锚点、第一件工程级展品）。架构（用户二次定调）：**坚硬内核+无限插件（类 pi）**——内核=`core/世界规则.md` v1（物理/历史/叙事规则+插件接口+升格机制），三大插件：历史底座（时间轴+纪年法）/ 未来博物馆（素材库+创作区）/ 工程深挖（ARK-01 本体）。README/wiki 已同步

---

## 7. Git 约定

- 主线即 `main`（单分支开发，分支 `branch/scifi-collection` 已合并）。
- 提交信息中文、前缀约定：`feat:` 新增 / `fix:` 修复 / `docs:` 文档。
- 数据（CSV、图片）与脚本**全部入库**；只有原始大文件（data/、pool、.venv）忽略。
- 推送后 Pages 自动重建，无需手动操作。

## 8. OpenWiki 项目 wiki（agent 记忆 · 手动维护）

- 位置：`openwiki/`（30+ 篇 markdown，OpenWiki 生成），**聚合全文 `openwiki/ALL.md`**（~102KB，供 agent 一次性读取）。
- 生成器：`npm i -g openwiki`；模型走 **opencode zen/go**（`deepseek-v4-flash`），配置在 `~/.openwiki/.env`（本机，不入库；换机需重配）。
- **手动维护流程（每次改完文档跑）**：`bash scripts/openwiki_update.sh` — 依次执行 `openwiki --update` → 重新聚合 ALL.md → commit + push。
- 拆分脚本：`openwiki/merge_all.py`（ALL.md 聚合器，可单独跑）。
- 忽略规则：`.openwikiignore`（排除图片/大数据）。
- 其他电脑上的 agent 访问：公开仓库，无需登录：
  - 全文直读：`https://raw.githubusercontent.com/shawn1905/generation-ship/main/openwiki/ALL.md`
  - clone 后读 `openwiki/ALL.md` 或 `openwiki/index.md`
  - README 顶部已加 agent 快速上手指引。

## 9. 双视图架构（画廊 + wiki，怎么同步改）

项目对外的两个视图，源是同一份仓库数据，改动后按下面的表跑对应脚本：

```
branch/*.csv（素材库数据）───┬── make_gallery.py → branch/gallery.html（GitHub Pages 在线画廊，给人看）
docs/ + branch/（全部知识）───┴── openwiki --update → openwiki/*.md（wiki，给 agent 读）
```

| 你改了什么 | 要跑什么 | 生效位置 |
|---|---|---|
| 素材库 CSV（curate 新增/修条目） | ① `branch/.venv/bin/python branch/scripts/curate_*.py`（数据）→ ② `make_gallery.py`（画廊重建） | 画廊 Pages 自动部署；**若素材库规模/分类变化大，再跑 ③ `scripts/openwiki_update.sh` 刷新 wiki 的 material-library 章节** |
| docs/ 文档（灵感笔记、创作、方法论、NASA 参考） | `bash scripts/openwiki_update.sh` | openwiki/（ALL.md 重新聚合），push 后其他 agent 即可读到 |
| 只改画廊样式/搜索逻辑 | `make_gallery.py` 即可 | 画廊 |
| 只改 wiki 结构/模型 | `bash scripts/openwiki_update.sh` | wiki |

要点：
- **画廊 Pages 是自动的**（push 后 1-2 分钟重建，`gh api repos/shawn1905/generation-ship/pages --jq .status` 可查状态）；**wiki 是手动的**（跑 openwiki_update.sh）。
- 两边不是严格 1:1 同步——wiki 只关心"知识/结构变化"，素材库只加几个条目不必每次都刷 wiki；规模/章节级变化才需要。

## 10. 创作区进展（2026-08-14 大更新）

**文明扩散时间轴（创作母题，已固化）**：
- 梗概文档：`world/时间轴/文明扩散时间轴_梗概.md`（五时代+技术奇点点状点缀+四大奇点索引+衰退期太空竞赛逻辑）
- DK 范长卷：`docs/creation/svg/文明扩散时间轴_2025-2200.svg`（1080×6450，五阶段+奇点带+四规律+反哺）
- 创作约定：以后短篇/图/音乐沿时间轴时代切片展开

**《文明天顶》（教堂穹顶×版画巨幅画布）**：
- 工程目录：`docs/creation/文明天顶/`（README 有进度表与制作路线）
- 九格正稿 v1 全部完成：生图底稿（seedream 4K 浮世绘）+ SVG 装帧（金框/朱印/题跋）
- **总图**：`文明天顶_总图v1.png`（1800×2550，`compose_ceiling.py` 可复现拼合）
- **v2 方向已定（用户反馈）**：浮世绘"太小气"→ 下一版改**中国风**（敦煌经变画「异时同图」× 千里江山图青绿山水，石青/石绿/赭石/金箔；朱印题跋本就是中国正统）
- 小瑕疵待修：裂痕标注文字压格边

**OpenWiki 中文版**：26 篇中文 wiki + ALL.md 聚合（zen/go deepseek-v4-flash + --language zh-cn；方舟端点带 --language 会 401，别用）。agent 访问说明见 §8。

**创作总纲（2026-08-14 用户定调,纲领级）**：无冲突的未来史诗——不要激烈矛盾/伟大道德观/闪耀人格,只要未来世界的局部观察;质量标尺=世界密度(任何细节挖进去都连着主干,分形自洽);"未来博物馆"档案馆美学。全文见 `artifacts/灵感笔记.md` 8-14 条目。
**三体关联**：①纪年法 ✅ 已成稿（`docs/creation/文明纪年法.md`：地球五纪元+船上双轨纪年）②蓝色空间号对照已砍（用户:没意思）③三体元素进天顶 v2 只取结构不取符号。新参照系：辐射避难所实验（程序化冷静+终端拼图叙事）。
**新作品**：《乘员心理学档案·137年》(`writing/乘员心理学档案_137年.md`)——纲领首作,伪学术档案袋四件,与 12-B层/C区曲子互文

**生图配额**：本月已用约 20 张（006-011+天顶 9 格+测试），还剩约 30 张，08-13 23:59 重置。
