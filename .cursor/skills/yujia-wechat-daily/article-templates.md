# 文章结构与排版模板

默认文风见 [style-guide.md](style-guide.md)（政企方案体）。成稿与 HTML 均按该风格执行。

## 一、各栏目正文结构

通用要求：正文 1200–2000 字；段落 ≤4 行；采用「导读 / 导语 / 一、二、三… / 结语」；**每节末尾必须有一句加粗收束金句**。

### 政策速递

1. 导读：读者对象 + 本文范围
2. 导语：政策名 + 生效时间 + 短问句加压 + 一句话影响判断
3. 一、政策改了什么（3–5 点，第一/第二/第三）
4. 二、对监管方 / 运营方 / 设备方分别意味着什么
5. 三、行业气氛或关联动态（可选，不作法律依据）
6. 四、落地视角（植入位）：闭环能力 → 一句带出「察控打评」或猎场一号
7. 结语：从「要不要管」收到「怎么常态化管、闭环管」

### 安全警示

1. 导语：场景破题（仅官方确认事实）+ 短问句（看得见？管得住？追得回？）
2. 一、事件要素还原（注明信源）
3. 二、为何会失灵（技术 / 管理 / 流程）
4. 三、防护启示与闭环能力（植入位：方法论，可不点产品名）
5. 结语：安全提醒金句

### 技术科普

1. 导语：一个具体实战问题切入
2. 一、原理用大白话拆开（可插图占位）
3. 二、主流路线对比（不点名竞品厂商）
4. 三、实战落地要注意什么（植入位：多源融合等自家路线用「业内做法」口吻）
5. 结语：一句能力收束

### 行业观察

1. 导语：数据或事件切入
2. 一至三、观察点拆解（每节有金句）
3. 结语：明确判断句
4. 通常不植入

### 案例洞察

1. 导语：场景与挑战（人流量、空域、安保要求）
2. 一至四、按「察 → 控 → 打 → 评」展开
3. 效果与复盘（只用可公开口径）
4. 本栏目可正面介绍猎场一号，仍禁客户内部信息与点位
5. 结语：闭环金句

## 二、固定文末模块

每篇文章末尾依次追加：

```
—— 关于我们 ——
羽嘉科技，城市级低空安全解决方案提供商，「猎场一号」警用低空防务智能实战平台研发者。
让低空管理从「被动应对」转向「主动防控」。

免责声明：本文相关信息引自公开渠道（信源见文中标注），仅供行业交流参考，
不构成任何决策依据。如有侵权请联系删除。
```

## 三、公众号排版 HTML 模板

公众号编辑器只保留内联样式，禁止 `<script>`、外链 CSS、`position` 定位。生成完整 HTML 文件，用户浏览器打开后全选复制粘贴。

配色（源自品牌视觉）：主色 `#2ea6e6`（青蓝），强调 `#1f8fd6`，正文 `#3f3f3f`，辅助灰 `#888888`。

完整样例见工作区 `published/2026-07-17/公众号-参考风格.html`。结构模块如下：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="utf-8"><title>{标题}</title></head>
<body style="margin:0;padding:24px;background:#fff;">
<section style="max-width:677px;margin:0 auto;font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif;font-size:16px;color:#3f3f3f;line-height:1.75;letter-spacing:.5px;">

  <!-- 栏目标签 -->
  <section style="text-align:center;margin-bottom:18px;">
    <span style="display:inline-block;padding:4px 16px;border:1px solid #2ea6e6;border-radius:999px;color:#2ea6e6;font-size:13px;letter-spacing:2px;">{栏目名}</span>
  </section>

  <!-- 不要写 h1 主标题：微信草稿箱用接口 title 展示标题，正文再写会重复。标题只放 <title> 与正文.md「标题备选」。 -->

  <!-- 导读 -->
  <section style="background:#f7f8fa;padding:12px 16px;margin:0 0 20px;border-radius:6px;">
    <p style="margin:0;font-size:14px;color:#666;line-height:1.7;"><strong style="color:#1f8fd6;">导读</strong>　{导读一句}</p>
  </section>

  <!-- 导语 -->
  <section style="background:#f2f9fd;border-left:4px solid #2ea6e6;padding:12px 16px;margin:0 0 24px;border-radius:0 8px 8px 0;">
    <p style="margin:0 0 8px;font-size:15px;font-weight:700;color:#1f8fd6;">导语：{导语标题}</p>
    <p style="margin:0;font-size:15px;color:#555;">{摘要或导语正文}</p>
  </section>

  <!-- 正文段落 -->
  <p style="margin:0 0 16px;text-align:justify;">{段落}</p>

  <!-- 短问句加压 -->
  <p style="margin:0 0 16px;text-align:justify;color:#1f8fd6;font-weight:600;">{问句？问句？}</p>

  <!-- 分节小标题（一、二、三…） -->
  <section style="margin:32px 0 16px;">
    <p style="margin:0;font-size:18px;font-weight:bold;color:#1f8fd6;">
      <span style="color:#2ea6e6;">一</span>&nbsp;&nbsp;{小标题}
    </p>
    <section style="width:36px;height:3px;background:#2ea6e6;border-radius:2px;margin-top:6px;"></section>
  </section>

  <!-- 分点 -->
  <p style="margin:0 0 12px;padding-left:8px;text-align:justify;"><span style="color:#2ea6e6;font-weight:700;">•</span>　<strong>第一，{要点}。</strong>{展开}</p>

  <!-- 节末金句 -->
  <p style="margin:16px 0 8px;padding:12px 14px;background:#f2f9fd;border-radius:6px;text-align:center;"><strong style="color:#1f8fd6;">{节末金句}</strong></p>

  <!-- 信源 -->
  <p style="margin:16px 0;font-size:14px;color:#888;">— 据{信源}，{日期}</p>

  <!-- [图片占位：说明] -->

  <!-- 植入块（≤1） -->
  <section style="background:#f2f9fd;padding:14px 16px;margin:16px 0 24px;border-radius:8px;">
    <p style="margin:0;text-align:justify;">{植入句}</p>
  </section>

  <!-- 文末关于我们 -->
  <section style="margin-top:40px;padding:18px 16px;background:#f7f8fa;border-radius:8px;text-align:center;">
    <p style="margin:0 0 8px;font-size:14px;color:#2ea6e6;letter-spacing:3px;">—— 关于我们 ——</p>
    <p style="margin:0;font-size:14px;color:#666;line-height:1.8;">羽嘉科技，城市级低空安全解决方案提供商，<br>「猎场一号」警用低空防务智能实战平台研发者。<br><strong style="color:#1f8fd6;">让低空管理从「被动应对」转向「主动防控」。</strong></p>
  </section>

  <p style="margin:20px 0 0;font-size:12px;color:#b0b0b0;text-align:center;">免责声明：本文相关信息引自公开渠道（信源见文中标注），仅供行业交流参考，不构成任何决策依据。如有侵权请联系删除。</p>

</section>
</body>
</html>
```

使用说明：

- 分节用「一、二、三…」，不用 01/02（与政企方案体一致）。
- **禁止**在正文 HTML 写与稿件同文的 `<h1>` 主标题（栏目标签后直接导读）；`push_draft.py` 推送时也会剥掉遗留 h1。
- 需要配图处插入 `<!-- [图片占位：说明] -->`；图片须在公众号后台上传。
- 摘要（公众号「摘要」栏）单独给出，≤120 字。
