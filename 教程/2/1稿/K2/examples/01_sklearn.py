# scikit-learn：统一的 fit / predict 接口 + 预处理 + 交叉验证 + 流水线
import sklearn, numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
print("scikit-learn", sklearn.__version__)

X, y = load_iris(return_X_y=True)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)
print("训练集", X_tr.shape, "测试集", X_te.shape)

models = {
    "逻辑回归(含标准化)": make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)),
    "随机森林": RandomForestClassifier(n_estimators=200, random_state=0),
}
for name, m in models.items():
    cv = cross_val_score(m, X_tr, y_tr, cv=5)
    m.fit(X_tr, y_tr)
    print(f"{name:<12} 5折交叉验证 {cv.mean():.3f}±{cv.std():.3f} | 测试集准确率 {m.score(X_te, y_te):.3f}")

best = models["逻辑回归(含标准化)"]
pred = best.predict(X_te)
print("混淆矩阵:\n", confusion_matrix(y_te, pred))
print(classification_report(y_te, pred, target_names=load_iris().target_names, digits=3))
print("预测概率(前 2 条):", np.round(best.predict_proba(X_te[:2]), 3))
rf = models["随机森林"]
print("随机森林特征重要性:", dict(zip(load_iris().feature_names, map(float, rf.feature_importances_.round(3)))))
