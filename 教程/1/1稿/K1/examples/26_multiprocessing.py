# 多进程：绕开 GIL，让 CPU 密集任务真正并行（每个进程有独立解释器与内存）
import os, time
from concurrent.futures import ProcessPoolExecutor

def cpu_heavy(n: int) -> int:
    total = 0
    for i in range(n):
        total += i * i % 7
    return total

if __name__ == "__main__":                       # Windows/macOS 的 spawn 方式要求此保护
    jobs = [3_000_000] * 4
    t0 = time.perf_counter()
    serial = [cpu_heavy(n) for n in jobs]
    t_serial = time.perf_counter() - t0

    t0 = time.perf_counter()
    with ProcessPoolExecutor(max_workers=4) as pool:
        parallel = list(pool.map(cpu_heavy, jobs))
    t_par = time.perf_counter() - t0

    assert serial == parallel
    print(f"CPU 核数: {os.cpu_count()}")
    print(f"串行 {t_serial:.2f}s | 4 进程 {t_par:.2f}s | 加速比 {t_serial / t_par:.1f}x")

    # 进程间不共享普通变量
    counter = {"n": 0}
    def bump(_):
        counter["n"] += 1
        return counter["n"]
    import multiprocessing as mp
    ctx = mp.get_context("fork") if hasattr(os, "fork") else mp.get_context()
    with ctx.Pool(2) as p:
        print("子进程各自看到的计数:", p.map(bump, range(4)), "| 主进程计数仍为:", counter["n"])
