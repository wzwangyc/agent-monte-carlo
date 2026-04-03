# Agent Monte Carlo v1.0 - 检验标准与验证流程

**版本：** 1.0  
**日期：** 2026-04-03  
**目标：** 建立系统化、可操作、经得起检验的验证标准

---

## 一、验证层次框架

### 1.1 四级验证体系

```
Level 1: 内部一致性 (Internal Consistency)
  ↓
Level 2: 实证匹配度 (Empirical Fit)
  ↓
Level 3: 样本外预测 (Out-of-Sample Prediction)
  ↓
Level 4: 结构有效性 (Structural Validity)
```

**通过要求：**
- Level 1: 必须 100% 通过
- Level 2: 必须 80% 通过
- Level 3: 必须 60% 通过
- Level 4: 建议通过

---

## 二、Level 1: 内部一致性检验

### 2.1 代码正确性

**检验 1.1: 单元测试**
```python
# 测试 Agent 基类
def test_agent_initialization():
    agent = MomentumAgent(agent_id='test', config={})
    assert agent.state.cash == 100000
    assert agent.state.holdings == {}
    assert agent.is_active == True

# 测试 EWA 学习
def test_ewa_update():
    ewa = EWALearning(n_strategies=3)
    ewa.update(chosen=0, realized_payoff=1.0, foregone=[0.5, 0.2])
    assert len(ewa.experience) == 1
    assert ewa.N > 1.0

# 测试做市商定价
def test_market_maker_quotes():
    mm = MarketMaker(mu=0.1, sigma_V=0.02)
    quotes = mm.set_quotes(fundamental_value=100)
    assert quotes['bid'] < quotes['ask']
    assert quotes['spread'] > 0
```

**通过标准：**
- [ ] 单元测试覆盖率 > 80%
- [ ] 所有测试通过
- [ ] 无边界条件错误

---

**检验 1.2: 数值稳定性**
```python
# 检验：无 NaN/Inf
def test_no_nan_inf():
    results = run_simulation(n_days=252)
    assert not np.isnan(results['prices']).any()
    assert not np.isinf(results['prices']).any()

# 检验：价格为正
def test_positive_prices():
    results = run_simulation(n_days=252)
    assert (results['prices'] > 0).all()

# 检验：财富守恒（近似）
def test_wealth_conservation():
    results = run_simulation(n_days=252)
    total_wealth = results['agent_wealth'].sum(axis=1)
    # 允许 1% 的数值误差
    assert np.std(total_wealth) / np.mean(total_wealth) < 0.01
```

**通过标准：**
- [ ] 无 NaN/Inf
- [ ] 价格始终为正
- [ ] 财富守恒（允许数值误差）

---

**检验 1.3: 随机种子可复现**
```python
def test_reproducibility():
    # 相同种子应产生相同结果
    results1 = run_simulation(seed=42)
    results2 = run_simulation(seed=42)
    assert np.allclose(results1['prices'], results2['prices'])
    
    # 不同种子应产生不同结果
    results3 = run_simulation(seed=123)
    assert not np.allclose(results1['prices'], results3['prices'])
```

**通过标准：**
- [ ] 相同种子 → 相同结果
- [ ] 不同种子 → 不同结果
- [ ] 种子记录完整

---

### 2.2 理论一致性

**检验 1.4: 极限情况**
```python
# 检验：无羊群时应接近正态
def test_no_herding_limit():
    config = {'herding_strength': 0.0}
    results = run_simulation(config, n_days=252*50)
    kurt = kurtosis(results['returns'])
    # 应接近正态分布的 3（允许偏差）
    assert 2.5 < kurt < 5.0

# 检验：无学习时应无适应
def test_no_learning_limit():
    config = {'learning_enabled': False}
    results = run_simulation(config, n_days=252*50)
    # 策略使用频率应恒定
    assert np.std(results['strategy_weights']) < 0.01

# 检验：μ=0 时价差应接近交易成本
def test_zero_mu_limit():
    mm = MarketMaker(mu=0.0, sigma_V=0.02, c=0.0005)
    quotes = mm.set_quotes(100)
    expected_spread = 2 * 0.0005  # 仅交易成本
    assert abs(quotes['spread'] - expected_spread) < 0.0001
```

