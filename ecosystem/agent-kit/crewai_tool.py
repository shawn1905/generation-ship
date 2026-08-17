"""CrewAI 工具集成 — 世代飞船多 AI 共创世界

用法:
    from crewai import Agent, Task, Crew
    from ecosystem.agent_kit.crewai_tool import list_open_cells, get_canon_example, submit_artifact

    writer = Agent(
        role="世代飞船档案记录员",
        goal="创作严谨硬核的未来历史档案",
        backstory="你是一名专注于严谨物理、冷峻档案体公文风格的科幻档案员。",
        tools=[list_open_cells, get_canon_example, submit_artifact],
        verbose=True
    )
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent

def list_open_cells() -> str:
    """List open coordinates and vacant cells across the 245-cell worldbuilding grid."""
    matrix = ROOT / "craft" / "格子状态矩阵.md"
    if matrix.exists():
        t = matrix.read_text(encoding="utf-8")
        m = re.search(r"## 总览.*?(?=## 如何看这张表)", t, re.S)
        return m.group(0) if m else t[:1500]
    return "Open coordinates across 7 Eras x 5 Zones x 7 Dimensions."

def get_canon_example(slug: str = "101955") -> str:
    """Read a canonical in-world document example to learn the archival tone and format."""
    writing = ROOT / "artifacts" / "writing"
    for f in writing.glob("*.md"):
        if slug in f.stem:
            return f.read_text(encoding="utf-8")
    return "Sample document not found."

def submit_artifact(text: str) -> str:
    """Submit a newly written in-world artifact (markdown with front matter) to incoming/ directory."""
    incoming = ROOT / "artifacts" / "incoming"
    incoming.mkdir(parents=True, exist_ok=True)
    tm = re.search(r"^title:\s*(.+)$", text, re.M)
    title = tm.group(1).strip().strip('"').strip("'") if tm else "submission_crewai"
    clean_title = re.sub(r'[\\/:*?"<>| ]', '_', title)
    target = incoming / f"{clean_title}.md"
    target.write_text(text, encoding="utf-8")
    return f"✅ Successfully submitted {clean_title}.md to incoming/ for review."
