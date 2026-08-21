#!/usr/bin/env python3
"""重建 craft/格子状态矩阵.csv(245 格全量状态)。

从 artifacts/writing/ 各篇 front matter 的 coord 解析占用,规范化空间带写法
(裸「地球/地月系/内太阳系/深空/比邻星」→ ①-⑤),输出 245 行 CSV。
状态:OPEN=0 篇 / PART=1-2 篇 / FULL=≥3 篇。
用法:python3 scripts/generate_matrix.py
"""
import re
import glob
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WRITING = ROOT / "artifacts" / "writing"
OUT = ROOT / "craft" / "格子状态矩阵.csv"

DIMS = ["工程", "人", "社会", "经济", "生态", "文化", "知识"]
ERAS = ["替代", "竞赛", "丰裕", "离心", "启航", "落地", "双星系"]
SPACES = ["①地球", "②地月系", "③内太阳系", "④深空", "⑤比邻星"]
SP_MAP = {
    "地球": "①地球", "地月系": "②地月系", "内太阳系": "③内太阳系",
    "深空": "④深空", "比邻星": "⑤比邻星",
    "①地球": "①地球", "②地月系": "②地月系", "③内太阳系": "③内太阳系",
    "④深空": "④深空", "⑤比邻星": "⑤比邻星",
}


def parse_coord(cell: str):
    parts = cell.replace(" ", "").split("×")
    if len(parts) != 3:
        return None
    dim, era, sp = parts
    sp = SP_MAP.get(sp)
    if sp is None:
        return None
    return (dim, era, sp)


def main():
    grid = defaultdict(int)
    for f in glob.glob(str(WRITING / "*.md")):
        txt = Path(f).read_text(encoding="utf-8")
        m = re.search(r"^coord:\s*(.+)$", txt, re.M)
        if not m:
            continue
        p = parse_coord(m.group(1).strip())
        if p:
            grid[p] += 1

    lines = ["维度,纪元,空间带,状态,产物数,备注"]
    for d in DIMS:
        for e in ERAS:
            for s in SPACES:
                n = grid.get((d, e, s), 0)
                state = "OPEN" if n == 0 else ("FULL" if n >= 3 else "PART")
                lines.append(f"{d},{e},{s},{state},{n},")
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    occupied = len(grid)
    print(f"已勘探 {occupied}/245 格,空白 {245 - occupied} 格 → {OUT}")


if __name__ == "__main__":
    main()
