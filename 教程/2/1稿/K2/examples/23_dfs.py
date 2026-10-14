# 深度优先搜索 DFS：一条路走到底再回溯（递归 / 栈）。用于连通性、环检测、回溯搜索
import sys
sys.setrecursionlimit(10_000)

graph = {"A": ["B", "C"], "B": ["D"], "C": ["D", "E"], "D": ["F"], "E": [], "F": []}
order = []
def dfs(u, seen=None):
    seen = seen if seen is not None else set()
    seen.add(u); order.append(u)
    for v in graph[u]:
        if v not in seen: dfs(v, seen)
dfs("A"); print("递归 DFS 访问顺序:", order)

def dfs_iter(start):
    seen, stack, out = set(), [start], []
    while stack:
        u = stack.pop()
        if u in seen: continue
        seen.add(u); out.append(u)
        stack.extend(reversed(graph[u]))      # 逆序压栈，保持与递归版相同的顺序
    return out
print("显式栈 DFS 访问顺序:", dfs_iter("A"))

# 有向图环检测（三色标记）：依赖是否循环？
def has_cycle(g):
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {u: WHITE for u in g}
    def visit(u):
        color[u] = GRAY
        for v in g[u]:
            if color[v] == GRAY or (color[v] == WHITE and visit(v)): return True
        color[u] = BLACK; return False
    return any(color[u] == WHITE and visit(u) for u in g)
print("graph 有环:", has_cycle(graph), "| 加一条 F->A 后有环:", has_cycle({**graph, "F": ["A"]}))

# 岛屿数量（连通分量）
sea = ["11000", "11010", "00100", "00011"]
seen = set()
def flood(r, c):
    if not (0 <= r < len(sea) and 0 <= c < len(sea[0])) or sea[r][c] == "0" or (r, c) in seen: return
    seen.add((r, c)); [flood(r+dr, c+dc) for dr, dc in ((1,0),(-1,0),(0,1),(0,-1))]
islands = 0
for r in range(len(sea)):
    for c in range(len(sea[0])):
        if sea[r][c] == "1" and (r, c) not in seen: flood(r, c); islands += 1
print("岛屿数量:", islands)

# 回溯：全排列（DFS 的典型应用）
def permutations(items, path=()):
    if not items: yield path; return
    for i, x in enumerate(items): yield from permutations(items[:i] + items[i+1:], path + (x,))
print("abc 全排列:", ["".join(p) for p in permutations("abc")])
