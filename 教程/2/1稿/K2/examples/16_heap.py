# 堆：完全二叉树 + 父节点 ≤ 子节点（最小堆）。取最小 O(1)，插入/弹出 O(log n)
import heapq, random

h = []
for x in [5, 3, 8, 1, 9, 2]:
    heapq.heappush(h, x)
print("堆的数组表示:", h, "| 堆顶(最小):", h[0])
print("依次弹出:", [heapq.heappop(h) for _ in range(len(h))])

# 数组下标关系：节点 i 的孩子是 2i+1, 2i+2
h = [1, 3, 2, 5, 9, 8]
ok = all(h[i] <= h[c] for i in range(len(h)) for c in (2*i+1, 2*i+2) if c < len(h))
print("满足堆性质:", ok)

# Top-K：从 100 万个数里找最大的 5 个，不用全排序
nums = [random.Random(0).random() for _ in range(5)] + list(range(1_000_000))
print("最大的 5 个:", heapq.nlargest(5, nums))

# 优先队列：任务调度（优先级, 序号, 任务），序号保证同优先级按先来后到
pq, seq = [], 0
for prio, task in [(2, "写日志"), (0, "处理告警"), (1, "回复用户"), (0, "重启服务")]:
    heapq.heappush(pq, (prio, seq, task)); seq += 1
print("调度顺序:", [heapq.heappop(pq)[2] for _ in range(len(pq))])

# 合并多个有序序列（归并 K 个有序文件/分片结果）
print("合并有序列表:", list(heapq.merge([1, 4, 9], [2, 3, 10], [0, 5])))

# Python 3.14+ 提供最大堆函数
if hasattr(heapq, "heappush_max"):
    mh = []
    for x in [5, 3, 8]: heapq.heappush_max(mh, x)
    print("最大堆（3.14+ heappush_max）堆顶:", mh[0])
