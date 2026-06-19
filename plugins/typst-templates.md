<!-- 作者：阿洋 -->

# Typst Templates — 排版模板索引

## 模板清单（7个模板）

| 模板文件 | 用途 | 适用场景 |
|---------|------|---------|
| research-report.typ | 深度研究报告 | research_report |
| wechat-article-export.typ | 公众号PDF导出 | wechat_article |
| course-lecture.typ | 幻灯片式讲义 | course_material (lecture) |
| cover-page.typ | 封面页 | 所有类型 |
| toc-page.typ | 目录页 | research_report |
| dimension-page.typ | 维度页 | research_report |
| appendix-page.typ | 附录页 | research_report |

## Typst CLI 调用方式

```bash
# 编译研究报告
typst compile \
  --root output/typst-templates/ \
  --font-path output/fonts \
  --input title="研究标题" \
  --input subtitle="副标题" \
  research-report.typ output.pdf

# 编译公众号文章
typst compile wechat-article-export.typ output.pdf

# 编译课程讲义
typst compile course-lecture.typ output.pdf
```

## 穷尽尝试策略（Typst不可用时的穷尽重试链路）

1. Typst 不可用 → Pandoc + WeasyPrint（Markdown → PDF）
2. Pandoc 不可用 → HTML内嵌样式（浏览器打印PDF）
3. HTML不可用 → Markdown纯文本
4. 全部不可用 → 纯文本

---

## 激活条件

```yaml
activation:
  condition: "document-renderer 输出格式 == PDF AND Typst 已安装"
  priority: "首选 PDF 排版引擎 — 原生PDF输出+高质量排版"
  exhaust-retry: "若 Typst 不可用，穷尽重试到 WeasyPrint → Pandoc → HTML → Markdown → 纯文本"
```

---

## 模板选择策略规则

```yaml
template_selection_strategy:
  rule_1_product_type:
    research_report:
      templates: [research-report.typ, cover-page.typ, toc-page.typ, dimension-page.typ, appendix-page.typ]
      reason: "研究报告需要完整模板套件"
    wechat_article:
      templates: [wechat-article-export.typ, cover-page.typ]
      reason: "公众号文章需要PDF导出模板"
    course_material:
      templates: [course-lecture.typ, cover-page.typ]
      reason: "课程讲义需要幻灯片式模板"

  rule_2_output_format:
    PDF:
      engine: "Typst（首选）"
      reason: "Typst原生PDF输出质量最高"
    PPTX:
      engine: "Marp CLI"
      reason: "Typst不支持PPTX，需使用Marp"
    HTML:
      engine: "WeasyPrint"
      reason: "Typst不支持HTML，需使用WeasyPrint"

  rule_3_font_availability:
    has_custom_fonts:
      action: "使用 --font-path 指定字体目录"
    no_custom_fonts:
      action: "使用系统默认字体 + 记录警告"
```

---

## 与 profound-cognition Task 节点集成

```yaml
task_integration:
  T20_output_rendering:
    trigger: "输出渲染 — PDF文档排版"
    strategy: "按模板选择策略规则选择模板"
    output: "PDF文件嵌入 T20 渲染输出"
    annotation: "[typst] 标签标记Typst排版"

  T13_cog_synthesize:
    trigger: "认知综合 — 研究报告PDF输出"
    strategy: "rule_1_product_type → research_report"
    output: "研究报告PDF注入综合分析"
    annotation: "[typst-report] 标签标记研究报告PDF"
```

---

## 错误处理

```yaml
error_handling:
  typst_not_installed:
    action: "穷尽重试到 WeasyPrint PDF渲染"
    log: "记录 Typst 不可用事件"
    exhaust_retry_chain: "Typst → WeasyPrint → Pandoc → HTML → Markdown → 纯文本"

  compile_error:
    action: "检查Typst语法错误，修正后重试"
    log: "记录编译错误事件，标注 error_line={line}"

  font_missing:
    action: "使用系统默认字体编译"
    log: "记录字体缺失事件"

  template_not_found:
    action: "使用 research-report.typ 默认模板"
    log: "记录模板未找到事件"

  output_too_large:
    action: "分卷输出（按章节拆分）"
    log: "记录输出过大事件"
```

---

## 穷尽重试策略

```yaml
exhaust_retry:
  L1_FULL:
    condition: "Typst 可用 + 自定义字体可用"
    behavior: "完整Typst排版 + 自定义字体 + 高质量PDF"

  L2_PARTIAL_DATA:
    condition: "Typst 可用但自定义字体缺失"
    behavior: "Typst排版 + 系统默认字体 + 标注[SYSTEM-FONT]"

  L3_TEXT_ONLY:
    condition: "Typst 不可用"
    behavior: "穷尽尝试到 WeasyPrint/Pandoc PDF + 标注[INTERNAL_REASONING-PDF]"

  L4_SERVICE_DOWN:
    condition: "所有PDF渲染工具不可用"
    behavior: "HTML/Markdown纯文本 + 标注[TEXT-ONLY]"
```
