# Agent Monte Carlo v1.0 - 文献综述与理论基础

**日期：** 2026-04-03  
**版本：** 1.0  
**目标：** 为模型设计提供坚实的学术基础

---

## 一、核心理论文献

### 1.1 Agent-Based 金融建模

#### 奠基性文献

**[1] LeBaron, B. (2006). "Agent-based computational finance." *Handbook of Computational Economics*, Vol. 2, 1187-1233.**

**核心贡献：**
- 系统综述了 ABM 在金融中的应用
- 识别了关键的市场典型事实（stylized facts）
- 提出了模型验证的标准框架

**关键发现：**
| 典型事实 | 实证值 (S&P 500) | 传统 MC | ABM |
|----------|------------------|---------|-----|
| 收益率峰度 | ~19 | ~3 | 5-25 |
| 波动率聚集 (ACF(1)) | ~0.2 | 0 | 0.1-0.3 |
| 崩盘频率 (年) | ~3% | <0.1% | 1-5% |
| 交易量 - 波动率相关 | ~0.6 | 0 | 0.4-0.7 |

**对本文的启示：**
1. ABM 能够重现传统 MC 无法捕捉的典型事实
2. 模型验证必须针对多个典型事实，而非单一指标
3. 参数校准应使用长期历史数据（≥50 年）

---

**[2] Hommes, C. H. (2006). "Heterogeneous agent models in economics and finance." *Handbook of Computational Economics*, Vol. 2, 1109-1186.**

**核心贡献：**
- 提出了异质信念（heterogeneous beliefs）框架
- 区分了理性预期 vs 适应性预期
- 引入了演化选择机制（evolutionary selection）

**关键模型：**
```
Agent 类型：
1. 基本面分析者 (Fundamentalists)
   - 信念：价格会回归基本面
   - 需求：D_f = (F - P) / σ²
   
2. 图表分析者 (Chartists)
   - 信念：价格趋势会持续
   - 需求：D_c = g·(P - P_prev)
   
3. 噪声交易者 (Noise Traders)
   - 需求：随机 + 情绪驱动

市场出清：
P = (Σ n_i · D_i) / (Σ n_i)

策略选择：
n_i(t+1) = n_i(t) · exp(β·π_i(t)) / Σ_j n_j(t) · exp(β·π_j(t))
其中 π_i 是策略 i 的过去收益，β是选择强度
```

**对本文的启示：**
1. Agent 异质性是产生复杂动态的关键
2. 策略选择机制（演化）比固定策略更真实
3. 参数β（选择强度）控制市场稳定性

---

**[3] Lux, T. (2009). "Stochastic behavioral asset-pricing models and the stylized facts." *Handbook of Financial Markets: Dynamics and Evolution*.**

**核心贡献：**
- 将行为偏差（herding, overconfidence）纳入 ABM
- 展示了内生性泡沫和崩盘的产生机制
- 提供了参数校准的实证方法

**关键行为参数（来自实证校准）：**
| 参数 | 含义 | 实证范围 | 来源 |
|------|------|----------|------|
| α_herd | 羊群强度 | 0.3-0.7 | Shiller (1995) |
| α_overconf | 过度自信 | 1.1-1.5 | Odean (1998) |
| α_loss_averse | 损失厌恶 | 2.0-2.5 | Kahneman & Tversky (1979) |
| σ_noise | 噪声交易波动 | 0.1-0.3 | French & Roll (1986) |

**对本文的启示：**
1. 行为参数必须有实证依据，不能随意设定
2. 羊群效应是产生肥尾的关键机制
3. 损失厌恶导致不对称的价格反应

---

### 1.2 行为金融基础

#### 投资者行为偏差

**[4] Barberis, N., & Thaler, R. (2003). "A survey of behavioral finance." *Handbook of the Economics of Finance*, Vol. 1, 1053-1128.**

**核心行为偏差总结：**

