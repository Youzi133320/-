# Seaborn：基于 Matplotlib 的统计可视化，一行代码画分组/分布/相关
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np, pandas as pd
from matplotlib import font_manager
print("seaborn", sns.__version__)

cjk = [f.name for f in font_manager.fontManager.ttflist if "CJK SC" in f.name]
sns.set_theme(style="whitegrid", font=cjk[0] if cjk else None, rc={"axes.unicode_minus": False})

rng = np.random.default_rng(42)
rows = []
for model, base in [("A", 80), ("B", 72), ("C", 86)]:
    for task, shift in [("代码", 0), ("对话", 5), ("数学", -8)]:
        for _ in range(30):
            rows.append({"模型": model, "任务": task,
                         "得分": rng.normal(base + shift, 6), "耗时秒": rng.gamma(2, 1.5)})
df = pd.DataFrame(rows)

fig, axes = plt.subplots(1, 3, figsize=(15, 4.2), constrained_layout=True)
sns.boxplot(data=df, x="任务", y="得分", hue="模型", ax=axes[0]); axes[0].set_title("各任务得分分布")
sns.histplot(data=df, x="耗时秒", hue="模型", kde=True, element="step", ax=axes[1]); axes[1].set_title("耗时分布")
sns.barplot(data=df, x="模型", y="得分", hue="任务", errorbar=("ci", 95), ax=axes[2]); axes[2].set_title("均值与 95% 置信区间")
axes[2].set_ylim(50, 100)
out = os.path.join(os.path.dirname(__file__), "..", "img", "seaborn-demo.png")
fig.savefig(out, dpi=110)
print("已保存:", os.path.basename(out))
print(df.groupby(["模型", "任务"])["得分"].mean().unstack().round(1))
