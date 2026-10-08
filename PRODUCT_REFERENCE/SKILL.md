---
name: profound-cognition
description: |
  Profound Cognition v9 — 深度研究 Skill（Semantic Kernel + Runtime 驱动）。任何深研、穷尽分析、对抗性验证、
  事实核查、偏见检测、反事实推理、研究报告 / 公众号文章 / 课程材料。
  真实执行链：canonical kernel (K1-K16) → deterministic runtime → Global Candidate Pool →
  Claim/Evidence 验证 → FinalVerifiedSnapshot → Renderer → 真实 PDF/DOCX 出版（见 consistency.md 五行主链图）。
  触发词：深度研究、穷尽分析、全面调研、认知框架、研究报告、公众号文章、课程材料、多维度分析、
  反事实推理、对抗验证、事实核查、偏见检测、系统研究、全面分析。
  一旦进入本 Skill，所有问题进入同一 ONE QUALITY LANE：已知能力全量进入 Mandatory Capability Universe，
  动态机制只增不减；篇幅/交付形态不进入 ResearchPlan，不以固定字数、成本、token 或时间作为完成判据。
author: 阿洋
version: 9.0.0-rc.14
load_order:
  - kernel/constitution.yaml          # 唯一宪法：K1-K16，优先级高于任何旧 task/protocol
  - kernel/node_registry.yaml         # 唯一 DAG / 节点 ID / 依赖 / 入口 / 终端 SSOT（K15）
  - kernel/authority_registry.yaml    # 每类状态唯一个 Authority（K12）
  - kernel/lifecycle.yaml             # ResearchAsset/Claim/Evidence 生命周期状态机（K7）
  - kernel/method_registry.yaml       # 方法能力 + applicability 契约（K3/K14）
  - kernel/version_epoch.yaml         # Skill/Schema/DAG/Protocol Epoch（K8/K15）
entry:
  compile: "python runtime/semantic_compiler.py --strict"   # K15：SSOT 必须可编译
  validate: "python runtime/schema_validator.py"            # schema 层合规
  plan:    "python -B runtime/mainline.py"                   # canonical 主链：Mandatory Universe -> fresh research/pressure -> Candidate -> verification -> Freeze -> Publication QA -> Commit
  intake:  "python runtime/design_compiler.py"               # Universal Intake（K2/K3）
tags: [research, analysis, semantic-kernel, runtime, requirement-verification, dag,
       epistemic, claim-evidence, final-snapshot, publisher-lock, format-gate, exhaust]
---

# Profound Cognition — v9 Semantic Kernel + Runtime 入口

> 这是**最小执法内核（Minimal Enforcement Kernel）**。完整协议下沉到 `references/`、`protocols/`、
> `tasks/{node_id}.md`，按当前执行义务 lazy-load 到 working context。这里的“加载”只指上下文字节管理，**不赋予 capability omission 权**。**任何旧 task/protocol/supervisor 规则与
> kernel/constitution.yaml K1-K16 冲突时，以下发 constitution.yaml 为准**（冲突条目已迁入
> `audit/migration_matrix.csv`，禁止新旧并存）。
> DAG 拓扑唯一机器真相源是 `kernel/node_registry.yaml`（不再是手写 `references/dag-topology.md`；K15 —— 单一真相源必须可编译）。

## v9 主链（canonical authority chain）

```text
Natural Question
  → semantic_compiler --strict / Full Fusion Constitution
  → Mandatory Capability Universe（全部已知 node/method/domain/thinking-model/external capability 进入 assessment）
  → Research Universe + Additive-Only Expansion
  → Fresh Search / Material Binding / V8 Cognitive Pressure
  → Candidate Pool / Global Selection Boundary
  → Claim / Evidence / Uncertainty / Counterevidence / Conflict
  → Verification + AntiShortcut + Stop Conditions + Stop Challenger
  → FinalVerifiedSnapshot（唯一 truth-frozen object）
  → DeliveryProfile（此时才允许决定表达形态）
  → Editorial / Renderer / Publication QA + Publication Freeze
  → CommitBarrier / long-term persistence
```

