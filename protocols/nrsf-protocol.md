<!-- 作者：阿洋 -->

# NRSF 叙事引用栈帧协议 (Narrative Reference Stack Frame Protocol) v3.0

> **职责边界声明（D3.4.1）**：本协议负责**研究状态的存储格式与叙事引用机制**——定义 §ref 标记、NRSF-Full/Summary 数据结构、并发写入协议、生命周期清除。本协议**不定义**输出长度、内容密度或展开规则（那是 `output-expansion-protocol.md` 的职责），也不定义格式转换或标记净化（那是 `output-rendering-protocol.md` 的职责）。两者在 T20 渲染节点交汇但职责正交：NRSF 提供"读什么"，output-expansion 提供"怎么展开"。详见 `docs/protocol-dependency-graph.md` §4.1。

## role
NRSF（Narrative Reference Stack Frame）叙事引用栈帧协议定义了整个 Profound Cognition v6.0.0 系统中叙事引用的标记格式、传递规则、并发写入协议和生命周期管理。NRSF 是连接所有节点产出的叙事桥梁，确保下游节点可以准确引用上游节点的关键叙事片段。

## context
所有节点产出通过 NRSF 实现叙事级别的引用和聚合。每个节点在产出 context_package 时，必须将本节点生成的叙事引用（§ref）注入 NRSF。下游节点通过 NRSF 获取上游节点的关键叙事片段，Gate 节点通过 NRSF 验证叙事一致性。

## §ref 标记格式规范

### 语法
```
§ref:<node_id>:<narrative_id>[:<version>]
```

### 组件说明
| 组件 | 类型 | 必填 | 说明 |
|------|------|------|------|
| node_id | string | 是 | 产生该叙事引用的节点标识，如 T02、T09、T13 |
| narrative_id | string | 是 | 叙事片段的唯一标识，如 main_narrative、path_3、insight_7 |
| version | string | 否 | 叙事版本号，默认 v1，格式 v{n} |

### 示例
```
§ref:T02:main_narrative
§ref:T09:path_3:v2
§ref:T13:insight_7
§ref:T22:nrsf_synthesis_final
§ref:T01:domain_engine_recommendations
```

### 引用格式
在 context_package 中引用上游 §ref 时使用：
```
参见：§ref:T02:main_narrative（第 3 段）
依托：§ref:T09:path_3:v2（推理链 C）
```

## 叙事引用传递规则

### R1: 节点产出引用
每个节点的 output 必须包含本节点生成的关键叙事片段的 §ref 标记列表。格式为：
```yaml
nrsf_refs:
  - node_id: T02
    narrative_id: main_narrative
    version: v1
    summary: "关于二战后全球经济秩序重建的核心叙事"
    token_count: 450
```

### R2: 上下文自动聚合
context_package 在构建时自动聚合所有上游节点的 nrsf_refs，形成 upsteam_refs 列表。Orchestrator 负责在 context_package 构建时解析依赖关系并注入上游引用。

### R3: 下游引用规则
下游节点可以引用上游任意节点的 §ref，但必须满足以下条件：
- 被引用的节点在当前节点的 deps 链上
- 引用的 narrative_id 在被引用节点的 nrsf_refs 中存在
- 引用时必须标注版本号（如存在多版本）

### R4: Gate 叙事一致性验证
每个 Gate 节点必须检查 nrsf_refs 的叙事一致性：
- 是否存在矛盾叙事（两个节点对同一事实产生矛盾结论）
- 是否存在遗漏叙事（关键节点未产出应有叙事）
- 是否存在断裂叙事（上游叙事未在下游被消费）

### R5: T20 渲染时解析
T20 渲染器在渲染时必须解析所有相关的 §ref，构建完整的叙事引用图，确保渲染输出不遗漏关键叙事片段。

## 版本管理（R3-04）

NRSF 支持叙事片段的版本管理，确保后续节点修改上游叙事时保留完整修改历史与可追溯性。版本管理适用于所有启用 `versionable: true` 标记的 §ref。

### 版本管理触发条件

以下节点的叙事片段强制启用版本管理：
- **T13**（认知综合）：其产出可能被 T13b（二次综合修正）、T22（NRSF 叙事综合）修改
- **T22**（NRSF 叙事综合）：其产出可能被 T23-T25（全息框架各部分）修改
- **任何被下游节点修改叙事的节点**：当下游节点需要修改上游叙事片段时，必须启用版本管理

### 版本生成规则

