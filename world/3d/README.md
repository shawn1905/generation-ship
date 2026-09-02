# 3D 渲染与物理建模资产库 (3D Visual & CAD Gallery)

本目录为「世代飞船 Generation Ship」的三维数字资产专区，专门归档：
- **宏观天体与深空极端环境物理渲染**（黑洞引力透镜、吸积盘、中子星、戴森云等）
- **世代飞船本体与人造结构 CAD / Blender 建模**（ARK-01 环状栖息地、激光推进阵列、深空信标等）
- **Mac (Apple Silicon) 专用硬件渲染工作流与基准测试（Benchmark）**

---

## 资产目录索引

| 资产名称 | 类型 | 核心技术 / 材质 | 硬件基准 (Benchmark) | 归档位置 |
|---|---|---|---|---|
| **Gargantua 黑洞物理模拟** | 极端天体物理渲染 | Cycles 双场景合成 / 折射引力透镜 / 体积粒子吸积盘 / 光子环 (Beauty Ring) | • Linux (i7-1160G7): 152s<br>• Mac M2 (Metal): 预估 ~25~35s | [`gargantua/`](./gargantua/) |

---

## 🖥️ 多端协同架构：Mac (Apple Silicon) 专属渲染工作流

为了解决本地工作站（轻薄本/Linux Agent）在物理光追和高细分 CAD 场景下算力有限的问题，本项目建立了 **「Agent 建模 + Mac 高速渲染」** 的协同机制：

```text
┌───────────────────────────────┐        Git Push        ┌───────────────────────────────┐
│     Linux / AI Agent 端       │ ─────────────────────> │      Mac 端 (Apple Silicon)    │
│  • Python/CAD 参数化建模      │   .blend 工程与脚本    │  • M2/M3 Metal GPU 硬件加速   │
│  • 场景编排与材质节点搭建     │                        │  • 100~500 采样 / 4K 超清出图 │
│  • 低采样快速验证 (32 samples)│ <───────────────────── │  • 关键帧动画批量渲染         │
└───────────────────────────────┘       Git Commit       └───────────────────────────────┘
                                      高清成品图入库
```

### 1. Mac 端环境要求
- **macOS**：macOS 12.3+ (推荐 macOS 14+)
- **芯片**：Apple Silicon (M1 / M2 / M3 系列芯片)
- **Blender**：Blender 3.1+ (已原生支持 Metal API，推荐 4.x / 5.x)
  - 推荐安装路径：`/Applications/Blender.app`

### 2. Mac 端一键渲染执行

克隆仓库后，在 Mac 终端直接执行专属渲染脚本：

```bash
# 进入仓库根目录
cd generation-ship

# 1. 一键渲染 Gargantua 黑洞（自动检测并启用 Metal GPU 加速）
./world/3d/render_mac.sh world/3d/gargantua/Gargantua.blend

# 2. 自定义参数渲染（例如：200 采样，100% 分辨率）
./world/3d/render_mac.sh world/3d/gargantua/Gargantua.blend 200 100
```

### 3. 在 Mac Blender GUI 中查看/调整
1. 双击打开任意资产目录下的 `.blend` 文件（如 `world/3d/gargantua/Gargantua.blend`）；
2. 首次使用请检查系统偏好设置：`Cmd + ,` → **System** → **Cycles Render Devices** 勾选 **Metal** 并勾选你的 **Apple M2 (GPU)**；
3. 视图着色方式切换到 **Rendered (渲染预览)**，即可体验接近实时的引力透镜与吸积盘粒子渲染。

---

## 📦 资产归档规范

新加入 3D 资产时，请确保包含三件套：
1. **工程源文件**：`.blend` 文件（包含材质贴图 Pack 内嵌），放在独立资产子目录下；
2. **渲染成品图**：`render_0001.png` 或 `render_mac_0001.png`（高清无损）；
3. **`README.md`**：记录物理设定、材质节点关键技巧、硬件配置与实测 Benchmark 耗时。
