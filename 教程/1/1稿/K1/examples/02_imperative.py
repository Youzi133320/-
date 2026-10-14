# 命令式：显式的状态 + 显式的步骤。看清"状态"如何一步步变化
inventory = {"apple": 5, "pear": 2}
orders = [("apple", 3), ("pear", 5), ("apple", 1)]

for step, (item, qty) in enumerate(orders, 1):
    before = inventory[item]
    if before >= qty:
        inventory[item] -= qty          # 修改状态（赋值 = 命令式的核心）
        result = "成功"
    else:
        result = "库存不足"
    print(f"第{step}步 {item}×{qty}: {before} -> {inventory[item]} ({result})")

print("最终状态:", inventory)
