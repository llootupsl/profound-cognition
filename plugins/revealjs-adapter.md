---
name: revealjs-adapter
description: Reveal.js 演示适配器
author: 阿洋
tags: [revealjs, presentation, adapter, html]
version: "1.0"
---

<!-- 作者：阿洋 -->


# Reveal.js Adapter
- Framework: Reveal.js 4.x
- Slide format: Horizontal slides, vertical sub-slides
- Features: Fragments, transitions, speaker notes, PDF export
- Theme: Custom profound-cognition theme

## 渲染模式
- 独立 HTML：引入 CDN Reveal.js，离线可用
- 嵌入部署：生成 &lt;section&gt; 片段嵌入已有 Reveal.js 项目

## 幻灯片模板
每张幻灯片包含：
- 标题（h2/h3）
- 要点（3-5 bullet points + 动画标注）
- 视觉元素（图表代码/图片链接/ASCII 图示）

## 动画标注
- `<!-- .element: class="fragment" -->` → 逐条显示
- `<!-- .element: class="fragment fade-in" -->` → 淡入
- `data-background-color="#hex"` → 背景色分段

## 穷尽重试
若 CDN 不可用 → 穷尽重试为 Slidev

---

## 激活条件

```yaml
activation:
  condition: "slide-renderer 输出格式 == HTML-SLIDES AND Reveal.js CDN 可用 AND 需要动画/过渡效果"
  priority: "动画密集型演示首选 — Fragments+Transitions+PDF导出"
  exhaust-retry: "若 Reveal.js CDN 不可用，穷尽重试到 Slidev → Marp → HTML幻灯片 → Markdown大纲"
```

---

## 演示策略选择规则

```yaml
presentation_strategy:
  rule_1_animation_heavy:
    trigger: "需要复杂动画/过渡效果的演示"
    engine: "Reveal.js"
    features: [Fragments逐条显示, Transitions过渡, 垂直子幻灯片]
    reason: "Reveal.js的动画系统最丰富"

  rule_2_interactive_html:
    trigger: "需要嵌入HTML交互内容的演示"
    engine: "Reveal.js"
    features: [独立HTML输出, 嵌入部署, 自定义主题]
    reason: "Reveal.js支持独立HTML和嵌入部署"

  rule_3_pdf_export:
    trigger: "需要从幻灯片导出PDF"
    engine: "Reveal.js"
    features: [PDF export, Print to PDF]
    reason: "Reveal.js内置PDF导出功能"

  rule_4_simple_slides:
    trigger: "简单幻灯片（无动画需求）"
    engine: "Marp（首选）"
    reason: "简单幻灯片不需要Reveal.js的复杂功能"
```

---

## 动画标注策略

```yaml
animation_strategy:
  fragment_reveal:
    trigger: "要点逐条显示"
    annotation: "<!-- .element: class="fragment" -->"
    reason: "Fragment是最常用的逐条显示动画"

  fade_in:
    trigger: "内容淡入效果"
    annotation: "<!-- .element: class="fragment fade-in" -->"
    reason: "淡入适合强调性内容"

  background_segmentation:
    trigger: "背景色分段（区分不同主题区域）"
    annotation: "data-background-color="#hex""
    reason: "背景色分段适合主题切换"

  speaker_notes:
    trigger: "演讲者备注"
    annotation: "<aside class="notes">备注内容</aside>"
    reason: "演讲者备注辅助演讲"
```

---

## 与 profound-cognition Task 节点集成

```yaml
task_integration:
  T20_output_rendering:
    trigger: "输出渲染 — course_material 动画演示"
    strategy: "按演示策略选择规则选择引擎"
    output: "Reveal.js HTML文件嵌入 T20 渲染输出"
    annotation: "[revealjs] 标签标记Reveal.js演示"

  T13_cog_synthesize:
    trigger: "认知综合 — 交互式内容演示化"
    strategy: "rule_2_interactive_html"
    output: "交互式演示注入综合分析"
    annotation: "[revealjs-interactive] 标签标记交互式演示"
```

---

## 错误处理

```yaml
error_handling:
  cdn_unavailable:
    action: "穷尽重试到 Slidev"
    log: "记录 Reveal.js CDN 不可用事件"
    exhaust_retry_chain: "Reveal.js → Slidev → Marp → HTML幻灯片 → Markdown大纲"

  theme_error:
    action: "使用 Reveal.js 默认主题"
    log: "记录主题错误事件"

  render_error:
    action: "穷尽重试到 Marp CLI"
    log: "记录渲染错误事件"

  fragment_error:
    action: "移除动画标注，使用静态幻灯片"
    log: "记录Fragment错误事件"
```

---

## 穷尽重试策略

```yaml
exhaust_retry:
  L1_FULL:
    condition: "Reveal.js CDN 可用"
    behavior: "完整Reveal.js演示 + Fragments + Transitions + PDF导出"

  L2_PARTIAL_DATA:
    condition: "Reveal.js CDN 可用但部分功能异常"
    behavior: "基础Reveal.js演示 + 标注[PARTIAL-FEATURE]"

  L3_TEXT_ONLY:
    condition: "Reveal.js CDN 不可用"
    behavior: "穷尽尝试到 Slidev/Marp + 标注[INTERNAL_REASONING-SLIDES]"

  L4_SERVICE_DOWN:
    condition: "所有演示工具不可用"
    behavior: "Markdown大纲 + 标注[MARKDOWN-ONLY]"
```
