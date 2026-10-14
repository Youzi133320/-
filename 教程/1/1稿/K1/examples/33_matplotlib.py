# Matplotlib：Python 绘图的底层标准。推荐面向对象接口 fig, ax = plt.subplots()
import os
import matplotlib
matplotlib.use("Agg")                     # 无界面环境保存图片
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
print("matplotlib", matplotlib.__version__)

# 中文字体：选系统里已有的 CJK 字体，否则中文显示为方块
cjk = [f.name for f in font_manager.fontManager.ttflist if "CJK SC" in f.name or "YaHei" in f.name or "PingFang" in f.name]
if cjk:
    plt.rcParams["font.family"] = cjk[0]
plt.rcParams["axes.unicode_minus"] = False
print("使用字体:", cjk[0] if cjk else "默认（可能不支持中文）")

steps = np.arange(1, 101)
rng = np.random.default_rng(0)
train = 2.5 * np.exp(-steps / 25) + 0.3 + rng.normal(0, 0.03, steps.size)
val = 2.5 * np.exp(-steps / 25) + 0.45 + 0.002 * np.maximum(0, steps - 60) + rng.normal(0, 0.03, steps.size)

fig, axes = plt.subplots(1, 2, figsize=(10, 4), constrained_layout=True)
ax = axes[0]
ax.plot(steps, train, label="训练损失")
ax.plot(steps, val, label="验证损失")
ax.axvline(int(steps[np.argmin(val)]), ls="--", c="gray")
ax.annotate("验证损失最低点\n（之后开始过拟合）", xy=(steps[np.argmin(val)], val.min()),
            xytext=(65, 1.5), arrowprops=dict(arrowstyle="->"))
ax.set(title="训练曲线", xlabel="训练步数", ylabel="损失")
ax.legend()

models, scores = ["A", "B", "C", "D"], [82, 75, 91, 68]
bars = axes[1].bar(models, scores, color=["#4C72B0", "#55A868", "#C44E52", "#8172B2"])
axes[1].bar_label(bars)
axes[1].set(title="模型得分", ylim=(0, 100))

out = os.path.join(os.path.dirname(__file__), "..", "img", "matplotlib-demo.png")
fig.savefig(out, dpi=120)
print("已保存:", os.path.basename(out))
