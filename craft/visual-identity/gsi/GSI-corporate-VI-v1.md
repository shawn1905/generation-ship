# GSI｜世代工业系统：巨型工业企业视觉规范 v1

**性质**：本文件是《世代飞船》及造物项目共用的**工业集团视觉生产规范**。GSI 的几何、配色、字体、版式和应用规则已获准作为项目默认 VI；它不是正典里已成立的公司，也不是 ARK-01 船徽。`GSI / GENERATION SYSTEMS INDUSTRIES / 世代工业系统` 仍是工作名；日后若确定正典企业名称，须同步替换两个仓库的字标与规范，不可在世界内公报中把本工作名写成既定事实。

**双仓同步**：造物仓库 `generation-ship-foundry/docs/visual/` 保存可编辑母版；`generation-ship/craft/visual-identity/gsi/` 保存同版镜像。新增或修改正式的标志、色值、字体、版式、业务应用规则、AI 提示词模板、风格参考及本规范时，必须在同一轮工作中更新两仓对应文件并核对 SHA-256；仅改一仓不能标记完成。一次性场景产物只有升格为正式参考时才纳入同步。具体步骤见两仓 `AGENTS.md` 和 `GSI-SYNC.md`。

**定位一句话**：一家能从月面矿、标准构件、轨道船厂、生态舱，到舰体维护连续交付数代人的工业巨企。它的 VI 要像一套能印在钢梁、设备、合同和城市入口上的制度，不像单次远航任务徽章。

主视觉：[跨场景风格总览](gsi-atmosphere-board.webp) · [集团 VI 总板](gsi-vi-master-board.svg) · [应用场景板](gsi-vi-applications.svg)；场景原图：[月面巨型工厂](gsi-campus-reference.webp) · [轨道船厂](gsi-orbital-yard-reference.webp)；可用标志：[符号](gsi-mark.svg) · [横向字标](gsi-lockup.svg)；供 AI/程序读取：[规范 JSON](gsi-vi-v1.json)。两张场景图由内置 ImageGen 生成，月面图在本地后期叠加本文件的准确标志；它们是视觉气氛参考，不是设施照片或历史物证。

## 叙事依据与身份边界

锁定上游 `generation-ship@147a63f` 的《世界轮廓》把太阳系工业化、亿级人口扩散和 ARK-01 建造放在一条文明主线上；《千禧编年史》写到企业联合体、月面常驻、轨道制造、L5 船台和深空支持体系。因此这套视觉身份覆盖**陆基—月面—轨道—深空**，并强调跨代可维护。它不替代地联、深空工程总署、远征信托或自治机构的标识，也不暗示这些机构由 GSI 控制。

锁定上游 `craft/视觉规范.md` 要求工业实体、宏大尺度、硬光与历史磨损。本 VI 将这些要求转成企业识别规则：大字号、清楚的资产编号、耐污的高对比标记和可回收的模块化版式。GSI 可以出现在远航船上，但身份首先来自工业生产网络。

## 品牌核心：可追溯的巨构

三个关键词：**制造 / 维护 / 交割**。品牌语气冷静、确定、负责。权力感来自密度和秩序：整齐的物流阵列、巨大的厂房字标、刻在构件上的序列号、能追到来源的装配记录。别用“征服星海”“人类最后希望”一类冒险口号。

**标准署名**：主标志 `GSI`，中文 `世代工业系统`，英文 `GENERATION SYSTEMS INDUSTRIES`；辅助短句 `把文明造得出来` 仅用于提案画面，不是正典口号。具体法定实体名称、商标状态和组织结构均待世界观确认。

## 标志

符号是**开口方框 + 内部承载梁 + 校准点**：方框代表标准构件和厂区，开口代表可接入的产线，承载梁让它在远处读成一枚坚硬的工业字形，右下小方点是批次与验收的视觉记号。它没有飞船、星星、行星环或翅膀，因此能从矿车延展到 ARK 外装甲。

- 方形符号在 24 px、单色印刷和磨损表面都要成立。高对比底色上的反白版只替换深色主形；氧化橙小点可保留或并入单色，不允许发光。
- 标准横向锁定：符号 : 字标高度约 1 : 0.7，间距至少一个主笔画宽；下方可以出现中文全称。小尺寸时只用符号或 `GSI`，不能挤压中文。
- 安全留白：符号四周至少一个主笔画宽；不得放入警示三角、安全色条、气密门状态灯的专用区域。
- 不转成盾徽、舰队臂章、企业家签名或科幻全息图。图形中的开口与小点位置固定；不为每个部门改造主标。

## 色彩系统

