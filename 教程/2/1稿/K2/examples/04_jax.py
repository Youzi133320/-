# JAX：NumPy 风格 API + 函数变换 grad / jit / vmap，要求纯函数
import time, jax, jax.numpy as jnp
print("jax", jax.__version__, "| 设备", jax.devices())

def f(x): return x ** 2 + 2 * x
print("grad(f)(3.0) =", jax.grad(f)(3.0), "| 二阶导 grad(grad(f))(3.0) =", jax.grad(jax.grad(f))(3.0))

# 线性回归：损失函数是参数的纯函数
key = jax.random.key(0)
k1, k2 = jax.random.split(key)              # 显式随机数 key：可复现
X = jax.random.normal(k1, (200, 3)); w_true = jnp.array([2.0, -1.0, 0.5])
y = X @ w_true + 0.1 * jax.random.normal(k2, (200,))
def loss(w, X, y): return jnp.mean((X @ w - y) ** 2)

@jax.jit
def step(w, X, y, lr=0.1): return w - lr * jax.grad(loss)(w, X, y)
w = jnp.zeros(3)
for _ in range(200): w = step(w, X, y)
print("学到的 w:", w.round(3), "| 真实 w:", w_true)

# jit 加速
def slow(x):
    for _ in range(20): x = jnp.sin(x) * 1.01 + jnp.cos(x)
    return x
fast = jax.jit(slow); xs = jnp.ones((1000, 1000))
fast(xs).block_until_ready()                 # 第一次调用触发编译
t0 = time.perf_counter(); slow(xs).block_until_ready(); t1 = time.perf_counter(); fast(xs).block_until_ready(); t2 = time.perf_counter()
print(f"未 jit {(t1-t0)*1000:.1f} ms | jit 后 {(t2-t1)*1000:.1f} ms")

# vmap：自动向量化（把单样本函数变成批处理）
def per_example_loss(w, x, y): return (x @ w - y) ** 2
batched = jax.vmap(per_example_loss, in_axes=(None, 0, 0))
print("vmap 逐样本损失前 3 个:", batched(w, X, y)[:3].round(5))

# 数组不可变：用 .at[].set() 返回新数组
a = jnp.zeros(3)
try: a[0] = 1
except TypeError as e: print("JAX 数组不可原地修改:", type(e).__name__)
print(".at[0].set(1) ->", a.at[0].set(1.0), "| 原数组仍是", a)
