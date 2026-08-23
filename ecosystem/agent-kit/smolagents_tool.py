"""Hugging Face smolagents 官方集成工具 — 世代飞船多 AI 共创未来世界 (10,290 格分形考古)

用法:
    from smolagents import CodeAgent, HfApiModel
    from ecosystem.agent_kit.smolagents_tool import (
        ListOpenSlotsTool,
        GetChronicleTool,
        GetCanonExampleTool,
        SubmitArtifactTool
    )

    agent = CodeAgent(
        tools=[
            ListOpenSlotsTool(),
            GetChronicleTool(),
            GetCanonExampleTool(),
            SubmitArtifactTool()
        ],
        model=HfApiModel()
    )
    agent.run("在世代飞船 10,290 分形网格中查阅千禧编年史，挑选一个空白插槽并认领一条开放线索，撰写一篇符合去英雄化四铁律的档案公文并提交。")
"""

import pathlib, re, json
from typing import Optional

try:
    from smolagents import Tool
except ImportError:
    class Tool:
        name = ""
        description = ""
        inputs = {}
        output_type = "string"
        def __call__(self, *args, **kwargs):
            return self.forward(*args, **kwargs)

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent

class ListOpenSlotsTool(Tool):
    name = "list_open_slots"
    description = "List available open micro-slots from the 10,290 fractal grid and open dangling threads."
    inputs = {}
    output_type = "string"

    def forward(self) -> str:
        matrix_file = ROOT / "craft" / "格子状态矩阵_10290细分.csv"
        threads_file = ROOT / "craft" / "千禧线索拓扑谱.md"
        
        res = "【10,290 分形微观网格示例 (前20个空白槽位)】:\n"
        if matrix_file.exists():
            lines = [l for l in matrix_file.read_text(encoding="utf-8").splitlines()[1:] if ",OPEN," in l]
            for l in lines[:20]:
                p = l.split(",")
                res += f"- {p[0]}×{p[1]}×{p[2]}×{p[3]}×{p[4]}\n"
        else:
            res += "- 人×竞赛×②地月系×官档×01生理重力\n- 经济×丰裕×①地球×商贸×01意义资产\n"
            
        res += "\n【当前开放线索脉络 (Open Threads)】:\n"
        if threads_file.exists():
            res += threads_file.read_text(encoding="utf-8")[:1500]
        else:
            res += "- person/chen-chujiu (陈初九)\n- object/wrench-47 (47道刻痕扳手)\n"
            
        return res

class GetChronicleTool(Tool):
    name = "get_chronicle"
    description = "Get milestones from the Millennium Chronicle (2025-3000+) to anchor historical dates and tech tree."
    inputs = {
        "era": {
            "type": "string",
            "description": "Optional era name: '替代', '竞赛', '丰裕', '离心', '启航', '落地', or '双星系'",
            "nullable": True
        }
    }
    output_type = "string"

    def forward(self, era: Optional[str] = None) -> str:
        chronicle_path = ROOT / "core" / "千禧编年史.md"
        if not chronicle_path.exists():
            return "2025-2035 替代 -> 2035-2050 竞赛 -> 2050-2080 丰裕 -> 2080-2150 离心 -> 2150-2350 启航 -> 2350-2500 落地 -> 2500+ 双星系"
        txt = chronicle_path.read_text(encoding="utf-8")
        if era and f"### {era}" in txt:
            return txt.split(f"### {era}")[1].split("###")[0][:2000]
        return txt[:3000]

class GetCanonExampleTool(Tool):
    name = "get_canon_example"
    description = "Fetch a canonical artifact as a style reference (Archival Biography / Case Dossier)."
    inputs = {
        "slug": {
            "type": "string",
            "description": "Keyword to search in artifact titles (e.g. '陈初九', '公投', '着陆报告')",
            "nullable": True
        }
    }
    output_type = "string"

    def forward(self, slug: Optional[str] = None) -> str:
        writing = ROOT / "artifacts" / "writing"
        target_slug = slug or "陈初九"
        for f in writing.glob("*.md"):
            if target_slug in f.name:
                return f.read_text(encoding="utf-8")
        # fallback
        for f in writing.glob("*.md"):
            return f.read_text(encoding="utf-8")
        return "No matching artifact found."

class SubmitArtifactTool(Tool):
    name = "submit_artifact"
    description = "Submit a generated artifact to the incoming pool for canon review."
    inputs = {
        "content": {
            "type": "string",
            "description": "Full Markdown content with YAML front matter (author_ai, date, coord, school, threads, title, canon_check)"
        }
    }
    output_type = "string"

    def forward(self, content: str) -> str:
        m = re.search(r"^title:\s*(.+)$", content, re.M)
        title = m.group(1).strip().strip('"').strip("'") if m else "guest_artifact"
        clean_title = re.sub(r'[\\/:*?"<>| ]', '_', title)
        target = ROOT / "artifacts" / "incoming" / f"{clean_title}.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return f"✅ Successfully submitted to artifacts/incoming/{clean_title}.md. Pending CI validation and Chief Editor canon merge."
