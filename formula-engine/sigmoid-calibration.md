<!-- 作者：阿洋 -->

# Sigmoid 置信度校准函数 (Sigmoid Confidence Calibration)

> 模块标识: formula-engine/sigmoid-calibration
> 能力卡编号: FE-004
> 职责: 把原始线性得分压缩成符合人类认知的置信度分布
> 调用位置: Gate 判定步骤中 Supervisor 输出置信度之前

## 数学形式
CalibratedConf(x) = 1 / (1 + exp(-k(x - μ)))

其中 x = 原始线性得分 [0, 1]，k = 陡峭度，μ = 中点偏移。

## 参数（默认值）
- k = 10（陡峭度，越大 sigmoid 越陡）
- μ = 0.5（中点偏移，x = μ 时 CalibratedConf = 0.5）

## 使用规则
1. Supervisor 计算原始线性得分 x 后
2. 通过 CalibratedConf(x) 校准
3. 校准后的值作为最终置信度输出

## 效果
- 中间区域（0.3-0.7）被拉伸 → 不确定性更清晰
- 极端值（<0.1, >0.9）被压缩 → 避免过度自信

## 异常处理：穷尽尝试所有替代计算路径

- 当 k 或 μ 参数不可用 → 穷尽尝试从历史校准数据中拟合参数，若仍不可用则使用默认值 k=10, μ=0.5，标注 formula_retrying=true, reason='sigmoid_default_params'
- 当原始得分 x 超出 [0, 1] → 先做 min-max 归一化到 [0, 1]，标注 formula_retrying=true, reason='sigmoid_input_normalized'

## 数学原理交叉引用（D12.4.1）

| 数学原理编号 | 原理名称 | 关联说明 |
|------------|---------|---------|
| MP-003 | 非线性动力学 (Nonlinear Dynamics) | Sigmoid 是非线性 S 型映射，将线性得分映射为非线性置信度 |
| MP-041 | 前景理论与累积前景理论 (Prospect Theory) | 中间区域拉伸/极端值压缩符合人类前景理论中的概率加权特征 |
| MP-050 | 凸优化 (Convex Optimization) | Sigmoid 的 S 型曲线是凸优化的经典激活函数 |

> 详见 `knowledge/math-principles-72.md` 第 3/41/50 项原理