<!-- 作者：阿洋 -->


> **版本治理元数据 (D12.4.2)**:
> - version: 1.0
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（能力卡补全版本治理元数据，D12.4.2）

# PaperVizAgent

> **v2.0 废弃说明**: PaperVizAgent 原为专有 API 可视化代理，采用 5-Agent × 3 轮迭代架构生成可视化图表。该方式依赖专有 API，违反"代码生成优先"原则，**已全面废弃**。所有原 PaperVizAgent 消费场景改为**代码生成**（Observable Plot / ECharts / 内联 SVG），由 LLM 直接书写代码生成可视化图表。详见 [illustration-generator.md §0 核心铁律](../../output/illustration-generator.md)。

## 基本信息
- **卡片编号**: #44
- **类型**: TC
- **优先级**: P2
- **层级**: L1
- **状态**: **deprecated**（已废弃）

## 废弃原因
1. PaperVizAgent 依赖专有 API 生成可视化图表
2. 违反用户明确要求"大多数时候图片应该用代码生成，而非用API"
3. 违反 [illustration-generator.md §0 核心铁律](../../output/illustration-generator.md) 的 `forbidden_apis` 清单

## 替代方案
所有原 PaperVizAgent 消费场景改为**代码生成**：

| 原 PaperVizAgent 场景 | 替代代码生成方式 |
|------------------------|-----------------|
| 复杂学术可视化 | Observable Plot / ECharts / 内联 SVG |
| 多维度数据展示 | ECharts / Plotly / Matplotlib |
| 批量论文图表 | 代码生成（Observable Plot / ECharts） |

## 历史调用方式（已废弃，仅供历史参考）

### 原输入参数（已废弃）
- `description` (string, 可视化需求描述)
- `data` (object, 可选, 图表数据)
- `iteration_rounds` (integer, 可选, 迭代轮数，默认 3)

### 原调用示例（已废弃）
```
# 已废弃——禁止调用
paperviz_generate.generate(description="多维度对比雷达图：全球主要城市生活质量指数", data={"cities": ["东京", "纽约", "伦敦", "上海"], "dimensions": ["安全", "教育", "医疗", "环境", "交通"]}, iteration_rounds=3)
```

## 替代代码生成示例

### Observable Plot 代码生成（替代 PaperVizAgent）
```javascript
import * as Plot from "@observablehq/plot";

const chart = Plot.plot({
  width: 600,
  height: 400,
  marks: [
    Plot.line(data, {x: "year", y: "value", stroke: "category"})
  ]
});
```

### ECharts 代码生成（替代 PaperVizAgent）
```javascript
const option = {
  radar: {
    indicator: [
      { name: '安全', max: 100 },
      { name: '教育', max: 100 },
      { name: '医疗', max: 100 }
    ]
  },
  series: [{
    type: 'radar',
    data: [{ value: [85, 92, 78] }]
  }]
};
```

## 依赖
- ~~专有 API~~ **已废弃**
- 替代依赖：**无外部依赖**（纯代码生成，由 LLM 直接书写 Observable Plot / ECharts / SVG 代码）

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

暂无显式 DAG 节点消费者。保留待扩展。

## 失败回退策略

- **触发条件**: 工具不可用、调用超时、输出质量不达标、依赖缺失
- **回退路径**: 降级到 LLM 内建能力，标注 [INTERNAL_REASONING]
- **回退声明**: 回退后失去工具增强能力，但保证流程不中断（EXHAUST 铁律）
- **穷尽重试**: 按 L1_FULL → L2_PARTIAL → L3_TEXT_ONLY → L4_SERVICE_DOWN 逐级降级

## 效果度量

| 度量指标 | 定义 | 目标值 |
|----------|------|--------|
| 执行成功率 | 成功调用次数 / 总调用次数 | ≥ 0.95 |
| 平均延迟 | 单次调用平均耗时 | ≤ 5s |
| 输出质量分 | Supervisor 评分（0-1） | ≥ 0.8 |
| 穷尽重试触发率 | 触发降级的调用次数 / 总调用次数 | ≤ 0.1 |

效果度量写入 NRSF，供 T19 质量检查消费。