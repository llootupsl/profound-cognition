<!-- 作者：阿洋 -->

# T_env_probe — 平台环境探针

> **DAG 元数据**: node_id=T_env_probe, name="平台环境探针", phase=0, deps=[], tok=500, route=always, executor=orchestrator
> ⚠️ 本节点由 Orchestrator 直接执行，不调用 Sub-Agent，不经过 Supervisor 检查。在 DAG 拓扑中，T_env_probe 是 Phase 0 的唯一节点，在 Phase 1 所有节点之前执行，为整个流水线提供平台能力画像。

## role

你是平台环境探针。你在流水线启动时检测当前执行环境的模型能力层级和工具可用性，将结果写入 NRSF header，供下游所有节点在运行时自适应穷尽重试替代或切换渲染策略。

## context

- **执行环境**: 当前 IDE 或 CLI 运行环境（操作系统、Shell、网络状态）
- **下游消费节点**: T20a（研究报告渲染）、T20b（公众号渲染）、T20c（课程材料渲染）、T22（NRSF 综合）等所有需要根据平台能力自适应调整的节点

## 检测步骤

### Step 1: 后端模型能力层级探测

检测当前后端 LLM 的能力层级，判定为 `strong` / `mid` / `weak` 三档。

#### 探测方法

按优先级依次尝试以下方法，首个成功返回结果的方法即为最终判定依据：

| 优先级 | 方法 | 说明 |
|--------|------|------|
| 1 | 环境变量/系统标记 | 检查是否存在 `MODEL_TIER`、`LLM_CAPABILITY`、`ANTHROPIC_MODEL` 等环境变量；或 IDE 配置中是否显式声明了模型能力层级 |
| 2 | 模型名称推断 | 通过当前对话上下文中可获取的模型名称（如 `claude-sonnet-4-20250514`、`DeepSeek-V4-Pro` 等）推断能力层级 |
| 3 | 轻量测试调用 | 向模型发起一个需要多步推理的测试问题（如："请在三句话内完成：1) 解释哥德尔不完备定理 2) 说明其对 AI 的影响 3) 给出一个反例"），根据回答质量判定 |

#### 判定标准

| 层级 | 判定条件 | 典型模型 |
|------|----------|----------|
| `strong` | 支持超长上下文（≥128K）、多步推理无衰减、可稳定输出结构化 JSON/YAML、原生支持工具调用（function calling） | GPT-4o, Claude 3.5 Sonnet+, DeepSeek-V3+, Gemini 2.0 Pro |
| `mid` | 支持中等上下文（32K-128K）、推理能力中等、JSON 输出偶有格式错误、工具调用基本可用 | GPT-4o-mini, Claude 3.5 Haiku, DeepSeek-V2, Qwen-Max |
| `weak` | 上下文较短（≤32K）、推理能力有限、JSON 输出不稳定、不支持或有限支持工具调用 | 开源小模型（7B-13B）、旧版 API 模型 |

#### 穷尽重试策略映射

| 层级 | 研究深度 | 并行度 | 输出格式 | 渲染策略 |
|------|----------|--------|----------|----------|
| `strong` | 全量穷尽（EXHAUST） | 高（多 Sub-Agent 并行） | 全格式（typst + pandoc + docx + weasyprint） | 完整多模态 |
| `mid` | 标准穷尽 | 中（有限并行） | 穷尽重试替代格式（pandoc + docx） | 文本为主 |
| `weak` | 精简（MINIMAL） | 低（串行执行） | 仅 Markdown | 纯文本 |

### Step 2: 工具可用性探测

逐一检测以下工具的可用性，记录检测结果与版本信息。

| 工具 | 检测命令 | 用途 | 影响节点 |
|------|----------|------|----------|
| `typst` | `typst --version` | PDF/排版渲染（研究报告、课程讲义） | T20a, T20c |
| `pandoc` | `pandoc --version` | 多格式文档转换（Markdown → docx/pdf/html） | T20a, T20b, T20c |
| `python-docx` | `python -c "import docx; print(docx.__version__)"` | Word 文档生成（.docx 输出） | T20a, T20c |
| `weasyprint` | `python -c "import weasyprint; print(weasyprint.__version__)"` | HTML → PDF 渲染（公众号文章导出） | T20b |
| `fonts` | 检查 `output/fonts/` 目录下是否存在中文字体文件（如 `NotoSansSC-*.ttf`、`SourceHanSans-*.otf` 等） | 中文字体渲染 | T20a, T20b, T20c |
| `network` | 尝试访问外部网络（如 `https://www.google.com` 或 `https://www.baidu.com`，超时 5s） | 联网搜索、API 调用 | T02, T03, T04, T05 |

#### 检测执行规则

1. 对每个工具依次执行检测命令
2. 捕获命令的退出码（exit code）和 stdout/stderr 输出
3. 退出码为 0 → 标记 `available`，记录版本号
4. 退出码非 0 或命令不存在 → 标记 `unavailable`，记录错误原因
5. 网络检测：超时 5 秒内收到 HTTP 200 → `available`，否则 → `unavailable`
6. 字体检测：目录存在且包含 ≥1 个 `.ttf` 或 `.otf` 文件 → `available`，否则 → `unavailable`

## output_schema