1. **首次产出**：节点首次产出叙事片段时，版本号为 `v1`
   ```
   §ref:T13:core_synthesis:v1
   ```
2. **后续修改**：后续节点修改该叙事片段时，版本号递增（v2、v3...），**不得覆盖原版本**
   ```
   §ref:T13:core_synthesis:v2  # T13b 修改后的版本
   §ref:T13:core_synthesis:v3  # T22 再次修改后的版本
   ```
3. **原始版本保留**：`v1` 版本永久保留在 NRSF 中，作为审计基线
4. **版本元数据**：每个版本必须记录以下元数据：

```yaml
version_metadata:
  - version: "v1"
    modifier: "T13"
    modified_at: "ISO 8601 timestamp"
    modification_reason: "首次产出"
    parent_version: null
  - version: "v2"
    modifier: "T13b"
    modified_at: "ISO 8601 timestamp"
    modification_reason: "二次综合修正——补充领域引擎分析后的结论修正"
    parent_version: "v1"
```

### 版本引用规则

下游节点引用启用版本管理的 §ref 时遵循以下规则：

1. **默认引用最新版本**：未显式指定版本号时，自动解析为最新版本
   ```
   §ref:T13:core_synthesis  →  自动解析为最新版本（如 v3）
   ```
2. **显式引用特定版本**：在 context_package 中显式指定版本号
   ```yaml
   context_package:
     refs:
       - ref: "§ref:T13:core_synthesis:v1"
         purpose: "审计原始综合结论"
       - ref: "§ref:T13:core_synthesis"  # 不带版本号 → 最新版本
         purpose: "消费最新综合结论"
   ```
3. **版本对比引用**：下游节点可同时引用多个版本进行差异分析
   ```yaml
   version_comparison:
     original: "§ref:T13:core_synthesis:v1"
     latest: "§ref:T13:core_synthesis:v3"
     diff_purpose: "识别历次修正的累积差异"
   ```

### 版本解析规则（严格解析，不静默跳过）

1. **§ref 不存在则报错**：引用的 §ref 在 NRSF 中不存在时，抛出 `§ref_NOT_FOUND` 错误，**不得静默跳过**
   ```yaml
   ref_resolution:
     on_not_found: "ERROR"
     error_format: "§ref_NOT_FOUND: {ref} 在 NRSF 中不存在"
     action: "阻塞当前节点执行，返回错误信息给 Orchestrator"
   ```
2. **版本不存在则报错**：引用的版本号不存在时，抛出 `§ref_VERSION_NOT_FOUND` 错误
   ```yaml
   version_resolution:
     on_version_not_found: "ERROR"
     error_format: "§ref_VERSION_NOT_FOUND: {ref} 的版本 {version} 不存在，可用版本: {available_versions}"
     action: "阻塞当前节点执行"
   ```
3. **narrative_id 不存在则报错**：引用的 narrative_id 不存在时，抛出 `§ref_NARRATIVE_NOT_FOUND` 错误
4. **禁止静默跳过**：任何 §ref 解析失败都不得静默跳过或使用空值替代——必须报错并阻塞执行

### 版本管理在 nrsf_refs 中的标记

启用版本管理的 §ref 在 nrsf_refs 中必须标记 `versionable: true`：

```yaml
nrsf_refs:
  - node_id: "T13"
    narrative_id: "core_synthesis"
    version: "v1"
    summary: "认知综合核心叙事"
    token_count: 450
    versionable: true  # 启用版本管理
  - node_id: "T13"
    narrative_id: "depth_satisfaction"
    version: "v1"
    summary: "深度满意度评分"
    token_count: 200
    versionable: true
```

### 版本冲突解决

当多个节点同时修改同一叙事片段时：
1. 按 DAG 拓扑序确定修改优先级——拓扑序靠后的节点修改优先
2. 并行修改（同一拓扑层）产生 alternate 版本，标注 `alternate_of` 字段
3. Orchestrator 负责合并 alternate 版本，生成最终版本

```yaml
alternate_version:
  - version: "v2a"
    modifier: "T13b"
    alternate_of: "v1"
  - version: "v2b"
    modifier: "T22"
    alternate_of: "v1"
  merged_to: "v3"
  merged_by: "Orchestrator"
```

## 并发写入协议

