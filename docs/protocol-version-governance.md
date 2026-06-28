<!-- 作者：阿洋 -->

# 协议版本治理规范 (Protocol Version Governance)

> **状态**: 正式发布
> **适用范围**: Profound Cognition protocols/ 目录下所有协议文件
> **最后更新**: 2026-06-25

---

## 1. 总则

### 1.1 目的

本规范定义 Profound Cognition 框架中所有协议文件的版本号治理规则，确保协议版本号全局一致、可追溯、可自动检测。

### 1.2 适用范围

适用于 `protocols/` 目录下的所有 `.md` 协议文件（当前 16 个）。`persona/persona-init-protocol.md` 等非 protocols/ 目录下的协议文件参考本规范执行。

---

## 2. 版本号规则

### 2.1 统一版本号

所有协议文件的版本号统一为 **v3.0**。

- YAML 代码块中的 `version:` 字段值必须为 `"3.0"`
- 文件标题中的协议版本标记必须为 `v3.0`
- 不允许出现 `"9"`、`"2"`、`"1.0"`、`"2.0"` 等非 `"3.0"` 的版本号

### 2.2 版本号格式

| 位置 | 格式 | 示例 |
|------|------|------|
| YAML `version:` 字段 | `"3.0"` | `version: "3.0"` |
| 文件标题 | `v3.0` | `# 检查点协议 (Checkpoint Protocol) v3.0` |

### 2.3 版本号变更规则

- 协议版本号变更时，**必须同步更新所有协议文件**中的版本号
- 不允许部分文件更新而其他文件滞后
- 版本号变更需在 `CHANGELOG.md` 中记录

---

## 3. 新增协议要求

新增协议文件时，**必须声明版本号**：

1. 文件标题中包含 `v3.0` 标记
2. YAML 代码块中的 `version:` 字段值为 `"3.0"`
3. 不声明版本号的协议文件视为不合规

---

## 4. 自动检测

### 4.1 检测脚本

`scripts/protocol-version-check.py` 负责自动检测协议版本号一致性：

- 扫描 `protocols/` 下所有 `.md` 文件的版本号
- 检查是否全部为 `v3.0`（YAML `version:` 字段为 `"3.0"`）
- 发现不一致时退出码 1 并打印差异

### 4.2 CI 集成

`protocol-version-check.py` 已集成至 `.github/workflows/ci.yml`，每次 push 和 pull request 自动执行。

### 4.3 本地运行

```bash
python scripts/protocol-version-check.py
```

退出码：
- `0`：全部一致
- `1`：存在不一致
- `2`：脚本执行错误

---

## 5. 例外说明

以下版本号**不受**本规范约束：

| 类型 | 说明 | 示例 |
|------|------|------|
| 框架版本引用 | 引用 Profound Cognition 框架版本（非协议版本） | `Profound Cognition v2` |
| 引擎版本 | 领域引擎的版本号 | `engine_version: "1.0"` |
| 变更日志版本 | CHANGELOG 中的历史版本记录 | `v2.0 | 2026-05-15 | 初始发布` |
| 子模块版本 | 协议内嵌套的子模块版本（如有明确语义） | `protocol_version:` 字段值 |

> 注：v6.0.0 Stage 0 已将所有 `version: "9"`、`version: "2"`、`version: "1.0"`、`version: "2.0"` 统一为 `version: "3.0"`。

---

## 6. 治理流程

```
协议版本号变更请求
  │
  ├─→ 1. 更新所有 protocols/*.md 的 version 字段
  ├─→ 2. 更新本治理文档的统一版本号
  ├─→ 3. 在 CHANGELOG.md 记录变更
  ├─→ 4. 运行 protocol-version-check.py 验证
  └─→ 5. CI 自动验证（push/PR 时触发）
```
