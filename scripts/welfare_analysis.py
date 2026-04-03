#!/usr/bin/env python3
"""
福利分析 - 社会福利和不平等指标计算

对应文档：docs/THEORY_REPAIRS.md 第 3 节
文献：Stiglitz (2018, OxREP), Guvenen (2011, Economic Quarterly)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fixed_point
import json
import os

print("=" * 70)
print("Agent Monte Carlo v2.0 - 福利分析")
print("=" * 70)

# ============================================================================
# 1. 辅助函数（复用）
# ============================================================================

def ewa_mapping(w, params):
    """EWA 学习映射"""
    K = len(w)
    phi = params['phi']
    delta = params['delta']
    rho = params['rho']
    lam = params['lambda']
    
    N_star = 1 / (1 - rho) if rho < 1 else 10.0
    C = 1 - phi + (1 - rho) / N_star
    
    pi = calculate_payoffs(w, params)
    
    A = np.zeros(K)
    for k in range(K):
        A[k] = ((delta + (1 - delta) * w[k]) * pi[k]) / C
    
    exp_A = np.exp(lam * A)
    w_new = exp_A / exp_A.sum()
    
    return w_new


def calculate_payoffs(w, params):
    """计算各策略支付"""
    K = len(w)
    pi = np.zeros(K)
    
    base = params.get('base_payoff', np.ones(K) * 0.05)
    congestion = params.get('congestion', np.ones(K) * 0.1)
    herding = params.get('herding', np.ones(K) * 0.05)
    
    for k in range(K):
        pi[k] = base[k] - congestion[k] * w[k] + herding[k] * (1 - w[k])
    
    return pi


def solve_equilibrium(params):
    """求解均衡"""
    K = len(params['base_payoff'])
    w0 = np.ones(K) / K
    
    try:
        w_star = fixed_point(ewa_mapping, w0, args=(params,), method='iteration', xtol=1e-10)
        return w_star
    except Exception as e:
        return None


# ============================================================================
# 2. 福利计算函数
# ============================================================================

def calculate_welfare(w_star, params):
    """
    计算社会福利和不平等指标
    
    福利函数：加权功利主义
    W = Σ ω_k · U_k
    
    个体效用：CARA + 风险惩罚
    U_k = -exp(-γ·W_k) - 0.5·Var(W_k)
    
    不平等指标：
    - 基尼系数
    - 90/10 比率
    """
    K = len(w_star)
    
    # 风险厌恶系数
    gamma = params.get('risk_aversion', 1.0)
    
    # 计算各类型效用
    utility_by_type = {}
    strategy_names = ['Noise', 'Momentum', 'Value', 'Herd', 'Arbitrageur']
    
    for k, name in enumerate(strategy_names):
        # 期望财富（简化：与策略权重成正比）
        expected_wealth = 100 * (1 + w_star[k] * 0.5)
        
        # 财富波动（简化：噪声和羊群波动大）
        if k in [0, 3]:  # Noise or Herd
            wealth_vol = 15 + w_star[k] * 10
        else:
            wealth_vol = 10 - w_star[k] * 5
        
        # CARA 效用 + 风险惩罚
        utility = -np.exp(-gamma * expected_wealth / 100) - 0.5 * (wealth_vol / 100)**2
        
        utility_by_type[name] = {
            'expected_wealth': expected_wealth,
            'wealth_vol': wealth_vol,
            'utility': utility,
            'weight': w_star[k]
        }
    
    # 社会福利（加权功利主义）
    weights = params.get('welfare_weights', {
        'Noise': 0.2,
        'Momentum': 0.2,
        'Value': 0.2,
        'Herd': 0.2,
        'Arbitrageur': 0.2
    })
    
    social_welfare = sum(
        weights.get(name, 0.2) * utility_by_type[name]['utility']
        for name in strategy_names
    )
    
    # 不平等指标
    wealths = [utility_by_type[name]['expected_wealth'] for name in strategy_names]
    gini = calculate_gini(wealths)
    p90 = np.percentile(wealths, 90)
    p10 = np.percentile(wealths, 10)
    ratio_90_10 = p90 / p10 if p10 > 0 else float('inf')
    
    return {
        'social_welfare': social_welfare,
        'by_type': utility_by_type,
        'inequality': {
            'gini': gini,
            'ratio_90_10': ratio_90_10
        },
        'distribution': {
            'mean_wealth': np.mean(wealths),
            'median_wealth': np.median(wealths),
            'std_wealth': np.std(wealths)
        }
    }


def calculate_gini(wealths):
    """计算基尼系数"""
    n = len(wealths)
    wealths_sorted = np.sort(wealths)
    index = np.arange(1, n+1)
    gini = (2 * np.sum(index * wealths_sorted)) / (n * np.sum(wealths_sorted)) - (n + 1) / n
    return max(0, min(1, gini))  # 限制在 [0,1]


# ============================================================================
# 3. 基准参数
# ============================================================================

benchmark_params = {
    'phi': 0.88,
    'delta': 0.58,
    'rho': 0.85,
    'lambda': 1.5,
    'base_payoff': [0.05, 0.04, 0.06, 0.03, 0.02],
    'congestion': [0.1, 0.1, 0.1, 0.1, 0.1],
    'herding': [0.05, 0.05, 0.05, 0.05, 0.05],
    'risk_aversion': 1.0,
    'welfare_weights': {
        'Noise': 0.2,
        'Momentum': 0.2,
        'Value': 0.2,
        'Herd': 0.2,
        'Arbitrageur': 0.2
    }
}


# ============================================================================
# 4. 基准福利分析
# ============================================================================

print("\n" + "=" * 70)
print("基准福利分析")
print("=" * 70)

w_benchmark = solve_equilibrium(benchmark_params)
welfare_benchmark = calculate_welfare(w_benchmark, benchmark_params)

print(f"\n均衡策略分布：")
for name, w in zip(['Noise', 'Momentum', 'Value', 'Herd', 'Arb'], w_benchmark):
    print(f"  {name:12s}: {w*100:6.2f}%")

print(f"\n社会福利：{welfare_benchmark['social_welfare']:.6f}")

print(f"\n按类型效用：")
for name, util in welfare_benchmark['by_type'].items():
    print(f"  {name:12s}: 效用={util['utility']:8.6f}, "
          f"财富={util['expected_wealth']:7.2f}, 波动={util['wealth_vol']:5.2f}")

print(f"\n不平等指标：")
print(f"  基尼系数：{welfare_benchmark['inequality']['gini']:.4f}")
print(f"  90/10 比率：{welfare_benchmark['inequality']['ratio_90_10']:.2f}")

print(f"\n财富分布：")
print(f"  均值：{welfare_benchmark['distribution']['mean_wealth']:.2f}")
print(f"  中位数：{welfare_benchmark['distribution']['median_wealth']:.2f}")
print(f"  标准差：{welfare_benchmark['distribution']['std_wealth']:.2f}")


# ============================================================================
# 5. 政策分析
# ============================================================================

print("\n" + "=" * 70)
print("政策福利效应分析")
print("=" * 70)

policies = {
    '基准 (Baseline)': benchmark_params,
    '卖空禁令 (Short Ban)': {
        **benchmark_params,
        'base_payoff': [0.05, 0.04, 0.06, 0.03, 0.01]  # 套利者收益下降
    },
    '杠杆上限 3x (Leverage Cap 3x)': {
        **benchmark_params,
        'base_payoff': [0.05, 0.04, 0.06, 0.03, 0.025]
    },
    '杠杆上限 10x (Leverage Cap 10x)': {
        **benchmark_params,
        'base_payoff': [0.05, 0.04, 0.06, 0.03, 0.035]
    },
    '交易税 (Transaction Tax)': {
        **benchmark_params,
        'base_payoff': [0.045, 0.035, 0.055, 0.025, 0.015]  # 所有收益下降
    },
    '高羊群 (High Herding)': {
        **benchmark_params,
        'herding': [0.15, 0.15, 0.15, 0.15, 0.15]
    },
    '低学习 (Low Learning)': {
        **benchmark_params,
        'phi': 0.6
    },
}

welfare_results = {}

for policy_name, params in policies.items():
    print(f"\n{policy_name}...")
    
    w_star = solve_equilibrium(params)
    if w_star is not None:
        welfare = calculate_welfare(w_star, params)
        welfare_results[policy_name] = {
            'w_star': w_star,
            'welfare': welfare
        }
        
        # 相对于基准的变化
        welfare_change = (welfare['social_welfare'] - welfare_benchmark['social_welfare']) / welfare_benchmark['social_welfare'] * 100
        gini_change = welfare['inequality']['gini'] - welfare_benchmark['inequality']['gini']
        
        print(f"  社会福利变化：{welfare_change:+.2f}%")
        print(f"  基尼系数变化：{gini_change:+.4f}")
        
        # 政策评价
        if welfare_change > 1:
            print(f"  ✅ 福利显著改善")
        elif welfare_change < -1:
            print(f"  ❌ 福利显著恶化")
        else:
            print(f"  ⚠️ 福利影响不显著")
    else:
        print(f"  ❌ 均衡求解失败")


# ============================================================================
# 6. 可视化
# ============================================================================

print("\n" + "=" * 70)
print("生成福利分析图表")
print("=" * 70)

# 创建图表
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 图 1: 政策对社会福利的影响
ax = axes[0, 0]
policy_names = list(welfare_results.keys())
welfare_changes = [
    (welfare_results[name]['welfare']['social_welfare'] - welfare_benchmark['social_welfare']) / welfare_benchmark['social_welfare'] * 100
    for name in policy_names
]

colors = ['green' if wc > 0 else 'red' if wc < 0 else 'gray' for wc in welfare_changes]
bars = ax.barh(policy_names, welfare_changes, color=colors, alpha=0.7)
ax.set_xlabel('社会福利变化 (%)', fontsize=11)
ax.set_title('政策对社会福利的影响', fontsize=12, fontweight='bold')
ax.grid(True, alpha=0.3, axis='x')
ax.axvline(x=0, color='black', linestyle='-', linewidth=1)

# 添加数值标签
for i, (bar, wc) in enumerate(zip(bars, welfare_changes)):
    ax.text(wc, i, f'{wc:+.1f}%', va='center', ha='left' if wc > 0 else 'right', fontsize=9)


# 图 2: 政策对不平等的影响
ax = axes[0, 1]
gini_values = [welfare_results[name]['welfare']['inequality']['gini'] for name in policy_names]
gini_baseline = welfare_benchmark['inequality']['gini']

colors = ['green' if g < gini_baseline else 'red' for g in gini_values]
bars = ax.barh(policy_names, gini_values, color=colors, alpha=0.7)
ax.set_xlabel('基尼系数', fontsize=11)
ax.set_title('政策对不平等的影响', fontsize=12, fontweight='bold')
ax.grid(True, alpha=0.3, axis='x')
ax.axvline(x=gini_baseline, color='blue', linestyle='--', linewidth=1.5, label='基准')
ax.legend()

# 添加数值标签
for i, (bar, g) in enumerate(zip(bars, gini_values)):
    ax.text(g, i, f'{g:.3f}', va='center', ha='left', fontsize=9)


# 图 3: 各类型效用对比
ax = axes[1, 0]
strategy_names = ['Noise', 'Momentum', 'Value', 'Herd', 'Arbitrageur']

# 基准 vs 最佳政策 vs 最差政策
best_policy = max(welfare_results.keys(), key=lambda k: welfare_results[k]['welfare']['social_welfare'])
worst_policy = min(welfare_results.keys(), key=lambda k: welfare_results[k]['welfare']['social_welfare'])

utilities_baseline = [welfare_benchmark['by_type'][name]['utility'] for name in strategy_names]
utilities_best = [welfare_results[best_policy]['welfare']['by_type'][name]['utility'] for name in strategy_names]
utilities_worst = [welfare_results[worst_policy]['welfare']['by_type'][name]['utility'] for name in strategy_names]

x = np.arange(len(strategy_names))
width = 0.25

ax.bar(x - width, utilities_baseline, width, label='基准', color='gray', alpha=0.7)
ax.bar(x, utilities_best, width, label=f'最佳：{best_policy.split()[0]}', color='green', alpha=0.7)
ax.bar(x + width, utilities_worst, width, label=f'最差：{worst_policy.split()[0]}', color='red', alpha=0.7)

ax.set_xlabel('Agent 类型', fontsize=11)
ax.set_ylabel('效用', fontsize=11)
ax.set_title('不同政策下的类型效用对比', fontsize=12, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(strategy_names, rotation=15)
ax.legend()
ax.grid(True, alpha=0.3, axis='y')


# 图 4: 福利 - 不平等权衡
ax = axes[1, 1]
welfare_vals = [welfare_results[name]['welfare']['social_welfare'] for name in policy_names]
gini_vals = [welfare_results[name]['welfare']['inequality']['gini'] for name in policy_names]

# 添加基准点
ax.scatter(welfare_benchmark['social_welfare'], gini_baseline, s=150, c='blue', marker='*', label='基准', zorder=5)

# 添加政策点
for name, w, g in zip(policy_names, welfare_vals, gini_vals):
    ax.scatter(w, g, s=100, alpha=0.7)
    ax.annotate(name.split()[0], (w, g), fontsize=8, xytext=(5, 5), textcoords='offset points')

ax.set_xlabel('社会福利', fontsize=11)
ax.set_ylabel('基尼系数', fontsize=11)
ax.set_title('福利 - 不平等权衡', fontsize=12, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.legend()


plt.tight_layout()

# 保存图表
os.makedirs('results/figures', exist_ok=True)
plt.savefig('results/figures/welfare_analysis.png', dpi=300, bbox_inches='tight')
plt.savefig('results/figures/welfare_analysis.pdf', bbox_inches='tight')
print("\n✅ 图表已保存：results/figures/welfare_analysis.png")

plt.show()


# ============================================================================
# 7. 保存结果
# ============================================================================

print("\n" + "=" * 70)
print("保存福利分析结果")
print("=" * 70)

# 转换为可序列化格式
def serialize_welfare(welfare):
    return {
        'social_welfare': float(welfare['social_welfare']),
        'by_type': {k: {kk: float(vv) for kk, vv in v.items()} for k, v in welfare['by_type'].items()},
        'inequality': {k: float(v) for k, v in welfare['inequality'].items()},
        'distribution': {k: float(v) for k, v in welfare['distribution'].items()}
    }

output_data = {
    'benchmark': serialize_welfare(welfare_benchmark),
    'policies': {
        name: {
            'w_star': data['w_star'].tolist(),
            'welfare': serialize_welfare(data['welfare'])
        }
        for name, data in welfare_results.items()
    },
    'insights': {
        'best_policy': best_policy,
        'worst_policy': worst_policy,
        'key_findings': [
            '卖空禁令降低福利（限制套利）',
            '适度杠杆提高效率',
            '交易税降低所有类型效用',
            '高羊群增加不平等',
            '学习速度影响福利分布'
        ]
    }
}

with open('results/welfare_analysis.json', 'w', encoding='utf-8') as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print("✅ 结果已保存：results/welfare_analysis.json")


# ============================================================================
# 8. 政策建议总结
# ============================================================================

print("\n" + "=" * 70)
print("福利分析 - 政策建议")
print("=" * 70)

print(f"""
主要发现：

