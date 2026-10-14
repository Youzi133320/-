# 用 ast 自动嗅探三种常见"代码异味"：过长函数、参数过多、魔法数字
import ast, textwrap

SOURCE = textwrap.dedent('''
def process(a, b, c, d, e, f):
    x = a * 86400
    if b > 3.14159:
        x += 42
    ''' + "\n    ".join(f"y{i} = {i}" for i in range(30)) + '''
    return x
''')

LIMIT_LINES, LIMIT_ARGS = 20, 5
ALLOWED = {0, 1, -1, 2}

tree = ast.parse(SOURCE)
for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef):
        length = node.end_lineno - node.lineno + 1
        if length > LIMIT_LINES:
            print(f"[过长函数] {node.name}: {length} 行 > {LIMIT_LINES}")
        if len(node.args.args) > LIMIT_ARGS:
            print(f"[参数过多] {node.name}: {len(node.args.args)} 个参数 > {LIMIT_ARGS}")
    if isinstance(node, ast.BinOp) or isinstance(node, ast.Compare) or isinstance(node, ast.AugAssign):
        for sub in ast.walk(node):
            if isinstance(sub, ast.Constant) and isinstance(sub.value, (int, float)) and sub.value not in ALLOWED:
                print(f"[魔法数字] 第 {sub.lineno} 行: {sub.value}")
