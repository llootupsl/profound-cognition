# Profound Cognition — Host-Native Deep Research & Publication Skill

> **V9 RC14 · Host-Native Spec-Corrected Candidate**（版本 `9.0.0-rc.14-host-native-spec-candidate`）
> 一个可安装的 Agent Skill：内置按 SHA-256 冻结的多 Agent 深度研究与出版 OS，全部研究执行交给 **Agent 宿主原生**的搜索、模型与隔离验证能力——**不需要配置任何第三方模型 / 搜索 API Key**。

**当前成熟度：`INSTALLABLE_LOCAL_ENGINEERING_CANDIDATE`（可安装的本地工程候选）——不是 Product RELEASE。**
详见 [STATUS.md](STATUS.md) 与 [IMPLEMENTATION_COVERAGE_AND_RELEASE_GAPS.md](IMPLEMENTATION_COVERAGE_AND_RELEASE_GAPS.md)。

---

## 这是什么

Profound Cognition 是一套"深研究 → 独立验证 → 认识论冻结 → 出版"的完整研究操作系统。本仓库把它打包成符合 **Agent Skills 规范**（根目录 `SKILL.md` 含必需的 `name` / `description` frontmatter）的可安装 Skill：

- **宿主原生执行**：检索网页正文、模型推理、独立审查全部使用宿主已有的工具与当前模型；缺失的能力如实保留为 `UNAVAILABLE / UNRESOLVED`，禁止伪装成"研究已完成"。
- **冻结 Product**：研究控制与认识论权威来自字节级锁定的 RC14 Product（内嵌于 `FROZEN_HANDOFF.zip`），本层只是宿主平台的原生工具适配器，绝不修改 Product。
- **不可妥协的认识论契约**：候选结论一律先入 Draft Pool；独立验证通过才有最终权威；真实来源字节 > 自我报告的结论；没有独立验证者必须如实 HOLD；只有 Stop Challenger 支持的认识论闭合与 truth-frozen 快照才允许出版。渲染器无新事实权。
- **Fail-closed**：无法形成真实出版时拒绝交付，不制造假成品。

## 完整性身份（SHA-256）

| 对象 | SHA-256 |
|---|---|
| RC14 Product（冻结研究 OS） | `7b538ae5cef0fce538ba1ff557f3fe1e1b61cdcd63c6c6e76a3168c14ebaa3e5` |
| Frozen Handoff（`FROZEN_HANDOFF.zip`） | `6b233e25914530f5aa95c485f90e22330a900e2c1cfcb996220893d80b960b54` |
| Bridge（`BRIDGE_REFERENCE/R01_REAL_MODEL_FILE_BRIDGE.py`） | `4ef997683636a49250f27c398d6f265b6f326e56d3a48331ccc91fb09578d370` |
| 发行候选 ZIP（`dist/`，29 个条目） | `4d73d7626ac510709b650d79babab14ecf6a2c1a368f904aa996b31ad4a485c8` |

安装后可用 `python -B src/native_host_bridge.py inspect --handoff FROZEN_HANDOFF.zip` 复验 Product / Handoff 哈希。

## 仓库结构

```
├── SKILL.md                 # Agent 平台入口（Agent Skills frontmatter 规范）
├── FROZEN_HANDOFF.zip       # 按 SHA 锁定的 RC14 Product + 字节级请求/响应 Bridge（不修改）
├── PRODUCT_REFERENCE/       # 取自 RC14 原始 Product 的 Skill 与 Kernel 宪法只读副本
│   └── kernel/              #   constitution / node / authority / method 注册表
├── BRIDGE_REFERENCE/        # R01 真实模型文件桥（执行专用参考件）
├── src/
│   ├── native_host_bridge.py   # 宿主原生 transport、证据留痕、启动与交付（无第三方 API 客户端）
│   └── publication_handoff.py  # 成品字节移交与复验（不授予发布授权）
├── tests/                   # 受控生产入口与恶意/无效响应测试
├── QA/                      # 本地测试证据（原始日志）
├── dist/                    # 唯一候选发行 ZIP
├── MANIFEST.sha256          # 全树字节清单
├── STATUS.md                # 当前阶段决策与限界
├── IMPLEMENTATION_COVERAGE_AND_RELEASE_GAPS.md   # 工程证据矩阵与发布缺口
└── CONTROL_STATE_RECONCILIATION_PROPOSAL.md      # 项目控制状态和解提案（非 Project 权威）
```

## 安装

