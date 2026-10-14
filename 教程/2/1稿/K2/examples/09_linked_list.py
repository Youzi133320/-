# 链表：节点通过指针相连；头部插入 O(1)，按下标访问 O(n)
from dataclasses import dataclass
from typing import Optional

@dataclass
class Node:
    val: int
    next: Optional["Node"] = None

class LinkedList:
    def __init__(self): self.head = None; self.size = 0
    def push_front(self, v):                 # O(1)
        self.head = Node(v, self.head); self.size += 1
    def find(self, v):                       # O(n)
        cur, steps = self.head, 0
        while cur:
            steps += 1
            if cur.val == v: return steps
            cur = cur.next
        return None
    def reverse(self):                       # 经典面试题：原地反转
        prev, cur = None, self.head
        while cur:
            cur.next, prev, cur = prev, cur, cur.next
        self.head = prev
    def __iter__(self):
        cur = self.head
        while cur: yield cur.val; cur = cur.next

ll = LinkedList()
for v in [3, 2, 1]: ll.push_front(v)
print("链表:", " -> ".join(map(str, ll)))
print("查找 3 走了", ll.find(3), "步")
ll.reverse(); print("反转后:", " -> ".join(map(str, ll)))

# 快慢指针判环
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast: return True
    return False
a, b, c = Node(1), Node(2), Node(3); a.next, b.next, c.next = b, c, a
print("有环吗:", has_cycle(a), "| 普通链表有环吗:", has_cycle(ll.head))

# 标准库里的双向链表实现：collections.deque（块状链表）
from collections import deque
from timeit import timeit
lst, dq = list(range(100_000)), deque(range(100_000))
print(f"头部插入删除 1000 次: list {timeit(lambda: lst.insert(0,1) or lst.pop(0), number=1000)*1000:.1f} ms"
      f" | deque {timeit(lambda: dq.appendleft(1) or dq.popleft(), number=1000)*1000:.2f} ms")
