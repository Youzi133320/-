# 二叉树与二叉搜索树（BST）：左 < 根 < 右，平衡时查找 O(log n)
from dataclasses import dataclass
from typing import Optional
import random

@dataclass
class N:
    key: int
    left: Optional["N"] = None
    right: Optional["N"] = None

def insert(root, key):
    if root is None: return N(key)
    if key < root.key: root.left = insert(root.left, key)
    else: root.right = insert(root.right, key)
    return root
def inorder(r):  return inorder(r.left) + [r.key] + inorder(r.right) if r else []
def preorder(r): return [r.key] + preorder(r.left) + preorder(r.right) if r else []
def height(r):   return 1 + max(height(r.left), height(r.right)) if r else 0
def search(r, k, steps=1):
    if r is None: return None
    if k == r.key: return steps
    return search(r.left if k < r.key else r.right, k, steps + 1)

root = None
for k in [50, 30, 70, 20, 40, 60, 80]: root = insert(root, k)
print("中序遍历(有序!):", inorder(root))
print("前序遍历:", preorder(root))
print("高度:", height(root), "| 查找 60 用了", search(root, 60), "步")

# 插入顺序决定形状：有序插入会退化成链表
import sys; sys.setrecursionlimit(10_000)
rnd, seq = None, None
keys = list(range(1000)); shuffled = keys[:]; random.Random(0).shuffle(shuffled)
for k in shuffled: rnd = insert(rnd, k)
for k in keys: seq = insert(seq, k)
print(f"1000 个键：随机插入高度 {height(rnd)}，有序插入高度 {height(seq)}（退化成链表）")
print("理想平衡高度 ≈ log2(1000) ≈ 10 → 这就是需要红黑树/AVL 等自平衡树的原因")

# 层序遍历（BFS）
from collections import deque
def level_order(r):
    out, q = [], deque([r])
    while q:
        level = [q.popleft() for _ in range(len(q))]
        out.append([n.key for n in level])
        q.extend(c for n in level for c in (n.left, n.right) if c)
    return out
print("层序遍历:", level_order(root))
