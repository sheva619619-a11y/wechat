# 羽嘉日更 · 定时自动化说明

## 目标

工作日 **09:30（北京时间）** 自动跑日更：采集 → 选题（默认按推荐直接成稿）→ 正文/HTML/配图 →（可选）推送微信草稿箱 → 人工复核发布。

## 前置条件（重要）

| 项 | 说明 |
|----|------|
| Cursor Automations | 在 **Agents Window** 中创建/保存；云端 Agent 需可访问仓库 |
| Git 仓库 | 当前 `公众号` 目录**还不是 git 仓库**。云端定时任务通常要 check out 远程仓库——请先把本目录纳入已有仓库并 push，或单独建仓 |
| Firecrawl | 日更采集依赖 Firecrawl。若 Automations 里用不了本机 `user-firecrawl-mcp`，请在 [cursor.com](https://cursor.com) 把 Firecrawl 配成 **Dashboard MCP**，或在指令里允许用网页搜索作降级 |
| 微信密钥 | `tools/wechat-draft/.env` 仅存本机；**不要**把 AppSecret 写进 Automation 指令正文。云端推草稿需改用 Cursor Secrets / 本机计划任务调脚本 |

## 推荐架构（两段）

### A. 云端：每天产稿（Cursor Automation）

- 触发：工作日 9:30（cron `30 9 * * 1-5`，时区在编辑器按北京时间确认）
- 指令：严格遵循 `yujia-wechat-daily` skill；默认按推荐选题成稿，不在聊天里等待确认
- 产出：写入仓库 `published/{当天日期}/`
- **本阶段不调用微信接口**（避免密钥进云）

### B. 本机：推草稿箱（Windows 计划任务或收工脚本）

产稿进仓库/同步到本机后执行：

```powershell
cd "f:\1.3\低空安全防护项目\公众号"
python tools\wechat-draft\push_draft.py --date (Get-Date -Format yyyy-MM-dd)
```

或每天 10:00 计划任务跑上述命令（给人工留半小时审本地稿再推，也可 9:45 紧接推送）。

## Automation 指令草案（粘贴用）

```text
你是羽嘉低空科技订阅号日更 Agent。严格按用户 skill「yujia-wechat-daily」执行今日日更（含 brand-facts、style-guide、article-templates）。

硬规则：
1. 政企方案体；非案例洞察植入 ≤1 处；禁写清单逐条遵守。
2. 同题材 7 天内不重复；参考 published/ 近 7 日选题简报避重。
3. 默认：采集后给出 2–3 候选，但直接采用推荐选题成稿（无需等待人工确认），除非无可用信源。
4. 交付到 published/{YYYY-MM-DD}/：选题简报.md、正文.md、公众号.html、配图/（含 00-封面.png）。
5. 禁止调用微信群发/发布接口；本任务不读取 WECHAT_APP_SECRET。
6. 成稿后用简短中文写一份「今日交付摘要」（栏目、标题、路径）。

今日日期以运行环境当前日期为准（Asia/Shanghai）。
```

## 微信订阅号能力确认

官方文档：订阅号（公众号）可调用 `draft/add` 写入草稿箱。推送成功 ≠ 已发布。
