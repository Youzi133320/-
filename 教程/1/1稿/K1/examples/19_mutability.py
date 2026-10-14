# 可变 vs 不可变；以及最经典的坑：可变默认参数
import sys
print("Python", sys.version.split()[0])

s = "abc"
try:
    s[0] = "z"
except TypeError as e:
    print("str 不可变:", e)

t = (1, [2, 3])           # 元组不可变，但里面的列表可变
t[1].append(4)
print("元组里的列表被改了:", t)
try:
    hash(t)
except TypeError as e:
    print("因此这个元组不可哈希:", e)

# 经典坑：默认参数只在函数定义时求值一次
def bad(item, bucket=[]):
    bucket.append(item); return bucket
def good(item, bucket=None):
    bucket = [] if bucket is None else bucket
    bucket.append(item); return bucket
print("bad :", bad(1), bad(2))
print("good:", good(1), good(2))

# 不可变带来的好处：可作为字典键、可安全共享
cache = {(3, 4): 5.0}
print("元组做键:", cache[(3, 4)])

# Python 3.15 新增内置 frozendict（PEP 814）：不可变、可哈希的字典
if sys.version_info >= (3, 15):
    fd = frozendict(model="deepseek", temperature=0.2)
    print("frozendict:", fd, "| 可哈希:", hash(fd) == hash(frozendict(temperature=0.2, model="deepseek")))
    try:
        fd["model"] = "x"
    except TypeError as e:
        print("frozendict 不可修改:", e)
