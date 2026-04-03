# Agent Monte Carlo v1.0 - 完整架构设计

**版本：** 1.0 (In Development)  
**日期：** 2026-04-03  
**状态：** 设计文档

---

## 一、项目愿景

构建一个**通用的多智能体模拟平台**，用于研究复杂适应系统中的涌现现象。金融市场的价格形成只是第一个应用场景。

### 核心目标

1. **学术严谨** - 可发表、可验证、可复制
2. **通用架构** - 不仅限于金融，支持多场景
3. **可扩展** - 插件式 Agent 设计
4. **数据驱动** - 参数从数据学习，非硬编码
5. **开源开放** - 完整文档、测试、示例

---

## 二、完整项目结构

```
agent-monte-carlo/
│
├── README.md                          # 项目说明（学术定位）
├── README_zh.md                       # 中文说明
├── LICENSE                            # MIT License
├── requirements.txt                   # Python 依赖
├── pyproject.toml                     # 项目配置（Poetry）
├── setup.py                           # 安装脚本
│
├── src/
│   └── agent_mc/
│       ├── __init__.py
│       │
│       ├── core/                      # 核心引擎
│       │   ├── __init__.py
│       │   ├── simulator.py           # 主模拟器
│       │   ├── environment.py         # 环境基类
│       │   ├── world.py               # 世界状态管理
│       │   └── clock.py               # 时间管理（离散/连续）
│       │
│       ├── agents/                    # Agent 系统
│       │   ├── __init__.py
│       │   ├── base.py                # Agent 基类
│       │   ├── registry.py            # Agent 注册表
│       │   ├── memory.py              # 记忆系统
│       │   ├── perception.py          # 感知系统
│       │   ├── decision.py            # 决策引擎
│       │   ├── learning.py            # 学习算法
│       │   └── communication.py       # 交流协议
│       │
│       ├── agents/types/              # Agent 类型（插件式）
│       │   ├── __init__.py
│       │   ├── random_agent.py        # 随机交易 Agent
│       │   ├── momentum_agent.py      # 动量交易 Agent
│       │   ├── value_agent.py         # 价值投资 Agent
│       │   ├── herd_agent.py          # 羊群 Agent
│       │   ├── market_maker.py        # 做市商 Agent
│       │   └── llm_agent.py           # LLM 驱动 Agent (v1.1)
│       │
│       ├── market/                    # 市场机制
│       │   ├── __init__.py
│       │   ├── orderbook.py           # 订单簿
│       │   ├── matching.py            # 撮合引擎
│       │   ├── price.py               # 价格发现
│       │   ├── clearing.py            # 清算结算
│       │   └── circuit_breaker.py     # 熔断机制
│       │
│       ├── orders/                    # 订单系统
│       │   ├── __init__.py
│       │   ├── base.py                # 订单基类
│       │   ├── limit_order.py         # 限价单
│       │   ├── market_order.py        # 市价单
│       │   └── stop_order.py          # 止损单
│       │
│       ├── config/                    # 配置系统
│       │   ├── __init__.py
│       │   ├── base.py                # 配置基类
│       │   ├── agent_config.py        # Agent 配置
│       │   ├── market_config.py       # 市场配置
│       │   └── simulation_config.py   # 模拟配置
│       │
│       ├── data/                      # 数据系统
│       │   ├── __init__.py
│       │   ├── loader.py              # 数据加载
│       │   ├── calibration.py         # 参数校准
│       │   ├── sources/               # 数据源
│       │   │   ├── yahoo.py           # Yahoo Finance
│       │   │   ├── fred.py            # FRED 经济数据
│       │   │   └── synthetic.py       # 合成数据生成
│       │   └── validators.py          # 数据验证
│       │
│       ├── metrics/                   # 指标计算
│       │   ├── __init__.py
│       │   ├── risk.py                # 风险指标（VaR, ES）
│       │   ├── statistical.py         # 统计指标（峰度、偏度）
│       │   ├── market.py              # 市场指标（波动率、流动性）
│       │   └── agent_metrics.py       # Agent 表现指标
│       │
│       ├── results/                   # 结果管理
│       │   ├── __init__.py
│       │   ├── recorder.py            # 数据记录
│       │   ├── analyzer.py            # 结果分析
│       │   └── exporter.py            # 导出（CSV/JSON/Parquet）
│       │
│       └── utils/                     # 工具函数
│           ├── __init__.py
│           ├── logging.py             # 日志配置
│           ├── random.py              # 随机数生成
│           └── parallel.py            # 并行计算
│
├── configs/                           # 配置文件
│   ├── default.yaml                   # 默认配置
│   ├── agents/                        # Agent 配置
│   │   ├── baseline.yaml              # 基准情景
│   │   ├── retail_dominated.yaml      # 散户主导
│   │   ├── institution_dominated.yaml # 机构主导
│   │   └── diverse.yaml               # 高度多样化
│   ├── markets/                       # 市场配置
│   │   ├── stock_market.yaml          # 股票市场
│   │   ├── crypto_market.yaml         # 加密货币市场
│   │   └── fx_market.yaml             # 外汇市场
│   └── experiments/                   # 实验配置
│       ├── calibration.yaml           # 校准实验
│       ├── sensitivity.yaml           # 敏感性分析
│       └── counterfactual.yaml        # 反事实分析
│
├── experiments/                       # 实验脚本
│   ├── __init__.py
│   ├── run_simulation.py              # 运行模拟
│   ├── calibration/                   # 参数校准
│   │   ├── calibrate_agents.py        # 校准 Agent 参数
│   │   └── calibrate_market.py        # 校准市场参数
│   ├── validation/                    # 模型验证
│   │   ├── validate_stylized_facts.py # 验证典型事实
│   │   ├── statistical_tests.py       # 统计检验
│   │   └── benchmark_comparison.py    # 基准对比
│   ├── sensitivity/                   # 敏感性分析
│   │   ├── agent_composition.py       # Agent 构成敏感性
│   │   ├── behavior_params.py         # 行为参数敏感性
│   │   └── market_rules.py            # 市场规则敏感性
│   └── counterfactual/                # 反事实分析
│       ├── policy_changes.py          # 政策变化（如做空限制）
│       ├── mechanism_design.py        # 机制设计（如 T+0 vs T+1）
│       └── shock_analysis.py          # 冲击分析
│
├── data/                              # 数据目录
│   ├── raw/                           # 原始数据
│   │   ├── sp500/                     # S&P 500 数据
│   │   ├── vix/                       # VIX 指数
│   │   └── treasury/                  # 国债利率
│   ├── processed/                     # 处理后的数据
│   │   ├── returns/                   # 收益率序列
│   │   └── calibrated_params/         # 校准后的参数
│   └── external/                      # 外部数据
│       └── [其他数据源]
│
├── results/                           # 模拟结果
│   ├── baseline/                      # 基准情景结果
│   ├── sensitivity/                   # 敏感性分析结果
│   ├── counterfactual/                # 反事实分析结果
│   └── paper/                         # 论文用图表数据
│
├── paper/                             # 学术论文
│   ├── main.tex                       # 论文主文件（LaTeX）
│   ├── sections/                      # 论文章节
│   │   ├── introduction.tex
│   │   ├── literature_review.tex
│   │   ├── model.tex
│   │   ├── calibration.tex
│   │   ├── results.tex
│   │   └── conclusion.tex
│   ├── figures/                       # 论文图表
│   │   ├── architecture.pdf
│   │   ├── calibration_results.pdf
│   │   └── validation_results.pdf
│   ├── tables/                        # 论文表格
│   ├── references.bib                 # 参考文献
│   └── supplements/                   # 补充材料
│       ├── additional_results.pdf
│       └── robustness_checks.pdf
│
├── notebooks/                         # Jupyter Notebooks
│   ├── 01_data_exploration.ipynb      # 数据探索
│   ├── 02_calibration_demo.ipynb      # 校准演示
│   ├── 03_simulation_demo.ipynb       # 模拟演示
│   ├── 04_validation_demo.ipynb       # 验证演示
│   └── 05_counterfactual_demo.ipynb   # 反事实演示
│
├── tests/                             # 单元测试
│   ├── __init__.py
│   ├── test_agents/                   # Agent 测试
│   │   ├── test_base_agent.py
│   │   ├── test_memory.py
│   │   └── test_learning.py
│   ├── test_market/                   # 市场测试
│   │   ├── test_orderbook.py
│   │   ├── test_matching.py
│   │   └── test_price_discovery.py
│   ├── test_core/                     # 核心引擎测试
│   │   ├── test_simulator.py
│   │   └── test_environment.py
│   └── integration/                   # 集成测试
│       ├── test_full_simulation.py
│       └── test_calibration.py
│
├── docs/                              # 文档
│   ├── ARCHITECTURE.md                # 架构设计（本文档）
│   ├── PROJECT_ANALYSIS.md            # 项目分析（已创建）
│   ├── API_REFERENCE.md               # API 参考
│   ├── TUTORIAL.md                    # 教程
│   ├── CONTRIBUTING.md                # 贡献指南
│   └── CHANGELOG.md                   # 变更日志
│
├── scripts/                           # 辅助脚本
│   ├── setup_environment.sh           # 环境设置
│   ├── download_data.py               # 下载数据
│   ├── run_all_experiments.sh         # 运行所有实验
│   └── generate_paper_figures.py      # 生成论文图表
│
└── app.py                             # Streamlit UI（重构后）
```

