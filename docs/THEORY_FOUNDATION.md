# Agent Monte Carlo v1.0 - 理论基础建设计划

**日期：** 2026-04-03  
**目标：** 在编码前建立坚实的理论基础  
**预计时间：** 7-10 天

---

## 一、为什么要先打理论基础？

### 惨痛教训（来自文献）

**案例 1：Lux & Marchesi (1999, Nature)**
- 早期 ABM 经典，被引 2000+ 次
- **问题：** 参数随意设定，无校准
- **后果：** 后续研究无法复现，声誉受损

**案例 2：Cont (2007) 批评**
> "Many agent-based models in finance suffer from ad hoc specification of behavioral rules without empirical justification."
> 
> 翻译：许多金融 ABM 模型的行为规则设定随意，缺乏实证依据。

**案例 3：Fagiolo et al. (2019) 建议**
> "ABM validation should follow a systematic protocol: (1) theoretical grounding, (2) calibration, (3) out-of-sample validation, (4) robustness checks."

---

## 二、理论基础建设清单

### Phase 1: 核心理论（3-4 天）

#### Day 1-2: Agent-Based 金融建模

**必读文献（精读）：**

**[1] LeBaron, B. (2006). "Agent-based computational finance." *Handbook of Computational Economics*.**

**阅读重点：**
- Section 3: 典型事实列表（必须重现哪些现象）
- Section 4: 模型验证方法
- Section 5: 参数校准讨论

**阅读笔记模板：**
```markdown
## LeBaron (2006) 笔记

### 核心问题
传统 MC 为什么无法重现肥尾和波动率聚集？

### 关键发现
1. 异质性 + 互动 → 涌现复杂行为
2. 学习机制 → 适应性市场
3. 参数敏感性：某些参数对结果影响巨大

### 对本文的启示
1. 必须校准到长期数据（≥50 年）
2. 必须验证多个典型事实，而非单一指标
3. 必须进行敏感性分析

### 待解决问题
1. 如何选择 Agent 类型的数量？
2. 学习速度应该多快？
3. 如何避免过度拟合？
```

**作业：**
- [ ] 写出 3000 字阅读笔记
- [ ] 列出 LeBaron 提到的所有典型事实
- [ ] 设计本文的典型事实验证清单

---

**[2] Hommes, C. H. (2006). "Heterogeneous agent models in economics and finance." *Handbook of Computational Economics*.**

**阅读重点：**
- Section 2: 异质信念框架
- Section 3: 适应性预期 vs 理性预期
- Section 4: 演化选择机制（关键！）

**关键公式推导：**
```
策略选择（复制者动态）：
n_i(t+1) = n_i(t) · exp(β·π_i(t)) / Σ_j n_j(t) · exp(β·π_j(t))

推导：
1. 假设 Agent 观察他人收益
2. 高收益策略吸引更多跟随者
3. β控制选择强度（β→∞ 时完全理性）

稳态分析：
- β=0: 随机选择，无演化
- β小：缓慢演化，多样性高
- β大：快速收敛，可能单一策略主导

对本文的启示：
- β是关键参数，必须校准
- 实证估计：β ≈ 1-5（Brock & Hommes, 1998）
```

**作业：**
- [ ] 推导策略选择公式
- [ ] 模拟不同β值下的演化动态
- [ ] 找到β的实证估计文献

---

**[3] Lux, T. (2009). "Stochastic behavioral asset-pricing models and the stylized facts."**

**阅读重点：**
- Section 2: 行为偏差建模
- Section 3: 羊群效应的微观机制
- Section 4: 参数校准方法

**关键洞察：**
```
羊群效应不是"非理性"，而是：
1. 信息 cascades（Scharfstein & Stein, 1990）
2. 声誉关注（职业顾虑）
3. 有限注意力（无法独立分析所有信息）

对本文的启示：
- 羊群参数不能随意设定
- 应该基于 Shiller (1995) 的 survey
- 实证范围：herding_strength ∈ [0.3, 0.7]
```

**作业：**
- [ ] 整理 Lux 提到的所有行为参数
- [ ] 找到每个参数的实证来源
- [ ] 设计本文的行为参数先验分布

---

#### Day 3-4: 学习理论

**必读文献（精读）：**

**[4] Camerer, C., & Ho, T. H. (1999). "Experience-weighted attraction learning in normal form games." *Econometrica*, 67(4), 827-874.**

**为什么重要：**
- 统一了强化学习和信念学习
- 参数有心理学解释
- 在 12 个实验中验证
- 被引 3000+ 次（学习理论经典）

