# 生成器：用 yield 写的"惰性迭代器"，按需产出，内存友好
import sys

def read_lines(n):
    for i in range(n):
        yield f"line {i}"            # 每次 next() 运行到这里暂停

lst = [f"line {i}" for i in range(100_000)]
gen = (f"line {i}" for i in range(100_000))
print("列表占用字节:", sys.getsizeof(lst), "| 生成器对象占用字节:", sys.getsizeof(gen))

# 生成器管道：像 Unix 管道一样逐条处理（AI 场景：流式处理大语料）
def parse(lines):
    for line in lines:
        yield line.upper()
def keep_even(lines):
    for line in lines:
        if int(line.split()[-1]) % 2 == 0:
            yield line
pipeline = keep_even(parse(read_lines(7)))
print("管道结果:", list(pipeline))

# 观察暂停/恢复
def demo():
    print("  → 开始"); yield 1
    print("  → 恢复"); yield 2
    print("  → 结束")
g = demo()
print("next:", next(g)); print("next:", next(g))
print("剩余:", list(g))

# yield from 委托；send 双向通信
def inner(): yield "a"; yield "b"
def outer(): yield from inner(); yield "c"
print("yield from:", list(outer()))

def running_avg():
    total, count, avg = 0, 0, None
    while True:
        x = yield avg
        total, count = total + x, count + 1
        avg = total / count
ra = running_avg(); next(ra)
print("send 求滑动平均:", [ra.send(v) for v in [10, 20, 60]])
