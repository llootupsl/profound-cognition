<!-- 作者：阿洋 -->

# 读者理解测试协议 (Reader Comprehension Test Protocol) v3.0

> **协议版本**：v3.0
> **关联需求**：R8-04
> **关联节点**：T19（交付守卫）、T20（渲染）

## 1. 概述

**方法论原理**：读者理解测试基于"可读性即质量"的认知假设：一份研究报告无论内容多么深刻，若读者无法准确理解其核心结论，则该报告的交付质量不合格。本协议定义读者理解测试题的设计规则、LLM 判定流程、三级评定、理解率统计与可读性优化触发机制，确保报告的可读性可度量、可优化、可验证。

本协议在 T19（交付守卫）通过后、T20（渲染）完成前**强制执行**（P1-8 / A6.8-F1 修复，Wave 5：统一触发时机描述，消除"自动触发 vs 可选 vs 强制"三重矛盾歧义），对最终报告进行读者理解测试。测试题由 LLM 基于报告内容自动生成，由模拟读者（独立 LLM 实例）作答，再由判定 LLM 对比回答与报告结论的一致性。

> **触发时机权威声明（P1-8 修复）**：本协议的触发时机以本节（§1 概述）为唯一权威源——**T19 通过后、T20 完成前强制执行**。其他文件（如 tasks/T_gate_delta.md）若与本声明不一致，以本节为准。本协议不依赖 T_gate_delta 触发，T_gate_delta 也不引用本协议；二者独立运行（T_gate_delta 处理哲学三元组形式化验证，本协议处理读者理解测试）。

## 2. 理解测试题设计规则（SubTask 5.5.1）

### 2.1 题目数量

每份报告生成 **5-10 个理解测试题**，具体数量根据报告长度动态调整：

| 报告字数 | 测试题数量 |
|---------|----------|
| < 5,000 字 | 5 题 |
| 5,000-20,000 字 | 7 题 |
| 20,000-50,000 字 | 8 题 |
| 50,000-100,000 字 | 9 题 |
| > 100,000 字 | 10 题 |

### 2.2 五类题型定义

测试题必须覆盖以下五类题型，每类至少 1 题：

#### 题型 1：事实回忆（Fact Recall）

**定义**：测试读者是否能准确回忆报告中的关键事实、数据、定义。

**设计规则**：
- 题目必须指向报告中的具体事实（统计数据、事件、定义、引用结论）
- 避免模糊表述（如"报告中提到了什么"），必须明确指向具体事实
- 答案必须在报告中有明确出处（章节+段落）

**示例**：
```
问题：根据报告，2025 年中国新能源汽车出口量同比增长了多少百分比？
预期答案：报告 §3.2 指出，2025 年中国新能源汽车出口量同比增长 30%。
```

#### 题型 2：趋势判断（Trend Judgment）

**定义**：测试读者是否能基于报告数据判断趋势方向与变化速率。

**设计规则**：
- 题目必须基于报告中的时间序列数据或对比数据
- 答案必须包含趋势方向（上升/下降/平稳）与变化幅度
- 避免仅问"趋势是什么"，必须要求读者判断趋势的成因或影响

**示例**：
```
问题：根据报告 §4.1 的数据，全球半导体市场份额在 2020-2025 年间呈现什么趋势？这一趋势的主要驱动因素是什么？
预期答案：全球半导体市场份额从 2020 年的 X% 上升至 2025 年的 Y%，呈上升趋势。主要驱动因素是 AI 芯片需求爆发和国产替代加速。
```

#### 题型 3：反证理解（Counter-evidence Understanding）

**定义**：测试读者是否能准确理解报告中的反证、对立观点与边界条件。

**设计规则**：
- 题目必须指向报告中的反证段落或对立观点
- 答案必须准确复述反证的核心论点，而非简单否认主结论
- 测试读者是否理解"反证不等于否定主结论，而是限定其适用范围"

