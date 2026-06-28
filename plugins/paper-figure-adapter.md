---
name: paper-figure-adapter
description: 论文图表适配器 — 提供学术论文图表生成与检索
author: 阿洋
tags: [paper, figure, adapter, academic]
---

<!-- 作者：阿洋 -->

# Paper Framework Figure Studio Pro Adapter — 手绘框架图生成

## 风格描述
内联 Mermaid/SVG 图生成 是手绘风格的学术框架图生成工具，产出具有手绘质感的SVG框架图，适用于研究论文和深度报告。

## 手绘框架图生成指引
1. 确定框架类型（研究框架图/知识图谱/方法论图）
2. 定义节点和边（概念节点 + 关系连线）
3. 选择手绘风格参数（线条抖动、字体倾斜、颜色渐变）
4. 生成SVG代码（含手绘效果CSS滤镜）
5. 嵌入到Typst/HTML文档中

## 3种框架图类型

### 类型1: 研究框架图（Research Framework）
- 用途：展示研究问题的概念框架
- 节点：核心概念、变量、假设
- 边：因果关系、影响方向、调节效应
- 示例：全息框架14维度关系图

### 类型2: 知识图谱（Knowledge Graph）
- 用途：展示领域知识结构
- 节点：实体、概念、理论
- 边：上下位关系、关联关系、引用关系
- 示例：跨领域知识关联图

### 类型3: 方法论图（Methodology Diagram）
- 用途：展示研究方法流程
- 节点：方法步骤、工具、数据源
- 边：数据流、依赖关系、迭代循环
- 示例：DAG流水线拓扑图

## 穷尽尝试到 Mermaid.js 的规则
当 内联 Mermaid/SVG 图生成 不可用时：
1. 使用 Mermaid.js 生成标准框架图
2. 添加手绘风格CSS（Mermaid主题配置）
3. 标注 [Mermaid Exhaust-Retry] 并在 T21 中记录

---

## 激活条件

```yaml
activation:
  condition: "需要生成手绘风格学术框架图 AND SVG/Mermaid 渲染可用"
  priority: "首选框架图引擎 — 手绘质感+学术风格"
  exhaust-retry: "若手绘渲染不可用，穷尽尝试到标准 Mermaid.js 图表 → 纯文本描述"
```

---

## 框架图类型选择规则

```yaml
figure_type_selection:
  rule_1_research_framework:
    trigger: "展示研究问题的概念框架"
    type: "研究框架图"
    elements: "核心概念节点 + 因果关系边 + 假设标注"
    style: "线条抖动0.5px + 字体倾斜2° + 渐变填充"
    reason: "研究框架需要清晰的因果逻辑表达"

  rule_2_knowledge_graph:
    trigger: "展示领域知识结构"
    type: "知识图谱"
    elements: "实体节点 + 上下位关系边 + 关联关系边"
    style: "线条抖动0.3px + 字体倾斜1° + 分层布局"
    reason: "知识图谱需要层级化和关联化表达"

  rule_3_methodology_diagram:
    trigger: "展示研究方法流程"
    type: "方法论图"
    elements: "方法步骤节点 + 数据流边 + 依赖关系边"
    style: "线条抖动0.4px + 字体倾斜1.5° + 流程布局"
    reason: "方法论图需要清晰的流程和依赖表达"
```

---

## 与 profound-cognition Task 节点集成

```yaml
task_integration:
  T20_output_rendering:
    trigger: "输出渲染 — 需要框架图时"
    strategy: "按框架图类型选择规则选择类型"
    output: "SVG框架图嵌入 T20 渲染输出"
    annotation: "[paper-figure] 标签标记手绘框架图"

  T13_cog_synthesize:
    trigger: "认知综合 — 概念框架可视化"
    strategy: "rule_1_research_framework"
    output: "研究框架图注入综合分析"
    annotation: "[paper-figure-framework] 标签标记研究框架图"
```

---

## 错误处理

```yaml
error_handling:
  svg_render_failure:
    action: "穷尽重试到 Mermaid.js 标准框架图"
    log: "记录 SVG 渲染失败事件"

  mermaid_failure:
    action: "穷尽重试到纯文本描述（ASCII图）"
    log: "记录 Mermaid 渲染失败事件"

  font_missing:
    action: "使用系统默认字体"
    log: "记录字体缺失事件"

  layout_overflow:
    action: "自动缩放节点大小和间距"
    log: "记录布局溢出事件"
```

---

## 穷尽重试策略

```yaml
exhaust_retry:
  L1_FULL:
    condition: "SVG手绘渲染可用"
    behavior: "完整手绘风格SVG框架图 + CSS滤镜"

  L2_PARTIAL_DATA:
    condition: "SVG渲染可用但手绘效果异常"
    behavior: "标准SVG框架图（无手绘效果）+ 标注[NO-SKETCH]"

  L3_TEXT_ONLY:
    condition: "SVG不可用但Mermaid可用"
    behavior: "Mermaid.js标准框架图 + 标注[INTERNAL_REASONING]"

  L4_SERVICE_DOWN:
    condition: "所有图表渲染不可用"
    behavior: "纯文本ASCII图 + 标注[TEXT-ONLY]"
```
