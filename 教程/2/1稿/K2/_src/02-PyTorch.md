---
id: k2.ml.pytorch
title: PyTorch：动态图深度学习框架
domain: AI/ML库
prerequisites: [k1.lib.numpy, k1.prog.oop, k2.math.gradient]
related: [k2.ml.tensorflow, k2.ml.jax, k2.ml.transformers, k2.math.optimization, k2.math.loss-function]
tags: [PyTorch, 张量, autograd, nn.Module, 训练循环, 深度学习]
---

# PyTorch：动态图深度学习框架

@@DISCLAIMER@@

## 一句话定义

PyTorch 是目前最主流的**深度学习框架**：提供可在 CPU/GPU 上运行的张量（Tensor）、自动求导（autograd）、神经网络模块（`nn.Module`）和优化器，用写普通 Python 代码的方式定义和训练模型。

## 为什么重要

- **事实上的研究与大模型标准**：Hugging Face Transformers 从 v5 起只支持 PyTorch 后端（见 [[k2.ml.transformers]]），绝大多数开源大模型以 PyTorch 权重发布。
- **“定义即运行”（eager）易于调试**：可以在任意一行打断点、打印张量形状（见 [[k1.prog.breakpoint]]）。
- **从研究到部署**：`torch.compile` 编译加速，`torch.export` 导出模型。

## 原理 / 图解

【有据可查】官方教程“Learn the Basics”：<https://docs.pytorch.org/tutorials/beginner/basics/intro.html> ；autograd 机制：<https://docs.pytorch.org/docs/stable/notes/autograd.html> 。本文使用 torch 2.14.1 CPU 版（PyPI 发布于 2026-09-30）。

训练循环的五步（几乎所有 PyTorch 训练代码都是这个骨架）：

```mermaid
flowchart LR
    A[取一批数据 x y] --> B[前向<br/>pred = model x]
    B --> C[算损失<br/>loss = loss_fn pred y]
    C --> D[清零梯度<br/>opt.zero_grad]
    D --> E[反向传播<br/>loss.backward]
    E --> F[更新参数<br/>opt.step]
    F --> A
```

autograd 在前向时记录计算图，`backward()` 时按链式法则从损失反向计算每个参数的梯度（原理见 [[k2.math.gradient]]）：

$$
\frac{\partial L}{\partial w} = \frac{\partial L}{\partial \hat{y}} \cdot \frac{\partial \hat{y}}{\partial z} \cdot \frac{\partial z}{\partial w}
$$

## 可运行示例

autograd 求导 + 用小 MLP 分类“两个交错半圆” + 保存/加载（Python 3.13 + torch 2.14.1 CPU 实际运行）：

@@CODE:02_pytorch.py@@

输出：

@@OUT:02_pytorch@@

- autograd 算出的导数 8.0 与手算一致。
- 只有 1218 个参数的网络，200 轮后测试准确率 100%——非线性激活（ReLU）让它能画出弯曲的决策边界。

## 常见误区

- **忘记 `zero_grad()`**：PyTorch 默认**累加**梯度，不清零会让梯度越来越大。
- **推理时不用 `model.eval()` 和 `torch.no_grad()`**：Dropout/BatchNorm 行为不对，且浪费显存记录计算图。
- **形状和设备不一致**：`RuntimeError: Expected all tensors to be on the same device`——模型和数据都要 `.to(device)`。
- **保存整个模型对象**：推荐保存 `state_dict`；加载时 `torch.load(..., weights_only=True)` 更安全（避免反序列化任意代码）。【有据可查】<https://docs.pytorch.org/docs/stable/generated/torch.load.html>
- **用 `.item()` 或 `print` 频繁同步 GPU**：在训练循环中会拖慢速度。

## 与 AI 开发的关系

- **大模型推理与微调的底座**：Transformers、PEFT、Diffusers、vLLM、Accelerate 等都构建在 PyTorch 上。
- **分布式训练**：DDP、FSDP 让模型跨多 GPU / 多机训练。【有据可查】<https://docs.pytorch.org/tutorials/beginner/dist_overview.html>
- **本地部署要谨慎**：CPU 版能跑通小模型和学习用例，但大模型推理/训练通常需要 GPU；个人场景下自购显卡往往不划算，可先用云端或 API。【社区共识】

## 延伸阅读

- PyTorch 官方教程：<https://docs.pytorch.org/tutorials/>
- autograd 机制说明：<https://docs.pytorch.org/docs/stable/notes/autograd.html>
- `torch.compile` 入门：<https://docs.pytorch.org/tutorials/intermediate/torch_compile_tutorial.html>
- 李沐等《动手学深度学习》（PyTorch 版，免费）：<https://zh.d2l.ai/>

## 无法核实 / 待考察点

- 【待考察/推测】torch 2.14 相对 2.13 的主要新特性未逐条核实。
- 【待考察/推测】本示例未在 GPU 上运行，GPU 下的速度与数值细节未验证。
