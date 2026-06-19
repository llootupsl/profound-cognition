---
name: TC-080-TLA-Alloy

> ★核心方法论已内化于 tasks/TM02_causal_verification.md，本文件仅作快速引用入口

description: 形式化模型检查工具，用于系统规范验证和一致性检查
version: "1.0"
category: external-tool
consuming_engines: []
integrated_nodes: [TM01, TM06]
---

<!-- 作者：阿洋 -->


# TC-080: TLA+/Alloy — 形式化模型检查

## 用途
TLA+（Temporal Logic of Actions）和Alloy是形式化规范语言和模型检查工具，用于验证系统设计的一致性和安全性属性，确保认知流水线的逻辑正确性。

## 授权/许可
MIT (TLA+) / MIT (Alloy)

## 下载源
- TLA+: https://github.com/tlaplus/tlaplus
- Alloy: https://github.com/AlloyTools/org.alloytools.alloy

## 集成节点
- **TM01 (系统动力学)**: 使用TLA+形式化验证系统动力学模型中的状态转换逻辑，确保反馈循环和因果链的一致性
- **TM06 (元层验证)**: 使用Alloy对认知流水线的元层规范进行模型检查，验证无死锁、无活锁等安全性属性

## tool-availability 探测
```bash
# 检测TLA+
java -jar tla2tools.jar -version 2>/dev/null || echo "TLA+ not available"
# 检测Alloy
java -jar alloy.jar -version 2>/dev/null || echo "Alloy not available"
# 或Python封装
python -c "import alloy; print('Alloy Python available')" 2>/dev/null
```

## 穷尽重试替代链
若不可用 → 穷尽重试替代为手动状态机验证 + 不变式标注；或穷尽重试替代为 P 语言 (p-org.github.io/P)

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

| 节点 | 用途 |
|------|------|
| TM01 | 形式化模型检查 |
| TM06 | 元层验证 |

