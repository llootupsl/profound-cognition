<!-- 作者：阿洋 -->


> **版本治理元数据 (D12.4.2)**:
> - version: 1.0
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（能力卡补全版本治理元数据，D12.4.2）

# TC-067: OWLAPY — OWL Ontology Construction

## 基本信息

> ★核心方法论已内化于 tasks/TM07_ontology_export.md，本文件仅作快速引用入口

- **名称**: owlapy
- **类别**: 本体构建
- **语言**: Python
- **版本要求**: ≥1.0
- **安装**: pip install owlapy
- **许可证**: Apache 2.0
- **仓库**: https://github.com/dice-group/owlapy

## 核心能力
- OWL 本体构建与推理
- 类/属性/实例管理
- OWL 2 DL 表达式支持
- 与 OWL API 兼容

## 在 profound-cognition 中的用途
- **T28 Step 3**: OWL 本体构建
- **穷尽重试替代路径**: 失败时穷尽重试替代为 JSON Schema 简化本体

## API 示例
```python
from owlapy.model import OWLClass, OWLObjectProperty, IRI
from owlapy.render import DLSyntaxObjectRenderer

cls_a = OWLClass(IRI.create("http://example.org#", "ConceptA"))
cls_b = OWLClass(IRI.create("http://example.org#", "ConceptB"))
prop = OWLObjectProperty(IRI.create("http://example.org#", "relatedTo"))
renderer = DLSyntaxObjectRenderer()
print(renderer.render(cls_a))
```

## 已知限制
- OWL 推理计算开销大
- 本体建模需要领域专业知识
- 纯文本研究场景本体质量依赖 LLM 建模能力

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

| 节点 | 用途 |
|------|------|
| TM07 | OWL本体构建 |


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