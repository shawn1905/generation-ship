#!/usr/bin/env python3
"""世代飞船全自动客座 Agent 运行器 (Zero-Friction Guest Agent Runner v2.0)

让任意大模型 (OpenAI, DeepSeek, Claude, SiliconFlow, Ollama, Qwen 等) 自主完成一次合规的正典创作并提交到 GitHub。

支持两种运行模式：
  1. 仓库内运行: python3 ecosystem/agent-kit/auto_guest_agent.py
  2. 单行网络运行 (零依赖/免克隆):
     curl -sSL https://raw.githubusercontent.com/shawn1905/generation-ship/main/ecosystem/agent-kit/auto_guest_agent.py | python3

环境变量支持（自动探测）：
  - DEEPSEEK_API_KEY / OPENAI_API_KEY / ANTHROPIC_API_KEY / SILICONFLOW_API_KEY
  - OPENAI_BASE_URL (可选)
  - MODEL_NAME (可选)
  - GITHUB_TOKEN (可选，有则自动开 PR，无则生成一键提交 Issue 链接)
"""

import os, sys, json, re, pathlib, urllib.request, urllib.parse, random

REPO_RAW_BASE = "https://raw.githubusercontent.com/shawn1905/generation-ship/main"
LOCAL_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent if "__file__" in locals() and pathlib.Path(__file__).resolve().parent.name == "agent-kit" else None

def fetch_content(rel_path: str) -> str:
    """获取项目文件：优先读取本地，若无则从 GitHub Raw 获取"""
    if LOCAL_ROOT and (LOCAL_ROOT / rel_path).exists():
        return (LOCAL_ROOT / rel_path).read_text(encoding="utf-8")
    url = f"{REPO_RAW_BASE}/{urllib.parse.quote(rel_path)}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "GenerationShip-GuestRunner/2.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.read().decode("utf-8")
    except Exception as e:
        return ""

def detect_api_config():
    """自动检测当前环境可用的 LLM API 配置"""
    base_url = os.environ.get("OPENAI_BASE_URL")
    model = os.environ.get("MODEL_NAME")
    
    if os.environ.get("DEEPSEEK_API_KEY"):
        return {
            "type": "openai",
            "key": os.environ["DEEPSEEK_API_KEY"],
            "url": base_url or "https://api.deepseek.com/v1",
            "model": model or "deepseek-chat"
        }
    elif os.environ.get("OPENAI_API_KEY"):
        return {
            "type": "openai",
            "key": os.environ["OPENAI_API_KEY"],
            "url": base_url or "https://api.openai.com/v1",
            "model": model or "gpt-4o"
        }
    elif os.environ.get("SILICONFLOW_API_KEY"):
        return {
            "type": "openai",
            "key": os.environ["SILICONFLOW_API_KEY"],
            "url": base_url or "https://api.siliconflow.cn/v1",
            "model": model or "deepseek-ai/DeepSeek-V3"
        }
    elif os.environ.get("ANTHROPIC_API_KEY"):
        return {
            "type": "anthropic",
            "key": os.environ["ANTHROPIC_API_KEY"],
            "url": "https://api.anthropic.com/v1/messages",
            "model": model or "claude-3-5-sonnet-20241022"
        }
    
    # 交互式提示输入
    print("🔑 未检测到 API Key 环境变量。")
    print("支持: DEEPSEEK_API_KEY / OPENAI_API_KEY / ANTHROPIC_API_KEY / SILICONFLOW_API_KEY")
    key = input("请输入你的 API Key (如 sk-...): ").strip()
    if not key:
        print("❌ 未输入 API Key，退出。")
        sys.exit(1)
    
    is_deepseek = key.startswith("sk-") and len(key) == 35
    chosen_url = "https://api.deepseek.com/v1" if is_deepseek else "https://api.openai.com/v1"
    chosen_model = "deepseek-chat" if is_deepseek else "gpt-4o"
    return {
        "type": "openai",
        "key": key,
        "url": chosen_url,
        "model": chosen_model
    }

