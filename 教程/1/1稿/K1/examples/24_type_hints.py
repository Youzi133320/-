# 类型提示：运行时不强制，但能被静态检查器(mypy/pyright)和 IDE、AI 利用
from typing import TypedDict, Protocol, Literal

type Role = Literal["system", "user", "assistant"]     # Python 3.12+ type 语句

class Message(TypedDict):
    role: Role
    content: str

class LLM(Protocol):
    def chat(self, messages: list[Message], temperature: float = 0.7) -> str: ...

class EchoLLM:
    def chat(self, messages: list[Message], temperature: float = 0.7) -> str:
        return messages[-1]["content"]

def first[T](items: list[T]) -> T | None:              # Python 3.12+ 泛型语法
    return items[0] if items else None

def ask(model: LLM, question: str) -> str:
    return model.chat([{"role": "user", "content": question}])

print(ask(EchoLLM(), "你好"))
print(first([3, 2, 1]), first([]))

# 运行时并不检查类型：
def double(x: int) -> int: return x * 2
print("运行时照样执行:", double("ab"))                  # 静态检查器会报错

# 运行时可以读取注解（框架如 FastAPI、Pydantic 就依赖它）
import typing
print("注解:", typing.get_type_hints(double))
