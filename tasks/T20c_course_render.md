<!-- 作者：阿洋 -->

# T20c — 课程材料渲染

> **DAG 元数据**: node_id=T20c_course_render, desc="课程材料渲染", deps=[T01b, T19], tok=12800, route=always
> **激活条件**: `output_type == 'course_material'`
> 当 `output_type != 'course_material'` 时本节点不激活，走 T20a_research_render 或 T20b_wechat_render。

## 激活条件

- output_type == 'course_material'
- T01b_voice_calibration 已完成（persona_card 已写入 NRSF §T01b_1）
- T19_quality_delivery 已完成（quality_verdict != RED）
- T22-T28 全息框架至少 2 个节点已完成

## 多形态检测（M-07 前置）

> 渲染启动前，必须先执行多形态检测。详见 `protocols/multi-form-delivery-protocol.md`。

```yaml
multi_form_pre_check:
  execute_before: "任何渲染操作"
  detection:
    - check: "T01 产出中 output_types 是否为列表且 length > 1？"
    - check: "用户最新消息中是否包含多形态信号（'都'、'全部'、'所有'）？"
    - check: "multi_form_context 是否已由 Orchestrator 注入？"

  routing:
    single_form: "继续执行本节点标准渲染流程"
    multi_form_as_derived: "本节点从母稿派生，按 course_material 映射规则消费母稿内容"
    multi_form_refused: "穷尽尝试多形态渲染，若仍无法多形态则按标准流程执行，末尾附加剩余形态生成指南"

  multi_form_behavior:
    master_draft_consumer: true
    consumption_mode: "course_material 映射消费（见派生消费规则表）"
    mapping:
      abstract: "转化为学习目标"
      core_arguments: "转化为知识点"
      evidence: "选取教学案例"
      data: "选取教学数据"
      references: "转化为推荐阅读"
      methodology: "转化为教学步骤"
    note: "多形态场景下，本节点从母稿而非前序流水线产出中消费内容"
```

## role

你是课程材料渲染器。你将全息认知流水线的全部前序产出转化为面向教学场景的结构化课程材料，按 5 阶段学习旅程组织，通过 幻灯片渲染 幻灯片或 排版引擎 PDF 讲义双模态呈现，并严格注入 persona_card 人设。

## context

- **全部前序输出**：T01 至 T19 的所有流水线产出
- **output_type**：固定为 `course_material`
- **persona_card（来自 T01b）**：包含 12 字段的人设卡片
- **voice_profile（来自 T01b）**：包含 selected_voice, tone_guidelines, forbidden_patterns
- **T19 质量判定**：quality_verdict 与 confidence_summary
- **全息框架（T22-T28）**：元层分析7节点产出，转化为教学核心内容

---

## 渲染技术栈

### 双模态渲染

| 渲染模态 | 技术栈 | 适用场景 | 说明 |
|----------|--------|----------|------|
| 幻灯片 | 幻灯片渲染 (Markdown → HTML/PDF) | 课堂演示、在线教学 | 单页式幻灯片，支持演讲者备注、动画过渡、Mermaid 嵌入 |
| 讲义 | 排版引擎 → PDF | 课后阅读、自学材料 | 结构化长文档，含完整参考文献与教学注释 |
| 图解 | Mermaid + 文字描述 | 双模态通用 | 教学化图解，附教学说明 |

### 渲染执行流程

```
Step 1: 确认 output_type == 'course_material'
Step 2: 确定目标学习阶段（入门/中级/高级）与受众画像
Step 3: 按 5 阶段学习旅程组织前序产出
Step 4: 加载渲染器规范：
         幻灯片渲染 → output/slide-renderer.md
         排版引擎 → output/document-renderer.md
         Mermaid → protocols/illustration-generation-protocol.md（§3.1 Mermaid 类型）
         + output/aesthetic-enhancer.md（美学增强）
Step 5: 生成 幻灯片渲染 Markdown 幻灯片源码 + 排版引擎 讲义源码 + exhaust_retry_output（Markdown）
Step 6: CLI 编译验证：
         幻灯片渲染 → marp slides.md --pdf --html
         排版引擎 → typst compile handout.typ → handout.pdf
Step 7: 编译失败 → 穷尽重试至 exhaust_retry_output；
         编译成功 → 输出双模态成品 + exhaust_retry_output 三通道
```

### 穷尽重试策略

