---
id: k2.ml.sklearn
title: Scikit-learn：经典机器学习工具箱
domain: AI/ML库
prerequisites: [k1.lib.numpy, k1.lib.pandas, k2.math.statistics]
related: [k2.math.regularization, k2.math.normalization, k2.math.loss-function, k2.ml.pytorch]
tags: [scikit-learn, sklearn, 分类, 回归, 交叉验证, Pipeline, fit/predict]
---

# Scikit-learn：经典机器学习工具箱

@@DISCLAIMER@@

## 一句话定义

scikit-learn（sklearn）是 Python 最常用的**经典机器学习库**：线性模型、决策树、随机森林、SVM、聚类、降维、预处理、评估指标，都通过同一套 `fit / predict / transform` 接口来使用。

## 为什么重要

- **表格数据的首选**：结构化数据（用户画像、风控、销量预测）上，经典模型加好的特征工程往往又快又准，未必需要深度学习。
- **方法论的“标准答案”**：训练/测试划分、交叉验证、流水线、指标——这些规范大多以 sklearn 的写法为参照。
- **深度学习项目也离不开它**：数据划分、标准化、评估指标（F1、AUC）、做基线模型（baseline）。

## 原理 / 图解

【有据可查】sklearn 的统一 API 设计（Estimator / Predictor / Transformer）见其 API 设计论文与开发者文档：<https://scikit-learn.org/stable/developers/develop.html> ；用户指南：<https://scikit-learn.org/stable/user_guide.html> 。本文使用 scikit-learn 1.9.1（PyPI 发布于 2026-09-10）。

```mermaid
flowchart LR
    D[原始数据 X y] --> S[train_test_split<br/>划分训练与测试]
    S --> P[Pipeline]
    subgraph P[Pipeline 流水线]
      T[StandardScaler<br/>fit 只在训练集] --> M[模型<br/>LogisticRegression]
    end
    P --> CV[cross_val_score<br/>K 折交叉验证选模型]
    CV --> F[在测试集上评估一次<br/>准确率 混淆矩阵 F1]
```

| 接口 | 作用 | 例子 |
|---|---|---|
| `fit(X, y)` | 从数据中学习参数 | 所有模型、预处理器 |
| `predict(X)` / `predict_proba(X)` | 预测类别 / 概率 | 分类器、回归器 |
| `transform(X)` | 变换数据 | `StandardScaler`、`PCA` |
| `score(X, y)` | 默认指标 | 分类为准确率、回归为 R² |

## 可运行示例

鸢尾花分类：两个模型的交叉验证、测试集评估、混淆矩阵与特征重要性（Python 3.13 + scikit-learn 1.9.1 实际运行）：

@@CODE:01_sklearn.py@@

输出：

@@OUT:01_sklearn@@

读结果：两个模型在这个小数据集上表现几乎一样；混淆矩阵显示唯一的错误是把一个 virginica 判成 versicolor——这两类本来就在花瓣尺寸上有重叠。随机森林认为花瓣长度/宽度最重要。

## 常见误区

- **数据泄漏**：先在全量数据上 `StandardScaler().fit` 再划分，测试集信息就泄漏进了训练。把预处理放进 `Pipeline`，交叉验证时每折都只在训练部分上 fit。【有据可查】官方“常见陷阱”文档：<https://scikit-learn.org/stable/common_pitfalls.html>
- **只看准确率**：类别不平衡时（如 1% 欺诈），全部预测“正常”也有 99% 准确率，要看精确率、召回率、F1、PR 曲线。
- **在测试集上反复调参**：测试集只用最后一次；调参用交叉验证或独立验证集。
- **线性模型 / SVM / KNN 不做标准化**：特征尺度差异会严重影响结果（见 [[k2.math.normalization]]）。
- **用 sklearn 训练大规模深度网络**：`MLPClassifier` 只适合小规模实验，深度学习请用 PyTorch 等。

## 与 AI 开发的关系

- **基线模型**：上大模型之前，先用 TF-IDF + 逻辑回归做文本分类基线，常常能发现“任务其实很简单”或“数据标注有问题”。【社区共识】
- **嵌入向量 + 经典模型**：用 LLM/嵌入模型提取向量，再用 sklearn 的逻辑回归、KMeans 做分类或聚类，是低成本且效果不错的组合。
- **评估工具箱**：`classification_report`、`roc_auc_score`、`confusion_matrix` 被大量深度学习项目直接调用。
- **降维可视化**：`PCA`、`TSNE` 把高维嵌入降到 2D 查看（原理见 [[k2.math.eigenvalue]]）。

## 延伸阅读

- 用户指南：<https://scikit-learn.org/stable/user_guide.html>
- 选择合适的估计器（流程图）：<https://scikit-learn.org/stable/machine_learning_map.html>
- 常见陷阱与推荐做法：<https://scikit-learn.org/stable/common_pitfalls.html>
- 交叉验证：<https://scikit-learn.org/stable/modules/cross_validation.html>

## 无法核实 / 待考察点

- 【待考察/推测】scikit-learn 1.9 相对 1.8 的新特性（如 Array API 支持进度、GPU 支持范围）未逐条核实。
