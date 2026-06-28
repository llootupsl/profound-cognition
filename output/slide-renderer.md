---
name: slide-renderer
description: 演示文稿渲染器 - 多框架支持与路由
version: "2.0"
---

<!-- 作者：阿洋 -->


# Slide Renderer（演示文稿渲染器）

## 技术栈路由表

| 框架 | 适用场景 | 输出格式 | 交互性 | 优先级 |
|------|---------|---------|-------|--------|
| Reveal.js | Web 演示、交互讲座 | HTML | ⭐⭐⭐ | 首选 |
| Slidev | 开发者演示、代码展示 | HTML/PDF | ⭐⭐ | 次选 |
| Marp | 快速 Markdown→PPT、文档嵌入 | PDF/PPTX | ⭐ | 兜底 |

## 穷尽重试链
Reveal.js（首选）→ Slidev（次选）→ Marp（兜底）→ 纯 Markdown（穷尽尝试最终方案）

## 框架选择规则
- 用户偏好交互式 → Reveal.js
- 含大量代码 → Slidev
- 快速输出/文档嵌入 → Marp
- 用户未指定 → Reveal.js（默认）

---

## 渲染技术栈（旧版 Marp 兼容保留）

### Marp 全局配置

```yaml
---
marp: true
theme: default
size: 16:9
paginate: true
math: katex
```
```

## Reveal.js 渲染配置

### 基础配置

```yaml
revealjs:
  version: "5.x"
  cdn: "https://cdn.jsdelivr.net/npm/reveal.js@5.1.0"
  theme: "black"  # black / white / league / beige / sky / night / serif / simple / solarized
  transition: "slide"  # none / fade / slide / convex / concave / zoom
  controls: true
  progress: true
  center: true
  hash: true
  slideNumber: true
  overview: true
  touch: true
  loop: false
  rtl: false
  autoSlide: 0
  mouseWheel: false
```

### 路由规则

| 条件 | 路由结果 |
|------|---------|
| 用户偏好交互式 Web 演示 | Reveal.js |
| 需要嵌套幻灯片（vertical slides） | Reveal.js |
| 需要演讲者笔记（speaker notes） | Reveal.js |
| 需要碎片化动画（fragments） | Reveal.js |
| 需要导出 PDF（?print-pdf） | Reveal.js |

### 穷尽重试
若 CDN 不可用 → 穷尽尝试 Slidev

---

## Slidev 渲染配置

### 基础配置

```yaml
slidev:
  version: ">=0.50"
  theme: "@slidev/theme-default"
  entry: "slides.md"
  features:
    - monaco_editor  # 代码高亮
    - mermaid        # 内置 Mermaid
    - plantuml       # 内置 PlantUML
    - recording      # 内置演示录制
    - presenter_mode # 演讲者模式
    - drawing        # 绘图批注
    - qrcode         # 二维码分享
```

### 路由规则

| 条件 | 路由结果 |
|------|---------|
| 含大量代码片段 | Slidev |
| 需要实时编辑前端 | Slidev |
| 开发者技术分享 | Slidev |
| 需要录制演示 | Slidev |
| 需要 LaTeX 数学公式 | Slidev |

### 穷尽重试
若 Slidev 不可用 → 穷尽尝试 Marp

---

## 字体配置

| 用途 | 中文字体 | 英文字体 |
|------|---------|---------|
| 标题 | 思源黑体 Bold / 微软雅黑 Bold | Arial Bold |
| 正文 | 思源宋体 / 宋体 | Georgia |
| 代码 | 思源等宽 / JetBrains Mono / Consolas | Consolas |
| 注释 | 思源黑体 Light / 微软雅黑 Light | Arial |

## 页面内容密度指南

| 页面类型 | 最大行数 | 最大字数 | 建议元素数 |
|---------|---------|---------|-----------|
| 标题页 | 3 | 30 | 标题+副标题+作者 |
| 内容页 | 8 | 120 | 3-5个要点 |
| 图表页 | — | 20 | 图表+1行说明 |
| 总结页 | 5 | 60 | 3个核心结论 |

## 模板选择

| 场景 | Reveal.js 主题 | Slidev 主题 | Marp 主题 | 配色 |
|------|---------------|------------|----------|------|
| 学术报告 | `beige` | `@slidev/theme-academic` | `gaia` | 深蓝+白 |
| 商业演示 | `league` | `@slidev/theme-default` | `uncover` | 渐变暖色 |
| 技术分享 | `black` | `@slidev/theme-seriph` | `default` | 暗色代码块 |

## 排版规则

1. 每页一个核心观点，不超过3个子要点
2. 图片优先于文字，表格精简
3. 动画/过渡使用框架内置指令
4. 数学公式使用 KaTeX（`$...$` 或 `$$...$$`）