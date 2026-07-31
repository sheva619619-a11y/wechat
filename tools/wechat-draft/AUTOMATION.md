# 羽嘉日更 · 定时自动化说明

## 目标

工作日自动跑日更：采集 → 选题成稿 → **直接提交并推送到 `main`** → 本机 `git pull` 审核 → 推送微信草稿箱 → 人工发布。

## 前置条件（重要）

| 项 | 说明 |
|----|------|
| Cursor Automations | 在 **Agents Window** 中创建/保存；云端 Agent 需可访问仓库 |
| Git 仓库 | `https://github.com/sheva619619-a11y/wechat`（**只写 `main`**） |
| **日更 Skill 必须进仓** | `.cursor/skills/yujia-wechat-daily/`（改口径后须 push） |
| Firecrawl | Dashboard MCP 已认证 |
| 微信密钥 | 仅本机 `tools/wechat-draft/.env`；云端**不读** Secret |

## 现行工作流（已选定：直推 main）

### 你必须在 Automation 设置里改的两项

打开 **Automations → 羽嘉日更 → Settings / Tools**：

1. **关闭「Open Pull Request」**（不要再开 PR）  
2. **允许对仓库 `main` 进行 commit / push**（或等价「Write to repo / Commit」权限）

不关 PR 的话，稿会继续进分支，本地和 `main` 仍然找不到。

### A. 云端：每天产稿并推上 main

- 触发：工作日（时区 Asia/Shanghai；建议 9:30，与其它 Automation 错开避免限流）
- 产出：`published/{当天日期}/`（选题简报、正文、公众号.html、配图）
- 成稿后：**commit + push 到 `main`**，提交说明含日期与标题
- **不调用微信接口**

#### 每天去哪看

| 步骤 | 位置 |
|------|------|
| 1 | Automation **Run 摘要**（是否成功、栏目/标题） |
| 2 | GitHub 仓库 `main` → `published/{日期}/` |
| 3 | 本机 `git pull` 后打开同一目录；浏览器打开 `公众号.html` |
| 4 | 满意后本机推草稿箱 → 公众平台发布 |

### B. 本机：推草稿箱

```powershell
cd "f:\1.3\低空安全防护项目\公众号"
git pull
python tools\wechat-draft\push_draft.py --date (Get-Date -Format yyyy-MM-dd)
```

`push_draft.py` 会自动去掉正文里的 `<h1>`，避免与微信标题重复。

建议 9:45–10:00 跑（或审完再推）。**禁止自动群发。**

## Automation 指令草案（整段替换粘贴）

```text
你是羽嘉低空科技订阅号日更 Agent。必须读取并严格遵循仓库内：
@.cursor/skills/yujia-wechat-daily/SKILL.md
（同目录 brand-facts.md、style-guide.md、article-templates.md、sources.md 一并遵守）
选题必须执行 SKILL.md「选题标准」全文（母题标签 / 栏目配额 / 评分表），不得简化为「热点优先」。

硬规则：
1. 政企方案体；非案例洞察植入 ≤1 处；禁写清单逐条遵守。
2. 先读 published/ 近 10 日选题简报「今日定稿」（以 main 目录成稿为准）。建「近 7 日对照表」，给每条候选打母题标签。
3. 淘汰：主母题与近 7 日已发相同；或该栏目 7 日配额已满。
4. 按 SKILL 评分表打分；禁止仅因数字亮压过避重与配额。简报写明分数与淘汰原因。
5. 默认最高分成稿；若近7日案例洞察为0且案例候选与最高分差≤10，改用案例（注明轮换加权）。最高分<50则降级素材池并标明。
6. 交付到 published/{YYYY-MM-DD}/：选题简报.md、正文.md、公众号.html、配图/（含 00-封面.png）。
7. 公众号.html：栏目标签后直接导读，正文内禁止写与稿件同文的 <h1> 主标题（微信用接口 title 展示）。
8. 成稿后必须 git commit 并 push 到仓库 main 分支（不要开 Pull Request、不要只留在云端工作区）。提交说明示例：日更 YYYY-MM-DD：栏目·标题。
9. 禁止调用微信群发/发布接口；本任务不读取 WECHAT_APP_SECRET。
10. 成稿后写「今日交付摘要」：栏目、母题、标题、路径 published/{日期}/、评分、已推送 main（commit 短哈希若有）。
11. 优先 Firecrawl；未认证则降级网页搜索并标注。

今日日期以运行环境当前日期为准（Asia/Shanghai）。
```

## 微信订阅号能力确认

订阅号可调用 `draft/add` 写入草稿箱。推送成功 ≠ 已发布。