**通过标准：**
- [ ] 极限情况符合理论预期
- [ ] 边界条件正确处理

---

**检验 1.5: 参数单调性**
```python
# 检验：羊群强度↑ → 峰度↑
def test_herding_monotonicity():
    kurtosis_values = []
    for h in [0.1, 0.3, 0.5, 0.7, 0.9]:
        results = run_simulation({'herding_strength': h})
        kurtosis_values.append(kurtosis(results['returns']))
    
    # 应单调递增（允许小波动）
    assert np.all(np.diff(kurtosis_values) > -0.1)

# 检验：知情交易者↑ → 价差↑
def test_mu_spread_monotonicity():
    spreads = []
    for mu in [0.05, 0.1, 0.2, 0.3]:
        mm = MarketMaker(mu=mu)
        quotes = mm.set_quotes(100)
        spreads.append(quotes['spread'])
    
    assert np.all(np.diff(spreads) > 0)
```

**通过标准：**
- [ ] 参数影响方向符合理论
- [ ] 无异常反转

---

## 三、Level 2: 实证匹配度检验

### 3.1 典型事实匹配

**检验 2.1: 肥尾（峰度）**
```python
def test_fat_tails():
    # 实证值
    target_kurtosis = 19.2  # S&P 500 1980-2024
    
    # 模拟值（1000 次重复）
    kurtosis_samples = []
    for i in range(1000):
        results = run_simulation(n_days=252*50, seed=i)
        kurt = kurtosis(results['returns'])
        kurtosis_samples.append(kurt)
    
    # 统计检验
    mean_kurt = np.mean(kurtosis_samples)
    std_kurt = np.std(kurtosis_samples)
    
    # t 检验：H0: κ_sim = 19.2
    t_stat = (mean_kurt - target_kurtosis) / (std_kurt / np.sqrt(1000))
    p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df=999))
    
    # 经济显著性：差异 < 10%
    relative_error = abs(mean_kurt - target_kurtosis) / target_kurtosis
    
    return {
        'mean_kurtosis': mean_kurt,
        'std_kurtosis': std_kurt,
        't_statistic': t_stat,
        'p_value': p_value,
        'relative_error': relative_error,
        'passed': p_value > 0.05 and relative_error < 0.1
    }
```

**通过标准：**
- [ ] 统计检验：p > 0.05（无显著差异）
- [ ] 经济显著性：相对误差 < 10%
- [ ] 95%CI 包含实证值

---

**检验 2.2: 波动率聚集**
```python
def test_volatility_clustering():
    # 实证值
    target_acf1 = 0.21  # S&P 500 ACF(1) of squared returns
    
    # 模拟值
    acf1_samples = []
    for i in range(1000):
        results = run_simulation(n_days=252*50, seed=i)
        returns = results['returns']
        acf1 = acf(returns**2, nlags=1)[1]
        acf1_samples.append(acf1)
    
    # LB 检验：H0: ACF = 0（无聚集）
    # 应拒绝 H0（p < 0.01）
    lb_stat, lb_p = acorr_ljungbox(
        np.concatenate([run_simulation(seed=i)['returns']**2 for i in range(100)]),
        lags=[10],
        return_df=True
    ).values[0]
    
    # 匹配检验
    mean_acf1 = np.mean(acf1_samples)
    relative_error = abs(mean_acf1 - target_acf1) / target_acf1
    
    return {
        'mean_acf1': mean_acf1,
        'lb_statistic': lb_stat,
        'lb_p_value': lb_p,
        'relative_error': relative_error,
        'passed': lb_p < 0.01 and relative_error < 0.3
    }
```

