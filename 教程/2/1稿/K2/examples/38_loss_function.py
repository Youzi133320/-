# 损失函数：衡量“预测离正确答案有多远”的数字，训练就是让它变小
import numpy as np
np.set_printoptions(precision=4, suppress=True)

# 回归：MSE / MAE / Huber，以及对异常值的敏感度
y = np.array([3.0, 5.0, 2.5, 7.0]); pred = np.array([2.5, 5.0, 3.0, 8.0])
def mse(y, p): return np.mean((y - p) ** 2)
def mae(y, p): return np.mean(np.abs(y - p))
def huber(y, p, d=1.0):
    e = np.abs(y - p); return np.mean(np.where(e <= d, 0.5 * e**2, d * (e - 0.5 * d)))
print(f"MSE {mse(y, pred):.4f} | MAE {mae(y, pred):.4f} | Huber {huber(y, pred):.4f}")
pred_out = pred.copy(); pred_out[3] = 27.0
print(f"一个预测离谱到 27 后：MSE {mse(y, pred_out):.2f}（暴涨）| MAE {mae(y, pred_out):.2f} | Huber {huber(y, pred_out):.2f}")

# 分类：交叉熵（与 softmax 搭配）
def softmax(z): z = z - z.max(axis=-1, keepdims=True); e = np.exp(z); return e / e.sum(axis=-1, keepdims=True)
def cross_entropy(logits, labels):
    logp = logits - logits.max(axis=1, keepdims=True)
    logp = logp - np.log(np.exp(logp).sum(axis=1, keepdims=True))     # log-softmax（数值稳定）
    return -np.mean(logp[np.arange(len(labels)), labels])
logits = np.array([[2.0, 0.5, -1.0], [0.1, 0.2, 3.0]]); labels = np.array([0, 2])
print("\nsoftmax 概率:\n", softmax(logits))
print(f"交叉熵 = {cross_entropy(logits, labels):.4f} = 平均 -log(正确类概率) = {np.mean(-np.log(softmax(logits)[[0,1],[0,2]])):.4f}")
for p in [0.99, 0.5, 0.01]:
    print(f"  正确类概率 {p:<4} → 损失 {-np.log(p):.3f}")
print(f"均匀猜 3 类的损失 ln3 = {np.log(3):.4f}；LLM 词表 10 万时的初始损失 ≈ ln(100000) = {np.log(100000):.2f}")

# 交叉熵的梯度极其简洁：softmax(z) - onehot(y)
z = logits[0]; onehot = np.eye(3)[0]
analytic = softmax(z[None])[0] - onehot
num = np.array([(cross_entropy((z + h)[None], labels[:1]) - cross_entropy((z - h)[None], labels[:1])) / 2e-6 for h in np.eye(3) * 1e-6])
print("交叉熵对 logits 的梯度 公式:", analytic, "数值:", num)

# 困惑度 perplexity = exp(平均交叉熵)，语言模型的常用指标
token_logprobs = np.log(np.array([0.5, 0.25, 0.8, 0.1]))
print(f"\n困惑度 PPL = exp({-token_logprobs.mean():.4f}) = {np.exp(-token_logprobs.mean()):.3f}")

# 二分类：BCE；数值稳定写法 BCE-with-logits
def bce_logits(z, t): return np.mean(np.maximum(z, 0) - z * t + np.log1p(np.exp(-np.abs(z))))
z, t = np.array([3.0, -2.0, 0.0, 50.0]), np.array([1.0, 0.0, 1.0, 0.0])
naive = -np.mean(t * np.log(1/(1+np.exp(-z))) + (1-t) * np.log(1 - 1/(1+np.exp(-z)) + 1e-300))
print(f"BCE-with-logits {bce_logits(z, t):.4f} | 朴素写法 {naive:.4f}（z=50 时 1-σ(z) 下溢为 0，需要加极小值兜底）")