---

## 三、核心模块详细设计

### 3.1 Agent 基类设计

```python
# src/agent_mc/agents/base.py

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import numpy as np

@dataclass
class AgentState:
    """Agent 内部状态"""
    cash: float = 100000.0        # 现金
    holdings: Dict[str, int] = field(default_factory=dict)  # 持仓
    wealth: float = 100000.0      # 总财富
    
@dataclass
class AgentMemory:
    """Agent 记忆"""
    price_history: List[float] = field(default_factory=list)
    trade_history: List[Dict] = field(default_factory=list)
    observation_history: List[Dict] = field(default_factory=list)
    
class Agent(ABC):
    """Agent 抽象基类"""
    
    def __init__(
        self,
        agent_id: str,
        agent_type: str,
        config: Dict[str, Any],
        seed: Optional[int] = None
    ):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.config = config
        self.state = AgentState()
        self.memory = AgentMemory()
        self.rng = np.random.default_rng(seed)
        
    @abstractmethod
    def perceive(self, observation: Dict[str, Any]) -> None:
        """感知环境"""
        pass
    
    @abstractmethod
    def decide(self) -> Dict[str, Any]:
        """做出决策"""
        pass
    
    @abstractmethod
    def act(self, decision: Dict[str, Any]) -> Any:
        """执行动作"""
        pass
    
    def learn(self, reward: float) -> None:
        """从结果中学习（可选）"""
        pass
    
    def update_state(self, trade_result: Dict) -> None:
        """更新状态"""
        pass
```

