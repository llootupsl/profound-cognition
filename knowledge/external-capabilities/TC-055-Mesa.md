<!-- 作者：阿洋 -->

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

