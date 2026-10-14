# SOLID 中最常用的两条：单一职责(S) + 依赖倒置(D)，并演示它们让测试变容易
from typing import Protocol

class Notifier(Protocol):              # 抽象（接口）
    def send(self, to: str, msg: str) -> None: ...

class EmailNotifier:
    def send(self, to, msg): print(f"[真实邮件] -> {to}: {msg}")

class FakeNotifier:                    # 测试替身
    def __init__(self): self.sent = []
    def send(self, to, msg): self.sent.append((to, msg))

class SignupService:
    """单一职责：只负责注册流程；通知方式由外部注入（依赖倒置）"""
    def __init__(self, notifier: Notifier):
        self.notifier = notifier
        self.users = set()
    def signup(self, email: str):
        if email in self.users:
            raise ValueError("已注册")
        self.users.add(email)
        self.notifier.send(email, "欢迎!")

SignupService(EmailNotifier()).signup("a@example.com")

fake = FakeNotifier()
svc = SignupService(fake)
svc.signup("b@example.com")
assert fake.sent == [("b@example.com", "欢迎!")]
print("测试通过：无需真的发邮件就能验证行为")

# 里氏替换(L)反例：正方形继承长方形会破坏"可替换性"
class Rect:
    def __init__(self, w, h): self.w, self.h = w, h
    def set_w(self, w): self.w = w
    def area(self): return self.w * self.h
class Square(Rect):
    def set_w(self, w): self.w = self.h = w
def stretch(r: Rect):
    r.set_w(10); return r.area()
print("Rect(2,5) 拉宽后面积:", stretch(Rect(2, 5)), " Square(5) 拉宽后面积:", stretch(Square(5, 5)), "← 调用方的预期被打破")
