#!/usr/bin/env python3
"""make_cctv.py — 监控画面（CCTV）档案配图后处理流水线。

用途：为档案体文书生成"监控画面 + 读图员批注"复合档案图。
形态：未来深空工业数字监控画面（非老式 CRT）+ 分析师红笔批注层，
     仿美国解密档案——机器画面与人工读图痕迹同帧共存。

设计原则（与正典互锁）：
1. 画面清晰度优先：不做重采样糊化、无 CRT 扫描线（未来监控是数字传感器），
   噪点控制在传感器合理水平，主体可读。
2. 标识锚定实体：目标圈注只落在检测到的真实实体上（边缘密度+亮度前景），
   检测不到不画框。批注（红圈/箭头/文字）与画面色调融合，非矢量白线。
3. 刻度/读数有物理依据：画面分划、中央准星+测距、底部比例尺、缩放标注。
4. 读图员批注层：仿 FBI 解档——红笔圈注、箭头、编号注释框、解档红章、
   批注引用世界内文号（如"深空工验〔2035〕第1118号"），标注由调用方提供，
   与文书数据逐一互锁。

用法：
    make_cctv.py <底图> <输出图> --cam <机位号> --time "<YYYY-MM-DD HH:MM:SS>" \
        --mode visible|thermal|ir|nv --loc "<位置>" \
        --annot "<编号>|<文字>" [--annot ...] \
        [--field-m <视场宽米>] [--zoom <倍率>] [--no-rec] [--seal <印章文字>]

依赖：python3 + PIL + numpy
"""
import argparse, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONT = "/System/Library/Fonts/SFNSMono.ttf"
FALLBACK_FONTS = [
    "/System/Library/Fonts/Courier.ttc",
    "/System/Library/Fonts/Menlo.ttc",
]

def _font(px):
    for f in [FONT] + FALLBACK_FONTS:
        if os.path.exists(f):
            try:
                return ImageFont.truetype(f, px)
            except Exception:
                continue
    return ImageFont.load_default()

# ---------- 波长映射（数字多光谱传感器，非 CRT 伪彩） ----------

def apply_wavelength(img, mode, hot_zones=None):
    a = np.asarray(img).astype(np.float32)
    if mode == "thermal":
        # 真实热像仪物理：热分布沿物体形状走（喷嘴/金属结构热，真空/岩石冷）。
        # 热区(zone)内做梯度检测，只加热结构显著像素 → 热区贴合形状，非矩形块。
        gray = a.mean(axis=2)
        h, w = gray.shape
        temp = np.clip(gray / 255.0, 0, 1) * 0.20 + 0.05   # 低温基底 0.05-0.25
        if hot_zones:
            heat_field = np.zeros((h, w), dtype=np.float32)
            for (zx1, zy1, zx2, zy2) in hot_zones:
                x1, y1 = int(zx1 * w), int(zy1 * h)
                x2, y2 = int(zx2 * w), int(zy2 * h)
                x1, y1 = max(x1, 2), max(y1, 2)
                x2, y2 = min(x2, w - 2), min(y2, h - 2)
                sub = gray[y1:y2, x1:x2]
                # 结构掩码：梯度显著 = 实体表面（喷嘴环/桁架/管线）
                gx = np.abs(np.diff(sub, axis=1, append=sub[:, -1:]))
                gy = np.abs(np.diff(sub, axis=0, append=sub[-1:, :]))
                grad = np.sqrt(gx ** 2 + gy ** 2)
                grad = (grad - grad.min()) / (grad.max() - grad.min() + 1e-9)
                shape = grad > 0.30
                shape = _dilate(shape, np.ones((7, 7)))   # 实体表面膨胀闭合
                # 形状内按亮度渐变温度：喷口亮=更热，暗结构=次热
                base_heat = 0.62 + 0.38 * np.clip(sub / 255.0, 0, 1)
                sh = shape.astype(np.float32)
                heat_field[y1:y2, x1:x2] = np.maximum(
                    heat_field[y1:y2, x1:x2], sh * base_heat)
            # 柔化热场边缘
            heat_field = _blur_mask(heat_field, k=6)
            temp = np.maximum(temp, heat_field)
        t = np.clip(temp, 0, 1)
        r = np.clip(np.interp(t, [0.0, 0.25, 0.5, 0.75, 1.0], [0, 0, 0.6, 1.0, 0.9]), 0, 1)
        g = np.clip(np.interp(t, [0.0, 0.25, 0.5, 0.75, 1.0], [0, 0.55, 1.0, 0.55, 0]), 0, 1)
        b = np.clip(np.interp(t, [0.0, 0.25, 0.5, 0.75, 1.0], [0.95, 1.0, 0.4, 0, 0]), 0, 1)
        return Image.fromarray((np.stack([r, g, b], 2) * 255).astype(np.uint8))
    if mode == "ir":
        gray = a.mean(axis=2)
        out = np.stack([gray * 0.70, gray * 0.82, gray * 1.08], 2)
        return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))
    if mode == "nv":
        gray = a.mean(axis=2)
        out = np.stack([gray * 0.22, gray * 0.95, gray * 0.42], 2)
        return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))
    return img