**示例**：
```
问题：报告 §6.3 提出了哪些反对"AI 将导致大规模失业"的反证？这些反证如何限定主结论的适用范围？
预期答案：反证包括（1）历史数据显示技术革命短期内创造的新岗位多于消灭的旧岗位；（2）AI 商业化催生了提示词工程师等新职业。这些反证限定了主结论的适用范围：AI 导致失业主要影响重复性高的岗位，而非所有岗位。
```

#### 题型 4：边界条件（Boundary Conditions）

**定义**：测试读者是否能识别报告结论的适用边界、前提假设与不确定性。

**设计规则**：
- 题目必须指向报告中的前提假设、不确定性标注或边界条件声明
- 答案必须准确复述边界条件，而非简单否认结论
- 测试读者是否理解"结论在边界外不成立"

**示例**：
```
问题：报告 §7.2 关于"2030 年可再生能源占比达 50%"的预测，其前提假设是什么？在什么条件下该预测不成立？
预期答案：前提假设包括（1）政策持续支持；（2）储能技术成本下降 30%；（3）无重大地缘政治冲突。若储能技术成本下降不及预期，或出现重大地缘政治冲突，该预测不成立。
```

#### 题型 5：应用推演（Application Reasoning）

**定义**：测试读者是否能基于报告结论进行推演，将结论应用到报告未直接覆盖的新场景。

**设计规则**：
- 题目必须构造一个报告未直接覆盖的新场景
- 答案必须基于报告的核心结论进行推演，而非凭空猜测
- 测试读者是否真正理解了结论的因果机制，而非仅记忆结论

**示例**：
```
问题：报告指出"碳关税将使中国新能源汽车出口成本上升 8-12%"。若欧盟将碳关税税率提高 50%，基于报告的因果分析，对中国新能源汽车出口的影响会如何变化？
预期答案：基于报告 §5.3 的因果分析，碳关税税率提高 50% 将使出口成本上升幅度从 8-12% 扩大至约 12-18%，可能导致部分低端车型失去价格优势，但高端车型因利润空间较大仍可承受。
```

### 2.3 题目生成规则

```python
def generate_comprehension_questions(report_content: str, report_metadata: dict) -> list:
    """基于报告内容生成 5-10 个理解测试题。

    Args:
        report_content: 最终报告全文
        report_metadata: 报告元数据（字数、章节数、核心结论列表）

    Returns:
        questions: 理解测试题列表
    """
    # 根据报告字数确定题目数量（§2.1）
    word_count = report_metadata.get("word_count", 0)
    if word_count < 5000:
        num_questions = 5
    elif word_count < 20000:
        num_questions = 7
    elif word_count < 50000:
        num_questions = 8
    elif word_count < 100000:
        num_questions = 9
    else:
        num_questions = 10

    # 确保五类题型各至少 1 题
    question_types = ["fact_recall", "trend_judgment", "counter_evidence",
                      "boundary_conditions", "application_reasoning"]

    prompt = f"""
你是一个理解测试题设计专家。基于以下报告内容，生成 {num_questions} 个理解测试题。

## 报告内容
{report_content[:50000]}  # 截断防止上下文溢出

## 设计规则
1. 必须覆盖五类题型：{question_types}，每类至少 1 题
2. 每题必须指向报告中的具体章节（§X.X）
3. 每题必须提供预期答案（基于报告内容）
4. 题目难度分布：基础 40%、进阶 40%、挑战 20%
5. 避免模糊表述，答案必须有明确出处

## 输出格式（JSON）
{{
  "questions": [
    {{
      "question_id": "Q1",
      "question_type": "fact_recall | trend_judgment | counter_evidence | boundary_conditions | application_reasoning",
      "difficulty": "basic | intermediate | advanced",
      "question": "问题文本",
      "expected_answer": "预期答案（基于报告内容）",
      "source_section": "§X.X",
      "scoring_criteria": "评分标准（什么算 fully_correct/partially_correct/incorrect）"
    }}
  ]
}}
"""
    result = invoke_llm(prompt)
    return result["questions"]
```