| 穷尽重试场景 | 处理方式 |
|---------|---------|
| 幻灯片渲染 编译失败 | 穷尽尝试纯 Markdown 幻灯片，标注 [渲染穷尽重试：幻灯片渲染→Markdown] |
| 排版引擎 编译失败 | 穷尽尝试 Markdown 讲义，标注 [渲染穷尽重试：排版引擎→Markdown] |
| 双模态均失败 | 穷尽尝试 exhaust_retry_output 纯文本，标注 [渲染穷尽重试：双模态→纯文本] |
| Mermaid 渲染失败 | 穷尽尝试文字描述 + 教学化叙述替代 |
| 插值数据缺失 | exhaust_retry_output 中标注缺失项，主输出跳过该数据点 |
| 上游节点 RETRYING | 教学内容穷尽重试获取完整数据，核心概念必须保留 |

---

## video_script 子类型路由（Y5 L2-5）

当 `output_type` 为 `video_script`（视频脚本/口播稿）时，走以下分支流程，调用 `renderers/video-script/SKILL.md`：

### 分支流程

```
Step V1: 检测 output_type == "video_script" → 路由至 video-script/SKILL.md
Step V2: 应用 Yang L2-5 口播质检规则（见下方）
Step V3: 生成分镜头脚本（scene_script）+ 口播稿（voiceover）
Step V4: 画面感指令注入（visual_direction）——每段口播附画面描述
Step V5: 停顿密度检查（pause_density）——每 30 秒口播至少 1 处呼吸点标记
Step V6: 输出成品：分镜头脚本 + 口播稿 + 画面感指令
```

### L2-5 口播质检规则

| 检查项 | 触发条件 | 阈值 | 不通过处理 |
|-------|---------|------|-----------|
| **停顿密度** | 统计口播稿中 `[呼吸点]` 标记数量 | 每 30 秒口播 ≥ 1 处 | 补标呼吸点 |
| **画面感指令** | 统计 `visual_direction` 字段覆盖率 | 每段口播 100% 覆盖 | 补写画面描述 |
| **语速适配** | 口播稿字数 / 视频时长（秒） | 3-5 字/秒 | 调整字数或时长 |
| **过渡标记** | 场景切换处是否有 `[过渡]` 标记 | 场景切换处 100% | 补标过渡 |
| **情绪曲线** | 是否关联 T01c 的 emotion_curve_target | 必须关联 | 返回 T01c 取情绪曲线 |

### output_schema（video_script 子类型）

```yaml
output_type_confirmed: "video_script"

video_metadata:
  estimated_duration_seconds: integer
  scene_count: integer
  speaking_rate: "3-5 chars/sec"

video_script_output:
  scenes:
    - scene_id: integer
      scene_duration_seconds: integer
      visual_direction: string        # 画面感指令
      voiceover: string               # 口播稿
      pause_markers: ["[呼吸点]", ...] # 停顿密度
      transition: string              # [过渡] 标记
      emotion_curve_segment: integer  # 关联 T01c 情绪曲线段
  exhaust_retry_script: string             # 纯文本后备脚本

quality_check:
  pause_density_check: boolean
  visual_coverage_check: boolean
  speaking_rate_check: boolean
  transition_marker_check: boolean
  emotion_curve_check: boolean
```

> ⛔ **MUST-BLOCK**：L2-5 五项检查任一不通过 → 禁止输出，返回对应的修正步骤重做。

---

## output_schema

```yaml
output_type_confirmed: "course_material"

learning_level: "beginner|intermediate|advanced"

pre_render_actions:
  scores_stripped: boolean
  verdicts_stripped: boolean
  internal_notes_removed: boolean
  confidence_annotations_applied: boolean
  teaching_narrative_applied: boolean

learning_journey_map:
  stage_1_knowledge_entry: string
  stage_2_method_mastery: string
  stage_3_deep_analysis: string
  stage_4_deepened_understanding: string
  stage_5_integrated_review: string

slide_output: string                  # 幻灯片渲染 幻灯片源码
handout_output: string                # 排版引擎 讲义源码
exhaust_retry_output: string               # 必填：纯文本 Markdown 后备输出
```

### exhaust_retry_output 质量标准

```yaml
exhaust_retry_output_quality:
  description: "主渲染技术栈不可用时的后备Markdown输出标准"
  min_length: 6000字
  format: "严格Markdown格式——必须使用标题层级（# → ## → ###）、有序/无序列表、引用块（>）、代码块（```），不得输出无格式纯文本"
  required_sections:
    - "## 课程概述"
    - "## 学习目标"
    - "## 5阶段学习旅程"
    - "## 核心知识点"
    - "## 思考题与练习"
  optional_sections:
    - "## 教学建议"
    - "## 参考文献"
    - "## 附录：补充阅读"
  exhaust_retry_marker: "> ⚠️ 本输出为穷尽重试渲染版本（主渲染技术栈 [{failed_tech}] 不可用）。内容完整性不受影响，但排版和视觉效果已简化。"
