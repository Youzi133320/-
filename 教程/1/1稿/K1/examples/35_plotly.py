# Plotly：交互式图表（悬停、缩放、导出 HTML），适合网页与仪表盘
import os
import plotly, plotly.express as px, plotly.graph_objects as go
import pandas as pd, numpy as np
print("plotly", plotly.__version__)

rng = np.random.default_rng(7)
df = pd.DataFrame({
    "模型": np.repeat(["A", "B", "C"], 20),
    "成本(元/千次)": np.concatenate([rng.normal(m, 0.3, 20) for m in (2, 1, 4)]).round(2),
    "得分": np.concatenate([rng.normal(m, 4, 20) for m in (80, 72, 88)]).round(1),
})
fig = px.scatter(df, x="成本(元/千次)", y="得分", color="模型", symbol="模型",
                 title="成本 vs 得分（悬停可看数值）", template="plotly_white")
fig.add_trace(go.Scatter(x=[1, 4], y=[70, 90], mode="lines", name="参考线", line=dict(dash="dash")))

out = os.path.join(os.path.dirname(__file__), "..", "img", "plotly-demo.html")
fig.write_html(out, include_plotlyjs="cdn")     # 用 CDN 引用 plotly.js，文件很小
print("已导出交互式 HTML:", os.path.basename(out), f"{os.path.getsize(out) / 1024:.0f} KB")
print("图中 trace 数:", len(fig.data), "| 类型:", sorted({t.type for t in fig.data}))
print("Figure 本质是 JSON:", list(fig.to_dict().keys()))