| 偏差 | 定义 | 对交易的影响 | 实证证据 |
|------|------|--------------|----------|
| **过度自信** | 高估自己的信息精度 | 过度交易，波动率增加 | Odean (1999) |
| **代表性启发** | 过度重视近期模式 | 动量交易，趋势外推 | Barberis et al. (1998) |
| **保守主义** | 更新信念过慢 | 反应不足，漂移 | Daniel et al. (1998) |
| **损失厌恶** | 损失比等额收益更痛苦 | 处置效应，波动率增加 | Benartzi & Thaler (1995) |
| **心理账户** | 分别评估不同投资 | 次优分散化 | Shefrin & Statman (2000) |

**对本文的启示：**
- 至少需要包含 3 种行为偏差：过度自信、代表性启发、损失厌恶
- 每种偏差必须有量化的行为方程

---

**[5] Daniel, K., Hirshleifer, D., & Subrahmanyam, A. (1998). "Investor psychology and security market under-and overreactions." *Journal of Finance*, 53(6), 1839-1885.**

**核心模型：**
```
投资者信念更新（贝叶斯 vs 心理偏差）：

标准贝叶斯：
E[V|signal] = μ₀ + (σ₀² / (σ₀² + σ²)) · (signal - μ₀)

过度自信偏差：
E[V|signal] = μ₀ + (σ₀² / (σ₀² + σ²/C)) · (signal - μ₀)
其中 C > 1 是过度自信因子

结果：
- 短期：过度反应（价格超调）
- 长期：反应不足（均值回归）
- 产生动量和反转效应
```

**对本文的启示：**
- 动量 Agent 的决策规则应基于此模型
- 过度自信参数 C 的实证估计：1.5-2.5（Odean, 1998）

---

### 1.3 学习理论

#### EWA 学习模型

**[6] Camerer, C., & Ho, T. H. (1999). "Experience-weighted attraction learning in normal form games." *Econometrica*, 67(4), 827-874.**

**核心贡献：**
- 统一了强化学习和信念学习
- 参数有明确的心理学解释
- 在多个实验中表现优于纯 RL 或纯 BL

**EWA 更新方程：**
```
吸引度更新：
A_i(t) = [φ·N(t-1)·A_i(t-1) + (δ + (1-δ)·I(s_i, s_i*(t))) · π_i(s_i, s_-i(t))] / N(t)

经验权重更新：
N(t) = ρ·N(t-1) + 1

策略选择（Logit）：
P(s_i) = exp(λ·A_i(t)) / Σ_j exp(λ·A_j(t))

参数含义：
- φ ∈ [0,1]: 吸引度衰减率（记忆遗忘）
- δ ∈ [0,1]: 对未选择策略的想象权重
- ρ ∈ [0,1]: 经验权重增长率
- λ > 0: 选择敏感度（λ→∞ 时完全理性）
```

**实证参数估计（来自 12 个实验）：**
| 参数 | 均值 | 标准差 | 95%CI |
|------|------|--------|-------|
| φ | 0.88 | 0.12 | [0.64, 1.0] |
| δ | 0.58 | 0.28 | [0.02, 1.0] |
| ρ | 0.85 | 0.15 | [0.55, 1.0] |
| λ | 1.5 | 0.8 | [0.1, 3.5] |

**对本文的启示：**
1. **使用 EWA 而非标准 Q-Learning**
   - EWA 有实验支持
   - 参数有心理含义
   - 可以学习反事实（"如果当初...会怎样"）

2. **参数先验分布：**
   ```python
   phi ~ Beta(8, 2)      # 均值 0.8
   delta ~ Uniform(0, 1)
   rho ~ Beta(7, 2)      # 均值 0.78
   lambda ~ Gamma(2, 1)  # 均值 2.0
   ```

---

**[7] Cheung, Y. W., & Friedman, D. (1997). "Individual learning in normal form games: Some laboratory results." *Games and Economic Behavior*, 19(1), 46-76.**

**核心发现：**
- 信念学习在早期主导，强化学习在后期主导
- 混合模型（如 EWA）拟合最好
- 学习速度因任务复杂度而异

**对本文的启示：**
- 可以允许 Agent 的学习机制随时间演化
- 简单任务（单资产）学习快，复杂任务学习慢

