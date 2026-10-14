# 梯度：多元函数对每个变量的偏导数组成的向量，指向函数增长最快的方向
import numpy as np
np.set_printoptions(precision=5, suppress=True)

def f(p): x, y = p; return x**2 + 3*y**2 + 2*x*y          # 一个碗形函数
def grad_analytic(p): x, y = p; return np.array([2*x + 2*y, 6*y + 2*x])
def grad_numeric(f, p, h=1e-6):                           # 中心差分
    g = np.zeros_like(p)
    for i in range(len(p)):
        e = np.zeros_like(p); e[i] = h
        g[i] = (f(p + e) - f(p - e)) / (2 * h)
    return g

p = np.array([1.0, 2.0])
print("解析梯度:", grad_analytic(p), "| 数值梯度:", grad_numeric(f, p), "| 一致:", np.allclose(grad_analytic(p), grad_numeric(f, p)))

# 梯度方向是最陡上升方向：沿不同方向走一小步，比较函数增量
g = grad_analytic(p); step = 1e-3
for name, d in [("梯度方向", g / np.linalg.norm(g)), ("负梯度方向", -g / np.linalg.norm(g)), ("x 轴方向", np.array([1., 0.])), ("随机方向", np.array([0.6, -0.8]))]:
    print(f"  沿{name:<6}走 {step}: f 变化 {f(p + step*d) - f(p):+.6f}")

# 梯度下降：沿负梯度迭代
p = np.array([1.0, 2.0])
for t in range(1, 101):
    p = p - 0.1 * grad_analytic(p)
    if t in (1, 10, 50, 100): print(f"第 {t:>3} 步: p={p}, f={f(p):.6f}")

# 链式法则 + 反向传播：y = sigmoid(w*x + b) 的梯度
x, w, b, target = 2.0, 0.5, -0.3, 1.0
z = w * x + b; y = 1 / (1 + np.exp(-z)); L = (y - target) ** 2
dL_dy = 2 * (y - target); dy_dz = y * (1 - y)
dL_dw, dL_db = dL_dy * dy_dz * x, dL_dy * dy_dz
num_w = ((1/(1+np.exp(-((w+1e-6)*x+b))) - target)**2 - (1/(1+np.exp(-((w-1e-6)*x+b))) - target)**2) / 2e-6
print(f"\n反向传播 dL/dw = {dL_dw:.6f} | 数值验证 {num_w:.6f} | dL/db = {dL_db:.6f}")

# 梯度消失：多层 sigmoid 连乘，导数最大只有 0.25
print("10 层 sigmoid 导数连乘上界: 0.25^10 =", 0.25 ** 10)
