# 正则化：给模型加约束，防止过拟合。L2(岭) / L1(Lasso) / Dropout / 早停
import numpy as np
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.pipeline import make_pipeline
rng = np.random.default_rng(0)

# 15 次多项式拟合 15 个点：不正则化会严重过拟合
x = np.sort(rng.uniform(0, 1, 15)); y = np.sin(2 * np.pi * x) + rng.normal(0, 0.2, 15)
xt = np.linspace(0, 1, 200); yt = np.sin(2 * np.pi * xt)
for name, model in [("无正则", LinearRegression()), ("L2 Ridge α=1e-3", Ridge(alpha=1e-3)), ("L1 Lasso α=1e-3", Lasso(alpha=1e-3, max_iter=200_000))]:
    pipe = make_pipeline(PolynomialFeatures(15), StandardScaler(), model).fit(x[:, None], y)
    coef = pipe[-1].coef_
    tr = np.mean((pipe.predict(x[:, None]) - y) ** 2); te = np.mean((pipe.predict(xt[:, None]) - yt) ** 2)
    print(f"{name:<16} 训练 MSE {tr:.4f} | 测试 MSE {te:10.4f} | 最大|系数| {np.abs(coef).max():10.1f} | 为 0 的系数 {np.sum(np.abs(coef) < 1e-8)}")

# L2 的闭式解：w = (XᵀX + λI)⁻¹ Xᵀy，λ 越大权重越小
X = rng.normal(size=(50, 5)); w_true = np.array([3., -2., 0., 0., 1.]); yy = X @ w_true + rng.normal(0, 0.5, 50)
for lam in [0, 1, 10, 100]:
    w = np.linalg.solve(X.T @ X + lam * np.eye(5), X.T @ yy)
    print(f"λ={lam:<4} 权重 {np.round(w, 3)}  ||w||={np.linalg.norm(w):.3f}")

# L1 产生稀疏解：真实为 0 的特征被压成 0（特征选择）
print("Lasso α=0.1 系数:", np.round(Lasso(alpha=0.1).fit(X, yy).coef_, 3), "← 第 3、4 个特征被置 0")

# Dropout：训练时随机置零并放大 1/(1-p)，期望不变
h = np.ones(100_000); p = 0.3
mask = rng.random(h.shape) > p
print(f"\nDropout p={p}: 保留比例 {mask.mean():.3f}，输出均值 {(h * mask / (1 - p)).mean():.4f}（≈1，与推理时一致）")

# 权重衰减（AdamW 的 weight_decay）：每步把权重乘以 (1 - lr*wd)
w = np.array([5.0, -3.0])
for _ in range(1000): w *= (1 - 1e-3 * 0.1)
print("纯权重衰减 1000 步后权重:", np.round(w, 4))

# 画出三种拟合曲线
import os, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
cjk = [f.name for f in font_manager.fontManager.ttflist if "CJK SC" in f.name]
if cjk: plt.rcParams["font.family"] = cjk[0]
plt.rcParams["axes.unicode_minus"] = False
fig, axes = plt.subplots(1, 3, figsize=(13, 4), sharey=True, constrained_layout=True)
for ax, (name, model) in zip(axes, [("无正则（过拟合）", LinearRegression()), ("L2 Ridge α=1e-3", Ridge(alpha=1e-3)), ("L1 Lasso α=1e-3", Lasso(alpha=1e-3, max_iter=200_000))]):
    pipe = make_pipeline(PolynomialFeatures(15), StandardScaler(), model).fit(x[:, None], y)
    ax.plot(xt, yt, "g--", label="真实函数 sin(2πx)")
    ax.plot(xt, pipe.predict(xt[:, None]), "C0", lw=2, label="15 次多项式拟合")
    ax.scatter(x, y, c="k", s=20, zorder=3, label="训练点")
    ax.set(title=name, ylim=(-2, 2), xlabel="x"); ax.legend(fontsize=8, loc="lower left")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "img", "regularization.png")
fig.savefig(out, dpi=120); print("已保存:", os.path.basename(out))
