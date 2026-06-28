# 版本历史目录

> **关联协议**：[version-management-protocol.md](../protocols/version-management-protocol.md)
> **关联工具**：[version-diff-tool.py](../scripts/version-diff-tool.py)

## 目录用途

本目录存放 Profound Cognition 框架所有版本的 Diff 报告与 Changelog，确保框架演进全过程可审计、可追溯。

## 文件命名规范

| 文件类型 | 命名格式 | 示例 |
|---------|---------|------|
| Diff 报告 | `v{VERSION}_diff.md` | `v6.0.0_diff.md` |
| Changelog | `v{VERSION}_changelog.md` | `v6.0.0_changelog.md` |
| 预发布 Diff | `v{VERSION}_diff_{PRERELEASE}.md` | `v6.1.0_diff_alpha.1.md` |
| PR Diff | `pr_{PR_ID}_diff.md` | `pr_42_diff.md` |
| 手动 Diff | `manual_{timestamp}_diff.md` | `manual_20260625T143000_diff.md` |

## Diff 报告格式

Diff 报告采用 YAML 格式，包含四类变更分类：

- **added（新增）**：新增的文件、章节、字段
- **modified（修改）**：修改了内容但对象仍存在
- **removed（删除）**：删除的文件、章节、字段
- **unchanged（未变）**：对象未发生变更

详细格式见 [version-management-protocol.md §3.2](../protocols/version-management-protocol.md#32-diff-报告-yaml-格式)。

## Changelog 格式

Changelog 采用 Keep a Changelog 1.0.0 规范，包含以下章节：

- **新增（Added）**：新增的功能
- **修改（Changed）**：修改的功能
- **破坏性变更（Removed/Breaking）**：不向后兼容的变更
- **关联需求**：本次版本关联的需求编号

## 版本号规则

框架采用 Semantic Versioning 2.0.0：

```
vMAJOR.MINOR.PATCH
│     │     │
│     │     └── PATCH：向后兼容的 bug 修复
│     └────── MINOR：向后兼容的功能新增
└──────────── MAJOR：不向后兼容的破坏性变更
```

详细规则见 [version-management-protocol.md §2](../protocols/version-management-protocol.md#2-版本号规则subtask-561)。

## 保留策略

- 正式版本（MAJOR/MINOR/PATCH）的 Diff 报告与 Changelog **永久保留**
- 预发布版本（alpha/beta/rc）的 Diff 报告在正式版发布后归档至 `archive/`
- PR Diff 在合并后保留 90 天，之后归档
- 手动 Diff 保留 30 天，之后可删除

## 工具使用

### 生成 Diff 报告

```bash
# 对比两个 Git Tag
python scripts/version-diff-tool.py --from v6.0.0 --to v6.1.0

# 对比两个提交
python scripts/version-diff-tool.py --from commit_a --to commit_b

# 对比当前工作区与最新 Tag
python scripts/version-diff-tool.py --from latest --to working
```

### 工具退出码

| 退出码 | 含义 |
|-------|------|
| 0 | 成功，无破坏性变更 |
| 1 | 成功，但存在破坏性变更（需人工确认 MAJOR 版本递增） |
| 2 | 工具执行错误 |

## 版本发布流程

1. 开发者完成代码变更
2. 运行 `version-diff-tool.py` 生成 Diff 报告
3. 工具自动判定变更类型（PATCH/MINOR/MAJOR）
4. 人工确认变更类型
5. 更新版本号（SKILL.md、README.md、CHANGELOG.md）
6. 生成 Changelog 文件（`docs/version_history/v{VERSION}_changelog.md`）
7. 提交 Git Tag（`v{VERSION}`）
8. 推送至远程仓库
9. 发布 Release（附带 Diff 报告与 Changelog）

## 当前版本

- **框架版本**：v6.0.0
- **协议版本**：v3.0
- **最新 Changelog**：见 [CHANGELOG.md](../../CHANGELOG.md)
