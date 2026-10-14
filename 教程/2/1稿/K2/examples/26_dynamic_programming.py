# 动态规划：把问题拆成重叠子问题，记住子问题的答案，避免重复计算
from functools import cache
import time

calls = 0
def fib_naive(n):
    global calls; calls += 1
    return n if n < 2 else fib_naive(n - 1) + fib_naive(n - 2)
t0 = time.perf_counter(); fib_naive(27); t_naive = time.perf_counter() - t0
@cache
def fib_memo(n): return n if n < 2 else fib_memo(n - 1) + fib_memo(n - 2)
t0 = time.perf_counter(); fib_memo(27); t_memo = time.perf_counter() - t0
print(f"fib(27): 朴素递归调用 {calls:,} 次 {t_naive*1000:.0f} ms | 记忆化 {fib_memo.cache_info().misses} 次 {t_memo*1e6:.0f} µs")

# 编辑距离（Levenshtein）：拼写纠错、文本相似度、评测 WER/CER 的基础
def edit_distance(a, b):
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(len(a) + 1): dp[i][0] = i
    for j in range(len(b) + 1): dp[0][j] = j
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            dp[i][j] = min(dp[i-1][j] + 1,                       # 删除
                           dp[i][j-1] + 1,                       # 插入
                           dp[i-1][j-1] + (a[i-1] != b[j-1]))    # 替换/相同
    return dp
dp = edit_distance("kitten", "sitting")
print("kitten → sitting 编辑距离:", dp[-1][-1])
print("DP 表:\n     " + "  ".join(" sitting"))
for ch, row in zip(" kitten", dp): print(f"  {ch}  " + "  ".join(map(str, row)))

# 0/1 背包：在显存预算内选择收益最大的模块组合
items = [("LoRA-A", 3, 40), ("LoRA-B", 4, 50), ("Adapter", 2, 15), ("Prefix", 5, 60)]   # (名, 显存GB, 收益)
cap = 8
best = [0] * (cap + 1); choice = [[] for _ in range(cap + 1)]
for name, w, v in items:
    for c in range(cap, w - 1, -1):                # 倒序：每件物品只用一次
        if best[c - w] + v > best[c]:
            best[c] = best[c - w] + v; choice[c] = choice[c - w] + [name]
print(f"显存 {cap}GB 内最优组合: {choice[cap]}，总收益 {best[cap]}")

# 最长公共子序列 LCS（diff 工具的核心）
@cache
def lcs(a, b):
    if not a or not b: return ""
    if a[-1] == b[-1]: return lcs(a[:-1], b[:-1]) + a[-1]
    return max(lcs(a[:-1], b), lcs(a, b[:-1]), key=len)
print("LCS('ABCBDAB', 'BDCABA') =", lcs("ABCBDAB", "BDCABA"))
