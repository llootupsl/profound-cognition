<!-- 作者：阿洋 -->


> **版本治理元数据 (D12.4.2)**:
> - version: 1.0
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（能力卡补全版本治理元数据，D12.4.2）

# SAFE (Search Augmented Factuality Evaluator)

## 基本信息
- **卡片编号**: SAFE（搜索增强事实验证器）
- **类型**: TC（事实核查工具）
- **优先级**: P1
- **层级**: L1
- **版本同步**: 与 Google SAFE 论文实现同步（Wei et al., 2024, "Long-form factuality in large language models"）

## 功能描述
搜索增强事实验证器。对原子事实（atomic facts）进行搜索增强验证，通过多轮搜索检索证据并判定每个原子事实的真伪。SAFE 由 Google DeepMind 提出，将原子事实验证转化为搜索问题：对每个原子事实生成搜索查询，检索相关证据后判定为 supported / refuted / not_enough_info 三态。SAFE 复用 SearXNG 适配器（`plugins/searxng-adapter.md`）作为搜索后端，避免重复造轮子。

## 核心能力
- **搜索查询生成**：基于原子事实自动生成多角度搜索查询（含同义词、相关术语变体）
- **多轮搜索验证**：对每个原子事实执行多轮搜索，复用 SearXNG 多引擎聚合
- **三态判定**：输出 supported（支持）/ refuted（反驳）/ not_enough_info（证据不足）三态裁决
- **证据溯源**：每条判定记录 evidence_url，支持证据链追溯

## 调用前置条件
- Python 3.8+
- 搜索 API（复用 SearXNG 适配器，详见 `plugins/searxng-adapter.md`）
- LLM 推理后端（用于搜索查询生成与判定推理）
- 可选：Google Search API（SAFE 官方实现默认使用，可替换为 SearXNG）

## 调用指令

### 输入参数
- `atomic_facts` (array, 待验证的原子事实列表)
- `search_backend` (string, 可选: 搜索后端，默认 searxng，可选 google)
- `max_search_rounds` (integer, 可选: 每个原子事实最大搜索轮数，默认 3)

### 输出格式
```yaml
safe_output:
  verification_results:
    - fact_id: "AF-1"
      atomic_fact: "string（原子事实陈述）"
      search_query: "string（生成的搜索查询）"
      verdict: "supported|refuted|not_enough_info"
      evidence_url: "string（支撑/反驳证据的 URL）"
      evidence_summary: "string（证据摘要，1-3 句话）"
      search_rounds: integer
  supported_rate: float      # supported 原子事实数 / 总数
  refuted_rate: float        # refuted 原子事实数 / 总数
  uncertain_rate: float      # not_enough_info 原子事实数 / 总数
```

### 调用示例
```
safe.verify(
  atomic_facts=[
    "X公司成立于2018年",
    "X公司总部在深圳",
    "X公司由张三创立"
  ],
  search_backend="searxng",
  max_search_rounds=3
)
```

## 失败回退策略
- **穷尽重试替代路径**: SAFE → FActScore 仅模式 → 人工事实核查
- **触发条件**: SearXNG 服务不可用 / 搜索 API 全部失败 / LLM 推理后端不可用
- **回退行为**: 回退到 FActScore 仅模式（使用 internal_knowledge 判定，不执行搜索增强），并在输出中标注 `degraded_mode: true`

## 效果度量
- **supported_rate** (0-1)：被支持的原子事实比例
- **refuted_rate** (0-1)：被反驳的原子事实比例
- **uncertain_rate** (0-1)：证据不足的原子事实比例
- 阈值规则：uncertain_rate > 0.2 时触发 confidence downgrade

## MCP 适配
- **MCP Tool 名称**: safe_verify
- **MCP 参数**: atomic_facts, search_backend, max_search_rounds

## 依赖
- SearXNG 适配器（`plugins/searxng-adapter.md`）作为搜索后端
- LLM 推理后端（用于搜索查询生成与判定推理）
- 可选：Google Search API（SAFE 官方实现默认使用）

## 消费关系

### 消费此卡片的领域引擎
暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

| 节点 | 用途 |
|------|------|
| T17 | 搜索增强验证（原子事实三态判定） |

## 与 FActScore 的协同关系
SAFE 在 FActScore 拆解的原子事实基础上执行搜索增强验证，提供更可靠的事实判定。两者融合使用流程：
1. FActScore 拆解原子事实
2. SAFE 对每个原子事实进行搜索增强验证
3. 基于 SAFE 验证结果计算 FActScore
4. FActScore < 0.8 触发 T17 RETRYING

详见 `knowledge/external-capabilities/FActScore.md`。

## 与 SearXNG 适配器的集成
SAFE 复用 SearXNG 适配器（`plugins/searxng-adapter.md`）作为搜索后端：
- 搜索查询生成后，通过 SearXNG 多引擎聚合获取结果
- 复用 SearXNG 的去重规则（URL 规范化、标题相似度、SimHash）
- 复用 SearXNG 的穷尽重试策略（SearXNG → 单引擎 → LLM 内建知识）
- 搜索结果按 SearXNG 适配器的来源标注格式记录
