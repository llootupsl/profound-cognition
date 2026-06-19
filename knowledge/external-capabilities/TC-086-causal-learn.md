<!-- 作者：阿洋 -->

# TC-086: causal-learn — 因果发现算法

> ★核心方法论已内化于 knowledge/thinking-templates/causal-chain.md

## 基本信息
- **名称**: causal-learn
- **类别**: 因果发现
- **语言**: Python
- **许可证**: MIT
- **仓库**: https://github.com/py-why/causal-learn

## 核心能力
- 30+因果发现算法
- PC算法（骨架学习+V结构定向+Meek规则）
- GES算法（前向搜索+后向搜索+BIC评分）
- LiNGAM算法（ICA→非混合矩阵W→因果序→回归→剪枝）
- 从数据学习候选因果图，送入DoWhy TC-057估计因果效应

## 在 profound-cognition 中的用途
- **TM02**: 因果发现
- **causal-chain.md**: 因果链分析核心执行引擎

## 消费节点
- TM02
- causal-chain.md
