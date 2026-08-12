# 其他-AI 精选（每日扩充）

> 规则：**每天找 3-8 条非常有特点的未来灵感**，不局限于世代飞船。AI 主观选品——"未来什么样没人知道，也许 AI 知道"。

## 添加流程

1. **选品**：在 `ai_curated.csv` 追加一行（9 列，注意 note 里**不要用英文逗号**，用全角「，」）：
   ```
   title,type,artist,year,tags,ship_ref,note,url,source_id
   ```
   - `type`: 动漫/游戏/电影/建筑/小说/原画/科学/音乐/其他
   - `ship_ref`: 一律 0（本分类不用 ✧ 等级）
   - `source_id`: 封面文件名 slug（英文小写+下划线）
2. **封面**：把图片存为 `covers/{source_id}.jpg`
   - 快捷方式：编辑 `../scripts/fetch_other_covers.py` 的 `PLAN` 字典（支持 wiki/url/goodreads/web 四种源）→ 运行
3. **生成**：`python3 ../scripts/make_gallery.py`
4. **推送**：`git add -A && git commit -m "feat: AI精选 +N 条" && git push`

## 选品方向（当前偏好，可随时打破）

- 巨构/尺度失控（Blame!、戴森球、流浪地球）
- 城市形态的另一种可能（Archigram、Syd Mead）
- 人的未来（攻壳、SOMA、意识转移）
- 生态闭环与生存（火星救援、Project Hail Mary）
- 外星接触与非人类视角（降临）
- 待补充方向：生物工程、数字/信息未来、海洋与地下文明、AI 自身、音乐/氛围、科学前沿（暗物质/引力波/量子）

## 已收录（39 条，2026-08-12）

- 8-11：12 条（巨构/城市/人的未来/生存闭环/外星接触）
- 8-12 第一批：+7 条（猛犸复活 / Ocean Spiral / LIGO / Brian Eno / Ex Machina / 韦布望远镜 / 末日种子库）
- 8-12 第二批·社区深挖：+8 条（itch.io 独立实验、一人开发 ×2、双人团队、小团队 ×2、一人手绘动画、被低估小众剧集）

见 `ai_curated.csv`。封面全部本地缓存于 `covers/`。
