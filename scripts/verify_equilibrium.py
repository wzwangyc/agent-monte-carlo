#!/usr/bin/env python3
"""
验证 EWA 学习均衡存在性和稳定性

对应文档：docs/THEORY_REPAIRS.md 第 1 节
文献：Camerer & Ho (1999, Econometrica)
"""

import numpy as np
from scipy.optimize import fixed_point
from numdifftools import Jacobian
import sys

print("=" * 70)
print("Agent Monte Carlo v2.0 - 均衡存在性验证")
print("=" * 70)

# ============================================================================
# 1. EWA 映射定义
# ============================================================================

def ewa_mapping(w, params):
    """
    EWA 学习映射 T: Δ(S) → Δ(S)
    
    参数:
        w: 策略分布 (K 维向量，Σw=1, w≥0)
        params: EWA 参数
    
    返回:
        w_new: 更新后的策略分布
    """
    K = len(w)
    phi = params['phi']
    delta = params['delta']
    rho = params['rho']
    lam = params['lambda']
    
    # 稳态经验权重
    N_star = 1 / (1 - rho) if rho < 1 else 10.0
    
    # 分母常数
    C = 1 - phi + (1 - rho) / N_star
    
    # 计算各策略支付
    pi = calculate_payoffs(w, params)
    
    # 计算稳态吸引度
    A = np.zeros(K)
    for k in range(K):
        A[k] = ((delta + (1 - delta) * w[k]) * pi[k]) / C
    
    # Logit 策略选择
    exp_A = np.exp(lam * A)
    w_new = exp_A / exp_A.sum()
    
    return w_new


def calculate_payoffs(w, params):
    """
    计算各策略的支付函数
    
    简化版本：线性支付函数
    π_k(w) = a_k - b_k·w_k + c_k·Σ_{j≠k} w_j
    
    更复杂的版本可以从市场模拟中计算
    """
    K = len(w)
    pi = np.zeros(K)
    
    base = params.get('base_payoff', np.ones(K) * 0.05)
    congestion = params.get('congestion', np.ones(K) * 0.1)
    herding = params.get('herding', np.ones(K) * 0.05)
    
    for k in range(K):
        # 策略 k 的支付
        pi[k] = (
            base[k] 
            - congestion[k] * w[k]
            + herding[k] * (1 - w[k])
        )
    
    return pi


# ============================================================================
# 2. 均衡存在性验证
# ============================================================================

def check_equilibrium_existence(params, max_attempts=10):
    """
    数值验证均衡存在性
    
    使用多个随机初始点，验证是否都能收敛到均衡
    """
    K = len(params['base_payoff'])
    
    results = []
    
    for attempt in range(max_attempts):
        # 随机初始分布
        w0 = np.random.uniform(0, 1, K)
        w0 = w0 / w0.sum()
        
        try:
            # 求解不动点
            w_star = fixed_point(
                ewa_mapping, 
                w0, 
                args=(params,), 
                method='iteration',
                xtol=1e-10,
                maxiter=1000
            )
            
            # 计算残差
            residual = np.max(np.abs(ewa_mapping(w_star, params) - w_star))
            
            results.append({
                'converged': True,
                'w_star': w_star,
                'residual': residual,
                'iterations': 'N/A'
            })
            
        except Exception as e:
            results.append({
                'converged': False,
                'error': str(e)
            })
    
    # 汇总结果
    n_converged = sum(1 for r in results if r['converged'])
    
    return {
        'exists': n_converged > 0,
        'convergence_rate': n_converged / max_attempts,
        'results': results
    }


# ============================================================================
# 3. 局部稳定性验证
# ============================================================================

def check_local_stability(w_star, params):
    """
    验证均衡的局部稳定性
    
    计算 Jacobian 矩阵的特征值
    如果谱半径 < 1，则局部渐近稳定
    """
    # 数值计算 Jacobian
    J = Jacobian(lambda w: ewa_mapping(w, params))(w_star)
    
    # 特征值
    eigenvalues = np.linalg.eigvals(J)
    spectral_radius = np.max(np.abs(eigenvalues))
    
    # 实部和虚部
    real_parts = np.real(eigenvalues)
    imag_parts = np.imag(eigenvalues)
    
    return {
        'stable': spectral_radius < 1,
        'spectral_radius': spectral_radius,
        'eigenvalues': eigenvalues,
        'real_parts': real_parts,
        'imag_parts': imag_parts,
        'jacobian': J
    }


# ============================================================================
# 4. 基准参数
# ============================================================================