**通过标准：**
- [ ] LB 检验：p < 0.01（显著聚集）
- [ ] ACF(1) 匹配：相对误差 < 30%

---

**检验 2.3: 崩盘频率**
```python
def test_crash_frequency():
    # 实证值
    target_crash_freq = 0.032  # 3.2% per year (S&P 500)
    crash_threshold = -0.20  # 单日跌幅 > 20%
    
    # 模拟值
    crash_counts = []
    for i in range(1000):
        results = run_simulation(n_days=252*50, seed=i)
        daily_returns = results['returns']
        # 每年崩盘次数
        yearly_crashes = (daily_returns < crash_threshold).sum() / 50
        crash_counts.append(yearly_crashes)
    
    # 泊松检验：H0: λ = 0.032
    mean_crashes = np.mean(crash_counts)
    
    # 近似正态检验
    std_crashes = np.std(crash_counts)
    z_stat = (mean_crashes - target_crash_freq) / (std_crashes / np.sqrt(1000))
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
    
    return {
        'mean_crash_frequency': mean_crashes,
        'z_statistic': z_stat,
        'p_value': p_value,
        'passed': p_value > 0.05
    }
```

**通过标准：**
- [ ] 泊松检验：p > 0.05（无显著差异）
- [ ] 95%CI: [0.02, 0.05]（合理范围）

---

**检验 2.4: 量 - 波相关**
```python
def test_volume_volatility_correlation():
    # 实证值
    target_corr = 0.6  # Karpoff (1987)
    
    # 模拟值
    corr_samples = []
    for i in range(1000):
        results = run_simulation(n_days=252*50, seed=i)
        volume = results['volume']
        volatility = np.abs(results['returns'])
        corr = np.corrcoef(volume, volatility)[0, 1]
        corr_samples.append(corr)
    
    mean_corr = np.mean(corr_samples)
    std_corr = np.std(corr_samples)
    
    # t 检验
    t_stat = (mean_corr - target_corr) / (std_corr / np.sqrt(1000))
    p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df=999))
    
    return {
        'mean_correlation': mean_corr,
        't_statistic': t_stat,
        'p_value': p_value,
        'passed': p_value > 0.05 and mean_corr > 0.3
    }
```

**通过标准：**
- [ ] 统计检验：p > 0.05
- [ ] 经济显著性：ρ > 0.3（正相关）

---

**检验 2.5: 动量收益**
```python
def test_momentum_profit():
    # 实证值
    target_momentum = 0.005  # 0.5% per month (Hvidkjaer, 2006)
    
    # 模拟值
    momentum_samples = []
    for i in range(1000):
        results = run_simulation(n_days=252*50, seed=i)
        prices = results['prices']
        
        # 计算 12-1 动量策略收益
        mom_returns = []
        for t in range(273, len(prices), 21):  # 每月调仓
            J12M1 = (prices[t-21] - prices[t-273]) / prices[t-273]
            # 做多高动量，做空低动量（简化）
            if J12M1 > 0.05:
                mom_returns.append((prices[t] - prices[t-21]) / prices[t-21])
        
        if len(mom_returns) > 0:
            avg_mom = np.mean(mom_returns)
            momentum_samples.append(avg_mom)
    
    mean_momentum = np.mean(momentum_samples)
    
    # t 检验：H0: μ = 0
    t_stat = mean_momentum / (np.std(momentum_samples) / np.sqrt(len(momentum_samples)))
    p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df=len(momentum_samples)-1))
    
    return {
        'mean_momentum': mean_momentum,
        't_statistic': t_stat,
        'p_value': p_value,
        'passed': p_value < 0.05 and mean_momentum > 0
    }
```

**通过标准：**
- [ ] 动量收益显著 > 0（p < 0.05）
- [ ] 量级合理（0.1%-1%/月）

---

### 3.2 综合匹配度

