# Polars 2：表达式 API + 惰性查询（默认流式引擎）
import polars as pl
print("polars", pl.__version__)

df = pl.DataFrame({
    "model": ["A", "B", "A", "C", "B", "A"],
    "task":  ["code", "chat", "chat", "code", "code", "code"],
    "score": [82, 75, None, 91, 68, 88],
    "cost":  [0.12, 0.05, 0.10, 0.30, 0.04, 0.11],
})

eager = (df.filter(pl.col("score").is_not_null())
           .group_by("model", maintain_order=True)            # 需要稳定顺序时显式声明
           .agg(pl.col("score").mean().alias("avg_score"),
                pl.len().alias("runs"),
                pl.col("cost").sum().alias("total_cost"))
           .sort("avg_score", descending=True))
print(eager)

lazy = (df.lazy()
          .with_columns((pl.col("score") / pl.col("cost")).alias("score_per_cost"))
          .filter(pl.col("task") == "code")
          .select("model", "score_per_cost")
          .sort("score_per_cost", descending=True))
print("优化后的查询计划:\n", lazy.explain())
print(lazy.collect())

# 写 Parquet 再惰性扫描：只读需要的列（谓词/投影下推）
import tempfile, os
path = os.path.join(tempfile.gettempdir(), "runs.parquet")
df.write_parquet(path)
print(pl.scan_parquet(path).filter(pl.col("model") == "A").select(pl.col("cost").sum()).collect())
