# 导数：函数在某点的瞬时变化率 f'(x) = lim (f(x+h)-f(x))/h
import numpy as np

f = lambda x: x ** 3
print("f(x)=x³ 在 x=2 处，理论导数 3x² = 12")
for h in [1e-1, 1e-3, 1e-5, 1e-8, 1e-12]:
    fwd = (f(2 + h) - f(2)) / h
    ctr = (f(2 + h) - f(2 - h)) / (2 * h)
    print(f"  h={h:<7g} 前向差分 {fwd:.10f}  中心差分 {ctr:.10f}")
print("→ h 太大有截断误差，h 太小有浮点舍入误差；中心差分精度更高")

# 常用导数（AI 中最常见的几个激活函数）
x = np.array([-2., 0., 2.])
sig = 1 / (1 + np.exp(-x))
def num(fn, x, h=1e-5): return (fn(x + h) - fn(x - h)) / (2 * h)
checks = {
    "sigmoid' = σ(1-σ)": (sig * (1 - sig), num(lambda t: 1/(1+np.exp(-t)), x)),
    "tanh' = 1-tanh²": (1 - np.tanh(x)**2, num(np.tanh, x)),
    "ReLU' = [x>0]": ((x > 0).astype(float), num(lambda t: np.maximum(0, t), x)),
    "(eˣ)' = eˣ": (np.exp(x), num(np.exp, x)),
    "(ln x)' = 1/x (x=1,2,4)": (1/np.array([1., 2., 4.]), num(np.log, np.array([1., 2., 4.]))),
}
for name, (formula, numeric) in checks.items():
    print(f"{name:<24} 公式 {np.round(formula, 5)}  数值 {np.round(numeric, 5)}")
print("注意 ReLU 在 0 处不可导：数值差分给出 0.5，框架通常约定取 0")

# 链式法则：(sin(x²))' = cos(x²)·2x
x0 = 1.3
print(f"\n链式法则 d/dx sin(x²) at 1.3: 公式 {np.cos(x0**2)*2*x0:.8f} | 数值 {num(lambda t: np.sin(t**2), x0):.8f}")

# 二阶导数：判断极值类型
g = lambda t: t**3 - 3*t
for x0 in [-1., 1.]:
    d2 = (g(x0 + 1e-4) - 2*g(x0) + g(x0 - 1e-4)) / 1e-8
    print(f"g(x)=x³-3x 在 x={x0:+}: g'≈{num(g, x0):.2e}, g''≈{d2:.2f} → {'极大值' if d2 < 0 else '极小值'}")
