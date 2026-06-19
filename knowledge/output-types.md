<!-- 作者：阿洋 -->

# 成品类型枚举 (v3)

## 三种成品类型

| 类型 | 说明 | 适用场景 | 字数范围 |
|------|------|----------|----------|
| `research_report` | 深度研究报告（合并 research_master/analysis_report/press_commentary/decision_memo/strategic_foresight/quick_insight/visual_brief） | 综合深度研究，消费全量节点产出，含完整全息框架3部分结构 | ≥100000字（不设上限） |
| `wechat_article` | 公众号文章 | 微信公众平台，人设叙事+能力卡片精选 | ≥3000字（不设上限） |
| `course_material` | 课程材料（合并 lecture_notes/video_script） | 教学/培训场景，讲义/视频脚本双模态 | 按模块数量弹性 |

## 类型详细定义

### research_report（深度研究报告）
- 消费全部节点产出（含Phase 7元维度引擎 T22-T28）
- 报告结构：全息框架3部分 × 14维度 × 40方面
  - 第一部分（问题认知与定义，4维度）：主题坐标系定位、核心要素分解、时空场演化、问题重构
  - 第二部分（全维全域分析，8维度）：技术/经济/政治/社会文化/生态/法律伦理/历史/心理认知
  - 第三部分（极限决策推理，2维度）：综合决策推演、深度洞察
- 排版引擎：Typst（首选）→ Pandoc + WeasyPrint → HTML内嵌 → Markdown → 纯文本
- 引用格式：段落级引用，L0-L3证据等级标注
- 图表要求：内联 Mermaid/SVG 图生成 手绘框架图
- 47张能力卡片按三层认知加载体系嵌入
- 受众：决策者 + 专业读者 + 公众传播

### wechat_article（公众号文章）
- 5阶段叙事架构：Hook → 信息阶梯 → 峰终定律 → 传播张力 → 行动号召
- 渲染引擎：T20b_wechat_render（独立节点）
- 渲染链：墨卡Moka → 内置公众号排版系统 → HTML内联 → 纯文本
- 图表：Mermaid SVG内嵌，≤5张
- 63张能力卡片精选嵌入（3-5张文末嵌入）
- Phase -1人设初始化需完整执行
- L4人工触感检查清单

### course_material（课程材料）
- output_subtype枚举：'lecture' | 'video_script'
- lecture子类型：5阶段学习旅程（引入→核心概念→深度分析→应用案例→反思练习）
- video_script子类型：含Manim动画脚本
- 图表：Mermaid图 + 每模块内联 Mermaid/SVG 图生成概念图生成
- 排版：Marp幻灯片 → Typst PDF

## 输出类型兼容映射

| 历史类型 | 标准类型 | 转换说明 |
|--------|--------|----------|
| research_master | research_report | 自动映射 |
| analysis_report | research_report | 自动映射 |
| press_commentary | research_report | 自动映射 |
| decision_memo | research_report | 自动映射 |
| strategic_foresight | research_report | 自动映射 |
| quick_insight | research_report | 自动映射 |
| visual_brief | research_report | 自动映射 |
| wechat_article | wechat_article | 保持不变 |
| lecture_notes | course_material | output_subtype='lecture' |
| video_script | course_material | output_subtype='video_script' |

## 类型推断关键词

| 类型 | 关键词 |
|------|--------|
| `research_report` | 研究、深度分析、综合报告、深度研究、分析、决策、前瞻、洞察 |
| `wechat_article` | 公众号、微信文章、自媒体、推文 |
| `course_material` | 讲义、课程、教案、教学材料、视频脚本、短视频、课程视频 |

## 渲染路由（v3）

- `research_report` → T20a_research_render（Typst → PDF/HTML）
- `wechat_article` → T20b_wechat_render（墨卡Moka → 内置公众号排版系统 → HTML内联）
- `course_material` → T20c_course_render（Marp幻灯片 → Typst PDF）

## v3 输出门控标准

所有输出类型均需通过以下门控：
1. 字数达标（research_report ≥100000, wechat_article ≥3000）
2. 引用均可溯源（严禁幻觉引用）
3. 反证比率 ≥ 0.25
4. 来源域名 ≥ 15个（research_report）
5. 偏差检测 ≥ 30 biases identified
6. 图完整性：所有图均有 caption + legend
7. 留白标记：无 []、TODO、待补充等留白标记