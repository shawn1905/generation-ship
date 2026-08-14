# 其他-AI 精选（每日扩充）

> 规则：**每天找 3-8 条非常有特点的未来灵感**，不局限于世代飞船。AI 主观选品——"未来什么样没人知道，也许 AI 知道"。

## 添加流程

1. **选品**：在 `ai_curated.csv` 追加一行（9 列，注意 note 里**不要用英文逗号**，用全角「，」）：
   ```
   title,type,artist,year,tags,ship_ref,note,url,source_id
   ```
   - `type`: 动漫/游戏/电影/建筑/小说/原画/科学/音乐/其他
   - `ship_ref`: 一律 0（本分类不用 ✧ 等级）
   - `source_id`: 封面文件名 slug（英文小写+下划线）
2. **封面**：把图片存为 `covers/{source_id}.jpg`
   - 快捷方式：编辑 `../scripts/fetch_other_covers.py` 的 `PLAN` 字典（支持 wiki/url/goodreads/web 四种源）→ 运行
3. **生成**：`python3 ../scripts/make_gallery.py`
4. **健康巡检（必跑）**：`python3 ../scripts/health_check_other.py` — 检查列错位/死链/缺封面，有异常先修再推
5. **推送**：`git add -A && git commit -m "feat: AI精选 +N 条" && git push`
6. **同步 wiki（快捷路径，默认走这个）**：手动改计数 + 重新聚合 + 推送：
   - 计数共 6 处「XX 条」：`openwiki/reference/categories.md`、`openwiki/docs/handover.md`（3 处）、`openwiki/quickstart.md`、`openwiki/reference/gallery.md`、`openwiki/reference/library_overview.md`
   - 然后 `python3 openwiki/merge_all.py` → `git add openwiki/ && git commit && git push`
   - ⚠️ 不要默认跑 `bash docs/openwiki_update.sh`（openwiki --update 是 LLM 全量扫描，10 分钟+ 易超时）；只有需要全量语义同步（新页面/结构变化）时才跑它

> ⚠️ 2026-08-12 踩坑：note 混入英文逗号会导致 CSV 列错位，画廊里表现为「死链+无图」。health_check 能一次全查出来。

## 选品方向（当前偏好，可随时打破）

### 总原则：越来越深入

- **深度优先于小众**——不必刻意追求冷僻，但每次扩充要比上次**钻进更深一层**：从「知道有这么个东西」到「这个东西里最值得看的那个部分」
- 进阶示例：戴森球（表层）→ 卡达舍夫等级（框架）→ 特定恒星的戴森候选异常（深处）；赛博朋克（表层）→ Citizen Sleeper 的打工人生存（具体）→ 某个具体设计师的概念稿（深处）
- 维度要拉开，不重复已有条目

### 参照系项目（每日选品前先看一眼，长期矿脉）

- **Orion's Arm**（orionsarm.com）——硬科幻协作世界观 25 年：规则委员会+百科条目制，挖它的 EG 条目找「规则下长出来的内容」范式
- **SCP 基金会**（scpwiki.com）——档案馆美学祖师爷：挖高分条目学「程序化冷静」的文体控制
- **All Tomorrows**（C.M. Kosemen）——无冲突史诗完成体：学「博物馆解说词」叙事姿态
- **Atomic Rockets**（projectrho.com）——内核即服务：挖具体技术论证（Δv/辐射/热管理）反哺工程深挖线

### 社区深挖雷达（按次轮有效渠道）

- **itch.io**：实验性独立游戏（免费/低成本，社区解谜文化）
- **Steam 独立标签**：一人开发 / 双人团队 / 小团队精品（Indie / Experimental / Atmospheric）
- **独立动画**：一人手绘、短片节入围、Vimeo Staff Picks
- **被低估剧集/作品**：口碑爆但受众少的
- **学术界/工程界提案**：NASA 概念赛、大学研究、建筑师 dream project
- **概念艺术家个人站**：ArtStation/个人 portfolio 深处的设定稿

### 已覆盖维度（供查重）

巨构/尺度失控、城市形态、人的未来（意识/义体/克隆）、生态闭环与生存、外星接触与非人类视角、科学前沿（引力波/韦布/CRISPR/卡达舍夫/费米）、自然生态启发（深海热泉/菌丝网络）、AI 自身（Her/Ex Machina）、音乐/空间氛围、文明备份、**独立/小众深挖**（itch 实验/一人开发/独立动画/被低估剧集）

## 已收录(53 条,2026-08-15)

- 8-11：12 条（巨构/城市/人的未来/生存闭环/外星接触）
- 8-12 第一批：+7 条（猛犸复活 / Ocean Spiral / LIGO / Brian Eno / Ex Machina / 韦布望远镜 / 末日种子库）
- 8-12 第二批·社区深挖：+8 条（itch.io 独立实验、一人开发 ×2、双人团队、小团队 ×2、一人手绘动画、被低估小众剧集）
- 8-14 第三批·更深一层:+8 条(塔比星戴森候选异常 / NaissanceE 巨构步行模拟 / Kaiba 记忆商品化 / 与拉玛相会 / melodysheep 未来延时 / The Line 线性城市 / 猎户座核脉冲推进 / 特德·姜《呼吸》)
- 8-15 第四批·更深一层:+6 条(O'Neill 圆柱栖息地原案 / 万年钟深时间 / All Tomorrows 纲领参照系入库 / 野生建造赞美诗 solarpunk 首开 / Aurora 世代飞船失败学 / Grabby Aliens 费米深一层)

见 `ai_curated.csv`。封面全部本地缓存于 `covers/`。
