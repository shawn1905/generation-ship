# Gargantua 黑洞物理模拟渲染 (Interstellar Black Hole)

本资产为复刻《星际穿越》（*Interstellar*）Gargantua 视觉效果的深空极端天体物理渲染工程。

![Gargantua Render](./render_0001.png)

---

## 场景结构与渲染技术

本场景并非简单的静态网格贴图，而是综合运用了多个光学与几何技巧：

1. **引力透镜 (`BH_03_Gravitational_Lens`)**：
   - 使用透明折射球体（Glass BSDF + Refraction），扭曲其后方吸积盘与深空背景的光线传播路径，在视网膜/镜头中形成物理引力透镜效应。
2. **炽热吸积盘 (`BH_02_Acrettion_Disk`)**：
   - 采用体积粒子系统 + 动态发射材质（Emission）+ 明暗遮罩（`Mask_v3.jpg`），呈现旋转气体的明暗与湍流细节。
3. **光子环 / 美丽环 (`BH_04_BeautyRing`)**：
   - 弯曲的光子层环形结构，还原事件视界边缘被强烈引力拉弯的光线轮廓。
4. **视界黑洞本体 (`BH_01_Singularity`)**：
   - 绝对吸收光线的致密中心。
5. **双场景合成 (Compositor)**：
   - 场景分为 `BlackHole`（黑洞本体与透镜层）与 `Universe`（深空星图背景 `DeepSpace_02_by_Krzyzowiec.jpg`）两组 Pass 分别计算，最后在 Blender 合成器（Compositor）中进行辉光与叠加合成。

---

## 硬件规格与渲染基准 (Benchmark)

| 指标 | 记录参数 |
|---|---|
| **CPU** | 11th Gen Intel(R) Core(TM) i7-1160G7 @ 1.20GHz (8 vCPUs) |
| **GPU / 核显** | Intel Corporation Tiger Lake-UP4 GT2 [Iris Xe Graphics] (rev 01) |
| **操作系统** | Linux 7.1.9-arch1-2 (x86_64) |
| **Blender 版本** | Blender 5.2.0 LTS (build 2026-08-08) |
| **渲染引擎** | Cycles Engine (CPU + GPU compute fallback) |
| **分辨率** | 1920 × 1080 (100% Scale) |
| **采样率** | 100 Samples per scene |
| **实测耗时** | **2 分 32 秒 11** (包含 Compositor 后期保存) |
| **产物文件** | `render_0001.png` (约 6.0 MB) |

---

## 本地复现命令

在装有 Blender 的终端执行：

```bash
# 后台无头渲染（Cycles 引擎，渲染第 1 帧）
blender -b Gargantua.blend -E CYCLES -o //render_ -f 1
```

输出图片将保存在当前工程同级目录下 `render_0001.png`。
