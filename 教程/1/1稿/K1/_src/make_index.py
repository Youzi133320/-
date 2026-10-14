import re, pathlib, yaml
K1 = pathlib.Path("/workspace/tutorials/K1")
rows = []
for p in sorted(K1.glob("[0-9][0-9]-*.md")):
    fm = yaml.safe_load(p.read_text(encoding="utf-8").split("---")[1])
    rows.append((p.name, fm))
ids = {fm["id"] for _, fm in rows}
for name, fm in rows:
    for k in ("prerequisites", "related"):
        for r in fm[k]:
            assert r in ids, (name, k, r)
def nid(i): return i.replace("k1.", "").replace(".", "_").replace("-", "_")
short = {fm["id"]: fm["title"].split("（")[0].split("：")[0] for _, fm in rows}
groups = {}
for name, fm in rows: groups.setdefault(fm["domain"], []).append((name, fm))
mm = ["flowchart LR"]
for g, items in groups.items():
    mm.append(f"    subgraph {g}")
    for _, fm in items: mm.append(f"      {nid(fm['id'])}[{short[fm['id']]}]")
    mm.append("    end")
for _, fm in rows:
    for r in fm["prerequisites"]: mm.append(f"    {nid(r)} --> {nid(fm['id'])}")
out = ["# K1 目录：编程基础 · Python 语言 · Python 数据与可视化", "",
"> **免责声明**：本批为“河洛序”知识图谱 K1 批次**初稿**，由 AI 辅助整理，仅供学习参考，不构成任何承诺。版本信息截至 2026-10-13。标注说明：**【有据可查】**附官方/原始来源；**【社区共识】**为业界普遍做法；**【待考察/推测】**为未能核实或推断。", "",
"## 本批概况", "",
f"- 节点数：**{len(rows)}**（编程基础 17 · Python 语言 10 · Python 数据与可视化 9），**一个知识点一篇，未合并**。",
"- 每篇结构：YAML front matter（id / title / domain / prerequisites / related / tags）→ 一句话定义 → 为什么重要 → 原理/图解 → 可运行示例 → 常见误区 → 与 AI 开发的关系 → 延伸阅读 → 无法核实/待考察点。",
"- 文中 `[[k1.xxx]]` 是图谱内部链接，指向对应 id 的节点；front matter 中的 prerequisites / related 只引用本批已存在的 id（已脚本校验）。",
"- 所有示例代码在 `examples/` 下，**均已实际运行**，文中输出为真实结果（保存在 `examples/out/`）。一键重跑：`examples/run_all.sh`。",
"- 配图在 `img/`：`matplotlib-demo.png`、`seaborn-demo.png`、`plotly-demo.png`（交互原文件 `plotly-demo.html`），均由示例代码生成。",
"- 难以查到可靠资料的问题，见 [待补查清单.md](待补查清单.md)。", "",
"## 运行环境（实测）", "",
"| 用途 | 解释器 / 库版本 |", "|---|---|",
"| 01–27 语言与编程基础示例 | CPython 3.15.0（2026-10-09 发布） |",
"| 27 多线程对比 | CPython 3.15.0 默认构建 + 3.15.0 自由线程构建（python3.15t） |",
"| 28–36 库示例 | CPython 3.13.5 + numpy 2.5.4、pandas 3.0.6、polars 2.0.0、openpyxl 3.1.5、pyarrow 25.0.1、matplotlib 3.11.2、seaborn 0.13.2、plotly 7.1.0、streamlit 1.65.0 |",
"| 24 静态类型检查 | mypy 2.4.0 |", "",
"## 节点列表", "",
"| # | 文件 | id | 领域 | 前置节点 |", "|---|---|---|---|---|"]
for i, (name, fm) in enumerate(rows, 1):
    pre = "、".join(f"`{r}`" for r in fm["prerequisites"]) or "—"
    out.append(f"| {i} | [{fm['title']}]({name}) | `{fm['id']}` | {fm['domain']} | {pre} |")
out += ["", "## 前置关系图", "", "箭头表示“先学 A 再学 B”（仅画 prerequisites，不画 related）。", "", "```mermaid", *mm, "```", "",
"## 建议学习路线", "",
"```mermaid", "flowchart LR",
"    A[范式三件套<br/>命令式 声明式 函数式 OOP] --> B[设计与质量<br/>设计模式 SOLID Clean Code 坏味道 重构]",
"    B --> C[协作<br/>文档 代码评审]",
"    A --> D[排错<br/>调试 断点 栈追踪 异常 日志]",
"    A --> E[Python 核心<br/>引用 可变性 迭代器 生成器 装饰器 上下文管理器 类型提示]",
"    E --> F[并发<br/>async 多进程 多线程]",
"    E --> G[数据<br/>NumPy Pandas Polars PyArrow OpenPyXL]",
"    G --> H[可视化与应用<br/>Matplotlib Seaborn Plotly Streamlit]",
"```", "",
"## 合并说明", "",
"本批 36 个节点**全部独立成篇，没有合并**。原因：每个节点都有官方文档或经典著作可引用，且都能写出可独立运行、能体现该知识点本质的示例（如“断点”可用 pdb 条件断点单独演示，“栈追踪”可用异常链单独演示），资料量足以支撑单篇。",
"相近节点之间的边界处理：命令式/声明式/函数式/OOP 由“编程范式”统领并互相 related；调试—断点—栈追踪—异常—日志 形成前置链；async/多进程/多线程各篇都有同一张“三种并发怎么选”的对照，避免重复展开。", "",
"## 修订记录", "", "- 2026-10-13：K1 初稿（36 篇）。", ""]
(K1 / "00-目录.md").write_text("\n".join(out), encoding="utf-8")
print("index ok", len(rows))
