# PyArrow：列式内存格式 Apache Arrow 的 Python 实现，Pandas/Polars/DuckDB 之间的"通用语"
import os, tempfile
import pyarrow as pa, pyarrow.compute as pc, pyarrow.parquet as pq
print("pyarrow", pa.__version__)

table = pa.table({
    "model": pa.array(["A", "B", "A", "C"]),
    "score": pa.array([82, 75, 88, 91], type=pa.int16()),
    "tags":  pa.array([["code"], ["chat", "zh"], [], ["code"]]),   # 嵌套类型
})
print(table.schema)
print("score 均值:", pc.mean(table["score"]).as_py())
print("过滤 score>80:", table.filter(pc.greater(table["score"], 80))["model"].to_pylist())

path = os.path.join(tempfile.gettempdir(), "arrow_demo.parquet")
pq.write_table(table, path, compression="zstd")
meta = pq.ParquetFile(path).metadata
print(f"Parquet 行数 {meta.num_rows}, 行组 {meta.num_row_groups}, 列 {meta.num_columns}")
print("只读一列:", pq.read_table(path, columns=["score"]).to_pydict())

# 与 pandas / polars 互转（多数情况零拷贝或低拷贝）
import pandas as pd, polars as pl
pdf = table.to_pandas()
pldf = pl.from_arrow(table)
print("pandas 列类型:", pdf.dtypes.to_dict())
print("polars 列类型:", pldf.schema)
