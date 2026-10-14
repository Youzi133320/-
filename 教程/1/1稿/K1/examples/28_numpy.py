# NumPy：n 维数组 + 向量化运算 + 广播
import time
import numpy as np
print("NumPy", np.__version__)

a = np.arange(12).reshape(3, 4)
print("数组:\n", a, "\n形状", a.shape, "类型", a.dtype)
print("按列求和:", a.sum(axis=0), "| 按行均值:", a.mean(axis=1))
print("布尔索引 (>5):", a[a > 5])

# 广播：形状 (3,4) 与 (4,) 自动对齐
col_mean = a.mean(axis=0)
print("每列减去列均值:\n", a - col_mean)

# 向量化 vs Python 循环
x = np.random.default_rng(0).random(1_000_000)
t0 = time.perf_counter(); s1 = sum(v * v for v in x); t_loop = time.perf_counter() - t0
t0 = time.perf_counter(); s2 = float(np.dot(x, x)); t_vec = time.perf_counter() - t0
print(f"循环 {t_loop * 1000:.0f} ms | 向量化 {t_vec * 1000:.1f} ms | 结果一致: {np.isclose(s1, s2)}")

# AI 里最常见的操作：余弦相似度（embedding 检索的核心）
emb = np.random.default_rng(1).normal(size=(5, 8))
q = emb[2] + 0.01
sims = emb @ q / (np.linalg.norm(emb, axis=1) * np.linalg.norm(q))
print("与查询最相似的向量下标:", int(np.argmax(sims)), "相似度", sims.round(3))

# 视图与拷贝
b = a[:, :2]; b[0, 0] = 999
print("切片是视图，原数组被改:", a[0, 0], "| 共享内存:", np.shares_memory(a, b))
