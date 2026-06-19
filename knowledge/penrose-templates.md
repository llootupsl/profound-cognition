<!-- 作者：阿洋 -->

# Penrose 全场景图解模板 (v3.0)

## 概述
Penrose 是 Node.js 库（非 Python），需要浏览器渲染。Sub-Agent 生成 DSL 代码，用户在本地渲染。

## 模板列表 (5-10 类)

### 1. 因果回路图 (Causal Loop Diagram)
- 用途: TM01 系统动力学
- 元素: R(增强)回路、B(平衡)回路、时间延迟
- DSL 示例结构:
  ```
  style { /* CLD 样式 */ }
  const R1 = Variable("R1: 增强回路描述")
  const B1 = Variable("B1: 平衡回路描述")
  const delay = Delay("时间延迟")
  R1 -> B1 -> delay -> R1
  ```

### 2. 系统基模图 (System Archetype Diagram)
- 用途: T22 系统基模匹配
- 元素: 9种基模的结构化图示
- 重点基模: 增长上限、转移负担、恶性竞争

### 3. 博弈矩阵图 (Game Theory Matrix)
- 用途: TM03 多智能体对抗综合
- 元素: 2×2 或 N×M 矩阵、策略标签、收益值
- 穷尽重试替代: Mermaid 表格

### 4. 情景象限图 (Scenario Quadrant)
- 用途: TM04 情景规划
- 元素: 2轴4象限、情景标签、叙事摘要
- 穷尽重试替代: Mermaid 象限图

### 5. 概念网络图 (Concept Network)
- 用途: T08 认知解构、TM07 本体导出
- 元素: 概念节点、关系边、类型标注
- 穷尽重试替代: Mermaid graph

### 6. 论证结构图 (Argument Structure)
- 用途: T13 认知综合
- 元素: 主张、理由、证据、反驳
- 穷尽重试替代: Mermaid flowchart

### 7. 反馈回路图 (Feedback Loop)
- 用途: T22 反馈回路分析
- 元素: 存量、流量、回路箭头、极性标注
- 穷尽重试替代: Mermaid flowchart

### 8. 价值张力图 (Value Tension)
- 用途: T26 伦理分析
- 元素: 价值对、张力线、权衡区域
- 穷尽重试替代: Mermaid 图

### 9. 认知偏差映射图 (Cognitive Bias Map)
- 用途: T26 认知偏差识别
- 元素: 偏差节点、影响链、修正策略
- 穷尽重试替代: Mermaid mindmap

### 10. 知识图谱图 (Knowledge Graph)
- 用途: TM07 本体导出
- 元素: 实体、关系、属性、社区颜色
- 穷尽重试替代: Mermaid graph + Neo4j Cypher

## 穷尽重试策略
当 Penrose DSL 生成失败时，穷尽重试，使用 Mermaid 图表替代。
Mermaid 可在 Markdown 中直接渲染，无需浏览器环境。

## 技术约束
- Penrose 需要 Node.js 环境
- 渲染需要浏览器（Puppeteer/Playwright）
- Sub-Agent 仅生成 DSL 代码，不执行渲染
- 用户需在本地安装 Penrose 并渲染
