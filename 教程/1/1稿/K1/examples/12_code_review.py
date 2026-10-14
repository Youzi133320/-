# 一个迷你"自动审查机器人"：在人工 Code Review 之前先拦下机械性问题
import ast, re, textwrap

DIFF_NEW_CODE = textwrap.dedent('''
import os
API_KEY = "sk-1234567890abcdef"
def load(path):
    try:
        return open(path).read()
    except:
        pass
def run(cmd):
    os.system(cmd)  # TODO: 以后再改
''')

findings = []
if re.search(r"sk-[A-Za-z0-9]{16,}", DIFF_NEW_CODE):
    findings.append(("阻断", "疑似硬编码 API Key"))
tree = ast.parse(DIFF_NEW_CODE)
for node in ast.walk(tree):
    if isinstance(node, ast.ExceptHandler) and node.type is None:
        findings.append(("必须修改", f"第 {node.lineno} 行: 裸 except 会吞掉所有异常"))
    if isinstance(node, ast.Call) and getattr(node.func, "attr", "") == "system":
        findings.append(("必须修改", f"第 {node.lineno} 行: os.system 存在命令注入风险，改用 subprocess.run([...])"))
    if isinstance(node, ast.Call) and getattr(node.func, "id", "") == "open":
        findings.append(("建议", f"第 {node.lineno} 行: open() 未用 with，且未指定 encoding"))
for i, line in enumerate(DIFF_NEW_CODE.splitlines(), 1):
    if "TODO" in line:
        findings.append(("讨论", f"第 {i} 行: TODO 需要关联 issue 或在本次解决"))

for level, msg in findings:
    print(f"[{level}] {msg}")
print(f"共 {len(findings)} 条；机械问题交给机器，人专注于设计与业务逻辑")
