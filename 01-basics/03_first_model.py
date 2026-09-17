"""
第 3 课：完整的机器学习流程 —— 从数据到模型到评估
====================================================

这是你真正意义上的「第一个机器学习项目」。

学习目标：
  1. 理解「训练集 / 测试集」为什么要分开
  2. 走完一遍标准流程：划分 → 训练 → 预测 → 评估
  3. 看懂「混淆矩阵」和「分类报告」
  4. 体会「过拟合」是什么感觉

核心心法：机器学习不是「让模型记住答案」，
         而是「让模型学会规律，并能应对没见过的新数据」。
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (accuracy_score, confusion_matrix,
                             classification_report, ConfusionMatrixDisplay)
import os

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.facecolor'] = 'white'

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'outputs')
os.makedirs(OUT, exist_ok=True)

RANDOM_STATE = 42   # 固定随机种子，保证每次跑结果一样（做研究必须这么做）


# ===============================================================
# 第 0 步：准备数据
# ===============================================================
print("=" * 70)
print("第 0 步：准备数据")
print("=" * 70)

iris = load_iris()
X = iris.data      # 特征，形状 (150, 4)
y = iris.target    # 标签，形状 (150,)

print(f"特征矩阵 X 形状: {X.shape}  → 150 个样本，每个 4 个特征")
print(f"标签向量 y 形状: {y.shape}  → 150 个答案")
print(f"类别: {list(iris.target_names)}")


# ===============================================================
# 第 1 步：划分训练集和测试集 —— 这是最容易被忽视、却最要命的一步
# ===============================================================
print("\n" + "=" * 70)
print("第 1 步：划分训练集 / 测试集")
print("=" * 70)

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.3,          # 30% 用来测试
    random_state=RANDOM_STATE,
    stratify=y              # 保证训练集和测试集的类别比例一致
)

print(f"训练集: {X_train.shape[0]} 个样本（模型从这里学）")
print(f"测试集: {X_test.shape[0]} 个样本（模型从没见过，用来检验）")
print("""
【为什么必须分开？】
  如果拿全部数据训练、再用同一批数据测试，模型只要「背下来」就能拿满分。
  这就像考试前把答案给学生背，然后夸他考得好 —— 毫无意义。

  测试集的意义：模拟「未来遇到的新数据」。
  这是整个机器学习里最重要的一个概念，没有之一。
""")


# ===============================================================
# 第 2 步：特征标准化
# ===============================================================
print("=" * 70)
print("第 2 步：特征标准化")
print("=" * 70)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)   # 在训练集上「学」均值方差
X_test_scaled = scaler.transform(X_test)         # 用同一套参数处理测试集

print("标准化前 训练集前 2 行:\n", X_train[:2].round(2))
print("\n标准化后 训练集前 2 行:\n", X_train_scaled[:2].round(2))
print("""
【关键细节 —— 新手最容易错的地方】
  1. scaler 只在训练集上 fit，测试集只能 transform
  2. 为什么？如果测试集也参与计算均值，就等于「偷看」了测试数据
     这个错误叫「数据泄露 (data leakage)」，是论文里常见的致命伤
  3. 很多算法（KNN、SVM、神经网络）对特征尺度敏感，
     不标准化会严重掉点
""")


# ===============================================================
# 第 3 步：训练三个模型，对比效果
# ===============================================================
print("=" * 70)
print("第 3 步：训练三个模型，对比效果")
print("=" * 70)

models = {
    'K近邻 (KNN)': KNeighborsClassifier(n_neighbors=5),
    '逻辑回归': LogisticRegression(max_iter=200, random_state=RANDOM_STATE),
    '决策树': DecisionTreeClassifier(max_depth=3, random_state=RANDOM_STATE),
}

results = {}
for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    acc = accuracy_score(y_test, y_pred)
    results[name] = {'model': model, 'pred': y_pred, 'acc': acc}
    n_test = len(y_test)
    print(f"  {name:14s} 测试集准确率 = {acc:.4f}  ({int(acc * n_test)}/{n_test} 个预测正确)")

best_name = max(results, key=lambda k: results[k]['acc'])
print(f"\n► 本轮表现最好: {best_name}")


# ===============================================================
# 第 4 步：深入看最好的那个模型 —— 混淆矩阵
# ===============================================================
print("\n" + "=" * 70)
print("第 4 步：混淆矩阵 —— 它到底错在哪？")
print("=" * 70)

best = results[best_name]
cm = confusion_matrix(y_test, best['pred'])
print(f"\n{best_name} 的混淆矩阵：")
print(pd.DataFrame(cm, index=iris.target_names, columns=iris.target_names))

print("\n► 详细的分类报告：")
print(classification_report(y_test, best['pred'], target_names=iris.target_names))

print("""
【怎么看混淆矩阵】
  行 = 真实类别，列 = 预测类别
  对角线上的数字 = 预测正确的数量
  非对角线 = 预测错误的数量

  本例解读（决策树、45 个测试样本）：
    对角线 15 + 15 + 14 = 44 个预测正确
    非对角线有 1 个：1 朵 virginica 被误判成 versicolor
    所以准确率 = 44 / 45 ≈ 0.978

  注意：Iris 太简单，97% 以上不稀奇，别因此高兴太早。
  真实项目里能到 85% 就值得庆祝 —— 所以后面我们会换更难的题。