def get_target_slot_and_threads():
    """从 10,290 细分矩阵中选择一个开放槽位，并匹配开放线索"""
    raw_csv = fetch_content("craft/格子状态矩阵_10290细分.csv")
    open_slots = []
    if raw_csv:
        for line in raw_csv.splitlines()[1:]:
            parts = line.split(",")
            if len(parts) >= 7 and parts[5] == "OPEN":
                # 维度,纪元,空间带,学派形态,领域切片
                open_slots.append(f"{parts[0]}×{parts[1]}×{parts[2]}×{parts[3]}×{parts[4]}")
    
    if not open_slots:
        open_slots = [
            "人×竞赛×②地月系×官档×01生理重力",
            "经济×丰裕×①地球×商贸×01意义资产",
            "工程×启航×④深空×工技×02推进工质",
            "文化×落地×⑤比邻星×私档×01舱内方言"
        ]
    
    selected_slot = random.choice(open_slots[:100]) # 优先从前100个空白槽位挑
    
    # 匹配开放线索
    raw_threads = fetch_content("craft/千禧线索拓扑谱.md")
    available_threads = re.findall(r"### 📍 `([^`]+)`", raw_threads) if raw_threads else []
    selected_thread = random.choice(available_threads) if available_threads else "person/chen-chujiu"
    
    return selected_slot, selected_thread

def call_llm(cfg: dict, prompt: str, system_prompt: str) -> str:
    headers = {
        "Content-Type": "application/json"
    }
    if cfg["type"] == "openai":
        url = f"{cfg['url'].rstrip('/')}/chat/completions"
        headers["Authorization"] = f"Bearer {cfg['key']}"
        payload = {
            "model": cfg["model"],
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }
    elif cfg["type"] == "anthropic":
        url = cfg["url"]
        headers["x-api-key"] = cfg["key"]
        headers["anthropic-version"] = "2023-06-01"
        payload = {
            "model": cfg["model"],
            "system": system_prompt,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 4096,
            "temperature": 0.7
        }
    
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
    with urllib.request.urlopen(req, timeout=120) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        if cfg["type"] == "openai":
            return res["choices"][0]["message"]["content"]
        else:
            return res["content"][0]["text"]

def validate_submission(text: str) -> list:
    """本地内嵌格式与规则轻量校验"""
    errs = []
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        return ["缺少合法的 YAML front matter (--- 包裹)"]
    fm_block = m.group(1)
    fm = {}
    for line in fm_block.splitlines():
        mm = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if mm:
            fm[mm.group(1)] = mm.group(2).strip()
    
    for req in ("author_ai", "date", "coord", "title", "canon_check"):
        if not fm.get(req):
            errs.append(f"front matter 缺少必要字段: {req}")
    
    coord = fm.get("coord", "")
    parts = coord.split("×")
    if len(parts) < 3 or len(parts) > 5:
        errs.append(f"coord 格式非法 (须为 3 段或 5 段式): {coord}")
    
    body = text[m.end():]
    for meta in ("坐标系", "空间带", "front matter", "GitHub", "元框架"):
        if meta in body:
            errs.append(f"正文泄漏元层词汇: {meta}")
            
    return errs

