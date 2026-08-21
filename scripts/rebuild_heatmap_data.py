#!/usr/bin/env python3
"""重建 scripts/heatmap_data.json(245 格档案舱数据)。

从 artifacts/writing/ 各篇 front matter 提取(coord/author_ai/title/image),
snippet 取正文首段截断,计算 245 格 cells 状态(已勘探格),输出与
ecosystem/heatmap_3d.html 内嵌 const DATA 同 schema 的 JSON。

用法:python3 scripts/rebuild_heatmap_data.py
"""
import json
import re
import glob
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WRITING = ROOT / "artifacts" / "writing"
OUT = ROOT / "scripts" / "heatmap_data.json"

DIMS = ["工程", "人", "社会", "经济", "生态", "文化", "知识"]
ERAS = ["替代", "竞赛", "丰裕", "离心", "启航", "落地", "双星系"]
SPACES = ["①地球", "②地月系", "③内太阳系", "④深空", "⑤比邻星"]
SP_MAP = {
    "地球": "①地球", "地月系": "②地月系", "内太阳系": "③内太阳系",
    "深空": "④深空", "比邻星": "⑤比邻星",
    "①地球": "①地球", "②地月系": "②地月系", "③内太阳系": "③内太阳系",
    "④深空": "④深空", "⑤比邻星": "⑤比邻星",
}
SNIPPET_LEN = 223


def parse_coord(cell: str):
    parts = cell.replace(" ", "").split("×")
    if len(parts) != 3:
        return None
    dim, era, sp = parts
    sp = SP_MAP.get(sp)
    if sp is None:
        return None
    return (dim, era, sp)


def parse_front_matter(txt: str):
    """返回 dict(field->value),仅 front matter 内字段。"""
    m = re.match(r"^---\n(.*?)\n---", txt, re.S)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        mm = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if mm:
            fm[mm.group(1)] = mm.group(2).strip()
    return fm


def main():
    docs = []
    coord_count = defaultdict(int)
    for f in sorted(glob.glob(str(WRITING / "*.md"))):
        txt = Path(f).read_text(encoding="utf-8")
        fm = parse_front_matter(txt)
        coord = fm.get("coord", "")
        p = parse_coord(coord)
        if not p:
            print(f"SKIP(coord 解析失败): {Path(f).name}")
            continue
        dim, era, sp = p
        dim_idx = DIMS.index(dim)
        era_idx = ERAS.index(era)
        zone_idx = SPACES.index(sp)
        # 正文(去除 front matter)
        body = txt
        m = re.match(r"^---\n.*?\n---\n?(.*)$", txt, re.S)
        if m:
            body = m.group(1)
        snippet = re.sub(r"\s+", " ", body).strip()[:SNIPPET_LEN]
        docs.append({
            "id": len(docs),
            "filename": Path(f).name,
            "title": fm.get("title", Path(f).stem),
            "author_ai": fm.get("author_ai", ""),
            "date": fm.get("date", ""),
            "coord": coord.replace(" ", ""),
            "archive_id": fm.get("archive_id", ""),
            "dim_idx": dim_idx,
            "era_idx": era_idx,
            "zone_idx": zone_idx,
            "dim_name": dim,
            "era_name": era,
            "zone_name": sp,
            "rel_path": f"artifacts/writing/{Path(f).name}",
            "image": fm.get("image", ""),
            "snippet": snippet,
            "full_text": body,
        })
        coord_count[(dim, era, sp)] += 1

    # cells: 245 格全量,doc_count/doc_ids 按 coord 聚合
    cells = []
    for e, era in enumerate(ERAS):
        for z, sp in enumerate(SPACES):
            for d, dim in enumerate(DIMS):
                ids = [doc["id"] for doc in docs
                       if doc["era_idx"] == e and doc["zone_idx"] == z and doc["dim_idx"] == d]
                cells.append({
                    "key": f"{e}_{z}_{d}",
                    "e": e, "z": z, "d": d,
                    "era": era, "zone": sp, "dim": dim,
                    "coord_str": f"{dim} × {era} × {sp}",
                    "doc_count": len(ids),
                    "doc_ids": ids,
                })

    data = {
        "eras": ERAS, "zones": SPACES, "dims": DIMS,
        "docs": docs,
        "cells": cells,
        "total_cells": 245,
        "explored_cells": sum(1 for c in cells if c["doc_count"] > 0),
        "total_docs": len(docs),
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    print(f"OK: {len(docs)} docs / {data['explored_cells']} cells explored / {len(cells)} total cells")
    print(f"写入 {OUT}")


if __name__ == "__main__":
    main()
