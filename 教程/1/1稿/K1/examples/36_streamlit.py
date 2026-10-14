# 用 Streamlit 官方测试工具 AppTest 无头运行 app.py，模拟用户操作并检查结果
import os
import streamlit
from streamlit.testing.v1 import AppTest
print("streamlit", streamlit.__version__)

app_path = os.path.join(os.path.dirname(__file__), "streamlit_app", "app.py")
at = AppTest.from_file(app_path).run()
print("标题:", at.title[0].value)
print("初始指标:", [(m.label, m.value) for m in at.metric])

at.multiselect[0].set_value(["B"]).run()          # 模拟用户只选模型 B
at.slider[0].set_value(70).run()                  # 把及格线拖到 70
print("只选 B、及格线 70 后:", [(m.label, m.value) for m in at.metric])

at.button[0].click().run(); at.button[0].click().run()
print("点击两次按钮后:", at.markdown[-1].value if at.markdown else [w.value for w in at.get("text")])
print("异常:", at.exception if len(at.exception) else "无")
