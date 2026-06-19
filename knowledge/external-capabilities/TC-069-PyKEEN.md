<!-- 作者：阿洋 -->

# TC-069: PyKEEN — Knowledge Graph Embedding

## 基本信息

> ★核心方法论已内化于 tasks/TM07_ontology_export.md，本文件仅作快速引用入口

- **名称**: PyKEEN
- **类别**: 知识图谱嵌入
- **语言**: Python
- **版本要求**: ≥1.10
- **安装**: pip install pykeen
- **许可证**: MIT
- **仓库**: https://github.com/pykeen/pykeen

## 核心能力
- 知识图谱嵌入 (TransE, RotatE, ComplEx 等)
- 链接预测
- 实体对齐
- 嵌入评估与比较

## 在 profound-cognition 中的用途
- **T28 Step 5**: PyKEEN 知识图谱嵌入
- **穷尽重试替代路径**: 失败时穷尽重试替代为基于规则的链接预测

## API 示例
```python
from pykeen.pipeline import pipeline

result = pipeline(
    model="TransE",
    dataset="nations",
    training_kwargs=dict(num_epochs=100),
)
result.save_to_directory("trans_e_nations")
```

## 已知限制
- 需要足够大的知识图谱数据
- 训练嵌入需要 GPU 资源
- 纯文本研究场景数据量通常不足以训练有效嵌入

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

| 节点 | 用途 |
|------|------|
| TM07 | 知识图谱嵌入 |