---

### 3.2 记忆系统设计

```python
# src/agent_mc/agents/memory.py

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from collections import deque
import numpy as np

@dataclass
class Experience:
    """单次经验"""
    timestamp: int
    observation: Dict[str, Any]
    action: Dict[str, Any]
    reward: float
    next_observation: Dict[str, Any]

class AgentMemory:
    """
    Agent 记忆系统
    
    功能：
    1. 存储历史观察、动作、奖励
    2. 支持不同时间尺度（短期/长期）
    3. 支持经验回放（用于强化学习）
    4. 支持记忆衰减（近期更重要）
    """
    
    def __init__(
        self,
        max_size: int = 10000,
        decay_factor: float = 1.0  # 记忆衰减因子
    ):
        self.max_size = max_size
        self.decay_factor = decay_factor
        
        # 短期记忆（deque 实现）
        self.short_term = deque(maxlen=max_size)
        
        # 长期记忆（关键事件）
        self.long_term: List[Experience] = []
        
        # 统计摘要
        self.statistics = {
            'total_trades': 0,
            'total_reward': 0.0,
            'win_rate': 0.0,
        }
    
    def add_experience(self, experience: Experience) -> None:
        """添加经验"""
        self.short_term.append(experience)
        
        # 重要事件存入长期记忆
        if abs(experience.reward) > self.config.get('important_threshold', 0.1):
            self.long_term.append(experience)
    
    def get_recent_observations(self, n: int = 10) -> List[Dict]:
        """获取最近 n 次观察"""
        return [exp.observation for exp in list(self.short_term)[-n:]]
    
    def sample_batch(self, batch_size: int = 32) -> List[Experience]:
        """经验回放采样"""
        import random
        return random.sample(list(self.short_term), batch_size)
    
    def get_statistics(self) -> Dict[str, float]:
        """获取记忆统计"""
        if not self.short_term:
            return self.statistics
        
        rewards = [exp.reward for exp in self.short_term]
        self.statistics['total_reward'] = sum(rewards)
        self.statistics['win_rate'] = np.mean([r > 0 for r in rewards])
        
        return self.statistics
```

