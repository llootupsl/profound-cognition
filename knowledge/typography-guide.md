<!-- 作者：阿洋 -->

# 排版方法论

> **版本治理元数据 (D12.4.2)**:
> - version: 1.1
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（排版引擎选择表 + 字体穷尽尝试链）
>   - v1.1 补全版本治理元数据与交叉引用（D12.4.2-D12.4.3）

## 交叉引用

- **上游**: `knowledge/output-types.md`（成品类型枚举，决定排版引擎选择）
- **下游**: `tasks/T20a_research_render.md`（研究报告渲染）、`tasks/T20b_wechat_render.md`（公众号渲染）、`tasks/T20c_course_render.md`（课程材料渲染）
- **相关**: `output/typography-system.md`（排版系统）、`output/font-scheme.md`（字体方案）、`output/rendering-tech-stack.md`（渲染技术栈）、`output/document-renderer.md`（文档渲染器）

## 1. 排版引擎选择表

| output_type | 首选引擎 | 备选引擎 | 输出格式 |
|-------------|---------|---------|---------|
| research_report | Typst → WeasyPrint | Pandoc | PDF/HTML |
| course_material | Marp / Typst | Pandoc | PDF/HTML |
| wechat_article | HTML内联 | 纯文本 | HTML/纯文本 |

## 2. 字体穷尽尝试链

```
霞鹜文楷 → 未来荧黑 → Fusion Pixel → 系统字体
```

### 2.1 字体选择规则
- 正文：霞鹜文楷（开源、可商用、中文友好）
- 标题：未来荧黑（现代感、辨识度高）
- 代码：Fusion Pixel（等宽、像素风）
- 穷尽尝试：系统默认字体

### 2.2 详细字体配置表

| output_type | document_class | 说明 | 字体方案 | 穷尽尝试方案 |
|-------------|---------------|------|---------|---------|
| **research_report** | `article` | 研究报告/分析报告/学术论文 | 正文：霞鹜文楷（noto-serif-regular），标题：未来荧黑（arapey-regular），代码：Fusion Pixel（jetbrains-mono-regular） | 思宋、Noto Serif SC、Times New Roman |

## 3. 中文学术排版规则

### 3.1 引用格式
- 遵循 GB/T 7714-2015 信息与文献 参考文献著录规则
- 格式：`[序号] 作者. 题名[文献类型标志]. 刊名, 年, 卷(期): 页码.`
- 示例：`[1] 张三. 人工智能发展研究[J]. 计算机学报, 2024, 45(3): 123-135.`

### 3.2 页眉页脚
- 页眉：左页章节标题，右页文档标题
- 页脚：页码居中

### 3.3 自动目录
- 生成三级目录（章→节→小节）
- 目录页码与正文页码分离

### 3.4 图表索引
- 图索引：按图编号排列
- 表索引：按表编号排列

## 4. 模板匹配规则

| output_type | 模板格式 | 模板位置 |
|-------------|---------|---------|
| research_report | Typst | templates/research_report.typ |
| research_report | Typst | templates/research_report.typ |
| research_report | Typst | templates/research_report.typ |
