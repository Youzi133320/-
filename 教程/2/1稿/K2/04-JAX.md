---
id: k2.ml.jax
title: JAX：可组合函数变换的数值计算库
domain: AI/ML库
prerequisites: [k1.lib.numpy, k1.prog.functional, k2.math.gradient]
related: [k2.ml.pytorch, k2.ml.tensorflow, k2.math.derivative, k1.py.mutability]
tags: [JAX, grad, jit, vmap, XLA, 函数式, 不可变数组]
---

# JAX：可组合函数变换的数值计算库

> **免责声明**：本文是“河洛序”知识图谱 K2 批次的**初稿**，由 AI 辅助整理，仅供学习参考，不构成任何承诺或保证。版本信息截至 2026-10-14；文中示例已在 Python 3.15.0（数据结构与算法，纯标准库）或 Python 3.13 + 所列库版本（AI/ML 库与数学）下**实际运行**，输出为真实结果，但换机器、换版本时数字（尤其是耗时）会不同。
>
> 标注说明：**【有据可查】** 附官方文档 / 原始出处链接；**【社区共识】** 为业界普遍做法，没有唯一权威出处；**【待考察/推测】** 为未能核实或作者推断，请勿当作定论。

## 一句话定义

JAX 是 Google 开发的**“NumPy + 自动求导 + 编译”**库：用和 NumPy 几乎一样的 `jax.numpy` 写纯函数，再用 `grad`（求导）、`jit`（编译）、`vmap`（自动批量化）等**函数变换**把它变成梯度函数、高速函数或批量函数。

## 为什么重要

- **函数变换可以任意组合**：`jit(vmap(grad(f)))` 一行得到“编译过的、批量的梯度函数”。
- **大规模训练**：在 TPU/GPU 集群上训练大模型时被大量使用（Gemma 等模型的参考实现提供 JAX 版本）。【有据可查】Gemma JAX 实现：<https://github.com/google-deepmind/gemma>
- **科学计算**：物理模拟、可微分编程、概率编程等领域常用。

## 原理 / 图解

【有据可查】JAX 官方文档“关键概念”：<https://docs.jax.dev/en/latest/key-concepts.html> ；“常见坑”（Sharp Bits）：<https://docs.jax.dev/en/latest/notebooks/Common_Gotchas_in_JAX.html> 。本文使用 jax 0.11.2（PyPI 发布于 2026-09-17）。

```mermaid
flowchart LR
    F[纯函数 f x<br/>用 jax.numpy 写] --> G[grad f<br/>导函数]
    F --> J[jit f<br/>XLA 编译]
    F --> V[vmap f<br/>自动批量]
    G --> C[jit vmap grad f<br/>可任意组合]
    J --> C
    V --> C
```

`grad` 的含义：输入函数 $f$，返回导函数 $f'$。对 $f(x)=x^2+3x$：

$$
f'(x) = 2x + 3,\qquad f'(2.5) = 8,\qquad f''(x) = 2
$$

## 可运行示例

`grad`、二阶导、用梯度下降做线性回归、`jit` 加速对比、`vmap`、不可变数组（Python 3.13 + jax 0.11.2 CPU 实际运行）：

