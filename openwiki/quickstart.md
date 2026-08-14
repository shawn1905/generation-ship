---
type: 概念
title: 快速入门导航
description: Generation Ship Design 项目的 OpenWiki 文档入口，包含导航概览和变更路由
tags: [navigation, quickstart]
---
# 快速入门：Generation Ship Design Wiki

欢迎访问 **Generation Ship Design** 项目的 OpenWiki 文档，这是一个协作工程计划，旨在设计一艘完整的 200 年星际世代飞船。

## 这是什么项目？

项目已从「设计一艘世代飞船」生长为**设想一个未来世界（2025—2200+）**，架构为**坚硬内核 + 无限插件**：内核 = [世界规则](../../docs/世界规则.md)（物理/历史/叙事规则 + 插件接口，一切内容的裁决依据）；在册插件——① 历史底座（文明扩散时间轴五纪元+文明纪年法）② 未来博物馆（2000+ 条素材库 branch/ + 原创内容区 docs/creation）③ 工程深挖（世代飞船 ARK-01 本体设计，基于严谨物理与开源研究，可在 Blender/FreeCAD 建模渲染）。世代飞船是这段历史的时代锚点与第一件工程级展品。

**关键结论**：前往比邻星 b 的 200 年任务需要采用两级架构的聚变脉冲推进，而最大的工程挑战是 **200 年累积辐射屏蔽** 和 **零补给闭环生命保障**。

## 导航地图

### 核心项目

- [项目概览](./project/overview.md) - 项目介绍、目标和核心原则
- [项目阶段](./project/phases.md) - 四阶段开发计划与各阶段落成状态

### 阶段 0：需求与预算

- [核心任务需求](./design/phase0/requirements.md) - 基本任务约束与需求
- [人口与农业](./design/phase0/population_agriculture.md) - 人口规模与农业面积计算
- [ARK-01 任务文件](./design/phase0/ark01_phase0.md) - Phase 0 总纲（v0，2026-08-15 启动）：SP-413 锚点已固化，质量/功率/人口/农业四大预算表骨架待逐项核算；锚点见 [NASA SP-413 预算表](./docs/nasa_reference.md)

### 阶段 1：概念架构与参数化建模

