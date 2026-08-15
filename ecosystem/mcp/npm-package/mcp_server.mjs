#!/usr/bin/env node
// Generation Ship MCP server — npm 发行版
// 说明:完整实现见仓库根 mcp_generation_ship.py(fastmcp/Python)。
// npm 版为瘦包装:拉取仓库最新 incoming/ 状态 + 提交入口,保持与主仓库同步。
// 用法: npx generation-ship-mcp
import { createServer } from 'node:http';

const REPO_API = 'https://api.github.com/repos/shawn1905/generation-ship';
console.error('[generation-ship-mcp] 简易版:完整 MCP 实现请用仓库内 Python 版 (uvx --from git+... 或 pip install)。');
console.error('[generation-ship-mcp] 在线文档: https://github.com/shawn1905/generation-ship');

const server = createServer((req, res) => {
  res.writeHead(200, { 'content-type': 'application/json' });
  res.end(JSON.stringify({
    ok: true,
    message: 'Generation Ship MCP (npm 占位版)。真实实现:仓库内 mcp_generation_ship.py — list_open_cells / get_artifact / submit_artifact',
    repo: 'https://github.com/shawn1905/generation-ship',
  }));
});
server.listen(0, () => console.error('[generation-ship-mcp] 已启动(占位,仅自检)'));
