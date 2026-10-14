# 栈：后进先出 LIFO。Python 用 list 的 append/pop 即可
def balanced(s: str) -> bool:
    pairs, stack = {")": "(", "]": "[", "}": "{"}, []
    for ch in s:
        if ch in "([{": stack.append(ch)
        elif ch in pairs:
            if not stack or stack.pop() != pairs[ch]: return False
    return not stack
for s in ["{[()]}", "([)]", '{"a": [1, 2]}', "(("]:
    print(f"{s!r:16} 括号匹配: {balanced(s)}")

# 逆波兰表达式求值（计算器、编译器的经典用法）
def rpn(tokens):
    st = []
    for t in tokens:
        if t in "+-*/":
            b, a = st.pop(), st.pop()
            st.append({"+": a + b, "-": a - b, "*": a * b, "/": a / b}[t])
        else: st.append(float(t))
    return st[0]
print("(3 + 4) * 2 的逆波兰 3 4 + 2 * =", rpn("3 4 + 2 *".split()))

# 函数调用栈本身就是栈：递归太深会溢出
import sys
def depth(n): return 0 if n == 0 else 1 + depth(n - 1)
print("默认递归上限:", sys.getrecursionlimit())
try: depth(100_000)
except RecursionError as e: print("RecursionError:", e)

# 用显式栈把递归改成循环（DFS 常用）
def depth_iter(n):
    stack, d = [n], 0
    while stack:
        x = stack.pop()
        if x: d += 1; stack.append(x - 1)
    return d
print("显式栈处理 100000 层:", depth_iter(100_000))
