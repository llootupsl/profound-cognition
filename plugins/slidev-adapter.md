---
name: slidev-adapter
description: Slidev 演示适配器
author: 阿洋
tags: [slidev, presentation, adapter, vue]
version: "1.0"
---

<!-- 作者：阿洋 -->


# Slidev Adapter
- Framework: Slidev (Vite-powered)
- Features: Markdown-driven, code highlighting, diagrams, recording
- Theme: Custom or @slidev/theme-seriph

## 适用场景
- 含大量代码片段的演示
- 需要实时编辑前端的演示
- 开发者技术分享

## 输出格式
生成 Slidev 兼容的 markdown 文件（单文件 .slides.md），支持代码高亮和内置图表

## 特性
- 代码高亮：Monaco Editor
- 绘图：内置 Mermaid/PlantUML
- 录制：内置演示录制
- 演讲者模式：Presenter Mode
- 绘图批注：Drawing

## 穷尽重试
若 Slidev 不可用 → 穷尽重试为 Marp

---

## 激活条件

```yaml
activation:
  condition: "slide-renderer 输出格式 == HTML-SLIDES AND Slidev 已安装 AND 含大量代码片段"
  priority: "代码密集型演示首选 — Markdown驱动+Monaco Editor+内置绘图"
  exhaust-retry: "若 Slidev 不可用，穷尽重试到 Marp → Reveal.js → HTML幻灯片 → Markdown大纲"
```

---

## 演示策略选择规则

```yaml
presentation_strategy:
  rule_1_code_heavy:
    trigger: "含大量代码片段的演示"
    engine: "Slidev"
    features: [Monaco Editor代码高亮, 实时编辑, 开发者技术分享]
    reason: "Slidev的Monaco Editor是代码演示的最佳选择"

  rule_2_interactive_demo:
    trigger: "需要实时编辑前端的演示"
    engine: "Slidev"
    features: [实时编辑, 绘图批注, 演讲者模式]
    reason: "Slidev支持实时编辑和交互"

  rule_3_developer_talk:
    trigger: "开发者技术分享"
    engine: "Slidev"
    features: [代码高亮, Mermaid/PlantUML, 录制]
    reason: "Slidev专为开发者演示设计"

  rule_4_non_code:
    trigger: "非代码密集型演示"
    engine: "Marp（首选）或 Reveal.js"
    reason: "非代码演示不需要Monaco Editor，Marp更简洁"
```

---

## 与 profound-cognition Task 节点集成

```yaml
task_integration:
  T20_output_rendering:
    trigger: "输出渲染 — course_material 幻灯片"
    strategy: "按演示策略选择规则选择引擎"
    output: "Slidev .slides.md 文件嵌入 T20 渲染输出"
    annotation: "[slidev] 标签标记Slidev演示"

  T13_cog_synthesize:
    trigger: "认知综合 — 技术内容演示化"
    strategy: "rule_1_code_heavy 或 rule_3_developer_talk"
    output: "技术演示注入综合分析"
    annotation: "[slidev-tech] 标签标记技术演示"
```

---

## 错误处理

```yaml
error_handling:
  slidev_not_installed:
    action: "穷尽重试到 Marp CLI"
    log: "记录 Slidev 不可用事件"
    exhaust_retry_chain: "Slidev → Marp → Reveal.js → HTML幻灯片 → Markdown大纲"

  vite_build_error:
    action: "检查Markdown语法，修正后重试"
    log: "记录Vite构建错误事件"

  theme_not_found:
    action: "使用 @slidev/theme-seriph 默认主题"
    log: "记录主题未找到事件"

  mermaid_render_error:
    action: "穷尽重试到纯文本描述图表"
    log: "记录Mermaid渲染错误事件"
```

---

## 穷尽重试策略

```yaml
exhaust_retry:
  L1_FULL:
    condition: "Slidev 可用 + Vite构建正常"
    behavior: "完整Slidev演示 + Monaco Editor + Mermaid + 录制"

  L2_PARTIAL_DATA:
    condition: "Slidev 可用但部分功能异常"
    behavior: "基础Slidev演示 + 标注[PARTIAL-FEATURE]"

  L3_TEXT_ONLY:
    condition: "Slidev 不可用"
    behavior: "穷尽尝试到 Marp/Reveal.js + 标注[INTERNAL_REASONING-SLIDES]"

  L4_SERVICE_DOWN:
    condition: "所有演示工具不可用"
    behavior: "Markdown大纲 + 标注[MARKDOWN-ONLY]"
```
