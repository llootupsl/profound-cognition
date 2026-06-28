<!-- 作者：阿洋 -->

# 能力卡版本同步与替代关系规范 (Capability Version Sync & Replacement Governance)

> **状态**: 正式发布
> **适用范围**: Profound Cognition knowledge/external-capabilities/ 目录下所有能力卡文件
> **最后更新**: 2026-06-25
> **对应任务**: D7.4.4（版本同步机制）/ D7.4.5（替代关系声明）

---

## 1. 总则

### 1.1 目的

本规范定义 Profound Cognition 框架中所有能力卡（Capability Card）的版本同步机制与替代关系声明规则，确保：

- 能力卡与上游开源项目版本保持可追溯的同步关系
- 能力卡之间的替代/共存关系显式声明，避免隐式冲突
- 版本升级与替代变更可自动检测、可审计

### 1.2 适用范围

适用于 `knowledge/external-capabilities/` 目录下的所有 `.md` 能力卡文件（当前 121 个）。非能力卡文件（如 `last30days-skill-consumer.md`）不受本规范约束。

> **【A6.3-F1/F2 修复 / P1-1，Wave 5，2026-06-27】数字定义说明**：
>
> - **基础能力卡（Basic Capability Cards，125 张）**：`knowledge/external-capabilities/` 目录下的 `.md` 文件，含 TC-XXX（工具卡，105 张）/ MC-XXX（方法论卡，9 张）/ LC-XXX（渲染层卡，6 张）/ 具名卡（如 FActScore.md / MAPIE.md / SAFE.md / Mem0.md / PaperQA2.md，5 张）。受本规范全部约束。
> - **能力映射卡（Ability Mapping Cards，47 张）**：`output/ability-cards.md` 中的 AC-XX 表格行（AC-01~AC-47），用于人机交互界面渲染。不受本规范全部约束（仅需编号无重复且分类正确）。
> - **总能力卡数 = 125 + 47 = 172 张**。
> - **历史数字更正**：v6.0.0 发布时（2026-06-25）记为"93 张"，是 v5.x 旧值。v6.0.0 发布后能力卡扩展（新增 TC-091~TC-128 等），实际已增长至 121 张。Audit-6 报告原"121 张"误指基础卡数（实际 93+28 误算），更正为：基础卡 121 + 映射卡 47 = 168 张。
> - **【Audit-7 Stage 2 补建说明（2026-06-27）】**：新增 TC-129~TC-132 共 4 张占位卡（Reflexion / Semantic Scholar API / OpenAlex API / SciencePlots），对应 v5.1.0 报告推荐项（4.3.9 / 4.3.11 / 4.3.12 / 4.3.13）。基础卡 121→125，TC-XXX 工具卡 101→105，总卡 168→172。

### 1.3 术语

| 术语 | 定义 |
|------|------|
| **能力卡** | 描述外部工具/库/框架的能力、调用方式、失败回退、效果度量的 Markdown 文件 |
| **上游项目** | 能力卡所封装的开源项目/库/服务（如 LangGraph、FActScore、MAPIE 等） |
| **版本同步** | 能力卡字段与上游项目 release 版本保持对应关系 |
| **替代关系** | 一张能力卡替代另一张能力卡（全部或部分功能）的显式声明 |
| **共存关系** | 两张能力卡同时存在、互补使用的声明 |

---

## 2. 版本同步机制（D7.4.4）

### 2.1 同步字段规范

每张能力卡**必须**在「基本信息」或「版本同步」章节声明以下字段：

| 字段 | 必填 | 说明 | 示例 |
|------|------|------|------|
| `upstream_project` | 是 | 上游项目名称 | `LangGraph` |
| `upstream_repo` | 是 | 上游仓库 URL | `https://github.com/langchain-ai/langgraph` |
| `upstream_version` | 是 | 当前适配的上游版本 | `>=0.2.0` |
| `sync_frequency` | 否 | 同步检查频率（默认每季度） | `quarterly` |
| `last_sync_check` | 否 | 上次同步检查日期（ISO8601） | `2026-06-25` |

### 2.2 字段格式

#### 格式 A：基本信息内联（适用于简短声明）

```markdown
## 基本信息
- **卡片编号**: #11
- **类型**: TC
- **优先级**: P1
- **层级**: L1
- **版本同步**: 与官方 lightrag 库（https://github.com/HKUDS/LightRAG）同步，适配版本 >=0.1.0
```

#### 格式 B：独立「版本同步」章节（适用于详细声明）

```markdown
## 版本同步机制
- **同步对象**：LangGraph 官方版本（https://github.com/langchain-ai/langgraph）
- **同步频率**：每季度检查一次官方 release，评估是否升级
- **当前适配版本**：langgraph >= 0.2.0
- **兼容性策略**：本框架使用稳定 API（StateGraph、add_node、add_edge、compile、interrupt_before、checkpointer），避免使用实验性 API
- **升级评估**：升级前需运行 scripts/cycle-detection-check.py 与 scripts/exhaust-consistency-check.py 双重验证
- **上次同步检查**：2026-06-25
```

