<!-- 作者：阿洋 -->

# 指数边际收益衰减模型 (Exponential Marginal Info Decay)

> 模块标识: formula-engine/info-decay
> 能力卡编号: FE-003
> 职责: 用每轮新增有效信息量的衰减曲线判断是否停止迭代
> 调用位置: context-budget-protocol.md 迭代终止逻辑 + I01 停止条件

## 数学形式
ΔInfo(t) = α · exp(-λt)

其中 t = 当前迭代轮次，α = 初始信息增益率，λ = 衰减系数。

## 参数（默认值）
- α = 1.0（初始信息增益率，第一轮可获取的信息量基准）
- λ = 0.3（衰减系数，越大衰减越快）
- ε = 0.05（终止阈值，ΔInfo(t) < ε 时自动终止）

## 使用规则
1. 每轮迭代后计算 ΔInfo(t)
2. 当 ΔInfo(t) < ε 时：自动终止迭代，标记为"信息增益收敛"
3. 不做固定轮数上限限制——衰减模型动态决定何时停止

## 替代说明
替代原硬阈值：depth_satisfaction ≥ 0.8 且质量驱动终止条件。

> **【A6.2-F8 修复，2026-06-27】旧值说明**：上述 `depth_satisfaction ≥ 0.8` 为 v5.x 旧阈值。v6.0 起当前系统实际阈值已更新为 `depth_satisfaction ≥ 0.85`（权威定义见 tasks/T13_cog_synthesize.md L28-29 / SKILL.md L2074 / CHANGELOG.md L89）。本式保留 0.8 仅作为"被替代的旧阈值"的历史引用，不代表当前生效阈值。

## 异常处理：穷尽尝试所有替代计算路径

- 当无法计算 ΔInfo(t)（无前轮对比数据）→ 穷尽尝试所有可用估算方法重建基线，若仍无法计算则由质量驱动终止条件决定，标注 formula_retrying=true, reason='info_decay_no_baseline'
- 当 α 或 λ 参数不可用 → 穷尽尝试从已有迭代数据中拟合参数，若仍不可用则使用默认值 α=1.0, λ=0.3，标注 formula_retrying=true, reason='info_decay_default_params'

## 场景化 ε 配置（D4.4.3 — 学术/商业场景差异化）

### 设计理由
不同场景对信息增益的敏感度不同：
- **学术研究**：追求穷尽性，即使微小的信息增量也有价值，应使用更小的 ε 延长迭代
- **商业分析**：注重效率，信息增量过小时应及时终止，避免过度投入

### 场景化 ε 配置表

```yaml
epsilon_config:
  academic:
    epsilon: 0.01                    # 学术场景：更严格，迭代更多轮
    description: "学术研究/论文/深度报告，追求穷尽性"
    max_iterations_hint: 15          # 建议最大迭代轮数（非硬性上限，EXHAUST 模式下仍无硬性上限）
    applicable_output_types: ["research_report"]
    
  commercial:
    epsilon: 0.05                    # 商业场景：当前默认值，平衡深度与效率
    description: "商业分析/决策建议/公众号文章，注重效率"
    max_iterations_hint: 8           # 建议最大迭代轮数（非硬性上限）
    applicable_output_types: ["wechat_article", "course_material"]
    
  default:
    epsilon: 0.05                    # 默认场景（未知/未指定时）
    description: "未明确场景时的默认配置，等同于商业场景"
```

### 场景识别规则（伪代码）

```python
def select_epsilon(output_type, research_depth_label=None):
    """
    根据输出类型和研究深度标签选择 ε（D4.4.3）
    """
    if output_type == "research_report":
        # research_report 默认使用学术 ε
        if research_depth_label == "commercial_brief":
            return 0.05  # 即使是 research_report，若标注为商业简报则用商业 ε
        return 0.01      # 学术 ε
    
    elif output_type in ["wechat_article", "course_material"]:
        return 0.05      # 商业 ε
    
    else:
        return 0.05      # 默认 ε
```

### 场景识别信号
- `output_type`: 从 T01 输入分流获取
- `research_depth_label`: 从 T00 研究大纲获取（可选，默认为 `"academic"`）
- **用户显式指定**: 用户在输入中明确指定 "深度研究"/"快速分析" 时覆盖自动识别

### 向下兼容
- 原 ε = 0.05 保持为 `default` 和 `commercial` 配置
- 现有引用 `info-decay.md` 的节点（I01、`context-budget-protocol.md`）无需修改，自动使用 `default` ε=0.05
- 新增 `academic` 场景时，I01 和 `context-budget-protocol.md` 可选读取场景化 ε

### ε 选择日志

```yaml
epsilon_selection_log:
  timestamp: "ISO 8601"
  output_type: "research_report"
  research_depth_label: "academic"
  selected_epsilon: 0.01
  selection_reason: "academic_scene_default"
  write_to: "execution_ledger.formula_config_log"
```

## 数学原理交叉引用（D12.4.1）

| 数学原理编号 | 原理名称 | 关联说明 |
|------------|---------|---------|
| MP-024 | 信息论 (Information Theory) | ΔInfo(t) 是信息增益的度量，ε 是信息增益的收敛阈值 |
| MP-023 | 随机过程 (Stochastic Processes) | 指数衰减是随机过程中常见的收敛模式 |
| MP-049 | 动态规划 (Dynamic Programming) | 迭代深化决策基于 ΔInfo(t) 的动态规划思想 |

> 详见 `knowledge/math-principles-72.md` 第 24/23/49 项原理