---

### 3.3 学习算法设计

```python
# src/agent_mc/agents/learning.py

from abc import ABC, abstractmethod
from typing import Dict, Any, List
import numpy as np

class LearningAlgorithm(ABC):
    """学习算法基类"""
    
    @abstractmethod
    def update(self, experience: Dict) -> None:
        pass
    
    @abstractmethod
    def get_policy(self) -> Dict:
        pass

class QLearning(LearningAlgorithm):
    """
    Q-Learning 实现
    
    用于 Agent 从交易经验中学习最优策略
    """
    
    def __init__(
        self,
        state_space: List[str],
        action_space: List[str],
        learning_rate: float = 0.1,
        discount_factor: float = 0.99,
        epsilon: float = 0.1
    ):
        self.state_space = state_space
        self.action_space = action_space
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
        
        # Q 表
        self.q_table = {}
    
    def get_q_value(self, state: str, action: str) -> float:
        """获取 Q 值"""
        return self.q_table.get((state, action), 0.0)
    
    def update(self, experience: Dict) -> None:
        """
        更新 Q 值
        
        Q(s,a) ← Q(s,a) + α[r + γ·max_a' Q(s',a') - Q(s,a)]
        """
        state = experience['state']
        action = experience['action']
        reward = experience['reward']
        next_state = experience['next_state']
        
        # 当前 Q 值
        current_q = self.get_q_value(state, action)
        
        # 下一状态最大 Q 值
        max_next_q = max(
            self.get_q_value(next_state, a) 
            for a in self.action_space
        )
        
        # Q 值更新
        new_q = current_q + self.lr * (reward + self.gamma * max_next_q - current_q)
        self.q_table[(state, action)] = new_q
    
    def get_policy(self) -> Dict:
        """获取当前策略（贪婪策略）"""
        policy = {}
        for state in self.state_space:
            q_values = [self.get_q_value(state, a) for a in self.action_space]
            best_action = self.action_space[np.argmax(q_values)]
            policy[state] = best_action
        return policy

class EvolutionaryStrategy(LearningAlgorithm):
    """
    演化策略
    
    用于群体层面的策略优化
    """
    
    def __init__(
        self,
        population_size: int = 100,
        mutation_rate: float = 0.1,
        elite_ratio: float = 0.2
    ):
        self.pop_size = population_size
        self.mutation_rate = mutation_rate
        self.elite_ratio = elite_ratio
        
        # 种群
        self.population = []
        self.fitness = []
    
    def evolve(self) -> List[Dict]:
        """演化一代"""
        # 选择精英
        elite_count = int(self.pop_size * self.elite_ratio)
        elite_indices = np.argsort(self.fitness)[-elite_count:]
        elites = [self.population[i] for i in elite_indices]
        
        # 生成新一代
        new_population = elites.copy()
        while len(new_population) < self.pop_size:
            parent = self.rng.choice(elites)
            child = self.mutate(parent)
            new_population.append(child)
        
        self.population = new_population
        return self.population
    
    def mutate(self, params: Dict) -> Dict:
        """变异操作"""
        mutated = params.copy()
        for key in mutated:
            if isinstance(mutated[key], (int, float)):
                mutated[key] += self.rng.normal(0, self.mutation_rate)
        return mutated
```

