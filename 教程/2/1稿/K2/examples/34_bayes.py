# 贝叶斯定理：P(H|E) = P(E|H) P(H) / P(E) —— 用证据更新信念
import numpy as np
rng = np.random.default_rng(0)

# 经典例子：疾病检测。患病率 1%，检测灵敏度 99%，误报率 5%
prior, sens, fpr = 0.01, 0.99, 0.05
p_pos = sens * prior + fpr * (1 - prior)
posterior = sens * prior / p_pos
print(f"检测阳性后真正患病的概率（公式）= {posterior:.4f}")
N = 2_000_000
sick = rng.random(N) < prior
pos = np.where(sick, rng.random(N) < sens, rng.random(N) < fpr)
print(f"模拟 {N:,} 人验证 = {sick[pos].mean():.4f}  ← 远低于直觉的 99%（基础比率谬误）")
p2 = sens * posterior / (sens * posterior + fpr * (1 - posterior))
print(f"再测一次仍阳性 → {p2:.4f}（上一次的后验成为这一次的先验）")

# 朴素贝叶斯垃圾邮件分类（拉普拉斯平滑）
train = [("免费 领取 红包", 1), ("点击 免费 中奖", 1), ("明天 开会 讨论", 0), ("项目 进度 讨论", 0), ("红包 明天 发", 0)]
vocab = sorted({w for t, _ in train for w in t.split()})
counts = {c: np.ones(len(vocab)) for c in (0, 1)}
priors = {c: np.mean([y == c for _, y in train]) for c in (0, 1)}
for t, y in train:
    for w in t.split(): counts[y][vocab.index(w)] += 1
def predict(text):
    scores = {}
    for c in (0, 1):
        lik = counts[c] / counts[c].sum()
        scores[c] = np.log(priors[c]) + sum(np.log(lik[vocab.index(w)]) for w in text.split() if w in vocab)
    m = max(scores.values()); ps = {c: np.exp(s - m) for c, s in scores.items()}; z = sum(ps.values())
    return {("垃圾" if c else "正常"): round(float(p / z), 3) for c, p in ps.items()}
for msg in ["免费 红包", "明天 讨论 项目", "红包 讨论"]:
    print(f"'{msg}' →", predict(msg))

# Beta-二项共轭：用点击数据更新对点击率的信念
from scipy import stats
a, b = 1, 1                          # 均匀先验
for clicks, views in [(3, 10), (30, 100), (300, 1000)]:
    post = stats.beta(a + clicks, b + views - clicks)
    lo, hi = post.ppf([0.025, 0.975])
    print(f"观察 {clicks}/{views}: 后验均值 {post.mean():.3f}, 95% 可信区间 [{lo:.3f}, {hi:.3f}]  ← 数据越多越确定")