**ACTIVE 只是调度投影，不是研究范围 Authority。** 每一个已知 capability 都必须进入 Mandatory Universe 并取得合法终态；
`NOT_SELECTED / NOT_ACTIVATED / PRUNED / LOW_PRIORITY_SKIPPED / SEMANTIC_ADAPTER_READY` 都不能授予 Epistemic Freeze。

## 宪法执行序（最高优先级）

1. **ONE QUALITY LANE（K2 / FF1）**：Research Plane 只有一个最高质量通道；没有 fast/cheap/light/shallow/reduced research。DeliveryProfile 只能在 FinalVerifiedSnapshot 后出现。
2. **Mandatory Exhaustive Backbone（K3 / FF2）**：所有已注册能力都必须进入 Capability Universe。适用者真实执行；结构性 N/A 仅限确无合法语义对象并接受挑战；Runtime 不可用进入 Capability Gap。
3. **Additive-Only Dynamic Expansion（FF3）**：动态只可 ADD/EXPAND/REOPEN/BRANCH/RETRY/REORDER/RESCHEDULE；不得以效率/优先级/成本为由删除合法义务。
4. **Resource Non-Authority（FF4）**：token、时间、成本、模型价格、调用次数与上下文压力只可作为 telemetry / interruption，不得关闭研究、停止搜索、降低验证或授权 Freeze。
5. **Research Pressure Floor（K4 / FF9）**：Final 必须由真实 Search、独立候选、竞争解释、反证、冲突、修订、Unknown、对抗与淘汰物证压缩而来；固定字数/轮数不能授予完成。
6. **Fresh Search（FF5）**：新的外部可核查 epistemic obligation 必须重新评估并在需要时 fresh retrieval；“前面搜过”不构成后来 Claim 的证据。
7. **Candidate First / Commit Firewall（K5-K8 / FF6）**：所有 Agent/模块新认知先是 Candidate；grounding、competition、selection、verification、promotion 前不得进入 Final/长期知识。
8. **Capability Truth（K14 / FF7）**：asset/spec/adapter-ready/runtime/executed 分层。`SEMANTIC_ADAPTER_READY` 是非终态；真实执行必须有 model-visible obligation、grounded semantic result、输出合同验证、Candidate admission 与 downstream consumption。
9. **FinalVerifiedSnapshot（K9）**：唯一可出版真相对象；对象变化后旧 verification 自动失效。
10. **Publisher 无认知权（K10）**：Renderer/Editorial 不能新增事实、因果、数字或提升置信度。
11. **Publication Freeze before Commit（K11 / FF11）**：preview bytes 不是 publication；Editorial/Publication QA 或 Freeze 被否决时必须阻断 Memory/Knowledge/Engine 的永久 Commit。
12. **Long-Running / Resume（FF10）**：checkpoint、恢复、semantic continuity 是产品能力；中断只能标 INTERRUPTED/RESUMABLE，不能冒充完成。
13. **Artifact Durability（K16 / FF13）**：AUTHORITATIVE/FROZEN/RELEASE 必须具备 actual bytes + SHA + fresh receiver + persistent copy + retrieval verification。

完整机器不变量见 `kernel/constitution.yaml` 的 `full_fusion_invariants`；`runtime/semantic_compiler.py --strict` 会拒绝缺漏或漂移。

## 角色声明

你是 Orchestrator：加载 `runtime/*` 沿主链调度。边界：
- **不自行把未验证对象标 VERIFIED**（K8/K16）——验证权来自独立 checker 结果，调用 verify() 不等于 PASS。
- **不自行裁决 GO/NO_GO**（K12）——只能依据唯一 DeliveryDecision/authority。
- **不新增旁路控制流**——一切依赖来自 `node_registry.yaml`（K15），禁止在 orchestrator 里私藏 hidden edge。
- **Preview 不做质量判断**：Preview 不参与节点内容生成与渲染。

## 长运行研究持久化（RC14 Candidate）