### 2.3 同步频率规则

| 能力卡优先级 | 同步频率 | 说明 |
|------------|---------|------|
| P0（核心编排） | 每月 | 如 LangGraph，影响全流程编排 |
| P1（关键工具） | 每季度 | 如 FActScore、SAFE、MAPIE、PaperQA2、LightRAG、Lean4 |
| P2（辅助工具） | 每半年 | 如可视化、格式转换工具 |
| P3（可选增强） | 每年 | 如实验性工具 |

### 2.4 升级评估流程

```
上游项目发布新版本
  │
  ├─→ 1. 评估新版本是否包含破坏性变更（Breaking Changes）
  │     ├─ 是 → 进入完整升级评估流程
  │     └─ 否 → 标记为「待跟进」，下次同步检查时处理
  │
  ├─→ 2. 完整升级评估流程：
  │     ├─ 2.1 阅读上游 CHANGELOG / Release Notes
  │     ├─ 2.2 检查本框架使用的 API 是否受影响
  │     ├─ 2.3 在测试环境验证新版本兼容性
  │     ├─ 2.4 运行相关检查脚本（见 §4.1）
  │     └─ 2.5 更新能力卡的 upstream_version 字段
  │
  ├─→ 3. 升级后验证：
  │     ├─ 3.1 运行 capability-binding-check.py
  │     ├─ 3.2 运行 exhaust-consistency-check.py
  │     └─ 3.3 在端到端测试中验证功能正常
  │
  └─→ 4. 记录变更：
        ├─ 4.1 在能力卡中更新 last_sync_check 日期
        ├─ 4.2 在 CHANGELOG.md 记录版本升级
        └─ 4.3 如有 API 变更，同步更新调用示例
```

### 2.5 版本号兼容性策略

| 兼容性类型 | SemVer 规则 | 本框架策略 |
|-----------|------------|----------|
| **补丁升级**（如 0.2.0 → 0.2.1） | 仅 bug 修复，无 API 变更 | 直接跟进，无需完整评估 |
| **次版本升级**（如 0.2.0 → 0.3.0） | 新增功能，向后兼容 | 运行检查脚本验证后跟进 |
| **主版本升级**（如 0.2.0 → 1.0.0） | 可能有破坏性变更 | 必须完整升级评估流程 |

---

## 3. 替代关系声明规范（D7.4.5）

### 3.1 声明要求

当一张能力卡替代另一张能力卡（全部或部分功能）时，**必须**在能力卡中声明「替代关系」章节。

### 3.2 声明格式

```markdown
## 替代关系声明
- **替代对象**：被本卡片替代的能力卡名称或文件名
- **替代范围**：全部功能 / 部分功能（需说明具体哪些功能）
- **不替代**：本卡片不替代的功能（需明确说明）
- **共存关系**：与本卡片互补使用的能力卡（如有）
- **迁移指引**：从被替代卡片迁移到本卡片的步骤（如适用）
```

### 3.3 替代类型

| 替代类型 | 说明 | 示例 |
|---------|------|------|
| **全部替代** | 新卡片完全替代旧卡片的功能 | LangGraph 替代 execution-protocol 的伪代码编排 |
| **部分替代** | 新卡片替代旧卡片的部分功能，旧卡片保留其余功能 | LightRAG 部分替代简单向量搜索 |
| **互补共存** | 两张卡片同时存在，功能互补 | FActScore + SAFE 互补使用 |
| **弃用标记** | 旧卡片被弃用，新卡片替代 | 旧版 API 客户端被新版替代 |

### 3.4 声明规范

#### 规则 1：显式声明

替代关系必须显式声明，不允许隐式替代（即新卡片功能覆盖旧卡片但未声明）。

#### 规则 2：双向标注

- **替代方**（新卡片）：声明「替代对象」字段
- **被替代方**（旧卡片）：声明「被替代」字段，指向新卡片

```markdown
# 新卡片（替代方）
## 替代关系声明
- **替代对象**：TC-OldTool
- **替代范围**：全部功能

# 旧卡片（被替代方）
## 替代关系声明
- **被替代**：TC-NewTool（自 v6.0.0 起）
- **弃用状态**：deprecated
- **迁移指引**：参见 TC-NewTool 的「调用指令」章节
```

#### 规则 3：共存关系声明

当两张能力卡互补使用时，双方均需声明共存关系：

```markdown
# 卡片 A
## 替代关系声明
- **共存关系**：与卡片 B 互补使用（A 负责 X，B 负责 Y）

# 卡片 B
## 替代关系声明
- **共存关系**：与卡片 A 互补使用（B 负责 Y，A 负责 X）
```

### 3.5 现有替代关系清单

截至 v6.0.0，已声明的替代/共存关系：

