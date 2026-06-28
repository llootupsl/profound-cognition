<!-- 作者：阿洋 -->


> **版本治理元数据 (D12.4.2)**:
> - version: 1.0
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（能力卡补全版本治理元数据，D12.4.2）

# Mem0 — 跨会话记忆系统能力卡

## 基本信息
- **卡片编号**: #5b
- **类型**: TC（工具能力卡）
- **优先级**: P0
- **层级**: L1
- **关联卡片**: [TC-005-Mem0.md](./TC-005-Mem0.md)（基础工具卡，**已弃用**——见 W4-F5；本卡为增强版）
- **协议引用**: [cross-session-memory-protocol.md](../protocols/cross-session-memory-protocol.md)

## 功能描述

Mem0 作为 Profound Cognition v6.0 的跨会话记忆系统，提供三层结构化记忆能力：

1. **用户偏好层**：存储用户的 output_type 偏好、Persona 配置、引用风格、深度偏好等，使框架能"记住"用户的长期偏好，无需每次会话重复采集
2. **历史结论层**：将 T13 认知综合产出的核心结论写入结构化数据库，支持语义检索，使新会话能复用历史研究结论
3. **未解决问题层**：将 I01 迭代深化中标记为 unclosable 的缺口写入数据库，使后续会话能继续探索未闭合问题

Mem0 提供三操作模型（add/search/update）+ 跨会话检查点 + 记忆衰减 + 记忆审计四大能力。支持 Mem0g 图增强版提供实体关系图。

## 三层记忆架构

### 第一层：用户偏好层（User Preference Layer）

```yaml
user_preference_memory:
  user_id: "string — 用户唯一标识"
  preferences:
    output_type: "research_report | wechat_article | course_material"
    persona_config:
      identity: "用户身份信息"
      core_values: "核心价值观"
      personal_stories: "个人故事"
      # ... 完整 Persona 7 字段
    citation_style: "apa | mla | chicago | gb_t_7714 | inline"
    depth_preference: "exhaust | standard | brief"
    language: "zh | en | bilingual"
    format_preferences:
      font_size: "small | medium | large"
      color_scheme: "warm | cool | neutral"
      # ... 其他格式偏好
  last_updated: "ISO8601"
  confidence: "float — 偏好置信度（基于交互次数）"
```

### 第二层：历史结论层（Historical Conclusions Layer）

```yaml
historical_conclusion_memory:
  memory_id: "string — 记忆唯一标识"
  user_id: "string"
  research_id: "string — 原研究会话 ID"
  problem: "string — 原始研究问题"
  conclusions:
    - {
        conclusion_id: "string",
        content: "string — 结论内容",
        confidence: "float — 置信度",
        evidence_count: "integer — 支持证据数",
        counter_evidence_count: "integer — 反证数",
      }
  domain_engines_activated: ["economics-engine", "tech-engine", ...]
  timestamp: "ISO8601"
  tags: ["半导体", "地缘政治", ...]  # 语义检索标签
  embedding: "vector — 结论的向量表示（用于语义检索）"
```

### 第三层：未解决问题层（Unsolved Problems Layer）

```yaml
unsolved_problem_memory:
  memory_id: "string"
  user_id: "string"
  research_id: "string"
  problem: "string — 原始研究问题"
  unclosable_gaps:
    - {
        gap_id: "string",
        description: "string — 缺口描述",
        gap_type: "data_gap | method_gap | theory_gap | evidence_gap",
        attempted_approaches: ["string — 已尝试的方法"],
        why_unclosable: "string — 无法闭合的原因",
        priority: "P0 | P1 | P2",
      }
  timestamp: "ISO8601"
  tags: ["string"]
  embedding: "vector"
```

## 调用指令

### 输入参数

| 操作 | 参数 | 说明 |
|------|------|------|
| `add` | `data`, `user_id`, `memory_layer` (`preference`/`conclusion`/`unsolved`), `metadata` | 写入记忆到指定层 |
| `search` | `query`, `user_id`, `memory_layer`, `limit`, `semantic_search` (bool) | 语义检索记忆 |
| `update` | `memory_id`, `data`, `user_id` | 更新现有记忆 |
| `delete` | `memory_id`, `user_id` | 删除指定记忆（记忆审计用） |
| `list_all` | `user_id`, `memory_layer` | 列出用户的所有记忆（记忆审计用） |
| `decay` | `user_id` | 触发记忆衰减（遗忘曲线） |

### 输出格式

```yaml
# add 操作
memory_id: "string"

# search 操作
results:
  - {
      memory_id: "string",
      content: "string",
      score: "float — 语义相似度",
      timestamp: "ISO8601",
      metadata: {...},
    }

# update / delete
status: "success | failed"
```

### 调用示例

```python
from mem0 import Memory

memory = Memory()

# 写入用户偏好
memory.add(
    data="用户偏好：output_type=research_report, citation_style=apa, depth=exhaust",
    user_id="user_001",
    memory_layer="preference",
    metadata={"source": "T00b_persona_collection", "timestamp": "2026-06-25T10:00:00Z"},
)

# 语义检索历史结论
results = memory.search(
    query="半导体产业链地缘政治风险",
    user_id="user_001",
    memory_layer="conclusion",
    limit=5,
    semantic_search=True,
)

# 写入未解决问题
memory.add(
    data="I01 标记的 unclosable gap: 缺少 2026Q3 半导体出口数据",
    user_id="user_001",
    memory_layer="unsolved",
    metadata={
        "research_id": "uuid-1234",
        "gap_type": "data_gap",
        "priority": "P1",
    },
)
```