| 层级 | 名称 | HEX | 用途 |
| --- | --- | --- | --- |
| 主色 | 炉心石墨 | `#18262C` | 字标、厂房立面、设备底色、正式文件标题 |
| 主色 | 陶瓷灰白 | `#E6E3DA` | 大型护板、文件纸面、反白背景 |
| 品牌识别 | 氧化朱 | `#BD573B` | GSI 校准点、厂房入口、资产牌的一条识别线；整画面一般不超过 8% |
| 中性 | 机械钛 | `#71838A` | 桁架、表格次级信息、结构分层 |
| 中性 | 旧纸灰 | `#B8B4AA` | 归档表面与低优先级背景 |
| 专用功能色 | 警示黄 | `#F1B94E` | **仅**安全/危险提示；不进入主 Logo |
| 专用功能色 | 系统绿 | `#59A58C` | **仅**运行状态；不作为品牌装饰线 |

整张企业广告/界面建议石墨与灰白合计 ≥75%，氧化朱 3–8%。品牌色不能覆盖既有安全、管线或设备状态色。实际热控/防辐射材料颜色由工程设计决定，VI 只规定可拆标识与画面呈现。

## 字体、网格与信息层级

- **字形母版**：视觉稿统一使用 `Sarasa Gothic SC`（更纱黑体 SC）；集团名称与一级标题用 700/800 粗度，正文用 400，英文字母同一字族。环境缺字时依次退到 `Noto Sans CJK SC`、系统无衬线。不同电脑的字体回退会改变字宽，因此**正式 Logo 字标须转曲并锁定轮廓**；当前 SVG 中的文字仍是可编辑预览，不可直接作为印刷母版。
- **版式**：采用 8 单位网格；标题、资产号、责任单位、日期/版本、警示五级。不要用伪技术乱码填充空间。
- **编号示例**：`GSI / ORB / MOD-042 / REV-C` 是**版式样例**，不是本库资产契约或已注册物料号。真实资产仍用各自的正式编号与数据模型。
- **画面**：一个主视角、一条明显的水平或垂直基准线、强对比的明暗面。人物/机械臂/巡检艇是尺度参照；品牌标志在真实表面上，不能漂浮在太空里。

## 品牌架构与应用

主标只用一个。`SURFACE / ORBITAL / HABITAT / DEEP SYSTEMS` 可作视觉稿中的**业务描述条**，不是正典子公司名称；它们共同使用同一个标志、网格和字体。建议落点：

1. **月面采矿基地**：厂房门楣大号反白 `GSI`；矿车侧板一条氧化朱识别线；构件仍保留正式资产号和危险标识。
2. **轨道船厂与物流箱**：标志刻在梁端铭牌和集装箱角柱；大面积外壳不铺满 Logo。龙骨、轨道吊机、工区牌共享相同的版式。
3. **舱段与舰体**：集团标志是小比例制造者铭牌，舰号/法权标识优先；船壳可沿用“双脊留白”造型，但不可把企业标志变成舰体轮廓。
4. **工服与采购文件**：胸前小标识、背部大号工区/岗位码；文件左上主标、右上版次与责任链，序列号最大可读性优先于装饰。

## 后续 AI 使用顺序

1. **先锁主体**：企业 VI、某件设备、厂房、工服、文件、产品铭牌，还是带标识的舰体。不要直接从“酷飞船”开始。
2. **给出资产与时代**：如月面质量投射器、轨道装配吊机、L3 生活舱；年月与责任单位若未确认，就写占位而非造正典事件。
3. **套用主规范**：石墨/灰白主导，氧化朱小面积；方框标志在真实表面；8 单位网格和真实编号区。精确 Logo 用 SVG 后期叠加，生图模型只留位置。
4. **再加入叙事磨损**：竞赛纪元粗粝，启航纪元精密，航中补修明显；**企业身份不随时代重画**，只随维护状态变化。
5. **检查**：把品牌标识从画面中盖住，仍能看出同一企业的比例、用色、编号与版式；缩到 320 px，主标和资产号仍清楚；安全色和状态色不被品牌色混淆。

**通用正向提示词**：

> Original industrial megacorporation visual identity for a multi-century Solar System infrastructure network. One consistent GSI masterbrand spanning lunar mining, orbital shipyards, modular habitats and deep-space maintenance. Bold square open-frame emblem placed on real fabricated surfaces, graphite and ceramic-white dominant palette, restrained oxidized vermilion identification stripe, disciplined 8-unit layout grid, large legible asset serial numbers and revision blocks, heavy modular machinery, traceable manufacturing details, tiny workers or service vehicles for scale, one hard physically sourced light, documentary industrial realism, no fantasy polish. Leave exact logo and text as clean spaces for vector postproduction.

**负向提示词**：`mission patch, spaceship-only brand, luxury concept yacht, superhero tech company, franchise corporate logo, winged W emblem, glowing hologram, cyberpunk neon, unreadable pseudo-text, random hazard stripes, orange covering safety labels, seamless toy plastic, unsupported shell, false engineering certification`。

## 与上一版的关系

`ARK-two-directions-v1.md` 是**舰船题材的画图参考**。本文件才是集团 VI 母规范；后续 AI 的默认入口应改为本文件和 `gsi-vi-v1.json`。前版 A/B 可在具体远航场景里作为涂装气氛参考，但不能代表整个企业，也不能把旧标志当 GSI Logo。
