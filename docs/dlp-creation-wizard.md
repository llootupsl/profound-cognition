<!-- 作者：阿洋 -->

# DLP 创建向导 (DLP Creation Wizard)

> **定位**: 交互式引导用户创建自定义 DLP（Design Language Profile）。通过 7 步问答引导用户填写 12 字段，最终生成可用的 DLP 文件。
> **配套文件**:
> - 模板文件: `output/dlp-templates/DLP-template.md`
> - 检索器扩展: `rendering-pipeline/dlp-retriever.md` §十一
> - ASR 验证: `../asr-rules.yaml`（项目根目录）
> - DLP 库: `rendering-pipeline/user-dlps/`
> **版本**: v1.0.0 (R6-04)

---

## 向导总览

```
Step 1: 基础信息（name / anchor / family）
  ↓
Step 2: 配色方案（color_palette 6 色板）
  ↓
Step 3: 字体方案（typography_scale + font_stack + font_weight_pairing）
  ↓
Step 4: 间距与栅格（spacing_system + grid_system）
  ↓
Step 5: 圆角阴影与动效（radius_shadow + motion_curve）
  ↓
Step 6: 场景标签（applicable_scenarios）
  ↓
Step 7: ASR 验证与入库
  ↓
输出: rendering-pipeline/user-dlps/DLP-{name}.md
```

---

## Step 1: 基础信息

### 1.1 询问 DLP 名称

```
Q1: 请为你的自定义 DLP 命名（小写连字符格式）：
  格式: DLP-{name}
  示例: DLP-my-brand / DLP-tech-blog / DLP-academic-poster
  约束: 名称唯一，不与 16 个内置 DLP 冲突
```

### 1.2 询问锚定实体

```
Q2: 这个 DLP 锚定哪个真实世界的设计实体？
  示例: "XX 公司 2024 年品牌设计" / "某杂志 2024 年版式" / "某产品 2024 年界面"
  约束: 必须锚定真实世界实体，不可凭空创造
  理由: DLP 的核心价值在于可追溯、可对标，锚定真实实体确保设计决策有据可依
```

### 1.3 询问族归属

```
Q3: 这个 DLP 属于哪个族？
  选项:
    1. academic-journal（学术期刊族 — 严谨、衬线、双栏）
    2. interface-brand（界面品牌族 — 现代、无衬线、单栏）
    3. publication-typesetting（出版物排版族 — 杂志、多栏、长文）
    4. data-visualization（数据可视化族 — 图表优先、克制配色）
    5. custom（自定义族 — 不属于以上任何族）
  推荐: 优先选择已有族，享受族内打分算法的检索优势
```

---

## Step 2: 配色方案（6 色板）

### 2.1 询问主色（primary）

```
Q4: 请提供主色（primary）的十六进制色值：
  用途: 标题、重点强调、链接
  约束:
    - 禁用 AI 紫 #7C3AED 系（ASR-COLOR-001 blocking）
    - 禁用 Tailwind 默认蓝 #3B82F6（ASR-COLOR-004 blocking）
    - 禁用纯黑 #000000 作为主色（ASR-COLOR-002 blocking）
  推荐: 学术蓝 #1A56DB / 暖调人文 #B45309 / 科技青 #06B6D4
  示例: #1A56DB
```

### 2.2 询问辅色（secondary）

```
Q5: 请提供辅色（secondary）的十六进制色值：
  用途: 次要强调、数据高亮
  约束: 与主色形成对比但不过于刺眼
  示例: #E60012（Nature 红）
```

### 2.3 询问强调色（accent）

```
Q6: 请提供强调色（accent）的十六进制色值：
  用途: 关键警示、CTA 按钮
  约束: 与主色/辅色形成视觉层级
  示例: #0066CC（链接蓝）
```

### 2.4 询问中性色（neutral）

```
Q7: 请提供中性色（neutral）的十六进制色值：
  用途: 次要文字、图注、脚注
  约束: 灰调须与背景色灰调一致（ASR-COLOR-006 warning）
  示例: #6C757D（冷灰）/ #78716C（暖灰）
```

### 2.5 询问背景色（background）

