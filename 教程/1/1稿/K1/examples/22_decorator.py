# 装饰器 = 接收函数、返回新函数的函数；@ 只是语法糖
import functools, time

def timer(fn):
    @functools.wraps(fn)                     # 保留原函数名与文档
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        result = fn(*args, **kwargs)
        print(f"[timer] {fn.__name__} 用时 {(time.perf_counter() - t0) * 1000:.1f} ms")
        return result
    return wrapper

def retry(times=3, exceptions=(Exception,)):  # 带参数的装饰器 = 三层函数
    def deco(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return fn(*args, **kwargs)
                except exceptions as e:
                    print(f"[retry] 第 {attempt} 次失败: {e}")
                    if attempt == times:
                        raise
        return wrapper
    return deco

calls = {"n": 0}
@timer
@retry(times=3, exceptions=(ConnectionError,))
def flaky_api():
    """模拟前两次失败的 API 调用"""
    calls["n"] += 1
    time.sleep(0.01)
    if calls["n"] < 3:
        raise ConnectionError("网络抖动")
    return "成功"

print(flaky_api(), "| 函数名仍是:", flaky_api.__name__, "| 文档:", flaky_api.__doc__)

# 标准库自带的装饰器
@functools.cache
def fib(n): return n if n < 2 else fib(n - 1) + fib(n - 2)
print("fib(80) =", fib(80), "| 缓存信息:", fib.cache_info())

# 等价写法：@timer 就是 f = timer(f)
def hello(): return "hi"
hello = timer(hello); hello()
