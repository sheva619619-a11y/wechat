# 羽嘉日更 · 定时自动化说明

## 目标

工作日自动跑日更：采集 → 按 **4B:1A** 选题成稿（默认调查叙事、写满篇幅）→ **commit + push `main`** → 本机审核 → 推微信草稿箱 → 人工发布。

文风与篇幅见仓库 `.cursor/skills/yujia-wechat-daily/style-guide.md`（B 3500–4500 字；A 4000–5500 字）。

## 前置条件

| 项 | 说明 |
|----|------|
| Cursor Automations | Agents Window；可写仓库 `main` |
| 关闭 Open Pull Request | 必须关，否则稿不进 main |
| Skill 在仓内 | `.cursor/skills/yujia-wechat-daily/` |
| Firecrawl | Dashboard MCP 已认证 |
| 微信密钥 | 仅本机 `.env`；云端不读 |

## 每天去哪看

1. Run 摘要（栏目、**B/A**、标题、字数）  
2. GitHub `main` → `published/{日期}/`  
3. 本机 `git pull` → 审 HTML  
4. `python tools/wechat-draft/push_draft.py --date 今天`  

## Automation 指令草案（整段替换）

```text
你是羽嘉低空科技订阅号日更 Agent。必须读取并严格遵循：
@.cursor/skills/yujia-wechat-daily/SKILL.md
@.cursor/skills/yujia-wechat-daily/style-guide.md
@.cursor/skills/yujia-wechat-daily/article-templates.md
@.cursor/skills/yujia-wechat-daily/reference-samples.md
（brand-facts.md、sources.md 一并遵守）

战略：先获量再触达特定读者。默认 B 调查叙事；滚动 7 日约 4B:1A。禁止再交 1200–2000 字浅稿。

硬规则：
1. 禁写清单逐条遵守；非案例洞察植入 ≤1。
2. 读 published/ 近 10 日定稿；建对照表 + 近 7 日 B/A 计数与母题标签。
3. 母题 7 日不重复；栏目配额按 SKILL；近 7 日 A=0 且 B≥3 时今日优先合格 A。
4. 荐 B 须满足深度门槛（反差事实 + 三层分析 + 信源≥2）；否则不硬写浅 B。
5. 篇幅：B 正文 3500–4500 字（<3200 不合格重写）；A 4000–5500 字（<3800 不合格重写）。对照 reference-samples 密度。
6. B 结构：对比钩子→事实写透→机制→规则/技术→建设启示嵌叙事→判断→短句结语；含数字卡；无正文 h1。
7. A 结构：导读导语+多节；至少 2 个能力/路径完整小节；可节末金句。
8. 交付 published/{YYYY-MM-DD}/：选题简报（标 B/A 与字数）、正文.md、公众号.html、配图/。
9. 成稿后 git commit 并 push 到 main（不要 Open PR）。说明：日更 YYYY-MM-DD：B|A·标题。
10. 禁止微信群发/读 WECHAT_APP_SECRET。
11. 交付摘要含：栏目、轨(B/A)、标题、字数、路径、评分、main commit。
12. 优先 Firecrawl；未认证则降级并标注。

今日日期以 Asia/Shanghai 为准。
```

## 本机推草稿

```powershell
cd "f:\1.3\低空安全防护项目\公众号"
git pull
python tools\wechat-draft\push_draft.py --date (Get-Date -Format yyyy-MM-dd)
```

`push_draft.py` 会去掉正文 `<h1>`。禁止自动群发。