### NRSF-Full（全量叙事研究状态文件）
```
nrsf/
├── header/
│   ├── session_id
│   ├── created_at
│   ├── updated_at
│   └── output_type
├── persona_card/
│   └── {T01b 产出的十二字段画像}
├── nodes/
│   ├── §T01-{ts}/
│   │   ├── nrsf_refs
│   │   └── narrative_body
│   ├── §T01b-{ts}/
│   │   ├── nrsf_refs
│   │   └── narrative_body
│   ├── §Phase-1-{ts}/
│   │   ├── nrsf_refs
│   │   └── narrative_body
│   ├── §T02-{ts}/
│   │   ├── nrsf_refs
│   │   └── narrative_body
│   ├── §T09-{ts}/
│   │   ├── nrsf_refs
│   │   └── narrative_body
│   ├── §T13-{ts}/
│   │   ├── nrsf_refs
│   │   └── narrative_body
│   ├── §T22-{ts}/
│   │   ├── nrsf_refs
│   │   └── narrative_body
│   └── ...
├── gates/
│   ├── gate_alpha/
│   ├── gate_beta/
│   ├── gate_gamma/
│   ├── gate_delta/
│   └── gate_final/
└── meta/
    ├── total_nodes
    ├── total_tokens
    └── completion_status
```

### NRSF-Summary（叙事研究摘要）
- 字数限制：≤ 8000 字
- 包含：session_id、output_type、persona_card 摘要、各节点关键叙事摘要、Gate 检查结果摘要、渲染建议
- 用途：T21 知识回收写入 Mem0

### persona_card 在 NRSF 中的位置
- 路径：`nrsf/persona_card/`
- 由 T01b 写入，在 NRSF-Full 和 NRSF-Summary 中均有体现
- 下游节点通过 `nrsf/persona_card/` 读取，不得自行修改

---

## §persona_card-{YYYYMMDDHHmmss}

### 槽位定义

`§persona_card-{YYYYMMDDHHmmss}` 是 NRSF 中的顶级叙事槽位，与各节点 `§T01-{ts}` 等并列。时间戳 `{YYYYMMDDHHmmss}` 为 persona 初始化时间，由 T01b 在写入时生成。

```yaml
persona_card_slot:
  slot_id: "§persona_card-{YYYYMMDDHHmmss}"
  writer: "T01b_voice_calibration"
  readers: ["T20a_research_render", "T20b_wechat_render", "T20c_course_render", "T19_quality_delivery"]
  write_once: true
```

### 12 字段 persona_card 内容

```yaml
persona_card:
  # === 12 采集字段（对应 persona-schema.yaml Yang's 12 fields） ===
  identity: string
  core_values: string
  personal_stories:
    - scenario: string
      emotion: string
      turning_point: string
      clarity_status: "完整 | 待补充"
  catchphrase: [string]
  emotion_expression: string
  self_deprecation: string
  knowledge_zones: [string]
  cultural_refs: [string]
  humor_style: string
  reader_name: string
  ending_pref: string
  style_ref: string

  # === derived_from 字段（T01b 推导，非直接采集） ===
  communication_style: string   # derived_from: identity + emotion_expression + humor_style
  emotional_baseline: string    # derived_from: emotion_expression + self_deprecation + personal_stories
```

### story_clarity_status

```yaml
story_clarity:
  total_stories: integer
  complete_count: integer
  pending_count: integer
  status_per_story:
    - story_index: integer
      clarity_status: "完整 | 待补充"
      missing_elements: [scenario | emotion | turning_point]
  overall: "全部完整 | 部分待补充 | 无故事"
```

### init_source

```yaml
init_source:
  type: enum
  values:
    - interactive      # 用户通过交互完整采集
    - exhaust-retry         # 用户跳过/拒绝，使用默认值
    - user_override    # 用户手动覆盖部分字段
    - generic          # persona_mode=generic，未采集任何人设
  timestamp: "ISO 8601"
  persona_mode: "customized | generic"
```

### 不可变约束

**一经写入，下游节点不得覆盖。** persona_card 是 NRSF 中唯一具有不可变性的叙事槽位。

```yaml
immutable_constraint:
  rule: "persona_card 字段一经 T01b 写入即锁定，所有下游节点仅可读取，不得修改"
  exception: "仅 T18 supervisor 标注 persona_drift 后，T20 渲染器可触发强制修正"
  drift_correction_flow:
    - "T18 在 Gate 检查中检测到 persona 偏离 → 输出 persona_drift 标注"
    - "T20 收到 persona_drift 后，在渲染中强制对齐 persona_card 原始值"
    - "persona_card 原值不变，仅修正渲染输出中的偏移"
  audit: "每次读取操作记录 reader_node_id + read_timestamp"
```

