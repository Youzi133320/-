# Diffusers：扩散模型工具箱。用随机初始化的微型 UNet + DDPM 调度器演示"加噪 → 去噪"流程（CPU）
import torch, diffusers
from diffusers import UNet2DModel, DDPMScheduler
print("diffusers", diffusers.__version__)
torch.manual_seed(0)

unet = UNet2DModel(sample_size=16, in_channels=3, out_channels=3, layers_per_block=1,
                   block_out_channels=(16, 32), down_block_types=("DownBlock2D", "DownBlock2D"),
                   up_block_types=("UpBlock2D", "UpBlock2D"), norm_num_groups=8)
print("微型 UNet 参数量:", f"{sum(p.numel() for p in unet.parameters()):,}")
sched = DDPMScheduler(num_train_timesteps=1000)

# 前向加噪：x_t = sqrt(ᾱ_t) x_0 + sqrt(1-ᾱ_t) ε
x0 = torch.zeros(1, 3, 16, 16) + 0.5
noise = torch.randn_like(x0)
for t in [0, 250, 500, 999]:
    xt = sched.add_noise(x0, noise, torch.tensor([t]))
    ab = sched.alphas_cumprod[t].item()
    print(f"t={t:>3}: ᾱ_t={ab:.4f}, 信号占比 sqrt(ᾱ)={ab**0.5:.3f}, x_t 标准差 {xt.std().item():.3f}")

# 训练一步：让 UNet 预测噪声（MSE 损失）
opt = torch.optim.AdamW(unet.parameters(), lr=1e-3)
imgs = torch.rand(4, 3, 16, 16) * 2 - 1
for step in range(1, 31):
    t = torch.randint(0, 1000, (4,))
    eps = torch.randn_like(imgs)
    pred = unet(sched.add_noise(imgs, eps, t), t).sample
    loss = torch.nn.functional.mse_loss(pred, eps)
    opt.zero_grad(); loss.backward(); opt.step()
    if step in (1, 30): print(f"训练第 {step} 步 噪声预测 MSE {loss.item():.4f}")

# 反向采样：从纯噪声出发，逐步去噪（只用 20 步演示）
sched.set_timesteps(20)
x = torch.randn(1, 3, 16, 16)
with torch.no_grad():
    for t in sched.timesteps:
        x = sched.step(unet(x, t).sample, t, x).prev_sample
print("采样完成，输出形状", tuple(x.shape), "数值范围", round(x.min().item(), 2), "~", round(x.max().item(), 2), "(未训练充分，图像无意义)")
