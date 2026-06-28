---
name: bmmd-adapter
description: 内置公众号排版系统适配器 — 14种排版样式映射，支持微信公众号一键复制格式
author: 阿洋
tags: [wechat, formatting, adapter, typography]
---

<!-- 作者：阿洋 -->

# 内置公众号排版系统 Adapter — 公众号排版助手

## 适配器配置
- role: 内置公众号排版系统 公众号排版助手
- activation: output_type == 'wechat_article'
- description: 14种排版样式映射，支持微信公众号一键复制格式

## 14种排版样式映射
| 样式ID | 样式名称 | 适用场景 | 公众号对应 |
|--------|---------|---------|-----------|
| STYLE_01 | 正文段落 | 标准正文 | 默认字号+行距 |
| STYLE_02 | 小标题 | 二级标题 | 加粗+居中 |
| STYLE_03 | 引用块 | 引用内容 | 左边框+灰色背景 |
| STYLE_04 | 列表项 | 要点罗列 | 圆点+缩进 |
| STYLE_05 | 编号列表 | 步骤说明 | 数字+缩进 |
| STYLE_06 | 代码块 | 技术内容 | 等宽字体+灰色背景 |
| STYLE_07 | 图片说明 | 图注文字 | 小字+居中+灰色 |
| STYLE_08 | 分割线 | 内容分隔 | 装饰线 |
| STYLE_09 | 强调文字 | 重点内容 | 加粗+着色 |
| STYLE_10 | 链接样式 | 超链接 | 蓝色+下划线 |
| STYLE_11 | 脚注 | 补充说明 | 小字+灰色 |
| STYLE_12 | 高亮块 | 核心观点 | 彩色背景+边框 |
| STYLE_13 | 折叠块 | 展开内容 | 可折叠区域 |
| STYLE_14 | 签名区 | 文末签名 | 右对齐+个性化 |

## 微信公众号一键复制格式
输出格式：HTML内联样式（符合微信公众号支持的HTML标签）
- 支持的标签：section, div, p, span, strong, em, a, img, br, h1-h6, blockquote, ul, ol, li
- 不支持的标签：iframe, script, style, form, input, button
- 样式限制：仅内联样式，不支持外部CSS和class/id选择器

---

## 激活条件

```yaml
activation:
  condition: "output_type == 'wechat_article' AND 需要14种基础排版样式"
  priority: "基础公众号排版 — 14种样式映射+一键复制"
  exhaust-retry: "若 bmmd 排版不可用，穷尽尝试到纯HTML内联样式 → Markdown纯文本"
```

---

## 样式选择策略规则

```yaml
style_selection_strategy:
  rule_1_content_type_matching:
    trigger: "根据内容类型选择排版样式"
    mapping:
      paragraph: "STYLE_01 正文段落"
      heading: "STYLE_02 小标题"
      quote: "STYLE_03 引用块"
      list: "STYLE_04 列表项"
      numbered_list: "STYLE_05 编号列表"
      code: "STYLE_06 代码块"
      caption: "STYLE_07 图片说明"
      divider: "STYLE_08 分割线"
      emphasis: "STYLE_09 强调文字"
      link: "STYLE_10 链接样式"
      footnote: "STYLE_11 脚注"
      highlight: "STYLE_12 高亮块"
      collapsible: "STYLE_13 折叠块"
      signature: "STYLE_14 签名区"

  rule_2_wechat_compatibility:
    trigger: "微信公众号HTML兼容性检查"
    rules:
      - "仅使用内联样式（不支持外部CSS和class/id选择器）"
      - "仅使用支持的HTML标签（section, div, p, span, strong, em, a, img, br, h1-h6, blockquote, ul, ol, li）"
      - "不使用iframe, script, style, form, input, button标签"
    reason: "微信公众号编辑器限制"

  rule_3_copy_paste_ready:
    trigger: "一键复制格式输出"
    format: "HTML内联样式（符合微信公众号支持的HTML标签）"
    reason: "公众号编辑器需要可直接粘贴的HTML"
```

---

## 与 profound-cognition Task 节点集成

```yaml
task_integration:
  T20_output_rendering:
    trigger: "输出渲染 — wechat_article 基础排版"
    strategy: "按样式选择策略规则选择样式"
    output: "HTML内联样式嵌入 T20 渲染输出"
    annotation: "[bmmd] 标签标记内置排版"

  T13_cog_synthesize:
    trigger: "认知综合 — 公众号内容格式化"
    strategy: "rule_1_content_type_matching"
    output: "格式化内容注入综合分析"
    annotation: "[bmmd-format] 标签标记格式化内容"
```

---

## 错误处理

```yaml
error_handling:
  style_not_found:
    action: "使用 STYLE_01 正文段落 作为默认样式"
    log: "记录样式未找到事件"

  html_render_error:
    action: "穷尽重试到 Markdown 纯文本"
    log: "记录HTML渲染错误事件"

  wechat_incompatible:
    action: "移除不兼容的标签和样式"
    log: "记录微信不兼容事件"

  copy_failure:
    action: "提供HTML源代码供手动复制"
    log: "记录复制失败事件"
```

---

## 穷尽重试策略

```yaml
exhaust_retry:
  L1_FULL:
    condition: "bmmd 排版可用"
    behavior: "完整14种样式映射 + 微信一键复制"

  L2_PARTIAL_DATA:
    condition: "bmmd 可用但部分样式异常"
    behavior: "可用样式排版 + 标注[PARTIAL-STYLE]"

  L3_TEXT_ONLY:
    condition: "bmmd 不可用"
    behavior: "纯HTML内联样式 + 标注[HTML-INLINE]"

  L4_SERVICE_DOWN:
    condition: "所有排版工具不可用"
    behavior: "Markdown纯文本 + 标注[MARKDOWN-ONLY]"
```
