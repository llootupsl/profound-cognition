---
name: llmlingua-compressor
description: LLMLingua 重要性感知压缩 — 减少75%推理开销的同时保持关键信息
author: 阿洋
tags: [compression, llmlingua, token-optimization, performance]
---

# LLMLingua 重要性感知压缩

## 平台要求

platform_requirements:
  primary_mode:
    name: "Python 语义压缩"
    requires: ["bash_execution", "python3.9+", "pip"]
    command: "pip install llmlingua && python -c \"...\""
  exhaust-retry_mode:
    name: "LLM-only 规则驱动摘要"
    trigger: "bash_execution == false OR python_import_error"
    method: "保留 key_findings 前 N 条 + main_conclusion + 按模式裁剪的上下文片段"
    description: "无代码执行能力的平台自动穷尽重试为规则驱动摘要，不尝试安装 Python 包"

## 概述

本模块实现基于重要性感知（Importance-Aware）的上下文压缩，在 Phase 1 上下文组装阶段对上游节点输出进行选择性压缩，减少下游节点推理开销，同时保持关键信号的完整性。

---

## 压缩触发条件

```yaml
compression_trigger:
  threshold: "context_package 预估 token >= 12000"
  target_ratio: "0.6x"
```

---

## 压缩策略分级

```yaml
compression_mode:
  level_1_cautious:
    description: "保留所有 key_findings（5条）+ 全部 main_refutation"
    method: "仅压缩非关键段落（如详细方法描述、背景铺垫）"
    info_loss_risk: "低"
    downstream_nodes: [T13, T14, T15, T20]

  level_2_balanced:
    description: "保留前4条 key_findings + main_refutation"
    method: "压缩非关键段落 + 将部分描述转为关键词列表"
    info_loss_risk: "中"
    downstream_nodes: [T16, T17, T18, T19]

  level_3_aggressive:
    description: "保留 core_conclusion + 前3条 key_findings"
    method: "大幅压缩，仅保留最核心的结构化信息"
    info_loss_risk: "高"
    downstream_nodes: [T20 渲染层]  # 仅渲染层使用
```

---

## 实现指南

### Python 实现参考

```python
# 安装: pip install llmlingua
from llmlingua import PromptCompressor

# 初始化压缩器
# 可选择使用本地小模型进行重要性评分
compressor = PromptCompressor(
    model_name="microsoft/llmlingua-2-bert-base-multilingual-cased-meetingbank",
    use_llmlingua2=True  # 使用 v2 版本的迭代式 token 级压缩
)

def compress_context(context: dict, level: str) -> dict:
    """
    对上下文进行重要性感知压缩

    Args:
        context: 上游节点输出字典，包含 summary, key_findings, raw_output 等
        level: 压缩级别 (cautious/balanced/aggressive)

    Returns:
        压缩后的上下文
    """
    if level == "level_1_cautious":
        # 仅压缩 raw_output 中的非关键段落
        # 保留所有 key_findings
        if "raw_output" in context and len(context["raw_output"]) > 2000:
            compressed_raw = compressor.compress_prompt(
                context["raw_output"],
                rate=0.5,  # 压缩50%
                force_tokens=["key_finding", "证据", "conclusion", "结论"]
            )
            context["raw_output"] = compressed_raw["compressed_prompt"]

    elif level == "level_2_balanced":
        # 压缩 raw_output + 保留前4条 key_findings
        if "raw_output" in context:
            compressed_raw = compressor.compress_prompt(
                context["raw_output"],
                rate=0.35,  # 压缩65%
                force_tokens=["conclusion", "结论", "evidence", "证据"]
            )
            context["raw_output"] = compressed_raw["compressed_prompt"]
        if "key_findings" in context:
            context["key_findings"] = context["key_findings"][:4]

    elif level == "level_3_aggressive":
        # 大幅压缩，仅保留核心
        if "raw_output" in context:
            del context["raw_output"]  # 完全删除原始输出
        if "key_findings" in context:
            context["key_findings"] = context["key_findings"][:3]
        # 将 summary 本身压缩
        if "summary" in context:
            compressed_summary = compressor.compress_prompt(
                context["summary"],
                rate=0.5,
                force_tokens=["结论", "发现", "insight"]
            )
            context["summary"] = compressed_summary["compressed_prompt"]

    return context
```

### 集成位置

在 Phase 1 context_package 组装完成后、节点执行前，执行压缩：

```
Phase 1 上下文组装 →
  预估 token →
  若超过 threshold → 触发压缩 →
  压缩完成后 → 传递 compressed_context 给 Sub-Agent
```

---

## 压缩日志

```yaml
compression_log:
  enabled: true
  fields:
    - node_id: "触发压缩的节点"
    - pre_compression_token: integer
    - post_compression_token: integer
    - compression_ratio: float  # 实际压缩比
    - target_ratio: float
    - level: "cautious|balanced|aggressive"
    - token_saved: integer
```

---

## 注意事项

- **保留最小字段**：始终遵守 handoff-protocol.md §3.1 `rule_6_minimum_fields` 规定的最少保留字段
- **不压缩用户输入**：仅压缩上游任务节点产出，不修改用户原始输入
- **上下文恢复**：在 T20 渲染阶段，如发现信息不足，可申请 "上下文恢复请求" 返回上层获取完整数据

---

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| v1.0 | 2026-05-25 | 初始发布：三级压缩策略 + LLMLingua v2 集成 |

---

(c) 阿洋


---

## 穷尽重试策略

```yaml
exhaust_retry:
  L1_FULL:
    condition: "LLMLingua 可用 + Python执行环境正常"
    behavior: "完整重要性感知压缩 + 三级策略 + 压缩日志"

  L2_PARTIAL_DATA:
    condition: "LLMLingua 可用但压缩质量不理想"
    behavior: "降低压缩率（提高保留比例）+ 标注[LOW-COMPRESSION]"

  L3_TEXT_ONLY:
    condition: "LLMLingua 不可用（无Python执行环境）"
    behavior: "穷尽尝试到 LLM-only 规则驱动摘要 + 标注[RULE-BASED]"

  L4_SERVICE_DOWN:
    condition: "压缩功能完全不可用"
    behavior: "不压缩，传递完整上下文 + 标注[NO-COMPRESSION] + 警告token超限风险"
```
