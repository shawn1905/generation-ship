---
type: 概念
title: NASA 真实影像素材
description: NASA Image Library 免 key 直连的 16 张真实工程参考原图（SP-413 环形栖息地/NERVA/猎户座/深空），按设计需求分区
tags: [reference, nasa, imagery, phase0, phase2]
timestamp: 2026-08-15
openwiki:
  roles: [integration, reference]
  change_kinds: [research]
  source_paths: [docs/nasa_参考影像/README.md]
---

# NASA 真实影像素材（世代飞船设计参考）

2026-08-13 互联网探索成果，源文档为 [`docs/nasa_参考影像/README.md`](../../docs/nasa_参考影像/README.md)。来源：NASA Image and Video Library（官方、免 key、大部分公有领域，遵循 NASA 媒体使用指南，署名 NASA 即可）。`docs/nasa_参考影像/images/` 已下载 **16 张核心参考原图**（43MB），文件名即 NASA ID。

## API 速查（零门槛）

```
搜索:  https://images-api.nasa.gov/search?q={关键词}&media_type=image
详情:  https://images-api.nasa.gov/asset/{nasa_id}      → 列出全部分辨率变体
直链:  https://images-assets.nasa.gov/image/{id}/{id}~{orig|large|medium|small|thumb}.jpg
网页:  https://images.nasa.gov/details/{nasa_id}
```

注意：部分老扫描件只有 orig/small 没有 large；orig 可达 30MB，入库优先 large。

## 影像分区（按设计需求）

### 一、环形栖息地 ★ 最贴主线（✧4 级参考）

**1975 年 NASA Ames + Stanford 夏季研究（NASA SP-413《Space Settlements: A Design Study》）**，艺术家 Don Davis / Rick Guidice——人类历史上最认真的旋转栖息地工程概念设计，直接对应双环栖息地布局（Phase 2）。已入库：`ARC-1975-AC75-2621`（环内景）、`ARC-1975-AC75-1920`（L-5 环内景）、`ARC-1976-AC76-1267`（环形轮全景）、`ARC-1975-AC75-1086`（环内生活区）、`ARC-1975-AC75-1886`（建造/组装）、`ARC-1976-AC76-0525`（多殖民地外观）、`ARC-1975-AC75-1924`（Bernal 球）、`ARC-1976-AC76-1089`、`AC76-0628`（球内剖面——重力沿赤道最强示意）。

### 二、推进系统（聚变脉冲的现实锚点）

已入库：`9902054` / `9902053`（**NERVA 核热火箭** 1963 概念图）、`9906395` / `9906382`（**猎户座计划 Project Orion** 核脉冲推进——与 Daedalus 聚变脉冲同谱系）、`ACS3_SolarPanels_001`（**ACS3 先进复合太阳帆**，2024 在轨，末端磁帆/光帆辅助制动的现实参照）。

### 三、闭环生命支持 / 空间农业（200 年零补给）

已入库：`KSC-20190613-PH_KLS01_0084` 等 APH 系列（**Advanced Plant Habitat 萝卜采收**）。检索词：`Advanced Plant Habitat`、`Veggie plant`、`plant growth chamber`。

### 四、真实在轨内部（内部结构建模材质/管线参考）

已入库：`iss017e015059`（ISS 星辰号服务舱内景，管线/设备密度参考）。在线未入库：TransHab 充气居住舱、NextSTEP 深空居住舱、Gateway 月球空间站构型图。

### 五、深空背景（渲染环境贴图/氛围）

已入库：`carina_nebula`（**JWST 船底座星云「宇宙悬崖」**，巡航段舷窗背景）、`GSFC_20171208_Archive_e000214`（**哈勃拍半人马座 α A/B**，目的地恒星真实照片——比邻星所在三星系统）。

## 使用建议

1. **Phase 2 内部结构**：环形栖息地系列直接对照甲板分区与双环布局——SP-413 报告全文（[PDF](https://ntrs.nasa.gov/citations/19770014162)，NTRS ID **19770014162**；⚠️ 旧记 19770076862 已 404）含人口 10000 人的质量/面积预算表，正好用于 [人口与农业核算](../design/phase0/population_agriculture.md)（Phase 0）。Table 4-1 方案对比 / 67 m²/人分解 / 屏蔽论证 / Colin Clark 下限等锚点数据已于 2026-08-15 提取固化入 [ARK-01 任务文件](../design/phase0/ark01_phase0.md) §2。
2. **材质质感**：环内景画作的「白色骨架 + 绿色农田 + 蓝天窗」是经典范式，但 200 年船可刻意偏离（更暗、更工业），ISS 实景照提供真实管线密度基准。
3. **推进段外形**：Orion 的盘形脉冲单元 + 减震机构是聚变脉冲级最可信的外形参考。
4. 检索入口长期有效，需要更多同系列图直接用上方 API 关键词续查。

## 版权

NASA 影像默认公有领域（非商用限制少），使用时署名 "Image credit: NASA"；Ames 概念画署名 "NASA Ames Research Center / Don Davis / Rick Guidice"。JWST/哈勃图注意 STScI 署名。

## 另见

- [项目交接与待办](./handover.md) - NASA 影像在项目中的定位与待办
- [人口与农业计算](../design/phase0/population_agriculture.md) - SP-413 预算表锚定的 Phase 0 核算
- [任务架构](../design/phase1/mission_architecture.md) - 双环栖息地布局对应影像
- [物理与推进](../design/phase1/physics.md) - 推进影像的现实锚点
hase0/population_agriculture.md) - SP-413 预算表锚定的 Phase 0 核算
- [任务架构](../design/phase1/mission_architecture.md) - 双环栖息地布局对应影像
- [物理与推进](../design/phase1/physics.md) - 推进影像的现实锚点
