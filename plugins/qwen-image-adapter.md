<!-- 作者：阿洋 -->

# Qwen-Image Adapter — 文生图

## 适配器配置
- role: 文生图引擎，用于生成概念插图、书法、对联、招牌文字
- model: qwen-image-max
- endpoint: DashScope API

## Prompt 模板

### 中文优化模板
```
你是一位专业插画师。请为以下概念创作一幅插图：
主题：{concept}
风格：{style}（学术插图/概念图/信息图）
色调：{color_scheme}
构图：{composition}
要求：专业、清晰、适合学术出版物
```

### 英文优化模板
```
Professional scientific illustration for the concept: {concept}
Style: {style} (academic illustration / conceptual diagram / infographic)
Color palette: {color_scheme}
Layout: {composition}
Requirements: professional, clean, publication-ready
```

## 适用场景
- 概念插图：全息框架各维度配图
- 书法：标题艺术字
- 对联：中文内容排版
- 招牌文字：品牌标识
- 数据可视化辅助：图表装饰

---

## 激活条件

```yaml
activation:
  condition: "需要生成概念插图/书法/对联/招牌文字 AND Qwen-Image API 可用"
  priority: "首选文生图引擎 — 中文优化+学术风格"
  exhaust-retry: "若 Qwen-Image 不可用，穷尽尝试到 Mermaid/SVG 图表 → 纯文本描述"
```

---

## 图像生成策略选择规则

```yaml
generation_strategy:
  rule_1_concept_illustration:
    trigger: "全息框架各维度配图"
    style: "学术插图"
    color_scheme: "aesthetic-enhancer.md 主色调"
    composition: "居中对称"
    size: "1024x1024"
    reason: "维度配图需要学术风格的清晰概念表达"

  rule_2_calligraphy:
    trigger: "标题艺术字/书法"
    style: "书法"
    color_scheme: "黑白为主+强调色点缀"
    composition: "竖排/横排"
    size: "1024x1536"
    reason: "书法需要高分辨率竖版画布"

  rule_3_infographic:
    trigger: "数据可视化辅助/信息图"
    style: "信息图"
    color_scheme: "aesthetic-enhancer.md 分类色"
    composition: "分层布局"
    size: "1536x1024"
    reason: "信息图需要横版画布和分层布局"

  rule_4_brand:
    trigger: "招牌文字/品牌标识"
    style: "品牌设计"
    color_scheme: "品牌主色"
    composition: "居中"
    size: "1024x1024"
    reason: "品牌标识需要正方形画布"
```

---

## 与 profound-cognition Task 节点集成

```yaml
task_integration:
  T20_output_rendering:
    trigger: "输出渲染 — 需要配图时"
    strategy: "按生成策略规则选择风格"
    output: "图像URL/文件注入 T20 渲染输出"
    annotation: "[qwen-image] 标签标记AI生成图像"

  T13_cog_synthesize:
    trigger: "认知综合 — 概念可视化辅助"
    strategy: "rule_1_concept_illustration"
    output: "概念插图注入综合分析"
    annotation: "[qwen-image-concept] 标签标记概念插图"
```

---

## 错误处理

```yaml
error_handling:
  api_timeout:
    action: "穷尽重试到 Mermaid/SVG 图表"
    log: "记录 Qwen-Image API 超时事件"
    timeout: 60000  # ms

  api_error:
    action: "穷尽重试到纯文本描述"
    log: "记录API错误事件，标注 error_code={code}"

  content_filter:
    action: "修改prompt重试（移除敏感词），穷尽重试直至成功"
    log: "记录内容过滤事件"

  quota_exceeded:
    action: "穷尽重试到 Mermaid/SVG 图表"
    log: "记录配额超限事件"

  quality_unsatisfied:
    action: "调整prompt参数重试，穷尽重试直至满意"
    log: "记录质量不满意事件"
```

---

## 穷尽重试策略

```yaml
exhaust_retry:
  L1_FULL:
    condition: "Qwen-Image API 可用"
    behavior: "完整文生图 + 中文优化 + 学术风格"

  L2_PARTIAL_DATA:
    condition: "Qwen-Image API 可用但响应慢"
    behavior: "降低分辨率/简化prompt + 标注[LOW-RES]"

  L3_TEXT_ONLY:
    condition: "Qwen-Image API 不可用"
    behavior: "穷尽尝试到 Mermaid/SVG 图表 + 标注[CHART-INTERNAL_REASONING]"

  L4_SERVICE_DOWN:
    condition: "所有图像生成工具不可用"
    behavior: "纯文本描述 + 标注[TEXT-ONLY]"
```
