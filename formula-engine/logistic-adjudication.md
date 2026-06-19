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