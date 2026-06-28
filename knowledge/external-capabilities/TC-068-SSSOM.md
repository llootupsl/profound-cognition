<!-- 作者：阿洋 -->


> **版本治理元数据 (D12.4.2)**:
> - version: 1.0
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（能力卡补全版本治理元数据，D12.4.2）

# TC-068: SSSOM — Semantic Mapping

## 基本信息

> ★核心方法论已内化于 tasks/TM07_ontology_export.md，本文件仅作快速引用入口

- **名称**: SSSOM (Simple Standard for Sharing Ontological Mappings)
- **类别**: 语义映射
- **语言**: Python
- **版本要求**: ≥0.3
- **安装**: pip install sssom
- **许可证**: MIT
- **仓库**: https://github.com/mapping-commons/sssom-py

## 核心能力
- 语义映射标准 (SSSOM)
- 本体间映射生成与验证
- 映射置信度评估
- 映射集合并与推理

## 在 profound-cognition 中的用途
- **T28 Step 4**: SSSOM 语义映射
- **穷尽重试替代路径**: 失败时穷尽重试替代为手动映射表

## API 示例
```python
from sssom import load_mapping_set, collapse

ms = load_mapping_set("mappings.sssom.tsv")
collapsed = collapse(ms)
```

## 已知限制
- 映射质量依赖源本体质量
- 自动映射可能产生错误关联
- 纯文本研究场景映射范围有限

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

| 节点 | 用途 |
|------|------|
| TM07 | 语义映射标准 |


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