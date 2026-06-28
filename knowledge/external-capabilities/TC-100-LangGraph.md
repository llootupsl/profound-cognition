<!-- 作者：阿洋 -->


> **版本治理元数据 (D12.4.2)**:
> - version: 1.1
> - last_updated: 2026-06-27
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（能力卡补全版本治理元数据，D12.4.2）
>   - v1.1 优先级 P1→P0（A6.2-F4 修复，与 capability-version-sync.md L88 P0 归类对齐，LangGraph 作为 DAG 原生编排引擎影响全流程）

# LangGraph

> ★DAG 原生编排引擎，将 58 节点 DAG 映射为 LangGraph StateGraph

## 基本信息
- **卡片编号**: #100
- **类型**: TC
- **优先级**: P0
- **层级**: L0
- **版本**: 0.2.x

## 功能描述
LangGraph 是基于图结构的状态机编排引擎，将 Profound Cognition 的 58 节点 DAG 拓扑映射为 LangGraph StateGraph，实现节点依赖关系的原生管理、状态自动传递、并行编排、中断恢复与循环检测。LangGraph 替代原有 execution-protocol.md 中的 `find_ready_nodes()` 伪代码调度逻辑，将"主 LLM 手动遍历 DAG 找就绪节点"升级为"LangGraph 引擎自动按拓扑序调度"。

### 核心能力
- **StateGraph 定义**：将 58 个 DAG 节点注册为 LangGraph 节点，依赖关系注册为 LangGraph 边，`context_package` 作为 LangGraph State 核心字段
- **checkpoint 机制**：自动保存 State 快照，支持断点恢复，替代 checkpoint-protocol.md 的手动 Phase 级快照
- **parallel 节点**：原生支持 fan-out/fan-in 模式，用于 T10/T11/T12 三路对抗验证并行执行
- **interrupt_before**：在指定节点前中断等待外部输入，用于 T00b（人设采集）和 I01（迭代深化用户确认）
- **循环检测**：编译期通过 `cycle-detection-check.py`（Kahn's algorithm）检测 DAG 是否有环；运行期通过 LangGraph 递归上限与状态指纹双重保护

## 调用前置条件
- Python 3.10+
- `langgraph` 库已安装（`pip install langgraph>=0.2.0`）
- `typing_extensions`、`operator`（标准库，无需额外安装）

## 失败回退策略
- **触发条件**：`langgraph` 库不可用（ImportError）、StateGraph 编译失败、运行期异常无法恢复
- **回退路径**：回退到原有 `execution-protocol.md` 中的 `find_ready_nodes()` 伪代码编排（保留为注释/文档说明，不删除）
- **回退声明**：回退后功能等价但失去 LangGraph 的原生并行调度、自动 checkpoint、interrupt_before 能力，需主 LLM 手动模拟上述机制

## 替代关系声明
- **替代对象**：`execution-protocol.md` 中的 `find_ready_nodes()` 伪代码、手动拓扑排序逻辑
- **不替代**：`checkpoint-protocol.md` 的 Phase 级业务语义检查点（LangGraph checkpoint 是状态级技术快照，二者互补，见 checkpoint-protocol.md「LangGraph Checkpoint 集成」章节）
- **共存关系**：`cycle-detection-check.py`（编译期环检测）与 LangGraph 运行期循环检测配合使用

## 调用指令

### 输入参数
- `dag_topology` (dict, SKILL.md 定义的 58 节点 DAG 拓扑)
- `initial_state` (dict, 初始 ResearchState，含 problem/output_type)
- `checkpoint_backend` (string, 可选: "memory"|"file"|"redis"，默认 "memory")
- `interrupt_nodes` (list, 可选: 需中断的节点 ID 列表，默认 ["T00b", "I01"])

### 输出格式
- 编译后的 `CompiledGraph` 实例，可调用 `.invoke()` / `.stream()` / `.get_state_history()`

### 调用示例
```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

class ResearchState(TypedDict):
    context_package: dict
    execution_ledger: Annotated[list, operator.add]
    node_outputs: dict
    current_phase: int

graph = StateGraph(ResearchState)
graph.add_node("T00a", t00a_node)
graph.add_edge("T00a", "T00b")
graph.add_edge("T28", END)
compiled = graph.compile(
    interrupt_before=["T00b", "I01"],
    checkpointer=checkpointer,
)
```

## 效果度量字段
| 字段 | 类型 | 说明 |
|------|------|------|
| `node_count` | int | 已注册的 LangGraph 节点总数（应为 57） |
| `edge_count` | int | 已注册的 LangGraph 边总数（含依赖边与 END 边） |
| `cycle_detected` | bool | 编译期是否检测到环（True=有环，编译失败） |
| `checkpoint_count` | int | 运行期已保存的 checkpoint 数量 |

## 版本同步机制
- **同步对象**：LangGraph 官方版本（https://github.com/langchain-ai/langgraph）
- **同步频率**：每季度检查一次官方 release，评估是否升级
- **兼容性策略**：本框架使用 `langgraph>=0.2.0` 的稳定 API（StateGraph、add_node、add_edge、compile、interrupt_before、checkpointer），避免使用实验性 API
- **升级评估**：升级前需运行 `scripts/cycle-detection-check.py` 与 `scripts/exhaust-consistency-check.py` 双重验证

## MCP 适配
- **MCP Tool 名称**: langgraph_compile
- **MCP 参数**: dag_topology, initial_state, checkpoint_backend, interrupt_nodes

## 依赖
- `langgraph>=0.2.0`
- Python 3.10+（TypedDict、Annotated 需要 3.9+，建议 3.10+）

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

| 节点 | 激活条件 | 使用方式 |
|------|---------|---------|
| 全部 58 节点 | always | LangGraph 编排引擎统一调度，非单节点消费 |
