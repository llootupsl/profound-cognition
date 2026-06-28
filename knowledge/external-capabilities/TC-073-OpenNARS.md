---
name: TC-073-OpenNARS

> ★核心方法论已内化于 tasks/T09_cog_reason.md，本文件仅作快速引用入口

description: 非公理推理引擎，支持矛盾容忍和不确定性推理
version: "1.0"
category: external-tool
consuming_engines: []
integrated_nodes: [T10, T11, T12]

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

# TC-073: OpenNARS — 非公理矛盾容忍推理

## 用途
基于非公理逻辑（NAL）的通用AI推理引擎，天然支持矛盾容忍、不确定性推理和实时学习，适用于对抗验证场景中的矛盾检测与处理。

## 授权/许可
MIT

## 下载源
https://github.com/opennars/opennars

## 集成节点
- **T10 (对抗逻辑)**: 利用NAL的矛盾容忍机制处理对抗性逻辑推理中发现的矛盾命题
- **T11 (对抗证据)**: 对证据冲突进行不确定性量化，输出置信度而非真假二值
- **T12 (对抗范围)**: 在推理资源受限条件下进行实时推理，支持"最佳当前答案"模式

## tool-availability 探测
```bash
# 检测OpenNARS是否可用
java -jar opennars.jar --version 2>/dev/null || echo "OpenNARS not available"
# 或Python封装
python -c "import opennars; print('OpenNARS Python available')" 2>/dev/null
```

## 穷尽重试替代链
若不可用 → 穷尽重试替代为概率推理（Pyro/贝叶斯网络）+ 手动矛盾标记；或穷尽重试替代为模糊逻辑规则

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

| 节点 | 用途 |
|------|------|
| T10 | 非公理矛盾容忍 |
| T11 | 证据冲突量化 |
| T12 | 资源受限推理 |