## 3. LLM 判定流程（SubTask 5.5.2）

### 3.1 模拟读者作答

理解测试题生成后，由**独立 LLM 实例**（模拟读者）作答。模拟读者必须满足以下条件：

1. **独立上下文**：模拟读者仅能看到报告全文，看不到预期答案
2. **独立会话**：模拟读者与题目生成 LLM 必须是不同会话，避免上下文污染
3. **角色设定**：模拟读者设定为"目标读者画像"（如行业从业者/学术研究者/普通公众）

```python
def simulate_reader_answer(question: dict, report_content: str, reader_persona: str) -> str:
    """模拟读者作答。

    Args:
        question: 理解测试题
        report_content: 报告全文（模拟读者可阅读）
        reader_persona: 读者画像（如"行业从业者"）

    Returns:
        reader_answer: 模拟读者的回答
    """
    prompt = f"""
你是一位{reader_persona}。请基于以下报告内容，回答问题。

## 报告内容
{report_content}

## 问题
{question['question']}

## 作答规则
1. 仅基于报告内容回答，不引入外部知识
2. 若报告中未涉及，明确标注"报告未提及"
3. 回答需完整、具体，避免模糊表述
"""
    return invoke_llm(prompt)
```

### 3.2 LLM 判定回答与报告结论一致性

模拟读者作答后，由**判定 LLM**（第三个独立 LLM 实例）对比读者回答与预期答案，判定一致性：

```python
def judge_answer_consistency(question: dict, reader_answer: str, report_content: str) -> dict:
    """判定读者回答与报告结论的一致性。

    Args:
        question: 理解测试题（含 expected_answer 和 scoring_criteria）
        reader_answer: 模拟读者的回答
        report_content: 报告全文（用于验证答案出处）

    Returns:
        judgment: 判定结果
    """
    prompt = f"""
你是一个严格的读者理解测试判定员。你的任务是判定读者的回答是否与报告结论一致。

## 报告相关章节
{report_content[question['source_section_range']]}  # 仅截取相关章节

## 问题
{question['question']}

## 预期答案
{question['expected_answer']}

## 评分标准
{question['scoring_criteria']}

## 读者回答
{reader_answer}

## 判定规则
1. 逐条对比读者回答与预期答案的关键信息点
2. 判定级别：
   - fully_correct：所有关键信息点准确复述，无错误、无遗漏
   - partially_correct：部分关键信息点准确复述，但有遗漏或轻微错误
   - incorrect：大部分关键信息点未复述或有严重错误
3. 列出已正确复述的信息点（correct_points）和遗漏/错误的信息点（missed_points）
4. 给出判定理由（rationale）

## 输出格式（JSON）
{{
  "verdict": "fully_correct | partially_correct | incorrect",
  "correct_points": ["已正确复述的信息点"],
  "missed_points": ["遗漏或错误的信息点"],
  "rationale": "判定理由"
}}
"""
    return invoke_llm(prompt)
```

### 3.3 三方独立原则

理解测试涉及三个独立 LLM 实例，避免自评偏差：

| 角色 | 职责 | 独立性要求 |
|------|------|----------|
| 题目生成 LLM | 基于报告生成测试题 | 独立会话，看不到读者回答 |
| 模拟读者 LLM | 阅读报告并作答 | 独立会话，看不到预期答案 |
| 判定 LLM | 对比读者回答与预期答案 | 独立会话，仅看相关章节 |

> **关键声明**：三方独立原则确保测试结果客观。若三方不独立（如题目生成 LLM 同时作判定），会导致判定偏向宽松，掩盖可读性问题。

## 4. 三级评定（SubTask 5.5.3）

### 4.1 评定级别定义

