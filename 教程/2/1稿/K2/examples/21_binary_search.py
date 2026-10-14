# 二分搜索：在有序序列中每次排除一半，O(log n)
import bisect

def binary_search(a, target):
    lo, hi, steps = 0, len(a) - 1, 0
    while lo <= hi:
        steps += 1
        mid = (lo + hi) // 2
        if a[mid] == target: return mid, steps
        if a[mid] < target: lo = mid + 1
        else: hi = mid - 1
    return -1, steps

a = list(range(0, 2_000_000, 2))          # 100 万个偶数
for t in [0, 777_778, 1_999_998, 3]:
    print(f"找 {t:>9}: 结果下标 {binary_search(a, t)[0]:>7}，用了 {binary_search(a, t)[1]} 步")
print("log2(1,000,000) ≈ 20 → 最多约 20 步")

# 标准库 bisect：找插入位置；保持列表有序地插入
scores = [60, 70, 80, 90]
print("85 应插入下标:", bisect.bisect_left(scores, 85))
grades = "FDCBA"
print("成绩等级:", [grades[bisect.bisect_right(scores, s)] for s in [55, 60, 75, 99]])

# "答案二分"：在单调的条件上二分 —— 找最大可用 batch size
def fits_in_memory(batch):                 # 假设：显存需求随 batch 单调增长
    return 1.2 + 0.37 * batch <= 24.0      # GB
lo, hi = 1, 1024
while lo < hi:
    mid = (lo + hi + 1) // 2
    if fits_in_memory(mid): lo = mid
    else: hi = mid - 1
print("不超过 24GB 的最大 batch size:", lo)

# 常见错误：在无序数据上二分
print("无序列表 [5, 1, 3, 9, 2] 上二分找 1:", binary_search([5, 1, 3, 9, 2], 1), "← 1 明明存在却返回 -1")
