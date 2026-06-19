<!-- 作者：阿洋 -->

# TC-066: MCDA — Multi-Criteria Decision Analysis

## 基本信息
- **名称**: MCDA (Multi-Criteria Decision Analysis)
- **类别**: 决策分析
- **语言**: 无专用工具
- **版本要求**: N/A
- **安装**: 无需安装（AHP/TOPSIS 手工计算）
- **许可证**: N/A
- **仓库**: N/A

## 核心能力
- 多准则决策分析
- AHP (层次分析法) 权重计算
- TOPSIS 综合评价
- 决策矩阵构建与一致性检验

## 在 profound-cognition 中的用途
- **T26 Step 5**: MCDA 多准则决策分析
- **穷尽重试替代路径**: 失败时穷尽重试替代为简化权重排序

## API 示例
```python
def ahp_weight_matrix(pairwise_matrix):
    import numpy as np
    n = pairwise_matrix.shape[0]
    eigenvalues, eigenvectors = np.linalg.eig(pairwise_matrix)
    max_idx = np.argmax(eigenvalues.real)
    weights = eigenvectors[:, max_idx].real
    weights = weights / weights.sum()
    return weights
```

## 已知限制
- AHP 一致性比率需人工校验
- 纯文本场景下准则权重依赖 LLM 判断
- TOPSIS 结果对正理想/负理想解定义敏感

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

| 节点 | 用途 |
|------|------|
| TM05 | 多准则决策分析 |

## 方法论内化

> ★核心方法论已内化于 tasks/TM05_meta_reflection.md (MC-069完整内化)，以下为快速参考

### 方法论原理
MCDA通过多准则决策分析解决冲突目标下的选择问题，解决了单一指标无法反映复杂决策的问题。

### 执行步骤
1. 定义决策准则
2. 确定权重(AHP/熵权)
3. 构建评价矩阵
4. 计算综合得分
5. 敏感性分析
6. 排序决策

### 决策规则
| 条件 | 动作 |
|------|------|
| 准则>5且有权重冲突 | MCDA |
| 准则≤3 | 简单加权 |
| 完全定性 | 德尔菲法 |

### 输出规范
```yaml
mcda_output:
  available: bool
  criteria_count: int
  ranking: list
  consistency_ratio: float
  degradation_note: str
```

### 穷尽重试策略
| 级别 | 方案 |
|------|------|
| L1 | MCDA完整(AHP+熵权+TOPSIS) |
| L2 | 简单加权 |
| L3 | 定性比较 |
| L4 | 直觉决策 |

