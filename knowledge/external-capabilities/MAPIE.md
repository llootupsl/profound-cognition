<!-- 作者：阿洋 -->


> **版本治理元数据 (D12.4.2)**:
> - version: 1.0
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（能力卡补全版本治理元数据，D12.4.2）

# MAPIE

## 基本信息
- **工具名称**: MAPIE (Model Agnostic Prediction Interval Estimator)
- **类型**: 不确定性量化与置信度校准
- **优先级**: P1
- **层级**: L1

## 功能描述

MAPIE（Model Agnostic Prediction Interval Estimator）是模型无关的预测区间估计库，为模型预测提供校准的预测区间并给出覆盖率保证。通过 conformal prediction（一致性预测）框架，MAPIE 能够在任意预训练模型之上构建统计有效的预测区间，区间覆盖率有理论保证（在交换性假设下，实际覆盖率 ≥ 1 - α）。

在 Profound Cognition 体系中，MAPIE 用于 T13（认知综合）阶段，为综合结论提供校准的置信度区间，将连续的覆盖率映射为离散的置信度等级（HIGH/MEDIUM/LOW/TENTATIVE），替代人工主观评定的置信度，实现置信度评定的可校准性与可验证性。

## 核心能力

- **预测区间估计**：为任意模型预测提供校准的预测区间，区间宽度反映预测不确定性
- **覆盖率保证**：基于 conformal prediction 框架，提供边际覆盖率保证（P(y ∈ interval) ≥ 1 - α）
- **模型无关**：适用于回归、分类、时序等各类预训练模型，无需修改模型本身
- **校准集驱动**：通过独立的校准集（calibration set）估计预测误差分布，生成区间
- **多 α 等级支持**：支持同时输出多个置信度等级的区间（如 90%、80%、50%）

## 调用前置条件

- **Python 版本**: Python 3.8+
- **依赖库**: `mapie`（`pip install mapie`）
- **校准集**: 需提供独立的校准集（来自 T02-T06 的已验证事实，L0-L2 级证据）
- **预训练模型**: 需有可用的预测模型（综合结论的评分模型或置信度估计模型）

## 调用指令

### 输入参数
- `model` (object, 预训练预测模型)
- `X_calib` (array, 校准集特征，来自 T02-T06 已验证事实)
- `y_calib` (array, 校准集标签，来自 T02-T06 已验证事实的验证状态)
- `X_test` (array, 待预测样本特征，即 T13 综合结论的嵌入表示)
- `alpha` (float, 显著性水平，默认 0.1，对应 90% 覆盖率)
- `method` (string, conformal prediction 方法，默认 "prefit")

### 输出格式
预测区间数组，每条含 lower_bound、upper_bound、coverage_rate、interval_width

### 调用示例
```python
from mapie.regression import MapieRegressor
from sklearn.linear_model import LinearRegression

# 使用 T02-T06 已验证事实作为校准集
model = LinearRegression().fit(X_train, y_train)
mapie = MapieRegressor(estimator=model, method="prefit")
mapie.fit(X_calib, y_calib)  # X_calib/y_calib 来自 T02-T06 已验证事实

# 为 T13 综合结论生成预测区间
y_pred, intervals = mapie.predict(X_test, alpha=0.1)

# intervals[:, :, 0] 为下界，intervals[:, :, 1] 为上界
coverage_rate = 1 - alpha  # 0.9
interval_width = np.mean(intervals[:, :, 1] - intervals[:, :, 0])
```

## 失败回退策略

当 MAPIE 不可用时（库未安装、校准集不足、模型不可用），按以下层级穷尽重试：

```yaml
fallback_strategy:
  L1_FULL:
    condition: "MAPIE 可用 + 校准集充分（≥ 30 条已验证事实）"
    action: "完整执行 conformal prediction，输出校准的预测区间"
    confidence_level: "由 MAPIE 覆盖率映射"

  L2_SMALL_CALIB:
    condition: "MAPIE 可用但校准集不足（< 30 条）"
    action: "使用可用校准集执行 conformal prediction，标注区间宽度估计不稳定"
    confidence_level: "覆盖率映射，但标注 [CALIB_SMALL]"

  L3_FIXED_CONFIDENCE:
    condition: "MAPIE 不可用（库未安装或模型不可用）"
    action: "回退到固定置信度 0.8（MEDIUM 等级），所有结论标注 [NO_MAPIE_CALIB]"
    confidence_level: "MEDIUM（固定 0.8 覆盖率）"

  L4_INTERNAL_REASONING:
    condition: "校准集完全缺失（无 T02-T06 已验证事实）"
    action: "使用 LLM 内建能力进行置信度估计，标注 [INTERNAL_REASONING]"
    confidence_level: "由 LLM 主观评定，上限为 MEDIUM"
```

**铁律**：回退到固定置信度（0.8）时，必须在 NRSF 日志中标注 `fallback_reason`，且所有结论的 confidence_level 不可全部为 HIGH。

## 效果度量

| 度量指标 | 定义 | 目标值 |
|----------|------|--------|
| **coverage_rate** | 实际覆盖率（校准集中真实值落入区间的比例） | ≥ 1 - α（如 α=0.1 时 ≥ 0.9） |
| **interval_width** | 预测区间的平均宽度 | 越窄越好，但须满足覆盖率保证 |

效果度量写入 NRSF `§mapie_log` 字段，供 T19 校准检查消费。

## 版本同步

- 与官方 `mapie` 库（https://github.com/scikit-learn-contrib/MAPIE）同步
- 当前适配版本：mapie ≥ 0.9
- 版本变更时需重新验证覆盖率保证是否仍成立
- 新版本 API 变更需同步更新本卡片及 T13 调用代码

## 消费关系

### 消费此卡片的 DAG 节点

- **T13（认知综合）**: 使用 MAPIE 为综合结论提供校准的预测区间，输出每个结论的置信度区间
- **T19（交付守卫）**: 校准检查——验证所有结论的置信度等级是否来自 MAPIE 校准

### 校准集来源

校准集来自 T02-T06 的已验证事实（L0-L2 级证据）：
- **T02（L1 基础事实 + L2 时间演化）**: `factual_checklist` 中 `verification_status = verified` 的事实
- **T03（L3 结构变量）**: 已验证的变量关系
- **T04（L4 利益相关者 + L5 情景）**: 已验证的利益相关者分析
- **T05（L6 证据边界 + L7 利益相关者）**: `evidence_strength ≥ 0.5` 的主张
- **T06（L8 反事实 + L9 知识边界）**: 已验证的反事实分析

校准集用于 MAPIE 的 conformal prediction，确保预测区间具有边际覆盖率保证。

## 连续覆盖率到离散等级映射

MAPIE 输出的连续 coverage_rate 映射为 T13 的离散 confidence_rating：

| 覆盖率区间 | 置信度等级 | 含义 |
|------------|-----------|------|
| coverage_rate ≥ 0.9 | HIGH | 高置信度——区间窄且覆盖率有保证 |
| 0.7 ≤ coverage_rate < 0.9 | MEDIUM | 中置信度——覆盖率基本保证 |
| 0.5 ≤ coverage_rate < 0.7 | LOW | 低置信度——覆盖率不足 |
| coverage_rate < 0.5 | TENTATIVE | 暂定——覆盖率严重不足，结论待验证 |

> 知识来源: MAPIE (Model Agnostic Prediction Interval Estimator)