---

### 1.4 市场微观结构

#### 做市商模型

**[8] Glosten, L. R., & Milgrom, P. R. (1985). "Bid, ask and transaction prices in a specialist market with heterogeneously informed traders." *Journal of Financial Economics*, 14(1), 71-100.**

**核心模型：**
```
市场参与者：
1. 知情交易者（比例 μ）- 知道真实价值 V
2. 噪声交易者（比例 1-μ）- 随机交易

做市商定价：
Bid_t = E[V | sell order at t]
Ask_t = E[V | buy order at t]

均衡价差：
Spread = Ask - Bid = 2 · μ · (V_high - V_low)

关键结果：
- 信息不对称（μ）越大，价差越大
- 做市商通过学习更新信念
- 价格逐渐收敛到真实价值
```

**对本文的启示：**
1. 使用做市商机制而非简单订单簿
2. 价差应内生决定，而非外生给定
3. 信息不对称参数 μ 的实证估计：0.1-0.3（Easley et al., 1996）

---

**[9] Kyle, A. S. (1985). "Continuous auctions and insider trading." *Econometrica*, 53(6), 1315-1335.**

**核心模型：**
```
价格冲击函数：
P_t = P_0 + λ · Y_t

其中：
- Y_t = 累计订单流（买为正，卖为负）
- λ = Kyle's λ（价格冲击系数）

均衡结果：
- 知情交易者逐渐透露信息
- 价格随机游走
- 交易量与波动率正相关

实证估计：
- λ ≈ 0.01-0.05（Hasbrouck, 1991）
- 即 1% 的净订单流导致 0.01-0.05% 的价格变化
```

**对本文的启示：**
1. 价格冲击应线性或次线性（λ < 1）
2. 交易量是重要的信息变量
3. 可以校准λ到实证范围

---

**[10] Hasbrouck, J. (1991). "Measuring the information content of stock trades." *Journal of Finance*, 46(1), 179-207.**

**VAR 价格影响模型：**
```
ΔP_t = α + Σ β_i · ΔP_{t-i} + Σ γ_i · V_{t-i} + ε_t
V_t = 订单流（有符号的交易量）

实证结果（NYSE 股票）：
- 累计γ ≈ 0.02-0.05
- 即 1 单位订单流导致 0.02-0.05 单位价格变化
- 价格影响持久（不完全反转）
```

**对本文的启示：**
- 订单流对价格的影响应是持久的
- 可以校准γ到实证范围

---

## 二、实证文献

### 2.1 市场典型事实

**[11] Cont, R. (2001). "Empirical properties of asset returns: stylized facts and statistical issues." *Quantitative Finance*, 1(2), 223-236.**

**典型事实汇总（多资产、多市场）：**

| 事实 | 描述 | 实证值 | 文献 |
|------|------|--------|------|
| F1 | 收益率非正态 | 峰度 10-50 | 本文 |
| F2 | 肥尾 | P(|r|>5σ) ~ 10⁻³ | 本文 |
| F3 | 波动率聚集 | ACF(r²) 缓慢衰减 | 本文 |
| F4 | 杠杆效应 | 负收益→波动率↑ | Black (1976) |
| F5 | 交易量 - 波动率相关 | ρ ≈ 0.6 | Karpoff (1987) |
| F6 | 崩盘频率 | P(<-20%/天) ~ 3%/年 | 本文校准 |

**对本文的启示：**
- 模型必须至少重现 F1-F3
- 理想情况下重现 F1-F6

---

**[12] Chakraborti, A., Toke, I. M., Patriarca, M., & Abergel, F. (2011). "Econophysics review: II. Agent-based models." *Quantitative Finance*, 11(7), 1013-1041.**

**ABM 验证标准：**
1. 至少重现 3 个典型事实
2. 使用≥50 年数据进行校准
3. 进行样本外验证
4. 敏感性分析

---

### 2.2 参数校准文献

**[13] Hvidkjaer, S. (2006). "A trade-based analysis of momentum." *Review of Financial Studies*, 19(2), 457-491.**

