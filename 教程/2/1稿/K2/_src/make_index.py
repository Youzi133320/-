import pathlib, yaml
K2 = pathlib.Path("/workspace/tutorials/K2"); K1 = pathlib.Path("/workspace/tutorials/K1")
def load(d):
    return [(p.name, yaml.safe_load(p.read_text(encoding="utf-8").split("---")[1])) for p in sorted(d.glob("[0-9][0-9]-*.md")) if not p.name.startswith("00-")]
rows, k1rows = load(K2), load(K1)
ids = {fm["id"] for _, fm in rows}; k1ids = {fm["id"]: fm for _, fm in k1rows}
assert len(ids) == len(rows) == 40
for name, fm in rows:
    assert fm["id"].startswith("k2."), name
    for k in ("prerequisites", "related"):
        for r in fm[k]:
            assert r in ids or r in k1ids, (name, k, r)
def nid(i): return i.replace(".", "_").replace("-", "_")
def short(fm): return fm["title"].split("（")[0].split("：")[0].split("与")[0] if fm["id"] != "k2.ml.peft" else "PEFT 与 LoRA"
gid = {"AI/ML库": ("ML", "AI 与 ML 库"), "数据结构": ("DS", "数据结构"), "算法": ("ALGO", "算法"), "数学": ("MATH", "数学")}
groups = {}
for name, fm in rows: groups.setdefault(fm["domain"], []).append(fm)
ext = sorted({r for _, fm in rows for r in fm["prerequisites"] if r.startswith("k1.")})
mm = ["flowchart LR", "    subgraph K1[K1 已有节点]"]
for r in ext: mm.append(f"      {nid(r)}([{short(k1ids[r])}])")
mm.append("    end")
for g, items in groups.items():
    a, b = gid[g]; mm.append(f"    subgraph {a}[{b}]")
    for fm in items: mm.append(f"      {nid(fm['id'])}[{short(fm)}]")
    mm.append("    end")
for _, fm in rows:
    for r in fm["prerequisites"]: mm.append(f"    {nid(r)} --> {nid(fm['id'])}")
cnt = {g: len(v) for g, v in groups.items()}
out = ["# K2 目录：AI/ML 库 · 数据结构 · 算法 · 数学", "",
"> **免责声明**：本批为“河洛序”知识图谱 K2 批次**初稿**，由 AI 辅助整理，仅供学习参考，不构成任何承诺。版本信息截至 2026-10-14。标注说明：**【有据可查】**附官方/原始来源；**【社区共识】**为业界普遍做法；**【待考察/推测】**为未能核实或推断。", "",
"## 本批概况", "",
f"- 节点数：**{len(rows)}**（AI/ML 库 {cnt['AI/ML库']} · 数据结构 {cnt['数据结构']} · 算法 {cnt['算法']} · 数学 {cnt['数学']}），**一个知识点一篇，未合并**。",
"- 每篇结构：YAML front matter（id / title / domain / prerequisites / related / tags）→ 一句话定义 → 为什么重要 → 原理/图解 → 可运行示例 → 常见误区 → 与 AI 开发的关系 → 延伸阅读 → 无法核实/待考察点。",
"- id 前缀为 `k2.`；prerequisites / related 可引用 K1 的 id（`k1.xxx`，如 `k1.lib.numpy`），所有引用均已脚本校验存在。文中 `[[k2.xxx]]` / `[[k1.xxx]]` 是图谱内部链接。",
"- 数学篇（28–40）公式统一用 `$$ … $$`（行内 `$ … $`），并配有 NumPy 数值验证代码。",
"- 所有示例代码在 `examples/` 下，**均已实际运行**，文中输出为真实结果（保存在 `examples/out/`）。一键重跑：`examples/run_all.sh`。",
"- 重型库（PyTorch / TensorFlow / JAX / Transformers / Diffusers / PEFT）示例全部用**本地构造的微型网络、CPU 运行**，无需下载大模型；全部装上并跑通，**没有“未实跑”项**。05 篇末尾可选地从 Hugging Face Hub 下载测试用微型模型 `hf-internal-testing/tiny-random-gpt2`（失败时自动跳过）。",
"- 输出中保留了库自身打印的日志（TensorFlow 的 oneDNN 提示、Transformers 的加载进度条与警告），以便读者对照自己的运行结果。",
"- 配图在 `img/`：`optimizers.png`（37 篇）、`regularization.png`（39 篇），均由示例代码生成。",
"- 难以查到可靠资料的问题，见 [待补查清单.md](待补查清单.md)。", "",
"## 运行环境（实测）", "",
"| 用途 | 解释器 / 库版本 |", "|---|---|",
"| 08–24、26–27 数据结构与算法 | CPython 3.15.0，仅标准库 |",
"| 01–07 AI/ML 库 | CPython 3.13.5 + scikit-learn 1.9.1、torch 2.14.1+cpu、tensorflow-cpu 2.21.0、keras 3.15.1、jax/jaxlib 0.11.2、transformers 5.19.0、diffusers 0.41.0、peft 0.21.2、accelerate 1.15.0 |",
"| 25 Dijkstra（含 SciPy 验证）、28–40 数学 | CPython 3.13.5 + numpy 2.5.4、scipy 1.18.1、scikit-learn 1.9.1、matplotlib、torch 2.14.1+cpu（40 篇对照） |",
"| 硬件 | 8 核 CPU、约 3GB 可用内存，无 GPU |", "",
"## 节点列表", "",
"| # | 文件 | id | 领域 | 前置节点 |", "|---|---|---|---|---|"]
for i, (name, fm) in enumerate(rows, 1):
    pre = "、".join(f"`{r}`" for r in fm["prerequisites"]) or "—"
    out.append(f"| {i} | [{fm['title']}]({name}) | `{fm['id']}` | {fm['domain']} | {pre} |")
