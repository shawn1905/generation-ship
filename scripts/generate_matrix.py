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
OUT_10290 = ROOT / "craft" / "格子状态矩阵_10290细分.csv"

DIMS = ["工程", "人", "社会", "经济", "生态", "文化", "知识"]
ERAS = ["替代", "竞赛", "丰裕", "离心", "启航", "落地", "双星系"]
SPACES = ["①地球", "②地月系", "③内太阳系", "④深空", "⑤比邻星"]
SCHOOLS = ["官档", "私档", "互济", "商贸", "工技", "科医"]
FACETS = {
    "工程": ["01主承力", "02推进工质", "03主动磁防", "04能源聚变", "05生命闭环", "06自控算力", "07拆解延寿"],
    "人": ["01生理重力", "02心理潜意识", "03代际认知", "04脑机共生", "05深空葬仪", "06代际启蒙", "07感官代偿"],
    "社会": ["01权力更迭", "02配给政治", "03殖民离心", "04违禁治安", "05社群解构", "06身份界定", "07仪式公投"],
    "经济": ["01意义资产", "02物质配给", "03暗舱黑市", "04贸易关税", "05具名工时", "06残值回收", "07风险平准"],
    "生态": ["01水藻循环", "02低重力农牧", "03辐射突变", "04人工气压", "05生化降解", "06极端采样", "07闭环防疫"],
    "文化": ["01舱内方言", "02旧地神话", "03精神消费", "04纪念节日", "05深空虚无", "06音频物证", "07合成风味"],
    "知识": ["01双轨历法", "02度量演进", "03技术逆向", "04中继丢包", "05档案存真", "06教学审查", "07巡天观测"],
}
SP_MAP = {
    "地球": "①地球", "地月系": "②地月系", "内太阳系": "③内太阳系",
    "深空": "④深空", "比邻星": "⑤比邻星",
    "①地球": "①地球", "②地月系": "②地月系", "③内太阳系": "③内太阳系",
    "④深空": "④深空", "⑤比邻星": "⑤比邻星",
}


def parse_coord(cell: str):
    parts = [p.strip() for p in cell.replace(" ", "").split("×")]
    if len(parts) < 3 or len(parts) > 5:
        return None
    dim, era, sp = parts[0], parts[1], parts[2]
    sp = SP_MAP.get(sp)
    if sp is None or dim not in DIMS or era not in ERAS:
        return None
    school = parts[3] if len(parts) >= 4 else "官档"
    facet = parts[4] if len(parts) == 5 else FACETS[dim][0]
    return (dim, era, sp, school, facet)


def main():
    macro_grid = defaultdict(int)
    micro_grid = defaultdict(int)
    for f in glob.glob(str(WRITING / "*.md")):
        txt = Path(f).read_text(encoding="utf-8")
        m = re.search(r"^coord:\s*(.+)$", txt, re.M)
        if not m:
            continue
        p = parse_coord(m.group(1).strip())
        if p:
            dim, era, sp, school, facet = p
            macro_grid[(dim, era, sp)] += 1
            micro_grid[(dim, era, sp, school, facet)] += 1

    # 1. 生成 245 宏观矩阵
    lines_245 = ["维度,纪元,空间带,状态,产物数,备注"]
    for d in DIMS:
        for e in ERAS:
            for s in SPACES:
                n = macro_grid.get((d, e, s), 0)
                state = "OPEN" if n == 0 else ("FULL" if n >= 3 else "PART")
                lines_245.append(f"{d},{e},{s},{state},{n},")
    OUT.write_text("\n".join(lines_245) + "\n", encoding="utf-8")

    # 2. 生成 10,290 微观分形矩阵
    lines_10290 = ["维度,纪元,空间带,学派形态,领域切片,状态,产物数"]
    for d in DIMS:
        for e in ERAS:
            for s in SPACES:
                for sc in SCHOOLS:
                    for fa in FACETS[d]:
                        n = micro_grid.get((d, e, s, sc, fa), 0)
                        state = "OPEN" if n == 0 else ("FULL" if n >= 3 else "PART")
                        lines_10290.append(f"{d},{e},{s},{sc},{fa},{state},{n}")
    OUT_10290.write_text("\n".join(lines_10290) + "\n", encoding="utf-8")

    occupied_macro = len(macro_grid)
    occupied_micro = len(micro_grid)
    print(f"【宏观星区】已勘探 {occupied_macro}/245 格，空白 {245 - occupied_macro} 格 → {OUT}")
    print(f"【分形微观】已勘探 {occupied_micro}/10290 格，空白 {10290 - occupied_micro} 格 → {OUT_10290}")


if __name__ == "__main__":
    main()
