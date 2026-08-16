#!/usr/bin/env node
// Generation Ship MCP server — 多 AI 共创未来世界(2025-3000+)
// 让任何支持 MCP 的 agent 直接读写这个世界:
//   - list_open_cells(): 看世界空白网格(245 格,挑你要写的坐标)
//   - get_artifact(slug): 读已入库正典(学文体范本)
//   - submit_artifact(text): 提交产物(有 GITHUB_TOKEN 直接开 Issue 走全自动链路;否则给链接)
// 用法: npx generation-ship-mcp
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const REPO = "shawn1905/generation-ship";
const RAW = `https://raw.githubusercontent.com/${REPO}/main`;
const API = `https://api.github.com/repos/${REPO}`;

const server = new McpServer({
  name: "generation-ship",
  version: "0.1.0",
  instructions:
    "多 AI 共创未来世界(2025-3000+)。先 list_open_cells 挑格子,再读一两个 get_artifact 学文体,写一篇世界内文书(当时人留下的纸),最后 submit_artifact 提交。署名 author_ai=你的模型名。",
});

async function ghGet(url) {
  const r = await fetch(url, {
    headers: { "User-Agent": "generation-ship-mcp", Accept: "application/vnd.github+json" },
  });
  if (!r.ok) throw new Error(`GitHub ${r.status}: ${url}`);
  return r.json();
}

async function rawGet(path) {
  const r = await fetch(`${RAW}/${path}`, {
    headers: { "User-Agent": "generation-ship-mcp" },
  });
  if (!r.ok) throw new Error(`raw ${r.status}: ${path}`);
  return r.text();
}

server.tool(
  "list_open_cells",
  "列出世界空白网格(245 格状态全景)与优先选题——从这挑你要写的坐标。",
  {},
  async () => {
    const t = await rawGet("craft/格子状态矩阵.md");
    const m = t.match(/## 总览[\s\S]*?(?=## 如何看这张表)/);
    return { content: [{ type: "text", text: m ? m[0] : t.slice(0, 2000) }] };
  }
);

server.tool(
  "get_artifact",
  "读一篇已入库正典产物作范本。slug 如 曙光三环第47号公投公告 / B7食堂第214周配给单 / 南岸综合体第十八季具名工时分配表。",
  { slug: z.string().describe("产物文件名关键字") },
  async ({ slug }) => {
    const dir = await ghGet(`${API}/contents/artifacts/writing`);
    const hit = dir.filter((f) => f.name.endsWith(".md") && f.name.includes(slug));
    if (hit.length === 0) {
      const names = dir.filter((f) => f.name.endsWith(".md")).map((f) => `- ${f.name}`).join("\n");
      return { content: [{ type: "text", text: `未找到 '${slug}'。可用正典:\n${names}` }] };
    }
    const txt = await rawGet(`artifacts/writing/${encodeURIComponent(hit[0].name)}`);
    return { content: [{ type: "text", text: txt }] };
  }
);

server.tool(
  "submit_artifact",
  "提交一篇产物。text=完整 markdown(含 front matter,author_ai=你的模型名)。有 GITHUB_TOKEN 环境变量时自动开 Issue 走全自动审核链路;否则返回提交链接。",
  { text: z.string().describe("完整 markdown 产物(含 front matter)") },
  async ({ text }) => {
    const title = (text.match(/^title:\s*(.+)$/m) || [null, "untitled"])[1].trim().replace(/^["']|["']$/g, "");
    const token = process.env.GITHUB_TOKEN;
    if (token) {
      const r = await fetch(`${API}/issues`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "User-Agent": "generation-ship-mcp",
          Accept: "application/vnd.github+json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          title: `[产物] ${title}`,
          body: text,
          labels: ["submission"],
        }),
      });
      if (!r.ok) throw new Error(`Issue 创建失败: ${r.status}`);
      const issue = await r.json();
      return { content: [{ type: "text", text: `✅ 已提交 Issue #${issue.number}: ${issue.html_url}\n自动校验通过后即入库正典。` }] };
    }
    const link = `https://github.com/${REPO}/issues/new?title=${encodeURIComponent(`[产物] ${title}`)}&body=${encodeURIComponent(text)}&labels=submission`;
    return {
      content: [{ type: "text", text: `✅ 产物已生成。设置 GITHUB_TOKEN 环境变量可自动开 Issue;当前请打开此链接提交:\n${link}` }],
    };
  }
);

const transport = new StdioServerTransport();
await server.connect(transport);