```
Q8: 请提供背景色（background）的十六进制色值：
  用途: 页面主背景
  约束:
    - 禁用纯黑 #000000（ASR-COLOR-002 blocking）
    - 禁用纯白 #FFFFFF 大面积（ASR-COLOR-003 warning）
  推荐: #FAFAFA（冷白）/ #FDFDFC（暖白）/ #0A0A0A（Off-Black 暗色）
```

### 2.6 询问文本色（text）

```
Q9: 请提供文本色（text）的十六进制色值：
  用途: 正文主文字色
  约束: 与背景色对比度 ≥ 4.5:1（WCAG AA 级）
  示例: #1A1A1A（近黑）/ #FAFAFA（暗色背景下的近白）
```

---

## Step 3: 字体方案

### 3.1 询问字号阶梯

```
Q10: 请提供字号阶梯（h1-h4 / body / caption / footnote）：
  格式: {px/rem} 或 {pt/px}
  示例:
    h1: "32px/2rem"
    h2: "24px/1.5rem"
    h3: "20px/1.25rem"
    h4: "16px/1rem"
    body: "16px/1rem"（行高 ≥ 1.5，ASR-TYPO-002 blocking）
    caption: "12px/0.75rem"
    footnote: "10px/0.625rem"
```

### 3.2 询问字体栈

```
Q11: 请提供西文字体栈（western）：
  约束:
    - 禁用 Inter 作为 Premium 字体（ASR-FONT-001 blocking）
    - 禁用 Roboto 作为品牌字体（ASR-FONT-002 blocking）
    - 禁用 Arial 作为正文字体（ASR-FONT-003 warning）
  推荐: Source Serif 4 / Fraunces / Geist / Satoshi / Cabinet Grotesk
  示例: '"Source Serif 4", "STIX Two Text", serif'

Q12: 请提供中文字体栈（chinese）：
  推荐: 思源宋体 / 思源黑体 / Noto Serif SC / Noto Sans SC
  示例: '"思源宋体", "Noto Serif SC", serif'

Q13: 请提供等宽字体栈（monospace）：
  推荐: JetBrains Mono / Cascadia Code / Geist Mono
  示例: '"JetBrains Mono", "Cascadia Code", monospace'

Q14: 确认字体族总数 ≤ 3 族（ASR-FONT-005 blocking）：
  当前字体族数: {western族 + chinese族 + monospace族 = N族}
  状态: {PASS|FAIL}
```

### 3.3 询问字重配对

```
Q15: 请提供字重配对：
  heading: "{标题字重}"（如 bold(700)）
  body: "{正文字重}"（如 regular(400)）
  emphasis: "{强调字重}"（如 italic(400)）
```

---

## Step 4: 间距与栅格

### 4.1 询问间距系统

```
Q16: 请提供间距基准单位（base）：
  推荐: 4px（4px 栅格系统，visual_dna 默认）
  示例: "4px"

Q17: 请提供间距阶梯（scale）：
  格式: {N1/N2/N3/.../Nn}px
  示例: "4/8/12/16/24/32px"
```

### 4.2 询问栅格系统

```
Q18: 请提供栅格列数（columns）：
  选项: 单栏 / 双栏 / 三栏 / 四栏 / 12列
  示例: "双栏"（学术）/ "12列"（Web）

Q19: 请提供列宽（column_width）：
  示例: "8.5cm/栏"（印刷）/ "N/A"（Web）

Q20: 请提供槽宽（gutter）：
  示例: "0.5cm"（印刷）/ "24px"（Web）

Q21: 请提供页边距（margin）：
  示例: "2cm"（印刷）/ "32px"（Web）

Q22: 请提供断点（breakpoint）：
  示例: "N/A(印刷媒介)" / "768px/1024px/1280px"
```

---

## Step 5: 圆角阴影与动效

### 5.1 询问圆角阴影

```
Q23: 请提供圆角（radius）：
  选项: "0px"（学术直角）/ "8px"（现代圆角）/ "16px"（大圆角）
  示例: "0px"

Q24: 请提供阴影（shadow）：
  选项: "none"（无阴影）/ "0 4px 12px rgba(0,0,0,0.1)"（轻阴影）
  约束: 阴影层数 ≤ 3 层（ASR-DECO-003 warning）
  示例: "none"
```

