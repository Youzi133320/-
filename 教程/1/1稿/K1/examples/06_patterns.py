# 三个最常用的设计模式：策略、观察者、工厂（Pythonic 写法）
from typing import Callable

# 策略模式：把"算法"作为可替换的参数
def no_discount(p): return p
def vip_discount(p): return p * 0.8
def checkout(price: float, strategy: Callable[[float], float]) -> float:
    return round(strategy(price), 2)
print("策略:", checkout(100, no_discount), checkout(100, vip_discount))

# 观察者模式：事件发布/订阅
class EventBus:
    def __init__(self): self._subs = {}
    def on(self, event, fn): self._subs.setdefault(event, []).append(fn)
    def emit(self, event, **data):
        for fn in self._subs.get(event, []): fn(**data)
bus = EventBus()
bus.on("order_paid", lambda order_id: print(f"观察者-发邮件: 订单 {order_id}"))
bus.on("order_paid", lambda order_id: print(f"观察者-加积分: 订单 {order_id}"))
bus.emit("order_paid", order_id=42)

# 工厂模式：根据配置创建对象，调用方不关心具体类
class OpenAIClient:
    def name(self): return "openai"
class OllamaClient:
    def name(self): return "ollama"
REGISTRY = {"openai": OpenAIClient, "ollama": OllamaClient}
def make_client(kind: str):
    try:
        return REGISTRY[kind]()
    except KeyError:
        raise ValueError(f"未知客户端: {kind}") from None
print("工厂:", make_client("ollama").name())