- [物理与推进](./design/phase1/physics.md) - 物理计算与聚变推进分析
- [任务架构](./design/phase1/mission_architecture.md) - 飞船整体配置与布局
- Blender 参数化建模脚本：**尚未落成**，见[待办事项](#待办事项)

### 阶段 2 与阶段 3（内部结构与渲染）

尚未落成详细设计（屏蔽质量分配、生命保障框图、甲板分区、渲染输出），当前相关证据集中在：

- [ARK-01 任务文件](./design/phase0/ark01_phase0.md) - §2.3 辐射屏蔽论证（SP-413 0.5 rem/yr / 4.5 t/m² 基准、主动屏蔽在飞船上重新成为头号权衡）
- [NASA 真实影像参考](./docs/nasa_reference.md) - SP-413 环形栖息地 / 推进段 / 舱内 / 农业 / 深空背景影像
- [人口与农业](./design/phase0/population_agriculture.md) - 闭环生命保障面积需求
- [任务架构](./design/phase1/mission_architecture.md) - 双环布局与屏蔽构型

### 科幻参考库

- [参考库概览](./reference/library_overview.md) - 精选 494 条科幻参考库的概览（另有其他-AI精选 53 条）
- [类别摘要](./reference/categories.md) - 各媒体类别和重要参考的摘要
- [交互式图库](./reference/gallery.md) - 交互式参考图库的使用指南
- [数据结构](./reference/data_structure.md) - CSV 数据结构说明
- [整理脚本](./reference/scripts.md) - 用于数据整理和图库生成的 Python 脚本

### 项目文档

- [概念讨论笔记](./docs/discussion_notes.md) - 原始概念讨论笔记和未决问题
- [交接与待办](./docs/handover.md) - 项目交接、待办清单和已知问题
- [NASA 真实影像参考](./docs/nasa_reference.md) - NASA Image Library 免 key 素材与 API 速查
- [AI 生图集](./docs/future_world_art.md) - 「我眼中的未来世界」系列概念图与生图方法论
- [原创内容区](./docs/creation_assets.md) - 项目原创创作资产（文字、SVG、音乐；含文明扩散时间轴母题与《文明天顶》工程）
- [灵感来源地图](./docs/inspiration_map.md) - 灵感映射笔记（2026-08-11）

## 变更路由表

| 您想要更改什么？ | 相关页面 | 源入口 |
|------------------------------|----------------|--------------------|
| 任务需求或核心物理 | [需求](./design/phase0/requirements.md), [物理与推进](./design/phase1/physics.md) | `docs/讨论稿-概念与待决问题.md` |
| 质量/电力预算 | [ARK-01 任务文件](./design/phase0/ark01_phase0.md), [项目阶段](./project/phases.md)（阶段 0 交付物） | `docs/ARK-01_Phase0_任务文件.md` §2/§4（SP-413 锚点 + 预算表骨架）、`docs/讨论稿-概念与待决问题.md` §2 |
| 飞船整体架构 | [任务架构](./design/phase1/mission_architecture.md) | `docs/讨论稿-概念与待决问题.md` §2 |
| Blender 参数化建模 | [项目阶段](./project/phases.md)（阶段 1） | 仓库尚无脚本；锚点 `docs/讨论稿-概念与待决问题.md` §4 |
| 辐射屏蔽 / 生命保障 / 居住区 | [ARK-01 任务文件](./design/phase0/ark01_phase0.md), [需求](./design/phase0/requirements.md), [人口与农业](./design/phase0/population_agriculture.md), [NASA 真实影像参考](./docs/nasa_reference.md) | `docs/ARK-01_Phase0_任务文件.md` §2.3/§3（屏蔽论证 + 可移植性）、`docs/讨论稿-概念与待决问题.md` §1-2、`docs/nasa_参考影像/README.md` |
| 参考库整理（CSV 增改） | [参考库概览](./reference/library_overview.md), [类别摘要](./reference/categories.md), [整理脚本](./reference/scripts.md) | `branch/scripts/curate_*.py`（人工清单 KNOWN_*） |
| 画廊样式/搜索逻辑 | [交互式图库](./reference/gallery.md) | `branch/scripts/make_gallery.py` → `branch/gallery.html` |
| 画廊数据重新生成/统计 | [数据结构](./reference/data_structure.md), [整理脚本](./reference/scripts.md) | `branch/.venv/bin/python branch/scripts/make_gallery.py`、`make_docs.py` |
| 每日 AI 精选扩充 | [类别摘要](./reference/categories.md)（其他-AI精选） | `branch/other/README.md`（流程）+ `health_check_other.py` |
| NASA 影像素材补充 | [NASA 真实影像参考](./docs/nasa_reference.md) | `docs/nasa_参考影像/README.md`（API 速查） |
| AI 生图（方法论版） | [AI 生图集](./docs/future_world_art.md) | `docs/未来世界_生图/生图提示词.md`、`docs/gen_future_v2.sh` |
| 原创内容/灵感笔记 | [原创内容区](./docs/creation_assets.md) | `docs/creation/`（灵感笔记.md、writing/、svg/、music/） |
| 灵感来源/参考扩充 | [灵感来源地图](./docs/inspiration_map.md) | `docs/灵感来源地图_20260811.md` |
| OpenWiki 文档维护 | [交接与待办](./docs/handover.md)（§8 维护流程） | `docs/openwiki_update.sh` |

## 待办事项

以下领域已列入计划，但尚未完整记录，因为实现仍在进行中或证据不足：

- **质量/功率/人口/农业预算逐项核算**（阶段 0）——[ARK-01 任务文件](./design/phase0/ark01_phase0.md) v0 已启动（2026-08-15）：框架 + SP-413 锚点数据已固化，四大预算表骨架待逐项核算并落成 CSV（`design/budget_*.csv`）；锚点：`docs/ARK-01_Phase0_任务文件.md` §2/§4、`docs/讨论稿-概念与待决问题.md` §2 参数表、`docs/nasa_参考影像/README.md` SP-413 万人栖息地预算表
- **Blender Python 参数化建模代码**（阶段 1）——仓库尚无 Blender 脚本；锚点：`docs/讨论稿-概念与待决问题.md` §4
- **阶段 2 内部结构详设**（辐射屏蔽质量分配/生命保障框图/甲板分区）——仅定义量级与开放问题；锚点：`docs/讨论稿-概念与待决问题.md` §1-2、`docs/nasa_参考影像/README.md`
- **阶段 3 CAD 模型与最终渲染**——仓库尚无渲染产出；锚点：`docs/讨论稿-概念与待决问题.md` §4
- **全站链接健康巡检脚本**——交接文档列为待办（playwright 批量验证链接），尚未实现（`docs/HANDOVER.md` §6）
- **《文明天顶》v2 中国风版**——v1 九格已定稿，v2 方向已定（敦煌经变画×青绿山水），十格完整版 + 9000×6000 总图未完成；锚点：`docs/creation/文明天顶/README.md`、`docs/creation/文明天顶_构思.md`（详见 [原创创作区](./docs/creation_assets.md)）

## 外部参考

- 原始 README: [/README.md](https://github.com/shawn1905/generation-ship/blob/main/README.md)
- 原始讨论稿: [/docs/讨论稿-概念与待决问题.md](https://github.com/shawn1905/generation-ship/blob/main/docs/讨论稿-概念与待决问题.md)
- 项目交接: [/docs/HANDOVER.md](https://github.com/shawn1905/generation-ship/blob/main/docs/HANDOVER.md)
- 素材库汇总: [/docs/科幻素材库-2000后.md](https://github.com/shawn1905/generation-ship/blob/main/docs/科幻素材库-2000后.md)