### 5.2 询问动效曲线

```
Q25: 请提供缓动函数（easing）：
  印刷媒介: "N/A(印刷媒介)"
  Web: "cubic-bezier(0.25, 0.1, 0.25, 1.0)"（标准 ease-out）
  约束: 禁用 linear 缓动（ASR-MOTION-002 warning）

Q26: 请提供动效时长（duration）：
  印刷媒介: "N/A"
  Web: "300ms"（推荐 200-400ms）
```

---

## Step 6: 场景标签

### 6.1 询问场景标签

```
Q27: 请提供场景标签（applicable_scenarios，3-6 个）：
  用途: DLP 检索器通过场景标签匹配内容语义信号
  示例:
    - "学术论文"
    - "期刊投稿"
    - "科学研究"
    - "同行评审"
  建议: 标签应覆盖该 DLP 适用的典型场景，便于检索器精准匹配
```

---

## Step 7: ASR 验证与入库

### 7.1 自动运行 ASR 验证

向导自动收集 Step 1-6 的所有回答，填充到 `DLP-template.md` 的 12 字段中，然后运行 ASR 硬门验证：

```
ASR 验证报告:
  blocking 违规数: {N}
  warning 警告数: {M}

  违规详情（如有）:
    [ASR-XXXX-NNN] {description}
      ├─ 违规代码: {具体值}
      ├─ 设计理由: {rationale}
      ├─ 严重等级: {blocking|warning}
      └─ 豁免条件: {override_condition}
```

### 7.2 入库决策

| 验证结果 | 决策 | 后续动作 |
|---------|------|---------|
| blocking = 0 且 warning = 0 | ✅ 入库 | 写入 `rendering-pipeline/user-dlps/DLP-{name}.md` |
| blocking = 0 且 warning > 0 | ⚠️ 入库（标记待优化） | 写入并标注 warning 项，建议后续优化 |
| blocking > 0 | ❌ 拒绝入库 | 返回违规清单，提示用户修正后重新提交 |

### 7.3 写入 DLP 库

```
入库路径: rendering-pipeline/user-dlps/DLP-{name}.md
入库时间: {ISO 8601 时间戳}
DLP 总数: user-dlps/ 目录下现有 {N} 个自定义 DLP
检索器状态: DLP 检索器将在下次执行时自动扫描并纳入新 DLP
```

---

## 向导输出示例

```yaml
dlp_creation_result:
  dlp_name: "DLP-my-brand"
  dlp_file: "rendering-pipeline/user-dlps/DLP-my-brand.md"
  family: "interface-brand"
  asr_validation:
    blocking_violations: 0
    warning_violations: 1
    warning_details:
      - rule: "ASR-COLOR-003"
        description: "背景色为纯白 #FFFFFF"
        suggestion: "建议替换为 #FAFAFA"
    validation_passed: true
 入库_status: "SUCCESS_WITH_WARNINGS"
  created_at: "2026-06-25T12:00:00+08:00"
```

---

## 常见问题

### Q: 自定义 DLP 会覆盖内置 DLP 吗？

A: 不会。自定义 DLP 与 16 个内置 DLP 平等参与检索器打分，按场景标签匹配度排序。自定义 DLP 不会替换内置 DLP，而是作为候选池的补充。

### Q: 自定义 DLP 如何被检索器发现？

A: DLP 检索器在执行时会扫描 `rendering-pipeline/user-dlps/` 目录下的所有 `.md` 文件，解析其 YAML frontmatter，纳入检索候选池。详见 `dlp-retriever.md` §十一。

### Q: 自定义 DLP 可以删除吗？

A: 可以。直接删除 `rendering-pipeline/user-dlps/DLP-{name}.md` 文件即可。检索器在下次执行时自动更新候选池。

### Q: 自定义 DLP 的场景标签如何与内置 DLP 区分？

A: 自定义 DLP 的场景标签建议包含品牌特定关键词（如"XX公司品牌"），避免与内置 DLP 的场景标签完全重复，确保检索器能精准匹配。

---

> 知识来源: R6-04 DLP 自定义入口 / Visual DNA 审美进化项目 / DLP 检索器规范
