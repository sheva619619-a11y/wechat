# 文章结构与排版模板

默认双轨见 [style-guide.md](style-guide.md)。成稿须先定 **B 或 A**，再选对应结构。  
篇幅：B 3500–4500 字；A 4000–5500 字（硬门槛见 style-guide）。

## 一、按轨选结构（栏目只决定选题切口，不决定深浅）

### B · 调查叙事（默认）

1. 对比钩子（反差场景/数字）  
2. 主事实写透（换算、误区、关联公开案例）  
3. 机制升维（概念/对手盘/制度缝隙）  
4. 规则或技术回应  
5. 建设启示嵌叙事（1 小节即可，勿改成能力清单体）  
6. 判断与短句结语  
7. 信息来源列表  

配图 4–6；至少 1 处**数字卡**。

### A · 方案建设（周内约 1 篇）

1. 导读 + 导语  
2. 为何建 / 为何失灵  
3. 目标重塑或总体架构  
4. 核心能力（**≥2 个完整小节**）  
5. 场景优先 / 分步路径 / 误区（择要）  
6. 结语  

可保留节末金句；植入 ≤1。

### 栏目与轨的常见搭配

| 栏目 | 默认轨 | 说明 |
|------|--------|------|
| 安全警示 / 行业观察 | B | 有事件与反差时 |
| 政策速递 | B 或 A | 热点解读用 B；纯体系建设用 A |
| 技术科普 | B 或 A | 原理故事用 B；能力展开用 A |
| 案例洞察 | A 偏多 | 可正面讲猎场一号，仍须写满篇幅 |

## 二、固定文末模块

```
—— 关于我们 ——
羽嘉科技，城市级低空安全解决方案提供商，「猎场一号」警用低空防务智能实战平台研发者。
让低空管理从「被动应对」转向「主动防控」。

免责声明：本文相关信息引自公开渠道（信源见文中标注），仅供行业交流参考，
不构成任何决策依据。如有侵权请联系删除。
```

## 三、HTML 公共约定

- 仅内联样式；无 script / 外链 CSS；无正文 `<h1>`  
- 主色 `#2ea6e6`，强调 `#1f8fd6`，正文 `#3f3f3f`  
- `push_draft.py` 会剥掉遗留 h1  

### B 专用模块示例

```html
<!-- 栏目标签：深度观察 或栏目名 -->
<section style="text-align:center;margin-bottom:18px;">
  <span style="display:inline-block;padding:4px 16px;border:1px solid #2ea6e6;border-radius:999px;color:#2ea6e6;font-size:13px;letter-spacing:2px;">深度观察</span>
</section>

<!-- 对比钩子段落后：数字卡 -->
<section style="margin:20px 0;padding:20px 16px;background:#f2f9fd;border-radius:8px;text-align:center;">
  <p style="margin:0;font-size:36px;font-weight:700;color:#1f8fd6;line-height:1.2;">{关键数字}</p>
  <p style="margin:8px 0 0;font-size:14px;color:#666;">{一行说明}</p>
</section>

<!-- 分节 -->
<section style="margin:32px 0 16px;">
  <p style="margin:0;font-size:18px;font-weight:bold;color:#1f8fd6;">
    <span style="color:#2ea6e6;">一</span>&nbsp;&nbsp;{小标题}
  </p>
  <section style="width:36px;height:3px;background:#2ea6e6;border-radius:2px;margin-top:6px;"></section>
</section>

<p style="margin:0 0 16px;text-align:justify;">{叙事段落，可连续多段写透}</p>

<!-- 结语短句 -->
<p style="margin:8px 0;text-align:center;font-size:16px;font-weight:600;color:#1a1a1a;">{短句一行}</p>

<!-- 信源列表 -->
<section style="margin:28px 0 12px;padding-top:16px;border-top:1px solid #e8e8e8;">
  <p style="margin:0 0 8px;font-size:14px;color:#888;font-weight:600;">信息来源与出处</p>
  <p style="margin:0;font-size:13px;color:#999;line-height:1.7;">{来源1 / 来源2 / …}</p>
</section>
```

### A 专用模块示例

```html
<section style="text-align:center;margin-bottom:18px;">
  <span style="display:inline-block;padding:4px 16px;border:1px solid #2ea6e6;border-radius:999px;color:#2ea6e6;font-size:13px;letter-spacing:2px;">{栏目名}</span>
</section>

<section style="background:#f7f8fa;padding:12px 16px;margin:0 0 20px;border-radius:6px;">
  <p style="margin:0;font-size:14px;color:#666;line-height:1.7;"><strong style="color:#1f8fd6;">导读</strong>　{导读一句}</p>
</section>

<section style="background:#f2f9fd;border-left:4px solid #2ea6e6;padding:12px 16px;margin:0 0 24px;border-radius:0 8px 8px 0;">
  <p style="margin:0 0 8px;font-size:15px;font-weight:700;color:#1f8fd6;">导语：{导语标题}</p>
  <p style="margin:0;font-size:15px;color:#555;">{导语正文}</p>
</section>

<p style="margin:0 0 12px;padding-left:8px;text-align:justify;"><span style="color:#2ea6e6;font-weight:700;">•</span>　<strong>第一，{要点}。</strong>{展开，勿一句带过}</p>

<p style="margin:16px 0 8px;padding:12px 14px;background:#f2f9fd;border-radius:6px;text-align:center;"><strong style="color:#1f8fd6;">{节末金句}</strong></p>
```

文末「关于我们」与免责声明模块同前（两轨共用）。

使用说明：

- 分节用「一、二、三…」  
- 禁止正文重复主标题 `<h1>`  
- 摘要 ≤120 字；选题简报须标注本篇为 **B 或 A** 及预估字数  