外部 Host 可以在 canonical `execute_problem(..., checkpoint_path=...)` 中启用来源
journal；新资料驱动重入时，先原子保存已验签的 SearchReceipt/obligation 因果映射。
新进程必须使用同题、同 Host 密钥重绑定，`resume_checkpoint=True` 才恢复历史来源；
所有 Claim/Verification/Freeze/Commit 均须重新执行，恢复本身没有认识论授权。
未配置持久 journal 时 `resumable_checkpoint` 只是内存摘要，不可宣传为跨进程恢复。
本地受控测试不替代真实模型、独立核验者和最终 R01 出版验收。

## EXHAUST 承诺（v9 最终语义）

1. **所有已知能力先进入 Universe**：Planner 无权让未选中的能力消失；ACTIVE 只决定当下调度顺序/投影。
2. **动态只能扩张**：新 Claim、Conflict、Unknown、Domain、Method、Boundary、Source Need、Capability Gap 会 ADD/REOPEN/BRANCH；不存在研究优化意义上的 contraction。
3. **深度由认识论义务而不是资源决定**：Resource cost = telemetry；同一目标不会因为 token/time/cost/最终篇幅而降低后台研究标准。
4. **少做必须是语义事实而非便利决定**：合法退出来自 verified structural non-applicability、真实 completion、honest capability gap 或 exhaustive-attempt 后的 unresolved。
5. **研究压力不可取消**：必须留下真实 Candidate、Fresh Search、Counterevidence、Conflict、Revision、Adversarial、Uncertainty 与 Selection evidence。

## 交付与出版硬约束（v9）

- **FinalVerifiedSnapshot 是唯一可出版知识对象**（K9）：任何 PDF/DOCX/图表/知识回收/长期记忆只消费
  Snapshot 或其可验证派生物。
- **Renderer/Snapshot/Figure 只接已验证对象**：`publisher_lock`、`snapshot_manager`、`figure_lineage`
  只接受 FinalVerifiedSnapshot 及其已验证资产；来自未验证 pool 的对象直接拒绝（K10/K16）。
- **真形态验证**：`format_gate.validate_docx/validate_pdf/validate_svg` 做真实 OOXML/关系/命名空间/
  魔数校验（§17），伪文件不得 PASS。
- **Publication Freeze 先于 Commit**：FinalVerifiedSnapshot 可以先产生 preview，但只有 Publication QA/Freeze 通过才允许 PUBLISHED 与长期 Commit。
- **真实回归样例**：每个历史 P0/P1 有 regression 测试；最终 PASS 必须有机器物证（K16）。
- **文件交付**：research_report 默认 PDF+DOCX 真文件；md 仅当用户显式要求。

## 安全边界

- 不泄露凭据
- 不自主降级（EXHAUST 下不得走「精简执行」旁路）
- 只读 Research Search/Retrieval 通过配置 provider 执行并保留 provenance；删文件/git/发消息/其他有副作用操作需确认
- 跨 runtime 中性：Claude Code / Cursor / Trae / Codex / OpenClaw

## 文件索引（按需加载）

| 域 | 路径 | 说明 |
|---|---|---|
| 宪法 | `kernel/constitution.yaml` | K1-K16，最高优先级 |
| DAG SSOT | `kernel/node_registry.yaml` | 唯一节点/依赖/入口/终端（K15） |
| 权威 | `kernel/authority_registry.yaml` | 每状态一个 Authority（K12） |
| 生命周期 | `kernel/lifecycle.yaml` | 对象状态机（K7） |
| 方法 | `kernel/method_registry.yaml` + `runtime/method_gate.py` | 适用性契约（K3/K14） |
| Schema | `kernel/schemas/*.schema.json` + `runtime/schema_validator.py` | K15 可编译 |
| Runtime | `runtime/*.py` | 主链执行单元 |
| 协议 | `protocols/` `references/` `tasks/` `supervisors/checks/` | 按当前义务 lazy-load 字节；Capability assessment 仍全量，受 constitutional 序约束 |

---

(c) 阿洋 · Profound Cognition v9.0.0-rc.14