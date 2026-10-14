# Pandas 3：表格数据的读取、清洗、分组、合并
import pandas as pd
import numpy as np
print("pandas", pd.__version__)

df = pd.DataFrame({
    "model":  ["A", "B", "A", "C", "B", "A"],
    "task":   ["code", "chat", "chat", "code", "code", "code"],
    "score":  [82, 75, None, 91, 68, 88],
    "cost":   [0.12, 0.05, 0.10, 0.30, 0.04, 0.11],
})
print(df.dtypes.to_dict())                      # pandas 3 默认字符串列为 str 类型
print("缺失值:", df["score"].isna().sum())

clean = df.dropna(subset=["score"]).assign(score_per_cost=lambda d: d.score / d.cost)
summary = (clean.groupby("model")
                .agg(avg_score=("score", "mean"), runs=("score", "size"), total_cost=("cost", "sum"))
                .sort_values("avg_score", ascending=False))
print(summary.round(2))

print("透视表:\n", clean.pivot_table(index="model", columns="task", values="score", aggfunc="mean"))

prices = pd.DataFrame({"model": ["A", "B", "C"], "vendor": ["甲", "乙", "丙"]})
print(clean.merge(prices, on="model", how="left")[["model", "vendor", "score"]].head(3))

# pandas 3 的 Copy-on-Write：链式赋值不再修改原表
sub = df[df["model"] == "A"]
sub.loc[:, "cost"] = 0          # 只改了 sub
print("原表 A 的 cost 未变:", df.loc[df.model == "A", "cost"].tolist())
df.loc[df.model == "A", "cost"] = 0.0   # 正确做法：直接在原表上用 .loc
print("用 .loc 修改原表后:", df.loc[df.model == "A", "cost"].tolist())
