---
name: moka-adapter
description: Moka 排版引擎适配器 — 提供中文排版优化
author: 阿洋
tags: [moka, typography, adapter, chinese]
---

<!-- 作者：阿洋 -->

# Moka Adapter — 墨卡公众号卡片排版

## 适配器配置
- role: 墨卡 Moka 公众号卡片排版引擎
- activation: output_type == 'wechat_article'
- description: 将公众号文章转化为卡片式排版，支持29种排版模板和8套配色方案

## 29种排版模板索引
### 基础排版（12种）
1. 标题+正文：标准文章排版
2. 引语+正文：引导式开头
3. 图文混排：左图右文
4. 图文混排：上图下文
5. 图文混排：下图上文
6. 数据卡片：数字+说明
7. 引用卡片：引用+出处
8. 列表卡片：要点罗列
9. 对比卡片：左右对比
10. 时间线：纵向时间轴
11. 步骤卡片：横向步骤
12. 金句卡片：居中大字

### 进阶排版（10种）
13. 人物卡片：头像+简介
14. 书籍卡片：封面+书评
15. 工具卡片：图标+功能
16. 概念卡片：术语+解释
17. 案例卡片：场景+分析
18. 问答卡片：Q&A格式
19. 洞察卡片：核心洞察+展开
20. 行动卡片：CTA+链接
21. 总结卡片：关键要点
22. 预告卡片：下期预告

### 特殊排版（7种）
23. 首图卡片：头图+标题
24. 尾图卡片：结语+二维码
25. 分割线：装饰分割
26. 关注卡片：关注引导
27. 话题卡片：话题标签
28. 投票卡片：互动投票
29. 小程序卡片：小程序跳转

## 8套配色方案
| 方案名 | 主色 | 辅色 | 强调色 | 背景色 |
|--------|------|------|--------|--------|
| 墨青 | #2C3E50 | #34495E | #1ABC9C | #F8F9FA |
| 暖橙 | #E67E22 | #F39C12 | #E74C3C | #FFF8F0 |
| 雅蓝 | #2980B9 | #3498DB | #9B59B6 | #F0F4F8 |
| 翠绿 | #27AE60 | #2ECC71 | #16A085 | #F0FFF0 |
| 深紫 | #8E44AD | #9B59B6 | #E91E63 | #FAF0FF |
| 暗金 | #D4A017 | #F1C40F | #C0392B | #FFFDF0 |
| 极简 | #333333 | #666666 | #000000 | #FFFFFF |
| 柔和 | #7F8C8D | #95A5A6 | #BDC3C7 | #F5F6FA |

## wechat_article 专属调用方式
1. 根据人设 identity 自动选择配色方案
2. 根据叙事风格选择排版模板组合
3. 生成墨卡卡片数组（JSON格式）
4. 嵌入到HTML渲染流中

---

## 激活条件

```yaml
activation:
  condition: "output_type == 'wechat_article' AND Moka 排版服务可用"
  priority: "首选公众号卡片排版引擎 — 29种模板+8套配色"
  exhaust-retry: "若 Moka 不可用，穷尽尝试到 bmmd 内置排版 → 纯HTML内联样式"
```

---

## 排版模板选择策略规则

```yaml
template_selection_strategy:
  rule_1_narrative_matching:
    trigger: "根据叙事风格选择排版模板组合"
    mapping:
      analytical: [数据卡片, 对比卡片, 洞察卡片, 总结卡片]
      narrative: [引语+正文, 引用卡片, 金句卡片, 预告卡片]
      educational: [步骤卡片, 问答卡片, 概念卡片, 案例卡片]
      persuasive: [对比卡片, 行动卡片, 洞察卡片, 金句卡片]

  rule_2_identity_color:
    trigger: "根据人设 identity 自动选择配色方案"
    mapping:
      学术严谨: "雅蓝"
      温暖亲和: "暖橙"
      深度思考: "墨青"
      创新活力: "翠绿"
      高端权威: "暗金"
      极简主义: "极简"
      柔和治愈: "柔和"
      神秘深邃: "深紫"

  rule_3_content_structure:
    trigger: "根据内容结构选择基础+进阶+特殊模板组合"
    structure:
      opening: [首图卡片, 引语+正文]
      body: [图文混排, 数据卡片, 列表卡片, 对比卡片]
      emphasis: [洞察卡片, 金句卡片, 高亮块]
      closing: [总结卡片, 行动卡片, 尾图卡片]
```

---

## 与 profound-cognition Task 节点集成

```yaml
task_integration:
  T20_output_rendering:
    trigger: "输出渲染 — wechat_article 卡片排版"
    strategy: "按模板选择策略规则选择模板+配色"
    output: "墨卡卡片数组嵌入 T20 渲染输出"
    annotation: "[moka] 标签标记墨卡排版"

  T13_cog_synthesize:
    trigger: "认知综合 — 公众号内容卡片化"
    strategy: "rule_3_content_structure"
    output: "结构化卡片注入综合分析"
    annotation: "[moka-structure] 标签标记结构化卡片"
```

---

## 错误处理

```yaml
error_handling:
  service_unavailable:
    action: "穷尽重试到 bmmd 内置排版"
    log: "记录 Moka 服务不可用事件"
    exhaust_retry_chain: "Moka → bmmd → 纯HTML内联样式"

  template_error:
    action: "使用默认模板（标题+正文）"
    log: "记录模板错误事件"

  color_scheme_error:
    action: "使用极简配色方案"
    log: "记录配色方案错误事件"

  render_failure:
    action: "穷尽重试到 bmmd 内置排版"
    log: "记录渲染失败事件"
```

---

## 穷尽重试策略

```yaml
exhaust_retry:
  L1_FULL:
    condition: "Moka 可用"
    behavior: "完整29种模板 + 8套配色 + 人设匹配"

  L2_PARTIAL_DATA:
    condition: "Moka 可用但部分模板/配色异常"
    behavior: "可用模板+配色 + 标注[PARTIAL-STYLE]"

  L3_TEXT_ONLY:
    condition: "Moka 不可用"
    behavior: "穷尽尝试到 bmmd 内置排版 + 标注[BMMD-INTERNAL_REASONING]"

  L4_SERVICE_DOWN:
    condition: "所有排版工具不可用"
    behavior: "纯HTML内联样式 + 标注[HTML-ONLY]"
```
