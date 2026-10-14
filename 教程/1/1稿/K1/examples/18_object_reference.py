# 变量 = 名字（标签），对象 = 内存中的值。赋值是"贴标签"，不是"复制"
a = [1, 2, 3]
b = a                     # b 与 a 指向同一个对象
b.append(4)
print("a =", a, "| a is b:", a is b, "| id 相同:", id(a) == id(b))

c = list(a)               # 新对象（浅拷贝）
print("c == a:", c == a, "| c is a:", c is a)   # == 比较值，is 比较身份

# 重新绑定 vs 原地修改
x = 10
y = x
x = x + 1                 # 创建新的 int 对象，x 改贴到新对象上
print("x, y =", x, y)

# 函数参数传的是"对象引用"
def add_item(lst):  lst.append("新")      # 原地修改：调用方可见
def rebind(lst):    lst = ["全新列表"]     # 重新绑定：调用方不可见
items = ["旧"]
add_item(items); rebind(items)
print("items =", items)

# 引用计数（CPython 实现细节）
import sys
obj = object()
print("引用计数(含 getrefcount 自身的临时引用):", sys.getrefcount(obj))
alias = obj
print("增加一个名字后:", sys.getrefcount(obj))

# 浅拷贝 vs 深拷贝
import copy
nested = [[1, 2], [3]]
shallow, deep = copy.copy(nested), copy.deepcopy(nested)
nested[0].append(99)
print("浅拷贝受影响:", shallow, "| 深拷贝不受影响:", deep)
