# PyTorch：张量 + 自动求导 + nn.Module + 训练循环。用一个小 MLP 拟合 XOR 风格的二维分类
import torch, torch.nn as nn
print("torch", torch.__version__, "| CUDA 可用:", torch.cuda.is_available())
torch.manual_seed(0)

# 1) 张量与自动求导
x = torch.tensor(3.0, requires_grad=True)
y = x ** 2 + 2 * x
y.backward()
print("y = x²+2x 在 x=3 的导数(autograd):", x.grad.item(), "(理论 2x+2 = 8)")

# 2) 数据：两个交错的半圆（非线性可分）
n = 400
t = torch.rand(n) * 3.1416
X = torch.cat([torch.stack([t.cos(), t.sin()], 1), torch.stack([1 - t.cos(), 0.5 - t.sin()], 1)]) + 0.1 * torch.randn(2 * n, 2)
Y = torch.cat([torch.zeros(n), torch.ones(n)]).long()
perm = torch.randperm(2 * n); X, Y = X[perm], Y[perm]
Xtr, Ytr, Xte, Yte = X[:600], Y[:600], X[600:], Y[600:]

# 3) 模型
class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(2, 32), nn.ReLU(), nn.Linear(32, 32), nn.ReLU(), nn.Linear(32, 2))
    def forward(self, x): return self.net(x)
model = MLP()
print("参数量:", sum(p.numel() for p in model.parameters()))

# 4) 训练循环：前向 → 损失 → 清梯度 → 反向 → 更新
opt = torch.optim.AdamW(model.parameters(), lr=1e-2)
loss_fn = nn.CrossEntropyLoss()
for epoch in range(1, 201):
    model.train()
    loss = loss_fn(model(Xtr), Ytr)
    opt.zero_grad(); loss.backward(); opt.step()
    if epoch in (1, 50, 200):
        model.eval()
        with torch.no_grad(): acc = (model(Xte).argmax(1) == Yte).float().mean().item()
        print(f"epoch {epoch:>3} 训练损失 {loss.item():.4f} 测试准确率 {acc:.3f}")

# 5) 保存与加载（推荐保存 state_dict）
import io
buf = io.BytesIO(); torch.save(model.state_dict(), buf); buf.seek(0)
m2 = MLP(); m2.load_state_dict(torch.load(buf, weights_only=True))
print("加载后输出一致:", torch.allclose(model(Xte[:5]), m2(Xte[:5])))
