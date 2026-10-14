# 矩阵：数字的二维表格，也是"线性变换"。AI 中的权重、注意力分数、图片都是矩阵
import numpy as np
np.set_printoptions(precision=3, suppress=True)
A = np.array([[1., 2.], [3., 4.]]); B = np.array([[0., 1.], [1., 0.]])

print("A @ B =\n", A @ B, "\nB @ A =\n", B @ A, "\n→ 矩阵乘法不满足交换律")
print("逐元素乘 A * B =\n", A * B)
print("转置 Aᵀ =\n", A.T, "\n(AB)ᵀ == BᵀAᵀ:", np.allclose((A @ B).T, B.T @ A.T))

Ainv = np.linalg.inv(A)
print("逆矩阵 A⁻¹ =\n", Ainv, "\nA @ A⁻¹ == I:", np.allclose(A @ Ainv, np.eye(2)))
print("迹 tr(A) =", np.trace(A), "| 行列式 det(A) =", round(np.linalg.det(A), 3))

# 形状规则：(m,k) @ (k,n) -> (m,n)
X = np.ones((32, 768)); W = np.ones((768, 3072))
print("批量 (32,768) @ (768,3072) ->", (X @ W).shape)
print("乘法次数 ≈ 32*768*3072 =", f"{32*768*3072:,}")

# 注意力分数：Q Kᵀ / sqrt(d)，再按行 softmax
rng = np.random.default_rng(0)
L, d = 4, 8
Q, K, V = (rng.normal(size=(L, d)) for _ in range(3))
S = Q @ K.T / np.sqrt(d)
P = np.exp(S - S.max(axis=1, keepdims=True)); P /= P.sum(axis=1, keepdims=True)
print("注意力权重矩阵 (每行和为 1):\n", P, "\n行和:", P.sum(axis=1))
print("输出 = P @ V 形状:", (P @ V).shape)

# 低秩近似：LoRA 的数学基础 —— 用 (d,r)@(r,d) 代替 (d,d)
d, r = 1024, 8
print(f"全量矩阵参数 {d*d:,} | 秩 {r} 分解参数 {2*d*r:,}（{2*d*r/(d*d):.2%}）")