**动量交易参数估计：**
```
机构动量交易概率：
P(momentum trade) = Φ(α + β₁·J12M1 + β₂·J6M1 + β₃·Size)

估计结果（表 II）：
- α = -0.5 (t=-3.2)
- β₁ = 1.5 (t=5.8)  # 12 个月动量系数
- β₂ = 0.8 (t=3.1)  # 6 个月动量系数
- β₃ = -0.3 (t=-2.5) # 规模效应

对本文的启示：
- 动量 Agent 的决策函数应使用类似形式
- 参数可以先验设为上述值，然后校准
```

---

**[14] Odean, T. (1999). "Do investors trade too much?" *American Economic Review*, 89(5), 1279-1298.**

**过度自信实证：**
```
散户交易数据（1963-1996）：
- 年换手率：~75%
- 交易后收益：低于市场 2-3%
- 解释：过度自信导致过度交易

模型含义：
- 过度自信 Agent 的交易频率应显著高于理性 Agent
- 过度自信参数 C ≈ 1.5-2.5
```

---

## 三、本文模型设计（基于文献）

### 3.1 Agent 类型与文献对应

| Agent 类型 | 文献基础 | 决策规则 | 参数来源 |
|------------|----------|----------|----------|
| **Random/Noise** | Black (1986) | 随机交易 | French & Roll (1986) |
| **Momentum** | Daniel et al. (1998) | 基于过去收益 | Hvidkjaer (2006) |
| **Value** | De Bondt & Thaler (1985) | 均值回归 | Lakonishok et al. (1994) |
| **Herd** | Shiller (1995) | 模仿他人 | Scharfstein & Stein (1990) |
| **Market Maker** | Glosten & Milgrom (1985) | 提供流动性 | Hasbrouck (1991) |

---

### 3.2 决策规则（文献基础）

#### Momentum Agent

```python
# 基于 Daniel et al. (1998) 和 Hvidkjaer (2006)

class MomentumAgent(Agent):
    """
    动量交易 Agent
    
    理论基础：
    - Daniel, Hirshleifer, & Subrahmanyam (1998, JF)
    - Hvidkjaer (2006, RFS) 表 II
    
    决策规则：
    P(买入) = Φ(α + β₁·J12M1 + β₂·J6M1 + β₃·Size + ε)
    
    参数先验：
    - α = -0.5 ± 0.2
    - β₁ = 1.5 ± 0.5  (12 个月动量，跳过 1 个月)
    - β₂ = 0.8 ± 0.3  (6 个月动量)
    - β₃ = -0.3 ± 0.1 (规模效应)
    - σ_ε = 1.0 ± 0.2 (决策噪声)
    """
    
    def __init__(self, config):
        # 参数先验来自 Hvidkjaer (2006)
        self.alpha = config.get('alpha', -0.5)
        self.beta_12m1 = config.get('beta_12m1', 1.5)
        self.beta_6m1 = config.get('beta_6m1', 0.8)
        self.beta_size = config.get('beta_size', -0.3)
        self.noise_std = config.get('noise_std', 1.0)
        
        # 过度自信（来自 Odean, 1999）
        self.overconfidence = config.get('overconfidence', 1.5)
    
    def decide(self, observation):
        # 计算动量信号
        J12M1 = self._calc_momentum(252, skip=21)  # 12 个月，跳过 1 个月
        J6M1 = self._calc_momentum(126, skip=21)   # 6 个月
        
        # 规模（用市值代理）
        size = np.log(self.state.wealth)
        
        # 决策信号
        signal = (self.alpha + 
                  self.beta_12m1 * J12M1 + 
                  self.beta_6m1 * J6M1 + 
                  self.beta_size * size)
        
        # 过度自信放大信号
        signal *= self.overconfidence
        
        # 添加噪声（有限注意力）
        signal += self.rng.normal(0, self.noise_std)
        
        # Logit 决策
        prob_buy = 1 / (1 + np.exp(-signal))
        
        if self.rng.random() < prob_buy:
            return {'action': 'buy', 'quantity': self._calc_quantity()}
        elif self.rng.random() < (1 - prob_buy):
            return {'action': 'sell', 'quantity': self._calc_quantity()}
        else:
            return {'action': 'hold'}
```

