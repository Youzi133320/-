# 归一化：把数据或中间激活调整到统一尺度。特征缩放 / BatchNorm / LayerNorm / RMSNorm
import numpy as np
np.set_printoptions(precision=4, suppress=True)
rng = np.random.default_rng(0)

# 1) 特征缩放：面积(平方米) 与 房间数 尺度差百倍
X = np.c_[rng.uniform(30, 200, 6), rng.integers(1, 6, 6)]
minmax = (X - X.min(0)) / (X.max(0) - X.min(0))
zscore = (X - X.mean(0)) / X.std(0)
print("原始:\n", X[:3], "\nMin-Max 到 [0,1]:\n", minmax[:3], "\nZ-score（均值0方差1）:\n", zscore[:3])
print("Z-score 后各列均值", zscore.mean(0).round(6), "标准差", zscore.std(0))

# 2) 尺度不一致让梯度下降很难：条件数对比
def steps_to_converge(X, y, lr):
    w = np.zeros(X.shape[1])
    for t in range(1, 100_001):
        g = X.T @ (X @ w - y) / len(y); w -= lr * g
        if np.linalg.norm(g) < 1e-6: return t
    return ">100000"
Xr = np.c_[rng.uniform(30, 200, 200), rng.integers(1, 6, 200)]; yr = Xr @ np.array([0.5, 10.0])
Xs = (Xr - Xr.mean(0)) / Xr.std(0); ys = yr - yr.mean()
print(f"\n条件数：原始 {np.linalg.cond(Xr.T @ Xr):.0f} | 标准化后 {np.linalg.cond(Xs.T @ Xs):.2f}")
print("梯度下降收敛步数：原始(lr=1e-5)", steps_to_converge(Xr, yr, 1e-5), "| 标准化后(lr=0.5)", steps_to_converge(Xs, ys, 0.5))

# 3) BatchNorm vs LayerNorm vs RMSNorm：沿不同的轴做归一化
H = rng.normal(5, 3, size=(4, 6))                      # (batch=4, features=6)
eps = 1e-5
bn = (H - H.mean(0)) / np.sqrt(H.var(0) + eps)         # 每个特征跨 batch
ln = (H - H.mean(1, keepdims=True)) / np.sqrt(H.var(1, keepdims=True) + eps)   # 每个样本跨特征
rms = H / np.sqrt((H ** 2).mean(1, keepdims=True) + eps)                     # 只除以均方根，不减均值
print("\nBatchNorm 后每列均值:", bn.mean(0).round(6))
print("LayerNorm 后每行均值:", ln.mean(1).round(6), "每行标准差:", ln.std(1).round(4))
print("RMSNorm 后每行均方根:", np.sqrt((rms ** 2).mean(1)).round(4), "（均值不为 0:", rms.mean(1).round(3), ")")

# 4) 与 PyTorch 对照验证（如已安装）
try:
    import torch
    t = torch.tensor(H, dtype=torch.float32)
    print("与 torch.nn.functional.layer_norm 一致:", np.allclose(torch.nn.functional.layer_norm(t, (6,)).numpy(), ln, atol=1e-4))
    if hasattr(torch.nn.functional, "rms_norm"):
        print("与 torch.nn.functional.rms_norm 一致:", np.allclose(torch.nn.functional.rms_norm(t, (6,), eps=eps).numpy(), rms, atol=1e-4))
except ImportError:
    print("未安装 PyTorch，跳过对照")

# 5) 向量 L2 归一化：嵌入检索前的常见步骤
E = rng.normal(size=(3, 4)); En = E / np.linalg.norm(E, axis=1, keepdims=True)
print("\nL2 归一化后各向量长度:", np.linalg.norm(En, axis=1))