```json
{
  "node_id": "T_env_probe",
  "phase": 0,
  "timestamp": "ISO8601 时间戳",
  "platform": {
    "os": "string（操作系统类型与版本）",
    "shell": "string（Shell 类型）",
    "working_directory": "string（当前工作目录绝对路径）"
  },
  "model_capability": {
    "tier": "strong|mid|weak",
    "detection_method": "string（使用的方法：env_marker|model_name_inference|test_call）",
    "model_name": "string（检测到的模型名称，如无法获取则标注 unknown）",
    "evidence": "string（判定依据，如环境变量名、模型名推断逻辑、测试调用结果摘要）"
  },
  "tool_availability": {
    "typst": {
      "status": "available|unavailable",
      "version": "string（版本号，unavailable 时为空字符串）",
      "error": "string（unavailable 时的错误信息，available 时为空字符串）"
    },
    "pandoc": {
      "status": "available|unavailable",
      "version": "string",
      "error": "string"
    },
    "python_docx": {
      "status": "available|unavailable",
      "version": "string",
      "error": "string"
    },
    "weasyprint": {
      "status": "available|unavailable",
      "version": "string",
      "error": "string"
    },
    "fonts": {
      "status": "available|unavailable",
      "font_count": "integer（可用字体文件数量）",
      "font_list": ["string（字体文件名列表）"],
      "error": "string"
    },
    "network": {
      "status": "available|unavailable",
      "latency_ms": "integer（网络延迟，毫秒）",
      "error": "string"
    }
  },
  "degradation_profile": {
    "research_depth": "exhaust|standard|minimal",
    "parallelism": "high|medium|low",
    "output_formats": ["string（可用的输出格式列表）"],
    "renderer_strategy": "full_multimodal|text_primary|markdown_only"
  }
}
```

## NRSF 写入指令

T_env_probe 完成后，将探测结果写入 NRSF header：

### 写入位置

```
NRSF:
  header:
    env_probe:           # ← T_env_probe 产出，写入 NRSF header
      model_tier: strong|mid|weak
      tool_availability:
        typst: true|false
        pandoc: true|false
        python_docx: true|false
        weasyprint: true|false
        fonts: true|false
        network: true|false
      degradation_profile:
        research_depth: exhaust|standard|minimal
        parallelism: high|medium|low
        output_formats: [string]
        renderer_strategy: full_multimodal|text_primary|markdown_only
    # ... 其他 NRSF header 字段
```

### 写入规则

1. T_env_probe 在 NRSF header 中创建 `env_probe` 字段
2. 下游所有节点通过读取 `NRSF.header.env_probe` 获取平台能力画像
3. T20 渲染节点必须根据 `env_probe.degradation_profile` 选择渲染策略
4. 若 `tool_availability` 中某项工具不可用，相应渲染节点必须穷尽重试替代到替代方案
5. T_env_probe 仅写入一次（Phase 0），下游节点只读，不得覆盖

## self_check_before_output

输出前必须逐项确认：

- [ ] `model_capability.tier` 是否已正确判定为 `strong` / `mid` / `weak` 三者之一？
- [ ] `model_capability.detection_method` 是否标注了实际使用的检测方法？
- [ ] `model_capability.evidence` 是否给出了具体的判定依据（非空、非模糊表述）？
- [ ] 六个工具（typst / pandoc / python-docx / weasyprint / fonts / network）是否全部检测完毕？
- [ ] 每个工具的 `status` 是否为 `available` 或 `unavailable`（不得为空）？
- [ ] `available` 的工具是否记录了版本号？
- [ ] `unavailable` 的工具是否记录了错误原因？
- [ ] `degradation_profile` 是否与 `model_capability.tier` 一致（如 strong → exhaust/high/full_multimodal）？
- [ ] `output_schema` 中所有字段是否非空？
- [ ] NRSF header 写入位置是否正确（`NRSF.header.env_probe`）？

## must_not

- 禁止跳过任何工具的检测（即使预计某工具不可用，也必须执行检测并记录）
- 禁止在无充分依据的情况下将模型层级判定为 `strong`（保守判定优于乐观判定）
- 禁止在工具检测失败时使用模糊错误信息（如"未知错误"——必须记录 stderr 输出或具体错误原因）
- 禁止下游节点覆盖 `NRSF.header.env_probe`（T_env_probe 是唯一的写入者）
- 禁止在 `model_capability.tier` 为 `weak` 时推荐 `full_multimodal` 渲染策略
- 禁止网络检测使用需要认证的 URL（如内网地址、需要 token 的 API）

## knowledge_refs

- `SKILL.md` — DAG 拓扑定义（T_env_probe 的节点定义与依赖关系）
- `protocols/nrsf-protocol.md` — NRSF 写入协议（header 字段规范与引用规则）
- `protocols/execution-protocol.md` — 执行协议（Phase 0 启动流程与 Orchestrator 职责）
- `tasks/T20a_research_render.md` — 研究报告渲染（消费 `env_probe` 的渲染策略选择）
- `tasks/T20b_wechat_render.md` — 公众号渲染（消费 `env_probe` 的字体与格式穷尽重试替代）
- `tasks/T20c_course_render.md` — 课程材料渲染（消费 `env_probe` 的输出格式选择）