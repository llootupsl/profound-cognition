<!-- 作者：阿洋 -->

# 渲染技术栈概要

## 技术栈分层

> **术语说明（R2-01）**：本文件中的渲染工具链称为「格式适配链」（format adaptation chain），不视为 EXHAUST 模式中的「降级」——从 Typst 到 Markdown 是格式变化，内容完整保留。判定标准：格式变化但内容完整保留 = 允许（格式适配链）；内容深度减少 = 禁止（降级）。

| 层级 | 工具 | 适用场景 | 安装命令 |
|------|------|---------|---------|
| 1 | Typst 0.13+ | 研究报告/学术论文首选排版 | `winget install typst` / `brew install typst` |
| 2 | WeasyPrint | PDF 渲染（Typst 不可用时） | `pip install weasyprint` |
| 3 | Pandoc | 跨格式转换枢纽 | `winget install pandoc` / `brew install pandoc` |
| 4 | HTML+CSS（内嵌） | **穷尽尝试层**：上述工具不可用时使用 | 无需安装，纯文本生成 |
| 5 | Markdown | 穷尽尝试最终方案 | 无需安装 |

## 演示文稿框架（1→3 路由）

| 优先级 | 框架 | 适配器 | 适用场景 | 输出格式 | 交互性 |
|--------|------|--------|---------|---------|--------|
| 首选 | Reveal.js 4.x | `plugins/revealjs-adapter.md` | Web 演示、交互讲座 | HTML | ⭐⭐⭐ |
| 次选 | Slidev | `plugins/slidev-adapter.md` | 开发者演示、代码展示 | HTML/PDF | ⭐⭐ |
| 兜底 | Marp | `plugins/marp-adapter.md` | 快速 Markdown→PPT | PDF/PPTX | ⭐ |

演示文稿穷尽重试链：Reveal.js → Slidev → Marp → 纯 Markdown

## 格式适配链（渲染工具穷尽尝试，R2-01）

当上层工具不可用时，按格式适配链穷尽尝试（格式变化，内容完整保留）：

```
research_report:  Typst → WeasyPrint → Pandoc → HTML（内嵌CSS）→ Markdown → 纯文本
wechat_article:   HTML（内嵌CSS）→ Typst → Pandoc → Markdown → 纯文本
course_material:  Marp → Typst PDF → HTML（内嵌CSS）→ Markdown → 纯文本
```

详细路由矩阵见 [aesthetic-enhancer.md](./aesthetic-enhancer.md)

## HTML 内嵌渲染穷尽尝试层

HTML 模板在 LLM IDE 中 100% 可用（纯文本生成，无需外部工具）。模板位置：`output/html-templates/`

- **research-report.html**：学术研究白皮书排版，包含封面、目录、章节、图表标注、参考文献

→ 详细路由矩阵见 [aesthetic-enhancer.md](./aesthetic-enhancer.md)
→ WeasyPrint 渲染器实现见 [document-renderer.md](./document-renderer.md)

## v3 排版引擎

### 排版引擎选择表

| 引擎 | 版本 | 适用 output_type | 优先级 |
|------|------|-----------------|--------|
| Typst | 0.13+ | research_report | 首选 |
| WeasyPrint | latest | research_report（Typst不可用时穷尽重试） | 备选 |
| Pandoc | latest | research_report | 备选 |
| 纯文本 | — | wechat_article, course_material | 穷尽尝试最终方案 |

详见 knowledge/typography-guide.md

### 字体穷尽尝试链

```
霞鹜文楷 → 未来荧黑 → Glow Sans SC → Source Han Sans SC → Noto Sans CJK SC → SimSun → 系统字体
```

Typst 模板字体声明（详见 `output/typst-templates/`）：
- research-report.typ: `("Glow Sans SC", "Source Han Sans SC", "Noto Sans CJK SC", "SimSun")`
- course-lecture.typ: `("Glow Sans SC", "Source Han Sans SC")`
- wechat-article-export.typ: `("Glow Sans SC", "Source Han Sans SC")`

等宽字体穷尽尝试链：
```
Fragment Mono → JetBrains Mono → Cascadia Code → Consolas → 系统等宽字体
```

### 图生成方案

> **铁律**: 所有图类型必须通过代码生成（SVG / Mermaid / Canvas / CSS），**禁止使用任何 AI 生图 API**（Flux / SD / Qwen-Image / DALL-E / Midjourney）。详见 [illustration-generator.md §0 核心铁律](./illustration-generator.md)。

| 图类型 | 首选工具（代码生成） | 穷尽重试工具（代码生成） | 适配器文件 |
|--------|---------|---------|-----------|
| 框架图 / 概念图 | 内联 SVG（手绘矢量） | Mermaid graph | `plugins/paper-figure-adapter.md` |
| 概念插图 | 内联 SVG（VCA 风格注入） | Mermaid graph + ASCII 兜底 | `plugins/qwen-image-adapter.md`（v2.0 已重构为代码生成图适配器） |
| 数据图表 | Observable Plot + ECharts | 内联 SVG 柱状图/折线图模板 | `output/chart-renderer.md` |
| 思维导图 | Markmap | Mermaid mindmap | `output/mindmap-renderer.md` |
| 知识图谱 | 内联 SVG（d3-force 风格） | Mermaid graph | `plugins/qwen-image-adapter.md` |
| 时间线 | 内联 SVG（时间线模板） | Mermaid timeline | `plugins/qwen-image-adapter.md` |
| 决策路径图 | 内联 SVG（决策树模板） | Mermaid flowchart | `plugins/qwen-image-adapter.md` |

详见 [protocols/illustration-generation-protocol.md §6](protocols/illustration-generation-protocol.md#6-论文框架图生成工作流-paper-framework-figure-generation)