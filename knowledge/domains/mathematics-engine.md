<!-- 作者：阿洋 -->

# 数学引擎

> **引擎名称**: mathematics-engine
> **版本**: 1.0
> **标识**: knowledge/domains/mathematics-engine
> **职责**: 为认知流水线提供数学与形式科学领域的分析框架、关键争议和认知方法论

## 1. 核心分析框架

### 维度一：形式化推理与证明结构
- 公理体系与形式演绎的严密性评估
- 定理证明的逻辑链条完整性分析
- 反例构造与命题否证方法论
- 形式系统的一致性、完备性与可判定性

### 维度二：数学建模与抽象化
- 现实问题的数学化抽象过程评估
- 模型假设的合理性与局限性分析
- 连续与离散建模范式的适用边界
- 参数敏感性与模型鲁棒性检验

### 维度三：数量关系与模式识别
- 统计规律与因果关系的区分
- 大数定律与中心极限定理的适用条件
- 相关性、关联性与因果性的层次辨析
- 异常值与极端值的统计意义评估

### 维度四：算法复杂性与计算边界
- 计算复杂性分类（P/NP/NP-hard/NP-complete）
- 算法效率的时间与空间权衡
- 不可计算问题与计算不可约性
- 近似算法与随机化算法的精度-效率平衡

### 维度五：数学哲学与认识论
- 数学对象的实在性（柏拉图主义 vs 形式主义 vs 构造主义）
- 数学直觉与形式化的张力
- 数学美的标准与启发力（简洁性、对称性、意外性）
- 数学知识的确定性与可错性

## 2. 关键争议与前沿问题

### 争议一：数学是发现还是发明？
- **柏拉图主义立场**：数学对象独立于人类思维存在，数学家是发现者
- **形式主义立场**：数学是符号游戏，一致性比真理性更重要
- **构造主义立场**：只有可构造的数学对象才存在，排中律不普遍适用
- **实践影响**：对 AI 数学推理能力边界的哲学评估

### 争议二：概率解释的分歧
- **频率学派**：概率是长期频率的极限，客观可重复
- **贝叶斯学派**：概率是信念度，主观但可理性更新
- **倾向性解释**：概率是物理系统的内在倾向
- **实践影响**：风险评估与决策分析中概率方法的选择

### 争议三：数学证明的未来
- **传统证明**：人类可理解的自然语言论证
- **计算机辅助证明**：四色定理模式，可验证但不可理解
- **形式化验证**：Coq/Lean 等证明助手的完全形式化
- **AI 生成证明**：自动定理证明的可靠性与可解释性

## 3. 认知方法论

### 公理化方法
- 从公理出发的演绎推理体系
- 公理选择的独立性、一致性与完备性检验
- 非欧几何对公理可变性的启示

### 数学归纳法与递归方法
- 自然数上的数学归纳法
- 结构归纳法（树、图等递归结构）
- 良基归纳法与超限归纳法

### 反证法与构造法
- 间接证明（归谬法）的逻辑结构
- 构造性证明的存在性承诺
- 非构造性证明的哲学争议

### 组合分析与概率方法
- 计数原理与容斥原理
- 概率方法证明存在性（Erdős 方法）
- 随机化算法的分析框架

## 4. 依赖的能力卡片

| 能力卡 | 用途 |
|--------|------|
| MC-140 Bayesian-Inference | 贝叶斯概率推理与后验更新 |
| MC-152 Causal-Effect-Confounding | 因果效应量计算与混淆变量识别 |
| MC-159 MECE-Prioritization | MECE 递归分解与优先级排序 |

## 5. 输出模板

```yaml
mathematics_analysis:
  formal_reasoning:
    axiom_system: "使用的公理体系"
    proof_structure: "证明的逻辑链结构"
    consistency_check: "一致性检验结果"

  modeling_assessment:
    abstraction_quality: "抽象化质量评估"
    assumption_validity: "假设合理性评分"
    model_limitations: ["模型局限性列表"]

  quantitative_insights:
    pattern_identified: "识别的数量模式"
    statistical_significance: "统计显著性"
    boundary_conditions: ["适用边界条件"]

  complexity_analysis:
    computational_class: "计算复杂性分类"
    algorithm_efficiency: "算法效率评估"
    undecidability_flags: ["不可判定问题标记"]

  philosophical_implications:
    ontology_position: "数学对象本体论立场"
    certainty_level: "确定性水平评估"
    alternative_frameworks: ["替代理论框架"]
```

## 6. 分析器清单

| 分析器 | 触发条件 | 输出 |
|--------|---------|------|
| 形式化推理分析器 | 检测到"证明/推导/公理/定理"类任务 | proof_structure, consistency_check |
| 建模评估分析器 | 检测到"模型/仿真/参数/拟合"类任务 | abstraction_quality, model_limitations |
| 统计推断分析器 | 检测到"概率/统计/显著性/相关性"类任务 | statistical_significance, boundary_conditions |
| 复杂性分析器 | 检测到"算法/计算/复杂度/可解"类任务 | computational_class, algorithm_efficiency |

## 7. 调用矩阵

| 任务节点 | 调用分析器 | 触发条件 |
|---------|-----------|---------|
| T09 路径 D（因果推理） | 统计推断分析器 | 涉及概率判断与统计推断 |
| T09 路径 E（反事实推理） | 建模评估分析器 | 涉及模型假设与反事实推演 |
| T15 领域分析 | 形式化推理分析器 | 数学/逻辑/形式科学领域问题 |
| TM02 因果验证 | 统计推断分析器 | 因果效应的统计验证 |


### 领域引擎穷尽重试策略

> 引用 exhaust-retry-protocol.md：当领域数据或工具不可用时，不穷尽重试替代，而是穷尽尝试所有替代路径，持续重试直至质量达标。

```yaml
domain_engine_exhaust_retry:
  L1_FULL:
    condition: "领域知识完整，所有分析器可用，形式化工具可访问"
    tools: [Coq, Lean4, Bayesian_Inference, Causal_Effect_Confounding, MECE_Prioritization]
    action: "完整数学分析流程：形式化推理+建模评估+统计推断+复杂性分析全量执行"
    confidence: "HIGH"
  L2_RETRYING_PARTIAL:
    condition: "形式化验证工具不可用或部分分析器重试中"
    tools: [manual_proof_check, simplified_Bayesian, basic_MECE]
    action: "穷尽重试：手动证明检查+简化贝叶斯推理+基础MECE分解，持续尝试恢复形式化验证工具"
    confidence: "MEDIUM"
    output_annotation: "领域引擎部分重试中：无形式化验证工具，手动证明检查，持续尝试恢复"
  L3_RETRYING_TEXT:
    condition: "所有外部工具不可用，穷尽重试后仅剩LLM自有知识"
    tools: [qualitative_proof_sketch, informal_reasoning]
    action: "穷尽重试：非形式化证明草图+直觉推理，持续尝试恢复形式化验证，标注'穷尽重试后仍无形式化验证'"
    confidence: "LOW-MEDIUM"
    output_annotation: "领域引擎穷尽重试：定性数学推理模式，持续尝试恢复形式化验证"
  L4_EXHAUSTED:
    condition: "领域知识完全不足（超出LLM知识范围的专业领域），穷尽重试后仍无法获得足够领域知识"
    tools: []
    action: "穷尽重试后仍领域知识不足，标注不确定性，建议人工专家介入"
    confidence: "LOW"
    output_annotation: "领域引擎穷尽重试后仍不足：建议专家介入"
```