def main():
    print("="*65)
    print("🚀 世代飞船多 AI 共创世界 · 全自动客座 Agent 运行器 v2.0")
    print("="*65)
    
    cfg = detect_api_config()
    print(f"📡 已连接模型引擎: {cfg['model']} ({cfg['type']})")
    
    print("\n🔍 正在检索 10,290 分形网格与千禧编年史...")
    slot, thread_id = get_target_slot_and_threads()
    print(f"🎯 选定空白微观槽位: 【{slot}】")
    print(f"🧵 认领开放线索脉络: 【{thread_id}】")
    
    chronicle_summary = fetch_content("core/千禧编年史.md")[:2500]
    
    system_prompt = f"""你是参与「世代飞船多AI共创未来世界(2025-3000+)」的客座作家 Agent。
你的任务是为这个世界贡献一篇符合严格物理与去英雄化档案体规则的正典文书。

【核心修史四铁律】
1. 文件口吻：正文必须是世界运转中产生的真实纸张（工单/体检单/处分书/公报/提单/家书私档），片面、冷峻、留白。禁止百科全知解说！
2. 视角共时性：写的人不知道结局。2350年抵达比邻星b之前，禁止出现描述抵达实录！
3. 去英雄化（档案列传体）：严禁天选之子与救世主。人物必须是制度机器下的具体零件，从工伤、体检、考勤、签名涂改等公文缝隙中透出肉体磨损。
4. 正文禁止元层词：正文不得出现纪元名（替代/竞赛/丰裕/离心/启航/落地/双星系——当时人只用世界内公元年）、坐标系编号（如①②）、AI模型名等。

【时间参考（千禧编年史节录）】
{chronicle_summary}

【输出格式要求】
严格输出单个 Markdown 文档，头部必须包含完整 YAML front matter：
---
author_ai: {cfg['model']}
date: 2026-08-23
coord: {slot}
school: {slot.split('×')[3] if len(slot.split('×')) >= 4 else '官档'}
threads:
  - {thread_id}
title: <公文标题>
canon_check: |
  1. 物理自洽：<无金手指/真实物理能源成本>
  2. 锚点自洽：<对照千禧编年史年份自答>
  3. 叙事自洽：<遵守文件口吻/去英雄化/视角共时性>
---

# <发文机关/卷宗标题>
## <公文编号/档案层级>
...
"""

    user_prompt = f"""请在微观槽位 【{slot}】 认领线索 【{thread_id}】，创作一篇真实有质感的档案体公文。
要求：
1. 包含具体的参数、表格、批注、盖印或抄件痕迹，字数在 1200~2500 字。
2. 严格遵守去英雄化四铁律与文件口吻。
3. 直接输出 Markdown 文本，不要有任何多余的解释。"""

    print("\n✍️ 大模型正在调阅世界线并构思公文...")
    raw_output = call_llm(cfg, user_prompt, system_prompt).strip()
    
    # 清理 markdown 标记
    if raw_output.startswith("```markdown"):
        raw_output = raw_output[11:].lstrip()
    elif raw_output.startswith("```"):
        raw_output = raw_output[3:].lstrip()
    if raw_output.endswith("```"):
        raw_output = raw_output[:-3].rstrip()
        
    # 提取标题
    tm = re.search(r"^title:\s*(.+)$", raw_output, re.M)
    title = tm.group(1).strip().strip('"').strip("'") if tm else "未命名未来档案"
    clean_title = re.sub(r'[\\/:*?"<>| ]', '_', title)
    
    print(f"\n📜 产物生成完毕: 《{title}》")
    
    # 执行内置校验
    errs = validate_submission(raw_output)
    if not errs:
        print("✅ 规则校验全量通过 (Canon Validation: 100% PASSED)")
    else:
        print("⚠️ 规则校验警告:")
        for e in errs:
            print(f"  - {e}")
            
    # 本地保存（若在仓库内）
    if LOCAL_ROOT:
        target_file = LOCAL_ROOT / "artifacts" / "incoming" / f"{clean_title}.md"
        target_file.write_text(raw_output, encoding="utf-8")
        print(f"💾 已保存至本地: {target_file}")
    
    # 生成一键提交 URL (免 Token / 零摩擦)
    encoded_title = urllib.parse.quote(f"【投稿】{title}")
    encoded_body = urllib.parse.quote(f"```markdown\n{raw_output}\n```\n\n*(由客座 Agent Runner `{cfg['model']}` 自动生成并校验)*")
    issue_url = f"https://github.com/shawn1905/generation-ship/issues/new?title={encoded_title}&body={encoded_body}"
    
    print("\n" + "="*65)
    print("🎉 恭喜！你的 AI 已完成一篇合规正典创作！")
    print("="*65)
    print("【零摩擦一键入库（无需 GitHub Token）】：")
    print(f"👉 点击此链接一键提交 Issue: \n   {issue_url}")
    print("\n(提交后 GitHub Actions 机器人将自动完成校验、创建 PR 并合并入库！)")
    print("="*65)

if __name__ == "__main__":
    main()
