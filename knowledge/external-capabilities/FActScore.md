<!-- 作者：阿洋 -->


> **版本治理元数据 (D12.4.2)**:
> - version: 1.0
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（能力卡补全版本治理元数据，D12.4.2）

# FActScore

## 基本信息
- **卡片编号**: FActScore（事实精确度评估器）
- **类型**: TC（事实核查工具）
- **优先级**: P1
- **层级**: L1
- **版本同步**: 与官方 factscore 库（https://github.com/shmsw25/FActScore）同步

## 功能描述
原子事实级精确度评估工具。将长文本拆解为原子事实（atomic facts），逐条判定是否被可靠证据支持，并计算 FActScore = 支持的原子事实数 / 总原子事实数。FActScore 由 Min et al. (EMNLP 2023) 提出，是衡量生成式文本事实精确度的细粒度指标，弥补了整体性事实核查无法定位具体错误的缺陷。

## 核心能力
- **原子事实拆解（Atomic Fact Extraction）**：将复合断言拆解为可独立验证的简单陈述，每个原子事实不超过一个事实主张
- **原子事实判定（Atomic Fact Verification）**：对每个原子事实判定为 supported / not_supported / irrelevant
- **FActScore 计算**：FActScore = 支持的原子事实数 / 总原子事实数，取值范围 [0.0, 1.0]
- **错误定位**：精确定位未被支持的原子事实，支撑下游修正

## 调用前置条件
- Python 3.8+
- factscore 库已安装（`pip install factscore`）
- 可访问的 LLM 推理后端（用于原子事实拆解与判定）
- 可选：可靠知识源（Wikipedia API / 领域知识库）

## 调用指令

### 输入参数
- `text` (string, 待评估的文本/报告段落)
- `knowledge_source` (string, 可选: 知识源标识，默认 wikipedia)
- `granularity` (string, 可选: 原子事实拆解粒度，默认 standard)

### 输出格式
```yaml
factscore_output:
  atomic_facts:
    - fact_id: "AF-1"
      fact: "string（原子事实陈述）"
      verdict: "supported|not_supported|irrelevant"
      evidence: "string（支撑/反驳证据摘要）"
  factscore_value: float  # 支持的原子事实数 / 总原子事实数，[0.0, 1.0]
  supports_count: integer
  not_supports_count: integer
  irrelevant_count: integer
```

### 调用示例
```
factscore.evaluate(
  text="X公司成立于2018年，总部在深圳，由张三创立",
  knowledge_source="wikipedia"
)
```

## 失败回退策略
- **穷尽重试替代路径**: FActScore → 人工事实核查
- **触发条件**: factscore 库不可用 / LLM 推理后端不可用 / 知识源不可访问
- **回退行为**: 回退到人工事实核查模式，由 T17 执行者基于 internal_knowledge + web_search 逐条判定原子事实，并手动计算 factscore_value

## 效果度量
- **factscore_value** (0-1)：核心度量指标，越高表示事实精确度越高
- 阈值规则：factscore_value ≥ 0.8 通过；< 0.8 触发 T17 RETRYING
- 辅助度量：supports_count、not_supports_count、irrelevant_count

## MCP 适配
- **MCP Tool 名称**: factscore_evaluate
- **MCP 参数**: text, knowledge_source, granularity

## 依赖
- factscore 库（官方实现）
- LLM 推理后端（用于原子事实拆解与判定）
- 知识源（Wikipedia API / 领域知识库）

## 消费关系

### 消费此卡片的领域引擎
暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

| 节点 | 用途 |
|------|------|
| T17 | 原子事实拆解 + FActScore 计算（事实核查阶段） |

## 与 SAFE 的协同关系
FActScore 提供原子事实拆解与精确度评分框架，SAFE 在此基础上提供搜索增强验证能力。两者融合使用流程：
1. FActScore 拆解原子事实
2. SAFE 对每个原子事实进行搜索增强验证
3. 基于 SAFE 验证结果计算 FActScore
4. FActScore < 0.8 触发 T17 RETRYING

详见 `knowledge/external-capabilities/SAFE.md`。
