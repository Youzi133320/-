# 用非交互方式演示 pdb：向调试器"喂"一串命令，观察断点处的变量
import subprocess, sys, textwrap, pathlib, tempfile

target = textwrap.dedent('''
def accumulate(xs):
    total = 0
    for i, x in enumerate(xs):
        total += x * i
    return total
print("结果:", accumulate([5, 6, 7, 8]))
''')
path = pathlib.Path(tempfile.gettempdir()) / "bp_demo.py"
path.write_text(target, encoding="utf-8")

commands = "\n".join([
    "b 5, i == 2",      # 条件断点：只在 i == 2 时停下
    "c",                # 继续运行到断点
    "p i, x, total",    # 打印变量
    "where",            # 查看调用栈
    "c",                # 继续直到结束
    "q",
]) + "\n"
out = subprocess.run([sys.executable, "-m", "pdb", str(path)], input=commands,
                     capture_output=True, text=True)
print(out.stdout.replace(str(path), "bp_demo.py"))
