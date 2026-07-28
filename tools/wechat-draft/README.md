# 微信公众号草稿箱推送（订阅号可用）

将本地日更产物（`公众号.html` + 封面/配图）写入**微信公众平台草稿箱**。  
**不自动群发、不自动发布**——推送成功后仍需你在后台复核后点发布。

官方接口：[`draft/add`](https://developers.weixin.qq.com/doc/subscription/api/draftbox/draftmanage/api_draft_add.html)（公众号/订阅号 ✔ · 服务号 ✔）

## 你需要准备

1. 登录 [微信公众平台](https://mp.weixin.qq.com) → 开发 → 基本配置  
2. 记录 **AppID**、**AppSecret**（重置后旧密钥失效）  
3. IP 白名单：把运行本脚本的服务器/本机公网 IP 加进白名单  
4. 复制环境变量模板：

```powershell
copy tools\wechat-draft\.env.example tools\wechat-draft\.env
# 编辑 .env 填入 WECHAT_APP_ID / WECHAT_APP_SECRET
```

`.env` 已在 `.gitignore` 中，**禁止提交仓库**。

## 用法

在 `公众号` 目录下：

```powershell
# 推送指定日期目录（默认读 published\YYYY-MM-DD\）
python tools\wechat-draft\push_draft.py --date 2026-07-28

# 试跑：只校验文件与登录，不真正写入草稿
python tools\wechat-draft\push_draft.py --date 2026-07-28 --dry-run
```

成功时打印 `media_id`，可到公众平台 → 草稿箱查看。

## 流程说明

1. 用 AppID/Secret 换 `access_token`  
2. 上传封面为永久素材 → `thumb_media_id`  
3. 正文 HTML 内本地图片 → 调用「上传图文消息内图片」换微信 CDN URL  
4. `draft/add` 写入草稿（标题/作者/摘要/正文/封面）  
5. **停止**。不调用 `freepublish` / 群发接口  

## 限制与注意

| 项 | 说明 |
|----|------|
| 标题 | ≤32 字（脚本会截断并警告） |
| 摘要 | ≤120 字 |
| 正文图 | 必须先换微信 URL，外链图会被过滤 |
| 权限 | 未认证订阅号可能拿不到部分接口；若报错按公众平台提示开通/认证 |
| 合规 | 推草稿 ≠ 已发布；涉及时政/安全评述仍须人工终审 |

## 与日更自动化的关系

定时 Agent 产完 `published/{日期}/` 后，可追加一步：

```text
python tools/wechat-draft/push_draft.py --date {今天}
```

密钥仅存在本机 `.env` 或 Cursor 密钥库，不要写进 skill / 聊天记录。
