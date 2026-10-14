# 故意写错，给 mypy 检查
def double(x: int) -> int:
    return x * 2

result: str = double(3)
double("ab")
