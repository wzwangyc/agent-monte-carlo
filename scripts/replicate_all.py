#!/usr/bin/env python3
"""
Replicate All Results - 完整复现脚本

运行此脚本将复现论文中的所有结果

预计时间：30-60 分钟
"""

import subprocess
import sys
import os
from datetime import datetime

print("=" * 70)
print("Agent Monte Carlo v2.0 - 完整复现")
print("=" * 70)
print(f"开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 70)

# 创建输出目录
os.makedirs('results/figures', exist_ok=True)
os.makedirs('results/tables', exist_ok=True)
os.makedirs('data/processed', exist_ok=True)

scripts = [
    ("1. 均衡验证", "scripts/verify_equilibrium.py", 5),
    ("2. Bootstrap 标准误", "scripts/bootstrap_se.py", 30),
    ("3. 模型对比", "scripts/model_comparison.py", 15),
    ("4. 福利敏感性", "scripts/welfare_sensitivity.py", 5),
    ("5. 收敛速度", "scripts/convergence_rate.py", 10),
    ("6. 国际验证", "scripts/international_validation.py", 20),
    ("7. 论文图表", "scripts/generate_paper_figures.py", 10),
]

total_time = sum(t[2] for t in scripts)
print(f"\n预计总时间：{total_time} 分钟\n")

results = {}

for i, (name, script, est_time) in enumerate(scripts, 1):
    print(f"\n[{i}/{len(scripts)}] 运行：{name} (预计 {est_time} 分钟)")
    print("-" * 70)
    
    try:
        start = datetime.now()
        result = subprocess.run(
            [sys.executable, script],
            capture_output=True,
            text=True,
            timeout=est_time * 60 * 2  # 2 倍缓冲时间
        )
        end = datetime.now()
        actual_time = (end - start).total_seconds() / 60
        
        if result.returncode == 0:
            print(f"✅ {name} 完成！实际时间：{actual_time:.1f} 分钟")
            results[name] = {'status': 'success', 'time': actual_time}
        else:
            print(f"❌ {name} 失败！")
            print(result.stderr)
            results[name] = {'status': 'failed', 'error': result.stderr}
            
    except subprocess.TimeoutExpired:
        print(f"⚠️ {name} 超时！")
        results[name] = {'status': 'timeout'}
    except Exception as e:
        print(f"❌ {name} 错误：{e}")
        results[name] = {'status': 'error', 'error': str(e)}

# 总结
print("\n" + "=" * 70)
print("复现总结")
print("=" * 70)

success_count = sum(1 for r in results.values() if r['status'] == 'success')
total_count = len(results)

print(f"\n成功：{success_count}/{total_count}")

for name, result in results.items():
    status = "✅" if result['status'] == 'success' else "❌"
    time_str = f"{result.get('time', 0):.1f} 分钟" if result['status'] == 'success' else result['status']
    print(f"  {status} {name}: {time_str}")

if success_count == total_count:
    print("\n🎉 所有结果复现成功！")
    print("\n输出文件：")
    print("  - results/figures/ - 所有图表")
    print("  - data/processed/ - 所有数据")
    print("  - results/tables/ - 所有表格")
else:
    print(f"\n⚠️ {total_count - success_count} 个脚本失败，请检查错误信息")

print("\n" + "=" * 70)
print(f"完成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 70)