---

### 3.4 订单簿设计

```python
# src/agent_mc/market/orderbook.py

from typing import List, Dict, Optional
from dataclasses import dataclass, field
from collections import defaultdict
import heapq

@dataclass
class Order:
    """订单"""
    order_id: str
    agent_id: str
    side: str  # 'buy' or 'sell'
    price: float
    quantity: int
    timestamp: int
    order_type: str = 'limit'  # 'limit', 'market', 'stop'

class OrderBook:
    """
    订单簿实现
    
    功能：
    1. 维护买单和卖单队列
    2. 价格优先、时间优先匹配
    3. 支持多种订单类型
    4. 记录交易历史
    """
    
    def __init__(self, tick_size: float = 0.01):
        self.tick_size = tick_size
        
        # 买单（价格降序）- 用负数实现最大堆
        self.bids: Dict[float, List[Order]] = defaultdict(list)
        
        # 卖单（价格升序）
        self.asks: Dict[float, List[Order]] = defaultdict(list)
        
        # 交易历史
        self.trades: List[Dict] = []
        
        # 当前价格
        self.last_price: Optional[float] = None
    
    def add_order(self, order: Order) -> List[Dict]:
        """
        添加订单，返回成交列表
        """
        trades = []
        
        if order.side == 'buy':
            trades = self._match_buy_order(order)
        else:
            trades = self._match_sell_order(order)
        
        # 记录未成交部分
        if order.quantity > 0:
            self._add_remaining_order(order)
        
        return trades
    
    def _match_buy_order(self, buy_order: Order) -> List[Dict]:
        """匹配买单"""
        trades = []
        
        # 从最低卖价开始匹配
        for ask_price in sorted(self.asks.keys()):
            if ask_price > buy_order.price:
                break
            
            for sell_order in self.asks[ask_price][:]:
                if buy_order.quantity <= 0:
                    break
                
                # 成交
                trade_qty = min(buy_order.quantity, sell_order.quantity)
                trade = {
                    'price': ask_price,
                    'quantity': trade_qty,
                    'buyer_id': buy_order.agent_id,
                    'seller_id': sell_order.agent_id,
                    'timestamp': buy_order.timestamp
                }
                trades.append(trade)
                
                # 更新订单
                buy_order.quantity -= trade_qty
                sell_order.quantity -= trade_qty
                
                if sell_order.quantity == 0:
                    self.asks[ask_price].remove(sell_order)
        
        return trades
    
    def get_best_bid(self) -> Optional[float]:
        """获取最优买价"""
        if not self.bids:
            return None
        return max(self.bids.keys())
    
    def get_best_ask(self) -> Optional[float]:
        """获取最优卖价"""
        if not self.asks:
            return None
        return min(self.asks.keys())
    
    def get_mid_price(self) -> Optional[float]:
        """获取中间价"""
        best_bid = self.get_best_bid()
        best_ask = self.get_best_ask()
        
        if best_bid and best_ask:
            return (best_bid + best_ask) / 2
        return self.last_price
    
    def get_spread(self) -> Optional[float]:
        """获取买卖价差"""
        best_bid = self.get_best_bid()
        best_ask = self.get_best_ask()
        
        if best_bid and best_ask:
            return best_ask - best_bid
        return None
```

