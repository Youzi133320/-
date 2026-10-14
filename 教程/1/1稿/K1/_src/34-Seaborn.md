---
id: k1.lib.seaborn
title: Seaborn：统计可视化
domain: Python数据与可视化
prerequisites: [k1.lib.matplotlib, k1.lib.pandas]
related: [k1.lib.plotly]
tags: [Seaborn, 统计图表, 箱线图, 分布图, 置信区间, 长格式数据]
---

# Seaborn：统计可视化

@@DISCLAIMER@@

## 一句话定义

Seaborn 是**建立在 Matplotlib 之上的统计图表库**：直接接收 Pandas 表格，一行代码就能按类别分组、着色，画出箱线图、分布图、带置信区间的均值图等统计图形，并自带美观的主题。

## 为什么重要

- **少写代码就能做“分组对比”**：`hue="模型"` 一个参数就完成按模型着色分组，用纯 Matplotlib 要写循环。
- **内置统计计算**：均值的置信区间、核密度估计（KDE）、回归拟合线自动算好。
- **探索性数据分析（EDA）利器**：快速看清分布、异常值、组间差异。

## 原理 / 图解

【有据可查】官方介绍：<https://seaborn.pydata.org/tutorial/introduction.html> 。Seaborn 按图形用途分为几大函数族：关系（`relplot`）、分布（`displot`）、类别（`catplot`），每族有对应的 Axes 级函数（如 `boxplot`、`histplot`、`barplot`）。0.12 起还提供了声明式的 `seaborn.objects` 接口：<https://seaborn.pydata.org/tutorial/objects_interface.html>

```mermaid
flowchart LR
    D[长格式 DataFrame<br/>每行一个观测] --> S[seaborn 函数<br/>x y hue 映射到列名]
    S --> ST[统计变换<br/>分组 均值 置信区间 KDE]
    ST --> M[Matplotlib Axes 绘制]
    M --> O[可以继续用 Matplotlib 微调]
```

**长格式（long-form / tidy）数据**是 Seaborn 的关键：每行一个观测，每列一个变量（模型、任务、得分），而不是“每个模型一列”的宽表。【有据可查】<https://seaborn.pydata.org/tutorial/data_structure.html>

| 想看什么 | 函数 |
|---|---|
| 组间分布与异常值 | `boxplot`、`violinplot` |
| 单变量分布 | `histplot`（可加 `kde=True`） |
| 组均值与不确定性 | `barplot`、`pointplot`（默认带误差线） |
| 两变量关系 | `scatterplot`、`regplot`、`lineplot` |
| 矩阵 | `heatmap` |

## 可运行示例

用模拟的“3 个模型 × 3 类任务 × 每组 30 次评测”数据画三张图（Python 3.13.5 + seaborn 0.13.2 实际运行）：

@@CODE:34_seaborn.py@@

输出：

@@OUT:34_seaborn@@

生成的图片：

![Seaborn 示例：箱线图、分布图、均值与置信区间](img/seaborn-demo.png)

- 左：箱线图显示每组的中位数、四分位范围和异常点（小圆圈）。
- 中：直方图 + KDE 曲线显示耗时呈右偏分布（多数快、少数很慢）——这正是 API 延迟的常见形态。
- 右：柱高是均值，黑色竖线是 95% 置信区间（Seaborn 通过自助法 bootstrap 计算）。**区间重叠很多的两组，差异可能并不可靠。**

## 常见误区

- **把宽表直接丢给 Seaborn**：先用 `df.melt(...)` 转成长格式。
- **只看均值柱状图**：均值会掩盖分布形态和异常值，配合箱线图或分布图一起看。
- **误读误差线**：Seaborn 0.12 起用 `errorbar=` 参数明确指定误差线含义（`"ci"`、`"sd"`、`"se"`、`"pi"`），报告中应写清楚是哪一种。【有据可查】<https://seaborn.pydata.org/tutorial/error_bars.html>
- **以为 Seaborn 在高频迭代**：截至 2026-10-13，PyPI 上最新版仍为 0.13.2（2024-01-25 发布）。它仍可正常使用，但新特性节奏较慢。
- **中文乱码**：与 Matplotlib 相同，需要在 `sns.set_theme(font=...)` 中指定中文字体。

## 与 AI 开发的关系

- **模型评测报告**：多模型 × 多任务的得分分布与置信区间，是判断“A 模型是否真的比 B 好”的基本工具——单次评测的平均分差距可能只是噪声。
- **数据集 EDA**：文本长度分布、标签分布、各来源数据量，训练前先画一遍能发现很多数据问题。
- **相关性热力图**：查看特征之间、评测指标之间的相关性（注意：随机噪声数据也可能出现看似明显的相关，需要足够样本量）。

## 延伸阅读

- Seaborn 教程：<https://seaborn.pydata.org/tutorial.html>
- 误差线说明：<https://seaborn.pydata.org/tutorial/error_bars.html>
- 数据结构（长格式与宽格式）：<https://seaborn.pydata.org/tutorial/data_structure.html>
- Hadley Wickham, *Tidy Data*（2014，长格式数据思想的经典论文）：<https://www.jstatsoft.org/article/view/v059i10>

## 无法核实 / 待考察点

- 【待考察/推测】Seaborn 是否有 0.14 / 1.0 的发布计划，未找到官方明确说明。
- 【待考察/推测】seaborn 0.13.2 与 pandas 3.x 的全部兼容性未全面测试，本文示例在 pandas 3.0.6 下运行正常。
