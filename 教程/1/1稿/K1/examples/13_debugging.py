# 调试的科学方法：复现 → 假设 → 验证 → 修复 → 回归测试
def average_scores(records):
    total = 0
    for r in records:
        total += r["score"]
    return total / len(records)

data = [{"name": "a", "score": 90}, {"name": "b", "score": "85"}, {"name": "c", "score": 70}]

# 1) 复现
try:
    average_scores(data)
except TypeError as e:
    print("复现成功:", e)

# 2) 假设：某条记录的 score 不是数字。3) 验证：打印类型（最朴素也最有效的探针）
for r in data:
    print(f"  {r['name']}: {r['score']!r} -> {type(r['score']).__name__}")

# 二分法定位：在大数据里找第一条坏记录
def first_bad(rows):
    lo, hi = 0, len(rows)
    while lo < hi:
        mid = (lo + hi) // 2
        if all(isinstance(r["score"], (int, float)) for r in rows[: mid + 1]):
            lo = mid + 1
        else:
            hi = mid
    return lo
print("二分定位到第一条坏记录下标:", first_bad(data))

# 4) 修复：在边界处做类型规整  5) 回归测试
def average_scores_fixed(records):
    if not records:
        return 0.0
    return sum(float(r["score"]) for r in records) / len(records)
assert average_scores_fixed(data) == (90 + 85 + 70) / 3
assert average_scores_fixed([]) == 0.0
print("修复并通过回归测试:", round(average_scores_fixed(data), 2))
