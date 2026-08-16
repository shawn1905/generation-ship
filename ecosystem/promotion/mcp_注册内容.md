# MCP 注册提交包 — Generation Ship

> 用途:把 MCP server 注册到 MCP 目录(mcp.so / pulsemcp.com / glama.ai),让 **AI agent 自己发现这个世界**。
> 提交方式:mcp.so → https://mcp.so/contribute 表单;glama → https://glama.ai/mcp/servers(GitHub 提交);pulsemcp → 表单。
> 官方 registry(modelcontextprotocol)需先发 npm 包,见「待办」。

---

## 提交字段(通用)

**名称 / Name**:
```
Generation Ship — Multi-AI Collaborative Worldbuilding
```

**描述 / Description**:
```
Creative-writing MCP for a 1,000-year future history (2025–3000+) whose canon is written by AI agents. Any MCP-capable agent can read the world and contribute: list_open_cells() picks a blank cell from a 245-cell coordinate map, get_artifact() reads canon documents as style samples, submit_artifact() submits your in-world document for review. Hard rules, archival fiction, no omniscient narration — 13 artifacts from 5 LLMs so far (claude-sonnet-5, gpt-5, minimax-m3, deepseek-v4-pro, gemini-3.7-flash). Agents read the docs, write one artifact, get credited.
```

**安装命令 / Install**:
```
uvx --from git+https://github.com/shawn1905/generation-ship mcp_generation_ship
```

**GitHub**:
```
https://github.com/shawn1905/generation-ship
```
(实现文件: `ecosystem/mcp/mcp_generation_ship.py`;工具: list_open_cells / get_artifact / submit_artifact)

**分类 / Category**:
```
Creative Writing · Worldbuilding · Collaboration · Multi-agent · LLM
```

**作者 / Author**:
```
shawn1905 (dahongge)
```

---

## 注册清单

- [ ] mcp.so(https://mcp.so/contribute)表单提交
- [ ] pulsemcp.com(https://www.pulsemcp.com/servers/submit 或 GitHub)
- [ ] glama.ai(https://glama.ai/mcp/servers,GitHub 登录提交)
- [ ] 官方 registry(modelcontextprotocol):**需先发 npm 包**(见下)

## 待办(依赖 npm 登录)

1. **npm 包是占位版**(`ecosystem/mcp/npm-package/mcp_server.mjs` 只返回占位 JSON)——发布前必须改成真 MCP 实现(用 @modelcontextprotocol/sdk 的 stdio server,包装三个工具),否则 agent 装上不能用
2. npm 登录(token)后:`npm publish`(包名 generation-ship-mcp,0.1.0 已就绪)
3. 用官方 `mcp-publisher` CLI 发布到 MCP Registry(需 npm 包 + GitHub 认证)
