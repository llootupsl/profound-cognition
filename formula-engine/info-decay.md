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

## 异常处理：穷尽尝试所有替代计算路径

- 当无法计算 ΔInfo(t)（无前轮对比数据）→ 穷尽尝试所有可用估算方法重建基线，若仍无法计算则由质量驱动终止条件决定，标注 formula_retrying=true, reason='info_decay_no_baseline'
- 当 α 或 λ 参数不可用 → 穷尽尝试从已有迭代数据中拟合参数，若仍不可用则使用默认值 α=1.0, λ=0.3，标注 formula_retrying=true, reason='info_decay_default_params'