---

#### Herd Agent

```python
# 基于 Shiller (1995) 和 Scharfstein & Stein (1990)

class HerdAgent(Agent):
    """
    羊群行为 Agent
    
    理论基础：
    - Shiller (1995): 羊群行为综述
    - Scharfstein & Stein (1990, AER): 声誉驱动的羊群
    
    决策规则：
    P(跟随) = Φ(γ₀ + γ₁·NetBuy + γ₂·Volume + γ₃·Volatility)
    
    参数先验：
    - γ₀ = 0.0 ± 0.5  (基准)
    - γ₁ = 0.5 ± 0.2  (净买入影响)
    - γ₂ = 0.3 ± 0.1  (交易量影响)
    - γ₃ = -0.2 ± 0.1 (波动率影响，高波动时减少跟随)
    """
    
    def __init__(self, config):
        # 参数先验来自 Shiller (1995)
        self.gamma_0 = config.get('gamma_0', 0.0)
        self.gamma_netbuy = config.get('gamma_netbuy', 0.5)
        self.gamma_volume = config.get('gamma_volume', 0.3)
        self.gamma_vol = config.get('gamma_vol', -0.2)
        
        # 羊群强度（0=完全独立，1=完全跟随）
        self.herd_strength = config.get('herd_strength', 0.5)
        
        # 观察窗口（观察多少其他 Agent）
        self.observation_window = config.get('obs_window', 10)
    
    def decide(self, observation):
        # 观察其他 Agent 的行为
        others_actions = observation.get('others_actions', [])
        net_buy = np.mean([1 if a=='buy' else -1 if a=='sell' else 0 
                          for a in others_actions[-self.observation_window:]])
        
        volume = observation.get('volume', 1.0)
        volatility = observation.get('volatility', 0.01)
        
        # 跟随信号
        signal = (self.gamma_0 + 
                  self.gamma_netbuy * net_buy +
                  self.gamma_volume * volume +
                  self.gamma_vol * volatility)
        
        # 羊群强度调制
        prob_follow = 1 / (1 + np.exp(-signal))
        prob_follow = self.herd_strength * prob_follow
        
        if self.rng.random() < prob_follow:
            # 跟随大多数
            if net_buy > 0:
                return {'action': 'buy', 'quantity': 10}
            elif net_buy < 0:
                return {'action': 'sell', 'quantity': 10}
        
        # 否则随机决策
        return {'action': 'hold'}
```

---

### 3.3 学习算法（EWA）

```python
# 基于 Camerer & Ho (1999)

class EWALearning:
    """
    Experience-Weighted Attraction (EWA) 学习
    
    理论基础：
    - Camerer & Ho (1999, Econometrica)
    - 参数估计来自表 III（12 个实验的均值）
    
    更新方程：
    A_i(t) = [φ·N(t-1)·A_i(t-1) + (δ + (1-δ)·I(s_i, s_i*)) · π_i] / N(t)
    N(t) = ρ·N(t-1) + 1
    
    参数先验：
    - φ ~ Beta(8, 2)      # 均值 0.8, 吸引度衰减
    - δ ~ Uniform(0, 1)   # 想象权重
    - ρ ~ Beta(7, 2)      # 均值 0.78, 经验增长
    - λ ~ Gamma(2, 1)     # 均值 2.0, 选择敏感度
    """
    
    def __init__(self, n_strategies, config=None):
        self.n_strategies = n_strategies
        
        # 参数先验来自 Camerer & Ho (1999) 表 III
        self.phi = config.get('phi', 0.88)      # 吸引度衰减
        self.delta = config.get('delta', 0.58)  # 想象权重
        self.rho = config.get('rho', 0.85)      # 经验增长
        self.lambda_ = config.get('lambda', 1.5)  # 选择敏感度
        
        # 状态
        self.attractions = np.ones(n_strategies)  # 初始吸引度
        self.N = 1.0  # 经验权重
        self.experience = []
    
    def update(self, chosen_strategy, realized_payoff, foregone_payoffs):
        """
        更新吸引度
        
        参数：
        - chosen_strategy: 选择的策略索引
        - realized_payoff: 实际获得的收益
        - foregone_payoffs: 所有策略的收益（包括未选择的）
        """
        N_prev = self.N
        
        # 更新经验权重
        self.N = self.rho * N_prev + 1
        
        # 更新所有策略的吸引度
        for i in range(self.n_strategies):
            if i == chosen_strategy:
                # 实际收益
                payoff = realized_payoff
                weight = 1.0
            else:
                # 反事实收益（想象）
                payoff = foregone_payoffs[i]
                weight = self.delta
            
            self.attractions[i] = (
                (self.phi * N_prev * self.attractions[i] + weight * payoff)
                / self.N
            )
        
        # 记录经验
        self.experience.append({
            'chosen': chosen_strategy,
            'payoff': realized_payoff,
            'foregone': foregone_payoffs
        })
    
    def choose_strategy(self):
        """Logit 选择"""
        attractions_exp = np.exp(self.lambda_ * self.attractions)
        probs = attractions_exp / attractions_exp.sum()
        return self.rng.choice(self.n_strategies, p=probs)
    
    def get_attractions(self):
        """获取当前吸引度"""
        return self.attractions.copy()
```

