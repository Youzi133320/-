---
id: k2.ml.diffusers
title: Diffusers：扩散模型工具库
domain: AI/ML库
prerequisites: [k2.ml.pytorch, k2.math.probability, k2.math.loss-function]
related: [k2.ml.transformers, k2.ml.peft, k2.math.normalization]
tags: [Diffusers, 扩散模型, DDPM, UNet, Scheduler, 文生图]
---

# Diffusers：扩散模型工具库

@@DISCLAIMER@@

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

@@CODE:06_diffusers.py@@

输出：

@@OUT:06_diffusers@@

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
