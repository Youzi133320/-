---
id: k1.lib.streamlit
title: Streamlit：用纯 Python 快速做数据应用
domain: Python数据与可视化
prerequisites: [k1.lib.pandas, k1.py.decorator]
related: [k1.lib.plotly, k1.lib.matplotlib, k1.py.generator]
tags: [Streamlit, 数据应用, 仪表盘, session_state, 缓存, AppTest, LLM Demo]
---

# Streamlit：用纯 Python 快速做数据应用

@@DISCLAIMER@@

## 一句话定义

Streamlit 是一个**只写 Python 脚本就能生成交互式网页应用**的框架：`st.slider`、`st.button`、`st.dataframe` 这样一行一个组件，不需要写 HTML/CSS/JavaScript。

## 为什么重要

- **从脚本到可分享的 Demo 只需几分钟**：数据看板、模型演示、内部小工具都很适合。
- **AI 应用原型的热门选择**：聊天界面组件（`st.chat_input`、`st.chat_message`）和流式输出（`st.write_stream`）让 LLM Demo 非常好做。
- **自带测试框架**：`AppTest` 可以无浏览器地自动化测试应用。

## 原理 / 图解

【有据可查】Streamlit 的核心执行模型：**每次用户交互，整个脚本从上到下重新运行一遍**；用缓存（`st.cache_data`、`st.cache_resource`）避免重复的耗时计算，用 `st.session_state` 在多次重跑之间保存状态：<https://docs.streamlit.io/develop/concepts/architecture/caching> 、<https://docs.streamlit.io/develop/concepts/architecture/session-state> 。本文使用 streamlit 1.65.0（PyPI 发布于 2026-10-02）。

```mermaid
sequenceDiagram
    participant 用户 as 浏览器用户
    participant 服务 as Streamlit 服务
    participant 脚本 as app.py
    用户->>服务: 打开页面
    服务->>脚本: 从头运行整个脚本
    脚本-->>用户: 渲染组件
    用户->>服务: 拖动滑块到 70
    服务->>脚本: 再次从头运行 滑块值为 70
    Note over 脚本: load_data 命中缓存 不重复加载
    Note over 脚本: session_state 中的计数被保留
    脚本-->>用户: 更新界面
```

| 机制 | 作用 | 适合放什么 |
|---|---|---|
| `@st.cache_data` | 缓存函数返回的**数据**（返回副本） | 读取的 DataFrame、API 结果 |
| `@st.cache_resource` | 缓存**全局共享资源**（不复制） | 模型对象、数据库连接、LLM 客户端 |
| `st.session_state` | 每个用户会话独立的状态字典 | 聊天历史、计数器、登录状态 |

## 可运行示例

**应用代码** `examples/streamlit_app/app.py`（用 `streamlit run app.py` 启动）：

@@CODE:streamlit_app/app.py@@

**自动化测试**：用官方的 `AppTest` 无头运行上面的应用，模拟用户选择、拖动滑块、点击按钮，并检查结果：

@@CODE:36_streamlit.py@@

输出（Python 3.13.5 + streamlit 1.65.0）：

@@OUT:36_streamlit@@

- 第一行 `missing ScriptRunContext` 警告是在测试/裸模式下运行时的正常提示，官方说明可忽略。
- 只选模型 B、及格线 70 后，样本数从 100 变为 50，及格率变为 60%——证明交互逻辑正确。
- 点击两次按钮后计数为 2：`session_state` 在两次重跑之间保存了状态。

【有据可查】`AppTest` 文档：<https://docs.streamlit.io/develop/api-reference/app-testing>

## 常见误区

- **不知道“整个脚本会重跑”**：在脚本顶部加载大模型而不加缓存，每次点击都会重新加载，应用会极慢。
- **用普通变量保存状态**：每次重跑都会被重置，应使用 `st.session_state`。
- **用 `cache_data` 缓存模型对象**：会尝试序列化/复制，应使用 `cache_resource`。
- **把 Streamlit 当成通用 Web 框架**：复杂的多页面权限、高并发、精细的前端交互更适合 FastAPI + 前端框架或 Dash。【社区共识】
- **把 API Key 写进代码**：应使用 `st.secrets`（`.streamlit/secrets.toml`，且不要提交到仓库）或环境变量。【有据可查】<https://docs.streamlit.io/develop/concepts/connections/secrets-management>

## 与 AI 开发的关系

- **LLM 聊天 Demo**：`st.chat_message` + `st.chat_input` + `st.write_stream`（接收生成器，见 [[k1.py.generator]]）十几行就能做出流式聊天界面。【有据可查】官方教程：<https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps>
- **模型/提示词对比工具**：侧边栏选模型和参数，主区域并排展示输出，方便非技术同事参与评测。
- **RAG 调试面板**：展示检索到的片段、相似度分数和最终回答，帮助定位“是检索错了还是生成错了”。
- **模型缓存**：用 `@st.cache_resource` 只加载一次嵌入模型或本地模型，所有会话共享。
- **用 `AppTest` 做回归测试**：配合假 LLM（见 [[k1.prog.solid]] 的依赖倒置），可以在 CI 中测试界面逻辑而不调用真实模型。

## 延伸阅读

- 官方入门：<https://docs.streamlit.io/get-started>
- 缓存：<https://docs.streamlit.io/develop/concepts/architecture/caching>
- Session State：<https://docs.streamlit.io/develop/concepts/architecture/session-state>
- App testing：<https://docs.streamlit.io/develop/api-reference/app-testing>

## 无法核实 / 待考察点

- 【待考察/推测】Streamlit 1.5x～1.65 期间新增组件与行为变化未逐版核实。
- 【待考察/推测】`AppTest` 对 `st.bar_chart` 等图表元素内容的检查能力有限，本文只检查了指标与文本。
