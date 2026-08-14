# 世代飞船设计 Generation Ship Design

> **🤖 Agent 快速上手（其他机器上的 agent 也适用）**：
> 1. 读 [`openwiki/ALL.md`](openwiki/ALL.md)（30+ 篇聚合全文，一次读完即可掌握项目全貌）
> 2. 或按入口导航 [`openwiki/index.md`](openwiki/index.md) 逐页阅读
> 3. 素材库清单见 [`branch/README.md`](branch/README.md)；创作区见 [`docs/creation/`](docs/creation/)
> 4. 项目交接/待办/踩坑：**[`docs/HANDOVER.md`](docs/HANDOVER.md)**（人类与 agent 的共同记忆）

一艘按「航行 200 年、抵达新行星」规模设计的世代飞船——目标是最终输出**内外部完整结构**，可直接在 3D 软件（Blender / FreeCAD）中建模渲染。

## 三条原则

1. **严谨的科技幻想** — 每个数字来自物理推导或可查证研究，不做科幻/玄幻/金手指
2. **参考开源项目** — 尽量引用 GitHub 已有开源项目与公开研究，不随意编造
3. **200 年尺度** — 按航行 200 年到达新星球的规模设计

## 核心判断

「200 年」不是众多方案之一，而是被时间常数逼出来的唯一解：

```
200 年 + 到达新行星
  → 目标 ≈ 比邻星 b（4.24 ly），巡航 ~0.03c（9000 km/s）
  → 化学 / 核热 / 核电推进均不可能（Isp 不够）
  → 唯一解：聚变脉冲推进（Daedalus / Longshot 谱系，Isp ~10⁶ s）
  → 两级构型：加速级 + 减速级，末端磁帆辅助制动
```

真正残酷的难题是 **200 年累计辐射剂量** 与 **200 年零补给的闭环生命支持**——这两项是全船最大不确定项。

## 文档

- [docs/讨论稿-概念与待决问题.md](docs/讨论稿-概念与待决问题.md) — 概念论证、物理推导、开源参考清单、待讨论决策点

## 规划（四阶段）

1. **Phase 0** 需求与预算：质量预算、功率预算、人口与农业核算
2. **Phase 1** 概念架构 + 参数化外壳（Blender Python 脚本）
3. **Phase 2** 内部结构：甲板分区、双环栖息地布局、剖视图
4. **Phase 3** 渲染：材质、光照、Cycles 出图

## 主要参考

- Project Longshot（Arrow-air/project-longshot）
- Project Daedalus 原始报告（BIS 1978）
- nasa/GMAT、nasa/trick、OpenMDAO/OpenMDAO
- OpenSpace/OpenSpace、Starshot-Lightsail/FlexSailSim
- O'Neill《The High Frontier》、Stanford Torus、BIOS-3 / MELiSSA
- Atomic Rockets（硬科幻工程参数百科）

详细清单见 [讨论稿](docs/讨论稿-概念与待决问题.md)。