**检验 2.6: 整体距离**
```python
def test_overall_fit():
    # 计算所有目标矩的距离
    target_moments = {
        'kurtosis': 19.2,
        'acf1': 0.21,
        'crash_freq': 0.032,
        'vol_vol_corr': 0.6,
        'momentum': 0.005
    }
    
    sim_moments = calculate_all_moments()  # 运行模拟并计算
    
    # 加权距离
    weights = {'kurtosis': 1.0, 'acf1': 1.0, 'crash_freq': 1.0, 
               'vol_vol_corr': 0.5, 'momentum': 0.5}
    
    distance = sum(
        weights[k] * ((sim_moments[k] - target_moments[k]) / target_moments[k])**2
        for k in target_moments
    )
    
    # 通过标准：距离 < 0.1（平均 10% 误差）
    return {
        'overall_distance': distance,
        'passed': distance < 0.1
    }
```

**通过标准：**
- [ ] 整体距离 < 0.1
- [ ] 无单一矩误差 > 30%

---

## 四、Level 3: 样本外预测检验

### 4.1 时期外验证

**检验 3.1: 不同时期**
```python
def test_out_of_sample_period():
    # 校准期：1980-2000
    # 验证期：2000-2024
    
    # 在校准期校准参数
    calibrated_params = calibrate(data_1980_2000)
    
    # 在验证期运行模拟
    sim_2000_2024 = run_simulation(calibrated_params, n_days=252*24)
    
    # 计算验证期矩
    val_moments = calculate_moments(sim_2000_2024)
    target_moments = calculate_moments(real_data_2000_2024)
    
    # 检验：匹配度
    errors = {k: abs(val_moments[k] - target_moments[k]) / target_moments[k] 
              for k in target_moments}
    
    return {
        'validation_errors': errors,
        'max_error': max(errors.values()),
        'passed': max(errors.values()) < 0.2  # 20% 误差
    }
```

**通过标准：**
- [ ] 最大误差 < 20%
- [ ] 平均误差 < 15%

---

### 4.2 市场外验证

**检验 3.2: 不同市场**
```python
def test_cross_market_validation():
    # 校准：S&P 500
    # 验证：NASDAQ
    
    calibrated_params = calibrate(sp500_data)
    sim_nasdaq = run_simulation(calibrated_params, n_days=252*50)
    
    # 比较 NASDAQ 实证矩
    nasdaq_moments = calculate_moments(nasdaq_real_data)
    sim_moments = calculate_moments(sim_nasdaq)
    
    # 允许更大误差（不同市场）
    errors = {k: abs(sim_moments[k] - nasdaq_moments[k]) / nasdaq_moments[k] 
              for k in nasdaq_moments}
    
    return {
        'cross_market_errors': errors,
        'passed': max(errors.values()) < 0.3  # 30% 误差
    }
```

**通过标准：**
- [ ] 最大误差 < 30%
- [ ] 定性特征一致

---

## 五、Level 4: 结构有效性检验

### 5.1 微观行为验证

**检验 4.1: Agent 交易频率**
```python
def test_agent_turnover():
    # 实证：散户年换手率 ~75% (Odean, 1999)
    target_turnover = 0.75
    
    results = run_simulation(n_days=252)
    agent_turnover = calculate_turnover(results['agent_trades'])
    
    # 检验：在合理范围内
    return {
        'sim_turnover': agent_turnover,
        'target': target_turnover,
        'passed': 0.5 < agent_turnover < 1.0
    }
```

**通过标准：**
- [ ] 换手率在实证范围内

---

**检验 4.2: 学习动态**
```python
def test_learning_dynamics():
    results = run_simulation(n_days=252*10, learning_enabled=True)
    
    # 检验：策略权重应收敛（但不完全）
    strategy_weights = results['strategy_weights']
    
    # 早期波动大，后期稳定
    early_vol = np.std(strategy_weights[:252], axis=0).mean()
    late_vol = np.std(strategy_weights[-252:], axis=0).mean()
    
    return {
        'early_volatility': early_vol,
        'late_volatility': late_vol,
        'passed': late_vol < early_vol  # 波动率下降
    }
```