| 评定级别 | 条件 | 分值 | 处理 |
|---------|------|------|------|
| **fully_correct** | 所有关键信息点准确复述，无错误、无遗漏 | 1.0 | 计入理解率分子 |
| **partially_correct** | 部分关键信息点准确复述，但有遗漏或轻微错误 | 0.5 | 计入理解率分子（按 0.5 计） |
| **incorrect** | 大部分关键信息点未复述或有严重错误 | 0.0 | 不计入理解率分子 |

### 4.2 评定示例

**fully_correct 示例**：
- 问题：报告指出 2025 年中国新能源汽车出口量同比增长了多少？
- 预期答案：30%
- 读者回答：根据报告 §3.2，2025 年中国新能源汽车出口量同比增长 30%。
- 判定：fully_correct（关键数据准确复述，出处正确）

**partially_correct 示例**：
- 问题：报告指出全球半导体市场份额在 2020-2025 年间呈现什么趋势？主要驱动因素是什么？
- 预期答案：呈上升趋势，主要驱动因素是 AI 芯片需求爆发和国产替代加速。
- 读者回答：呈上升趋势。驱动因素是市场需求增加。
- 判定：partially_correct（趋势方向正确，但驱动因素描述模糊，遗漏"AI 芯片"和"国产替代"两个关键点）

**incorrect 示例**：
- 问题：报告 §6.3 提出了哪些反对"AI 将导致大规模失业"的反证？
- 预期答案：反证包括（1）历史数据显示技术革命创造新岗位；（2）AI 催生新职业。
- 读者回答：报告认为 AI 不会导致失业。
- 判定：incorrect（仅复述主结论，完全遗漏反证的具体内容）

## 5. 理解率统计与可读性优化触发（SubTask 5.5.4）

### 5.1 理解率计算

```python
def calculate_comprehension_rate(judgments: list) -> dict:
    """计算理解率。

    Args:
        judgments: 判定结果列表

    Returns:
        comprehension_stats: 理解率统计
    """
    total = len(judgments)
    fully_correct = sum(1 for j in judgments if j["verdict"] == "fully_correct")
    partially_correct = sum(1 for j in judgments if j["verdict"] == "partially_correct")
    incorrect = sum(1 for j in judgments if j["verdict"] == "incorrect")

    # 理解率 = (fully_correct × 1.0 + partially_correct × 0.5) / total
    comprehension_rate = (fully_correct * 1.0 + partially_correct * 0.5) / total if total > 0 else 0.0

    return {
        "total_questions": total,
        "fully_correct": fully_correct,
        "partially_correct": partially_correct,
        "incorrect": incorrect,
        "comprehension_rate": comprehension_rate,
        "verdict_distribution": {
            "fully_correct_rate": fully_correct / total if total > 0 else 0.0,
            "partially_correct_rate": partially_correct / total if total > 0 else 0.0,
            "incorrect_rate": incorrect / total if total > 0 else 0.0,
        },
    }
```

### 5.2 <70% 触发可读性优化

当理解率 < 70% 时，触发可读性优化流程：

```yaml
readability_optimization:
  trigger: "comprehension_rate < 0.70"
  optimization_steps:
    - step_1_diagnose:
        description: "诊断可读性问题根因"
        actions:
          - 提取所有 incorrect 和 partially_correct 的题目
          - 分析失败模式：
            - 事实回忆失败 → 报告中关键事实表述模糊或位置隐蔽
            - 趋势判断失败 → 数据呈现方式不直观（如缺少图表）
            - 反证理解失败 → 反证段落与主结论混淆，缺乏明确标注
            - 边界条件失败 → 前提假设未在显著位置声明
            - 应用推演失败 → 因果机制阐述不清晰
          - 生成 readability_diagnosis_report
    - step_2_optimize:
        description: "执行可读性优化"
        actions:
          - 重写失败题目对应的报告章节
          - 优化策略：
            - 关键事实加粗或使用 callout 框标注
            - 趋势数据增加可视化图表
            - 反证段落使用明确的"反证"标题标注
            - 前提假设在章节开头集中声明
            - 因果机制使用流程图或因果链图示
          - 优化后重新生成报告
    - step_3_retest:
        description: "重新执行理解测试"
        actions:
          - 对优化后的报告重新生成测试题
          - 重新模拟读者作答
          - 重新判定一致性
          - 计算新的理解率
    - step_4_verify:
        description: "验证优化效果"
        actions:
          - 若新理解率 ≥ 70% → 优化成功，进入交付
          - 若新理解率仍 < 70% → 持续优化，不设重试上限
          - 每次优化记录到 readability_optimization_log
```

