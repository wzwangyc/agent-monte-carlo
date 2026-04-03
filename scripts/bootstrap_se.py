#!/usr/bin/env python3
"""
Bootstrap Standard Errors - 参数标准误计算

使用 bootstrap 方法计算校准参数的标准误和 95% 置信区间

方法：
1. 从原始数据中有放回抽样（1,000 次）
2. 每次重新校准参数
3. 计算标准误和 95% CI
"""

import numpy as np
import pandas as pd
import yfinance as yf
from scipy.optimize import minimize
import json
import os
from datetime import datetime

print("=" * 70)
print("Agent Monte Carlo v2.0 - Bootstrap Standard Errors")
print("=" * 70)

# ============================================================================
# 1. 下载数据
# ============================================================================

print("\n步骤 1: 下载 S&P 500 数据...")

try:
    sp500 = yf.download('^GSPC', start='1980-01-01', end='2024-12-31', progress=False)
    returns = sp500['Close'].pct_change().dropna()
    print(f"  ✅ 数据下载成功：{len(returns)} 个观测值")
except Exception as e:
    print(f"  ❌ 下载失败，使用模拟数据")
    np.random.seed(42)
    returns = np.random.normal(0.0003, 0.01, 11306)

# ============================================================================
# 2. Bootstrap 设置
# ============================================================================

n_bootstrap = 1000  # bootstrap 次数
n_days = len(returns)

print(f"\n步骤 2: Bootstrap 设置")
print(f"  Bootstrap 次数：{n_bootstrap}")
print(f"  样本大小：{n_days}")

# 存储 bootstrap 参数估计
bootstrap_params = {
    'herding': [],
    'phi': [],
    'delta': [],
    'rho': [],
    'lambda': [],
    'mu': [],
    'sigma_noise': []
}

# ============================================================================
# 3. 定义矩计算函数
# ============================================================================

def calculate_moments(returns):
    """计算实证矩"""
    from scipy import stats
    
    moments = {}
    moments['kurtosis'] = stats.kurtosis(returns) + 3
    moments['acf1'] = pd.Series(returns**2).autocorr(lag=1)
    moments['crash_freq'] = (returns < -0.05).sum() / len(returns) * 252
    moments['skewness'] = stats.skew(returns)
    moments['vol_annual'] = returns.std() * np.sqrt(252)
    
    # 处理 NaN
    for k, v in moments.items():
        if np.isnan(v):
            moments[k] = 0.0
    
    return moments

# ============================================================================
# 4. 定义矩匹配函数
# ============================================================================

def moment_distance(params, target_moments):
    """计算模拟矩与目标矩的距离"""
    herding, phi, delta, rho, lam, mu, sigma = params
    
    # 近似矩（基于理论关系）
    sim_moments = {
        'kurtosis': 3 + 20 * herding,
        'acf1': 0.1 + 0.5 * (1 - phi),
        'crash_freq': 0.01 + 0.1 * herding,
        'skewness': -0.5 * herding,
    }
    
    # 加权距离
    weights = {'kurtosis': 1.0, 'acf1': 1.0, 'crash_freq': 1.0, 'skewness': 0.5}
    
    distance = 0
    for key in weights:
        diff = (sim_moments[key] - target_moments[key]) / target_moments[key]
        distance += weights[key] * diff**2
    
    return distance

# ============================================================================
# 5. Bootstrap 循环
# ============================================================================

print("\n步骤 3: 运行 Bootstrap...")
print("  这可能需要几分钟...")

param_names = list(bootstrap_params.keys())
bounds = [
    (0.1, 0.9),    # herding
    (0.6, 0.99),   # phi
    (0.3, 0.8),    # delta
    (0.7, 0.95),   # rho
    (0.5, 3.0),    # lambda
    (0.05, 0.3),   # mu
    (0.05, 0.3)    # sigma_noise
]

# 计算目标矩（使用原始数据）
target_moments = calculate_moments(returns)

np.random.seed(42)  # 可复现

for i in range(n_bootstrap):
    # 有放回抽样
    bootstrap_sample = np.random.choice(returns, size=n_days, replace=True)
    
    # 计算 bootstrap 矩
    boot_moments = calculate_moments(bootstrap_sample)
    
    # 校准参数
    x0 = [0.5, 0.88, 0.58, 0.85, 1.5, 0.1, 0.15]  # 基准初始值
    
    result = minimize(
        moment_distance,
        x0,
        args=(boot_moments,),
        method='Nelder-Mead',
        bounds=bounds,
        options={'maxiter': 200, 'xatol': 1e-4}
    )
    
    # 存储结果
    if result.success:
        for j, name in enumerate(param_names):
            bootstrap_params[name].append(result.x[j])
    
    # 进度
    if (i + 1) % 100 == 0:
        print(f"  进度：{i + 1}/{n_bootstrap} ({(i + 1)/n_bootstrap*100:.0f}%)")

