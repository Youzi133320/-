---
id: k2.ml.diffusers
title: Diffusers：扩散模型工具库
domain: AI/ML库
prerequisites: [k2.ml.pytorch, k2.math.probability, k2.math.loss-function]
related: [k2.ml.transformers, k2.ml.peft, k2.math.normalization]
tags: [Diffusers, 扩散模型, DDPM, UNet, Scheduler, 文生图]
---

# Diffusers：扩散模型工具库

> **免责声明**：本文是“河洛序”知识图谱 K2 批次的**初稿**，由 AI 辅助整理，仅供学习参考，不构成任何承诺或保证。版本信息截至 2026-10-14；文中示例已在 Python 3.15.0（数据结构与算法，纯标准库）或 Python 3.13 + 所列库版本（AI/ML 库与数学）下**实际运行**，输出为真实结果，但换机器、换版本时数字（尤其是耗时）会不同。
>
> 标注说明：**【有据可查】** 附官方文档 / 原始出处链接；**【社区共识】** 为业界普遍做法，没有唯一权威出处；**【待考察/推测】** 为未能核实或作者推断，请勿当作定论。

## 一句话定义

Diffusers 是 Hugging Face 的**扩散模型库**：把“去噪网络（UNet / Transformer）+ 噪声调度器（Scheduler）+ 推理流水线（Pipeline）”模块化，用于图像、视频、音频生成以及训练自己的扩散模型。

## 为什么重要

- **文生图 / 图生图的主流实现方式**：Stable Diffusion、FLUX 等开源图像模型通常提供 Diffusers 格式。
- **组件可替换**：同一个模型可以换不同调度器，在速度和质量间取舍。
- **理解生成式 AI 原理的入口**：扩散模型的核心公式可以用很小的代码观察。

## 原理 / 图解

【有据可查】DDPM 论文（Ho 等，2020）：<https://arxiv.org/abs/2006.11239> ；Diffusers 文档：<https://huggingface.co/docs/diffusers/index> 。本文使用 diffusers 0.41.0（PyPI 发布于 2026-10-06）。

**前向过程**逐步加噪；**反向过程**训练网络预测噪声并逐步去噪：

```mermaid
flowchart LR
    X0[清晰图像 x0] -->|加噪| X1[x1] -->|加噪| XM[...] -->|加噪| XT[纯噪声 xT]
    XT -.网络预测噪声 去噪.-> XM2[...]
    XM2 -.去噪.-> Y0[生成图像]
```

DDPM 允许一步直接从 $x_0$ 得到任意时刻 $t$ 的加噪图像，$\bar\alpha_t$ 从接近 1 逐渐降到接近 0：

$$
x_t = \sqrt{\bar\alpha_t}\,x_0 + \sqrt{1-\bar\alpha_t}\,\varepsilon,\qquad \varepsilon \sim \mathcal{N}(0, I)
$$

训练目标（简化版）是让网络预测出加进去的噪声：

$$
L = \mathbb{E}_{x_0,\varepsilon,t}\left[\lVert \varepsilon - \varepsilon_\theta(x_t, t) \rVert^2\right]
$$

## 可运行示例

本地构造一个 16 万参数的微型 UNet（随机初始化，无需下载），查看噪声调度、做 30 步训练、跑 20 步采样（Python 3.13 + diffusers 0.41.0 + torch CPU 实际运行）：

```python
# 文件：examples/06_diffusers.py
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
```

输出：

```text
diffusers 0.41.0
微型 UNet 参数量: 164,563
t=  0: ᾱ_t=0.9999, 信号占比 sqrt(ᾱ)=1.000, x_t 标准差 0.010
t=250: ᾱ_t=0.5214, 信号占比 sqrt(ᾱ)=0.722, x_t 标准差 0.704
t=500: ᾱ_t=0.0778, 信号占比 sqrt(ᾱ)=0.279, x_t 标准差 0.977
t=999: ᾱ_t=0.0000, 信号占比 sqrt(ᾱ)=0.006, x_t 标准差 1.018
训练第 1 步 噪声预测 MSE 1.2351
训练第 30 步 噪声预测 MSE 0.5230
采样完成，输出形状 (1, 3, 16, 16) 数值范围 -1.0 ~ 1.0 (未训练充分，图像无意义)
```

- $\bar\alpha_t$ 在 t=0 时 ≈1（几乎无噪），t=999 时 ≈0（几乎纯噪声），与公式一致。
- 30 步训练损失下降只说明“网络开始学”，生成真正图像需要大量数据和长时间训练；示例输出只是检验流程。

## 常见误区

- **以为采样步数越多越好**：现代调度器（如 DPM-Solver 系列）几十步就能得到不错结果，步数增加的边际收益递减。【社区共识】
- **低估显存需求**：大型文生图模型推理常需 8GB 以上显存，本地部署请按模型卡要求保守评估，个人可先用在线服务。【社区共识】
- **忽视模型许可证与内容安全策略**：开源权重各有许可条款，生成内容同样要遵守法律与平台规则。
- **把 `safety_checker` 等安全组件当作可随意移除的“限制”**：本文不提供绕过安全措施的方法。

## 与 AI 开发的关系

- **图像生成应用**：通过 Pipeline 封装文生图、图像修复、风格迁移等能力。
- **LoRA 风格微调**：Diffusers 与 PEFT 集成，可加载/训练 LoRA 适配器（见 [[k2.ml.peft]]）。
- **理解多模态模型**：扩散、流匹配（flow matching）是图像/视频生成模型的核心范式之一。

## 延伸阅读

- Diffusers 文档：<https://huggingface.co/docs/diffusers/index>
- DDPM 论文：<https://arxiv.org/abs/2006.11239>
- Hugging Face 扩散模型课程：<https://huggingface.co/learn/diffusion-course/unit0/1>
- Lilian Weng《What are Diffusion Models?》：<https://lilianweng.github.io/posts/2021-07-11-diffusion-models/>

## 无法核实 / 待考察点

- 【待考察/推测】diffusers 0.41 的新增模型与调度器清单未逐条核实。
- 【待考察/推测】未在 GPU 上运行任何真实大模型 Pipeline，相关显存数字为社区经验，非实测。