### 5.3 理解率阈值

| 理解率 | 判定 | 处理 |
|--------|------|------|
| ≥ 90% | 优秀 | 直接交付 |
| 70%-89% | 合格 | 交付，但标注可读性改进建议 |
| < 70% | 不合格 | 触发可读性优化，持续重试直至 ≥ 70% |

### 5.4 理解率报告写入

理解测试完成后，生成理解率报告并写入 NRSF：

```yaml
comprehension_test_report:
  session_id: "会话 ID"
  report_id: "报告 ID"
  test_timestamp: "ISO8601"
  questions_generated: integer
  reader_persona: "模拟读者画像"
  judgments:
    - question_id: "Q1"
      question_type: "fact_recall"
      difficulty: "basic"
      verdict: "fully_correct"
      correct_points: ["..."]
      missed_points: ["..."]
      rationale: "..."
  comprehension_stats:
    total_questions: integer
    fully_correct: integer
    partially_correct: integer
    incorrect: integer
    comprehension_rate: float
  verdict: "excellent | pass | fail"
  optimization_triggered: boolean
  optimization_log: ["..."]  # 若触发优化
```

## 6. 难度分级（SubTask 5.5.5）

### 6.1 三级难度定义

| 难度级别 | 占比 | 定义 | 示例 |
|---------|------|------|------|
| **基础（basic）** | 40% | 直接复述报告中的事实、数据、定义，无需推理 | "报告指出 2025 年新能源汽车出口增长多少？" |
| **进阶（intermediate）** | 40% | 需要理解报告中的趋势、反证、边界条件，涉及轻度推理 | "报告中的反证如何限定主结论的适用范围？" |
| **挑战（advanced）** | 20% | 需要基于报告结论进行应用推演，将结论迁移到新场景 | "若碳关税税率提高 50%，基于报告的因果分析，影响如何变化？" |

### 6.2 难度分配规则

- 5 题方案：基础 2 题 + 进阶 2 题 + 挑战 1 题
- 7 题方案：基础 3 题 + 进阶 3 题 + 挑战 1 题
- 8 题方案：基础 3 题 + 进阶 3 题 + 挑战 2 题
- 9 题方案：基础 4 题 + 进阶 4 题 + 挑战 1 题（或基础 3 + 进阶 4 + 挑战 2）
- 10 题方案：基础 4 题 + 进阶 4 题 + 挑战 2 题

### 6.3 难度与题型交叉矩阵

| 题型 \ 难度 | 基础 | 进阶 | 挑战 |
|------------|------|------|------|
| 事实回忆 | ✓ 常见 | ✓ 可选 | ✗ 不适用 |
| 趋势判断 | ✓ 可选 | ✓ 常见 | ✓ 可选 |
| 反证理解 | ✗ 不适用 | ✓ 常见 | ✓ 可选 |
| 边界条件 | ✗ 不适用 | ✓ 常见 | ✓ 可选 |
| 应用推演 | ✗ 不适用 | ✗ 不适用 | ✓ 常见 |

### 6.4 难度加权理解率

除总体理解率外，还计算难度加权理解率，用于识别"表面理解但深层不理解"的情况：

