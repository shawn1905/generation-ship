---
type: 概念
title: 任务架构
description: 总体任务与飞船架构配置
tags: [design, phase1, architecture, configuration]
---
# 任务架构

## 飞船总体配置

飞船采用 Daedalus 风格的“列车”布局：

```
[Forward Payload Module] → [Central Double Counter-Rotating Habitat Rings] → [Water/Propellant Tanks (Radiation Shielding)] → [Rear: Two-Stage Fusion Propulsion + Radiators + Magnetic Sail]
```

### 各部分职责

1. **前部载荷模块**
   - 包含用于目的行星的登陆艇和前哨模块
   - 最前端设有前向惠普尔屏蔽层，用于抵御星际尘埃

2. **中央居住区**
   - 两个反向旋转的居住环提供人工重力（1g），并抵消总角动量
   - 容纳生活区、农业区、生命保障系统、工业与维护设施
   - 水/推进剂储罐环绕居住区，提供被动辐射屏蔽

3. **后部推进段**
   - 第一级（加速）聚变推进系统（加速后抛弃）
   - 第二级（减速）聚变推进系统
   - 用于排出废热的大型散热器
   - 折叠式磁帆，在减速阶段展开

## 总体质量分布

- **最大质量部件**：辐射屏蔽（主动磁屏蔽 + 被动水/推进剂储罐）
- **第二大**：居住区与生命保障系统
- **第三大**：推进系统与推进剂
- **最小**：有效载荷与登陆艇

## 关键设计特性

### 双反向旋转居住环

- 通过离心力提供 1g 人工重力
- 反向旋转可抵消整艘飞船的净角动量，简化姿态控制
- 半径 250–500 m 时转速约为 1.2–1.9 rpm，符合 NASA 关于可接受科里奥利效应的指南（≤ 2 rpm）

### 被动辐射屏蔽

- 环绕居住区的水与推进剂储罐具有双重用途：
  1. 储存推进剂和生命保障用水
  2. 针对银河宇宙射线提供有效辐射屏蔽
- 与主动超导偶极屏蔽相结合，提供额外保护

### 两级推进

- 加速后抛弃第一级可显著降低巡航质量
- 整个任务只需携带所需的减速推进系统和推进剂
- 提高整体质量效率

## Mermaid 图：总体架构

```mermaid
flowchart LR
    W[Whipple Dust Shield] --> F[Forward Payload: Lander + Outpost]
    F --> H1[Habitat Ring 1: Living + Agriculture]
    H1 --> H2[Habitat Ring 2: Counter-Rotating]
    H2 --> S[Shielding Tanks: Water + Propellant]
    S --> P1[Stage 1: Acceleration Fusion Engine]
    P1 --> P2[Stage 2: Deceleration Fusion Engine]
    P2 --> R[Radiators: Waste Heat Rejection]
    R --> M[Magnetic Sail: Folded for Cruise]
```

## 另请参阅

- [物理与推进](./physics.md)
- [NASA 真实影像参考](../../docs/nasa_reference.md) - 环形栖息地（SP-413）与推进段外形参考
- [需求](../phase0/requirements.md)