**核心模型推导：**
```
EWA 更新方程：
A_i(t) = [φ·N(t-1)·A_i(t-1) + (δ + (1-δ)·I(s_i, s_i*)) · π_i] / N(t)

参数含义：
- φ: 吸引度衰减率（记忆遗忘）
  - φ=1: 永久记忆
  - φ=0: 只记得最近一次
  - 实证：φ ≈ 0.8-0.9（记忆持续约 5-10 期）

- δ: 想象权重（对未选择策略的关注）
  - δ=0: 纯强化学习（只关心实际收益）
  - δ=1: 纯信念学习（关心所有策略收益）
  - 实证：δ ≈ 0.5-0.7（介于两者之间）

- ρ: 经验权重增长率
  - ρ=1: 线性增长
  - ρ<1: 近期经验更重要
  - 实证：ρ ≈ 0.8-0.9

- λ: 选择敏感度
  - λ=0: 随机选择
  - λ→∞: 总是选择最优
  - 实证：λ ≈ 1-3（有限理性）

数学性质：
1. 收敛性：在平稳环境中收敛到 Nash 均衡
2. 适应性：在非平稳环境中持续适应
3. 路径依赖：历史影响长期结果
```

**作业：**
- [ ] 完整推导 EWA 方程
- [ ] 用 Python 实现 EWA
- [ ] 在简单博弈中测试（如囚徒困境）
- [ ] 复现 Camerer & Ho (1999) 的部分结果

---

**[5] Cheung, Y. W., & Friedman, D. (1997). "Individual learning in normal form games." *Games and Economic Behavior*.**

**阅读重点：**
- 实验设计（如何测试学习理论）
- 信念学习 vs 强化学习的证据
- 学习速度的个体差异

**关键发现：**
```
1. 早期：信念学习主导（观察他人）
2. 后期：强化学习主导（基于自身经验）
3. 个体差异：有些人学得快，有些人学得慢

对本文的启示：
- 可以允许 Agent 的学习参数异质
- 学习速度本身可以演化
```

**作业：**
- [ ] 设计一个简单实验验证 EWA
- [ ] 比较 EWA vs Q-Learning 的表现

---

#### Day 5-6: 市场微观结构

**必读文献（精读）：**

**[6] Glosten, L. R., & Milgrom, P. R. (1985). "Bid, ask and transaction prices in a specialist market with heterogeneously informed traders." *Journal of Financial Economics*, 14(1), 71-100.**

**为什么重要：**
- 做市商模型的奠基之作
- 解释了价差的微观起源
- 被引 10000+ 次

**核心模型推导：**
```
模型设定：
- 资产价值 V ~ {V_L, V_H}，概率各 0.5
- 交易者：知情（比例μ）vs 噪声（比例 1-μ）
- 做市商：风险中性，竞争性

均衡定价：
Bid_t = E[V | sell order at t]
Ask_t = E[V | buy order at t]

贝叶斯更新：
如果观察到买入订单：
P(V=V_H | buy) = P(buy | V_H) · P(V_H) / P(buy)
               = (1-μ)·0.5 / [(1-μ)·0.5 + μ·1]
               = (1-μ) / (1+μ)

均衡价差：
Spread = Ask - Bid
       = 2 · μ · (V_H - V_L)

关键洞察：
1. 价差来自信息不对称（μ）
2. 做市商通过价差保护自己
3. 知情交易者越多，价差越大

对本文的启示：
- 价差应该内生，而非外生给定
- μ是关键参数，实证估计≈0.1-0.3
```

**作业：**
- [ ] 完整推导 Glosten-Milgrom 模型
- [ ] 模拟不同μ值下的价差动态
- [ ] 找到μ的实证估计文献（Easley et al., 1996）

---

**[7] Kyle, A. S. (1985). "Continuous auctions and insider trading." *Econometrica*, 53(6), 1315-1335.**

**阅读重点：**
- 价格冲击函数（Kyle's lambda）
- 知情交易者的最优策略
- 市场深度与流动性

**核心公式：**
```
价格形成：
P_t = P_0 + λ · Y_t

其中：
- Y_t = 累计订单流
- λ = Kyle's lambda（价格冲击系数）

均衡结果：
- λ = σ_V / (2 · σ_Z)
- σ_V = 价值波动
- σ_Z = 噪声交易波动

实证估计（Hasbrouck, 1991）：
- λ ≈ 0.01-0.05
- 即 1% 的净订单流导致 0.01-0.05% 的价格变化

对本文的启示：
- 价格冲击应该线性或次线性
- λ必须校准到实证范围
```

**作业：**
- [ ] 推导 Kyle's lambda 公式
- [ ] 用实证数据估计λ（后续）

