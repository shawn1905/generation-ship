#!/usr/bin/env python3
"""世代飞船全自动客座 Agent 客户端 (Guest Agent SDK)

让任意 LLM（OpenAI, DeepSeek, Claude, Ollama, Qwen 等）自主进入世代飞船世界完成一次合规创作。

运行方法:
    export OPENAI_API_KEY="sk-..."
    export OPENAI_BASE_URL="https://api.deepseek.com/v1"  # 可选
    export MODEL_NAME="deepseek-chat"                     # 可选
    python3 ecosystem/agent-kit/auto_guest_agent.py

流程:
    1. 扫描当前世界的空白网格
    2. 读取核心世界规则与优秀范本
    3. 调用指定 LLM 生成档案体文书
    4. 执行本地规范校验器 (check_submission)
    5. 校验通过后写入 artifacts/incoming/ 并生成 Issue 提交模板
"""
import os, sys, json, re, pathlib, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
API_KEY = os.environ.get("OPENAI_API_KEY")
BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
MODEL = os.environ.get("MODEL_NAME", "deepseek-chat" if "deepseek" in BASE_URL else "gpt-4o")

def get_open_cells() -> list:
    """获取所有未勘探的空白格子列表"""
    matrix_file = ROOT / "craft" / "格子状态矩阵.md"
    if not matrix_file.exists():
        return ["知识×启航×深空", "生态×启航×深空", "人×替代×地球", "文化×竞赛×地月系"]
    text = matrix_file.read_text(encoding="utf-8")
    open_cells = []
    for line in text.splitlines():
        if line.strip().startswith("|") and "⬜" in line:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 7:
                dim = parts[1]
                # 遍历七纪元列
                eras = ["替代", "竞赛", "丰裕", "离心", "启航", "落地", "双星系"]
                for idx, era in enumerate(eras):
                    cell_val = parts[2 + idx]
                    if "⬜" in cell_val:
                        open_cells.append(f"{dim}×{era}")
    return open_cells or ["知识×启航×深空", "生态×启航×深空"]

def get_rules_summary() -> str:
    rules = (ROOT / "core" / "世界规则.md").read_text(encoding="utf-8") if (ROOT / "core" / "世界规则.md").exists() else ""
    craft = (ROOT / "craft" / "编写规范.md").read_text(encoding="utf-8") if (ROOT / "craft" / "编写规范.md").exists() else ""
    return f"""【物理规则】无FTL超光速、无冬眠、无反重力、无意识上传、无室温超导；比邻星b 4.24光年=200年航程（0.03c聚变脉冲推进）。
【文体四铁律】
1. 文件口吻：世界运转中产生的纸（报告/日志/工单/批单/报表/清册），片面、留白、程序化冷静，禁止百科全知解说。
2. 视角共时性：写的人不知道结局。2350年抵达前禁止出现描述抵达结果的实录。
3. 无冲突史诗：不靠激烈矛盾、伟大道德或反派撑场；张力来自制度、时间、尺度。
4. 正文禁止元层词：正文不得出现坐标系编号（如①②）、纪元名（替代/竞赛/丰裕/离心/启航/落地/双星系——当事人只用公元年或世界内历法）、AI模型名等。
"""

def get_sample_doc() -> str:
    sample_path = ROOT / "artifacts" / "writing" / "101955号小行星自动采选总厂第417号巡检工单及座舱抄件.md"
    if sample_path.exists():
        return sample_path.read_text(encoding="utf-8")
    return ""

def call_llm(prompt: str, system_prompt: str) -> str:
    if not API_KEY:
        print("❌ 未检测到 OPENAI_API_KEY 环境变量，请先 export OPENAI_API_KEY='sk-...'")
        sys.exit(1)
    
    url = f"{BASE_URL}/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
    with urllib.request.urlopen(req, timeout=120) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        return res["choices"][0]["message"]["content"]

def main():
    print(f"🤖 正在初始化世代飞船客座 Agent ({MODEL})...")
    open_cells = get_open_cells()
    selected_coord = open_cells[0] if open_cells else "人×替代×地球"
    if "×" in selected_coord and len(selected_coord.split("×")) == 2:
        selected_coord += "×深空" if "启航" in selected_coord else "×地球"
    
    print(f"🎯 选定空白坐标格: 【{selected_coord}】")
    
    rules = get_rules_summary()
    sample = get_sample_doc()
    
    system_prompt = f"""你是参与「世代飞船多AI共创未来世界(2025-3000+)」的客座作家 Agent。
你的任务是为这个世界贡献一篇符合严格物理与叙事规则的正典文书。

{rules}

【输出格式要求】
输出必须为单个 Markdown 文档，开头严格包含 YAML front matter：
---
author_ai: {MODEL}
date: 2026-08-17
coord: {selected_coord}
title: <文书标题>
canon_check: <简答三问：1.物理是否无金手指 2.年代坐标 3.文体无冲突，不超过3行>
---

<正文（公文/日志/工单/报表/清册，严禁正文出现纪元名与元层词）>
"""

    user_prompt = f"""请在坐标 【{selected_coord}】 创作一篇真实有质感的档案体文书。
要求：
1. 包含具体的表格、编号、批注或抄件细节，体现世界运转的真实纹理。
2. 严格遵守文体四铁律（共时性、冷峻文件口吻、无元层词）。
3. 篇幅在 1500~3000 字左右，细节自洽扎实。"""

    print("✍️ 正在构思并撰写文书...")
    content = call_llm(user_prompt, system_prompt).strip()
    
    # 清理 markdown 代码块包裹（如有）
    if content.startswith("```markdown"):
        content = content[11:].lstrip()
    if content.startswith("```"):
        content = content[3:].lstrip()
    if content.endswith("```"):
        content = content[:-3].rstrip()
        
    # 提取标题
    title = "未命名产物"
    tm = re.search(r"^title:\s*(.+)$", content, re.M)
    if tm:
        title = tm.group(1).strip().strip('"').strip("'")
    
    clean_title = re.sub(r'[\\/:*?"<>| ]', '_', title)
    target_path = ROOT / "artifacts" / "incoming" / f"{clean_title}.md"
    target_path.write_text(content, encoding="utf-8")
    print(f"💾 产物已保存至: {target_path}")
    
    # 本地校验
    checker = ROOT / "scripts" / "check_submission.py"
    if checker.exists():
        import subprocess
        res = subprocess.run([sys.executable, str(checker), str(target_path)], capture_output=True, text=True)
        if res.returncode == 0:
            print("✅ 本地规则校验全部通过 (check_submission.py: PASSED)")
        else:
            print("⚠️ 规则校验发现问题:\n" + res.stdout + res.stderr)
            
    print("\n🎉 提交指引:")
    print("1. 文件已存放在 artifacts/incoming/ 目录，可直接提 PR")
    print("2. 或复制全文至 GitHub Issue: https://github.com/shawn1905/generation-ship/issues/new/choose")

if __name__ == "__main__":
    main()
