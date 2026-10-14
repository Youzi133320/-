# 概率：用 0~1 的数描述不确定性。用模拟验证公式
import numpy as np
rng = np.random.default_rng(42)
N = 1_000_000

die = rng.integers(1, 7, N)
print(f"掷骰子 P(6) 理论 {1/6:.4f} | 模拟 {np.mean(die == 6):.4f}")
two = rng.integers(1, 7, (N, 2)).sum(axis=1)
print(f"两骰子和为 7 理论 {6/36:.4f} | 模拟 {np.mean(two == 7):.4f}")

# 条件概率 P(A|B) = P(A∩B)/P(B)
A, B = die % 2 == 0, die > 3            # A: 偶数, B: 大于 3
print(f"P(偶数|大于3) 理论 {2/3:.4f} | 模拟 {np.mean(A & B) / np.mean(B):.4f}")

# 期望与方差
print(f"骰子期望 理论 3.5 | 模拟 {die.mean():.4f}；方差 理论 {35/12:.4f} | 模拟 {die.var():.4f}")

# 常见分布
print("二项分布 B(10,0.3) 均值 理论 3.0 | 模拟", rng.binomial(10, 0.3, N).mean().round(4))
normal = rng.normal(0, 1, N)
print(f"正态分布 |x|<1 比例 理论 0.6827 | 模拟 {np.mean(np.abs(normal) < 1):.4f}")

# 生日问题：23 人中有人同生日的概率
k = 23
exact = 1 - np.prod([(365 - i) / 365 for i in range(k)])
sim = np.mean([len(set(rng.integers(0, 365, k))) < k for _ in range(20_000)])
print(f"生日问题 23 人 理论 {exact:.4f} | 模拟 {sim:.4f}")

# softmax：把模型打分变成概率分布；温度控制"尖锐程度"
logits = np.array([2.0, 1.0, 0.1])
for T in [0.5, 1.0, 2.0]:
    p = np.exp(logits / T); p /= p.sum()
    print(f"温度 {T}: 概率 {p.round(3)}，和 = {p.sum():.1f}")
# 按概率采样（LLM 采样的本质）
p = np.exp(logits); p /= p.sum()
samples = rng.choice(3, size=N, p=p)
print("按 softmax 概率采样的频率:", np.bincount(samples) / N)
