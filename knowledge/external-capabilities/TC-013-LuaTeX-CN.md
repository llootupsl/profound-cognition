<!-- 作者：阿洋 -->


> **版本治理元数据 (D12.4.2)**:
> - version: 1.0
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（能力卡补全版本治理元数据，D12.4.2）

# LuaTeX-CN

## 基本信息
- **卡片编号**: #13
- **类型**: TC
- **优先级**: P1
- **层级**: L1

## 功能描述
LuaTeX-CN 中文 LaTeX 引擎，基于 LuaTeX 的中文排版方案，原生支持 ctex 宏包和中文断行规则。适用于含大量中文内容的学术论文、技术报告排版，提供精细的字体配置和中日韩排版控制。

## 调用指令

### 输入参数
- `source_tex` (string, LaTeX 源码或 .tex 文件路径)
- `output_format` (string, 输出格式: pdf，默认 pdf)
- `font_config` (object, 可选字体配置，含 main_font/mono_font/cjk_font)

### 输出格式
PDF

### 调用示例
```
luatex.compile(source_tex="/output/chinese_paper.tex", output_format="pdf", font_config={"main_font": "Source Han Serif SC", "cjk_font": "Source Han Sans SC"})
```

## 穷尽重试策略
- **穷尽重试替代路径**: LuaTeX-CN → Typst → WeasyPrint
- **触发条件**: LuaTeX 编译失败或 ctex 宏包缺失

## MCP 适配
- **MCP Tool 名称**: luatex_compile
- **MCP 参数**: source_tex, output_format, font_config

## 依赖
- TeX Live / MiKTeX 发行版 + ctex 宏包 + 中文字体（霞鹜文楷/思源宋体）

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

暂无显式 DAG 节点消费者。保留待扩展。

## 方法论内化

> ★核心方法论已内化于 rendering-pipeline/ARCHITECTURE.md，以下为快速参考

### 方法论原理
LuaTeX是TeX生态的编程扩展，通过Lua脚本实现中文排版自动化，解决了CJK字体配置和排版规则定制问题。

### 执行步骤
1. 配置中文字体和排版规则
2. 编写LaTeX+Lua内容
3. 处理中文断行和标点压缩
4. 编译为PDF

### 决策规则
| 条件 | 动作 |
|------|------|
| 需要中文专业排版 | LuaTeX-CN |
| 需要现代工具链 | Typst |
| 需要简单中文 | Markdown |

### 输出规范
```yaml
luatex_cn_output:
  available: bool
  pdf_path: str
  cjk_support: bool
  degradation_note: str
```

### 穷尽重试策略
| 级别 | 方案 |
|------|------|
| L1 | LuaTeX-CN完整编译 |
| L2 | Typst(简化中文) |
| L3 | WeasyPrint |
| L4 | 纯文本 |


## 效果度量

| 度量指标 | 定义 | 目标值 |
|----------|------|--------|
| 执行成功率 | 成功调用次数 / 总调用次数 | ≥ 0.95 |
| 平均延迟 | 单次调用平均耗时 | ≤ 5s |
| 输出质量分 | Supervisor 评分（0-1） | ≥ 0.8 |
| 穷尽重试触发率 | 触发降级的调用次数 / 总调用次数 | ≤ 0.1 |

效果度量写入 NRSF，供 T19 质量检查消费。