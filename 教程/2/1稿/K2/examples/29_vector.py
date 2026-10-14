# 向量：有大小和方向的量；在 AI 中，一切（词、图片、用户）都被表示成向量
import numpy as np
np.set_printoptions(precision=4, suppress=True)
a, b = np.array([3., 4.]), np.array([4., 3.])

print("加法 a+b =", a + b, "| 数乘 2a =", 2 * a)
print("L2 范数 ||a|| =", np.linalg.norm(a), "= sqrt(3²+4²)")
print("L1 范数 =", np.linalg.norm(a, 1), "| 无穷范数 =", np.linalg.norm(a, np.inf))

dot = a @ b
cos = dot / (np.linalg.norm(a) * np.linalg.norm(b))
print(f"点积 a·b = {dot} = 3*4+4*3 | 余弦相似度 = {cos:.4f} | 夹角 = {np.degrees(np.arccos(cos)):.2f}°")
print("正交向量点积:", np.array([1., 0.]) @ np.array([0., 5.]))

# 投影：b 在 a 方向上的分量
proj = (a @ b) / (a @ a) * a
print("b 在 a 上的投影:", proj, "| 残差与 a 正交:", np.isclose((b - proj) @ a, 0))

# 单位向量化后，点积 = 余弦相似度（向量检索的常用技巧）
na, nb = a / np.linalg.norm(a), b / np.linalg.norm(b)
print("单位化后点积:", round(na @ nb, 4), "== 余弦:", np.isclose(na @ nb, cos))

# 词向量类比的玩具示例：king - man + woman ≈ queen
E = {"king": np.array([0.9, 0.8, 0.1]), "queen": np.array([0.9, 0.1, 0.8]),
     "man": np.array([0.1, 0.9, 0.1]), "woman": np.array([0.1, 0.1, 0.9]), "apple": np.array([0.5, 0.5, 0.5])}
q = E["king"] - E["man"] + E["woman"]
best = max((w for w in E if w not in ("king", "man", "woman")),
           key=lambda w: E[w] @ q / np.linalg.norm(E[w]) / np.linalg.norm(q))
print("king - man + woman 最接近:", best)

# 高维诅咒：随机高维向量几乎两两正交
rng = np.random.default_rng(0)
for d in [2, 100, 4096]:
    V = rng.normal(size=(200, d)); V /= np.linalg.norm(V, axis=1, keepdims=True)
    c = V @ V.T; off = c[~np.eye(200, dtype=bool)]
    print(f"维度 {d:>4}: 随机向量两两余弦的平均绝对值 {np.abs(off).mean():.3f}")
