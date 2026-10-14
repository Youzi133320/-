# 贪心：每一步都选"当前看起来最好"的。对某些问题能得到最优解，对另一些不能
# 1) 活动选择（会议室安排）：按结束时间最早贪心 → 可证明最优
meetings = [("A", 1, 4), ("B", 3, 5), ("C", 0, 6), ("D", 5, 7), ("E", 3, 9), ("F", 5, 9), ("G", 6, 10), ("H", 8, 11)]
chosen, end = [], -1
for name, s, e in sorted(meetings, key=lambda m: m[2]):
    if s >= end: chosen.append(name); end = e
print("最多能安排的会议:", chosen)

# 2) 找零：人民币面额下贪心最优；换一套面额就可能失败
def greedy_change(amount, coins):
    out = []
    for c in sorted(coins, reverse=True):
        while amount >= c: amount -= c; out.append(c)
    return out
def dp_change(amount, coins):
    best = [0] + [None] * amount
    for a in range(1, amount + 1):
        opts = [best[a - c] for c in coins if c <= a and best[a - c] is not None]
        best[a] = min(opts) + 1 if opts else None
    return best[amount]
print("人民币面额 [1,5,10,20,50,100] 凑 88:", greedy_change(88, [1, 5, 10, 20, 50, 100]))
print("面额 [1,3,4] 凑 6：贪心", greedy_change(6, [1, 3, 4]), f"用 {len(greedy_change(6, [1,3,4]))} 枚；动态规划最优只需 {dp_change(6, [1,3,4])} 枚 (3+3)")

# 3) 哈夫曼编码：反复合并频率最小的两个节点 → 最优前缀码（压缩、BPE 的近亲思想）
import heapq
from collections import Counter
text = "abracadabra"
heap = [[f, i, {ch: ""}] for i, (ch, f) in enumerate(Counter(text).items())]
heapq.heapify(heap); uid = len(heap)
while len(heap) > 1:
    f1, _, c1 = heapq.heappop(heap); f2, _, c2 = heapq.heappop(heap)
    merged = {k: "0" + v for k, v in c1.items()} | {k: "1" + v for k, v in c2.items()}
    heapq.heappush(heap, [f1 + f2, uid, merged]); uid += 1
codes = heap[0][2]
bits = sum(len(codes[ch]) for ch in text)
print("哈夫曼编码:", dict(sorted(codes.items())), f"| 共 {bits} bit，定长编码需 {len(text)*3} bit")

# 4) LLM 的贪心解码：每步取概率最大的 token，不一定得到整体概率最大的句子
p = {"": {"我": 0.6, "你": 0.4}, "我": {"们": 0.5, "很": 0.5}, "你": {"好": 0.9, "们": 0.1}}
g1 = max(p[""], key=p[""].get); g2 = max(p[g1], key=p[g1].get)
print(f"贪心解码: {g1+g2} 概率 {p[''][g1]*p[g1][g2]:.2f} | 全局最优: 你好 概率 {0.4*0.9:.2f}")