def _blur_mask(zz, k=15):
    """盒式模糊热区掩码（柔化边缘）"""
    from PIL import Image as _I
    m = _I.fromarray((zz * 255).astype(np.uint8))
    m = m.filter(ImageFilter.GaussianBlur(k))
    return np.asarray(m).astype(np.float32) / 255.0

# ---------- 目标检测（锚定真实实体） ----------

def detect_targets(img, mode, min_area_frac=0.012, max_area_frac=0.75):
    """返回 [(x1,y1,x2,y2,score), ...]，只在有实体的地方给框。
    thermal/nv/ir: 亮度显著区 = 主体/热源；visible: 边缘密度连通域。
    检测在 1/4 降采样图上做（连通域瓶颈），坐标映射回原图。
    """
    a = np.asarray(img.convert("RGB")).astype(np.float32)
    gray = a.mean(axis=2)
    h, w = gray.shape
    scale = 4
    gh = gray[::scale, ::scale]  # 降采样
    hh, ww = gh.shape

    if mode in ("thermal", "nv", "ir"):
        mask = gh > gh.mean() + 0.7 * gh.std()
    else:
        gx = np.abs(np.diff(gh, axis=1, append=gh[:, -1:]))
        gy = np.abs(np.diff(gh, axis=0, append=gh[-1:, :]))
        grad = np.sqrt(gx ** 2 + gy ** 2)
        grad = (grad - grad.min()) / (grad.max() - grad.min() + 1e-9)
        block = 24
        bh, bw = hh // block, ww // block
        dens = np.zeros((bh, bw), dtype=np.float32)
        for i in range(bh):
            for j in range(bw):
                dens[i, j] = grad[i*block:(i+1)*block, j*block:(j+1)*block].mean()
        dens = np.clip(dens / (dens.max() + 1e-9), 0, 1)
        mask = dens > 0.32
        k = np.ones((3, 3))
        mask = _dilate(mask, k)
        mask = np.kron(mask, np.ones((block, block)))[:hh, :ww]

    labeled, n = _label(mask)
    boxes = []
    min_area_px = (w * h * min_area_frac) / (scale * scale)
    max_area_px = (w * h * max_area_frac) / (scale * scale)
    for k in range(1, n + 1):
        ys, xs = np.where(labeled == k)
        if len(ys) < 20:
            continue
        x1, y1, x2, y2 = int(xs.min()) * scale, int(ys.min()) * scale, (int(xs.max()) + 1) * scale, (int(ys.max()) + 1) * scale
        area = (x2 - x1) * (y2 - y1)
        if area < w * h * min_area_frac or area > w * h * max_area_frac:
            continue
        region = gray[y1:y2+1, x1:x2+1]
        bg = gray.mean()
        score = float(np.clip((region.mean() - bg) / (bg + 1e-9), 0, 2))
        boxes.append((x1, y1, x2, y2, round(score, 3)))
    return boxes

def _dilate(m, k):
    from numpy.lib.stride_tricks import sliding_window_view
    pad = k.shape[0] // 2
    mp = np.pad(m, pad)
    win = sliding_window_view(mp, k.shape)
    return win.max(axis=(-2, -1))

