# 快速排序：选基准 pivot，分成 <pivot 和 >pivot 两部分，递归。平均 O(n log n)，最坏 O(n^2)
import random, time, sys
sys.setrecursionlimit(100_000)

def quicksort_simple(a):                       # 易读版（额外空间）
    if len(a) <= 1: return a
    p = a[len(a) // 2]
    return quicksort_simple([x for x in a if x < p]) + [x for x in a if x == p] + quicksort_simple([x for x in a if x > p])

comparisons = 0
def quicksort_inplace(a, lo=0, hi=None, pick=lambda lo, hi: hi):   # Lomuto 分区，原地
    global comparisons
    if hi is None: hi = len(a) - 1
    if lo >= hi: return
    k = pick(lo, hi); a[k], a[hi] = a[hi], a[k]
    p, i = a[hi], lo
    for j in range(lo, hi):
        comparisons += 1
        if a[j] < p: a[i], a[j] = a[j], a[i]; i += 1
    a[i], a[hi] = a[hi], a[i]
    quicksort_inplace(a, lo, i - 1, pick); quicksort_inplace(a, i + 1, hi, pick)

data = [5, 2, 9, 1, 5, 6, 3]
print("简单版:", quicksort_simple(data))
b = data[:]; quicksort_inplace(b); print("原地版:", b)

n = 3000
rng = random.Random(0)
for desc, arr, pick in [("随机数组 + 末尾作基准", [rng.random() for _ in range(n)], lambda lo, hi: hi),
                        ("已排序数组 + 末尾作基准", list(range(n)), lambda lo, hi: hi),
                        ("已排序数组 + 随机基准", list(range(n)), lambda lo, hi: rng.randint(lo, hi))]:
    comparisons = 0; quicksort_inplace(arr, pick=pick)
    assert arr == sorted(arr)
    print(f"{desc:<16} n={n} 比较次数 {comparisons:>9,}  (n log2 n≈{int(n*11.55):,}, n²/2={n*n//2:,})")

# 实际开发：直接用内置 sorted（Timsort/Powersort，稳定，O(n log n)）
big = [rng.random() for _ in range(200_000)]
t0 = time.perf_counter(); quicksort_simple(big); t1 = time.perf_counter(); sorted(big); t2 = time.perf_counter()
print(f"20 万个数：手写快排 {(t1-t0)*1000:.0f} ms vs 内置 sorted {(t2-t1)*1000:.0f} ms")