""")

# 画混淆矩阵图
fig, ax = plt.subplots(figsize=(6, 5))
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=iris.target_names)
disp.plot(ax=ax, cmap='Blues', colorbar=False, values_format='d')
ax.set_title(f'{best_name} 混淆矩阵', fontsize=13, pad=12)
plt.tight_layout()
p_cm = os.path.join(OUT, '05_confusion_matrix.png')
plt.savefig(p_cm, dpi=130, bbox_inches='tight')
plt.close()
print("已保存:", p_cm)


# ===============================================================
# 第 5 步：理解「过拟合」—— 一个必须亲眼看到的坑
# ===============================================================
print("=" * 70)
print("第 5 步：决策树的深度实验 —— 什么是过拟合")
print("=" * 70)

print(f"\n{'树深':<6}{'训练集准确率':<16}{'测试集准确率':<16}{'差距':<10}")
print("-" * 52)

depths = [1, 2, 3, 4, 5, 8, 12, None]
train_accs, test_accs = [], []

for d in depths:
    tree = DecisionTreeClassifier(max_depth=d, random_state=RANDOM_STATE)
    tree.fit(X_train_scaled, y_train)
    tr = accuracy_score(y_train, tree.predict(X_train_scaled))
    te = accuracy_score(y_test, tree.predict(X_test_scaled))
    train_accs.append(tr)
    test_accs.append(te)
    label = str(d) if d else '不限制'
    print(f"{label:<8}{tr:<18.4f}{te:<18.4f}{tr - te:<10.4f}")

fig, ax = plt.subplots(figsize=(8, 5))
x = range(len(depths))
labels = [str(d) if d else '不限' for d in depths]
ax.plot(x, train_accs, 'o-', color='#378ADD', linewidth=2, markersize=7, label='训练集准确率')
ax.plot(x, test_accs, 's-', color='#D85A30', linewidth=2, markersize=7, label='测试集准确率')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_xlabel('决策树最大深度')
ax.set_ylabel('准确率')
ax.set_title('过拟合现象：训练集越来越好，测试集可能变差', fontsize=13, pad=12)
ax.legend()
ax.grid(alpha=0.3)
ax.set_ylim(0.8, 1.02)
plt.tight_layout()
p_ov = os.path.join(OUT, '06_overfitting.png')
plt.savefig(p_ov, dpi=130, bbox_inches='tight')
plt.close()
print("\n已保存:", p_ov)

print("""
【这张图是本课最重要的一张】
  树越深 → 模型越复杂 → 训练集准确率一路涨到 100%
  但测试集准确率不涨反跌，两者差距越拉越大

  这就是「过拟合 (overfitting)」：
  模型把训练数据的噪声和偶然规律也背下来了，
  结果面对新数据反而变差。

  训练集 100% + 测试集 90%  ≠  好模型
  训练集 96%  + 测试集 95%  =  真正的好模型

  你在写论文时，必须同时报告两个数字，
  只报测试集、或者只报训练集，都是学术不端或被拒稿的理由。
""")


# ===============================================================
# 第 6 步：更严谨的评估 —— 交叉验证
# ===============================================================
print("=" * 70)
print("第 6 步：交叉验证 —— 告别「一次划分的运气」")
print("=" * 70)

print("""
【问题】刚才只划分了一次，如果运气好刚好分到简单样本，结果虚高怎么办？

【解法】5 折交叉验证：
   把训练集切成 5 份，轮流拿其中 1 份当验证集，其余 4 份训练，
   做 5 次，取平均。这样结果稳定得多。

   这是论文里报告结果的标准做法。
""")

print(f"\n{'模型':<16}{'5折交叉验证均值':<18}{'标准差':<12}")
print("-" * 46)
for name, model in models.items():
    scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='accuracy')
    print(f"{name:<18}{scores.mean():<20.4f}{scores.std():<12.4f}")

print("""
【怎么解读】
  - 均值 = 模型的真实水平
  - 标准差 = 结果的稳定性。标准差大 → 模型对数据划分敏感，不够可靠
  - 论文里标准写法：准确率 95.3% ± 1.2%
  - 只报一个数字、不报标准差的，审稿人会要求你补做
""")


# ===============================================================
# 小结
# ===============================================================
print("=" * 70)
print("第 3 课小结 —— 你现在掌握了一套完整的 ML 流程")
print("=" * 70)
print("""
这个流程，换成任何数据集都通用：

  1. 准备数据         → 看形状、看分布、看缺失
  2. 划分训练/测试    → 绝对不能混用
  3. 特征标准化       → 只在训练集 fit
  4. 训练多个模型     → 准备一个简单 baseline
  5. 评估             → 准确率 + 混淆矩阵 + 分类报告
  6. 检查过拟合       → 训练集和测试集对比
  7. 交叉验证         → 让结果更可信

【下一步可以自己动手改的地方】
  - 把 test_size 改成 0.2 或 0.4，看结果怎么变
  - 把 RANDOM_STATE 改成别的数，看波动有多大（这就是「运气」）
  - 换 KNN 的 n_neighbors（试试 1 和 15），体会超参数的影响
  - 试试加大树的 max_depth 到 20，看看测试集掉多少

  动手改参数 → 看结果变化 → 思考为什么
  这个循环，就是你从「会用」到「理解」的唯一路径。
""")
print("=" * 70)
