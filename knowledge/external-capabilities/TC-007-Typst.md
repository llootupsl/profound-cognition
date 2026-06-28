<!-- 作者：阿洋 -->


> **版本治理元数据 (D12.4.2)**:
> - version: 1.0
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（能力卡补全版本治理元数据，D12.4.2）

# Typst

## 基本信息
- **卡片编号**: #7
- **类型**: TC
- **优先级**: P0
- **层级**: L1

## 功能描述
学术排版引擎，Typst 0.13+ 版本，支持中文排版、自动目录、引用管理、数学公式。作为 research_master 和 lecture_notes 的备选排版引擎（WeasyPrint 不可用时的穷尽重试替代路径）。

## 调用指令

### 输入参数
- `source` (string, Typst 源码)
- `input_files` (array, 附加文件路径)
- `output_format` (string, pdf/svg/png)
- `font_paths` (array, 字体路径)

### 输出格式
PDF/SVG/PNG

### 调用示例
```
typst.compile(source="research_master.typ", output_format="pdf", font_paths=["/fonts/"])
```

## 穷尽重试策略
- **穷尽重试替代路径**: Typst → WeasyPrint → HTML
- **触发条件**: Typst 编译失败或服务不可用

## MCP 适配
- **MCP Tool 名称**: typst_compile
- **MCP 参数**: source, input_files, output_format, font_paths

## 依赖
- Typst 0.13+ 安装 + 中文字体（霞鹜文楷/未来荧黑）

## 调用前置条件
- Python 3.9+ 运行环境（如需代码执行）
- Typst 0.13+ 已安装 + 中文字体已配置（见上方「依赖」）
- 本地文件系统可写（Typst 为本地编译工具）
- 上游节点产出已就绪（根据消费节点依赖关系）

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

暂无显式 DAG 节点消费者。保留待扩展。

## 方法论内化

> ★核心方法论已内化于 rendering-pipeline/ARCHITECTURE.md，以下为快速参考

### 方法论原理
Typst是现代排版系统，通过可编程标记语言实现学术文档的自动化排版，解决了LaTeX配置复杂、编译慢的痛点。

### 执行步骤
1. 定义文档类和样式
2. 编写Typst标记内容
3. 插入公式/图表/引用
4. 编译为PDF

### 决策规则
| 条件 | 动作 |
|------|------|
| 需要可编程排版 | Typst |
| 需要LaTeX生态 | LuaTeX |
| 需要简单排版 | WeasyPrint |

### 输出规范
```yaml
typst_output:
  available: bool
  pdf_path: str
  compile_success: bool
  degradation_note: str
```

### 穷尽重试策略
| 级别 | 方案 |
|------|------|
| L1 | Typst完整编译 |
| L2 | WeasyPrint(HTML→PDF) |
| L3 | Markdown+Pandoc |
| L4 | 纯文本 |


## 效果度量

| 度量指标 | 定义 | 目标值 |
|----------|------|--------|
| 执行成功率 | 成功调用次数 / 总调用次数 | ≥ 0.95 |
| 平均延迟 | 单次调用平均耗时 | ≤ 5s |
| 输出质量分 | Supervisor 评分（0-1） | ≥ 0.8 |
| 穷尽重试触发率 | 触发降级的调用次数 / 总调用次数 | ≤ 0.1 |

效果度量写入 NRSF，供 T19 质量检查消费。