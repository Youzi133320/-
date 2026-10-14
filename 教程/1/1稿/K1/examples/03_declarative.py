# 声明式：描述"想要的结果"，由引擎决定怎么做
import re, sqlite3

# 例 1：SQL —— 不写循环，数据库自己选择执行计划
con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE sales(region TEXT, amount INT);
INSERT INTO sales VALUES ('华东',120),('华北',80),('华东',60),('华南',200);
""")
for row in con.execute("SELECT region, SUM(amount) s FROM sales GROUP BY region ORDER BY s DESC"):
    print(row)
print("执行计划:", con.execute("EXPLAIN QUERY PLAN SELECT region, SUM(amount) FROM sales GROUP BY region").fetchall())

# 例 2：正则表达式 —— 描述"模式"，不描述匹配算法
print(re.findall(r"\b\d{3}-\d{4}\b", "电话 555-1234 和 666-9876，不是 12-34"))

# 例 3：配置即声明（类似 YAML/Docker Compose 的思想），由"执行器"负责落实
desired = {"web": 3, "worker": 2}
current = {"web": 1, "worker": 4}
plan = {svc: desired[svc] - current.get(svc, 0) for svc in desired}
print("对比期望状态得到的调整计划:", plan)
