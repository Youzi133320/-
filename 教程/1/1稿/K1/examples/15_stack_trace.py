# 读懂 Stack Trace：从下往上读；以及异常链 (raise ... from ...)
import traceback, json

def parse_config(text):
    return json.loads(text)

def load_settings(text):
    try:
        cfg = parse_config(text)
    except json.JSONDecodeError as e:
        raise RuntimeError("配置文件格式错误") from e   # 保留原始原因
    return cfg["model"]

def main():
    return load_settings('{"model": "deepseek",}')     # 多了一个逗号

try:
    main()
except RuntimeError:
    tb = traceback.format_exc()
    print(tb.replace(__file__, "15_stack_trace.py"))

# 程序化地获取栈帧信息（日志/监控系统就是这样提取"出错位置"的）
try:
    main()
except RuntimeError as e:
    frames = traceback.extract_tb(e.__traceback__)
    last = frames[-1]
    print("最内层帧:", last.name, "第", last.lineno, "行")
    print("根因类型:", type(e.__cause__).__name__)
