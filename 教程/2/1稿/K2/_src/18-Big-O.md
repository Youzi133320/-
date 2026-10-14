---
id: k2.algo.big-o
title: Big O：时间与空间复杂度
domain: 算法
prerequisites: [k2.ds.array]
related: [k2.algo.quicksort, k2.algo.binary-search, k2.ds.hash-table, k2.ml.transformers]
tags: [Big O, 时间复杂度, 空间复杂度, 渐进分析, 摊还分析, 注意力复杂度]
---

# Big O：时间与空间复杂度

@@DISCLAIMER@@

## 一句话定义

Big O 描述**当输入规模 $n$ 增大时，算法所需时间或空间的增长速度上界**，忽略常数和低阶项。比如 $O(n^2)$ 意味着数据翻倍，耗时大约变成 4 倍。

## 为什么重要

- **预测“能不能跑完”**：$n=10^6$ 时 $O(n\log n)$ 约 2000 万次操作，几秒内完成；$O(n^2)$ 是 $10^{12}$ 次，要跑几个小时甚至更久。
- **选择数据结构的依据**：list 查找 $O(n)$ vs set 查找 $O(1)$（见 [[k2.ds.hash-table]]）。
- **理解大模型成本**：标准自注意力对上下文长度是 $O(n^2)$。

## 原理 / 图解

形式化定义：若存在常数 $c>0$ 和 $n_0$，使得对所有 $n \ge n_0$ 都有 $f(n) \le c \cdot g(n)$，则记 $f(n) = O(g(n))$：

$$
f(n) = O(g(n)) \iff \exists\, c>0,\ n_0,\ \forall n \ge n_0:\ f(n) \le c\, g(n)
$$

例：$3n^2 + 5n + 100 = O(n^2)$，因为 $n$ 大了以后 $n^2$ 项主导一切。

```mermaid
flowchart LR
    A[O 1<br/>字典查找] --> B[O log n<br/>二分搜索] --> C[O n<br/>遍历] --> D[O n log n<br/>排序] --> E[O n²<br/>两两比较] --> F[O 2^n<br/>枚举子集]
```

| 复杂度 | 名称 | 典型例子 |
|---|---|---|
| $O(1)$ | 常数 | 数组下标访问、哈希查找 |
| $O(\log n)$ | 对数 | 二分搜索、平衡树操作 |
| $O(n)$ | 线性 | 遍历、线性搜索 |
| $O(n \log n)$ | 线性对数 | 归并排序、快速排序（平均） |
| $O(n^2)$ | 平方 | 冒泡排序、双重循环、标准注意力 |
| $O(2^n)$ | 指数 | 朴素递归斐波那契、子集枚举 |

【有据可查】Python 内置类型操作的复杂度表：<https://wiki.python.org/moin/TimeComplexity>

## 可运行示例

“倍增实验”：把 $n$ 从 1000 翻倍到 2000，观察不同复杂度算法的耗时倍数；再打印增长表与注意力矩阵规模（Python 3.15.0 实际运行）：

@@CODE:18_big_o.py@@

输出：

@@OUT:18_big_o@@

- $O(n)$、$O(n\log n)$ 翻倍后约 2 倍，$O(n^2)$ 约 4.5 倍，与理论吻合。
- $O(1)$ 那一行的 0.4 倍是**测量噪声**：耗时太短（亚微秒级），计时误差占主导。
- 上下文从 8K 到 128K（16 倍），注意力分数矩阵元素多了 256 倍。

## 常见误区

- **Big O 小就一定快**：常数因子很重要。小规模时 $O(n^2)$ 的插入排序可能比 $O(n\log n)$ 算法快（Timsort 对短片段就用插入排序）。
- **忽略最坏情况**：快速排序平均 $O(n\log n)$，最坏 $O(n^2)$（见 [[k2.algo.quicksort]]）。
- **混淆平均、最坏、摊还**：`list.append` 是摊还 $O(1)$，单次扩容时是 $O(n)$。
- **只看时间不看空间**：归并排序需要 $O(n)$ 额外空间。
- **忘了隐藏循环**：`x in list`、`list.index`、字符串拼接 `s += t` 在循环中都可能让复杂度悄悄升阶。

## 与 AI 开发的关系

- **注意力的平方代价**：标准自注意力计算和存储 $n\times n$ 分数矩阵，时间 $O(n^2 d)$。FlashAttention 不改变计算量的阶，但通过分块避免显式存储整个矩阵，降低显存占用和 IO。【有据可查】<https://arxiv.org/abs/2205.14135>
- **向量检索**：暴力检索每次查询 $O(Nd)$；HNSW 等近似索引把查询降到经验上的亚线性。
- **数据处理管道**：千万级日志或语料上，一个 $O(n^2)$ 去重就可能让任务跑不完。

## 延伸阅读

- Python Wiki 时间复杂度：<https://wiki.python.org/moin/TimeComplexity>
- Big-O Cheat Sheet：<https://www.bigocheatsheet.com/>
- 维基百科：大 O 符号 <https://en.wikipedia.org/wiki/Big_O_notation>

## 无法核实 / 待考察点

- 【待考察/推测】倍增实验中的具体倍数受 CPU 缓存、频率调节影响，不同机器差异很大。
