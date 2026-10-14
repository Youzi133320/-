# 统计学：从样本推断总体。描述统计 + 推断统计（置信区间、假设检验）
import numpy as np
from scipy import stats
rng = np.random.default_rng(0)

latency = rng.lognormal(mean=0, sigma=0.6, size=1000) * 800    # 模拟 API 延迟(ms)，右偏
print(f"均值 {latency.mean():.0f} ms | 中位数 {np.median(latency):.0f} ms | 标准差 {latency.std(ddof=1):.0f}")
print(f"P90 {np.percentile(latency, 90):.0f} ms | P99 {np.percentile(latency, 99):.0f} ms  ← 偏态数据看分位数比看均值更有意义")

# 中心极限定理：样本均值的分布接近正态，标准误 = σ/√n
means = rng.lognormal(0, 0.6, (10_000, 50)).mean(axis=1)
print(f"50 个样本均值的标准差 实测 {means.std():.4f} | 理论 σ/√n = {np.sqrt((np.exp(0.36)-1)*np.exp(0.36))/np.sqrt(50):.4f}")

# 两个模型在 200 道题上的准确率：差异显著吗？
n = 200
a = rng.random(n) < 0.78     # 模型 A 真实准确率 78%
b = rng.random(n) < 0.72
pa, pb = a.mean(), b.mean()
se = np.sqrt(pa*(1-pa)/n + pb*(1-pb)/n)
print(f"\n模型A {pa:.3f} vs 模型B {pb:.3f}，差 {pa-pb:.3f}，95% CI [{pa-pb-1.96*se:.3f}, {pa-pb+1.96*se:.3f}]")
t, pval = stats.ttest_ind(a.astype(float), b.astype(float))
print(f"t 检验 p 值 = {pval:.3f} → {'显著' if pval < 0.05 else '在 0.05 水平下不显著'}")

# 自助法 bootstrap 求置信区间（不依赖分布假设）
boots = [rng.choice(a, n).mean() - rng.choice(b, n).mean() for _ in range(5000)]
print(f"bootstrap 95% CI [{np.percentile(boots, 2.5):.3f}, {np.percentile(boots, 97.5):.3f}]")

# 相关 ≠ 因果；以及皮尔逊相关对异常值敏感
x = rng.normal(size=100); y = 0.5 * x + rng.normal(size=100)
print(f"\n皮尔逊 r = {stats.pearsonr(x, y)[0]:.3f} | 斯皮尔曼 ρ = {stats.spearmanr(x, y)[0]:.3f}")
x2, y2 = np.append(x, 20), np.append(y, -20)
print(f"加入一个异常点后：皮尔逊 r = {stats.pearsonr(x2, y2)[0]:.3f} | 斯皮尔曼 ρ = {stats.spearmanr(x2, y2)[0]:.3f}")