benchmark_params = {
    'phi': 0.88,       # 吸引度衰减 (Camerer & Ho, 1999)
    'delta': 0.58,     # 想象权重
    'rho': 0.85,       # 经验增长
    'lambda': 1.5,     # 选择敏感度
    'base_payoff': [0.05, 0.04, 0.06, 0.03, 0.02],  # 5 种策略
    'congestion': [0.1, 0.1, 0.1, 0.1, 0.1],
    'herding': [0.05, 0.05, 0.05, 0.05, 0.05]
}


# ============================================================================
# 5. 主验证流程
# ============================================================================

print("\n" + "=" * 70)
print("测试 1: 均衡存在性 (命题 1)")
print("=" * 70)

eq_result = check_equilibrium_existence(benchmark_params, max_attempts=20)

print(f"\n初始点数量：20")
print(f"收敛次数：{sum(1 for r in eq_result['results'] if r['converged'])}/20")
print(f"收敛率：{eq_result['convergence_rate']*100:.1f}%")

if eq_result['exists']:
    # 选择残差最小的结果
    converged_results = [r for r in eq_result['results'] if r['converged']]
    best_result = min(converged_results, key=lambda r: r['residual'])
    w_star = best_result['w_star']
    
    print(f"\n✅ 均衡存在！")
    print(f"残差：{best_result['residual']:.2e}")
    
    print(f"\n均衡策略分布：")
    strategy_names = ['Noise', 'Momentum', 'Value', 'Herd', 'Arbitrageur']
    for i, (name, w_k) in enumerate(zip(strategy_names, w_star)):
        print(f"  {name:12s}: {w_k*100:6.2f}%")
    
    # 验证是概率分布
    assert np.all(w_star >= 0), "均衡分布出现负值！"
    assert np.abs(w_star.sum() - 1.0) < 1e-6, "均衡分布和不等于 1！"
    print(f"\n✅ 验证：w* 是有效的概率分布")
    
else:
    print(f"\n❌ 均衡不存在！")
    sys.exit(1)


print("\n" + "=" * 70)
print("测试 2: 局部稳定性 (命题 2)")
print("=" * 70)

stability = check_local_stability(w_star, benchmark_params)

print(f"\nJacobian 谱半径：{stability['spectral_radius']:.6f}")
print(f"最大特征值：{np.max(np.abs(stability['eigenvalues'])):.6f}")
print(f"特征值实部范围：[{stability['real_parts'].min():.4f}, {stability['real_parts'].max():.4f}]")

if stability['stable']:
    print(f"\n✅ 均衡局部渐近稳定！")
    print(f"谱半径 {stability['spectral_radius']:.4f} < 1 ✓")
else:
    print(f"\n❌ 均衡不稳定！")
    print(f"谱半径 {stability['spectral_radius']:.4f} ≥ 1 ✗")
    sys.exit(1)


print("\n" + "=" * 70)
print("测试 3: 参数敏感性")
print("=" * 70)

# 测试不同参数组合
param_sets = {
    '基准': benchmark_params,
    '高羊群': {**benchmark_params, 'herding': [0.15]*5},
    '低学习': {**benchmark_params, 'phi': 0.6},
    '高选择': {**benchmark_params, 'lambda': 3.0},
    '低衰减': {**benchmark_params, 'rho': 0.6},
}

print(f"\n测试 5 组不同参数...")

all_stable = True
for name, params in param_sets.items():
    eq = check_equilibrium_existence(params, max_attempts=5)
    
    if eq['exists']:
        w_eq = [r for r in eq['results'] if r['converged']][0]['w_star']
        stab = check_local_stability(w_eq, params)
        
        status = "✅ 稳定" if stab['stable'] else "❌ 不稳定"
        print(f"  {name:8s}: ρ(J)={stab['spectral_radius']:.4f} {status}")
        
        if not stab['stable']:
            all_stable = False
    else:
        print(f"  {name:8s}: ❌ 均衡不存在")
        all_stable = False


print("\n" + "=" * 70)
print("验证总结")
print("=" * 70)

if all_stable:
    print("\n✅ 所有测试通过！")
    print("\n理论命题验证：")
    print("  ✓ 命题 1 (均衡存在性) - 数值验证通过")
    print("  ✓ 命题 2 (局部稳定性) - 数值验证通过")
    print("  ✓ 命题 3 (参数稳健性) - 数值验证通过")
    print("\n可以安全地用于论文！")
    print("\n下一步：")
    print("  1. 运行比较静态分析")
    print("  2. 运行福利分析")
    print("  3. 生成论文图表")
else:
    print("\n⚠️ 部分测试未通过，需要检查参数设置")
    sys.exit(1)


print("\n" + "=" * 70)
print("验证完成！")
print("=" * 70)
