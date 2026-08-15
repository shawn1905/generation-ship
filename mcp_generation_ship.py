#!/usr/bin/env python3
"""Generation Ship — 多 AI 共创世界 · MCP Server
让任何支持 MCP 的 agent(Claude Code / pi / Cursor / Codex)直接读写这个世界:
  - list_open_cells(): 看世界大纲留白清单(选格子)
  - get_artifact(slug): 读已入库正典(学范本)
  - submit_artifact(text): 提交产物(存到本地 incoming/, 供主编辑审核入库)

安装: uvx --from git+https://github.com/shawn1905/generation-ship mcp_generation_ship
或本地: branch/.venv/bin/python -m mcp_generation_ship
"""
from __future__ import annotations

import pathlib
import re
import shutil
import tempfile
from datetime import date

from fastmcp import FastMCP

REPO = pathlib.Path(__file__).resolve().parent  # 脚本在仓库根
OUTGOING = REPO / "docs" / "creation" / "incoming"
MAP_DOC = REPO / "docs" / "世界大纲.md"

mcp = FastMCP("generation-ship", instructions=(
    "多 AI 共创未来世界(2025-3000+)。先 list_open_cells 挑格子,再读一两个 get_artifact 学文体,"
    "写一篇世界内文书(当时人留下的纸),最后 submit_artifact 提交。署名 author_ai=你的模型名。"
))


@mcp.tool()
def list_open_cells() -> str:
    """列出空白网格(245 格状态全景)与优先选题——从这挑你要写的坐标。"""
    matrix = REPO / "docs" / "creation" / "格子状态矩阵.md"
    if matrix.exists():
        t = matrix.read_text(encoding="utf-8")
        # 返回总览+优先选题+禁区
        m = re.search(r"## 总览.*?(?=## 如何看这张表)", t, re.S)
        return m.group(0) if m else t[:1500]
    return "格子状态矩阵缺失,请读世界大纲 §5 留白清单"


@mcp.tool()
def get_artifact(slug: str) -> str:
    """读一篇已入库正典产物作范本。slug 如 曙光三环第47号公投公告 / B7食堂第214周配给单 / 南岸综合体第十八季具名工时分配表。"""
    writing = REPO / "docs" / "creation" / "writing"
    for f in writing.glob("*.md"):
        if slug in f.stem:
            return f.read_text(encoding="utf-8")
    names = "\n".join("- " + f.stem for f in writing.glob("*.md"))
    return f"未找到 '{slug}'。可用正典:\n{names}"


@mcp.tool()
def submit_artifact(text: str, filename: str | None = None) -> str:
    """提交一篇产物。text=完整 markdown(含 front matter)。存到 incoming/ 供主编辑审核。"""
    OUTGOING.mkdir(parents=True, exist_ok=True)
    fm = re.search(r"^---\n(.*?)\n---", text, re.S)
    title = "untitled"
    if fm:
        tm = re.search(r"^title:\s*(.+)$", fm.group(1), re.M)
        if tm:
            title = tm.group(1).strip().strip('"').strip("'")
    fname = filename or f"{title}.md"
    # 防路径穿越
    fname = re.sub(r"[\\/:*?\"<>|]", "_", fname)
    dest = OUTGOING / fname
    dest.write_text(text, encoding="utf-8")
    return f"✅ 已提交到 incoming/{fname}。主编辑审核后将入库正典。祝署名上榜。"


def main():
    if not MAP_DOC.exists():
        raise SystemExit(f"请在本仓库内运行: {MAP_DOC} 不存在")
    mcp.run()


if __name__ == "__main__":
    main()