---

### 3.5 撮合引擎设计

```python
# src/agent_mc/market/matching.py

from typing import List, Dict
from dataclasses import dataclass

@dataclass
class Trade:
    """成交记录"""
    trade_id: str
    price: float
    quantity: int
    buyer_id: str
    seller_id: str
    timestamp: int
    buyer_order_id: str
    seller_order_id: str

class MatchingEngine:
    """
    撮合引擎
    
    原则：
    1. 价格优先：买单高价优先，卖单低价优先
    2. 时间优先：同价格先提交优先
    3. 数量优先：大单优先（可选）
    """
    
    def __init__(self):
        self.trade_counter = 0
        self.trades: List[Trade] = []
    
    def execute_trades(self, orderbook, new_order) -> List[Trade]:
        """
        执行撮合
        
        流程：
        1. 接收新订单
        2. 检查是否有可匹配的订单
        3. 按优先级撮合
        4. 记录成交
        5. 更新订单簿
        """
        trades = []
        
        # 添加订单并获取成交
        matched_trades = orderbook.add_order(new_order)
        
        # 转换为 Trade 对象
        for trade_data in matched_trades:
            self.trade_counter += 1
            trade = Trade(
                trade_id=f"T{self.trade_counter:08d}",
                price=trade_data['price'],
                quantity=trade_data['quantity'],
                buyer_id=trade_data['buyer_id'],
                seller_id=trade_data['seller_id'],
                timestamp=trade_data['timestamp'],
                buyer_order_id=new_order.order_id if new_order.side == 'buy' else trade_data.get('order_id'),
                seller_order_id=new_order.order_id if new_order.side == 'sell' else trade_data.get('order_id')
            )
            trades.append(trade)
            self.trades.append(trade)
        
        return trades
```

---

## 四、模拟流程

### 4.1 主模拟循环

```python
# src/agent_mc/core/simulator.py

class AgentMonteCarloSimulator:
    """
    Agent Monte Carlo 主模拟器
    
    模拟流程：
    1. 初始化环境和 Agent
    2. 加载历史数据（用于校准）
    3. 运行模拟循环
    4. 记录结果
    5. 分析输出
    """
    
    def __init__(self, config: SimulationConfig):
        self.config = config
        self.environment = Environment(config)
        self.agents = self._create_agents(config)
        self.market = Market(config)
        self.recorder = DataRecorder(config)
    
    def run(self, n_steps: int) -> SimulationResults:
        """运行模拟"""
        
        # 初始化
        self._initialize()
        
        # 主循环
        for t in range(n_steps):
            # 1. 环境观察
            observation = self.environment.get_observation()
            
            # 2. Agent 感知
            for agent in self.agents:
                agent.perceive(observation)
            
            # 3. Agent 决策
            orders = []
            for agent in self.agents:
                decision = agent.decide()
                order = agent.act(decision)
                if order:
                    orders.append(order)
            
            # 4. 市场撮合
            for order in orders:
                trades = self.market.match(order)
                
                # 5. 更新 Agent 状态
                for trade in trades:
                    buyer = self._get_agent(trade.buyer_id)
                    seller = self._get_agent(trade.seller_id)
                    buyer.update_state(trade)
                    seller.update_state(trade)
            
            # 6. 记录数据
            self.recorder.record(t, self.market.get_state())
            
            # 7. Agent 学习（定期）
            if t % self.config.learning_interval == 0:
                for agent in self.agents:
                    agent.learn()
        
        # 分析结果
        results = self._analyze_results()
        return results
```

---

## 五、配置文件示例

### 5.1 Agent 配置