---

### Phase 2: 实证文献（2-3 天）

#### Day 7: 市场典型事实

**必读文献：**

**[8] Cont, R. (2001). "Empirical properties of asset returns: stylized facts and statistical issues." *Quantitative Finance*, 1(2), 223-236.**

**阅读重点：**
- 所有典型事实的列表
- 每个事实的实证证据
- 统计检验方法

**作业：**
- [ ] 整理 Cont 提到的所有典型事实
- [ ] 为每个事实找到至少 2 篇支持文献
- [ ] 设计本文的验证清单

---

**[9] Chakraborti, A., et al. (2011). "Econophysics review: II. Agent-based models." *Quantitative Finance*, 11(7), 1013-1041.**

**阅读重点：**
- ABM 验证标准
- 与实证数据的对比方法

---

#### Day 8-9: 参数校准文献

**[10] Hvidkjaer, S. (2006). "A trade-based analysis of momentum." *Review of Financial Studies*, 19(2), 457-491.**

**阅读重点：**
- 动量交易的实证模型
- 参数估计方法
- 表 II 的参数估计值

**作业：**
- [ ] 复现 Hvidkjaer 的动量交易模型
- [ ] 用本文框架实现类似的决策规则

---

**[11] Odean, T. (1999). "Do investors trade too much?" *American Economic Review*, 89(5), 1279-1298.**

**阅读重点：**
- 过度自信的实证证据
- 交易频率的分布
- 交易后的收益表现

---

### Phase 3: 方法论文献（1-2 天）

#### Day 10-11: 校准与验证方法

**[12] Gilli, M., & Winker, P. (2009). "A review of heuristic optimization methods in econometrics."**

**阅读重点：**
- 矩匹配方法
- 模拟退火、遗传算法
- 全局优化 vs 局部优化

---

**[13] Fagiolo, G., et al. (2019). "Validation of agent-based models in economics and finance."**

**阅读重点：**
- ABM 验证的系统框架
- 样本内 vs 样本外验证
- 稳健性检验方法

**作业：**
- [ ] 设计本文的验证流程
- [ ] 列出所有统计检验方法

---

## 三、理论学习输出

### 3.1 阅读笔记

**格式：**
```markdown
## [作者 (年份)] 笔记

### 研究问题
论文要解决什么问题？

### 核心模型
关键公式和假设

### 主要发现
1. ...
2. ...

### 对本文的启示
1. 模型设计：...
2. 参数选择：...
3. 验证方法：...

### 待解决问题
1. ...
2. ...

### 相关文献
- 延伸阅读：[文献列表]
```

### 3.2 参数手册

**创建文件：** `docs/PARAMETER_HANDBOOK.md`

**格式：**
```markdown
## 行为参数

### 羊群强度 (herding_strength)
- **含义：** Agent 模仿他人的倾向
- **先验范围：** [0.3, 0.7]
- **来源：** Shiller (1995), Scharfstein & Stein (1990)
- **校准方法：** 矩匹配（峰度）
- **敏感性：** 高（对肥尾影响大）

### 过度自信 (overconfidence)
- **含义：** 高估信息精度
- **先验范围：** [1.1, 1.5]
- **来源：** Odean (1998), Daniel et al. (1998)
- **校准方法：** 交易量匹配
- **敏感性：** 中
```

### 3.3 理论框架文档

**创建文件：** `docs/THEORETICAL_FRAMEWORK.md`

**内容：**
1. 模型假设（清晰列出）
2. 与现有理论的关系
3. 主要命题（Propositions）
4. 可检验的预测

---

## 四、每日学习计划

### Week 1: 核心理论

| 日期 | 内容 | 产出 |
|------|------|------|
| Day 1 | LeBaron (2006) | 阅读笔记 3000 字 |
| Day 2 | Hommes (2006) | 阅读笔记 + 公式推导 |
| Day 3 | Camerer & Ho (1999) | EWA 实现 + 测试 |
| Day 4 | Lux (2009) | 行为参数列表 |
| Day 5 | Glosten & Milgrom (1985) | 模型推导 |
| Day 6 | Kyle (1985) | Kyle's lambda 分析 |
| Day 7 | Cont (2001) | 典型事实清单 |

### Week 2: 实证与方法

| 日期 | 内容 | 产出 |
|------|------|------|
| Day 8 | Hvidkjaer (2006) | 动量参数估计 |
| Day 9 | Odean (1999) | 过度自信参数 |
| Day 10 | Gilli & Winker (2009) | 校准方法设计 |
| Day 11 | Fagiolo et al. (2019) | 验证流程设计 |
| Day 12 | 补充阅读 | 完善笔记 |
| Day 13 | 整合 | 理论框架文档 |
| Day 14 | 复习 | 准备编码 |

