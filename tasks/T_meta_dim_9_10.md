<!-- 作者：阿洋 -->
<!-- output_type_restriction: [research_report]  # R1-02 分层激活 -->

# T_meta_dim_9_10 — 无知之学与认知神经心理学

## role
你是元维度9-10的产出者。你的任务是产出"无知之学（Agnotology）"和"认知神经心理学"两个高阶维度，将"已知"与"未知"、"认知"与"元认知"连接起来。维度9聚焦于"未知"的结构化研究，维度10引入双系统理论等认知科学工具审计研究过程。

## context
- 依赖 T25_meta_dim_part3 的全息框架第三部分产出
- 消费 NRSF §T25_* 的全部输出（极限决策推理）
- 全息框架前三维度的产出作为认知基线

## output_schema
> **JSON Schema 规范 (D2.4.1)**: 本节点 output_schema 遵循 `protocols/output-schema-spec.md` 定义的 JSON Schema 统一格式。字段类型遵循 JSON Schema Draft 2020-12 规范。
> **execution_params**: object  # 实际执行参数，必须达到 SKILL.md 规定的最低值（R2-05 防深度缩水）

```yaml
T_meta_dim_9_10:
  dim_9_agnotology:
    aspect_25_unknown_map:
      technical_unknowns: [{description, access_path, time_window}]
      structural_unknowns: [{description, barrier, breakthrough_condition}]
      principled_unknowns: [{description, philosophical_basis}]
      count: "≥3 each level"
    aspect_26_red_team:
      attack_paths: [{id, hypothesis, path, evidence, defense}]
      stress_test: {degradation_point, collapse_point, residual_validity}
      count: "≥3 attack paths"
    aspect_27_black_swan:
      black_swans: [{description, unpredictability, impact, antifragile_strategy}]
      dragon_kings: [{description, warning_signals, neglect_reason, detection}]
      antifragile_modules: [{strategy, mechanism, applicability}]
      count: "≥3 black swans, ≥2 dragon kings, ≥3 modules"
  dim_10_cognitive_neuropsychology:
    aspect_28_dual_system:
      fluency_audit: [{statement_id, system1, system2, type, bias_warning}]
      type_distribution: {A, B, C, D}
      count: "≥5 statements audited"
    aspect_29_regret_minimization:
      regret_scenarios: [{type, horizon, description, trigger, prevention, cost}]
      count: "≥3 scenarios, 3 time horizons"
    aspect_30_mental_models:
      mental_models: [{name, description, assumptions, boundaries, blind_spots}]
      alignment_audit: {cross_model_consistency, conflict_points, resolution}
      count: "≥3 models"
  nrsf_append: "§T_meta_dim_9_10"
```

## self_check_before_output
> **量化标准 (D2.4.3)**: 本节点 self_check_before_output 遵循 `protocols/output-schema-spec.md` §4 定义的量化通过判据。self_check_score >= 85 方可输出。
- [ ] 维度9：三级未知等级地图是否完整（技术性/结构性/原则性各≥1）？
- [ ] 维度9：红队攻击路径是否≥3条，且每条包含完整的攻击假设→路径→证据→防御链？
- [ ] 维度9：反向应力测试是否标注了退化点、崩溃点和残余有效性？
- [ ] 维度9：黑天鹅≥3、龙王≥2、抗脆弱模块≥3？
- [ ] 维度10：双系统审计是否覆盖≥5个关键陈述？
- [ ] 维度10：后悔情景是否覆盖三类后悔类型（遗漏/过度自信/框架）×三个时间窗口？
- [ ] 维度10：心智模型≥3个且每个含核心假设、边界和盲区？
- [ ] 维度10：对齐审计含跨模型一致性评估和冲突消解策略？
- [ ] 与 §T25 的交叉引用是否正确（§ref 前向引用）？
- [ ] NRSF 附录是否已写入 §T_meta_dim_9_10？

## must_not
- 禁止仅列举"未知"而不区分三级（技术性/结构性/原则性）
- 禁止红队攻击流于表面（每条攻击路径必须有逻辑链条而非仅表态）
- 禁止将伪解决方案包装为可消解冲突
- 禁止双系统审计仅做表面标注而不给偏差警告
- 禁止后悔最小化框架仅做定性感慨而不具体化触发条件和预防措施
- 禁止心智模型外化时遗漏盲区标注

## knowledge_refs
- `knowledge/external-capabilities/TC-063-元认知网络.md` — 元认知网络
- `knowledge/external-capabilities/TC-064-认识网络分析.md` — 认识网络分析 认知网络分析
- `knowledge/thinking-models/general/systems-thinking.md` — 系统思维
- `tasks/T25_meta_dim_part3.md` — 全息框架第三部分