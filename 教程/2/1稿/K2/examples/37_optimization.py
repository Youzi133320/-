# 优化：找让目标函数最小的参数。对比 GD / Momentum / Adam 在"狭长山谷"上的表现
import numpy as np
from scipy.optimize import minimize

def rosen(p): x, y = p; return (1 - x)**2 + 100 * (y - x**2)**2       # Rosenbrock 函数，最小值在 (1,1)
def rosen_grad(p):
    x, y = p
    return np.array([-2*(1 - x) - 400*x*(y - x**2), 200*(y - x**2)])

def run(update, steps=5000):
    p, state = np.array([-1.5, 2.0]), {}
    for t in range(1, steps + 1):
        p = update(p, rosen_grad(p), state, t)
    return p, rosen(p)

def sgd(p, g, s, t, lr=1e-3): return p - lr * g
def momentum(p, g, s, t, lr=1e-3, beta=0.9):
    s["v"] = beta * s.get("v", 0) + g; return p - lr * s["v"]
def adam(p, g, s, t, lr=1e-2, b1=0.9, b2=0.999, eps=1e-8):
    s["m"] = b1 * s.get("m", 0) + (1 - b1) * g
    s["v"] = b2 * s.get("v", 0) + (1 - b2) * g * g
    mh, vh = s["m"] / (1 - b1**t), s["v"] / (1 - b2**t)
    return p - lr * mh / (np.sqrt(vh) + eps)

for name, fn in [("梯度下降 GD", sgd), ("动量 Momentum", momentum), ("Adam", adam)]:
    p, val = run(fn)
    print(f"{name:<14} 5000 步后 p = {np.round(p, 4)}, f = {val:.2e}")

# 学习率太大会发散
p = np.array([-1.5, 2.0])
with np.errstate(over="ignore", invalid="ignore"):
    for _ in range(50): p = p - 1e-2 * rosen_grad(p)
print("GD 学习率 0.01（太大）50 步后:", p, "← 发散")

# 用成熟优化库：拟牛顿法 BFGS
res = minimize(rosen, x0=[-1.5, 2.0], jac=rosen_grad, method="BFGS")
print(f"scipy BFGS: p = {np.round(res.x, 6)}, 迭代 {res.nit} 次, 成功 {res.success}")

# 非凸：不同起点落到不同局部最小值
g = lambda x: np.sin(3 * x) + 0.1 * x**2
dg = lambda x: 3 * np.cos(3 * x) + 0.2 * x
for x0 in [-2.0, 0.0, 2.0]:
    x = x0
    for _ in range(500): x -= 0.01 * dg(x)
    print(f"非凸函数 从 x0={x0:+} 出发 → 收敛到 x={x:+.4f}, f={g(x):+.4f}")

# 画出三种优化器在 Rosenbrock 等高线上的轨迹
import os, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
cjk = [f.name for f in font_manager.fontManager.ttflist if "CJK SC" in f.name]
if cjk: plt.rcParams["font.family"] = cjk[0]
plt.rcParams["axes.unicode_minus"] = False
def trajectory(update, steps=5000):
    p, state, pts = np.array([-1.5, 2.0]), {}, []
    for t in range(1, steps + 1):
        p = update(p, rosen_grad(p), state, t); pts.append(p.copy())
    return np.array(pts)
xx, yy = np.meshgrid(np.linspace(-2, 2, 400), np.linspace(-1, 3, 400))
zz = (1 - xx)**2 + 100 * (yy - xx**2)**2
fig, ax = plt.subplots(figsize=(7, 5.5), constrained_layout=True)
ax.contour(xx, yy, np.log10(zz + 1e-3), levels=30, cmap="Greys", linewidths=0.6)
for name, fn, c in [("梯度下降 GD", sgd, "#C44E52"), ("动量 Momentum", momentum, "#4C72B0"), ("Adam", adam, "#55A868")]:
    tr = trajectory(fn); ax.plot(tr[:, 0], tr[:, 1], c=c, lw=1.6, label=name)
ax.plot(-1.5, 2.0, "ko"); ax.annotate("起点", (-1.5, 2.0), xytext=(-1.9, 2.6), arrowprops=dict(arrowstyle="->"))
ax.plot(1, 1, "r*", ms=15); ax.annotate("最小值 (1,1)", (1, 1), xytext=(1.2, 0.2), arrowprops=dict(arrowstyle="->"))
ax.set(title="Rosenbrock 函数上三种优化器 5000 步的轨迹", xlabel="x", ylabel="y"); ax.legend(loc="upper right")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "img", "optimizers.png")
fig.savefig(out, dpi=130); print("已保存:", os.path.basename(out))
