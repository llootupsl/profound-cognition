<!-- 作者：阿洋 -->


> **版本治理元数据 (D12.4.2)**:
> - version: 1.0
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（能力卡补全版本治理元数据，D12.4.2）

# TC-064: ENA — Epistemic Network Analysis

## 基本信息

> ★核心方法论已内化于 tasks/T26_meta_insight_cross.md，本文件仅作快速引用入口

- **名称**: rENA
- **类别**: 认识论网络分析
- **语言**: Python/R
- **版本要求**: ≥0.2
- **安装**: pip install rENA
- **许可证**: GPL-3
- **仓库**: https://github.com/epistemic-analytics/rENA

## 核心能力
- 认识论网络分析 (ENA)
- 高维连接数据降维
- 网络模型统计比较
- 认知状态轨迹可视化

## 在 profound-cognition 中的用途
- **T26 Step 3**: ENA 认识论网络分析
- **穷尽重试替代路径**: 失败时穷尽重试替代为定性认知结构描述

## API 示例
```python
from rENA import ENA

ena = ENA(
    data=data,
    units=["unit_id"],
    conversations=["conversation_id"],
    codes=["code_A", "code_B", "code_C"]
)
ena.generate()
ena.plot()
```

## 已知限制
- 需要结构化编码数据
- 降维过程可能丢失细节
- 纯文本研究场景需手动编码

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

| 节点 | 用途 |
|------|------|
| TM05 | 认知网络分析 |
| T_meta_dim_9_10 | 元维度分析 |


## 调用前置条件

- Python 3.9+ 运行环境（如需代码执行）
- 对应工具库已安装（详见卡片「安装」或「基本信息」字段）
- 网络连接可用（如需远程 API 或数据源）
- 上游节点产出已就绪（根据消费节点依赖关系）

## 效果度量

| 度量指标 | 定义 | 目标值 |
|----------|------|--------|
| 执行成功率 | 成功调用次数 / 总调用次数 | ≥ 0.95 |
| 平均延迟 | 单次调用平均耗时 | ≤ 5s |
| 输出质量分 | Supervisor 评分（0-1） | ≥ 0.8 |
| 穷尽重试触发率 | 触发降级的调用次数 / 总调用次数 | ≤ 0.1 |

效果度量写入 NRSF，供 T19 质量检查消费。