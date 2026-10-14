import re, pathlib
K1 = pathlib.Path("/workspace/tutorials/K2"); SRC = K1 / "_src"; EX = K1 / "examples"
DISC = ("> **免责声明**：本文是“河洛序”知识图谱 K2 批次的**初稿**，由 AI 辅助整理，仅供学习参考，不构成任何承诺或保证。"
        "版本信息截至 2026-10-14；文中示例已在 Python 3.15.0（数据结构与算法，纯标准库）或 Python 3.13 + 所列库版本（AI/ML 库与数学）下**实际运行**，"
        "输出为真实结果，但换机器、换版本时数字（尤其是耗时）会不同。\n>\n"
        "> 标注说明：**【有据可查】** 附官方文档 / 原始出处链接；**【社区共识】** 为业界普遍做法，没有唯一权威出处；"
        "**【待考察/推测】** 为未能核实或作者推断，请勿当作定论。")
def code(m):
    f = m.group(1); lang = "python" if f.endswith(".py") else ""
    return f"```{lang}\n# 文件：examples/{f}\n" + (EX / f).read_text(encoding="utf-8").rstrip() + "\n```"
def out(m):
    t = (EX / "out" / f"{m.group(1)}.txt").read_text(encoding="utf-8").rstrip()
    t = t.replace("/home/box/.local/share/uv/python/cpython-3.15.0-linux-x86_64-gnu", "<python3.15>")
    t = t.replace("/workspace/tutorials/K2/examples/", "").replace("/workspace/.k2venv/lib/python3.13/site-packages", "<site-packages>")
    return "```text\n" + t + "\n```"
for p in sorted(SRC.glob("*.md")):
    s = p.read_text(encoding="utf-8")
    s = s.replace("@@DISCLAIMER@@", DISC)
    s = re.sub(r"@@CODE:([\w./]+)@@", code, s)
    s = re.sub(r"@@OUT:([\w.]+)@@", out, s)
    assert "@@" not in s, p
    (K1 / p.name).write_text(s, encoding="utf-8")
print("built", len(list(SRC.glob('*.md'))))
