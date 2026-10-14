# 线性代数全景：向量、矩阵、线性变换、线性方程组、秩
import numpy as np
np.set_printoptions(precision=3, suppress=True)

# 线性方程组 Ax = b： 2x + y = 5,  x - 3y = -1
A = np.array([[2., 1.], [1., -3.]]); b = np.array([5., -1.])
x = np.linalg.solve(A, b)
print("解 x =", x, "| 验证 A@x == b:", np.allclose(A @ x, b))

# 矩阵 = 线性变换：旋转 90° 和 缩放
R = np.array([[0., -1.], [1., 0.]]); S = np.diag([2., 0.5])
v = np.array([1., 0.])
print("旋转后:", R @ v, "| 先旋转再缩放:", S @ R @ v, "| 顺序反过来:", R @ S @ v)
print("线性性验证 T(2u+3w) == 2T(u)+3T(w):", np.allclose(R @ (2*v + 3*np.array([0., 1.])), 2*R@v + 3*R@np.array([0., 1.])))

# 秩与行列式：矩阵是否“压扁”了空间
M = np.array([[1., 2.], [2., 4.]])           # 第二行是第一行的 2 倍
print("rank(A) =", np.linalg.matrix_rank(A), "det(A) =", round(np.linalg.det(A), 3))
print("rank(M) =", np.linalg.matrix_rank(M), "det(M) =", round(np.linalg.det(M), 3), "→ 不可逆")

# 最小二乘：方程比未知数多（过定），找误差最小的解 —— 线性回归的本质
rng = np.random.default_rng(0)
X = np.c_[np.ones(50), rng.uniform(0, 10, 50)]
y = 3 + 2 * X[:, 1] + rng.normal(0, 1, 50)
w, *_ = np.linalg.lstsq(X, y, rcond=None)
w_normal = np.linalg.inv(X.T @ X) @ X.T @ y    # 正规方程 (XᵀX)⁻¹Xᵀy
print("最小二乘 [截距, 斜率] =", w, "| 正规方程结果一致:", np.allclose(w, w_normal))

# 神经网络的一层 = 矩阵乘法 + 偏置 + 非线性
W1, b1 = rng.normal(size=(4, 3)), np.zeros(4)
h = np.maximum(0, W1 @ np.array([1., 2., 3.]) + b1)
print("一层 ReLU(W x + b) 输出形状:", h.shape, h)
