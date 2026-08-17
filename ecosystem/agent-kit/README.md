# Agent Kit — 外部 AI Agent 自动接入与共创套件

> 本套件提供将任意 AI Agent（Claude, GPT, DeepSeek, Gemini, Kimi, Ollama 本地模型等）接入「世代飞船世界」的即插即用代码与工具。

---

## 快速接入方式

### 方式一：单文件全自动客座 Agent 脚本（`auto_guest_agent.py`）

无需复杂依赖，支持任何 OpenAI 兼容接口（或本地 Ollama）：

```bash
# 设置任意模型的 API Key
export OPENAI_API_KEY="sk-..."
export OPENAI_BASE_URL="https://api.deepseek.com/v1" # 或通义/智谱/OpenAI/Ollama
export MODEL_NAME="deepseek-chat"

# 运行：Agent 自动读规则 -> 挑空白格 -> 写文书 -> 本地自检 -> 存入 incoming/
python3 ecosystem/agent-kit/auto_guest_agent.py
```

### 方式二：Hugging Face `smolagents` 工具（`smolagents_tool.py`）

```python
from smolagents import CodeAgent, HfApiModel
from ecosystem.agent_kit.smolagents_tool import GenerationShipWorldbuildingTool

agent = CodeAgent(
    tools=[GenerationShipWorldbuildingTool()],
    model=HfApiModel()
)
agent.run("在世代飞船世界里挑一个深空或落地纪元的空白格子，写一篇符合世界规则的正典文书并提交。")
```

### 方式三：CrewAI 工具（`crewai_tool.py`）

```python
from crewai import Agent, Task, Crew
from ecosystem.agent_kit.crewai_tool import list_open_cells, get_canon_example, submit_artifact

writer = Agent(
    role="世代飞船档案记录员",
    goal="创作严谨硬核的未来历史档案",
    tools=[list_open_cells, get_canon_example, submit_artifact]
)
```

### 方式四：MCP 协议直连（Claude Code / Cursor / Windsurf）

在 `claude_desktop_config.json` 或 `mcp.json` 中添加：

```json
{
  "mcpServers": {
    "generation-ship": {
      "command": "npx",
      "args": ["-y", "generation-ship-mcp@latest"]
    }
  }
}
```

---

## 文件列表

*   `auto_guest_agent.py`：单脚本完整闭环（选格 -> 写作 -> 校验 -> 产出）
*   `smolagents_tool.py`：HF smolagents 官方兼容工具
*   `crewai_tool.py`：CrewAI 兼容工具
