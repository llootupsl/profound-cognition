<!-- 作者：阿洋 -->


> **版本治理元数据 (D12.4.2)**:
> - version: 1.0
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（能力卡补全版本治理元数据，D12.4.2）

# TC-055: Mesa — Agent-Based Modeling Framework

> ★核心方法论已内化于 tasks/TM01_system_dynamics.md

## 基本信息
- **名称**: Mesa
- **类别**: 仿真框架
- **语言**: Python
- **版本要求**: ≥3.0
- **安装**: pip install mesa
- **许可证**: Apache 2.0
- **仓库**: https://github.com/projectmesa/mesa

## 核心能力
- 基于 Agent 的建模与仿真 (ABM)
- 模块化 Agent/Model/Schedule 设计
- 内置可视化 (Mesa Visualization)
- 批量运行与参数扫描
- 数据收集器 (DataCollector)

## 在 profound-cognition 中的用途
- **T22 Step 6**: ABM 仿真执行
- **穷尽重试替代路径**: 无定量参数时穷尽重试替代为 PARTIAL_B（仅定性 ABM 设计文档）

## API 示例
```python
from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

class ResearchAgent(Agent):
    def __init__(self, unique_id, model, agent_type):
        super().__init__(unique_id, model)
        self.agent_type = agent_type

    def step(self):
        pass

class ResearchModel(Model):
    def __init__(self, N):
        self.schedule = RandomActivation(self)
        for i in range(N):
            agent = ResearchAgent(i, self, "stakeholder")
            self.schedule.add(agent)

    def step(self):
        self.schedule.step()
```

## 已知限制
- 大规模仿真（>10000 agents）性能受限
- 需要定量参数才能执行完整仿真
- 纯文本研究场景仅能生成定性设计文档

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

| 节点 | 用途 |
|------|------|
| TM01 | ABM仿真框架 |


## 调用前置条件

- Python 3.9+ 运行环境（如需代码执行）
- 对应工具库已安装（详见卡片「安装」或「基本信息」字段）
- 网络连接可用（如需远程 API 或数据源）
- 上游节点产出已就绪（根据消费节点依赖关系）

## 效果度量

| 度量指标 | 定义 | 目标值 |
|----------|------|--------|
| 执行成功率 | 成功调用次数 / 总调用次数 | ≥ 0.95 |
| 平均延迟 | 单次调用平均耗时 | ≤ 5s |
| 输出质量分 | Supervisor 评分（0-1） | ≥ 0.8 |
| 穷尽重试触发率 | 触发降级的调用次数 / 总调用次数 | ≤ 0.1 |

效果度量写入 NRSF，供 T19 质量检查消费。