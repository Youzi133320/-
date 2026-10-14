# 函数式：纯函数、不可变数据、函数作为一等公民、组合
from functools import reduce, partial

def compose(*fs):
    return lambda x: reduce(lambda acc, f: f(acc), fs, x)

strip = str.strip
lower = str.lower
def remove_punct(s): return "".join(c for c in s if c.isalnum() or c.isspace())

normalize = compose(strip, lower, remove_punct)
print(repr(normalize("  Hello, World!  ")))

# 纯函数 vs 有副作用的函数
counter = 0
def impure_add(x):
    global counter
    counter += x          # 修改外部状态 = 副作用
    return counter
def pure_add(acc, x):
    return acc + x        # 只依赖输入
print("不纯:", impure_add(1), impure_add(1))   # 同样输入，不同输出
print("纯:", pure_add(0, 1), pure_add(0, 1))     # 同样输入，同样输出

# 不可变数据：返回新对象而不是改旧对象
from dataclasses import dataclass, replace
@dataclass(frozen=True)
class User:
    name: str
    level: int
u1 = User("ann", 1)
u2 = replace(u1, level=2)
print(u1, u2)

# 高阶函数与偏函数
power = lambda base, exp: base ** exp
square = partial(power, exp=2)
print(list(map(square, [1, 2, 3])))
