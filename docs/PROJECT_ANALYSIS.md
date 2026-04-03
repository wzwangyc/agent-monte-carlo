# Agent Monte Carlo - 项目现状与演进路线分析

**日期：** 2026-04-03  
**作者：** Leo (AI Assistant)  
**状态：** 战略规划文档

---

## 一、当前项目状态

### 1.1 已实现的功能

| 模块 | 状态 | 说明 |
|------|------|------|
| **Traditional MC** | ✅ 完成 | 基于 GBM 的蒙特卡洛模拟 |
| **Agent MC (简化版)** | ⚠️ 部分完成 | 硬编码的行为偏差模拟 |
| **Streamlit UI** | ✅ 完成 | 双模式对比可视化 |
| **风险指标计算** | ✅ 完成 | VaR, ES, Kurtosis, MaxDD |
| **波动率聚集** | ✅ 完成 | GARCH-like 效应 |
| **混合计费模式** | ✅ 完成 | Free Tier + Pro Mode |

### 1.2 当前架构

```
┌─────────────────────────────────────────────────────────┐
│                    Streamlit UI                          │
│  (app.py - 硬编码 Agent 行为 + 可视化)                    │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│              generate_agent_mc_paths()                   │
│  - 硬编码 3 种 Agent 类型 (retail/institution/hedge)      │
│  - 硬编码行为参数 (herding=0.3, overconfidence=0.2)      │
│  - 硬编码 GARCH 参数 (α=0.1, β=0.85)                     │
│  - 无 Agent 记忆                                         │
│  - 无 Agent 学习                                         │
│  - 无 Agent 交流                                         │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│              输出：价格路径 + 风险指标                    │
└─────────────────────────────────────────────────────────┘
```

---

## 二、当前版本 vs 目标版本 差距分析

### 2.1 核心差距

| 维度 | 当前版本 | 目标版本 | 差距 |
|------|----------|----------|------|
| **Agent 定义** | 硬编码 3 种类型 | 可配置/可扩展 | 🔴 大 |
| **决策机制** | 固定公式 | 可学习/可演化 | 🔴 大 |
| **交流机制** | 无 | Agent 间对话/观察 | 🔴 大 |
| **记忆系统** | 无 | 历史互动记录 | 🔴 大 |
| **学习算法** | 无 | 强化学习/遗传算法 | 🔴 大 |
| **市场机制** | 简化价格更新 | 订单簿/撮合 | 🟡 中 |
| **适用场景** | 仅金融 | 通用多 Agent 平台 | 🔴 大 |
| **学术严谨性** | 初步验证 | 可发表水平 | 🟡 中 |

### 2.2 硬编码问题清单

```python
# ❌ 当前硬编码
agent_types = ['retail', 'institution', 'hedge_fund']
agent_weights = [0.6, 0.3, 0.1]
herding_strength = 0.3
overconfidence = 0.2
loss_aversion = 2.5
omega = 0.000001
alpha = 0.1
beta = 0.85
```

**问题：**
1. 无法动态调整 Agent 类型
2. 无法添加新 Agent 类型
3. 行为参数无法从数据学习
4. 无法做敏感性分析（除非改代码）

---

## 三、Agent Monte Carlo 能否保留？

### 3.1 可以保留的部分 ✅

| 模块 | 保留理由 | 修改需求 |
|------|----------|----------|
| **Traditional MC** | 作为基准对照 | 无需修改 |
| **风险指标计算** | 通用金融指标 | 无需修改 |
| **Streamlit UI 框架** | 交互设计有效 | 重构为通用 UI |
| **可视化图表** | 对比展示有效 | 扩展为多场景 |
| **回测框架** | 基础设施 | 扩展数据源 |

### 3.2 需要重构的部分 ⚠️

| 模块 | 问题 | 重构方案 |
|------|------|----------|
| `generate_agent_mc_paths()` | 硬编码 | 拆分为 Agent 类 + 环境 |
| 行为参数 | 写死 | 配置文件/从数据学习 |
| Agent 类型 | 固定 3 种 | 插件式架构 |
| 价格更新 | 简化公式 | 订单驱动/做市商 |

### 3.3 需要新增的部分 🆕

| 模块 | 功能 | 优先级 |
|------|------|--------|
| `Agent` 基类 | 统一接口 | P0 |
| `Memory` 系统 | 历史记录 | P0 |
| `Communication` | Agent 交流 | P1 |
| `Learning` | 策略更新 | P1 |
| `Market` | 订单簿/撮合 | P0 |
| `Config` | 可配置参数 | P0 |

---

## 四、演进路线

### 4.1 阶段 1：去硬编码化（2 周）

**目标：** 让当前版本可配置、可扩展

**任务：**
```
1. 创建 Agent 基类
   - 定义统一接口 (observe, decide, act)
   - 支持子类继承

2. 配置文件支持
   - YAML/JSON 配置 Agent 类型和参数
   - 支持运行时加载

3. 参数敏感性分析
   - 批量运行不同参数组合
   - 输出敏感性热力图

4. 数据校准
   - 从历史数据学习行为参数
   - 最小化模拟 vs 真实差异
```

**交付物：**
- `src/agents/base.py` - Agent 基类
- `configs/agents.yaml` - Agent 配置
- `scripts/calibrate.py` - 参数校准

---

### 4.2 阶段 2：核心能力建设（4 周）

**目标：** 实现真正的多 Agent 系统

