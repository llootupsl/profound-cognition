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