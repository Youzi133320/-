# 队列：先进先出 FIFO。用 collections.deque，不要用 list.pop(0)
from collections import deque
q = deque()
for job in ["任务A", "任务B", "任务C"]: q.append(job)
print("出队顺序:", [q.popleft() for _ in range(len(q))])

# 固定长度的滑动窗口（如最近 N 轮对话、最近 N 个指标）
window = deque(maxlen=3)
for loss in [2.0, 1.5, 1.2, 1.0, 0.9]:
    window.append(loss)
    print(f"新值 {loss} -> 窗口 {list(window)} 平均 {sum(window)/len(window):.2f}")

# 线程安全队列：生产者-消费者
import queue, threading
jobs, results = queue.Queue(maxsize=2), []
def worker():
    while (item := jobs.get()) is not None:
        results.append(item * item); jobs.task_done()
    jobs.task_done()
t = threading.Thread(target=worker); t.start()
for i in range(5): jobs.put(i)          # 队列满时 put 会阻塞 = 背压
jobs.put(None); jobs.join(); t.join()
print("消费者结果:", results)

# 优先队列（见“堆”）与 asyncio.Queue 也都是队列家族成员
import asyncio
async def main():
    aq = asyncio.Queue()
    for i in range(3): await aq.put(f"请求{i}")
    return [await aq.get() for _ in range(3)]
print("asyncio.Queue:", asyncio.run(main()))
