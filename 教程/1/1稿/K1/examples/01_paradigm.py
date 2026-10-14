# 同一个任务：求 1..10 中偶数的平方和，用三种范式各写一遍
nums = range(1, 11)

# 1) 命令式：一步步告诉计算机"怎么做"
total = 0
for n in nums:
    if n % 2 == 0:
        total += n * n
print("命令式:", total)

# 2) 函数式：用纯函数组合数据变换
from functools import reduce
print("函数式:", reduce(lambda acc, x: acc + x,
                        map(lambda n: n * n, filter(lambda n: n % 2 == 0, nums)), 0))

# 3) 面向对象：把数据和行为封装在一起
class EvenSquareSummer:
    def __init__(self, data):
        self.data = list(data)
    def evens(self):
        return [n for n in self.data if n % 2 == 0]
    def total(self):
        return sum(n * n for n in self.evens())
print("面向对象:", EvenSquareSummer(nums).total())

# 4) 声明式（SQL）：只描述"要什么"
import sqlite3
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE t(n INTEGER)")
con.executemany("INSERT INTO t VALUES (?)", [(n,) for n in nums])
print("声明式SQL:", con.execute("SELECT SUM(n*n) FROM t WHERE n % 2 = 0").fetchone()[0])
