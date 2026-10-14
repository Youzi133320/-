# 最短路径问题家族：不同的图用不同算法
from collections import deque
import math

# 1) 无权图：BFS
g = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": ["E"], "E": []}
dist, q = {"A": 0}, deque(["A"])
while q:
    u = q.popleft()
    for v in g[u]:
        if v not in dist: dist[v] = dist[u] + 1; q.append(v)
print("无权图 BFS 跳数:", dist)

# 2) 有负权边（无负环）：Bellman-Ford，O(V·E)
edges = [("S", "A", 4), ("S", "B", 5), ("B", "A", -3), ("A", "T", 2)]
V = {"S", "A", "B", "T"}
d = {v: math.inf for v in V}; d["S"] = 0
for _ in range(len(V) - 1):
    for u, v, w in edges:
        if d[u] + w < d[v]: d[v] = d[u] + w
print("Bellman-Ford（含负权）:", dict(sorted(d.items())))
neg_cycle = any(d[u] + w < d[v] for u, v, w in edges)
print("存在负环:", neg_cycle)

# 3) 全源最短路：Floyd-Warshall，O(V^3)
nodes = ["A", "B", "C", "D"]
W = {("A","B"): 3, ("B","C"): 1, ("A","C"): 7, ("C","D"): 2, ("B","D"): 6}
D = {(i, j): 0 if i == j else W.get((i, j), math.inf) for i in nodes for j in nodes}
for k in nodes:
    for i in nodes:
        for j in nodes:
            D[i, j] = min(D[i, j], D[i, k] + D[k, j])
print("Floyd-Warshall 距离矩阵:")
for i in nodes: print("  ", i, [D[i, j] if D[i, j] < math.inf else "∞" for j in nodes])

# 4) 非负权单源：Dijkstra（见下一篇），对比 BFS 在有权图上的错误
wg = {"S": [("A", 1), ("B", 10)], "A": [("C", 1)], "C": [("B", 1)], "B": []}
hops, q = {"S": 0}, deque(["S"])
while q:
    u = q.popleft()
    for v, _ in wg[u]:
        if v not in hops: hops[v] = hops[u] + 1; q.append(v)
print(f"BFS 按跳数选 S→B 直达（{hops['B']} 跳，代价 10）；真实最短是 S→A→C→B（3 跳，代价 1+1+1=3）← 有权图不能用 BFS")
