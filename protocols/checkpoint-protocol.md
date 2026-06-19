<!-- 作者：阿洋 -->

# 检查点与断点恢复协议 (Checkpoint & Recovery Protocol) v3

## 1. 协议概述

**方法论原理**：检查点协议基于"可恢复性是长流程可靠性的基础"的认知假设：长时间运行的认知分析流程可能因中断、错误或资源限制而失败，检查点机制使流程能够从最近的有效状态恢复，避免从头重新执行。

本协议定义认知流水线的检查点保存与断点恢复机制，确保长时间运行的推理任务在中断后可从最近状态恢复，避免重复计算。检查点在每个 Phase 完成后自动触发，保存完整上下文快照。

**触发条件**：每个 Phase（Phase 0-4、Phase 7）完成后自动触发检查点保存；用户再次触发同等任务时触发断点恢复。

## 2. 检查点保存

每个 Phase 完成后自动保存上下文快照：
- phase_id：当前 Phase 编号
- node_completion_status：各节点完成状态映射 {node_id: completed|retrying|skipped}
- core_conclusions：该 Phase 产出的核心结论摘要（≤ 500 字）
- nrsf_position：NRSF 中的当前写入位置

**Phase 4（输出渲染）检查点额外保存**：
- rendered_sections：已渲染的 §1-§8 章节列表及字数
- rendering_artifacts：渲染产物路径（HTML/Markdown/DOCX）
- gate_terminal_status：Gate-终 (T28) 检查状态

**Phase 7（元维度引擎）检查点额外保存**：
- meta_dimensions_status：元维度 9-14 扩展完成状态
- scientific_layer_status：TM01-TM07 科学层 7 模块完成状态
- philosophical_core_status：哲学三元组完成状态
- knowledge_graph_ontology：知识图谱本体导出状态（TM07）

## 3. 断点恢复

用户再次触发同等任务时：
1. 读取最近 checkpoint
2. 从对应 Phase 起点恢复执行
3. 已完成的节点标记为 CACHED，不重新执行

## 4. 增量更新模式

已完成报告支持基于新数据/新证据增量追加：
1. 定位到报告最后一个完整章节
2. 在该章节后追加新的 §N+1 增量章节
3. 增量章节标注数据来源时间和有效期限

## 5. 时间衰减权重

来源越近权重越高：
w(source) = exp(-λ · age_in_days)
- λ = 0.01（默认，来源约 100 天后权重降至 ~0.37）
- 对超过 365 天的来源，权重自动 < 0.03

## 6. 输出规范

```yaml
checkpoint:
  phase_id: "Phase 0|1|2|3|4|7"
  timestamp: "ISO8601时间戳"
  node_completion_status: {node_id: "completed|retrying|skipped|cached"}
  core_conclusions: "该Phase核心结论摘要"
  nrsf_position: "NRSF当前写入位置"
  recovery_point: "恢复执行的起点节点"
  # Phase 4 额外字段
  rendered_sections: ["§1", "§2", ...]
  rendering_artifacts: {html: "path", markdown: "path", docx: "path"}
  gate_terminal_status: "pass|fail|pending"
  # Phase 7 额外字段
  meta_dimensions_status: {dim_9_10: "completed", dim_11_12: "completed", dim_13_14: "completed"}
  scientific_layer_status: {TM01: "completed", TM02: "completed", ..., TM07: "completed"}
  philosophical_core_status: "completed"
  knowledge_graph_ontology: "exported|pending"
```

## 7. 异常处理与穷尽重试

| 异常场景 | 处理策略 |
|---------|---------|
| 检查点文件损坏或丢失 | 从上一个有效检查点恢复；若无任何有效检查点，从头开始执行 |
| 检查点版本不兼容 | 忽略不兼容检查点，从头开始执行，标注"检查点版本不兼容" |
| 恢复后节点状态不一致 | 对CACHED节点执行轻量验证（检查输出字段是否存在），不一致的节点重新执行 |
| 增量更新与已有内容冲突 | 冲突部分标注"时间戳冲突"，保留两个版本供人工裁决 |
| 存储空间不足无法保存检查点 | 持续重试保存直至成功，不设重试上限，不跳过完整上下文快照 |

## 决策规则

| 条件 | 动作 | 优先级 |
|------|------|--------|
| Phase完成且输出通过门控 | 保存检查点 | P0 |
| 长时间运行任务(>30min) | 每15min增量保存 | P1 |
| 用户中断请求 | 立即保存当前状态 | P0 |
| 检查点文件损坏 | 从最近有效检查点恢复 | P0 |
| 增量更新累积>5次 | 压缩为完整检查点 | P2 |
| 恢复后输出与之前不一致 | 重新执行当前Phase | P1 |