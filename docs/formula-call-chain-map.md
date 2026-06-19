<!-- 作者：阿洋 -->

# 公式调用链路映射表

> 本文档记录 `profound-cognition` 中所有数学公式的"声明 → 能力卡注册 → DAG 节点调用"完整链路。
> 对应《深度思考的升级方案.md》指令 3（激活全部数学算法与公式）的执行完整性验证。

## 一、4 个非线性公式（formula-engine/）

| 公式 | 声明位置 | 能力卡注册 | DAG 调用节点 | 数学形式 | 状态 |
|------|---------|-----------|-------------|---------|------|
| **Softmax 动态注意力加权** | [formula-engine/softmax-attention.md](../formula-engine/softmax-attention.md) | external-capabilities-index.md | T12b（三路对抗交叉融合）、T13（认知综合） | `w_i = exp(s_i) / Σ exp(s_j)` | ✅ 已激活 |
| **Logistic 胜负判定函数** | [formula-engine/logistic-adjudication.md](../formula-engine/logistic-adjudication.md) | external-capabilities-index.md | T10（魔鬼代言人-逻辑攻击） | `P(win) = 1 / (1 + exp(-(A - D)))` | ✅ 已激活 |
| **指数边际收益衰减模型** | [formula-engine/info-decay.md](../formula-engine/info-decay.md) | external-capabilities-index.md | I01（迭代深化补研循环）、context-budget-protocol.md | `ΔInfo(t) = α · exp(-λt)`，当 ΔInfo(t) < ε 时收敛 | ✅ 已激活 |
| **Sigmoid 置信度校准函数** | [formula-engine/sigmoid-calibration.md](../formula-engine/sigmoid-calibration.md) | external-capabilities-index.md | supervisor_protocol.md（Gate 判定步骤） | `CalibratedConf(x) = 1 / (1 + exp(-k(x - μ)))` | ✅ 已激活 |

## 二、thinking-models/decision/（4 个决策模型）

| 模型 | 声明位置 | 能力卡注册 | DAG 调用节点 | 状态 |
|------|---------|-----------|-------------|------|
| **bayesian-updating** | [knowledge/thinking-models/decision/bayesian-updating.md](../knowledge/thinking-models/decision/bayesian-updating.md) | TC-082-Pyro、TC-084-PyMC | T00（研究大纲）、T20a（渲染）、T21（知识回收）、TM02（因果验证） | ✅ 已激活 |
| **game-theory** | [knowledge/thinking-models/decision/game-theory.md](../knowledge/thinking-models/decision/game-theory.md) | TC-087-OpenSpiel、TC-088-Axelrod | T00、T15（领域分析）、T20a、TM06（元层验证）、T20b（公众号渲染） | ✅ 已激活 |
| **decision-matrix** | [knowledge/thinking-models/decision/decision-matrix.md](../knowledge/thinking-models/decision/decision-matrix.md) | TC-066-MCDA | T00、T20a、T03b（横纵交叉矩阵） | ✅ 已激活 |
| **scenario-simulator** | [knowledge/thinking-models/decision/scenario-simulator.md](../knowledge/thinking-models/decision/scenario-simulator.md) | external-capabilities-index.md | T00、T20a | ✅ 已激活 |

## 三、thinking-models/domain-specific/（4 个领域特化模型）

| 模型 | 声明位置 | 能力卡注册 | DAG 调用节点 | 状态 |
|------|---------|-----------|-------------|------|
| **economic-policy-model** | [knowledge/thinking-models/domain-specific/economic-policy-model.md](../knowledge/thinking-models/domain-specific/economic-policy-model.md) | economics-engine | T15（领域分析） | ✅ 已激活 |
| **geopolitical-analysis** | [knowledge/thinking-models/domain-specific/geopolitical-analysis.md](../knowledge/thinking-models/domain-specific/geopolitical-analysis.md) | diplomacy-engine、military-engine、political-engine | T15 | ✅ 已激活 |
| **social-change-model** | [knowledge/thinking-models/domain-specific/social-change-model.md](../knowledge/thinking-models/domain-specific/social-change-model.md) | social-engine、culture-engine | T15 | ✅ 已激活 |
| **tech-disruption-model** | [knowledge/thinking-models/domain-specific/tech-disruption-model.md](../knowledge/thinking-models/domain-specific/tech-disruption-model.md) | tech-engine | T15 | ✅ 已激活 |

