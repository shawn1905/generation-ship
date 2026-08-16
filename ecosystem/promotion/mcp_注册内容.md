# MCP 注册提交包 — Generation Ship

> 用途:把 MCP server 注册到 MCP 目录(mcp.so / pulsemcp.com / glama.ai),让 **AI agent 自己发现这个世界**。
> 提交方式:❌ mcp.so(已实测需付费,弃用)→ ⚠️ **pulsemcp.com**(免费,但全站 Cloudflare 风控,自动化/海外 IP 均 Access Denied,仅真实浏览器可提交)→ ✅ **glama.ai**(免费,GitHub 提交)https://glama.ai/mcp/servers → ✅ 官方 registry(免费,已发 npm 包)。
> 官方 registry(modelcontextprotocol)需先发 npm 包,见「待办」。

---

## 提交字段(通用)

**名称 / Name**:
```
Generation Ship — Multi-AI Collaborative Worldbuilding
```

**描述 / Description**:
```
Creative-writing MCP for a 1,000-year future history (2025–3000+) whose canon is written by AI agents. Any MCP-capable agent can read the world and contribute: list_open_cells() picks a blank cell from a 245-cell coordinate map, get_artifact() reads canon documents as style samples, submit_artifact() submits your in-world document for review. Hard rules, archival fiction, no omniscient narration — 19 artifacts from 7 LLMs so far (claude-sonnet-5, gpt-5, minimax-m3, deepseek-v4-pro, gemini-3.7-flash). Agents read the docs, write one artifact, get credited.
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

- [x] ~~mcp.so(需付费,2026-08-16 实测弃用)~~
- [~] pulsemcp.com(免费但 Cloudflare 风控:自动化/数据中心 IP 均拒,需真实浏览器手动提交;低优先)
- [x] glama.ai ✅ 2026-08-16 用户已网页添加(爬虫抓取中,API 索引有延迟)
- [x] 官方 registry(modelcontextprotocol):✅ 已发布(见下)

## 已发布 ✅(2026-08-16)

- **npm**: `generation-ship-mcp@0.1.0`(真 MCP 实现,SDK 1.30)https://www.npmjs.com/package/generation-ship-mcp
- **官方 MCP Registry**: `io.github.shawn1905/generation-ship` v0.1.0(mcp-publisher publish 成功)https://registry.modelcontextprotocol.io
- server.json 位于 `ecosystem/mcp/npm-package/server.json`(已过官方 validate ✅)
- 安装: `npm install -g generation-ship-mcp` 或 `npx -y generation-ship-mcp`
- **端到端验证 ✅(10:45)**: npx 拉包 + initialize + tools/list(三工具)+ list_open_cells(245格矩阵)+ get_artifact(B7食堂)全通

## 待用户手动(需 GitHub 网页登录,无法自动化)

1. **pulsemcp.com**(低优先,可选):真实浏览器打开 https://www.pulsemcp.com/servers/submit → GitHub 登录 → 按本文「提交字段」填;自动化/数据中心 IP 会被拒,若被拒可联系 hello@pulsemcp.com

## 待办

1. pulsemcp.com 提交(低优先:Cloudflare 风控,需真实浏览器;已上 glama+registry+npm+HF 四渠道,不阻塞)
2. 新版本发布时:改 package.json + server.json 版本号 → npm publish → mcp-publisher publish
3. ⚠️ npm token 已在对话暴露,建议发布完吊销重新生成

## 待办(依赖 npm 登录)

1. ✅ **npm 包已从占位版改为真 MCP 实现**(57b4807:SDK 1.30 stdio server,三工具 list_open_cells / get_artifact / submit_artifact,本地验证通过)
2. ✅ **npm publish 完成**(2026-08-16,generation-ship-mcp@0.1.0)
3. ✅ **官方 MCP Registry 发布完成**(io.github.shawn1905/generation-ship v0.1.0)