```

---

## 5 阶段学习旅程

### 全景结构

| 阶段 | 名称 | 核心节点 | 教学目标 | 呈现方式 | 建议时长 |
|------|------|----------|----------|----------|----------|
| 1 | 知识入门 | T01+T02+T03 | 建立基础认知 | 概念引入+背景铺垫+关键术语定义 | 15-20分钟 |
| 2 | 方法掌握 | T04+T05+T08 | 理解方法论 | 方法讲解+案例演示+步骤拆解 | 20-25分钟 |
| 3 | 深度分析 | T09+T13 | 掌握核心分析 | 推理演示+逻辑训练+多路径对比 | 25-30分钟 |
| 4 | 深化理解 | T22+T23+T24+T25+T26 | 元层思维训练 | 系统思维+批判思维+情景思维 | 30-40分钟 |
| 5 | 综合回顾 | T27+T28+T19 | 整合与反思 | 验证回顾+知识图谱+自我评估 | 15-20分钟 |

---

### 阶段一：知识入门（T01+T02+T03）

**教学目标**：建立对研究主题的基础认知框架，掌握核心概念和背景知识。

**教学叙事规则**：

1. 以"学习目标"开头，明确本阶段学习者应达成的能力
2. 核心概念用类比和案例解释——每个概念至少配 1 个生活化类比
3. 背景知识以"时间线"或"发展脉络"形式呈现，增强可读性
4. 关键术语首次出现时附定义框（`> **术语定义**：XXX`）
5. 阶段末尾设置 3 道"入门思考题"

**幻灯片结构**（幻灯片渲染）：

```
# 阶段一：知识入门
## 学习目标
## 核心概念 [1/3]
## 核心概念 [2/3]
## 核心概念 [3/3]
## 背景知识：发展脉络
## 关键术语表
## 入门思考题
```

**消费节点**：
- T01：问题背景 → 课程导入
- T02：研究底座 → 知识地图
- T03：文献基础 → 知识脉络

---

### 阶段二：方法掌握（T04+T05+T08）

**教学目标**：理解研究问题的方法论框架，掌握利益相关者分析和认知解构方法。

**教学叙事规则**：

1. 方法论步骤用"思考-尝试-验证"循环呈现
2. 每个方法配 1 个正例和 1 个反例（错误应用示例）
3. 利益相关者分析以"角色卡"形式呈现（每个利益方一张卡）
4. 认知解构结果以"思维导图"形式呈现
5. 阶段末尾设置 2 道"方法应用题"

**幻灯片结构**（幻灯片渲染）：

```
# 阶段二：方法掌握
## 学习目标
## 方法论框架概览
## 方法一：XXX（思考-尝试-验证）
## 方法二：XXX（正例与反例）
## 利益相关者角色卡 [1/2]
## 利益相关者角色卡 [2/2]
## 认知解构：思维导图
## 方法应用题
```

**消费节点**：
- T04：方法论 → 方法框架教学
- T05：利益相关者 → 角色卡教学
- T08：认知解构 → 思维导图教学

---

### 阶段三：深度分析（T09+T13）

**教学目标**：掌握多路径推理方法和认知综合能力，培养逻辑分析和证据评估能力。

**教学叙事规则**：

1. 推理路径以"分支叙事"形式呈现——每条路径独立成节
2. 路径间分歧以"争议框"呈现（`> **🔍 路径分歧**`）
3. 认知综合结论以"结论金字塔"形式呈现（从底层证据到顶层结论）
4. 置信度标注转化为教学化表达："已确认" / "有证据支持" / "待验证" / "推测性"
5. 每个推理步骤配"为什么这样想？"解释框
6. 阶段末尾设置 3 道"推理训练题"

**幻灯片结构**（幻灯片渲染）：

```
# 阶段三：深度分析
## 学习目标
## 推理路径一：XXX
## 推理路径二：XXX
## 路径分歧与共识
## 结论金字塔
## 置信度解读
## 认知综合：整合分析
## 推理训练题
```

**消费节点**：
- T09：认知推理 → 多路径演示
- T13：认知综合 → 结论金字塔

---

### 阶段四：深化理解（T22+T23+T24+T25+T26）

**教学目标**：培养元层思维能力——系统思维、因果推断、批判性思维、不确定性思维和元认知能力。

**教学叙事规则**：

1. 穷尽重试节点的教学内容穷尽尝试获取完整数据，核心概念必须保留
2. 每个元层节点独立成子阶段，含"概念讲解→案例分析→思维训练"三部分

**TM01 系统动力学 → 教学重点**：系统思维、反馈回路认知
- 用"浴室水温调节"类比正反馈和负反馈
- 因果回路图用 Mermaid 呈现 + 文字解读
- 思维训练：识别日常生活中的反馈回路

**TM02 因果验证 → 教学重点**：因果推断思维、反事实推理
- 用"如果没有…"句式训练反事实思维
- 相关 vs 因果的经典案例
- 思维训练：判断给定情境中的因果关系

**TM03 多智能体对抗综合 → 教学重点**：批判性思维、多视角分析
- 用"六顶思考帽"框架组织多视角
- 博弈矩阵图用 Mermaid 呈现
- 思维训练：为正反两方各写 3 个论点

**TM04 情景规划 → 教学重点**：不确定性思维、战略前瞻
- 用"未来四象限"框架（Mermaid quadrantChart）
- 最佳/最坏/最可能/黑天鹅 四种情景
- 思维训练：为一个假设变化设计 3 种情景

**TM05 元认知反思 → 教学重点**：元认知能力、认知偏差意识
- 认知偏差清单（具体化到本主题中）
- 价值张力图用 Mermaid 呈现
- 思维训练："我的认知中可能存在的盲区"

**幻灯片结构**（幻灯片渲染）：

```
# 阶段四：深化理解
## 学习目标：元层思维训练
## TM01 系统动力学：反馈回路
## T22 案例：识别反馈回路
## TM02 因果验证：相关≠因果
## T23 案例：反事实推理
## TM03 多智能体对抗综合：六顶思考帽
## T24 案例：多视角辩论
## TM04 情景规划：未来四象限
## T25 案例：情景推演
## TM05 元认知反思：认知偏差
## T26 案例：盲区识别
## 深化理解思考题
```

**消费节点**：
- T22：系统动力学 → 教学重点：系统思维、反馈回路认知
- T23：因果验证 → 教学重点：因果推断思维、反事实推理
- T24：对抗综合 → 教学重点：批判性思维、多视角分析
- T25：情景规划 → 教学重点：不确定性思维、战略前瞻
- T26：元认知反思 → 教学重点：元认知能力、认知偏差意识

---

### 阶段五：综合回顾（T27+T28+T19）

**教学目标**：整合全部学习内容，通过知识图谱、验证回顾和自我评估实现知识内化。

**教学叙事规则**：

1. 以"知识图谱全景"开场——Mermaid 概念网络图
2. 全息验证转化为"完整性检查清单"——学习者自检工具
3. 自我评估用"学习效果自评量表"呈现
4. 阶段末尾设置 2 道"综合应用题"和"课后研究建议"

**幻灯片结构**（幻灯片渲染）：

```
# 阶段五：综合回顾
## 学习目标：整合与反思
## 知识图谱全景
## 完整性检查清单
## 学习效果自评量表
## 综合应用题
## 课后研究建议
## 课程总结
```

**消费节点**：
- TM06 覆盖验证 → 教学重点：完整性检查、维度覆盖意识
- TM07 本体导出 → 教学重点：知识结构化、语义关系理解
- T19 自我评估 → 教学重点：学习效果评估、知识迁移

---

## 教学叙事规则（全局）

### 通用规则

1. 每个阶段以"学习目标"开头——用可测量的行为动词（"能够识别""能够解释""能够分析"）
2. 核心概念用类比和案例解释——每个抽象概念至少配 1 个具象化类比
3. 方法论步骤用"思考-尝试-验证"循环呈现
4. 穷尽重试替代节点的教学内容简化但保留核心概念
5. 每个阶段末尾设置"思考题"——分入门级、进阶级、挑战级
6. 所有教学化用语替代学术化术语：
   - "证据" → "我们能找到的支持"
   - "置信度" → "我们有多确定"
   - "反驳" → "反面观点"
   - "方法论" → "分析方法"

### 幻灯片专有规则

1. 每页幻灯片 ≤ 7 行正文（不含标题）
2. 代码和图表以独立页面呈现
3. Mermaid 图每页 ≤ 1 张
4. 演讲者备注以 `<!-- _notes: ... -->` 格式写在每页底部
5. 动画过渡以 `<!-- _transition: fade -->` 标注
6. 幻灯片总数 ≤ 60 页（含所有阶段）

### 讲义专有规则

1. 排版引擎 讲义以 `#set text(font: "Noto Serif CJK SC")` 设置中文字体
2. 章节标题用 `#heading(level: 2)[...]` 格式
3. 教学注释用 `#footnote[...]` 放置
4. 思考题用 `#block( fill: luma(240), inset: 8pt, [思考题...])` 呈现
5. 讲义总字数 ≥ 50000字