---

## 五、学习检验标准

### 5.1 理解检验

**能够回答以下问题：**

**ABM 基础：**
1. 为什么 ABM 能重现肥尾，而传统 MC 不能？
2. 异质性的重要性是什么？
3. 学习机制如何影响市场动态？

**学习理论：**
4. EWA 与 Q-Learning 的区别是什么？
5. 参数φ, δ, ρ, λ的经济含义是什么？
6. 如何选择合适的学习速度？

**市场微观结构：**
7. 价差为什么存在？
8. Kyle's lambda 的含义是什么？
9. 信息不对称如何影响流动性？

**实证：**
10. 必须重现哪些典型事实？
11. 每个典型事实的实证值是多少？
12. 如何统计检验模型"成功"？

### 5.2 实现检验

**能够完成以下任务：**
1. 用 Python 实现 EWA 学习
2. 推导 Glosten-Milgrom 定价公式
3. 计算 Kyle's lambda 的实证值
4. 设计矩匹配校准流程
5. 编写统计检验代码

---

## 六、推荐学习资源

### 6.1 在线课程

1. **Complexity Explorer - Agent-Based Modeling**
   - 网址：https://www.complexityexplorer.org/
   - 内容：ABM 基础 + NetLogo 实践

2. **Coursera - Game Theory (Stanford)**
   - 内容：博弈论基础，学习理论

### 6.2 代码资源

1. **Econ-ARK**
   - 网址：https://github.com/econ-ark
   - 内容：ABM 经济模型框架

2. **Mesa Examples**
   - 网址：https://github.com/projectmesa/mesa-examples
   - 内容：Python ABM 示例

### 6.3 数据资源

1. **Yahoo Finance**
   - S&P 500 日度数据（免费）

2. **FRED**
   - 宏观经济数据（免费）

3. **WRDS**
   - 学术数据库（需要机构订阅）

---

## 七、学习进度追踪

### 检查点

**Week 1 结束（Day 7）：**
- [ ] 完成 6 篇核心理论文献阅读
- [ ] 写出 6 篇阅读笔记（每篇≥3000 字）
- [ ] 实现 EWA 学习算法
- [ ] 推导 Glosten-Milgrom 模型

**Week 2 结束（Day 14）：**
- [ ] 完成 5 篇实证与方法文献阅读
- [ ] 创建参数手册
- [ ] 创建理论框架文档
- [ ] 设计校准和验证流程
- [ ] 通过理解检验（能回答所有问题）

---

## 八、开始编码的条件

**只有满足以下条件才开始编码：**

1. ✅ 完成所有 11 篇核心文献阅读
2. ✅ 写出完整的阅读笔记（总计≥3 万字）
3. ✅ 创建参数手册（所有参数有文献来源）
4. ✅ 实现 EWA 学习并通过测试
5. ✅ 推导所有核心公式
6. ✅ 设计完整的校准和验证流程
7. ✅ 能够清晰回答所有理解检验问题

**如果未满足条件：**
- 继续阅读文献
- 补充笔记
- 不要急于编码！

---

## 九、预期成果

### 9.1 文档成果

1. **阅读笔记集** - 11 篇文献，每篇 3000-5000 字
2. **参数手册** - 所有参数的来源、范围、敏感性
3. **理论框架** - 清晰的模型假设和命题
4. **校准验证计划** - 详细的实证设计

### 9.2 代码成果

1. **EWA 实现** - 经过测试的学习算法
2. **公式推导** - 所有核心公式的 Python 验证
3. **数据下载脚本** - S&P 500 数据处理

### 9.3 知识成果

1. **深入理解 ABM** - 知道为什么有效，何时失效
2. **掌握学习理论** - EWA 的原理和应用
3. **熟悉市场微观结构** - 价格形成的机制
4. **了解实证事实** - 模型必须重现的现象

---

## 十、开始学习！

**今天（Day 1）任务：**

1. 下载 LeBaron (2006) PDF
2. 精读 Section 1-3
3. 写出 3000 字笔记
4. 列出典型事实清单

**明天（Day 2）任务：**

1. 下载 Hommes (2006) PDF
2. 精读 Section 2-4
3. 推导策略选择公式
4. 写出 3000 字笔记

---

**记住：磨刀不误砍柴工！**

**1 周的理论准备，可能节省 1 个月的返工时间！**

**更重要的是：决定论文能否发表！**

---

*学习计划制定时间：2026-04-03*  
*开始执行：2026-04-03*  
*预计完成：2026-04-17*
