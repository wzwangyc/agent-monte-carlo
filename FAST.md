# Agent Monte Carlo - 快速修复指南

**版本：** 1.0  
**日期：** 2026-04-03  
**目标：** 快速定位并修复关键问题

---

## 🔴 P0 关键问题（立即修复）

### EC1: 均衡存在性证明

**状态：** ✅ 已完成  
**文档：** docs/THEORY_REPAIRS.md 第 1 节  
**文献：** Camerer & Ho (1999, Econometrica)  
**证明：** Brouwer 不动点定理  
**数值验证：** 待运行

**下一步：**
```bash
python scripts/verify_equilibrium.py
# 验证均衡存在和稳定性
```

---

### EC2: 比较静态分析

**状态：** ✅ 已完成  
**文档：** docs/THEORY_REPAIRS.md 第 2 节  
**文献：** Brock & Hommes (1998, JEDC)  
**框架：** 参数扰动 + 导数公式  
**数值验证：** 待运行

**下一步：**
```bash
python scripts/comparative_statics.py
# 生成参数扰动结果和图表
```

---

### EC3: 福利分析

**状态：** ✅ 已完成  
**文档：** docs/THEORY_REPAIRS.md 第 3 节  
**文献：** Stiglitz (2018, OxREP), Guvenen (2011)  
**框架：** CARA 效用 + 基尼系数  
**政策分析：** 待运行

**下一步：**
```bash
python scripts/welfare_analysis.py
# 计算福利指标和政策效应
```

---

## 🟠 P1 重要问题（本周修复）

### E1: 循环依赖

**状态：** ⏳ 待修复  
**问题：** agents/ → market/ → agents/  
**修复：** 引入 interfaces/ 层  
**难度：** 中

**修复方案：**
```python
# 新增 src/agent_mc/interfaces.py
class IMarketProvider(Protocol):
    def get_quotes(self) -> Dict: ...
    def execute_order(self, order) -> Trade: ...

# agents 和 market 都依赖 interfaces，而非互相依赖
```

---

### E5: 内存管理

**状态：** ⏳ 待修复  
**问题：** 可能 OOM  
**修复：** 环形缓冲区 + 定期聚合  
**难度：** 中

**修复方案：**
```python
from collections import deque

# 只保留最近 100 步
recent_states = deque(maxlen=100)

# 每 50 步聚合
if t % 50 == 0:
    agg = aggregate_statistics(recent_states)
    aggregated_stats.append(agg)
    recent_states.clear()
```

---

### E8: 数据验证

**状态：** ⏳ 待修复  
**问题：** 无数据质量检查  
**修复：** pandera 模式验证  
**难度：** 中

**修复方案：**
```python
import pandera as pa

price_schema = pa.DataFrameSchema({
    "date": pa.Column("datetime64[ns]", unique=True),
    "close": pa.Column("float", pa.Check.greater_than(0)),
    # ...
})

price_schema.validate(df)  # 验证数据
```

---

## 🟡 P2 次要问题（本月修复）

### E2: 配置管理
### E3: 错误处理
### E4: 性能监控
### E6: 测试覆盖
### E7: 数据版本控制
### EC4: 识别策略
### EC5: 因果推断

详见：docs/ENGINEERING_ECONOMICS_REVIEW.md

---

## 📋 今日待办 (2026-04-03)

- [x] 创建 THEORY_REPAIRS.md
- [x] 完成均衡存在性证明
- [x] 完成比较静态框架
- [x] 完成福利分析框架
- [ ] 运行数值验证脚本
- [ ] 生成论文图表
- [ ] 修复循环依赖
- [ ] 实现内存管理

---

## 🚀 快速运行

```bash
# 1. 验证均衡
python scripts/verify_equilibrium.py

# 2. 比较静态
python scripts/comparative_statics.py

# 3. 福利分析
python scripts/welfare_analysis.py

# 4. 生成论文图表
python scripts/generate_paper_figures.py

# 5. 运行完整测试
pytest tests/ -v
```

---

**快速修复指南 - 随时更新**
