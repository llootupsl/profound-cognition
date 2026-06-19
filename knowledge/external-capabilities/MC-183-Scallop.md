<!-- 作者：阿洋 -->

# MC-183: Scallop — 神经符号推理

> ★核心方法论已内化于 tasks/T09_cog_reason.md

## 基本信息
- **名称**: Scallop
- **类别**: 方法论卡片
- **类型**: MC
- **语言**: Rust/Python
- **许可证**: MIT
- **仓库**: https://github.com/scallop-lang/scallop

## 核心能力
- Datalog前向链式推理（match_body→instantiate_head→不动点）
- 分层否定（stratified negation）
- 概率前向链式推理与溯源半环（provenance semiring）
- 神经-符号桥接

## 在 profound-cognition 中的用途
- **T09**: 神经符号推理引擎，Pyro与OpenNARS之间第三种范式
- **T13**: 推理路径增强

## 消费节点
- T09
- T13