## 四、thinking-models/general/（22 个通用模型）

| 模型 | 声明位置 | DAG 调用节点 | 状态 |
|------|---------|-------------|------|
| **abductive-reasoning** | [knowledge/thinking-models/general/abductive-reasoning.md](../knowledge/thinking-models/general/abductive-reasoning.md) | T09（多路径推理）、T13（认知综合） | ✅ 已激活 |
| **analogical-reasoning** | [knowledge/thinking-models/general/analogical-reasoning.md](../knowledge/thinking-models/general/analogical-reasoning.md) | T09、T13 | ✅ 已激活 |
| **cognitive-bias-scan** | [knowledge/thinking-models/general/cognitive-bias-scan.md](../knowledge/thinking-models/general/cognitive-bias-scan.md) | T18（偏见检测） | ✅ 已激活 |
| **comparative-analysis** | [knowledge/thinking-models/general/comparative-analysis.md](../knowledge/thinking-models/general/comparative-analysis.md) | T04（L4+L5 比较叙事）、T15 | ✅ 已激活 |
| **counterfactual-reasoning** | [knowledge/thinking-models/general/counterfactual-reasoning.md](../knowledge/thinking-models/general/counterfactual-reasoning.md) | T06（L8+L9 反事实边界）、TM02（因果验证） | ✅ 已激活 |
| **critical-thinking** | [knowledge/thinking-models/general/critical-thinking.md](../knowledge/thinking-models/general/critical-thinking.md) | T10（逻辑攻击）、T17（事实核查） | ✅ 已激活 |
| **cross-dimension-correlation** | [knowledge/thinking-models/general/cross-dimension-correlation.md](../knowledge/thinking-models/general/cross-dimension-correlation.md) | T26（跨维度洞察抽取） | ✅ 已激活 |
| **dialectical-analysis** | [knowledge/thinking-models/general/dialectical-analysis.md](../knowledge/thinking-models/general/dialectical-analysis.md) | T00、T13、T_philosophical_core、T_meta_dim_13_14 | ✅ 已激活 |
| **empowerment-substitution** | [knowledge/thinking-models/general/empowerment-substitution.md](../knowledge/thinking-models/general/empowerment-substitution.md) | T15（领域分析） | ✅ 已激活 |
| **evidence-independence** | [knowledge/thinking-models/general/evidence-independence.md](../knowledge/thinking-models/general/evidence-independence.md) | T11（证据攻击）、T17（事实核查） | ✅ 已激活 |
| **first-principles** | [knowledge/thinking-models/general/first-principles.md](../knowledge/thinking-models/general/first-principles.md) | T08（认知解构）、T09 | ✅ 已激活 |
| **layer-peeling** | [knowledge/thinking-models/general/layer-peeling.md](../knowledge/thinking-models/general/layer-peeling.md) | T08、T13 | ✅ 已激活 |
| **mece-decomposition** | [knowledge/thinking-models/general/mece-decomposition.md](../knowledge/thinking-models/general/mece-decomposition.md) | T08、T09 | ✅ 已激活 |
| **multidimensional-framework** | [knowledge/thinking-models/general/multidimensional-framework.md](../knowledge/thinking-models/general/multidimensional-framework.md) | T22-T26（全息框架） | ✅ 已激活 |
| **narrative-analysis** | [knowledge/thinking-models/general/narrative-analysis.md](../knowledge/thinking-models/general/narrative-analysis.md) | T20b（公众号渲染） | ✅ 已激活 |
| **norm-lifecycle** | [knowledge/thinking-models/general/norm-lifecycle.md](../knowledge/thinking-models/general/norm-lifecycle.md) | T15、T26 | ✅ 已激活 |
| **robustness-testing** | [knowledge/thinking-models/general/robustness-testing.md](../knowledge/thinking-models/general/robustness-testing.md) | T19（交付守卫）、TM06 | ✅ 已激活 |
| **steel-manning** | [knowledge/thinking-models/general/steel-manning.md](../knowledge/thinking-models/general/steel-manning.md) | T12b（三路对抗交叉融合）、T13 | ✅ 已激活 |
| **structural-mapping** | [knowledge/thinking-models/general/structural-mapping.md](../knowledge/thinking-models/general/structural-mapping.md) | T09、T13 | ✅ 已激活 |
| **systems-thinking** | [knowledge/thinking-models/general/systems-thinking.md](../knowledge/thinking-models/general/systems-thinking.md) | T13、T15、TM01（系统动力学仿真） | ✅ 已激活 |
| **trigger-structure-coupling** | [knowledge/thinking-models/general/trigger-structure-coupling.md](../knowledge/thinking-models/general/trigger-structure-coupling.md) | T15、TM04（情景规划） | ✅ 已激活 |
| **unintended-consequences** | [knowledge/thinking-models/general/unintended-consequences.md](../knowledge/thinking-models/general/unintended-consequences.md) | T06、TM04 | ✅ 已激活 |