```python
# 文件：examples/04_jax.py
# JAX：NumPy 风格 API + 函数变换 grad / jit / vmap，要求纯函数
import time, jax, jax.numpy as jnp
print("jax", jax.__version__, "| 设备", jax.devices())

def f(x): return x ** 2 + 2 * x
print("grad(f)(3.0) =", jax.grad(f)(3.0), "| 二阶导 grad(grad(f))(3.0) =", jax.grad(jax.grad(f))(3.0))

# 线性回归：损失函数是参数的纯函数
key = jax.random.key(0)
k1, k2 = jax.random.split(key)              # 显式随机数 key：可复现
X = jax.random.normal(k1, (200, 3)); w_true = jnp.array([2.0, -1.0, 0.5])
y = X @ w_true + 0.1 * jax.random.normal(k2, (200,))
def loss(w, X, y): return jnp.mean((X @ w - y) ** 2)

@jax.jit
def step(w, X, y, lr=0.1): return w - lr * jax.grad(loss)(w, X, y)
w = jnp.zeros(3)
for _ in range(200): w = step(w, X, y)
print("学到的 w:", w.round(3), "| 真实 w:", w_true)

# jit 加速
def slow(x):
    for _ in range(20): x = jnp.sin(x) * 1.01 + jnp.cos(x)
    return x
fast = jax.jit(slow); xs = jnp.ones((1000, 1000))
fast(xs).block_until_ready()                 # 第一次调用触发编译
t0 = time.perf_counter(); slow(xs).block_until_ready(); t1 = time.perf_counter(); fast(xs).block_until_ready(); t2 = time.perf_counter()
print(f"未 jit {(t1-t0)*1000:.1f} ms | jit 后 {(t2-t1)*1000:.1f} ms")

# vmap：自动向量化（把单样本函数变成批处理）
def per_example_loss(w, x, y): return (x @ w - y) ** 2
batched = jax.vmap(per_example_loss, in_axes=(None, 0, 0))
print("vmap 逐样本损失前 3 个:", batched(w, X, y)[:3].round(5))

# 数组不可变：用 .at[].set() 返回新数组
a = jnp.zeros(3)
try: a[0] = 1
except TypeError as e: print("JAX 数组不可原地修改:", type(e).__name__)
print(".at[0].set(1) ->", a.at[0].set(1.0), "| 原数组仍是", a)
```

输出：

```text
jax 0.11.2 | 设备 [CpuDevice(id=0)]
grad(f)(3.0) = 8.0 | 二阶导 grad(grad(f))(3.0) = 2.0
学到的 w: [ 1.9990001  -1.013       0.50100005] | 真实 w: [ 2.  -1.   0.5]
未 jit 241.6 ms | jit 后 64.7 ms
vmap 逐样本损失前 3 个: [6.459e-02 4.711e-02 5.000e-05]
JAX 数组不可原地修改: TypeError
.at[0].set(1) -> [1. 0. 0.] | 原数组仍是 [0. 0. 0.]
```

- 第一次调用 `jit` 函数包含编译时间，示例中先“预热”再计时；本机 CPU 上 jit 约快 3–4 倍，换硬件会不同。
- JAX 数组不可变，修改要用 `x.at[i].set(v)` 返回新数组（对照 [[k1.py.mutability]]）。

## 常见误区

- **在 jit 函数里写副作用**：`print`、修改全局变量只在“追踪（trace）”时执行一次，之后不再执行。调试用 `jax.debug.print`。
- **用 Python `if` 判断张量值**：jit 下值未知，会报错；改用 `jnp.where` 或 `jax.lax.cond`。
- **随机数用法**：JAX 没有全局随机状态，必须显式传 `key` 并用 `jax.random.split` 拆分。【有据可查】<https://docs.jax.dev/en/latest/random-numbers.html>
- **默认 float32**：与 NumPy 默认 float64 不同，需要双精度时设 `jax_enable_x64`。
- **计时不加 `block_until_ready()`**：JAX 异步执行，不等待结果会测出“假快”。

## 与 AI 开发的关系

- **训练框架生态**：Flax（神经网络）、Optax（优化器）、MaxText（大模型训练）构建于 JAX 之上。【有据可查】<https://github.com/AI-Hypercomputer/maxtext>
- **Keras 3 后端之一**：可以用 Keras 写模型、JAX 跑（见 [[k2.ml.tensorflow]]）。
- **Transformers v5 不再内置 JAX/Flax 模型**，JAX 用户需要通过其他生态工具（如 MaxText）使用开源模型。【有据可查】<https://github.com/huggingface/transformers/blob/main/MIGRATION_GUIDE_V5.md>

## 延伸阅读

- JAX 快速入门：<https://docs.jax.dev/en/latest/quickstart.html>
- JAX 的常见坑：<https://docs.jax.dev/en/latest/notebooks/Common_Gotchas_in_JAX.html>
- 自动微分说明：<https://docs.jax.dev/en/latest/automatic-differentiation.html>
- Flax 文档：<https://flax.readthedocs.io/>

## 无法核实 / 待考察点

- 【待考察/推测】jax 0.11 系列相对 0.10 的不兼容变化未逐条核实。
- 【待考察/推测】JAX 在 GPU/TPU 上相对 PyTorch 的性能优劣与模型和硬件强相关，没有通用结论。
