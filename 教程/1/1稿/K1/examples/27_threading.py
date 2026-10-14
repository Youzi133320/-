# 多线程：I/O 等待型任务的利器；CPU 密集任务受 GIL 限制（free-threaded 构建除外）
import sys, time, threading
from concurrent.futures import ThreadPoolExecutor

gil = getattr(sys, "_is_gil_enabled", lambda: True)()
print(f"Python {sys.version.split()[0]} | GIL 启用: {gil}")

def io_task(i):
    time.sleep(0.2)                    # 模拟等待网络/磁盘，期间释放 GIL
    return i

def cpu_task(n):
    total = 0
    for i in range(n):
        total += i * i % 7
    return total

for name, fn, arg in [("I/O 型", io_task, None), ("CPU 型", cpu_task, 2_000_000)]:
    args = list(range(4)) if arg is None else [arg] * 4
    t0 = time.perf_counter(); [fn(a) for a in args]; t_serial = time.perf_counter() - t0
    t0 = time.perf_counter()
    with ThreadPoolExecutor(4) as ex:
        list(ex.map(fn, args))
    t_thr = time.perf_counter() - t0
    print(f"{name}: 串行 {t_serial:.2f}s | 4 线程 {t_thr:.2f}s | 加速比 {t_serial / t_thr:.1f}x")

# 共享状态需要加锁：竞态条件演示
count = 0
lock = threading.Lock()
def add_many(use_lock):
    global count
    for _ in range(200_000):
        if use_lock:
            with lock: count += 1
        else:
            tmp = count; count = tmp + 1   # 读-改-写分离，放大竞态窗口
for use_lock in (False, True):
    count = 0
    ts = [threading.Thread(target=add_many, args=(use_lock,)) for _ in range(4)]
    [t.start() for t in ts]; [t.join() for t in ts]
    print(f"{'加锁' if use_lock else '不加锁'}: 期望 800000，实际 {count}")