out += ["", "## 前置关系图", "", "箭头表示“先学 A 再学 B”（仅画 prerequisites，不画 related）；圆角框为 K1 中的前置节点。", "", "```mermaid", *mm, "```", "",
"## 建议学习路线", "",
"```mermaid", "flowchart LR",
"    A[基础数据结构<br/>数组 链表 栈 队列 哈希表] --> B[层级与关系<br/>树 二叉树 堆 Trie 图]",
"    A --> C[复杂度与经典算法<br/>Big O 排序 二分]",
"    B --> D[图算法<br/>BFS DFS 最短路径 Dijkstra]",
"    C --> E[算法思想<br/>动态规划 贪心]",
"    F[数学一 线性代数<br/>向量 矩阵 特征值] --> H[数学三 学习原理<br/>导数 梯度 损失 优化 正则化 归一化]",
"    G[数学二 不确定性<br/>概率 统计 贝叶斯] --> H",
"    H --> I[框架<br/>Scikit-learn PyTorch TensorFlow JAX]",
"    I --> J[大模型生态<br/>Transformers Diffusers PEFT]",
"```", "",
"## 合并说明", "",
"本批 40 个节点**全部独立成篇，没有合并**。原因：每个节点都有官方文档、原始论文或经典教材可引用，且都能写出独立运行、体现该知识点本质的示例，资料量足以支撑单篇。",
"边界处理：**最短路径**与 **Dijkstra** 分开——“最短路径”篇是问题总览（BFS / Bellman-Ford / Floyd-Warshall 与选型），“Dijkstra”篇只深入讲这一个算法（正确性论证、负权反例）；**梯度**与**导数**分开——导数篇讲一元变化率、数值微分与链式法则，梯度篇讲多元梯度与反向传播；**线性代数**篇为总览，向量、矩阵、特征值各自深入。", "",
"## 修订记录", "", "- 2026-10-14：K2 初稿（40 篇）。", ""]
(K2 / "00-目录.md").write_text("\n".join(out), encoding="utf-8")
print("index ok", len(rows), "external K1 refs:", ext)
