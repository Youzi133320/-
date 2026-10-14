# 树：有层级、无环的结构。文件系统、DOM、JSON、AST、组织架构都是树
from dataclasses import dataclass, field

@dataclass
class TreeNode:
    name: str
    children: list["TreeNode"] = field(default_factory=list)
    def add(self, *kids): self.children.extend(kids); return self

root = TreeNode("project").add(
    TreeNode("src").add(TreeNode("main.py"), TreeNode("utils.py")),
    TreeNode("tests").add(TreeNode("test_main.py")),
    TreeNode("README.md"))

def show(node, prefix=""):                   # 前序遍历：先处理自己再处理孩子
    print(prefix + node.name)
    for c in node.children: show(c, prefix + "  ")
show(root)

def height(n): return 1 + max((height(c) for c in n.children), default=0)
def count_leaves(n): return 1 if not n.children else sum(count_leaves(c) for c in n.children)
print("高度:", height(root), "| 叶子数:", count_leaves(root))

def path_to(n, target, path=()):
    path = path + (n.name,)
    if n.name == target: return "/".join(path)
    for c in n.children:
        if (p := path_to(c, target, path)): return p
print("查找路径:", path_to(root, "test_main.py"))

# Python 代码本身就是一棵树（AST）
import ast
tree = ast.parse("y = (a + b) * 2")
print(ast.dump(tree.body[0].value, indent=1)[:200])

# JSON 也是树
import json
doc = json.loads('{"model": {"name": "x", "layers": [{"type": "attn"}, {"type": "mlp"}]}}')
print("JSON 树深处取值:", doc["model"]["layers"][1]["type"])
