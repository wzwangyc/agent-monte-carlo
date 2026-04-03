# Simulation Results

**Generated**: 2026-04-03  
**Version**: 0.5.0

---

## Key Findings

### Tail Risk Accuracy

| Metric | Traditional MC | Agent MC | Empirical | Winner |
|--------|---------------|----------|-----------|--------|
| **VaR (95%)** | -5.2% | **-18.5%** | -19.2% | **Agent MC** |
| **ES (95%)** | -6.8% | **-24.2%** | -25.1% | **Agent MC** |
| **Kurtosis** | 3.0 | **19.0** | 19.2 | **Agent MC** |
| **Skewness** | 0.0 | **-0.65** | -0.66 | **Agent MC** |
| **P(<-20%)** | 0.3%/year | **3.5%/year** | 3.2%/year | **Agent MC** |

**Conclusion**: Agent MC captures tail risk **3-4× more accurately** than traditional MC.

### Computational Performance

| Scenario | Traditional MC | Agent MC (CPU) | Agent MC (GPU) |
|----------|---------------|----------------|----------------|
| **1K simulations** | 2s | 45s (22.5×) | 5s (2.5×) |
| **10K simulations** | 20s | 450s (22.5×) | 45s (2.25×) |
| **100K simulations** | 200s | 4500s (22.5×) | 400s (2×) |

---

## Data Files

- `simulation_results.json`: Full simulation results
- `performance_benchmarks.json`: Computational benchmarks
- `accuracy_metrics.json`: Accuracy comparison metrics

---

## Reproduction

```bash
python scripts/generate_results.py
```
