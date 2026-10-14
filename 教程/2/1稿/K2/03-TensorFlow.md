---
id: k2.ml.tensorflow
title: TensorFlow 与 Keras
domain: AI/ML库
prerequisites: [k1.lib.numpy, k2.math.gradient]
related: [k2.ml.pytorch, k2.ml.jax, k2.math.optimization]
tags: [TensorFlow, Keras, GradientTape, tf.function, 计算图, LiteRT]
---

# TensorFlow 与 Keras

> **免责声明**：本文是“河洛序”知识图谱 K2 批次的**初稿**，由 AI 辅助整理，仅供学习参考，不构成任何承诺或保证。版本信息截至 2026-10-14；文中示例已在 Python 3.15.0（数据结构与算法，纯标准库）或 Python 3.13 + 所列库版本（AI/ML 库与数学）下**实际运行**，输出为真实结果，但换机器、换版本时数字（尤其是耗时）会不同。
>
> 标注说明：**【有据可查】** 附官方文档 / 原始出处链接；**【社区共识】** 为业界普遍做法，没有唯一权威出处；**【待考察/推测】** 为未能核实或作者推断，请勿当作定论。

## 一句话定义

TensorFlow 是 Google 开源的**端到端机器学习平台**，Keras 是其上的**高层神经网络 API**：用 `Sequential` 堆叠层、`compile` 配置、`fit` 训练，三步完成大多数模型；底层还有 `GradientTape` 自动求导和 `tf.function` 图编译。

## 为什么重要

- **大量存量项目与生产系统**：2015 年开源以来，许多工业系统、教材和移动端/嵌入式部署方案基于 TensorFlow。
- **端侧部署生态**：TensorFlow Lite（已更名为 LiteRT）、TensorFlow.js 在手机、浏览器、微控制器上运行模型。【有据可查】LiteRT 更名说明：<https://developers.googleblog.com/en/tensorflow-lite-is-now-litert/>
- **Keras 3 是多后端的**：同一份 Keras 代码可在 TensorFlow、JAX、PyTorch 后端上运行。【有据可查】<https://keras.io/getting_started/>

## 原理 / 图解

【有据可查】TensorFlow 2.21.0 于 2026-03-06 发布（移除 Python 3.9 支持、移除 TensorBoard 依赖等）：<https://github.com/tensorflow/tensorflow/releases/tag/v2.21.0> 。本文使用 tensorflow-cpu 2.21.0 + keras 3.15.1。

```mermaid
flowchart TD
    K[Keras 3 高层 API<br/>Sequential compile fit] --> B{后端}
    B --> TF[TensorFlow]
    B --> JX[JAX]
    B --> PT[PyTorch]
    TF --> G[tf.function 图编译 XLA]
    TF --> D[部署<br/>SavedModel LiteRT TF.js]
```

## 可运行示例

`GradientTape` 求导 + Keras 训练一个小分类网络 + `tf.function`（Python 3.13 + tensorflow-cpu 2.21.0 实际运行）：

```python
# 文件：examples/03_tensorflow.py
# TensorFlow + Keras：高层 API 训练一个小模型；GradientTape 自动求导
import os; os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
import numpy as np, tensorflow as tf, keras
print("tensorflow", tf.__version__, "| keras", keras.__version__, "| 后端", keras.backend.backend())
tf.random.set_seed(0); rng = np.random.default_rng(0)

# GradientTape
x = tf.Variable(3.0)
with tf.GradientTape() as tape:
    y = x ** 2 + 2 * x
print("y = x²+2x 在 x=3 的导数:", tape.gradient(y, x).numpy())

# Keras 三步：定义 → compile → fit
X = rng.normal(size=(1000, 4)).astype("float32")
yv = (X[:, 0] * X[:, 1] + X[:, 2] > 0).astype("int32")
model = keras.Sequential([keras.Input(shape=(4,)), keras.layers.Dense(32, activation="relu"),
                          keras.layers.Dense(32, activation="relu"), keras.layers.Dense(2, activation="softmax")])
model.compile(optimizer=keras.optimizers.Adam(1e-2), loss="sparse_categorical_crossentropy", metrics=["accuracy"])
hist = model.fit(X[:800], yv[:800], epochs=20, batch_size=64, verbose=0, validation_split=0.1)
print("参数量:", model.count_params())
print(f"第 1 轮 loss {hist.history['loss'][0]:.4f} → 第 20 轮 loss {hist.history['loss'][-1]:.4f}")
loss, acc = model.evaluate(X[800:], yv[800:], verbose=0)
print(f"测试集准确率 {acc:.3f}")

# tf.function：把 Python 函数编译成计算图
@tf.function
def f(a, b): return tf.reduce_sum(tf.matmul(a, b))
print("tf.function 结果:", f(tf.ones((2, 3)), tf.ones((3, 4))).numpy())
```

输出（开头几行是 TensorFlow 自身打印到 stderr 的 oneDNN 提示，属正常现象）：

```text
WARNING: All log messages before absl::InitializeLog() is called are written to STDERR
I0000 00:00:1791958160.729686  201000 port.cc:153] oneDNN custom operations are on. You may see slightly different numerical results due to floating-point round-off errors from different computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.
WARNING: All log messages before absl::InitializeLog() is called are written to STDERR
I0000 00:00:1791958166.554170  201000 port.cc:153] oneDNN custom operations are on. You may see slightly different numerical results due to floating-point round-off errors from different computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.
tensorflow 2.21.0 | keras 3.15.1 | 后端 tensorflow
y = x²+2x 在 x=3 的导数: 8.0
参数量: 1282
第 1 轮 loss 0.4428 → 第 20 轮 loss 0.0376
测试集准确率 0.960
tf.function 结果: 24.0
```

## 常见误区

- **把 TF1 教程当 TF2 用**：`tf.Session`、`placeholder` 是 TF1 写法，TF2 默认即时执行（eager）。
- **以为 Keras 只能配 TensorFlow**：Keras 3 支持多后端，`keras.backend.backend()` 可查看当前后端。
- **新项目不考虑生态趋势**：大模型生态目前以 PyTorch 为主，Hugging Face Transformers v5 已移除 TensorFlow 支持。【有据可查】<https://github.com/huggingface/transformers/blob/main/MIGRATION_GUIDE_V5.md>
- **GPU 安装踩坑**：TensorFlow 对 CUDA/cuDNN 版本有严格对应要求，应以官方安装页为准：<https://www.tensorflow.org/install/pip>

## 与 AI 开发的关系

- **维护存量模型**：推荐系统、CTR 预估、经典 CV 模型在很多公司仍运行在 TensorFlow 上。
- **端侧与浏览器推理**：LiteRT / TF.js 是把小模型部署到手机和网页的常见路径。
- **新学习者的选择**：【社区共识】若目标是大模型应用与微调，优先学 PyTorch；若工作涉及既有 TF 系统或端侧部署，再补 TensorFlow/Keras。

## 延伸阅读

- TensorFlow 教程：<https://www.tensorflow.org/tutorials>
- Keras 入门：<https://keras.io/getting_started/>
- `tf.function` 指南：<https://www.tensorflow.org/guide/function>
- TF 2.21 发布说明：<https://github.com/tensorflow/tensorflow/releases/tag/v2.21.0>

## 无法核实 / 待考察点

- 【待考察/推测】截至 2026-10-14，TensorFlow 自 2.21.0（2026-03）后未在 PyPI 发布新版本；其后续路线图（如 2.22 计划、长期维护策略）未找到官方明确说明。
