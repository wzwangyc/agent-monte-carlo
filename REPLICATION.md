# Agent Monte Carlo v2.0 - 复现说明

**版本：** 2.0  
**日期：** 2026-04-03  
**Python 版本：** 3.11+  
**预计时间：** 30-60 分钟

---

## 📋 系统要求

### 硬件要求

- **CPU:** 4 核以上（推荐 8 核）
- **内存:** 8GB 以上（推荐 16GB）
- **存储:** 2GB 可用空间
- **网络:** 用于下载数据

### 软件要求

- **Python:** 3.11 或更高版本
- **包管理器:** pip 或 conda
- **可选:** Docker（用于容器化复现）

---

## 🚀 快速开始

### 方法 1: pip 安装（推荐）

```bash
# 1. 克隆仓库
git clone https://github.com/wzwangyc/agent-monte-carlo.git
cd agent-monte-carlo

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 验证安装
python -c "import agent_mc; print(agent_mc.__version__)"

# 5. 运行复现脚本
python scripts/replicate_all.py
```

---

### 方法 2: Docker 容器

```bash
# 1. 构建 Docker 镜像
docker build -t agent-monte-carlo .

# 2. 运行容器
docker run -it agent-monte-carlo bash

# 3. 在容器内运行
python scripts/replicate_all.py
```

---

## 📊 复现所有结果

### 完整复现（推荐）

```bash
# 运行完整复现脚本（约 30-60 分钟）
python scripts/replicate_all.py
```

**该脚本将执行：**
1. 下载 S&P 500 数据（1980-2024）
2. 运行均衡验证
3. 运行 Bootstrap 标准误（1,000 次）
4. 运行模型对比（vs GARCH, SV）
5. 运行福利敏感性分析
6. 运行收敛速度分析
7. 运行国际验证（5 市场）
8. 生成所有图表
9. 生成所有表格

**输出：**
- `results/figures/` - 所有图表（13+ 个）
- `data/processed/` - 所有数据（9 个 JSON 文件）
- `results/tables/` - 所有表格

---

### 分步复现

如果希望分步复现，可以单独运行每个脚本：

```bash
# 1. 均衡验证（5 分钟）
python scripts/verify_equilibrium.py

# 2. Bootstrap 标准误（30 分钟）
python scripts/bootstrap_se.py

# 3. 模型对比（15 分钟）
python scripts/model_comparison.py

# 4. 福利敏感性（5 分钟）
python scripts/welfare_sensitivity.py

# 5. 收敛速度（10 分钟）
python scripts/convergence_rate.py

# 6. 国际验证（20 分钟）
python scripts/international_validation.py

# 7. 生成论文图表（10 分钟）
python scripts/generate_paper_figures.py
```

---

## 📁 文件结构

```
agent-monte-carlo/
├── src/agent_mc/              # 核心代码
│   ├── agents/                # Agent 系统
│   ├── market/                # 市场机制
│   ├── core/                  # 模拟引擎
│   └── utils/                 # 工具函数
├── scripts/                   # 复现脚本
│   ├── replicate_all.py       # 完整复现
│   ├── verify_equilibrium.py  # 均衡验证
│   ├── bootstrap_se.py        # Bootstrap
│   ├── model_comparison.py    # 模型对比
│   └── ...
├── data/
│   ├── raw/                   # 原始数据
│   └── processed/             # 处理后的数据
├── results/
│   ├── figures/               # 图表
│   └── tables/                # 表格
├── paper/
│   ├── sections/              # 论文章节
│   └── figures/               # 论文图表
├── tests/                     # 测试
├── requirements.txt           # 依赖
├── REPLICATION.md             # 本文档
└── README.md                  # 项目说明
```

---

## ✅ 验证复现结果

### 关键结果验证

运行以下命令验证关键结果：

```bash
# 验证均衡收敛率
python -c "
import json
with open('data/processed/bootstrap_results.json') as f:
    data = json.load(f)
    print(f\"Herding: {data['results']['herding']['mean']:.4f} ± {data['results']['herding']['se']:.4f}\")
    print(f\"Expected: 0.72 ± 0.08\")
"

# 验证模型对比
python -c "
import json
with open('data/processed/model_comparison.json') as f:
    data = json.load(f)
    print(f\"Agent MC Kurtosis Error: {data['agent_mc_error']['kurtosis']:.1f}%\")
    print(f\"Expected: <10%\")
"

# 验证国际验证
python -c "
import json
with open('data/processed/international_validation.json') as f:
    data = json.load(f)
    print(f\"Cross-market Kurtosis Mean: {data['cross_market_stats']['kurtosis']['mean']:.2f}\")
    print(f\"Expected: ~19\")
"
```

---

## 🐛 故障排除

### 常见问题

**问题 1: 数据下载失败**

```bash
# 解决方案：使用离线数据
python scripts/download_data.py --offline
```

**问题 2: 内存不足**

```bash
# 解决方案：减少 Bootstrap 次数
python scripts/bootstrap_se.py --n-bootstrap 500
```

**问题 3: 依赖冲突**

```bash
# 解决方案：使用 Docker
docker run -it agent-monte-carlo bash
```

**问题 4: 图表生成失败**

```bash
# 解决方案：检查 matplotlib 后端
export MPLBACKEND=Agg
python scripts/generate_paper_figures.py
```

---

## 📊 预期结果

### 关键数值

| 指标 | 预期值 | 容差 |
|------|--------|------|
| 均衡收敛率 | 100% | ±0% |
| 残差 | 3.2e-09 | ±1e-09 |
| 谱半径 | 0.7342 | ±0.01 |
| 峰度误差 | <10% | ±2% |
| ACF 误差 | <15% | ±3% |
| 崩盘频率误差 | <10% | ±2% |

### 图表清单

应生成 13+ 个图表：
1. figure1_equilibrium.png
2. figure2_herding_comparative.png
3. figure3_welfare_policy.png
4. figure4_tradeoff.png
5. figure5_robustness.png
6. calibration_results.png
7. bootstrap_distributions.png
8. model_comparison.png
9. welfare_sensitivity.png
10. convergence_analysis.png
11. international_validation.png
12. cross_validation.png
13. phase_diagram.png

---

## 🔬 高级复现

### 修改参数

```bash
# 使用自定义参数运行
python scripts/empirical_calibration.py \
  --herding 0.7 \
  --phi 0.85 \
  --lambda 1.5
```

### 并行运行

```bash
# 使用多核并行
python scripts/replicate_all.py --n-cores 8
```

### 生成 LaTeX 表格

```bash
# 生成论文用表格
python scripts/generate_tables.py --format latex
```

---

## 📞 获取帮助

如果遇到任何问题，请：

1. 查看 [GitHub Issues](https://github.com/wzwangyc/agent-monte-carlo/issues)
2. 发送邮件至 wangreits@163.com
3. 查看项目文档

---

## 📄 许可证

代码：MIT License  
数据：CC BY 4.0  
文档：CC BY-SA 4.0

---

**最后更新：** 2026-04-03  
**维护者：** Wang Yucheng  
**状态：** ✅ 已验证