### 认知安全等级

每个 persona_card 槽位附带认知安全元数据，控制人设信息在渲染输出中的暴露程度：

```yaml
cogsec_level:
  field: "cogsec"
  type: enum
  values:
    L0: "公开 — 可在渲染输出中直接展示（如 identity、catchphrase）"
    L1: "内部 — 仅用于风格控制，不直接暴露在输出中（如 core_values、humor_style）"
    L2: "敏感 — 仅用于 T01b 推导 derived_from 字段，不传递至下游可见（如 personal_stories 原始文本）"
    L3: "高风险 — 仅在 T01b 内部使用，不得以任何形式出现在 NRSF-Summary 或渲染输出中"
  default_per_field:
    identity: L0
    core_values: L1
    personal_stories: L2
    catchphrase: L0
    emotion_expression: L1
    self_deprecation: L1
    knowledge_zones: L1
    cultural_refs: L1
    humor_style: L1
    reader_name: L0
    ending_pref: L1
    style_ref: L1
    communication_style: L1
    emotional_baseline: L1
```

### 更新触发器（N-03 级联）

当以下条件触发时，自动更新 persona_card 的关联元数据：

```yaml
update_triggers:
  total_word_count:
    trigger: "NRSF 全量字数累计超过上一阈值时更新"
    thresholds: [5000, 10000, 20000, 40000, 80000]
    action: "更新 persona_card 的 total_session_words 字段"
    consumer: "T20 渲染器据此调整 persona 字段注入密度（字数越少，注入越精炼）"
  cited_source_count:
    trigger: "上游节点 nrsf_refs 中 source_count 更新时级联"
    action: "更新 persona_card 的 cited_source_count 字段"
    consumer: "T19 质量判定据此评估信息广度"
```

### NRSF 分层摘要机制（R-C3）

当 NRSF 累积数据量超过 8000 tokens 时，自动触发分层摘要生成。后续节点默认引用分层摘要，按需展开完整内容：

```yaml
layered_summary:
  trigger: "NRSF-Full 预估 token 数 ≥ 8000"
  layers:
    L0_一句话:
      max_length: "≤ 30 字"
      content: "全局主题提炼，包含 output_type + 核心结论"
      usage: "门控节点快速校验、T19 质量判定摘要"
    L1_一段:
      max_length: "≤ 200 字"
      content: "各阶段关键叙事摘要 + 主要 Gate 检查结果"
      usage: "下游渲染节点默认引用层"
    L2_一页:
      max_length: "≤ 800 字"
      content: "包含关键 §ref 指针的叙事骨架，保留结论性陈述"
      usage: "T20 渲染器在需要深入上下文时按需展开"
    L3_完整:
      max_length: "无上限"
      content: "对应节点的完整 narrative_body + nrsf_refs"
      usage: "仅在当前阶段 deps 链上直接依赖时透传完整内容"
  default_reference: "后续节点默认引用 L1 分层摘要，通过 §ref 指针按需上钻至 L2/L3"
  compression_rules:
    - "L3→L2：折叠过程性笔记（推理链中间步骤、探索性分析）"
    - "L2→L1：仅保留结论性陈述 + 关键证据的 §ref 指针"
    - "L1→L0：提炼为单句主题陈述"
    - "删除：已被后续节点覆盖/修正的过时结论"
  direct_passthrough:
    rule: "仅当前阶段 deps 链上直接需要的 NRSF 节点透传 L3 完整层"
    example: "T13 阶段仅透传 T09、T02 的 L3 完整叙事，其他节点默认 L1 摘要"
  recovery: "下游节点可通过 §ref 指针按需恢复被折叠的完整叙事体（L2 → L3 上钻）"
```

## 并发写入协议

### 写入策略
Sub-Agent 将产出写入临时文件（tmp/），Orchestrator 负责合并到 NRSF-Full。

### 写入流程
1. Sub-Agent 完成节点任务后，将 nrsf_refs 写入 `tmp/{node_id}_{ts}.json`
2. Orchestrator 在每个 Sub-Agent 完成后，将 tmp 文件合并到 NRSF-Full
3. 合并时检查 nrsf_refs 的格式正确性
4. 写入完成后删除 tmp 文件

### 冲突解决策略
- 同一 narrative_id 的多次写入：最新版本优先（version 号最大者保留）
- 同一 narrative_id 的同一版本写入：第一次写入保留，后续写入合并为 alternate 版本
- 冲突时写入 NRSF 冲突日志

