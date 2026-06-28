<!-- 作者：阿洋 -->


> **版本治理元数据 (D12.4.2)**:
> - version: 1.0
> - last_updated: 2026-06-27
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（Audit-7 Stage 2 补建，对应 v5.1.0 报告推荐项）

# TC-132: SciencePlots — matplotlib 科学绘图样式

## 基本信息
- **名称**: SciencePlots
- **类别**: matplotlib 科学绘图样式
- **语言**: Python
- **版本要求**: >=1.1
- **许可证**: MIT
- **仓库**: https://github.com/garrettj403/SciencePlots
- **维护方**: John Garrett

## 核心能力
- matplotlib 科学绘图样式库（Nature / Science / IEEE 等期刊风格）
- 多种期刊/配色样式（science / ieee / nature / notes / scatter 等）
- 与 LaTeX 集成（支持 pgfplots 后端，数学公式原生渲染）
- 跨平台一致的学术图表风格（DPI / 字体 / 线宽标准化）

## 在 profound-cognition 中的用途
- **T27 可视化渲染**: T27 可视化渲染节点备选样式库；当前主路径使用 matplotlib + 自定义样式 + DLP-scienceplots 画像，SciencePlots 可作为期刊风格一键应用入口待激活
- **状态**: 待激活
- **对应 v5.1.0 报告项**: 第四章 4.3.13 节

## 消费节点
- T27 可视化渲染（待激活）

## 调用前置条件

- Python 3.9+ 运行环境（如需代码执行）
- 对应工具库已安装（详见「基本信息」字段）
- 网络连接可用（如需远程 API 或数据源）
- 上游节点产出已就绪（根据消费节点依赖关系）

## 失败回退策略

- **触发条件**: 工具不可用、调用超时、输出质量不达标、依赖缺失
- **回退路径**: 降级到 LLM 内建能力，标注 [INTERNAL_REASONING]
- **回退声明**: 回退后失去工具增强能力，但保证流程不中断（EXHAUST 铁律）
- **穷尽重试**: 按 L1_FULL → L2_PARTIAL → L3_TEXT_ONLY → L4_SERVICE_DOWN 逐级降级

## 效果度量

| 度量指标 | 定义 | 目标值 |
|----------|------|--------|
| 执行成功率 | 成功调用次数 / 总调用次数 | >= 0.95 |
| 平均延迟 | 单次调用平均耗时 | <= 5s |
| 输出质量分 | Supervisor 评分（0-1） | >= 0.8 |
| 穷尽重试触发率 | 触发降级的调用次数 / 总调用次数 | <= 0.1 |

## 替代关系
- **可被替代为**: matplotlib + 手动样式配置（DLP-scienceplots 画像已内化）
- **替代说明**: 见 v5.1.0 报告第四章 4.3.13 节融入方案

## Audit-7 Stage 2 备注
- **核验状态**: ❌缺失 → ✅已补建（Audit-7 Stage 2）
- **对应 v5.1.0 报告项**: 4.3.13
- **核验日期**: 2026-06-27
- **审计员**: 独立审计子代理（Audit-7）
