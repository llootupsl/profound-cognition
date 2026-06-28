<!-- 作者：阿洋 -->


> **版本治理元数据 (D12.4.2)**:
> - version: 1.0
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（能力卡补全版本治理元数据，D12.4.2）

# MarkItDown

## 基本信息

> ★核心方法论已内化于 knowledge/search-strategy.md，本文件仅作快速引用入口

- **卡片编号**: #4
- **类型**: TC
- **优先级**: P0
- **层级**: L1

## 功能描述
文档格式转换工具，支持 PDF/DOCX/PPTX/XLSX → Markdown 转换，保留结构和格式

## 调用指令

### 输入参数
- `file_path` (string, 文件路径或 URL)
- `output_format` (string, 默认 markdown)
- `preserve_images` (boolean, 默认 true)

### 输出格式
Markdown（保留标题层级、表格、列表）

### 调用示例
```
markitdown.convert(file_path="report.pdf", output_format="markdown", preserve_images=true)
```

## 穷尽重试策略
- **穷尽重试替代路径**: MarkItDown → pandoc → 手动解析
- **触发条件**: MarkItDown 转换失败

## MCP 适配
- **MCP Tool 名称**: markitdown_convert
- **MCP 参数**: file_path, output_format, preserve_images

## 依赖
- MarkItDown 库安装

## 调用前置条件
- Python 3.9+ 运行环境（如需代码执行）
- MarkItDown 库已安装（见上方「依赖」）
- 本地文件系统可读（MarkItDown 为文件转换工具）
- 上游节点产出已就绪（根据消费节点依赖关系）

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

暂无显式 DAG 节点消费者。保留待扩展。


## 效果度量

| 度量指标 | 定义 | 目标值 |
|----------|------|--------|
| 执行成功率 | 成功调用次数 / 总调用次数 | ≥ 0.95 |
| 平均延迟 | 单次调用平均耗时 | ≤ 5s |
| 输出质量分 | Supervisor 评分（0-1） | ≥ 0.8 |
| 穷尽重试触发率 | 触发降级的调用次数 / 总调用次数 | ≤ 0.1 |

效果度量写入 NRSF，供 T19 质量检查消费。