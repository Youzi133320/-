# Big O：输入规模翻倍时，耗时怎么变？用实测验证
import time, bisect

def timed(fn, n, reps=3):
    best = float("inf")
    for _ in range(reps):
        t0 = time.perf_counter(); fn(n); best = min(best, time.perf_counter() - t0)
    return best

data = {}
def o1(n): return data.get(n)                            # O(1)
def ologn(n): arr = range(n); return bisect.bisect_left(arr, n // 3)   # O(log n)
def on(n): return sum(range(n))                          # O(n)
def onlogn(n): return sorted(range(n, 0, -1))            # O(n log n)（逆序输入）
def on2(n): return sum(1 for i in range(n) for j in range(n))  # O(n^2)

print(f"{'复杂度':<10}{'n=1000':>12}{'n=2000':>12}{'倍数':>8}")
for name, fn, n in [("O(1)", o1, 1000), ("O(log n)", ologn, 1000), ("O(n)", on, 200_000),
                    ("O(n log n)", onlogn, 200_000), ("O(n^2)", on2, 1000)]:
    t1, t2 = timed(fn, n), timed(fn, 2 * n)
    print(f"{name:<10}{t1*1e6:>10.1f}µs{t2*1e6:>10.1f}µs{t2/t1:>8.1f}")
print("理论倍数：O(1)≈1, O(log n)≈1.1, O(n)≈2, O(n log n)≈2.1, O(n^2)≈4（实测受缓存和常数影响）")

# 增长速度表
import math
print(f"\n{'n':>8}{'log n':>8}{'n log n':>12}{'n^2':>16}{'2^n':>12}")
for n in [10, 100, 1000, 10**6]:
    two = f"{2**n:.1e}" if n <= 1000 else "天文数字"
    print(f"{n:>8}{math.log2(n):>8.1f}{n*math.log2(n):>12.0f}{n*n:>16.0e}{two:>12}")

# Transformer 自注意力：序列长度 L 的 O(L^2) 代价
for L in [1024, 8192, 131072]:
    print(f"上下文 {L:>6} tokens：注意力分数矩阵有 {L*L:>17,} 个元素")