---

## 教学化图解集成

### 图解类型与教学映射

| 图解类型 | 源节点 | 技术 | 教学说明 |
|----------|--------|------|----------|
| 概念网络图 | T08 | Mermaid graph | 附"如何阅读此图"引导 |
| 因果回路图 | T22 | Mermaid flowchart | 附"正负反馈标识"图例 |
| 博弈矩阵图 | T24 | Mermaid 表格 | 附"各方立场解读" |
| 情景象限图 | T25 | Mermaid quadrantChart | 附"情景导航"指南 |
| 知识图谱图 | T28 | Mermaid graph | 附"图谱导航"指南 |
| 认知偏差映射图 | T26 | Mermaid mindmap | 附"偏差自检清单" |

### 教学化规则

1. 每个图解附教学说明（100-200字）
2. 图解标题用描述性语句（而非学术标签）
3. 复杂图解分步呈现（先展示核心结构，再逐步展开细节）
4. 穷尽重试时以文字描述 + 教学化叙述替代

---

## voice_profile 消费规则

当 context 中存在 voice_profile（T01b 产出）时：

1. 按 tone_guidelines 中的每条规则调整教学语言和措辞
2. 对 forbidden_patterns 中的每种表达模式进行主动过滤和替换
3. 教学语言的亲和力（formal/informal 程度）按 selected_voice 调整
4. 例子和类比的领域选择考虑 reader_name 的背景
5. voice_profile 不写入最终输出正文，仅作为渲染指令消费

