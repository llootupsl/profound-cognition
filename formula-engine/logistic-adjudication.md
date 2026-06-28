<!-- 作者：阿洋 -->

# Logistic 胜负判定函数 (Logistic Adjudication Function)

> 模块标识: formula-engine/logistic-adjudication
> 能力卡编号: FE-002
> 职责: 将攻击强度与辩护强度映射为 0-1 连续的攻击成功率
> 调用位置: T10（魔鬼代言人-逻辑攻击）结果判定步骤

## 数学形式
P(win) = 1 / (1 + exp(-(A - D)))

其中 A = 攻击强度（Attack），D = 辩护强度（Defense）。

## 输入
- A: 攻击强度 [0, 10]
- D: 辩护强度 [0, 10]

## 输出
- P(win): 攻击成功率 [0, 1]，连续值

## 判定阈值
- P(win) > 0.7: 攻击成功（原论证被击穿）
- 0.3 ≤ P(win) ≤ 0.7: 攻防均衡（论证部分有效）
- P(win) < 0.3: 攻击失败（原论证成立）

## 替代说明
替代原"有效/无效"二元硬判断，提供连续概率。

## 异常处理：穷尽尝试所有替代计算路径

- 当 |A - D| > 20（极端差值导致溢出）→ clamp P(win) 到 [0.01, 0.99]，标注 formula_retrying=true, reason='logistic_overflow_clamped'
- 当 A 或 D 无法量化 → 穷尽尝试所有可用估算方法，若仍无法量化则使用默认值 A=5.0, D=5.0（平局），标注 formula_retrying=true, reason='logistic_default_input'

## 参数校准机制（D4.4.1 — 基于历史数据动态调整阈值）

### 校准目标
固定阈值 0.7/0.3 在不同领域/场景下可能过严或过松。通过历史数据驱动的参数校准，使判定阈值适应当前使用场景的攻击-辩护分布特征，提升判定的实际准确率。

### 校准数据源
- 每次 T10 执行后，记录 `(A, D, P(win), actual_verdict)` 四元组到 `execution_ledger.formula_calibration_history`
- `actual_verdict`: 由 Supervisor 或人工标注的实际结果，取值 `"attack_succeeded" | "balanced" | "attack_failed"`
- 累计 ≥ 30 条记录后触发首次校准

### 校准算法（伪代码）

```python
def calibrate_logistic_thresholds(history):
    """
    基于历史数据动态调整 P(win) 判定阈值
    """
    # 1. 计算当前阈值的预测准确率
    correct = 0
    for record in history:
        predicted = classify_p_win(record.p_win, 
                                    threshold_high=0.7, 
                                    threshold_low=0.3)
        if predicted == record.actual_verdict:
            correct += 1
    accuracy = correct / len(history)
    
    # 2. 若准确率达标，保持当前阈值
    if accuracy >= 0.75:
        return {"threshold_high": 0.7, "threshold_low": 0.3, 
                "calibration_triggered": False}
    
    # 3. 准确率不达标，网格搜索最优阈值
    best_accuracy = 0
    best_thresholds = {"threshold_high": 0.7, "threshold_low": 0.3}
    for th_high in frange(0.6, 0.8, 0.01):
        for th_low in frange(0.2, 0.4, 0.01):
            if th_low >= th_high:
                continue
            acc = evaluate_thresholds(history, th_high, th_low)
            if acc > best_accuracy:
                best_accuracy = acc
                best_thresholds = {"threshold_high": th_high, 
                                   "threshold_low": th_low}
    
    # 4. 硬约束 clamp（防止漂移过大）
    best_thresholds["threshold_high"] = clamp(best_thresholds["threshold_high"], 0.6, 0.8)
    best_thresholds["threshold_low"] = clamp(best_thresholds["threshold_low"], 0.2, 0.4)
    best_thresholds["calibration_triggered"] = True
    return best_thresholds
```

### 校准参数配置

```yaml
calibration_config:
  min_samples: 30                    # 触发首次校准的最少样本数
  recalibration_cycle: 50            # 每 50 次执行重新校准一次
  accuracy_threshold: 0.75           # 低于此准确率触发阈值搜索
  search_range:
    threshold_high: [0.6, 0.8]       # 攻击成功阈值搜索范围
    threshold_low: [0.2, 0.4]        # 攻击失败阈值搜索范围
  search_step: 0.01                  # 网格搜索步长
  clamp_range:
    threshold_high: [0.6, 0.8]       # 校准后阈值硬约束范围（防止漂移过大）
    threshold_low: [0.2, 0.4]
```

### 校准日志格式

```yaml
calibration_log:
  timestamp: "ISO 8601"
  formula_id: "FE-002"
  samples_used: int
  pre_calibration_accuracy: float
  post_calibration_accuracy: float
  old_thresholds: {high: 0.7, low: 0.3}
  new_thresholds: {high: float, low: float}
  calibration_triggered: true|false
  write_to: "execution_ledger.formula_calibration_log"
```

### 校准安全约束
- 校准后阈值必须在 `clamp_range` 范围内（防止漂移过大导致判定失效）
- 校准**不修改公式本身**（`P(win) = 1/(1+exp(-(A-D)))` 不变），仅调整判定阈值
- 校准日志必须写入 `execution_ledger`，可审计可回溯
- 首次使用（无历史数据）时使用默认阈值 0.7/0.3
- 校准失败（如历史数据质量差）时回退到默认阈值，标注 `calibration_fallback: true`

## 数学原理交叉引用（D12.4.1）

| 数学原理编号 | 原理名称 | 关联说明 |
|------------|---------|---------|
| MP-003 | 非线性动力学 (Nonlinear Dynamics) | Logistic 函数是典型的非线性 S 型曲线，将线性差值 (A-D) 映射为非线性概率 |
| MP-024 | 信息论 (Information Theory) | P(win) 可视为攻击信息的传递效率，0.5 为信息熵最大点 |
| MP-041 | 前景理论 (Prospect Theory) | 0.7/0.3 阈值反映人类对"成功/失败"的认知不对称性 |

> 详见 `knowledge/math-principles-72.md` 第 3/24/41 项原理