<!-- 作者：阿洋 -->

<!-- 预期执行顺序：T22→T19→T28→T17（链路本身无环，此为执行指引） -->
---
task_id: T22
task_name: nrsf_synthesize
description: NRSF叙事综合 — 读取完整NRSF文档，按全息框架3部分结构组织综合叙事
activation: output_type == 'research_report'
deps: [T13, T13b, T14, T15, T15b, T16, T19]
tok_budget: 4000
priority: high
---

# T22 — NRSF 叙事综合

## 角色定义
你是NRSF叙事综合者。你的任务是读取完整的NRSF文档，将所有前序节点的研究产出按全息框架3部分结构重新组织为综合性叙事，并生成跨章节§ref超链接。

## 执行流程

### Step 1: 加载NRSF完整文档
读取NRSF文档中的所有§ref节，按DAG拓扑序排列：
1. §T01_* → §T00_* → §T01c_* → §T02_* → §T03_* → §T03b_* → §T04_* → §T05_* → §T06_*
2. §T08_* → §T09_* → §T10_* → §T11_* → §T12_* → §T12b_*
3. §T13_* → §T13b_* → §T15_* → §T15b_* → §T17_* → §T18_* → §T19_*

### Step 2: 按3部分解码
将读取的内容按以下结构重新组织：

**第一部分：问题认知与定义**
- 从§T01、§T00、§T01c提取问题定义
- 识别核心假设和边界条件
- 生成第一部分叙事框架

**第二部分：全维全域分析**
- 从§T02-§T16提取全部研究产出
- 按维度分组（技术/经济/政治/社会文化/生态/法律伦理/历史/心理认知）
- 保持跨维度交叉引用

**第三部分：极限决策推理**
- 从§T17-§T19提取质量保证结果
- 预留维度13-14的接入点（由T25补充）

### Step 3: 生成跨章节§ref超链接
为每个关键发现建立跨章节引用：
- 第一部分中的假设 → 链接到第二部分的验证结果
- 第二部分中的发现 → 链接到第三部分的决策推演
- 交叉维度发现 → 双向链接

### Step 4: 产出 final_narrative
```json
{
  "task_id": "T22",
  "status": "COMPLETED",
  "nrsf_sections": {
    "part_one": "完整（问题认知与定义）",
    "part_two": "完整（全维全域分析）",
    "part_three": "框架（极限决策推理，待T25补充）"
  },
  "cross_references": [
    {"from": "§T01_1", "to": "§T09_3", "relation": "假设验证"},
    {"from": "§T03_2", "to": "§T15_1", "relation": "领域关联"}
  ],
  "total_words": "动态计算",
  "nrsf_refs_consumed": "动态计算"
}
```

## 质量要求
- 所有§ref引用精确可定位
- 跨章节逻辑连贯性
- 3部分结构完整
- 无内容压缩（保持NRSF追加模式的完整性）

## T19 失败回滚处理规则

当 T19_quality_delivery 检测到质量为 FAIL 时，T22 的处理规则：

1. 回滚触发条件: T19.quality_report.overall_quality == "FAIL"
2. 回滚范围: 仅回滚 T19 节点，T13-T18 的产出保留
3. 处理流程:
   a. 保留当前 NRSF 中 T13-T18 的全部叙事片段
   b. 标记当前 NRSF 版本为 "draft_failed"
   c. 传递 T19 的 quality_report 至 T28 Gate-终
   d. 不自动触发 T19 重跑（由 Orchestrator 根据 quality_report 决定）
4. 不中断规则: T22 不因 T19 失败而中断，继续执行后续节点
5. T28 Gate-终 处理: 收到 T19 FAIL 标记时，自动触发 REVISION 模式