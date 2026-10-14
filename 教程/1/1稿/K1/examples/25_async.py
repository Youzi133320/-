# async/await：单线程内并发处理大量"等待型"任务（网络请求、模型 API）
import asyncio, time

async def call_model(name: str, delay: float) -> str:
    await asyncio.sleep(delay)          # 模拟网络等待；await 时让出控制权
    return f"{name} 完成({delay}s)"

async def sequential():
    return [await call_model(f"任务{i}", 0.3) for i in range(3)]

async def concurrent():
    return await asyncio.gather(*(call_model(f"任务{i}", 0.3) for i in range(3)))

async def with_taskgroup_and_timeout():
    results = []
    async with asyncio.TaskGroup() as tg:                 # Python 3.11+ 结构化并发
        tasks = [tg.create_task(call_model(f"TG{i}", 0.1 * i)) for i in range(1, 4)]
    results = [t.result() for t in tasks]
    try:
        async with asyncio.timeout(0.2):                  # Python 3.11+ 超时
            await call_model("慢任务", 1.0)
    except TimeoutError:
        results.append("慢任务超时被取消")
    return results

async def limited(n_tasks=6, limit=2):
    sem = asyncio.Semaphore(limit)                        # 限制并发数（对付 API 限流）
    async def one(i):
        async with sem:
            await asyncio.sleep(0.1)
            return i
    t0 = time.perf_counter()
    await asyncio.gather(*(one(i) for i in range(n_tasks)))
    return time.perf_counter() - t0

for fn in (sequential, concurrent):
    t0 = time.perf_counter()
    out = asyncio.run(fn())
    print(f"{fn.__name__:10s} 用时 {time.perf_counter() - t0:.2f}s -> {out}")
print(asyncio.run(with_taskgroup_and_timeout()))
print(f"6 个任务、并发上限 2，用时约 {asyncio.run(limited()):.2f}s（≈3 批 × 0.1s）")