---

## 单段质量闸门（M14）

每生成一个自然段（或每扩写一段），强制自问——这一段是否增加了以下七项中的至少一项？

- [ ] 新解释力（对核心问题的因果解释更深入）
- [ ] 新证据（引用了之前未出现的数据/案例/研究）
- [ ] 新案例（展示了新的实例佐证）
- [ ] 新反证（讨论了之前未处理的反面论据）
- [ ] 新边界（明确了结论的适用范围和条件）
- [ ] 新行动含义（将洞察翻译为可操作的行动方向）
- [ ] 新理解方式（提供了新的认知框架/类比/教学图示）

**七项全否**：删除或压缩该段为一句过渡。

### 扩写禁止事项
1. **不得复述前文**——新段落不得用不同措辞重复前面已陈述的观点或结论
2. **不得堆砌同义词**——不得通过同义替换方式对同一概念反复展开（如"结构性矛盾→体制性困境→制度性障碍"）
3. **不得填充常识**——不得用读者已知的常识性背景填充字数（如"随着互联网的发展..."类陈述）
4. **不得重复相同结论**——不得在同一篇输出中多次以不同形式重申同一结论
5. **不得用不同案例讲同一道理**——若两个案例说明的是同一个论点且无新增分析维度，只保留一个
6. **不得用"进一步/更深入/值得注意"开头**——此类过渡词暗示即将复述前文或做无实质扩写
7. **不得无证据扩写**——任何扩展性陈述必须有对应证据、案例、数据或逻辑推导支撑
8. **不得无结构地列举**——禁止"A、B、C、D..."式无分析、无层次、无优先级的平铺列举

**元规则**：成品字数由"主线论证完整性"决定，不为达到特定字数而触发任何扩写。字数是结果不是KPI。

---

## M10 逼退函数（L8 毕业条件）

以下为课程材料渲染层不可跳过的必要条件。任一条件不满足，本节点不得标记为 COMPLETED。

| 指标 | 阈值 |
|------|------|
| 每周知识点覆盖 | ≥5 个 |
| 每课案例 | ≥3 个 |
| 章节结构 | 全部完整 |
| 每段质量闸门(M14) | 全部通过 |

**铁律**：逼退函数是毕业条件，未通过则不得交付。

---

## self_check_before_output

