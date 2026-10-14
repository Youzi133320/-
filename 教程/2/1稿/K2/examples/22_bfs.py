# 广度优先搜索 BFS：一圈一圈向外扩展（队列）。无权图中找到的就是最短路径
from collections import deque

grid = ["S.#.....",
        ".##.###.",
        "....#...",
        ".##...#G"]
R, C = len(grid), len(grid[0])
start = next((r, c) for r in range(R) for c in range(C) if grid[r][c] == "S")
goal = next((r, c) for r in range(R) for c in range(C) if grid[r][c] == "G")

def bfs(start, goal):
    q, parent = deque([start]), {start: None}
    order = 0
    while q:
        cur = q.popleft(); order += 1
        if cur == goal: break
        r, c = cur
        for nr, nc in ((r+1, c), (r-1, c), (r, c+1), (r, c-1)):
            if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] != "#" and (nr, nc) not in parent:
                parent[(nr, nc)] = cur; q.append((nr, nc))
    path, p = [], goal
    while p: path.append(p); p = parent.get(p)
    return path[::-1], order

path, visited = bfs(start, goal)
print(f"最短路径长度 {len(path)-1} 步，共出队 {visited} 个格子")
canvas = [list(row) for row in grid]
for r, c in path[1:-1]: canvas[r][c] = "*"
print("\n".join("".join(row) for row in canvas))

# 社交网络：几度好友（按层 BFS）
friends = {"你": ["A", "B"], "A": ["C"], "B": ["C", "D"], "C": ["E"], "D": [], "E": []}
dist, q = {"你": 0}, deque(["你"])
while q:
    u = q.popleft()
    for v in friends[u]:
        if v not in dist: dist[v] = dist[u] + 1; q.append(v)
print("几度好友:", dist)
