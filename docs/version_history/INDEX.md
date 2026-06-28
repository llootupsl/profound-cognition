<!-- 作者：阿洋 -->

# 版本历史索引（Version History Index）

> **用途**：汇总 Profound Cognition 框架所有已发布版本的 changelog 位置，便于审计与追溯。
> **关联协议**：[version-management-protocol.md](../protocols/version-management-protocol.md)
> **关联工具**：[version-diff-tool.py](../../scripts/version-diff-tool.py)
> **主 Changelog**：[../../CHANGELOG.md](../../CHANGELOG.md)
> **维护规则**：每次发布新版本时，必须更新本索引；v6.0.0 起新版本须同时生成本目录下独立 changelog 文件。

---

## 1. 版本清单

> 共 14 个已发布版本（v1.0 → v6.0.0）。早期版本（v1.0 ~ v5.2.0）的 changelog 统一记录在主 CHANGELOG.md 中；v6.0.0 起新版本须同时生成本目录下独立 changelog 文件。

| 版本 | 发布日期 | 类型 | Changelog 位置 | 备注 |
|------|---------|------|---------------|------|
| v1.0 | 2025 | MAJOR | CHANGELOG.md §[v1.0] | 初始版本（推测性回溯） |
| v2.0 | 2025 | MAJOR | CHANGELOG.md §[v2.0] | 框架扩展（推测性回溯） |
| v3.0 | 2026 | MAJOR | CHANGELOG.md §[v3.0] | 深度思考升级方案落地（推测性回溯） |
| v3.1 | 2026 | MINOR | CHANGELOG.md §[v3.1] | EXHAUST 一致性强化 |
| v4.0 | 2026-06-17 | MAJOR | CHANGELOG.md §[v4.0] | 鲁班打磨 v5 |
| v4.1 | 2026-06-17 | MINOR | CHANGELOG.md §[v4.1] | 鲁班打磨 v5 续 |
| v4.1.1 | 2026-06-17 | PATCH | CHANGELOG.md §[v4.1.1] | 鲁班慢刨方案A：补地基 |
| v4.1.2 | 2026-06-17 | PATCH | CHANGELOG.md §[v4.1.2] | 鲁班慢刨方案B：精雕 |
| v4.1.3 | 2026-06-17 | PATCH | CHANGELOG.md §[v4.1.3] | 真实运行产物反思 |
| v4.1.4 | 2026-06-17 | PATCH | CHANGELOG.md §[v4.1.4] | 深度反思第二轮 |
| v4.1.5 | 2026-06-17 | PATCH | CHANGELOG.md §[v4.1.5] | 深度反思第三轮 |
| v4.1.6 | 2026-06-17 | PATCH | CHANGELOG.md §[v4.1.6] | 全面修复 |
| v5.0.0 | 2026-06-19 | MAJOR | CHANGELOG.md §[v5.0.0] | Visual DNA 审美进化 |
| v5.1.0 | 2026-06-20 | MINOR | CHANGELOG.md §[v5.1.0] | 十五维度深度审计（60 项） |
| v5.2.0 | 2026-06-21 | MINOR | CHANGELOG.md §[v5.2.0] | 十轮迭代改进（50 项） |
| v6.0.0 | 2026-06-25 | MAJOR | ./v6.0.0_changelog.md | 终极升级（合并 v5.1.0 + v5.2.0 两份审计，110+ 项改进） |

---

## 2. 文件命名规范

| 文件类型 | 命名格式 | 示例 | 适用版本 |
|---------|---------|------|---------|
| 独立 Changelog | `v{VERSION}_changelog.md` | `v6.0.0_changelog.md` | v6.0.0+ |
| Diff 报告 | `v{VERSION}_diff.md` | `v6.0.0_diff.md` | v6.0.0+（待生成） |
| 预发布 Diff | `v{VERSION}_diff_{PRERELEASE}.md` | `v6.1.0_diff_alpha.1.md` | 预发布版本 |
| PR Diff | `pr_{PR_ID}_diff.md` | `pr_42_diff.md` | PR 合并 |
| 手动 Diff | `manual_{timestamp}_diff.md` | `manual_20260625T143000_diff.md` | 临时对比 |

> 早期版本（v1.0 ~ v5.2.0）的 changelog 仅在主 CHANGELOG.md 中记录，不强制生成独立文件。v6.0.0 起新版本必须同时生成本目录下独立 changelog 文件，并在本索引中登记。

---

## 3. 版本演进脉络

```
v1.0 (初始版本, 2025)
  └─ v2.0 (框架扩展, 2025)
       └─ v3.0 (深度思考升级, 2026)
            └─ v3.1 (EXHAUST 一致性, 2026)
                 └─ v4.0 (鲁班打磨 v5, 2026-06-17)
                      └─ v4.1 ~ v4.1.6 (6 次 PATCH 修复, 2026-06-17)
                           └─ v5.0.0 (Visual DNA 审美进化, 2026-06-19)
                                └─ v5.1.0 (十五维度审计, 2026-06-20)
                                     └─ v5.2.0 (十轮迭代改进, 2026-06-21)
                                          └─ v6.0.0 (终极升级, 2026-06-25)
                                               └─ v6.0.1 (Audit-6 修复, 待发布)
```

---

## 4. 当前版本

- **框架版本**：v6.0.0（2026-06-25 发布）
- **协议版本**：v3.0
- **下一计划版本**：v6.0.1（Audit-6 超深度审计与修复）
- **最新 Changelog**：
  - v6.0.0 → [./v6.0.0_changelog.md](./v6.0.0_changelog.md)
  - v6.0.0 之前 → [../../CHANGELOG.md](../../CHANGELOG.md)

---

## 5. 审计追溯

每次 MAJOR/MINOR 版本发布须由独立审计员确认 changelog 完整性。本索引文件由版本管理员维护，更新时同步在主 CHANGELOG.md 中记录。

| 审计项 | 验证内容 | 状态 |
|--------|---------|------|
| H8（Audit-6 Wave 1） | version_history/ 补录历史版本索引 | ✅ 已修复（2026-06-26） |
| R8-05/R10-05 | 版本管理系统完整性 | ✅ 已实现（协议 + 工具 + 索引 + v6.0.0 changelog） |

---

© 阿洋
