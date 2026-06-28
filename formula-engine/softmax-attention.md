<!-- 作者：阿洋 -->

# Softmax 动态注意力加权 (Softmax Dynamic Attention Weighting)

> 模块标识: formula-engine/softmax-attention
> 能力卡编号: FE-001
> 职责: 将路径/证据的强度得分转换为归一化权重，替代等权平均
> 调用位置: T12b（三路对抗交叉融合）、T13（认知综合）

## 数学形式
w_i = exp(s_i) / Σ exp(s_j)

其中 s_i 为路径/证据 i 的强度得分（来自 T10/T11/T12 的攻击/辩护结果）。

## 输入
- s_i: 各路径/证据的强度得分，范围 [0, 10]，由三路对抗（T10/T11/T12）产出

## 输出
- w_i: 归一化权重，Σ w_i = 1

## 使用规则
1. 可服/不可反驳/证据扎实的路径 → s_i 高 → 自动获得更高权重
2. 被击穿/证据薄弱的路径 → s_i 低 → 自动降低权重
3. 温度参数 T 控制权重分布的熵（默认 T=1.0，T 越大权重越均匀）

## 调用示例
在 T12b 证据融合步骤中：
1. 收集 T10/T11/T12 产出的每条路径强度得分 s_i
2. 计算 w_i = exp(s_i / T) / Σ exp(s_j / T)
3. 以 w_i 为权重整合各路径结论

## 异常处理：穷尽尝试所有替代计算路径

- 当所有 s_i = 0（零输入）→ 穷尽重试为等权平均 w_i = 1/N，标注 formula_retrying=true, reason='softmax_zero_input'
- 当 s_i 包含极端值（|s_i| > 100）→ 先做 min-max 归一化到 [0, 10] 再计算，标注 formula_retrying=true, reason='softmax_extreme_input'
- 当温度参数 T → 0 → 穷尽重试为 argmax（赢者通吃），标注 formula_retrying=true, reason='softmax_zero_temperature'

## 数值稳定版本（D4.4.2 — 减最大值后 exp）

### 问题背景
当 s_i 较大时（如 s_i > 700），`exp(s_i)` 会超出浮点数表示范围导致溢出（`inf`）。虽然当前 s_i 范围为 [0, 10] 不易触发，但在以下场景仍需防御：
- 温度参数 T 极小时（如 T=0.01），`s_i / T` 可达 1000，`exp(1000)` 必溢出
- 异常输入未归一化时
- 未来扩展 s_i 范围时

### 数值稳定公式

```
w_i = exp(s_i - max(s)) / Σ exp(s_j - max(s))
```

其中 `max(s) = max(s_1, s_2, ..., s_N)`。

**数学等价性证明**：
- 原式：`w_i = exp(s_i) / Σ exp(s_j)`
- 稳定式：`w_i = exp(s_i - m) / Σ exp(s_j - m)`，其中 `m = max(s)`
- 展开：`= [exp(s_i) · exp(-m)] / [Σ exp(s_j) · exp(-m)]`
- 约去 `exp(-m)`：`= exp(s_i) / Σ exp(s_j)`
- 与原式**完全等价**

### 实现伪代码

```python
def softmax_stable(scores, temperature=1.0):
    """
    数值稳定的 Softmax 实现（D4.4.2）
    减最大值后 exp，避免溢出
    """
    # 1. 温度缩放
    scaled = [s / temperature for s in scores]
    
    # 2. 减最大值（数值稳定关键步骤）
    max_val = max(scaled)
    shifted = [s - max_val for s in scaled]
    
    # 3. 计算 exp（此时所有值 <= 0，exp 结果在 (0, 1]，不会溢出）
    exps = [math.exp(s) for s in shifted]
    
    # 4. 归一化
    total = sum(exps)
    weights = [e / total for e in exps]
    
    return weights
```

### 异常处理更新
- **原**：当 s_i 包含极端值（|s_i| > 100）→ 先做 min-max 归一化到 [0, 10] 再计算
- **新**：数值稳定版本自动处理极端值（减最大值后所有 exp 参数 ≤ 0，不会溢出），但仍保留 min-max 归一化作为输入净化的最佳实践
- 当温度参数 T → 0 → 穷尽重试为 argmax（赢者通吃），标注 `formula_retrying=true, reason='softmax_zero_temperature'`
- 当所有 s_i 相等 → 减最大值后全为 0，exp(0)=1，结果为等权 1/N（自然退化，无需特殊处理）

### 验证测试用例

| 输入 | 原始实现 | 稳定实现 | 结果一致 |
|------|---------|---------|---------|
| [1.0, 2.0, 3.0] | [0.09, 0.24, 0.67] | [0.09, 0.24, 0.67] | ✅ |
| [1000, 1001, 1002] | [inf, inf, inf] → NaN | [0.09, 0.24, 0.67] | ✅ 稳定版正确 |
| [0, 0, 0] | [0.33, 0.33, 0.33] | [0.33, 0.33, 0.33] | ✅ |

## 数学原理交叉引用（D12.4.1）

| 数学原理编号 | 原理名称 | 关联说明 |
|------------|---------|---------|
| MP-024 | 信息论 (Information Theory) | Softmax 是信息熵最大化的分布（最大熵原理） |
| MP-025 | 熵 (Entropy) | 温度参数 T 控制输出分布的熵，T 越大熵越大（越均匀） |
| MP-026 | KL 散度与互信息 (KL Divergence) | Softmax 输出与均匀分布的 KL 散度衡量路径强度的分化程度 |

> 详见 `knowledge/math-principles-72.md` 第 24/25/26 项原理