```yaml
# configs/agents/baseline.yaml

agents:
  - type: random_agent
    count: 20
    proportion: 0.2
    params:
      trade_probability: 0.1
      order_size_mean: 10
      order_size_std: 5
  
  - type: momentum_agent
    count: 30
    proportion: 0.3
    params:
      lookback_window: 20
      entry_threshold: 0.02
      exit_threshold: 0.01
      learning_rate: 0.05
  
  - type: value_agent
    count: 30
    proportion: 0.3
    params:
      fundamental_value: 100
      mean_reversion_speed: 0.1
      confidence_threshold: 0.05
  
  - type: herd_agent
    count: 20
    proportion: 0.2
    params:
      herding_strength: 0.5
      observation_window: 10
      imitation_probability: 0.7

learning:
  algorithm: q_learning  # q_learning, evolutionary, none
  learning_rate: 0.1
  discount_factor: 0.99
  exploration_rate: 0.1
```

### 5.2 市场配置

```yaml
# configs/markets/stock_market.yaml

market:
  tick_size: 0.01
  lot_size: 1
  initial_price: 100.0
  
  # 交易规则
  trading_hours:
    open: 9
    close: 16
    timezone: EST
  
  # 涨跌停限制
  price_limits:
    enabled: true
    limit_up: 0.10
    limit_down: 0.10
  
  # 熔断机制
  circuit_breaker:
    enabled: true
    thresholds: [0.07, 0.13, 0.20]
    cooling_off_period: 900  # seconds
  
  # 交易费用
  fees:
    maker_fee: 0.0001
    taker_fee: 0.0002
```

---

## 六、开发计划

### 阶段 1：核心框架（2 周）

**Week 1:**
- [ ] Agent 基类实现
- [ ] 记忆系统实现
- [ ] 配置文件加载

**Week 2:**
- [ ] 订单簿实现
- [ ] 撮合引擎实现
- [ ] 主模拟循环

**交付物：** 可运行的最小系统

---

### 阶段 2：Agent 类型（2 周）

**Week 3:**
- [ ] Random Agent
- [ ] Momentum Agent
- [ ] Value Agent

**Week 4:**
- [ ] Herd Agent
- [ ] Market Maker
- [ ] 学习算法集成

**交付物：** 5 种 Agent 类型

---

### 阶段 3：校准与验证（2 周）

**Week 5:**
- [ ] 数据加载器
- [ ] 参数校准脚本
- [ ] 统计指标计算

**Week 6:**
- [ ] 典型事实验证
- [ ] 敏感性分析框架
- [ ] 结果可视化

**交付物：** 校准工具 + 验证结果

---

### 阶段 4：学术写作（2 周）

**Week 7:**
- [ ] 实验设计
- [ ] 运行所有实验
- [ ] 生成论文图表

**Week 8:**
- [ ] 论文初稿
- [ ] 补充材料
- [ ] GitHub 整理

**交付物：** 论文草稿 + 开源仓库

---

## 七、技术栈

| 类别 | 技术 |
|------|------|
| **核心语言** | Python 3.11+ |
| **数值计算** | NumPy, Pandas |
| **统计分析** | SciPy, Statsmodels |
| **机器学习** | Scikit-learn, PyTorch (可选) |
| **数据源** | yfinance, FRED API |
| **可视化** | Plotly, Matplotlib |
| **Web UI** | Streamlit |
| **测试** | pytest |
| **文档** | Sphinx, MkDocs |
| **打包** | Poetry, setuptools |

---

## 八、关键设计决策

### 8.1 为什么用离散时间？

- 简化实现
- 易于复现
- 符合日度/分钟度数据

### 8.2 为什么订单簿驱动？

- 真实市场机制
- 价格内生涌现
- 支持多种订单类型

### 8.3 为什么插件式 Agent？

- 易于扩展
- 便于对比不同 Agent 类型
- 支持用户自定义

### 8.4 为什么配置驱动？

- 参数可追溯
- 实验可复现
- 敏感性分析方便

---

**下一步：** 开始实现阶段 1 - 核心框架！