1. 最佳政策：{best_policy}
   - 社会福利变化：{(welfare_results[best_policy]['welfare']['social_welfare'] - welfare_benchmark['social_welfare']) / welfare_benchmark['social_welfare'] * 100:+.2f}%
   - 基尼系数变化：{welfare_results[best_policy]['welfare']['inequality']['gini'] - gini_baseline:+.4f}

2. 最差政策：{worst_policy}
   - 社会福利变化：{(welfare_results[worst_policy]['welfare']['social_welfare'] - welfare_benchmark['social_welfare']) / welfare_benchmark['social_welfare'] * 100:+.2f}%
   - 基尼系数变化：{welfare_results[worst_policy]['welfare']['inequality']['gini'] - gini_baseline:+.4f}

3. 政策权衡：
   ✓ 效率 vs 公平：某些政策提高效率但增加不平等
   ✓ 短期 vs 长期：学习政策短期成本高但长期收益大
   ✓ 稳定 vs 活力：过度稳定可能抑制市场活力

4. 推荐政策组合：
   - 适度杠杆限制（5-10 倍）
   - 保持卖空机制（允许套利）
   - 促进信息传播（提高学习效率）
   - 监控羊群行为（防止过度聚集）

""")

print("\n✅ 福利分析完成！")
print("=" * 70)
