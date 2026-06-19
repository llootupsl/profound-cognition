<!-- 作者：阿洋 -->

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