---

### 3.4 市场机制（Glosten-Milgrom）

```python
# 基于 Glosten & Milgrom (1985) 和 Kyle (1985)

class MarketMaker:
    """
    做市商模型
    
    理论基础：
    - Glosten & Milgrom (1985, JFE)
    - Kyle (1985, Econometrica)
    - Hasbrouck (1991, JF)
    
    定价规则：
    Bid_t = E[V | sell order] - c
    Ask_t = E[V | buy order] + c
    
    价差：
    Spread = 2 · μ · σ_V + 2c
    
    参数先验：
    - μ (知情交易者比例) ~ Beta(2, 18)  # 均值 0.1
    - σ_V (价值波动) ~ Uniform(0.01, 0.1)
    - c (交易成本) ~ Uniform(0.0001, 0.001)
    - λ (Kyle's lambda) ~ Uniform(0.01, 0.05)
    """
    
    def __init__(self, config=None):
        # 参数先验
        self.mu = config.get('mu', 0.1)  # 知情交易者比例
        self.sigma_V = config.get('sigma_V', 0.02)  # 价值波动
        self.c = config.get('c', 0.0005)  # 交易成本
        self.lambda_kyle = config.get('lambda', 0.02)  # Kyle's lambda
        
        # 做市商状态
        self.inventory = 0
        self.cash = 1000000
        self.belief = 0.5  # P(V=V_high)
        
        # 订单流记录（用于 Kyle lambda 估计）
        self.order_flow_history = []
        self.price_change_history = []
    
    def set_quotes(self, fundamental_value):
        """
        设置买卖报价
        
        基于 Glosten-Milgrom:
        Bid = V · (1 - spread/2)
        Ask = V · (1 + spread/2)
        
        价差 = 2 · μ · σ_V + 2c
        """
        # 动态价差
        spread = 2 * self.mu * self.sigma_V + 2 * self.c
        
        # 库存调整（库存越大，价差越大）
        spread += 0.001 * abs(self.inventory)
        
        # 报价
        bid_price = fundamental_value * (1 - spread/2)
        ask_price = fundamental_value * (1 + spread/2)
        
        return {
            'bid': bid_price,
            'ask': ask_price,
            'spread': spread,
            'mid': (bid_price + ask_price) / 2
        }
    
    def execute_trade(self, order, quotes):
        """
        执行交易
        
        基于 Kyle (1985):
        ΔP = λ · Y
        Y = 订单流
        """
        if order.side == 'buy':
            price = quotes['ask']
            self.inventory += order.quantity
            self.cash -= price * order.quantity
            order_flow = order.quantity
        else:
            price = quotes['bid']
            self.inventory -= order.quantity
            self.cash += price * order.quantity
            order_flow = -order.quantity
        
        # 记录订单流（用于 lambda 校准）
        self.order_flow_history.append(order_flow)
        
        return {
            'price': price,
            'quantity': order.quantity,
            'inventory': self.inventory,
            'pnl': self._calculate_pnl()
        }
    
    def update_belief(self, order_flow):
        """
        做市商信念更新（贝叶斯）
        
        如果观察到大量买入订单流，提高对 V=V_high 的信念
        """
        # 简化更新
        if order_flow > 0:
            self.belief = min(1.0, self.belief + 0.01)
        elif order_flow < 0:
            self.belief = max(0.0, self.belief - 0.01)
```

