# 用户自定义 DLP 库 (User DLP Library)

> **定位**: 用户自定义设计语言画像（DLP）的存储目录。此目录下的所有 `.md` 文件会被 DLP 检索器自动扫描并纳入检索候选池，与 16 个内置 DLP 平等参与打分排序。
> **配套文件**:
> - 模板: `output/dlp-templates/DLP-template.md`
> - 创建向导: `docs/dlp-creation-wizard.md`
> - 检索器: `rendering-pipeline/dlp-retriever.md` §十一
> - ASR 验证: `../../asr-rules.yaml`（项目根目录）
> **版本**: v1.0.0 (R6-04)

---

## 一、目录用途

本目录用于存储用户创建的自定义 DLP 文件，实现跨会话复用：

- **跨会话复用**: 用户在会话 A 中创建的自定义 DLP，在会话 B 中可被 DLP 检索器自动发现并使用
- **品牌一致性**: 企业用户可在此目录存储品牌 DLP，确保所有产出遵循品牌设计规范
- **场景扩展**: 当 16 个内置 DLP 无法覆盖特定场景时，用户可创建自定义 DLP 扩展覆盖范围

---

## 二、DLP 文件命名规范

```
DLP-{name}.md
```

- `name`: 小写连字符格式，如 `my-brand` / `tech-blog` / `academic-poster`
- 示例: `DLP-my-brand.md` / `DLP-tech-blog.md`

**命名约束**:
- 不得与 16 个内置 DLP 名称冲突（DLP-nature / DLP-science / DLP-ieee / DLP-springer / DLP-linear / DLP-aesop / DLP-stripe-press / DLP-gov-uk / DLP-economist / DLP-ted / DLP-newyorker / DLP-kami / DLP-economist-chart / DLP-scienceplots / DLP-nature-figure / DLP-plotivy）
- 不得包含空格或特殊字符（仅允许小写字母、数字、连字符）

---

## 三、DLP 文件格式

每个自定义 DLP 文件必须包含完整的 12 字段 YAML frontmatter，格式详见 `output/dlp-templates/DLP-template.md`。

最小示例：

```yaml
---
name: "DLP-my-brand"
anchor: "XX 公司 2024 年品牌设计"
family: "interface-brand"

color_palette:
  primary: "#1A56DB"
  secondary: "#E60012"
  accent: "#0066CC"
  neutral: "#6C757D"
  background: "#FAFAFA"
  text: "#1A1A1A"

typography_scale:
  h1: "32px/2rem"
  h2: "24px/1.5rem"
  h3: "20px/1.25rem"
  h4: "16px/1rem"
  body: "16px/1rem"
  caption: "12px/0.75rem"
  footnote: "10px/0.625rem"

font_stack:
  western: '"Source Serif 4", "STIX Two Text", serif'
  chinese: '"思源宋体", "Noto Serif SC", serif'
  monospace: '"JetBrains Mono", monospace'

font_weight_pairing:
  heading: "bold(700)"
  body: "regular(400)"
  emphasis: "italic(400)"

spacing_system:
  base: "4px"
  scale: "4/8/12/16/24/32px"

grid_system:
  columns: "12列"
  column_width: "N/A"
  gutter: "24px"
  margin: "32px"
  breakpoint: "768px/1024px/1280px"

radius_shadow:
  radius: "8px"
  shadow: "0 4px 12px rgba(0,0,0,0.1)"

motion_curve:
  easing: "cubic-bezier(0.25, 0.1, 0.25, 1.0)"
  duration: "300ms"

applicable_scenarios:
  - "品牌官网"
  - "企业文档"
  - "产品界面"
---
```

---

## 四、入库流程

```
Step 1: 复制模板
  cp output/dlp-templates/DLP-template.md rendering-pipeline/user-dlps/DLP-{name}.md

Step 2: 填写 12 字段
  按 DLP-template.md 的注释填写所有字段
  或使用 docs/dlp-creation-wizard.md 交互式向导引导填写

Step 3: ASR 验证
  按 DLP-template.md §三 验证清单逐项检查
  blocking 违规必须修正，warning 违规建议修正

Step 4: 入库
  验证通过后，文件即入库
  DLP 检索器在下次执行时自动扫描并纳入检索候选池
```

---

## 五、检索器集成

DLP 检索器（`rendering-pipeline/dlp-retriever.md`）在执行时会：

1. 扫描 `rendering-pipeline/user-dlps/` 目录下所有 `.md` 文件
2. 解析每个文件的 YAML frontmatter（12 字段）
3. 将自定义 DLP 纳入检索候选池（与 16 个内置 DLP 平等参与打分）
4. 按场景标签（`applicable_scenarios`）匹配度打分排序

详见 `dlp-retriever.md` §十一 自定义 DLP 检索。

---

## 六、DLP 清单

> 此处由用户手动维护已创建的自定义 DLP 清单（可选，检索器不依赖此清单）。

| DLP 名称 | 锚定实体 | 族 | 场景标签 | 创建时间 | ASR 验证状态 |
|---------|---------|-----|---------|---------|-------------|
| _（示例）DLP-my-brand_ | _XX 公司 2024 年品牌设计_ | _interface-brand_ | _品牌官网/企业文档_ | _2026-06-25_ | _PASS_ |

---

## 七、注意事项

1. **ASR 验证强制**: 所有自定义 DLP 必须通过 ASR 硬门验证（blocking 项全部 PASS）方可入库
2. **场景标签唯一性**: 自定义 DLP 的场景标签建议包含品牌特定关键词，避免与内置 DLP 完全重复
3. **文件大小**: 单个 DLP 文件建议 < 10KB（仅含 12 字段 YAML frontmatter + 简要说明）
4. **版本管理**: 建议使用 Git 管理本目录，追踪 DLP 的变更历史
5. **备份**: 重要 DLP 建议备份到外部存储，避免目录误删

---

> 知识来源: R6-04 DLP 自定义入口 / Visual DNA 审美进化项目
