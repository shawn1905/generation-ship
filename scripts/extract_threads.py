#!/usr/bin/env python3
"""全库线索提取与拓扑谱生成器 (Threading Topology Engine)。

用法: python3 scripts/extract_threads.py
功能: 扫描 artifacts/writing/ 下所有正典的 front matter 中的 threads 字段，
      聚合四大线索命名空间 (person/, object/, lineage/, system/, event/)，
      生成 craft/千禧线索拓扑谱.md，为新 AI 创作者提供「开放线索池」。
"""

import re
import glob
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WRITING = ROOT / "artifacts" / "writing"
OUT = ROOT / "craft" / "千禧线索拓扑谱.md"


def parse_front_matter(txt: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---", txt, re.S)
    if not m:
        return {}
    fm = {}
    current_key = None
    current_val = []
    for line in m.group(1).splitlines():
        mm = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if mm:
            if current_key:
                fm[current_key] = "\n".join(current_val).strip()
            current_key = mm.group(1)
            val = mm.group(2).strip()
            current_val = [val] if val else []
        elif current_key and (line.startswith(" ") or line.startswith("\t") or line.startswith("-")):
            current_val.append(line.strip())
    if current_key:
        fm[current_key] = "\n".join(current_val).strip()
    return fm


def main():
    threads_map = defaultdict(list)
    total_docs = 0

    for f in sorted(glob.glob(str(WRITING / "*.md"))):
        if Path(f).name in ("README.md", "TEMPLATE.md"):
            continue
        total_docs += 1
        txt = Path(f).read_text(encoding="utf-8")
        fm = parse_front_matter(txt)
        archive_id = fm.get("archive_id", "GS-????-??")
        title = fm.get("title", Path(f).stem)
        coord = fm.get("coord", "")
        author_ai = fm.get("author_ai", "")
        threads_raw = fm.get("threads", "")

        if not threads_raw:
            continue

        items = [t.strip().lstrip("- ") for t in threads_raw.splitlines() if t.strip().lstrip("- ")]
        for t in items:
            threads_map[t].append({
                "archive_id": archive_id,
                "title": title,
                "coord": coord,
                "filename": Path(f).name,
                "author_ai": author_ai,
            })

    # 分类聚合
    categories = {
        "person": ("👤 人物命运线 (Person Threads)", "记录个体在制度与物理环境中的一生磨损与选择"),
        "object": ("🔧 物证流转线 (Object Provenance)", "记录具体工具、器具、信标与生活遗物在世纪间的漂移"),
        "lineage": ("🧬 血脉与回声线 (Lineage & Letters)", "记录跨光年家族通信、麦种繁育、语言变异与记忆流转"),
        "system": ("⚙️ 制度与技术线 (System & Tech)", "记录某项法典、公约或工程构型从立项到退役的演化史"),
        "event": ("🏛️ 重大事件案卷 (Event Dossiers)", "聚拢同一重大历史事件下不同学派的公文证据链"),
    }

    lines = [
        "# 千禧线索拓扑谱（开放线索池）",
        "",
        "> **【创作者工作台】**",
        f"> 本谱由 `scripts/extract_threads.py` 自动扫描全库 **{total_docs} 篇正典** 实时生成。",
        "> 每一个线索 ID 都是跨越时空的「线」，将散落在 10,290 个网格中的「点」穿引成文明之网。",
        "> **如何认领**：新来的 AI 或人类创作者在选定网格后，可在下方挑选已有线索进行接棒续写，并在 front matter 的 `threads:` 中声明。",
        "",
        "---",
        "",
    ]

    for prefix, (cat_title, cat_desc) in categories.items():
        sub_threads = {k: v for k, v in threads_map.items() if k.startswith(prefix + "/")}
        lines.append(f"## {cat_title}")
        lines.append(f"> {cat_desc}")
        lines.append("")
        if not sub_threads:
            lines.append("*暂无挂载线索（欢迎首开线头）*")
            lines.append("")
            continue

        for tid, doc_list in sorted(sub_threads.items()):
            lines.append(f"### 📍 `{tid}`")
            lines.append(f"- **已贯穿网格数**：{len(doc_list)} 篇")
            for doc in doc_list:
                lines.append(f"  - **[{doc['archive_id']}]** `{doc['coord']}` 《{doc['title']}》 *(by {doc['author_ai']})*")
            lines.append("")

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"提取完成：发现 {len(threads_map)} 条线索，写入 {OUT}")


if __name__ == "__main__":
    main()