**通过标准：**
- [ ] 学习导致策略稳定化
- [ ] 但保留一定多样性

---

### 5.2 反事实预测

**检验 4.3: 政策实验**
```python
def test_short_sale_constraint():
    # 实验：禁止做空
    results_no_short = run_simulation({'short_selling': False})
    results_baseline = run_simulation({'short_selling': True})
    
    # 预测：波动率下降，崩盘减少
    vol_no_short = np.std(results_no_short['returns'])
    vol_baseline = np.std(results_baseline['returns'])
    
    crash_no_short = (results_no_short['returns'] < -0.20).sum()
    crash_baseline = (results_baseline['returns'] < -0.20).sum()
    
    return {
        'volatility_change': (vol_no_short - vol_baseline) / vol_baseline,
        'crash_change': crash_no_short - crash_baseline,
        'passed': vol_no_short < vol_baseline and crash_no_short < crash_baseline
    }
```

**通过标准：**
- [ ] 反事实预测符合经济直觉
- [ ] 与实证研究一致

---

## 六、检验结果汇总

### 6.1 通过标准汇总

| Level | 检验数 | 必须通过 | 实际通过 | 状态 |
|-------|--------|----------|----------|------|
| **L1: 内部一致性** | 10 | 10 (100%) | TBD | 📅 |
| **L2: 实证匹配** | 6 | 5 (80%) | TBD | 📅 |
| **L3: 样本外** | 3 | 2 (60%) | TBD | 📅 |
| **L4: 结构有效** | 3 | 2 (60%) | TBD | 📅 |
| **总计** | 22 | 19 (86%) | TBD | 📅 |

---

### 6.2 检验报告模板

```markdown
## 检验报告

**日期：** YYYY-MM-DD  
**版本：** v1.0  
**检验者：** [姓名]

### Level 1: 内部一致性

| 检验 | 结果 | p 值 | 通过 |
|------|------|------|------|
| 1.1 单元测试 | 覆盖率 85% | - | ✅ |
| 1.2 数值稳定性 | 无 NaN/Inf | - | ✅ |
| ... | ... | ... | ... |

**L1 状态：** ✅ 通过 (10/10)

### Level 2: 实证匹配

| 检验 | 模拟值 | 实证值 | 误差 | p 值 | 通过 |
|------|--------|--------|------|------|------|
| 2.1 峰度 | 18.5 | 19.2 | 3.6% | 0.12 | ✅ |
| 2.2 ACF(1) | 0.19 | 0.21 | 9.5% | 0.08 | ✅ |
| ... | ... | ... | ... | ... | ... |

**L2 状态：** ✅ 通过 (5/6)

### Level 3: 样本外

...

### Level 4: 结构有效

...

### 总体结论

**通过检验：** 19/22 (86%)  
**状态：** ✅ 通过

**未通过检验：**
- 2.4 量 - 波相关（误差 35% > 30%）
- 3.2 跨市场验证（误差 32% > 30%）

**改进建议：**
1. 调整量 - 波相关参数
2. 增加市场异质性

**签字：** ___________  
**日期：** ___________
```

---

## 七、持续改进流程

### 7.1 检验失败处理

**流程：**
```
检验失败
  ↓
记录失败详情（值、误差、p 值）
  ↓
分析原因（代码错误？参数问题？模型缺陷？）
  ↓
提出修正方案
  ↓
重新运行检验
  ↓
记录改进结果
```

---

### 7.2 版本控制

**每次检验后更新：**
- [ ] 检验结果表
- [ ] 未通过检验列表
- [ ] 改进建议
- [ ] 版本号

---

**本检验标准是 Agent Monte Carlo 质量保证的核心！**

**所有结果必须通过这些检验才能发表！**

**任何例外必须有充分理由并记录！**

---

*标准制定时间：2026-04-03*  
*版本：1.0*  
*下次更新：首次完整检验后*
