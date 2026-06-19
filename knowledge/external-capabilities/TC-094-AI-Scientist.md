<!-- 作者：阿洋 -->

# TC-094: AI-Scientist — 科学发现流水线

> ★核心方法论已内化于 extensions/scientific-discovery.md

## 基本信息
- **名称**: AI-Scientist
- **类别**: 科学发现
- **语言**: Python
- **许可证**: MIT
- **仓库**: https://github.com/SakanaAI/AI-Scientist

## 核心能力
- 假设生成（三种变异操作：组合/方向/反事实）
- H_score假设评估（0.4×新颖度 + 0.3×可行性 + 0.3×影响力）
- 实验类型决策树（RCT/quasi-experimental/observational/simulation/formal_verification/A/B_test）
- 实验评估（p_value<0.05 且 effect_size>0.2→SUPPORTED）
- 自动化科学方法全流程（假设→实验→代码→论文）

## 在 profound-cognition 中的用途
- **scientific-discovery.md**: 科学发现核心执行引擎

## 消费节点
- scientific-discovery.md