**任务：**
```
1. 记忆系统
   - 每个 Agent 有独立记忆
   - 记录历史价格、交易、观察

2. 交流机制
   - Agent 可观察其他 Agent 行为
   - 可选：直接对话（基于 LLM）
   - 社交网络结构

3. 学习算法
   - 强化学习（Q-learning/Policy Gradient）
   - 或：遗传算法（策略演化）
   - 定期更新策略

4. 市场机制
   - 订单簿实现
   - 撮合引擎
   - 价格发现
```

**交付物：**
- `src/agents/memory.py` - 记忆系统
- `src/agents/communication.py` - 交流协议
- `src/agents/learning.py` - 学习算法
- `src/market/orderbook.py` - 订单簿

---

### 4.3 阶段 3：学术验证（4 周）

**目标：** 达到可发表水平

**任务：**
```
1. 实证检验
   - 校准：用 S&P 500 1980-2024
   - 验证：肥尾、波动率聚集、崩盘频率
   - 统计检验：KS 检验、自相关检验

2. 反事实分析
   - 改变 Agent 结构（散户比例）
   - 改变监管政策（做空限制）
   - 改变交易机制（T+0 vs T+1）

3. 论文写作
   - 文献综述
   - 方法论
   - 结果与讨论
   - 稳健性检验

4. 开源发布
   - GitHub 仓库整理
   - 文档完善
   - 示例 Notebook
```

**交付物：**
- `paper/main.tex` - 论文草稿
- `results/validation/` - 验证结果
- `experiments/counterfactual/` - 反事实分析

---

## 五、当前代码重构建议

### 5.1 立即可做的改进

```python
# ❌ 当前硬编码
def generate_agent_mc_paths(...):
    agent_types = ['retail', 'institution', 'hedge_fund']
    herding_strength = 0.3
    ...

# ✅ 改进后：配置驱动
class AgentMonteCarloConfig:
    agent_types: List[Dict]
    behavior_params: Dict
    market_params: Dict

class AgentSimulator:
    def __init__(self, config: AgentMonteCarloConfig):
        self.agents = self._create_agents(config)
        self.market = Market(config.market_params)
    
    def run(self, n_steps: int) -> Results:
        for t in range(n_steps):
            for agent in self.agents:
                observation = self.market.observe()
                action = agent.decide(observation)
                self.market.submit_order(action)
            self.market.clear()
        return self.market.get_results()
```

### 5.2 新的项目结构

```
agent-monte-carlo/
├── src/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base.py          # Agent 基类
│   │   ├── retail.py        # 散户 Agent
│   │   ├── institution.py   # 机构 Agent
│   │   ├── hedge_fund.py    # 对冲基金 Agent
│   │   ├── memory.py        # 记忆系统
│   │   └── learning.py      # 学习算法
│   ├── market/
│   │   ├── __init__.py
│   │   ├── orderbook.py     # 订单簿
│   │   ├── clearing.py      # 撮合引擎
│   │   └── price.py         # 价格发现
│   ├── config/
│   │   ├── __init__.py
│   │   ├── agent_config.py  # Agent 配置
│   │   └── market_config.py # 市场配置
│   ├── simulator.py         # 主模拟器（重构）
│   └── results.py           # 结果结构
├── configs/
│   ├── baseline.yaml        # 基准配置
│   ├── sensitivity/         # 敏感性分析配置
│   └── calibration/         # 校准配置
├── experiments/
│   ├── calibration.py       # 参数校准
│   ├── validation.py        # 模型验证
│   └── counterfactual.py    # 反事实分析
├── data/
│   ├── raw/                 # 原始数据
│   └── processed/           # 处理后的数据
├── results/
│   ├── baseline/            # 基准结果
│   └── sensitivity/         # 敏感性结果
├── paper/                   # 论文相关
├── app.py                   # Streamlit UI（重构）
└── tests/                   # 单元测试
```

---

## 六、决策建议

### 6.1 保留 Agent Monte Carlo 名称

**理由：**
- 品牌已建立
- 核心思想正确（Agent + MC）
- 只是实现需要完善

### 6.2 立即行动项

| 优先级 | 任务 | 预计时间 |
|--------|------|----------|
| P0 | 创建 Agent 基类 | 2 天 |
| P0 | 配置文件支持 | 2 天 |
| P0 | 参数敏感性框架 | 3 天 |
| P1 | 记忆系统设计 | 3 天 |
| P1 | 学习算法原型 | 5 天 |
| P2 | 订单簿实现 | 5 天 |

### 6.3 学术定位

**论文标题建议：**
> "Agent Monte Carlo: A Hybrid Framework for Endogenous Market Dynamics"

**目标期刊：**
- Journal of Finance
- Review of Financial Studies
- Journal of Financial Economics
- Management Science

**核心贡献：**
1. 方法论：传统 MC + ABM 的混合框架
2. 实证：重现多个市场异象
3. 政策：评估监管政策效果
4. 开源：可复制的研究

---

## 七、下一步

### 本周行动

1. **今天：** 确认本分析文档
2. **明天：** 创建 Agent 基类
3. **本周内：** 完成配置文件支持
4. **周末：** 运行第一个敏感性分析

### 本月目标

- ✅ 去硬编码化完成
- ✅ 记忆系统原型
- ✅ 初步校准结果

---

**结论：** 当前版本可以保留，但需要系统重构。核心思想（Agent + MC）是正确的，只是实现过于简化。通过去硬编码化、添加学习和交流机制，可以达到学术发表水平。

---

*Last updated: 2026-04-03*