| 能力卡 | 关系类型 | 对象 | 说明 |
|--------|---------|------|------|
| TC-100-LangGraph | 全部替代 | execution-protocol.md 的 `find_ready_nodes()` 伪代码 | LangGraph StateGraph 替代手动拓扑排序 |
| TC-100-LangGraph | 共存 | checkpoint-protocol.md | LangGraph checkpoint（状态级）与 Phase 级检查点（业务语义级）互补 |
| TC-100-LangGraph | 共存 | cycle-detection-check.py | 编译期环检测与 LangGraph 运行期循环检测配合 |
| FActScore | 共存 | SAFE | FActScore 拆解原子事实，SAFE 搜索增强验证，二者融合使用 |
| TC-011-LightRAG | 部分替代 | 简单向量搜索 | LightRAG 图增强检索优于简单向量搜索，但回退时使用简单向量搜索 |

---

## 4. 自动检测

### 4.1 检查脚本

`scripts/capability-binding-check.py` 负责自动检测能力卡字段完整性：

- 扫描 `knowledge/external-capabilities/` 下所有 `.md` 文件
- 检查 D7.4.1（调用前置条件/prerequisites）字段覆盖
- 检查 D7.4.2（失败回退/fallback_strategy/穷尽重试策略）字段覆盖
- 检查 D7.4.3（效果度量/effect_metrics）字段覆盖
- 检查 consumer_nodes 引用的 DAG 节点是否存在
- 输出未绑定能力卡清单（WARNING）和无效绑定清单（ERROR）

### 4.2 CI 集成

`capability-binding-check.py` 已集成至 `.github/workflows/ci.yml`，每次 push 和 pull request 自动执行。

### 4.3 本地运行

```bash
python scripts/capability-binding-check.py
```

退出码：
- `0`：全部通过（未绑定卡为 WARNING，不阻塞）
- `1`：存在无效绑定（consumer_nodes 引用了不存在的 DAG 节点）

### 4.4 版本同步检查（手动）

版本同步检查为手动流程，建议每季度执行一次：

1. 遍历所有能力卡的 `upstream_version` 字段
2. 访问上游项目仓库，检查是否有新版本发布
3. 对有新版本的能力卡执行 §2.4 升级评估流程
4. 更新 `last_sync_check` 字段

---

## 5. 治理流程

### 5.1 新增能力卡

新增能力卡时，**必须**包含以下字段：

| 字段 | 对应任务 | 必填 |
|------|---------|------|
| 调用前置条件（prerequisites） | D7.4.1 | 是 |
| 失败回退策略（fallback_strategy/穷尽重试策略） | D7.4.2 | 是 |
| 效果度量（effect_metrics） | D7.4.3 | 是 |
| 版本同步（upstream_project/upstream_repo/upstream_version） | D7.4.4 | 是 |
| 替代关系声明（如有替代/共存关系） | D7.4.5 | 条件必填 |
| 消费节点（consumer_nodes） | D1.4.3 | 推荐（未绑定为 WARNING） |

### 5.2 版本升级流程

```
能力卡版本升级请求
  │
  ├─→ 1. 评估上游新版本（§2.4）
  ├─→ 2. 更新能力卡的 upstream_version 字段
  ├─→ 3. 更新调用示例（如 API 变更）
  ├─→ 4. 运行 capability-binding-check.py 验证
  ├─→ 5. 在 CHANGELOG.md 记录变更
  └─→ 6. CI 自动验证（push/PR 时触发）
```

### 5.3 替代关系变更流程

```
能力卡替代关系变更请求
  │
  ├─→ 1. 在新卡片添加「替代关系声明」章节
  ├─→ 2. 在旧卡片添加「被替代」声明（如适用）
  ├─→ 3. 更新消费节点的引用（如消费节点需切换到新卡片）
  ├─→ 4. 运行 capability-binding-check.py 验证
  ├─→ 5. 在 CHANGELOG.md 记录替代关系变更
  └─→ 6. CI 自动验证（push/PR 时触发）
```

---

## 6. 例外说明

以下能力卡**不受**本规范全部约束：

| 类型 | 说明 | 豁免内容 |
|------|------|---------|
| 内置工具卡 | 描述 Profound Cognition 自身内置工具的卡片 | 无需 upstream_repo 字段 |
| 概念卡 | 描述方法论/概念框架的卡片（如思维模型卡） | 无需 upstream_version 字段 |
| 已弃用卡 | 标记为 deprecated 的卡片 | 无需同步检查，但需保留替代关系声明 |

---

## 7. 附录

### 7.1 能力卡字段完整性检查清单

- [ ] 调用前置条件（D7.4.1）
- [ ] 失败回退策略（D7.4.2）
- [ ] 效果度量（D7.4.3）
- [ ] 版本同步字段（D7.4.4）
- [ ] 替代关系声明（D7.4.5，如有）
- [ ] 消费节点（D1.4.3）

### 7.2 相关文档

- `docs/protocol-version-governance.md`：协议版本治理规范
- `docs/protocol-dependency-graph.md`：协议依赖图
- `scripts/capability-binding-check.py`：能力卡绑定检查脚本
- `knowledge/external-capabilities/TC-100-LangGraph.md`：替代关系声明示例
- `knowledge/external-capabilities/FActScore.md`：版本同步示例
