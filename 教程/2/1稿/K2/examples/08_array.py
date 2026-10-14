# 数组：连续内存 + 下标 O(1) 访问；Python 的 list 是"动态数组"
import sys, time, array
from timeit import timeit

lst = []
sizes = []
for i in range(20):
    lst.append(i)
    sizes.append(sys.getsizeof(lst))
print("append 过程中 list 占用字节变化（容量成倍预留）:", sorted(set(sizes)))

big = list(range(1_000_000))
t_idx = timeit(lambda: big[500_000], number=100_000)
t_end = timeit(lambda: big.append(0) or big.pop(), number=100_000)
t_head = timeit(lambda: big.insert(0, 0) or big.pop(0), number=1_000)
print(f"随机访问 {t_idx/100_000*1e9:.0f} ns | 尾部增删 {t_end/100_000*1e9:.0f} ns | 头部增删 {t_head/1_000*1e6:.0f} µs")

# 紧凑数组：array 模块按 C 类型存储，比 list 省内存
a = array.array("d", range(1000))
print("list 1000 个浮点约", sys.getsizeof(list(map(float, range(1000)))) + 1000 * sys.getsizeof(1.0), "字节",
      "| array('d') 约", sys.getsizeof(a), "字节")

# 二维数组的坑：[[0]*3]*3 复制的是同一行的引用
bad = [[0] * 3] * 3; bad[0][0] = 1
good = [[0] * 3 for _ in range(3)]; good[0][0] = 1
print("bad :", bad); print("good:", good)