### Mem0 存储规范
- 原子添加：每个 narrative 作为独立实体添加
- 三路检索：语义检索 + 关键词检索 + 实体检索
- 生命周期：对话结束后不持久化 NRSF 全量数据，仅保留 NRSF-Summary 的关键洞察

## NRSF 生命周期清除规则

### 清除时机
对话结束后，NRSF 数据按以下规则清除：

1. **NRSF-Full**：立即清除，不持久化
2. **NRSF-Summary**：提取关键洞察后清除原始数据
3. **persona_card**：不持久化，仅本次会话使用
4. **tmp/** 文件：任务完成后立即清除
5. **Mem0 存储**：仅保留 NRSF-Summary 中的关键洞察（≤ 500 字），标记为 `session:expired` 后 72 小时清除

### 清除验证
Orchestrator 在对话结束时验证：
- nrsf/ 目录下无残留文件
- Mem0 中无完整 persona_card 数据
- tmp/ 目录为空

## output_schema
```yaml
nrsf_refs:
  type: array
  items:
    type: object
    required: [node_id, narrative_id, version, summary]
    properties:
      node_id:
        type: string
        description: "产生该叙事的节点标识"
      narrative_id:
        type: string
        description: "叙事片段唯一标识"
      version:
        type: string
        pattern: "^v\\d+$"
        description: "叙事版本号"
      summary:
        type: string
        max_length: 200
        description: "叙事片段摘要"
      token_count:
        type: integer
        description: "叙事片段 token 数"
      tags:
        type: array
        items:
          type: string
        description: "叙事标签"
```

## self_check_before_output
- [ ] §ref 标记语法是否正确（§ref:node_id:narrative_id:version）
- [ ] node_id 是否在 deps 链上
- [ ] narrative_id 是否为本节点生成
- [ ] version 格式是否为 v{n}
- [ ] summary 是否 ≤ 200 字
- [ ] nrsf_refs 列表是否包含所有关键叙事片段
- [ ] 不会与已有 §ref 冲突（相同 narrative_id 的不同版本 OK）
- [ ] NRSF-Full 模板是否包含 §T01b 段和 §Phase-1 段

## must_not
- 不得引用不在 deps 链上的节点
- 不得修改已写入 NRSF 的其他节点的 narrative_body
- 不得在 NRSF-Full 中持久化 persona_card 全量数据
- 不得在对话结束后保留 NRSF 全量数据
- 不得在叙事引用中包含敏感用户信息
- 不得创建重复的 narrative_id（同节点同 id 同版本）

## knowledge_refs
- execution-protocol.md
- output-rendering-protocol.md
- checkpoint-protocol.md
## 协议概述补充

NRSF（Narrative Reference Stack Frame）协议定义认知流水线的研究笔记格式规范。NRSF采用§ref段落级引用机制，支持跨节点直通传递和增量追加。

**核心原则**：NRSF只追加不删减，确保研究过程完整可追溯。

## 穷尽重试策略

### L1: 完整NRSF写入
正常执行NRSF叙事累积体系写入

### L2: NRSF写入部分失败
- 持续重试直至质量达标，不设上限

### L3: NRSF体系不可用
- 持续重试直至质量达标，不设上限

### L4: 输出系统完全不可用
- 持续重试直至质量达标，不设上限


---

## 测试用例 (D3.4.4)

### 测试用例 1：§ref 标记格式校验

**给定输入**：节点产出包含 §ref:T02:main_narrative:v1。

**应产出**：§ref 解析成功，node_id=T02、narrative_id=main_narrative、version=v1，从 NRSF 中提取对应叙事片段。

### 测试用例 2：NRSF 只追加不删除

**给定输入**：T13 修订了之前的叙事片段 main_narrative（v1→v2）。

**应产出**：NRSF 保留 v1（不删除），追加 v2，下游节点默认引用 v2，可在 context_package 指定引用 v1。

### 测试用例 3：并发写入冲突

**给定输入**：T10/T11/T12 并行执行，同时向 NRSF 写入叙事片段。

**应产出**：并发写入协议生效，每个节点写入独立的 narrative_id（path_10/path_11/path_12），无冲突。

### 测试用例 4：NRSF 写入失败穷尽重试

**给定输入**：NRSF 写入失败（磁盘满）。

**应产出**：按 L1→L2→L3→L4 穷尽重试：L1 完整写入 → L2 部分写入重试 → L3 内存暂存 → L4 输出系统完全不可用时持续重试。
