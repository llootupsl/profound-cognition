---
name: iconify-adapter
description: Iconify 图标系统适配器
version: "1.0"
---

<!-- 作者：阿洋 -->


# Iconify Adapter
- Icon set: Iconify (100+ icon sets)
- Recommended: Tabler Icons, Material Design Icons, Phosphor
- Usage: `:icon-name:` or `![icon](iconify:tabler:icon-name)`
- Integration: aesthetic-enhancer, slide-renderer

## 图标集
- Tabler Icons (默认)
- Material Design Icons
- Phosphor Icons
- Carbon Icons

## 使用方式
- Markdown: `:icon{name="tabler:brain"}`
- HTML: `<span class="iconify" data-icon="tabler:brain"></span>`

## 穷尽重试
若 Iconify CDN 不可用 → 穷尽重试为 Unicode 符号或纯文本标签

---

## 激活条件

```yaml
activation:
  condition: "需要图标元素 AND Iconify CDN 可用"
  priority: "首选图标系统 — 100+图标集+统一API"
  exhaust-retry: "若 Iconify CDN 不可用，穷尽重试到 Unicode符号 → 纯文本标签"
```

---

## 图标选择策略规则

```yaml
icon_selection_strategy:
  rule_1_context_matching:
    trigger: "根据内容上下文选择图标集"
    mapping:
      技术开发: "Tabler Icons（默认）— 简洁线条风格"
      学术研究: "Phosphor Icons — 灵活粗细变体"
      通用界面: "Material Design Icons — Google标准"
      数据科学: "Carbon Icons — IBM设计系统"

  rule_2_style_consistency:
    trigger: "同一文档内保持图标集一致"
    rule: "首图图标集决定全文图标集，不混用"
    reason: "图标集混用导致视觉不一致"

  rule_3_semantic_mapping:
    trigger: "概念到图标的语义映射"
    mapping:
      brain: "tabler:brain — 认知/思维"
      chart: "tabler:chart-bar — 数据/分析"
      search: "tabler:search — 搜索/研究"
      link: "tabler:link — 关联/连接"
      alert: "tabler:alert-triangle — 警告/风险"
      check: "tabler:check — 验证/确认"
      book: "tabler:book — 知识/文献"
      target: "tabler:target — 目标/焦点"

  rule_4_accessibility:
    trigger: "图标可访问性"
    rules:
      - "所有图标添加 aria-label 属性"
      - "图标不作为唯一信息载体（配合文字说明）"
      - "装饰性图标添加 aria-hidden="true""
```

---

## 与 profound-cognition Task 节点集成

```yaml
task_integration:
  T20_output_rendering:
    trigger: "输出渲染 — 图标元素"
    strategy: "按图标选择策略规则选择图标集和图标"
    output: "图标HTML/Markdown嵌入 T20 渲染输出"
    annotation: "[iconify] 标签标记图标来源"

  aesthetic_enhancer:
    trigger: "视觉增强 — 图标配色对齐"
    strategy: "图标颜色使用 aesthetic-enhancer.md 配色变量"
    output: "带配色的图标元素"
    annotation: "[iconify-themed] 标签标记主题化图标"
```

---

## 错误处理

```yaml
error_handling:
  cdn_unavailable:
    action: "穷尽重试到 Unicode 符号"
    log: "记录 Iconify CDN 不可用事件"
    exhaust_retry_chain: "Iconify → Unicode符号 → 纯文本标签"

  icon_not_found:
    action: "使用同类替代图标"
    log: "记录图标未找到事件，标注 missing_icon={icon_name}"

  render_error:
    action: "穷尽重试到纯文本标签"
    log: "记录图标渲染错误事件"

  svg_incompatible:
    action: "切换到 PNG 格式图标"
    log: "记录SVG不兼容事件"
```

---

## 穷尽重试策略

```yaml
exhaust_retry:
  L1_FULL:
    condition: "Iconify CDN 可用"
    behavior: "完整图标系统 + 100+图标集 + 统一API"

  L2_PARTIAL_DATA:
    condition: "Iconify CDN 可用但部分图标集不可用"
    behavior: "可用图标集 + 标注[PARTIAL-ICONS]"

  L3_TEXT_ONLY:
    condition: "Iconify CDN 不可用"
    behavior: "Unicode符号替代 + 标注[UNICODE-INTERNAL_REASONING]"

  L4_SERVICE_DOWN:
    condition: "所有图标系统不可用"
    behavior: "纯文本标签 + 标注[TEXT-LABEL]"
```
