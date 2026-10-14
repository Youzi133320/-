# Clean Code：同一逻辑的"难读版"与"整洁版"，并用断言证明行为一致
def f(l, t):
    r = []
    for i in l:
        if i[1] > t and i[2] == 1:
            r.append(i[0])
    return r

from dataclasses import dataclass
ACTIVE = 1

@dataclass
class Employee:
    name: str
    salary: int
    status: int

def names_of_active_employees_earning_over(employees: list[Employee], threshold: int) -> list[str]:
    """返回薪资高于 threshold 的在职员工姓名。"""
    return [e.name for e in employees
            if e.salary > threshold and e.status == ACTIVE]

raw = [("ann", 9000, 1), ("bob", 12000, 0), ("cat", 15000, 1)]
emps = [Employee(*row) for row in raw]
assert f(raw, 8000) == names_of_active_employees_earning_over(emps, 8000)
print(names_of_active_employees_earning_over(emps, 8000))
print("两版行为一致，但第二版不需要注释也能读懂")
