# TensorFlow + Keras：高层 API 训练一个小模型；GradientTape 自动求导
import os; os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
import numpy as np, tensorflow as tf, keras
print("tensorflow", tf.__version__, "| keras", keras.__version__, "| 后端", keras.backend.backend())
tf.random.set_seed(0); rng = np.random.default_rng(0)

# GradientTape
x = tf.Variable(3.0)
with tf.GradientTape() as tape:
    y = x ** 2 + 2 * x
print("y = x²+2x 在 x=3 的导数:", tape.gradient(y, x).numpy())

# Keras 三步：定义 → compile → fit
X = rng.normal(size=(1000, 4)).astype("float32")
yv = (X[:, 0] * X[:, 1] + X[:, 2] > 0).astype("int32")
model = keras.Sequential([keras.Input(shape=(4,)), keras.layers.Dense(32, activation="relu"),
                          keras.layers.Dense(32, activation="relu"), keras.layers.Dense(2, activation="softmax")])
model.compile(optimizer=keras.optimizers.Adam(1e-2), loss="sparse_categorical_crossentropy", metrics=["accuracy"])
hist = model.fit(X[:800], yv[:800], epochs=20, batch_size=64, verbose=0, validation_split=0.1)
print("参数量:", model.count_params())
print(f"第 1 轮 loss {hist.history['loss'][0]:.4f} → 第 20 轮 loss {hist.history['loss'][-1]:.4f}")
loss, acc = model.evaluate(X[800:], yv[800:], verbose=0)
print(f"测试集准确率 {acc:.3f}")

# tf.function：把 Python 函数编译成计算图
@tf.function
def f(a, b): return tf.reduce_sum(tf.matmul(a, b))
print("tf.function 结果:", f(tf.ones((2, 3)), tf.ones((3, 4))).numpy())
