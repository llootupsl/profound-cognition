<!-- 作者：阿洋 -->

# 版本管理协议 (Version Management Protocol) v3.0

> **协议版本**：v3.0
> **关联需求**：R8-05、R10-05
> **关联目录**：docs/version_history/、scripts/version-diff-tool.py

## 1. 概述

**方法论原理**：版本管理基于"可追溯性是质量基石"的认知假设：框架的每次变更都必须可追溯、可对比、可回滚。没有版本管理，就无法判断"这次变更改进了什么、退化了什么"。本协议定义 Profound Cognition 框架的版本号规则、Diff 报告格式、版本历史写入规范与版本对比工具，确保框架演进全过程可审计。

本协议覆盖以下对象的版本管理：
- **协议文件**（protocols/*.md）
- **任务文件**（tasks/*.md）
- **能力卡**（knowledge/external-capabilities/*.md）
- **领域引擎**（knowledge/domains/*.md）
- **思维模型**（knowledge/thinking-models/*.md）
- **配置文件**（SKILL.md、persona/*.yaml、plugins/config.yaml）
- **脚本**（scripts/*.py）

## 2. 版本号规则（SubTask 5.6.1）

### 2.1 Semantic Versioning 适配

框架采用 Semantic Versioning 2.0.0 规范，版本号格式为 `MAJOR.MINOR.PATCH`：

```
v6.0.0
│ │ │
│ │ └── PATCH：向后兼容的 bug 修复、文档订正、小幅优化
│ └──── MINOR：向后兼容的功能新增、协议扩展、能力卡新增
└────── MAJOR：不向后兼容的破坏性变更、架构重构、协议重写
```

### 2.2 版本号递增规则

| 变更类型 | 递增规则 | 示例 |
|---------|---------|------|
| **小改（PATCH）** | PATCH + 1 | v6.0.0 → v6.0.1 |
| **中改（MINOR）** | MINOR + 1，PATCH 归零 | v6.0.1 → v6.1.0 |
| **大改（MAJOR）** | MAJOR + 1，MINOR 和 PATCH 归零 | v6.1.0 → v7.0.0 |

### 2.3 变更类型判定标准

#### PATCH（小改 +0.0.1）

- 修复 bug、拼写错误、格式问题
- 文档订正（如补充缺失的交叉引用）
- 小幅优化（如调整阈值数值、优化提示词措辞）
- 不改变协议接口、不新增字段、不删除字段

#### MINOR（中改 +0.1.0）

- 新增协议章节（如新增「测试用例」章节）
- 新增字段（如 feedback_item 中新增 user_confirmation 字段）
- 新增能力卡、新增领域引擎、新增思维模型
- 新增脚本工具
- 协议接口扩展但向后兼容（旧字段保留，新字段可选）

#### MAJOR（大改 +1.0.0）

- 删除字段或协议章节（破坏性变更）
- 修改字段语义（如将 tok 从硬性预算改为建议预算）
- 架构重构（如 Phase 编号重整、DAG 拓扑重构）
- 协议重写（如从 v2 到 v3 的协议版本升级）
- 移除 LEGACY 别名等不向后兼容的变更

### 2.4 协议版本号 vs 框架版本号

| 版本类型 | 格式 | 示例 | 作用域 |
|---------|------|------|--------|
| **框架版本号** | `vMAJOR.MINOR.PATCH` | v6.0.0 | 整个 Profound Cognition 框架 |
| **协议版本号** | `vMAJOR` | v3.0 | 单个协议文件（如 context-budget-protocol.md） |
| **能力卡版本号** | `vMAJOR.MINOR` | v1.2 | 单个能力卡 |

> **关键声明**：框架版本号与协议版本号独立演进。框架从 v6.0.0 升级到 v6.1.0 时，若仅新增协议章节而未破坏兼容性，协议版本号可保持 v3.0 不变。

### 2.5 预发布版本与构建元数据

支持 Semantic Versioning 的预发布版本与构建元数据标注：

```
v6.0.0-alpha.1     — 预发布版本（alpha 阶段第 1 次）
v6.0.0-beta.2      — 预发布版本（beta 阶段第 2 次）
v6.0.0-rc.1        — 发布候选（Release Candidate 第 1 次）
v6.0.0+20260625    — 构建元数据（构建日期）
v6.0.0-alpha.1+dev — 预发布 + 构建元数据
```

预发布版本优先级：`alpha < beta < rc < 正式版`。

## 3. Diff 报告格式（SubTask 5.6.2）

### 3.1 四类变更分类

每次版本变更必须生成 Diff 报告，将所有变更归类为四类：

| 变更类型 | 标识 | 定义 | 示例 |
|---------|------|------|------|
| **新增（added）** | `+` | 新增的文件、章节、字段 | 新增 comprehension-test-protocol.md |
| **修改（modified）** | `~` | 修改了内容但对象仍存在 | 修改 context-budget-protocol.md 的阈值 |
| **删除（removed）** | `-` | 删除的文件、章节、字段 | 删除 LEGACY 别名字段 |
| **未变（unchanged）** | `=` | 对象未发生变更 | self-evaluation-protocol.md 未修改 |

### 3.2 Diff 报告 YAML 格式

```yaml
version_diff_report:
  # 版本信息
  from_version: "v6.0.0"
  to_version: "v6.1.0"
  change_type: "MINOR"  # PATCH | MINOR | MAJOR
  release_date: "ISO8601"
  release_notes: "本次版本变更摘要（≤500字）"

  # 变更统计
  summary:
    total_files_changed: integer
    added: integer
    modified: integer
    removed: integer
    unchanged: integer

  # 详细变更清单
  changes:
    # 新增项
    added:
      - path: "protocols/comprehension-test-protocol.md"
        type: "file"
        description: "新增读者理解测试协议"
        related_requirement: "R8-04"
      - path: "protocols/context-budget-protocol.md#测试用例"
        type: "section"
        description: "新增测试用例章节（6 个测试用例）"
        related_requirement: "R10-01"

    # 修改项
    modified:
      - path: "protocols/context-budget-protocol.md"
        type: "file"
        description: "阈值收紧：80/120/150 → 60/80/95；新增 tiktoken 精确计数"
        related_requirement: "R10-01"
        change_details:
          - section: "§3.1 阈值定义"
            old: "GREEN<80%/YELLOW 80-120%/RED 120-150%/强制落盘>150%"
            new: "GREEN<60%/YELLOW 60-80%/RED 80-95%/强制落盘>95%"
            reason: "tiktoken 精确计数替代字符估算后，估算安全垫不再需要"
      - path: "protocols/user-feedback-protocol.md"
        type: "file"
        description: "新增反馈闭环验证章节"
        related_requirement: "R10-06"

    # 删除项
    removed:
      - path: "persona/persona-schema.yaml#LEGACY_aliases"
        type: "field"
        description: "移除 LEGACY 别名字段"
        reason: "v6.0 移除 LEGACY 别名，不向后兼容"
        migration: "使用语义化字段名替代（如 A_core_identity → identity）"

    # 未变项（仅列出关键未变文件，非全部列举）
    unchanged:
      - path: "protocols/self-evaluation-protocol.md"
        type: "file"
        description: "未修改"
      - path: "knowledge/thinking-models/general/first-principles.md"
        type: "file"
        description: "未修改"

  # 破坏性变更标注
  breaking_changes:
    - path: "persona/persona-schema.yaml"
      description: "移除 LEGACY 别名字段，不向后兼容"
      migration_guide: "将所有 LEGACY 字段名替换为语义化字段名"
      impact: "使用 LEGACY 字段名的脚本将报错"

  # 关联需求
  related_requirements:
    - "R8-04: 读者理解测试"
    - "R10-01: 上下文超载主动缓解"
    - "R10-06: 用户反馈闭环验证"

  # 审计信息
  audit:
    author: "变更作者"
    reviewer: "审核人"
    approved_by: "批准人"
    timestamp: "ISO8601"
```

### 3.3 Diff 报告生成时机

| 时机 | 触发条件 | 报告位置 |
|------|---------|---------|
| 版本发布时 | MAJOR/MINOR/PATCH 版本递增 | docs/version_history/v{VERSION}_diff.md |
| PR 合并时 | 每次合并到 main 分支 | docs/version_history/pr_{PR_ID}_diff.md |
| 手动触发 | 运行 version-diff-tool.py | docs/version_history/manual_{timestamp}_diff.md |

## 4. 版本历史目录（SubTask 5.6.3）

### 4.1 目录结构

```
docs/version_history/
├── README.md                          — 版本历史目录说明
├── v6.0.0_diff.md                     — v5.x → v6.0.0 的 Diff 报告
├── v6.0.0_changelog.md                — v6.0.0 的 Changelog
├── v6.1.0_diff.md                     — v6.0.x → v6.1.0 的 Diff 报告
├── v6.1.0_changelog.md                — v6.1.0 的 Changelog
├── v6.0.1_diff.md                     — v6.0.0 → v6.0.1 的 Diff 报告
├── v6.0.1_changelog.md                — v6.0.1 的 Changelog
└── ...
```

### 4.2 文件命名规范

| 文件类型 | 命名格式 | 示例 |
|---------|---------|------|
| Diff 报告 | `v{VERSION}_diff.md` | `v6.0.0_diff.md` |
| Changelog | `v{VERSION}_changelog.md` | `v6.0.0_changelog.md` |
| 预发布 Diff | `v{VERSION}_diff_{PRERELEASE}.md` | `v6.1.0_diff_alpha.1.md` |
| PR Diff | `pr_{PR_ID}_diff.md` | `pr_42_diff.md` |
| 手动 Diff | `manual_{timestamp}_diff.md` | `manual_20260625T143000_diff.md` |

### 4.3 Changelog 格式

每个版本对应一个 Changelog 文件，格式参考 Keep a Changelog 1.0.0：

```markdown
# Changelog — v6.1.0

> 发布日期：2026-06-25
> 变更类型：MINOR
> 上一版本：v6.0.0

## 新增（Added）
- 新增 protocols/comprehension-test-protocol.md（R8-04）
- 新增 protocols/version-management-protocol.md（R8-05/R10-05）
- 新增 protocols/cross-session-memory-protocol.md（R10-03/R9-08）
- 新增 knowledge/external-capabilities/Mem0.md 跨会话记忆能力卡（R10-03）
- 新增 docs/version_history/ 目录与 README.md
- 新增 scripts/version-diff-tool.py 版本对比工具
- context-budget-protocol.md 新增「测试用例」章节（6 个测试用例）
- user-feedback-protocol.md 新增「测试用例」章节（5 个测试用例）

## 修改（Changed）
- context-budget-protocol.md 阈值收紧：80/120/150 → 60/80/95（R10-01）
- context-budget-protocol.md 新增 tiktoken 精确 token 计数（R10-01）
- context-budget-protocol.md 新增 LLMLingua 压缩策略（R10-01）
- execution-protocol.md 新增「执行遥测」章节（R10-02）
- checkpoint-protocol.md 新增「跨会话检查点」章节（R10-03）
- user-feedback-protocol.md 新增「反馈闭环验证」章节（R10-06）

## 破坏性变更（Removed/Breaking）
- 无

## 关联需求
- R8-04: 读者理解测试
- R8-05: 版本管理系统
- R10-01: 上下文超载主动缓解
- R10-02: 执行遥测
- R10-03: 跨会话记忆系统
- R10-05: 版本管理
- R10-06: 用户反馈闭环验证
```

### 4.4 版本历史保留策略

- 所有正式版本（MAJOR/MINOR/PATCH）的 Diff 报告与 Changelog **永久保留**
- 预发布版本（alpha/beta/rc）的 Diff 报告在正式版发布后可归档至 `docs/version_history/archive/`
- PR Diff 在合并后保留 90 天，之后可归档
- 手动 Diff 保留 30 天，之后可删除

## 5. 版本对比工具（SubTask 5.6.4）

### 5.1 工具概述

`scripts/version-diff-tool.py` 是框架内置的版本对比工具，用于：

1. 对比两个 Git Tag（或两个提交）之间的文件变更
2. 自动生成 Diff 报告（YAML 格式）
3. 自动判定变更类型（PATCH/MINOR/MAJOR）
4. 将 Diff 报告写入 `docs/version_history/`

### 5.2 工具调用方式

```bash
# 对比两个 Git Tag
python scripts/version-diff-tool.py --from v6.0.0 --to v6.1.0

# 对比两个提交
python scripts/version-diff-tool.py --from commit_a --to commit_b

# 对比当前工作区与最新 Tag
python scripts/version-diff-tool.py --from latest --to working

# 指定输出文件
python scripts/version-diff-tool.py --from v6.0.0 --to v6.1.0 --output docs/version_history/v6.1.0_diff.md
```

### 5.3 工具实现

详见 `scripts/version-diff-tool.py`。

### 5.4 工具输出

工具输出包含：
1. **Diff 报告**（YAML 格式，写入 docs/version_history/）
2. **控制台摘要**（变更统计、变更类型判定、破坏性变更警告）
3. **退出码**：
   - 0：成功，无破坏性变更
   - 1：成功，但存在破坏性变更（需人工确认 MAJOR 版本递增）
   - 2：工具执行错误

### 5.5 CI 集成

版本对比工具集成到 CI 流程（.github/workflows/ci.yml）：

```yaml
- name: Version Diff Check
  run: |
    python scripts/version-diff-tool.py --from latest --to working
    # 若退出码为 1（破坏性变更），CI 标记为需要人工确认
    # 若退出码为 2（错误），CI 失败
```

## 6. 版本发布流程

```
1. 开发者完成代码变更
       ↓
2. 运行 version-diff-tool.py 生成 Diff 报告
       ↓
3. 工具自动判定变更类型（PATCH/MINOR/MAJOR）
       ↓
4. 人工确认变更类型
       ↓
5. 更新版本号（SKILL.md、README.md、CHANGELOG.md）
       ↓
6. 生成 Changelog 文件（docs/version_history/v{VERSION}_changelog.md）
       ↓
7. 提交 Git Tag（v{VERSION}）
       ↓
8. 推送至远程仓库
       ↓
9. 发布 Release（GitHub Release 附带 Diff 报告与 Changelog）
```

## 7. 与其他协议的关系

- **self-evaluation-protocol.md**：T19 交付守卫检查版本号一致性
- **execution-protocol.md**：执行遥测记录版本号
- **checkpoint-protocol.md**：检查点文件标注版本号
- **context-budget-protocol.md**：协议版本号纳入审计

## 8. 异常处理

| 异常场景 | 处理策略 |
|---------|---------|
| 版本号不一致（SKILL.md 与 README.md 不匹配） | 触发 version-consistency-check.py，CI 失败 |
| Diff 报告生成失败 | 持续重试直至成功，不跳过 Diff 报告生成 |
| 破坏性变更未标注 MAJOR | 工具警告，要求人工确认后才能合并 |
| 版本历史文件缺失 | 工具自动补全，标注"历史版本缺失，从当前版本开始记录" |

---

## 测试用例（R8-05/R10-05）

> **测试用例格式声明**：每个测试用例遵循「给定输入 X，应产出 Y」格式，覆盖版本管理的关键路径与边界条件。

### TC-1: PATCH 版本递增

**给定输入**：
- 当前版本：v6.0.0
- 变更内容：修复 context-budget-protocol.md 中的拼写错误（3 处）
- 无新增字段、无删除字段、无接口变更

**应产出**：
- version-diff-tool.py 判定变更类型为 `PATCH`
- 新版本号：v6.0.1
- Diff 报告：changes.modified 包含 context-budget-protocol.md，无 added/removed
- 无破坏性变更标注

### TC-2: MINOR 版本递增

**给定输入**：
- 当前版本：v6.0.0
- 变更内容：
  - 新增 protocols/comprehension-test-protocol.md
  - context-budget-protocol.md 新增「测试用例」章节
  - 无删除字段、无接口变更

**应产出**：
- version-diff-tool.py 判定变更类型为 `MINOR`
- 新版本号：v6.1.0
- Diff 报告：changes.added 包含 comprehension-test-protocol.md 和测试用例章节
- 无破坏性变更标注

### TC-3: MAJOR 版本递增（破坏性变更）

**给定输入**：
- 当前版本：v6.0.0
- 变更内容：
  - 删除 persona-schema.yaml 中的 LEGACY 别名字段
  - 修改 tok 字段语义（从硬性预算改为建议预算）
  - 新增 comprehension-test-protocol.md

**应产出**：
- version-diff-tool.py 判定变更类型为 `MAJOR`（因存在删除字段和语义变更）
- 新版本号：v7.0.0
- Diff 报告：breaking_changes 包含 LEGACY 别名删除和 tok 字段语义变更
- 退出码：1（破坏性变更，需人工确认）
- CI 标记为需要人工确认

### TC-4: Diff 报告生成

**给定输入**：
- 执行命令：`python scripts/version-diff-tool.py --from v6.0.0 --to v6.1.0`
- v6.0.0 到 v6.1.0 之间有 5 个文件变更：2 个新增、2 个修改、1 个删除

**应产出**：
- 生成 docs/version_history/v6.1.0_diff.md
- Diff 报告 YAML 包含：
  - summary: total_files_changed=5, added=2, modified=2, removed=1, unchanged=N
  - changes.added: 2 个文件
  - changes.modified: 2 个文件
  - changes.removed: 1 个文件
- 控制台输出变更摘要

### TC-5: 版本号一致性检查

**给定输入**：
- SKILL.md 中 version: "6.0.0"
- README.md 中 badge 显示 v6.0.1
- persona-init-protocol.md 中 version: "6.0.0"

**应产出**：
- version-consistency-check.py 检测到不一致
- CI 失败，错误信息："版本号不一致：SKILL.md=6.0.0, README.md=6.0.1, persona-init-protocol.md=6.0.0"
- 要求开发者统一版本号后才能合并