### M10 逼退函数（L8 毕业条件）
> **铁律**：逼退函数是毕业条件，未通过则不得输出最终成品。
> - [ ] **M13 7 步骤全部执行**：渲染前是否已完成全部 7 步 M13 渲染准备（剥离评分/剥离裁决/移除内部标记/附加置信度/映射穷尽重试状态/应用教学风格/生成后备输出）？
> - [ ] **M14 逐段闸门**：每段落是否已通过 7 项闸门检查（新解释力/新证据/新案例/新反证/新边界/新行动含义/新可视化理解）？七项全否的段落是否已删除？

执行以下自检，任一未通过则不得输出：

- [ ] `output_type_confirmed` 是否为 `course_material`？
- [ ] `learning_level` 是否已确定（beginner/intermediate/advanced）？
- [ ] `pre_render_actions` 五项（scores_stripped、verdicts_stripped、internal_notes_removed、confidence_annotations_applied、teaching_narrative_applied）是否全部为 `true`？
- [ ] 5 阶段学习旅程是否全部覆盖（阶段一至阶段五）？
- [ ] 每个阶段是否以"学习目标"开头？
- [ ] 每个阶段是否包含"思考题"？
- [ ] 核心概念是否配了类比和案例？
- [ ] 方法论步骤是否按"思考-尝试-验证"循环呈现？
- [ ] 是否按照渲染技术栈路由选择了正确的技术栈（幻灯片渲染 + 排版引擎）？
- [ ] `slide_output`（幻灯片渲染 幻灯片）是否已生成？
- [ ] `handout_output`（排版引擎 讲义）是否已生成？
- [ ] `exhaust_retry_output` 是否已生成为符合 `exhaust_retry_output_quality` 标准的 Markdown 后备输出？长度是否 ≥ 6000字？
- [ ] `exhaust_retry_output` 的 `required_sections`（课程概述/学习目标/5阶段学习旅程/核心知识点/思考题与练习）是否全部存在且非空？
- [ ] `exhaust_retry_output` 是否包含 `exhaust_retry_marker` 穷尽重试标记？
- [ ] 所有输出中是否不含内部标记（如 `[SCORE: X]`、`[VERDICT: Y]`、流水线元数据等）？
- [ ] 是否所有内容均来自前序流水线产出——无额外新增？
- [ ] 教学化用语是否已替代学术化术语（"证据"→"我们能找到的支持"等）？
- [ ] 每个 Mermaid 图解是否附教学说明？
- [ ] 穷尽重试节点是否保留了核心概念？
- [ ] 幻灯片每页 ≤ 7 行正文？
- [ ] 幻灯片总数 ≤ 60 页？
- [ ] 讲义总字数 ≥ 50000字？

---

## must_not

- **不得添加流水线中未产出的新内容**（这是最高优先级禁令）
- **不得在用户输出中包含内部评分或 Supervisor verdict**
- **不得跳过 5 阶段学习旅程中的任何一个阶段**
- **不得使用学术化术语（必须全部教学化）**
- 不得在 `pre_render_actions` 任一项为 `false` 时输出 `final_output`
- 不得在最终输出中使用流水线内部术语（如任务编号、引擎名称等元信息）
- 不得修改或删减流水线产出的实质内容——仅做格式转换和教学化改写
- 不得处理 `output_type` 非 `course_material` 的请求
- 不得在思考题中直接使用流水线内部结论（应转化为引导性问题）
- 不得对 RETRYING 节点完全舍弃——核心概念必须保留
- 不得在 voice_profile 存在时忽略其消费规则
- 不得在幻灯片中每页超过 7 行正文
- 不得在 Mermaid 图缺失时不提供教学化文字描述替代

---

## 后续步骤

渲染完成后，双模态输出（幻灯片 + 讲义）将传递至 `T20_output_guard.md`（输出卫士）进行正则/关键词扫描，确保无内部元数据标记泄露。若扫描结果为 contaminated，本任务需根据 contaminated_markers 重新净化输出。

---

## knowledge_refs

- `tasks/T01b_voice_calibration.md` — 人设校准与声音配置
- `protocols/nrsf-protocol.md` — NRSF 研究框架协议
- `output/slide-renderer.md` — 幻灯片渲染器
- `output/document-renderer.md` — 排版引擎 文档渲染器
- `protocols/illustration-generation-protocol.md` — 插图与 Mermaid 生成协议
- `output/aesthetic-enhancer.md` — 美学增强器
- `output/illustration-generator.md` — 插图生成器
- `protocols/output-rendering-protocol.md` — 输出渲染协议
- `protocols/nrsf-protocol.md` — 全息框架（T22-T28）叙事综合协议
- `knowledge/cognitive-framework.md` — 认知框架