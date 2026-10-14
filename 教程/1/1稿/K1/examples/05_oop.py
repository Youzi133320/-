# OOP 四要素：封装、继承、多态、抽象
from abc import ABC, abstractmethod

class Shape(ABC):                      # 抽象：只定义"能做什么"
    @abstractmethod
    def area(self) -> float: ...
    def describe(self):
        return f"{type(self).__name__} 面积={self.area():.2f}"

class Circle(Shape):                   # 继承
    def __init__(self, r): self._r = r # 封装：下划线表示"内部使用"
    def area(self): return 3.14159 * self._r ** 2

class Rect(Shape):
    def __init__(self, w, h): self.w, self.h = w, h
    def area(self): return self.w * self.h

for s in [Circle(1), Rect(2, 3)]:      # 多态：同一调用，不同行为
    print(s.describe())

try:
    Shape()
except TypeError as e:
    print("抽象类不能实例化:", e)

# 组合优于继承：Car "有一个" Engine，而不是 "是一个" Engine
class Engine:
    def start(self): return "引擎启动"
class Car:
    def __init__(self): self.engine = Engine()
    def drive(self): return self.engine.start() + " → 出发"
print(Car().drive())
