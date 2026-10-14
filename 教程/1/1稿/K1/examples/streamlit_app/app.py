# streamlit run app.py
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="模型评测看板", layout="wide")
st.title("模型评测看板")

@st.cache_data
def load_data(seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    return pd.DataFrame({
        "模型": np.repeat(["A", "B", "C"], 50),
        "得分": np.concatenate([rng.normal(m, 5, 50) for m in (80, 72, 88)]),
    })

df = load_data(0)
models = st.multiselect("选择模型", sorted(df["模型"].unique()), default=["A", "C"])
threshold = st.slider("及格线", 50, 100, 75)

view = df[df["模型"].isin(models)]
col1, col2 = st.columns(2)
col1.metric("样本数", len(view))
col2.metric("及格率", f"{(view['得分'] >= threshold).mean():.0%}" if len(view) else "—")
st.bar_chart(view.groupby("模型")["得分"].mean())

if "clicks" not in st.session_state:
    st.session_state.clicks = 0
if st.button("点我计数"):
    st.session_state.clicks += 1
st.write("按钮被点击次数:", st.session_state.clicks)
