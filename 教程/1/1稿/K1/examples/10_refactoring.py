# 重构 = 不改变外部行为的前提下改善内部结构。关键：先有测试，再小步修改
import unittest

# --- 重构前 ---
def price_v1(kind, qty):
    if kind == "book":
        p = qty * 30
        if qty > 10: p = p * 0.9
    elif kind == "pen":
        p = qty * 5
        if qty > 10: p = p * 0.9
    else:
        raise ValueError(kind)
    return round(p, 2)

# --- 重构后：提取常量表 + 提取函数，消除重复 ---
UNIT_PRICE = {"book": 30, "pen": 5}
BULK_QTY, BULK_RATE = 10, 0.9
def bulk_discount(amount, qty):
    return amount * BULK_RATE if qty > BULK_QTY else amount
def price_v2(kind, qty):
    if kind not in UNIT_PRICE:
        raise ValueError(kind)
    return round(bulk_discount(UNIT_PRICE[kind] * qty, qty), 2)

class CharacterizationTest(unittest.TestCase):
    """特征测试：锁定旧行为，保证重构不改变它"""
    def test_same_behavior(self):
        for kind in ["book", "pen"]:
            for qty in [0, 1, 10, 11, 100]:
                self.assertEqual(price_v1(kind, qty), price_v2(kind, qty))
    def test_unknown(self):
        with self.assertRaises(ValueError): price_v2("cup", 1)

unittest.main(argv=["x", "-v"], exit=False)
