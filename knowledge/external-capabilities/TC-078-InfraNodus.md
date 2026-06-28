---
name: TC-078-InfraNodus

> ★核心方法论已内化于 tasks/T03b_cross_axis_matrix.md，本文件仅作快速引用入口

description: 文本网络分析工具，用于结构洞发现和知识空白识别
version: "1.0"
category: external-tool
consuming_engines: []
integrated_nodes: [T15b]

## 调用前置条件

- Python 3.9+ 运行环境（如需代码执行）
- 对应工具库已安装（详见卡片「安装」或「基本信息」字段）
- 网络连接可用（如需远程 API 或数据源）
- 上游节点产出已就绪（根据消费节点依赖关系）

## 失败回退策略

- **触发条件**: 工具不可用、调用超时、输出质量不达标、依赖缺失
- **回退路径**: 降级到 LLM 内建能力，标注 [INTERNAL_REASONING]
- **回退声明**: 回退后失去工具增强能力，但保证流程不中断（EXHAUST 铁律）
- **穷尽重试**: 按 L1_FULL → L2_PARTIAL → L3_TEXT_ONLY → L4_SERVICE_DOWN 逐级降级

## 效果度量

| 度量指标 | 定义 | 目标值 |
|----------|------|--------|
| 执行成功率 | 成功调用次数 / 总调用次数 | ≥ 0.95 |
| 平均延迟 | 单次调用平均耗时 | ≤ 5s |
| 输出质量分 | Supervisor 评分（0-1） | ≥ 0.8 |
| 穷尽重试触发率 | 触发降级的调用次数 / 总调用次数 | ≤ 0.1 |

效果度量写入 NRSF，供 T19 质量检查消费。
---

<!-- 作者：阿洋 -->



> **版本治理元数据 (D12.4.2)**:
> - version: 1.0
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（能力卡补全版本治理元数据，D12.4.2）

# TC-078: InfraNodus — 结构洞发现

## 用途
基于文本网络分析的知识图谱工具，通过识别概念网络中的结构洞（structural gaps）来发现知识空白和潜在的创新连接点，支持知识图谱的完整性评估。

## 授权/许可
AGPL-3.0

## 下载源
https://github.com/noduslabs/infranodus

## 集成节点
- **T15b (跨域矩阵)**: 在跨域知识图谱中识别结构洞——即两个或多个知识域之间缺乏连接的区域，发现潜在的跨域创新机会

## tool-availability 探测
```bash
# 检测InfraNodus
python -c "import infranodus; print('InfraNodus available')" 2>/dev/null || echo "InfraNodus not installed"
# 或检测API端点
curl -s http://localhost:3000/api/status 2>/dev/null || echo "InfraNodus server not running"
```

## 穷尽重试替代链
若不可用 → 穷尽重试替代为 NetworkX 中心性分析 + 社区检测（Louvain/Girvan-Newman）；或手动结构洞识别

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

| 节点 | 用途 |
|------|------|
| T15b | 结构洞发现 |

