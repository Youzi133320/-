# 哈希表：key --哈希函数--> 桶位置，平均 O(1) 查找。Python 的 dict / set
from timeit import timeit
n = 100_000
data_list, data_set = list(range(n)), set(range(n))
print(f"在 {n} 个元素中查找: list {timeit(lambda: n-1 in data_list, number=200)/200*1e6:.0f} µs"
      f" | set {timeit(lambda: n-1 in data_set, number=200)/200*1e9:.0f} ns")

# 手写一个最简哈希表（链地址法），观察冲突
class HashMap:
    def __init__(self, cap=8): self.buckets = [[] for _ in range(cap)]
    def _idx(self, k): return hash(k) % len(self.buckets)
    def put(self, k, v):
        b = self.buckets[self._idx(k)]
        for i, (kk, _) in enumerate(b):
            if kk == k: b[i] = (k, v); return
        b.append((k, v))
    def get(self, k):
        for kk, v in self.buckets[self._idx(k)]:
            if kk == k: return v
        raise KeyError(k)
m = HashMap(4)
for k in ["apple", "pear", "fig", "kiwi", "plum", "lime"]: m.put(k, len(k))
print("get('plum') =", m.get("plum"), "| 各桶长度:", [len(b) for b in m.buckets], "(字符串哈希每次进程启动都随机化，分布会变)")

# 可哈希才能做键；相等的对象哈希必须相等
print("hash(1) == hash(1.0) == hash(True):", hash(1) == hash(1.0) == hash(True), "→ 字典里它们是同一个键:", {1: "a", 1.0: "b", True: "c"})
try: {[1, 2]: "x"}
except TypeError as e: print("列表不能做键:", e)

# 常用：计数、分组、去重
from collections import Counter, defaultdict
words = "the cat and the hat and the bat".split()
print("词频 Top2:", Counter(words).most_common(2))
groups = defaultdict(list)
for w in words: groups[len(w)].append(w)
print("按长度分组:", dict(groups))
print("保序去重:", list(dict.fromkeys(words)))
