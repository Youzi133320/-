# Dijkstra：非负权图的单源最短路。每次取"当前已知距离最小"的点（最小堆），O((V+E) log V)
import heapq

city = {
    "家": [("地铁站", 5), ("公交站", 2)],
    "公交站": [("地铁站", 2), ("商场", 9)],
    "地铁站": [("公司", 7), ("商场", 3)],
    "商场": [("公司", 2)],
    "公司": [],
}

def dijkstra(g, src):
    dist, prev = {src: 0}, {}
    pq, popped = [(0, src)], []
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist.get(u, float("inf")): continue      # 过期条目（惰性删除）
        popped.append(f"{u}({d})")
        for v, w in g[u]:
            nd = d + w
            if nd < dist.get(v, float("inf")):
                dist[v], prev[v] = nd, u
                heapq.heappush(pq, (nd, v))
    return dist, prev, popped

dist, prev, popped = dijkstra(city, "家")
print("出堆（确定最短距离）顺序:", " → ".join(popped))
print("到各地最短时间(分钟):", dist)
path, p = [], "公司"
while p: path.append(p); p = prev.get(p)
print("家到公司最短路线:", " → ".join(reversed(path)), f"共 {dist['公司']} 分钟")

# 负权边会让 Dijkstra 出错：教科书版本中一个点出堆后距离即"定稿"，不再更新
def dijkstra_textbook(g, src):
    dist, done, pq = {src: 0}, set(), [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if u in done: continue
        done.add(u)
        for v, w in g[u]:
            if v not in done and d + w < dist.get(v, float("inf")):
                dist[v] = d + w; heapq.heappush(pq, (d + w, v))
    return dist
neg = {"S": [("A", 2), ("B", 5)], "B": [("A", -4)], "A": [("C", 1)], "C": []}
print("有负权边时 Dijkstra 给出 S→C =", dijkstra_textbook(neg, "S")["C"], "（真实最短 S→B→A→C = 5-4+1 = 2）")

# 用 scipy 验证（如已安装）
try:
    import numpy as np
    from scipy.sparse.csgraph import dijkstra as sp_dijkstra
    names = list(city); ix = {n: i for i, n in enumerate(names)}
    M = np.zeros((len(names), len(names)))
    for u, es in city.items():
        for v, w in es: M[ix[u], ix[v]] = w
    print("scipy 验证 家→公司:", sp_dijkstra(M, indices=ix["家"])[ix["公司"]])
except ImportError:
    print("未安装 scipy，跳过验证")
