# 图：节点 + 边。表示方式：邻接表（稀疏图首选）与邻接矩阵（稠密图）
from collections import defaultdict

edges = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("D", "E")]
adj = defaultdict(list)
for u, v in edges:            # 无向图：两个方向都加
    adj[u].append(v); adj[v].append(u)
print("邻接表:", dict(adj))

nodes = sorted(adj)
idx = {n: i for i, n in enumerate(nodes)}
mat = [[0] * len(nodes) for _ in nodes]
for u, v in edges: mat[idx[u]][idx[v]] = mat[idx[v]][idx[u]] = 1
print("邻接矩阵:")
print("   " + " ".join(nodes))
for n, row in zip(nodes, mat): print(f"{n}  " + " ".join(map(str, row)))
print("各节点度数:", {n: len(adj[n]) for n in nodes})

# 有向图 + 拓扑排序：任务依赖、pip 依赖解析、计算图都靠它
from graphlib import TopologicalSorter
deps = {"train": {"tokenize", "download"}, "tokenize": {"download"}, "eval": {"train"}, "report": {"eval", "train"}}
print("拓扑序（先做谁）:", list(TopologicalSorter(deps).static_order()))
from graphlib import CycleError
try: list(TopologicalSorter({"a": {"b"}, "b": {"a"}}).static_order())
except CycleError as e: print("检测到环:", e.args[1])

# 空间对比：n 个节点、m 条边
n, m = 10_000, 50_000
print(f"n={n}, m={m}: 邻接矩阵需 {n*n:,} 个格子，邻接表约 {2*m:,} 个条目")
