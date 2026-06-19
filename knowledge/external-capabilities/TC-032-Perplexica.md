<!-- 作者：阿洋 -->

# Perplexica

## 基本信息
- **卡片编号**: #32
- **类型**: TC
- **优先级**: P2
- **层级**: L1

## 功能描述
Perplexica AI 搜索引擎，支持多角度查询重写和深度搜索。自动将用户查询从多个角度重写为子查询，并行执行搜索并聚合结果，支持焦点模式（全部/学术/写作/数学/视频）切换，适用于需要多维度信息检索和深度探索的场景。

## 调用指令

### 输入参数
- `query` (string, 搜索查询文本)
- `focus_mode` (string, 可选: 焦点模式 all/academic/writing/math/youtube，默认 all)
- `rewrite_angles` (array, 可选: 自定义重写角度列表)

### 输出格式
搜索结果 + 重写查询，每条含 title、url、snippet、source_angle

### 调用示例
```
perplexica_search(query="量子计算在密码学中的应用前景", focus_mode="academic", rewrite_angles=["理论安全","工程实现","标准化进展"])
```

## 穷尽重试策略
- **穷尽重试替代路径**: Perplexica → SearXNG 直接搜索
- **触发条件**: Perplexica 服务不可用或查询重写模块超时

## MCP 适配
- **MCP Tool 名称**: perplexica_search
- **MCP 参数**: query, focus_mode, rewrite_angles

## 依赖
- Perplexica 服务部署 + SearXNG 搜索引擎 + LLM 推理后端

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

暂无显式 DAG 节点消费者。保留待扩展。

