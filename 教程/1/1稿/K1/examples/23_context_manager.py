# 上下文管理器：保证"进入"与"退出"成对执行，哪怕中间抛异常
import contextlib, time, os, tempfile

class Timer:
    def __enter__(self):
        self.t0 = time.perf_counter(); return self
    def __exit__(self, exc_type, exc, tb):
        self.elapsed = time.perf_counter() - self.t0
        print(f"[Timer] 用时 {self.elapsed * 1000:.1f} ms, 异常: {exc_type.__name__ if exc_type else None}")
        return False              # False = 不吞掉异常

with Timer():
    sum(range(1_000_00))

try:
    with Timer():
        raise ValueError("中途出错")
except ValueError:
    print("异常照常抛出，但 __exit__ 已执行")

# contextlib.contextmanager：用生成器写上下文管理器
@contextlib.contextmanager
def temp_env(key, value):
    old = os.environ.get(key)
    os.environ[key] = value
    try:
        yield
    finally:                      # 无论如何都恢复
        if old is None: os.environ.pop(key)
        else: os.environ[key] = old

with temp_env("MODEL", "test-model"):
    print("块内 MODEL =", os.environ["MODEL"])
print("块外 MODEL =", os.environ.get("MODEL"))

# 文件：with 自动关闭
path = os.path.join(tempfile.gettempdir(), "cm_demo.txt")
with open(path, "w", encoding="utf-8") as f:
    f.write("hello")
print("文件已关闭:", f.closed)

# ExitStack：动态管理多个资源；suppress：有意忽略某类异常
with contextlib.ExitStack() as stack:
    files = [stack.enter_context(open(path, encoding="utf-8")) for _ in range(3)]
    print("同时打开", len(files), "个文件")
print("全部已关闭:", all(f.closed for f in files))
with contextlib.suppress(FileNotFoundError):
    os.remove("/不存在的文件")
print("suppress 忽略了 FileNotFoundError")