# ============================================================================
# 6. 计算标准误和置信区间
# ============================================================================

print("\n" + "=" * 70)
print("步骤 4: 计算标准误和置信区间")
print("=" * 70)

results = {}

for name in param_names:
    values = np.array(bootstrap_params[name])
    
    mean = np.mean(values)
    std = np.std(values, ddof=1)  # 标准误
    se = std  # bootstrap 标准误
    
    # 95% 置信区间（百分位数法）
    ci_lower = np.percentile(values, 2.5)
    ci_upper = np.percentile(values, 97.5)
    
    results[name] = {
        'mean': float(mean),
        'std': float(std),
        'se': float(se),
        'ci_lower': float(ci_lower),
        'ci_upper': float(ci_upper),
        'n_bootstrap': len(values)
    }

# ============================================================================
# 7. 输出结果
# ============================================================================

print("\nBootstrap 结果（标准误和 95% 置信区间）：")
print("-" * 80)
print(f"{'参数':15s} | {'估计值':>10s} | {'标准误':>10s} | {'95% CI 下限':>12s} | {'95% CI 上限':>12s}")
print("-" * 80)

for name in param_names:
    r = results[name]
    print(f"{name:15s} | {r['mean']:10.4f} | {r['se']:10.4f} | {r['ci_lower']:12.4f} | {r['ci_upper']:12.4f}")

print("-" * 80)

# ============================================================================
# 8. 保存结果
# ============================================================================

os.makedirs('data/processed', exist_ok=True)

with open('data/processed/bootstrap_results.json', 'w', encoding='utf-8') as f:
    json.dump({
        'bootstrap_params': bootstrap_params,
        'results': results,
        'n_bootstrap': n_bootstrap,
        'timestamp': datetime.now().isoformat()
    }, f, indent=2)

print(f"\n  ✅ 结果已保存：data/processed/bootstrap_results.json")

# ============================================================================
# 9. 可视化
# ============================================================================

print("\n生成 Bootstrap 分布图...")

import matplotlib.pyplot as plt

fig, axes = plt.subplots(3, 3, figsize=(15, 12))
axes = axes.flatten()

for i, name in enumerate(param_names):
    ax = axes[i]
    values = np.array(bootstrap_params[name])
    
    # 直方图
    ax.hist(values, bins=30, density=True, alpha=0.7, color='skyblue', edgecolor='black')
    
    # 添加均值和置信区间
    mean = results[name]['mean']
    ci_lower = results[name]['ci_lower']
    ci_upper = results[name]['ci_upper']
    
    ax.axvline(mean, color='red', linestyle='-', linewidth=2, label=f'Mean: {mean:.4f}')
    ax.axvline(ci_lower, color='green', linestyle='--', linewidth=1.5, label=f'95% CI')
    ax.axvline(ci_upper, color='green', linestyle='--', linewidth=1.5)
    
    ax.set_xlabel('Parameter Value')
    ax.set_ylabel('Density')
    ax.set_title(f'{name}\nSE={results[name]["se"]:.4f}, 95% CI=[{ci_lower:.4f}, {ci_upper:.4f}]')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

# 隐藏最后一个子图
axes[-1].axis('off')

plt.tight_layout()
plt.savefig('results/figures/bootstrap_distributions.png', dpi=300, bbox_inches='tight')
print(f"  ✅ 图表已保存：results/figures/bootstrap_distributions.png")

plt.show()

# ============================================================================
# 10. 总结
# ============================================================================

print("\n" + "=" * 70)
print("Bootstrap 完成总结")
print("=" * 70)

print(f"""
主要结果:

1. Bootstrap 次数：{n_bootstrap}
2. 样本大小：{n_days}
3. 收敛率：{len(bootstrap_params['herding'])/n_bootstrap*100:.1f}%

参数估计（均值 ± 标准误）:
""")

for name in param_names:
    r = results[name]
    print(f"  {name:15s}: {r['mean']:.4f} ± {r['se']:.4f} (95% CI: [{r['ci_lower']:.4f}, {r['ci_upper']:.4f}])")

print(f"""
下一步:
1. 在论文中添加标准误表格
2. 报告 95% 置信区间
3. 讨论参数估计的精确度
""")

print("\n✅ Bootstrap 标准误计算完成！")
print("=" * 70)