```python
def calculate_weighted_comprehension_rate(judgments: list) -> dict:
    """计算难度加权理解率。"""
    weights = {"basic": 0.5, "intermediate": 1.0, "advanced": 1.5}

    weighted_total = sum(weights[j["difficulty"]] for j in judgments)
    weighted_correct = sum(
        weights[j["difficulty"]] * (1.0 if j["verdict"] == "fully_correct" else
                                    0.5 if j["verdict"] == "partially_correct" else 0.0)
        for j in judgments
    )

    weighted_rate = weighted_correct / weighted_total if weighted_total > 0 else 0.0

    # 分难度统计
    difficulty_stats = {}
    for diff in ["basic", "intermediate", "advanced"]:
        diff_judgments = [j for j in judgments if j["difficulty"] == diff]
        if diff_judgments:
            diff_rate = sum(
                1.0 if j["verdict"] == "fully_correct" else
                0.5 if j["verdict"] == "partially_correct" else 0.0
                for j in diff_judgments
            ) / len(diff_judgments)
            difficulty_stats[diff] = {
                "count": len(diff_judgments),
                "comprehension_rate": diff_rate,
            }

    return {
        "weighted_comprehension_rate": weighted_rate,
        "difficulty_stats": difficulty_stats,
    }
```

**异常检测规则**：
- 若基础理解率 ≥ 80% 但挑战理解率 < 40% → 标注"表面理解风险"，触发可读性优化（针对挑战难度章节）
- 若挑战理解率 ≥ 80% 但基础理解率 < 60% → 标注"基础事实表述模糊"，触发可读性优化（针对基础事实章节）

## 7. 执行流程

```
T19 交付守卫通过
    ↓
T20 渲染完成
    ↓
生成 5-10 个理解测试题（§2）
    ↓
模拟读者作答（§3.1）
    ↓
判定 LLM 对比一致性（§3.2）
    ↓
计算理解率（§5.1）
    ↓
理解率 ≥ 70%？
    ├─ 是 → 交付（标注可读性评级）
    └─ 否 → 触发可读性优化（§5.2）
              ↓
              优化后重新测试
              ↓
              理解率 ≥ 70%？
              ├─ 是 → 交付
              └─ 否 → 持续优化，不设重试上限
```

## 8. 与其他协议的关系

- **self-evaluation-protocol.md**：理解测试是 T19 交付守卫的补充，T19 通过后执行理解测试
- **output-rendering-protocol.md**：可读性优化可能触发 T20 重新渲染
- **user-feedback-protocol.md**：用户反馈可触发理解测试重跑
- **context-budget-protocol.md**：理解测试题生成与判定消耗上下文预算，需纳入预算管理

## 9. 异常处理与穷尽重试

| 异常场景 | 处理策略 |
|---------|---------|
| LLM 生成测试题失败 | 持续重试直至生成成功，不设重试上限 |
| 模拟读者 LLM 不可用 | 持续重试直至可用，不跳过模拟读者环节 |
| 判定 LLM 不可用 | 持续重试直至可用，不跳过判定环节 |
| 理解率持续 < 70% | 持续优化报告，不设重试上限，不降低理解率标准 |
| 三方独立原则被破坏（如同一 LLM 实例） | 标注"独立性受损"，重新分配 LLM 实例后重跑 |

---

## 测试用例（R8-04）

> **测试用例格式声明**：每个测试用例遵循「给定输入 X，应产出 Y」格式，覆盖理解测试的关键路径与边界条件。

### TC-1: 基础事实回忆题（fully_correct）

**给定输入**：
- 报告 §3.2 指出"2025 年中国新能源汽车出口量同比增长 30%"
- 生成测试题：Q1，题型=fact_recall，难度=basic
- 问题："根据报告，2025 年中国新能源汽车出口量同比增长了多少百分比？"
- 模拟读者回答："根据报告 §3.2，2025 年中国新能源汽车出口量同比增长 30%。"

