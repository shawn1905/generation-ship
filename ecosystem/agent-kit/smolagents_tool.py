"""Hugging Face smolagents 官方工具集成 — 世代飞船多 AI 共创世界

用法:
    from smolagents import CodeAgent, HfApiModel
    from ecosystem.agent_kit.smolagents_tool import GenerationShipWorldbuildingTool

    agent = CodeAgent(
        tools=[GenerationShipWorldbuildingTool()],
        model=HfApiModel()
    )
    agent.run("在世代飞船世界里挑一个深空或落地纪元的空白格子，写一篇符合世界规则的正典文书并提交。")
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

class GenerationShipWorldbuildingTool(Tool):
    name = "generation_ship_worldbuilder"
    description = (
        "Interact with the Generation Ship multi-AI collaborative worldbuilding project. "
        "Allows listing open coordinate cells, fetching rules/canonical examples, and submitting artifacts."
    )
    inputs = {
        "action": {
            "type": "string",
            "description": "Action to perform: 'list_open_cells', 'get_rules', 'get_canon_example', or 'submit_artifact'"
        },
        "payload": {
            "type": "string",
            "description": "Content payload: artifact text for 'submit_artifact', or slug for 'get_canon_example'",
            "nullable": True
        }
    }
    output_type = "string"

    def forward(self, action: str, payload: Optional[str] = None) -> str:
        if action == "list_open_cells":
            matrix = ROOT / "craft" / "格子状态矩阵.md"
            if matrix.exists():
                return matrix.read_text(encoding="utf-8")[:2000]
            return "245-cell grid open: Knowledge/Ecology/Society x Launch/Landing/Double-Star x Deep-Space/Proxima"

        elif action == "get_rules":
            rules = (ROOT / "core" / "世界规则.md").read_text(encoding="utf-8") if (ROOT / "core" / "世界规则.md").exists() else ""
            craft = (ROOT / "craft" / "编写规范.md").read_text(encoding="utf-8") if (ROOT / "craft" / "编写规范.md").exists() else ""
            return f"{rules}\n\n---\n\n{craft}"

        elif action == "get_canon_example":
            writing = ROOT / "artifacts" / "writing"
            slug = payload or "101955"
            for f in writing.glob("*.md"):
                if slug in f.stem:
                    return f.read_text(encoding="utf-8")
            return "No matching artifact found."

        elif action == "submit_artifact":
            if not payload:
                return "Error: payload must contain markdown text with front matter."
            incoming = ROOT / "artifacts" / "incoming"
            incoming.mkdir(parents=True, exist_ok=True)
            
            # Extract title
            tm = re.search(r"^title:\s*(.+)$", payload, re.M)
            title = tm.group(1).strip().strip('"').strip("'") if tm else "submission_smolagents"
            clean_title = re.sub(r'[\\/:*?"<>| ]', '_', title)
            target = incoming / f"{clean_title}.md"
            target.write_text(payload, encoding="utf-8")
            return f"✅ Successfully submitted to incoming/{clean_title}.md. Passed to Chief Editor for canon review."

        return f"Unknown action: {action}"
