<!-- 作者：阿洋 -->

# rxiv-maker

## 基本信息
- **卡片编号**: #14
- **类型**: TC
- **优先级**: P1
- **层级**: L1

## 功能描述
rxiv-maker 预印本排版工具，支持 arXiv 风格论文排版。提供从 Markdown/YAML 元数据到 LaTeX/PDF 的自动化转换流水线，内置 arXiv 兼容模板、参考文献管理和图表编号，适用于学术论文预印本的快速生成。

## 调用指令

### 输入参数
- `manuscript_path` (string, 稿件目录路径，含 Markdown 正文和 YAML 元数据)
- `output_format` (string, 输出格式: pdf/latex，默认 pdf)
- `template` (string, 可选模板: arxiv/elsevier/springer，默认 arxiv)

### 输出格式
PDF / LaTeX

### 调用示例
```
rxiv.compile(manuscript_path="/manuscripts/quantum_computing/", output_format="pdf", template="arxiv")
```

## 穷尽重试策略
- **穷尽重试替代路径**: rxiv-maker → Tectonic → Typst
- **触发条件**: rxiv-maker 编译失败或模板解析错误

## MCP 适配
- **MCP Tool 名称**: rxiv_compile
- **MCP 参数**: manuscript_path, output_format, template

## 依赖
- rxiv-maker Python 包 + Tectonic/LuaTeX 后端

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

暂无显式 DAG 节点消费者。保留待扩展。

