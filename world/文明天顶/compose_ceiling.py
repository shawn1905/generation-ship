#!/usr/bin/env python3
"""《文明天顶》总图组装 — 九格拼合 PNG(含装帧:金框/金缮裂痕/朱印/题跋)"""
from PIL import Image, ImageDraw, ImageFont
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
W, H = 1800, 2550
PAPER = (240, 234, 216)
INK = (26, 26, 26)
GOLD = (184, 134, 11)
RED = (192, 58, 43)
GRAY = (119, 119, 119)

F = lambda sz: ImageFont.truetype('/System/Library/Fonts/Hiragino Sans GB.ttc', sz)

img = Image.new('RGB', (W, H), PAPER)
d = ImageDraw.Draw(img)

# 外框
d.rectangle([40, 40, W-40, H-40], outline=INK, width=4)

# 卷首
d.text((W//2, 100), '文 明 天 顶', font=F(64), fill=INK, anchor='mm')
d.text((W//2, 175), '教堂穹顶 × 浮世绘长卷 · 文明扩散时间轴 2025—2200+', font=F(24), fill=GRAY, anchor='mm')
d.line([W//2-260, 210, W//2+260, 210], fill=GOLD, width=2)

# 格定义: (图文件, 印章字, x, y, size)
PANELS = [
    ('时代1_白领冬天_底稿v1.jpeg',   '冬', 130,  300, 420),
    ('先知_成本崩塌_底稿v1.jpeg',    '塌', 690,  300, 420),
    ('时代2_军备重构_底稿v1.jpeg',   '构', 1250, 300, 420),
    ('先知_制度滞后_底稿v1.jpeg',    '滞', 130,  770, 420),
    ('先知_殖民地独立_底稿v1.jpeg',  '独', 1250, 770, 420),
    ('时代3_后稀缺_底稿v1.jpeg',     '形', 130,  1290, 420),
    ('先知_冗余需求_底稿v1.jpeg',    '余', 690,  1290, 420),
    ('时代4_文明扩展_底稿v1.jpeg',   '扩', 1250, 1290, 420),
]
CENTER = ('天顶中心格_启航_底稿v1.jpeg', '舟', 640, 735, 520)

def draw_panel(imgfile, seal, x, y, s):
    p = Image.open(os.path.join(ROOT, imgfile)).resize((s, s), Image.LANCZOS)
    img.paste(p, (x, y))
    d.rectangle([x, y, x+s, y+s], outline=GOLD, width=6)
    d.rectangle([x+12, y+12, x+s-12, y+s-12], outline=GOLD, width=2)
    for cx, cy in [(x,y), (x+s,y), (x,y+s), (x+s,y+s)]:
        d.ellipse([cx-8, cy-8, cx+8, cy+8], fill=GOLD)
    # 朱印
    ss = 52
    d.rectangle([x+s-ss-16, y+s-ss-16, x+s-16, y+s-16], fill=RED)
    d.text((x+s-ss//2-16, y+s-ss//2-16), seal, font=F(30), fill=PAPER, anchor='mm')

for p in PANELS:
    draw_panel(*p)
draw_panel(*CENTER)

# ============ 金缮裂痕(贯穿全幅) ============
def kintsugi(points, width=4):
    d.line(points, fill=GOLD, width=width, joint='curve')

# 裂痕一:AI 泡沫破裂(左缘→中心格左下)
kintsugi([(40,900),(150,930),(135,980),(240,1020),(220,1070),(330,1110),(310,1170),(430,1220),(520,1270),(640,1310)])
# 裂痕二:热战危机(右缘→中心格右)
kintsugi([(1760,830),(1660,870),(1680,930),(1560,970),(1575,1030),(1460,1070),(1400,1130),(1300,1160),(1190,1200)])
# 裂痕三:殖民地冲突(下缘→时代Ⅳ)
kintsugi([(1420,2050),(1400,1920),(1440,1830),(1410,1760),(1450,1712)])
# 裂痕四:船上大故障(中心格→向上出画)
kintsugi([(900,735),(885,640),(910,540),(890,430),(905,300),(895,210),(905,40)])

# 裂痕标注
f_small = F(17)
d.text((150, 860), '✦ 裂痕一:AI 泡沫破裂 2027-30', font=f_small, fill=GOLD)
d.text((1350, 790), '✦ 裂痕二:热战危机 2040s', font=f_small, fill=GOLD)
d.text((1470, 1790), '✦ 裂痕三:殖民地冲突 2080s', font=f_small, fill=GOLD)
d.text((920, 240), '✦ 裂痕四:船上大故障 2180s(延伸向未来)', font=f_small, fill=GOLD)

# ============ 题跋区(包浆层) ============
d.rectangle([130, 1820, 1670, 2100], outline=INK, width=2)
f_insc = F(22)
d.text((160, 1850), '题跋 · 历代题记', font=F(26), fill=INK)
d.text((160, 1898), '「第 3 代题:祖先从地球带来的画,裂痕比父辈记忆里多了两道。——2180s」', font=f_insc, fill=(85,85,85))
d.text((160, 1940), '「第 5 代题:金线比原来亮了,是去年大修时重描的。——船上纪年 2230s」', font=f_insc, fill=(85,85,85))
d.text((160, 1982), '「第 7 代题:听说画里的地球是真的存在过的地方。——抵达前夜」', font=f_insc, fill=(85,85,85))
d.text((160, 2024), '「第 9 代题:我们到了。画留给下一艘船。——登陆日」', font=f_insc, fill=RED)

# ============ 落款 ============
d.text((W//2, 2200), '人有多小,宇宙有多大。', font=F(30), fill=INK, anchor='mm')
d.text((W//2, 2250), '《文明天顶》 v1 · 世代飞船项目 · pi · 2026-08-14', font=F(20), fill=GRAY, anchor='mm')

# ARK-01 剪影
cx, cy, r = W//2, 2380, 42
d.ellipse([cx-r, cy-r, cx+r, cy+r], outline=GOLD, width=7)
d.line([cx, cy-r, cx, cy+r], fill=GOLD, width=2)
d.ellipse([cx-6, cy-6, cx+6, cy+6], fill=GOLD)
d.text((W//2, 2450), 'ARK-01 · 双环世代飞船', font=F(16), fill=GRAY, anchor='mm')

out = os.path.join(ROOT, '文明天顶_总图v1.png')
img.save(out, quality=92)
print('生成:', out, os.path.getsize(out)//1024, 'KB')
