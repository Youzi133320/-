# 归并排序：分成两半分别排好，再合并。稳定、始终 O(n log n)、需 O(n) 额外空间
def merge(left, right):
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]: out.append(left[i]); i += 1    # <= 保证稳定
        else: out.append(right[j]); j += 1
    return out + left[i:] + right[j:]

trace = []
def merge_sort(a, depth=0):
    if len(a) <= 1: return a
    mid = len(a) // 2
    l, r = merge_sort(a[:mid], depth + 1), merge_sort(a[mid:], depth + 1)
    m = merge(l, r); trace.append(("  " * depth) + f"合并 {l} + {r} -> {m}")
    return m

print("结果:", merge_sort([38, 27, 43, 3, 9, 82, 10]))
print("\n".join(trace))

# 稳定性：相同分数的人保持原来的先后顺序
people = [("小明", 90), ("小红", 85), ("小刚", 90), ("小丽", 85)]
def merge_sort_key(a, key):
    if len(a) <= 1: return a
    mid = len(a) // 2
    l, r = merge_sort_key(a[:mid], key), merge_sort_key(a[mid:], key)
    out, i, j = [], 0, 0
    while i < len(l) and j < len(r):
        if key(l[i]) <= key(r[j]): out.append(l[i]); i += 1
        else: out.append(r[j]); j += 1
    return out + l[i:] + r[j:]
print("按分数稳定排序:", merge_sort_key(people, key=lambda p: p[1]))

# 外部排序思想：每块各自排好，再用堆做 K 路归并（大文件、分布式结果合并）
import heapq, random
rng = random.Random(1)
chunks = [sorted(rng.sample(range(100), 5)) for _ in range(3)]
print("3 个已排序分块:", chunks)
print("K 路归并:", list(heapq.merge(*chunks)))
