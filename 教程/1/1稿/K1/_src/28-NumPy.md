---
id: k1.lib.numpy
title: NumPy：数值计算的地基
domain: Python数据与可视化
prerequisites: [k1.py.object-reference, k1.py.iterator]
related: [k1.lib.pandas, k1.lib.pyarrow, k1.lib.matplotlib, k1.py.multiprocessing]
tags: [NumPy, ndarray, 向量化, 广播, dtype, 视图, 余弦相似度]
---

# NumPy：数值计算的地基

@@DISCLAIMER@@

## 一句话定义

NumPy 是 Python 的**多维数组（ndarray）与向量化数学运算库**：它把一大块同类型数字放在连续内存里，用 C 写的循环一次性处理整个数组，比纯 Python 循环快几十到几百倍。

## 为什么重要

- **整个 Python 科学计算与 AI 生态的地基**：Pandas、SciPy、scikit-learn、Matplotlib 都建立在 NumPy 之上；PyTorch 张量和 JAX 数组的 API 也大量借鉴 NumPy。
- **“数组思维”是 AI 编程的基本功**：形状（shape）、轴（axis）、广播（broadcasting）这些概念会一直伴随你进入深度学习。
- **数组接口标准**：其他库通过数组协议与 NumPy 互通。【有据可查】Python 数组 API 标准：<https://data-apis.org/array-api/latest/>

## 原理 / 图解

【有据可查】NumPy 官方入门：<https://numpy.org/doc/stable/user/absolute_beginners.html> ；本文使用 NumPy 2.5.4（PyPI 发布于 2026-10-10）。NumPy 2.0（2024 年 6 月）是 2006 年以来首个大版本，调整了类型提升规则并清理了大量 API：<https://numpy.org/doc/stable/numpy_2_0_migration_guide.html>

**为什么快**：

```mermaid
flowchart LR
    subgraph Python列表
      L1[指针] --> O1[int 对象<br/>类型信息 引用计数 值]
      L2[指针] --> O2[int 对象]
      L3[指针] --> O3[int 对象]
    end
    subgraph NumPy数组
      H[头信息<br/>dtype shape strides] --> B[连续内存<br/>8字节 8字节 8字节 ...]
    end
    B --> V[C 循环加 SIMD 指令<br/>一次处理整块]
```

**广播规则**：从最后一个维度开始对齐，每个维度要么相等、要么其中一个为 1（会被“拉伸”），否则报错。【有据可查】<https://numpy.org/doc/stable/user/basics.broadcasting.html>

| 形状 A | 形状 B | 结果 |
|---|---|---|
| (3, 4) | (4,) | (3, 4)：B 被复制到每一行 |
| (3, 1) | (1, 4) | (3, 4)：两边都被拉伸 |
| (3, 4) | (3,) | 报错：最后一维 4 与 3 不匹配 |

## 可运行示例

@@CODE:28_numpy.py@@

输出（Python 3.13.5 + NumPy 2.5.4）：

@@OUT:28_numpy@@

- 100 万个数的平方和：Python 循环约 108 ms，`np.dot` 约 0.4 ms，**快两百多倍**（具体倍数因机器而异）。
- 余弦相似度那几行就是向量检索（RAG）最核心的计算：查询向量与所有文档向量做一次矩阵乘法。
- 最后一行：切片 `a[:, :2]` 是**视图**，修改它会改到原数组。【有据可查】<https://numpy.org/doc/stable/user/basics.copies.html>

## 常见误区

- **在 NumPy 数组上写 Python for 循环**：失去了全部速度优势。先想“能不能用整个数组的运算表达”。
- **搞混 `axis`**：`axis=0` 是“沿着行的方向压缩”（结果是每列一个值），初学者常常理解反。
- **以为切片会复制**：NumPy 基本切片返回视图（与 Python 列表切片相反）；需要独立副本时用 `.copy()`。花式索引（布尔/整数数组索引）则返回副本。
- **dtype 溢出**：`int8`、`uint8` 等小整数类型会静默溢出（例如图像像素相加超过 255）。
- **用 `np.random.seed` 全局种子**：推荐使用 `np.random.default_rng(seed)` 生成器对象。【有据可查】<https://numpy.org/doc/stable/reference/random/index.html>

## 与 AI 开发的关系

- **嵌入向量与相似度检索**：小规模 RAG 原型完全可以只用 NumPy 做暴力检索；规模变大再换 FAISS 或向量数据库。
- **与 PyTorch 互转**：`torch.from_numpy(arr)` 与 `tensor.numpy()` 在 CPU 上**共享内存**，改一边另一边也变。【有据可查】<https://docs.pytorch.org/docs/stable/generated/torch.from_numpy.html>
- **数据预处理**：图像就是 `(高, 宽, 通道)` 的 uint8 数组，音频就是一维 float 数组，很多预处理都是 NumPy 运算。
- **评估指标计算**：准确率、混淆矩阵、困惑度等常用 NumPy 一行完成。

## 延伸阅读

- NumPy 入门（绝对新手版）：<https://numpy.org/doc/stable/user/absolute_beginners.html>
- 广播规则：<https://numpy.org/doc/stable/user/basics.broadcasting.html>
- 视图与副本：<https://numpy.org/doc/stable/user/basics.copies.html>
- Nicolas P. Rougier, *From Python to NumPy*（免费在线书）：<https://www.labri.fr/perso/nrougier/from-python-to-numpy/>

## 无法核实 / 待考察点

- 【待考察/推测】NumPy 2.5 系列相对 2.0 的具体新增功能本文未逐条核对，以官方 release notes 为准：<https://numpy.org/doc/stable/release.html>
