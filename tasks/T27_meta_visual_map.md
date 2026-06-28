<!-- output_type_restriction: [research_report, wechat_article, course_material]  # R1-02 分层激活 -->
---
task_id: T27
task_name: meta_visual_map
description: 14维度关系可视化 — 内联 Mermaid/SVG，自足生成
activation: output_type == 'research_report'
deps: [T26]
suggested_tok: 1500  # D2.4.4: 建议预算（非硬性上限），与 EXHAUST 模式"Token 不设上限"原则一致
priority: medium
---

<!-- 作者：阿洋 -->


# T27 — 14维度关系可视化

## 角色定义
你是维度关系可视化者。你的任务是**直接在成品文件中写出 Mermaid 代码块或内联 SVG**，生成 3 种可视化产出，展示 14 维度间的关系。不依赖任何外部制图服务/技能——目标平台原生渲染 Mermaid/SVG。

## 3种可视化产出

### 可视化1: 维度关系图
- 实现：**Mermaid `graph`（或内联 SVG 网络图）**
- 节点：14 个维度
- 边：T26 识别的交叉关系
- 视觉编码：节点标签标注维度权重；用边标签或线型表达关系强度
- 美化为可选项；服务不可用绝不省略此图

### 可视化2: 权重热力图
- 实现：**内联 SVG 14×14 色块矩阵**（或带背景色标注的 Markdown 矩阵表作为兜底）
- 编码：颜色深度 = 维度间关联强度
- 标注：对角线为维度自身权重

### 可视化3: 主题-维度映射图
- 实现：**Mermaid `sankey-beta`（或内联 SVG 冲积图）**
- 流向：研究主题 → 14 维度 → 关键发现
- 编码：流量宽度 = 证据强度

## 产出结构
> **execution_params**: object  # 实际执行参数，必须达到 SKILL.md 规定的最低值（R2-05 防深度缩水）

```json
{
  "task_id": "T27",
  "status": "COMPLETED",
  "visualizations": {
    "dimension_network": "Mermaid graph / 内联 SVG 网络图",
    "weight_heatmap": "内联 SVG 色块矩阵 / 带色标 Markdown 矩阵",
    "topic_dimension_flow": "Mermaid sankey-beta / 内联 SVG 冲积图"
  },
  "figure_engine": "inline-mermaid-svg (self-contained)",
  "enhancement": "外部论文制图服务（可选，不可用时不影响产出）"
}
```

## 质量要求
- 3 种可视化全部产出，且均为成品文件中可直接渲染的 Mermaid/SVG
- 每图附 ≤2 句图注（含图号、标题、数据/来源）
- 视觉风格一致
- 附录写入 NRSF §T27_*
