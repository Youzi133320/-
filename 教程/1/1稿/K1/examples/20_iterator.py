# 迭代器协议：__iter__ 返回迭代器，__next__ 逐个产出，耗尽时抛 StopIteration
class Countdown:
    def __init__(self, start): self.current = start
    def __iter__(self): return self
    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        self.current -= 1
        return self.current + 1

print("自定义迭代器:", list(Countdown(3)))

# for 循环在底层做了什么
it = iter(["a", "b"])
print(next(it), next(it))
try:
    next(it)
except StopIteration:
    print("耗尽 → StopIteration（for 循环会自动处理它）")

# 可迭代对象(iterable) vs 迭代器(iterator)：迭代器只能走一遍
nums = [1, 2, 3]
it = iter(nums)
print("第一次:", list(it), "第二次:", list(it), "| 列表本身可重复遍历:", list(nums), list(nums))

# itertools：惰性组合
import itertools
print("前 5 个奇数平方:", list(itertools.islice((n * n for n in itertools.count(1, 2)), 5)))
print("分批:", list(itertools.batched(range(7), 3)))   # Python 3.12+
