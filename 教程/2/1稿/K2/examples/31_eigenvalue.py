# 特征值与特征向量：A v = λ v —— 矩阵只把 v 拉伸 λ 倍，不改变方向
import numpy as np
np.set_printoptions(precision=4, suppress=True)

A = np.array([[2., 1.], [1., 2.]])
vals, vecs = np.linalg.eig(A)
print("eig 返回的 dtype:", vals.dtype, "（NumPy 2.5 起 eig 总是返回复数类型，实对称矩阵建议用 eigh；这里取 .real）")
vals, vecs = vals.real, vecs.real
print("特征值:", vals)
for lam, v in zip(vals, vecs.T):
    print(f"  λ={lam:.1f}, v={v}, A@v={A@v}, λ*v={lam*v}, 相等: {np.allclose(A@v, lam*v)}")
print("特征值之和 =", vals.sum(), "= 迹", np.trace(A), "| 特征值之积 =", round(vals.prod(), 4), "= 行列式", round(np.linalg.det(A), 4))

# 对称矩阵：用 eigh（更快更稳），特征向量两两正交，可分解 A = Q Λ Qᵀ
w, Q = np.linalg.eigh(A)
print("Q Λ Qᵀ 还原 A:", np.allclose(Q @ np.diag(w) @ Q.T, A), "| Q 正交:", np.allclose(Q.T @ Q, np.eye(2)))

# 幂迭代：反复乘矩阵，向量会转向最大特征值方向（PageRank 的思想）
v = np.array([1., 0.])
for i in range(20): v = A @ v; v /= np.linalg.norm(v)
print("幂迭代 20 次得到的方向:", v, "| 对应特征值估计:", round(v @ A @ v, 6))

# PCA：协方差矩阵的特征向量 = 数据方差最大的方向
rng = np.random.default_rng(0)
X = rng.normal(size=(500, 2)) @ np.array([[3., 0.], [0., 0.5]]) @ np.array([[np.cos(0.5), -np.sin(0.5)], [np.sin(0.5), np.cos(0.5)]]).T
Xc = X - X.mean(axis=0)
C = Xc.T @ Xc / (len(X) - 1)
w, V = np.linalg.eigh(C)
order = w.argsort()[::-1]
print("协方差特征值（各主成分方差）:", w[order], "| 第一主成分解释方差比:", round(w[order][0] / w.sum(), 4))
print("第一主成分方向:", V[:, order[0]], "（数据被旋转了 0.5 弧度，期望约 ±[0.8776, 0.4794]）")

# 稳定性：循环神经网络中权重矩阵最大特征值 >1 会爆炸，<1 会消失
for rho in [0.9, 1.1]:
    W = rho * np.eye(2); h = np.ones(2)
    for _ in range(50): h = W @ h
    print(f"谱半径 {rho}: 乘 50 次后 ||h|| = {np.linalg.norm(h):.4g}")