1. 下载 [`dist/PROFOUND_COGNITION_V9_RC14_AGENT_SKILLS_SPEC_CORRECTED_CANDIDATE.zip`](dist/PROFOUND_COGNITION_V9_RC14_AGENT_SKILLS_SPEC_CORRECTED_CANDIDATE.zip)（或直接使用本仓库源码树，两者字节一致）。
2. 校验完整性：`sha256sum -c MANIFEST.sha256`。
3. 解压到兼容 Agent 宿主的 Skills 目录下、名为 `profound-cognition` 的**单独 Skill 目录**；不要把内容直接散放在多个 Skill 的共用根目录。

要求：本地 Python 3、可读写的运行目录、宿主具备网页正文检索工具、可执行当前模型、可真正隔离的审查 Agent。

## 使用（USER_RESEARCH 普通研究流程）

让宿主 Agent 阅读根目录 `SKILL.md`，针对任意自然语言研究问题执行：

```bash
# 1. 验证冻结身份
python -B src/native_host_bridge.py inspect --handoff FROZEN_HANDOFF.zip

# 2. 解包冻结 Product 到独立空 evidence 目录（无需任何项目授权文件）
python -B src/native_host_bridge.py prepare --handoff FROZEN_HANDOFF.zip --evidence <独立的新目录>

# 3. 以真实问题启动（scope 固定为 user）
python -B src/native_host_bridge.py start --scope user \
  --evidence <独立的新目录> --question '你的自然语言研究问题' \
  --model-provider <主Agent主体ID> --model-id <宿主模型ID> \
  --verifier-provider <隔离审查主体ID> --verifier-model <审查模型ID>

# 4. 循环：next 取真实请求 → 宿主实际调用搜索/模型/隔离审查 → submit 回传
python -B src/native_host_bridge.py next     --evidence <目录>
python -B src/native_host_bridge.py submit   --evidence <目录> --result result.json --trace trace.json

# 5. Product 给出合法终态后，移交真实成品字节（非发布授权）
python -B src/native_host_bridge.py deliver  --evidence <evidence目录> --destination <新的空成品目录>
```

`result.json` / `trace.json` 必须记录宿主**实际返回**的字节；`kind`、`request_sha256`、`result_sha256`、`host_tool_call_id`、`host_context_id` 须与实际调用一致。旧响应、模拟回复、虚构工具 ID、纯 URL 或摘要均被拒绝。

### 项目 R01（工程验收）不在本 Skill 授权范围内

通用安装版一律拒绝 `start --scope r01`：本地放置的状态文本（即使写着 `R01_AUTHORIZATION: GRANTED`）不构成项目授权。正式 R01 只能由经过独立项目控制状态核验、具备受信执行权的项目执行方启动冻结 Product，并按原始证据独立验收。当前 R01 未授权。

## 测试与证据（本地受控）

- 冻结 Product Full Fusion 套件：**61/61 PASS**（限于其自身测试契约）。
- 宿主原生字节 transport 与负例路径：**20/20 PASS**（含陈旧响应、伪造 provenance、非空 evidence 目录、Handoff 哈希不匹配等拒绝路径）。
- USER_RESEARCH 受控正向入口 + 5 项负向守卫 PASS；任意自然语言问题可驱动真实 RC14 Product 发出真实 `OPEN_WORLD_SEARCH` 请求。
- 新鲜解包外层清单、Product 引用字节相等性、ZIP CRC 与嵌套 Handoff 身份校验 PASS。

**如实保留的未通过项**：`tests/contract_consolidation` 在独立重跑时未通过——旧 fixture 产出重复模板化流程结果，被 Product 拒绝 105 次能力执行后无法进入出版冻结，随后测试因假设非空 `publication_freeze` 而报错。该负结果不被改写为 PASS，也不据此放松验证器。

CI（`.github/workflows/expand-rc14-candidate.yml`）在推送/手动触发时按 SHA 校验发行 ZIP、安全解包并复验全树清单。

## 状态与限界（不可夸大）

已证明的仅是：运行入口可用、真实 Product 搜索请求产生、受控回传与负例拒绝、冻结 Product 字节未变。**尚未证明**：

- 真实 Agent 宿主完成整条"外部检索 → 接地模型推理 → 候选准入 → 独立审查 → Stop Challenger 闭合 → FinalVerifiedSnapshot → 出版冻结 → 最终用户成品"链路；
- 宿主自报的模型 / Agent 身份构成真正的独立性；
- 项目控制状态已更新（Project-backed 控制文件仍是陈旧版本）。

因此本候选可用于宿主原生执行测试，但**不得**被表述为"独立验证过的研究/出版"或 Product RELEASE。`deliver` 的验收仅为字节完整性，最终独立认识论验收始终 `INDEPENDENT_ACCEPTANCE_PENDING`。

## License

[MIT](LICENSE) © 2025–2026 阿洋