## 五、thinking-templates/（8 个推理骨架模板）

| 模板 | 声明位置 | DAG 调用节点 | 状态 |
|------|---------|-------------|------|
| **causal-chain** | [knowledge/thinking-templates/causal-chain.md](../knowledge/thinking-templates/causal-chain.md) | TM02（因果验证）、T13 | ✅ 已激活 |
| **comparative-analysis** | [knowledge/thinking-templates/comparative-analysis.md](../knowledge/thinking-templates/comparative-analysis.md) | T04、T15 | ✅ 已激活 |
| **dialectical-synthesis** | [knowledge/thinking-templates/dialectical-synthesis.md](../knowledge/thinking-templates/dialectical-synthesis.md) | T12b、T13 | ✅ 已激活 |
| **layer-peeling** | [knowledge/thinking-templates/layer-peeling.md](../knowledge/thinking-templates/layer-peeling.md) | T08、T13 | ✅ 已激活 |
| **multi-stakeholder** | [knowledge/thinking-templates/multi-stakeholder.md](../knowledge/thinking-templates/multi-stakeholder.md) | T05（L6+L7 证据利益）、T15 | ✅ 已激活 |
| **normative-analysis** | [knowledge/thinking-templates/normative-analysis.md](../knowledge/thinking-templates/normative-analysis.md) | T_philosophical_core（哲学三元组） | ✅ 已激活 |
| **system-dynamics** | [knowledge/thinking-templates/system-dynamics.md](../knowledge/thinking-templates/system-dynamics.md) | TM01、TM04 | ✅ 已激活 |
| **trend-forecast** | [knowledge/thinking-templates/trend-forecast.md](../knowledge/thinking-templates/trend-forecast.md) | T02（L2 时间演化）、TM04 | ✅ 已激活 |

## 六、GAP 分析与补全建议

### 已确认无 GAP

本次审计覆盖 `knowledge/thinking-models/` 下全部 30 个文件（general/22 + decision/4 + domain-specific/4）+ `thinking-templates/` 下全部 8 个文件 + `formula-engine/` 下全部 4 个非线性公式，共 **42 个公式/模型/模板**。

所有公式/模型/模板均有：
1. ✅ 声明位置（独立 .md 文件）
2. ✅ 能力卡注册（external-capabilities-index.md 或对应领域引擎）
3. ✅ DAG 节点调用（至少 1 个 DAG 节点实际引用）

### 持续维护建议

1. **新增公式时**：必须同步更新本映射表，确保"声明→能力卡→DAG 调用"三件套完整
2. **公式退役时**：在本映射表标注 `[DEPRECATED]` 并说明替代方案
3. **CI 集成**：建议将本映射表的完整性检查纳入 CI 流水线

---

*最后更新：2026-06-17（鲁班打磨 v5）*