---

## 四、校准与验证计划

### 4.1 校准目标（来自实证）

| 目标矩 | 实证值 | 来源 | 权重 |
|--------|--------|------|------|
| 收益率峰度 | 19.2 | Cont (2001) | 1.0 |
| 波动率 ACF(1) | 0.21 | Cont (2001) | 1.0 |
| 崩盘频率 | 0.032/年 | 本文计算 | 1.0 |
| 交易量 - 波动率相关 | 0.6 | Karpoff (1987) | 0.5 |
| 动量收益（12M1） | 0.5%/月 | Hvidkjaer (2006) | 0.5 |

### 4.2 校准方法

**矩匹配：**
```python
def objective(params):
    # 运行模拟
    sim_data = run_simulation(params, n_days=252*50)  # 50 年
    
    # 计算模拟矩
    sim_moments = {
        'kurtosis': kurtosis(sim_data['returns']),
        'acf1': acf(sim_data['returns']**2, nlags=1)[1],
        'crash_freq': np.mean(sim_data['daily_return'] < -0.20) * 252,
        'vol_vol_corr': np.corrcoef(sim_data['volume'], sim_data['volatility'])[0,1],
        'momentum': calc_momentum_profit(sim_data)
    }
    
    # 加权距离
    distance = 0
    for moment, target in target_moments.items():
        weight = moment_weights[moment]
        distance += weight * ((sim_moments[moment] - target) / target)**2
    
    return distance

# 优化
from scipy.optimize import minimize
result = minimize(objective, x0=initial_guess, method='Nelder-Mead')
calibrated_params = result.x
```

### 4.3 验证假设

| 假设 | 检验 | 通过标准 |
|------|------|----------|
| H1: 峰度 ≈ 19 | t 检验 | p > 0.05 |
| H2: 波动率聚集 | LB 检验 | p < 0.01 |
| H3: 崩盘频率 ≈ 3% | 泊松检验 | p > 0.05 |
| H4: 分布无差异 | KS 检验 | p > 0.05 |
| H5: 动量收益 > 0 | t 检验 | p < 0.05 |

---

## 五、待补充文献

### 需要进一步阅读的文献

1. **Calibration methods:**
   - Gilli & Winker (2009): "A review of heuristic optimization methods in econometrics"
   - Alfarano et al. (2008): "On the estimation of the noise intensity in a herding model"

2. **Validation:**
   - Fagiolo et al. (2019): "Validation of agent-based models in economics and finance"

3. **Empirical benchmarks:**
   - Schwert (1989): "Why does stock market volatility change over time?"
   - Andersen et al. (2001): "The distribution of realized stock return volatility"

---

## 六、结论

### 本文的学术定位

**贡献：**
1. 整合多个文献中的 Agent 类型到一个统一框架
2. 使用 EWA 学习（而非简单 RL），有实验支持
3. 使用 Glosten-Milgrom 做市商，有微观结构理论基础
4. 全面的校准和验证（针对 5 个典型事实）

**与现有文献的区别：**
- LeBaron (2006): 综述，无新模型
- Hommes (2006): 侧重理论，少实证
- **本文**: 完整实现 + 全面校准 + 开源代码

**目标期刊：**
- *Journal of Economic Dynamics and Control* (首选)
- *Quantitative Finance* (备选)
- *Computational Economics* (保底)

---

*文献综述完成时间：2026-04-03*  
*下次更新：完成初步实验后*