**应产出**：
- judge_answer_consistency 返回 `verdict: "fully_correct"`
- correct_points: ["准确复述增长率为 30%", "正确引用章节 §3.2"]
- missed_points: []
- 计入理解率：fully_correct × 1.0

### TC-2: 趋势判断题（partially_correct）

**给定输入**：
- 报告 §4.1 指出"全球半导体市场份额从 2020 年的 12% 上升至 2025 年的 18%，主要驱动因素是 AI 芯片需求爆发和国产替代加速"
- 生成测试题：Q2，题型=trend_judgment，难度=intermediate
- 问题："全球半导体市场份额在 2020-2025 年间呈现什么趋势？主要驱动因素是什么？"
- 模拟读者回答："呈上升趋势。驱动因素是市场需求增加。"

**应产出**：
- judge_answer_consistency 返回 `verdict: "partially_correct"`
- correct_points: ["趋势方向正确（上升）"]
- missed_points: ["未提及具体数据（12%→18%）", "驱动因素描述模糊，遗漏'AI 芯片'和'国产替代'"]
- 计入理解率：partially_correct × 0.5

### TC-3: 应用推演题（incorrect）

**给定输入**：
- 报告 §5.3 指出"碳关税将使中国新能源汽车出口成本上升 8-12%，因果链为：碳关税 → 碳排放核算 → 成本内部化 → 出口价格上升"
- 生成测试题：Q3，题型=application_reasoning，难度=advanced
- 问题："若欧盟将碳关税税率提高 50%，基于报告的因果分析，对中国新能源汽车出口的影响会如何变化？"
- 模拟读者回答："中国新能源汽车出口会减少。"

**应产出**：
- judge_answer_consistency 返回 `verdict: "incorrect"`
- correct_points: []
- missed_points: ["未基于因果链推演", "未量化影响幅度（应从 8-12% 扩大至 12-18%）", "未分析对不同车型的影响差异"]
- 计入理解率：incorrect × 0.0

### TC-4: 理解率 <70% 触发可读性优化

**给定输入**：
- 某报告生成 7 个测试题
- 判定结果：2 题 fully_correct，1 题 partially_correct，4 题 incorrect
- 理解率 = (2×1.0 + 1×0.5 + 4×0.0) / 7 = 2.5/7 ≈ 0.357（< 0.70）

**应产出**：
- calculate_comprehension_rate 返回：
  ```yaml
  total_questions: 7
  fully_correct: 2
  partially_correct: 1
  incorrect: 4
  comprehension_rate: 0.357
  verdict: fail
  ```
- 触发 readability_optimization 流程：
  - step_1_diagnose：分析 4 题 incorrect 的失败模式（如"反证段落与主结论混淆"）
  - step_2_optimize：重写反证段落，使用明确"反证"标题标注
  - step_3_retest：重新生成测试题、模拟作答、判定
  - step_4_verify：若新理解率 ≥ 70% → 交付；否则持续优化

### TC-5: 难度加权理解率异常检测

**给定输入**：
- 某报告 8 个测试题：基础 3 题、进阶 3 题、挑战 2 题
- 判定结果：
  - 基础：3 题 fully_correct → 基础理解率 = 100%
  - 进阶：2 题 partially_correct，1 题 incorrect → 进阶理解率 = 33%
  - 挑战：2 题 incorrect → 挑战理解率 = 0%

**应产出**：
- calculate_weighted_comprehension_rate 返回：
  ```yaml
  weighted_comprehension_rate: 0.3125
  difficulty_stats:
    basic:
      count: 3
      comprehension_rate: 1.0
    intermediate:
      count: 3
      comprehension_rate: 0.33
    advanced:
      count: 2
      comprehension_rate: 0.0
  ```
- 异常检测：基础理解率 ≥ 80% 但挑战理解率 < 40% → 标注"表面理解风险"
- 触发可读性优化：针对挑战难度章节（因果机制、应用推演相关内容）优化