def _label(mask):
    h, w = mask.shape
    lab = np.zeros((h, w), dtype=np.int32)
    nxt = 1
    equiv = {}
    for y in range(h):
        for x in range(w):
            if not mask[y, x]:
                continue
            up = lab[y-1, x] if y > 0 else 0
            left = lab[y, x-1] if x > 0 else 0
            if up == 0 and left == 0:
                lab[y, x] = nxt; nxt += 1
            elif up == 0:
                lab[y, x] = left
            elif left == 0:
                lab[y, x] = up
            elif up == left:
                lab[y, x] = up
            else:
                lab[y, x] = min(up, left)
                equiv[max(up, left)] = min(up, left)
    def find(a):
        while a in equiv:
            a = equiv[a]
        return a
    for y in range(h):
        for x in range(w):
            if lab[y, x]:
                lab[y, x] = find(lab[y, x])
    uniq = {v: i + 1 for i, v in enumerate(sorted(set(lab[lab > 0].tolist())))}
    for y in range(h):
        for x in range(w):
            if lab[y, x]:
                lab[y, x] = uniq[lab[y, x]]
    return lab, len(uniq)

# ---------- 数字监控刻度（克制、融合） ----------

def draw_rulers(d, W, H, field_m, zoom):
    f_s = _font(12)
    dim = (200, 205, 210)   # 与画面融合的灰，非高亮白
    # 1/3 分划（细线，低对比）
    for i in range(1, 3):
        x = W * i // 3
        d.line([(x, 0), (x, H)], fill=(dim[0], dim[1], dim[2], 60), width=1)
        d.line([(0, H * i // 3), (W, H * i // 3)], fill=(dim[0], dim[1], dim[2], 60), width=1)
    # 中央准星（细十字+刻度齿，半透明感）
    cx, cy = W // 2, H // 2
    for (x1, y1, x2, y2) in [(cx-36, cy, cx-10, cy), (cx+10, cy, cx+36, cy),
                             (cx, cy-36, cx, cy-10), (cx, cy+10, cx, cy+36)]:
        d.line([(x1, y1), (x2, y2)], fill=dim, width=1)
    d.ellipse([cx-2, cy-2, cx+2, cy+2], outline=dim)
    d.text((cx+8, cy+6), f"+{field_m*0.25:.1f}m", font=_font(11), fill=dim)
    # 底部比例尺
    bar_w = int(W * 0.16)
    yb = H - 13
    d.line([(18, yb), (18+bar_w, yb)], fill=dim, width=2)
    d.line([(18, yb-5), (18, yb+5)], fill=dim, width=2)
    d.line([(18+bar_w, yb-5), (18+bar_w, yb+5)], fill=dim, width=2)
    m_per_px = field_m / W
    bar_m = max(int(bar_w * m_per_px / 10) * 10, 5)
    d.text((22, yb-20), f"{bar_m}m", font=f_s, fill=dim)
    d.text((W-150, H-24), f"ZOOM x{zoom}", font=f_s, fill=dim)

# ---------- FBI 解档批注层（红笔手写 + 涂黑 + 豁免码 + 高亮） ----------

FBI_FONT = "/System/Library/Fonts/MarkerFelt.ttc"
FBI_FONT2 = "/System/Library/Fonts/Noteworthy.ttc"

def _fbi_font(px):
    for f in [FBI_FONT, FBI_FONT2, FONT]:
        if os.path.exists(f):
            try:
                return ImageFont.truetype(f, px)
            except Exception:
                continue
    return _font(px)

def _wobbly_ellipse(d, cx, cy, r, color, width=2, wobble=3):
    """手绘风椭圆（FBI 红笔圈，带抖动）"""
    import random
    random.seed(int(cx) + int(cy) + int(r))
    n = 32
    pts = []
    for i in range(n):
        ang = 2 * np.pi * i / n
        rr = r + random.uniform(-wobble, wobble)
        pts.append((cx + rr * np.cos(ang), cy + rr * np.sin(ang) * 0.85))
    pts.append(pts[0])
    d.line(pts, fill=color, width=width, joint="curve")

def _wobbly_line(d, p1, p2, color, width=2, seg=6, wobble=2.5):
    """手绘风箭头线（FBI 红笔引线）"""
    import random
    random.seed(int(p1[0]) + int(p1[1]) + int(p2[0]) + int(p2[1]))
    x1, y1 = p1
    x2, y2 = p2
    dx, dy = x2 - x1, y2 - y1
    dist = max(np.hypot(dx, dy), 1)
    nseg = max(int(dist / seg), 3)
    pts = []
    for i in range(nseg + 1):
        t = i / nseg
        px = x1 + dx * t
        py = y1 + dy * t
        if 0 < t < 1:
            px += random.uniform(-wobble, wobble)
            py += random.uniform(-wobble, wobble)
        pts.append((px, py))
    d.line(pts, fill=color, width=width, joint="curve")
    # 箭头头部
    ang = np.arctan2(dy, dx)
    al = 12
    for da in (2.6, -2.6):
        d.line([(x2, y2), (x2 - al * np.cos(ang + da), y2 - al * np.sin(ang + da))],
               fill=color, width=width)

def draw_annotations(img, annots):
    """FBI 解档批注：红笔圈注 + 手写箭头 + 手写注释（MarkerFelt/Noteworthy）。
    annots: list of dicts:
       {num, text, x, y, arrow_to?, redact?}  num 如 "A-1"/"B-2"
    同时画：编号圆（红笔手写）、侧边手写注释、涂黑块（黑块+豁免码）。
    """
    d = ImageDraw.Draw(img)
    W, H = img.size
    f_num, f_note = _fbi_font(20), _fbi_font(15)

    # 荧光高亮（可选：annot 带 highlight=True 时，在坐标处画半透明黄条）
    for an in annots:
        if an.get("highlight"):
            x, y = an["x"], an["y"]
            overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
            od = ImageDraw.Draw(overlay)
            od.rectangle([x - 30, y - 8, x + an.get("hw", 120), y + 8], fill=(255, 240, 0, 90))
            img.paste(Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB"), (0, 0))
            d = ImageDraw.Draw(img)

    for an in annots:
        cx, cy = an["x"], an["y"]
        color = an.get("color", (200, 30, 30))
        num = an["num"]
        r = an.get("r", 26)

        # 涂黑块（redaction）：an 带 redact=True 时画黑块+豁免码
        if an.get("redact"):
            bw, bh = an.get("rw", 160), an.get("rh", 60)
            d.rectangle([cx, cy, cx + bw, cy + bh], fill=(15, 15, 15))
            d.text((cx + 6, cy + bh - 16), an.get("exemption", "b6"),
                   font=_font(12), fill=(200, 200, 200))
            continue

        # 红笔圈注（手绘椭圆 + 编号）
        _wobbly_ellipse(d, cx, cy, r, color, width=2)
        d.text((cx - 8, cy - 12), num, font=f_num, fill=color)

        # 手写箭头引线（到注释位置）
        if an.get("arrow_to"):
            _wobbly_line(d, (cx + r, cy), an["arrow_to"], color, width=2)

        # 侧边手写注释（FBI 边缘批注感：MarkerFelt 手写体）
        text = an["text"]
        nx, ny = an.get("note_pos", (cx + r + 16, cy - 20))
        # 手写体逐字带轻微抖动更真实，但保持可读性：直接画，稍带旋转感省略
        d.text((nx, ny), text, font=f_note, fill=color)

    # 印章独立处理在 make_cctv 内（draw_seal）

def draw_thermal_scale(img, field_m, t_min=-30, t_max=62):
    """热像仪温度刻度条：ironbow 色板竖条 + 温度读数 + 中心十字测温"""
    W, H = img.size
    d = ImageDraw.Draw(img)
    bar_x, bar_w = W - 30, 16
    bar_y0, bar_h = 90, H - 180
    # 色板（与 apply_wavelength ironbow 一致）
    def ironbow(t):
        r = np.clip(np.interp(t, [0.0, 0.25, 0.5, 0.75, 1.0], [0, 0, 0.6, 1.0, 0.9]), 0, 1)
        g = np.clip(np.interp(t, [0.0, 0.25, 0.5, 0.75, 1.0], [0, 0.55, 1.0, 0.55, 0]), 0, 1)
        b = np.clip(np.interp(t, [0.0, 0.25, 0.5, 0.75, 1.0], [0.95, 1.0, 0.4, 0, 0]), 0, 1)
        return (int(r*255), int(g*255), int(b*255))
    for i in range(bar_h):
        t = 1 - i / bar_h  # 上热下冷
        d.line([(bar_x, bar_y0 + i), (bar_x + bar_w, bar_y0 + i)], fill=ironbow(t))
    # 温度刻度
    f = _font(11)
    d.text((bar_x - 4, bar_y0 - 16), f"{t_max}C", font=f, fill=(255, 255, 255))
    d.text((bar_x - 4, bar_y0 + bar_h + 2), f"{t_min}C", font=f, fill=(150, 200, 255))
    d.text((bar_x - 34, bar_y0 + bar_h // 2 - 8), f"{int((t_max+t_min)/2)}C", font=f, fill=(255, 255, 255))
    # 框
    d.rectangle([bar_x - 2, bar_y0 - 20, bar_x + bar_w + 2, bar_y0 + bar_h + 18], outline=(255, 255, 255, 160), width=1)
    # 中心测温十字（最大热区提示）
    cx, cy = W // 2, H // 2 - 20
    for (x1, y1, x2, y2) in [(cx-20, cy, cx-6, cy), (cx+6, cy, cx+20, cy),
                             (cx, cy-20, cx, cy-6), (cx, cy+6, cx, cy+20)]:
        d.line([(x1, y1), (x2, y2)], fill=(255, 255, 255), width=1)
    d.text((cx + 8, cy + 4), f"MAX {t_max-8}..{t_max}C", font=_font(11), fill=(255, 220, 180))
    return img


def draw_seal(img, text, x=None, y=None):
    W, H = img.size
    x = x if x is not None else W - 150
    y = y if y is not None else 120
    overlay = Image.new("RGBA", (140, 140), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    red = (200, 30, 30, 165)
    f = _font(20)
    od.ellipse([6, 6, 134, 134], outline=red, width=3)
    tw = od.textlength(text, font=f)
    od.text(((140 - tw) / 2, 60), text, font=f, fill=red)
    overlay = overlay.rotate(8, expand=False, resample=Image.BICUBIC)
    full = Image.new("RGBA", img.size, (0, 0, 0, 0))
    full.paste(overlay, (x, y))
    img.paste(Image.alpha_composite(img.convert("RGBA"), full).convert("RGB"), (0, 0))

# ---------- 标准监控 OSD（参考真实 CCTV/NVR 界面） ----------

def draw_osd(img, cam, timestamp, loc, rec, events=None, motion_boxes=None,
             pip=None, pip_box=None, mode="visible"):
    """标准监控 OSD：右上时间戳、相机标签条、REC 计时、底部事件滚动条、
    运动检测框、画中画全局定位。参考真实 DVR/NVR 界面元素。
    pip: 母图 PIL Image；pip_box: 当前画面在母图中的区域 (x1,y1,x2,y2)
    events: [(time, level, text), ...] 底部事件滚动条
    """
    W, H = img.size
    d = ImageDraw.Draw(img)
    f_ts, f_s, f_m = _font(22), _font(14), _font(12)

    # 右上：时间戳（白字黑底半透明条，标准 CCTV 样式）
    ts_text = timestamp
    tw = d.textlength(ts_text, font=f_ts)
    d.rectangle([W - tw - 24, 10, W - 10, 42], fill=(0, 0, 0, 170))
    d.text((W - tw - 16, 14), ts_text, font=f_ts, fill=(255, 255, 255))
    # 右上角下方：REC + 录制计时
    if rec:
        d.ellipse([W - 150, 50, W - 134, 66], fill=(235, 40, 40))
        d.text((W - 126, 48), "REC", font=f_s, fill=(235, 60, 60))
        d.text((W - 150, 70), "0:08:42", font=f_m, fill=(200, 205, 210))

    # 左上：相机标签（黑底条，黄/白色文字）
    label = f"CAM-{cam}  {loc}"
    lw = d.textlength(label, font=f_s)
    d.rectangle([10, 10, 10 + lw + 16, 36], fill=(0, 0, 0, 170))
    d.text((18, 15), label, font=f_s, fill=(255, 235, 80))
    # 左上角下方：系统状态行（分辨率/编码/信号）
    d.rectangle([10, 40, 10 + d.textlength("4K 30fps H.265 CH-01 ONLINE", font=f_m) + 16, 58], fill=(0, 0, 0, 140))
    d.text((18, 44), "4K 30fps H.265 CH-01 ONLINE", font=f_m, fill=(140, 220, 140))

    # 画中画：全局定位（PTZ 数字变焦时显示母图+当前框）
    if pip is not None and pip_box:
        pw, ph = 260, 146
        px, py = W - pw - 14, H - ph - 70
        small = pip.resize((pw, ph), Image.LANCZOS)
        img.paste(small, (px, py))
        d = ImageDraw.Draw(img)
        # 当前区域在母图中的比例框
        mx1, my1, mx2, my2 = pip_box
        bx = px + int(pw * mx1 / pip.width)
        by = py + int(ph * my1 / pip.height)
        bw_ = max(int(pw * (mx2 - mx1) / pip.width), 4)
        bh_ = max(int(ph * (my2 - my1) / pip.height), 4)
        d.rectangle([bx, by, bx + bw_, by + bh_], outline=(255, 80, 80), width=2)
        d.text((px + 4, py - 18), "全局定位 · CAM-01 全景", font=_font(11), fill=(255, 235, 80))

    # 运动检测框（绿框 + MD 标签，闪烁感）
    if motion_boxes:
        for mb in motion_boxes:
            x1, y1, x2, y2 = mb
            d.rectangle([x1, y1, x2, y2], outline=(120, 255, 120), width=2)
            d.text((x1, y1 - 18), "MOTION", font=_font(11), fill=(120, 255, 120))

    # 底部：事件滚动条（NVR 事件日志）
    if events:
        yb = H - 26
        d.rectangle([0, yb, W, H], fill=(0, 0, 0, 190))
        ev_line = "  |  ".join(f"[{t}] {lvl} {txt}" for (t, lvl, txt) in events)
        d.text((10, yb + 5), ev_line, font=_font(11), fill=(200, 205, 210))
    else:
        d.rectangle([0, H - 24, W, H], fill=(0, 0, 0, 170))
        d.text((10, H - 19), f"REC-{cam} · {timestamp} · 站钟同步", font=_font(12), fill=(160, 165, 170))


# ---------- 主流程 ----------

def make_cctv(base, out, cam, timestamp, mode="visible", loc="",
              field_m=40.0, zoom=1.0, rec=True, annots=None,
              seal=None, targets_override=None, label_prefix="SUBJ",
              crop=None, events=None, motion_boxes=None, pip=None, pip_box=None,
              hot_zones=None):
    img = Image.open(base).convert("RGB")
    W, H = img.size
    # 裁剪派生（数字变焦：从母图裁区域放大到全幅，保证同源）
    if crop:
        x1, y1, x2, y2 = [int(v) for v in crop]
        img = img.crop((x1, y1, x2, y2)).resize((W, H), Image.LANCZOS)
    img = apply_wavelength(img, mode, hot_zones=hot_zones)
    # 轻噪点（数字传感器水平，不糊化）
    a = np.asarray(img).astype(np.float32)
    a += np.random.normal(0, 6, a.shape[:2])[..., None]
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(img)
    f_big, f_s = _font(20), _font(14)

    # 目标检测
    targets = targets_override if targets_override is not None else detect_targets(img, mode)
    if targets:
        for idx, t in enumerate(targets, 1):
            x1, y1, x2, y2 = t[:4]
            x1, y1 = max(x1, 2), max(y1, 2)
            x2, y2 = min(x2, W - 2), min(y2, H - 2)
            color = (240, 190, 60) if mode == "thermal" else (140, 230, 170)
            d.rectangle([x1, y1, x2, y2], outline=color, width=1)
            label = f"{label_prefix}-{idx:02d}"
            lw = d.textlength(label, font=f_s)
            tag_y = max(y1 - 20, 2)
            d.rectangle([x1, tag_y, x1 + lw + 8, tag_y + 17], fill=(20, 20, 20, 180))
            d.text((x1 + 4, tag_y + 1), label, font=_font(12), fill=color)
            w_m = (x2 - x1) * field_m / W
            d.text((x1, y2 + 2), f"{w_m:.1f}m", font=_font(11), fill=color)

    # 数字监控刻度（弱化，OSD 之下）
    draw_rulers(d, W, H, field_m, zoom)

    # 标准监控 OSD
    draw_osd(img, cam, timestamp, loc, rec, events=events,
             motion_boxes=motion_boxes, pip=pip, pip_box=pip_box, mode=mode)

    # 读图员批注层（FBI 解档风，最后画压在最上）
    if annots:
        draw_annotations(img, annots)
    if seal:
        draw_seal(img, seal)
    # 热像温度刻度条（ironbow 色板 + 温度读数）
    if mode == "thermal":
        img = draw_thermal_scale(img, field_m)

    img.save(out, quality=90)
    return {"out": out, "targets": targets, "size": [W, H]}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("base")
    ap.add_argument("out")
    ap.add_argument("--cam", required=True)
    ap.add_argument("--time", required=True)
    ap.add_argument("--mode", default="visible", choices=["visible", "thermal", "ir", "nv"])
    ap.add_argument("--loc", default="")
    ap.add_argument("--annot", action="append", default=[], help="编号|文字|x|y[|箭头x|箭头y]")
    ap.add_argument("--field-m", type=float, default=40.0)
    ap.add_argument("--zoom", type=float, default=1.0)
    ap.add_argument("--no-rec", action="store_true")
    ap.add_argument("--seal", default="")
    ap.add_argument("--prefix", default="SUBJ")
    ap.add_argument("--crop", default="", help="x1,y1,x2,y2 母图裁剪区域（数字变焦）")
    ap.add_argument("--event", action="append", default=[], help="时间|级别|文本（底部事件滚动条）")
    ap.add_argument("--motion", action="append", default=[], help="x1,y1,x2,y2 运动检测框")
    ap.add_argument("--pip", default="", help="母图路径（画中画全局定位）")
    ap.add_argument("--pip-box", default="", help="x1,y1,x2,y2 当前画面在母图中的区域")
    ap.add_argument("--hot", action="append", default=[], help="x1,y1,x2,y2 归一化热区（热像模式，推进器/热源位置）")
    args = ap.parse_args()

    annots = []
    for a in args.annot:
        parts = a.split("|")
        an = {"num": parts[0], "text": parts[1], "x": int(parts[2]), "y": int(parts[3])}
        # 扩展字段：第5位起，可含 arrow_to/note_pos 坐标对或 redact/highlight 标志
        rest = parts[4:]
        flags = [f for f in rest if f in ("redact", "highlight")]
        coords = [int(v) for v in rest if v not in ("redact", "highlight")]
        if len(coords) >= 2:
            an["arrow_to"] = (coords[0], coords[1])
        if len(coords) >= 4:
            an["note_pos"] = (coords[2], coords[3])
        for f in flags:
            an[f] = True
        annots.append(an)

    res = make_cctv(args.base, args.out, args.cam, args.time, args.mode,
                    args.loc, args.field_m, args.zoom, not args.no_rec,
                    annots, args.seal, label_prefix=args.prefix,
                    crop=[int(v) for v in args.crop.split(",")] if args.crop else None,
                    events=[tuple(e.split("|")) for e in args.event] if args.event else None,
                    motion_boxes=[tuple(int(v) for v in m.split(",")) for m in args.motion] if args.motion else None,
                    pip=Image.open(args.pip) if args.pip else None,
                    pip_box=[int(v) for v in args.pip_box.split(",")] if args.pip_box else None,
                    hot_zones=[tuple(float(v) for v in h.split(",")) for h in args.hot] if args.hot else None)
    print(f"OK: {res['out']}  targets={res['targets']}  annots={len(annots)}")