## 记忆衰减（遗忘曲线）

Mem0 集成艾宾浩斯遗忘曲线，对历史结论层与未解决问题层实施记忆衰减：

```python
import math

def memory_weight(age_in_days: int, access_count: int) -> float:
    """记忆权重计算（艾宾浩斯遗忘曲线变体）。

    Args:
        age_in_days: 记忆创建后的天数
        access_count: 被检索访问的次数（每次访问增强记忆）

    Returns:
        权重 (0-1)，低于 0.1 的记忆进入"待遗忘"队列
    """
    # 基础遗忘曲线：R = exp(-t/S)，S 为记忆强度
    # 每次访问增强 S（S = base_S * (1 + log(1 + access_count))）
    base_S = 30  # 默认记忆强度 30 天
    S = base_S * (1 + math.log(1 + access_count))
    retention = math.exp(-age_in_days / S)
    return retention
```

**衰减规则**：
- 权重 < 0.1：记忆进入"待遗忘"队列，30 天后自动删除（除非用户访问）
- 权重 0.1-0.3：记忆标记为"弱记忆"，检索时降权
- 权重 > 0.3：记忆正常保留
- **用户偏好层不衰减**（偏好是长期稳定的，不遗忘）
- **每次访问重置衰减**：被检索访问的记忆，access_count + 1，权重回升

## 记忆审计

用户可查看与删除自己的记忆，保障隐私与可控性：

```python
def audit_user_memories(user_id: str) -> dict:
    """生成用户记忆审计报告。"""
    return {
        "user_id": user_id,
        "preference_count": memory.count(user_id, layer="preference"),
        "conclusion_count": memory.count(user_id, layer="conclusion"),
        "unsolved_count": memory.count(user_id, layer="unsolved"),
        "total_memories": ...,
        "oldest_memory": "ISO8601",
        "newest_memory": "ISO8601",
        "memories": memory.list_all(user_id),  # 完整记忆列表
    }


def delete_user_memory(user_id: str, memory_id: str) -> dict:
    """删除指定记忆（用户行使被遗忘权）。"""
    memory.delete(memory_id=memory_id, user_id=user_id)
    return {"status": "deleted", "memory_id": memory_id}


def export_user_memories(user_id: str) -> dict:
    """导出用户全部记忆（数据可携带权）。"""
    return {
        "format": "json",
        "user_id": user_id,
        "memories": memory.list_all(user_id),
    }
```

## 穷尽重试策略

- **穷尽重试替代路径**: Mem0 → 纯文件模式（NRSF-Summary Markdown 文件 + JSON 索引）
- **触发条件**: Mem0 API 连续 3 次超时
- **回退行为**: 记忆写入本地 JSON 文件（`./memory/user_{user_id}.json`），检索时全量扫描

## MCP 适配

- **MCP Tool 名称**: `mem0_cross_session`
- **MCP 参数**: `operation`, `data`, `user_id`, `memory_layer`, `memory_id`, `query`, `limit`, `semantic_search`

## 依赖

- Mem0 服务部署 + API Key
- 向量数据库（Qdrant，用于语义检索的 embedding 存储）
- 可选：Mem0g 图增强版（用于实体关系图）

## 消费关系

### 消费此卡片的 DAG 节点

| 节点 | 消费方式 | 说明 |
|------|---------|------|
| T00b（输入情绪基调提取） | `search(preference)` | 会话开始时检索用户偏好，预填 Persona 字段 |
| T00（研究大纲生成） | `search(preference)` | 检索 output_type/depth_preference，影响 DAG 裁剪 |
| T13（认知综合） | `add(conclusion)` | 将核心结论写入历史结论层 |
| I01（迭代深化） | `add(unsolved)` | 将 unclosable gaps 写入未解决问题层 |
| I01（迭代深化） | `search(unsolved)` | 检索历史未解决问题，作为新一轮迭代的起点 |
| T02（L1+L2 研究） | `search(conclusion)` | 检索历史相关结论，作为研究起点 |

**注**：上表消费关系为协议层声明（详见 `cross-session-memory-protocol.md`），任务文件无显式 Mem0 调用代码。跨会话记忆的读写由执行引擎在任务执行前后自动触发，详见上方声明段。

### 消费此卡片的协议

- [cross-session-memory-protocol.md](../protocols/cross-session-memory-protocol.md) — 跨会话记忆协议
- [checkpoint-protocol.md §10](../protocols/checkpoint-protocol.md) — 跨会话检查点

## 效果度量

| 度量指标 | 定义 | 目标值 |
|----------|------|--------|
| 执行成功率 | 成功调用次数 / 总调用次数 | ≥ 0.95 |
| 平均延迟 | 单次调用平均耗时 | ≤ 5s |
| 输出质量分 | Supervisor 评分（0-1） | ≥ 0.8 |
| 穷尽重试触发率 | 触发降级的调用次数 / 总调用次数 | ≤ 0.1 |

效果度量写入 NRSF，供 T19 质量检查消费。