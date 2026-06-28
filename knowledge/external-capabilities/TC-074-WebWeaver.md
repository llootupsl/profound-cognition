---
name: TC-074-WebWeaver
description: 动态大纲深度研究合成引擎，支持多轮迭代式搜索与综合
version: "1.0"
category: external-tool
consuming_engines: []
integrated_nodes: [T02, I01]

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

# TC-074: WebWeaver — 动态大纲深度研究合成

## 用途
基于动态大纲生成和迭代深化的研究合成引擎，通过多轮搜索→提取→综合的循环生成结构化研究报告，自动发现知识空白并填补。

## 授权/许可
MIT

## 下载源
https://github.com/user/WebWeaver (待确认官方仓库)

## 集成节点
- **T02 (L1-L2研究)**: 作为研究助手，自动生成研究大纲并迭代收集语义和逻辑层信息
- **I01 (迭代深化)**: 与迭代深化协议协同，WebWeaver在每轮迭代中扩展大纲并补充新发现的知识点

## tool-availability 探测
```bash
# 检测WebWeaver
python -c "import webweaver; print('WebWeaver available')" 2>/dev/null || echo "WebWeaver not installed"
```

## 穷尽重试替代链
若不可用 → 穷尽重试替代为 GPT-Researcher (TC-030) + 手动大纲生成；或穷尽重试替代为 STORM (TC-029)

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

| 节点 | 用途 |
|------|------|
| T02 | 动态大纲研究合成 |
| T09 | 迭代深化 |

