"""
第 2 课：pandas + matplotlib —— 把数据「看」出来
==================================================

学习目标：
  1. 用 pandas 加载数据、看数据长什么样
  2. 用 matplotlib 画图，把数字变成图形
  3. 体会「数据探索」到底在探什么

本课用的数据：鸢尾花数据集 (Iris)
  - 这是机器学习界的「Hello World」
  - 150 朵花，3 个品种，每朵花测了 4 个特征
  - sklearn 自带了，不用下载

运行后会在 outputs/ 目录下生成 4 张图。
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
import os

# 中文和负号显示设置（Windows 上必须加，否则中文会变成方块）
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
# 设置一个干净的主题
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.3

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'outputs')
os.makedirs(OUT, exist_ok=True)


# ===============================================================
# 第一部分：加载数据，看看它长什么样
# ===============================================================
print("=" * 70)
print("第一部分：认识数据")
print("=" * 70)

iris = load_iris()

# sklearn 返回的是一个「字典式」对象，我们要把它变成 pandas 的 DataFrame
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df['species'] = iris.target
df['species_name'] = df['species'].map(dict(enumerate(iris.target_names)))

print("\n► 数据形状 (行数, 列数):", df.shape)
print("\n► 前 5 行：")
print(df.head())

print("\n► 每一列的数据类型和缺失情况：")
print(df.info())

print("\n► 数值列的统计摘要（均值、标准差、最值、四分位数）：")
print(df.describe().round(2))

print("\n► 三个品种各有多少朵花：")
print(df['species_name'].value_counts())

print("""
【要理解的关键点】
  1. 拿到数据第一件事永远是：看形状、看前几行、看有没有缺失值
  2. describe() 能让你 3 秒内判断数据有没有异常（比如均值远离中位数 → 有离群点）
  3. 分类任务的标签分布要均匀，如果某一类只有 2 个样本，模型学不好
""")


# ===============================================================
# 第二部分：画图 —— 直方图
# ===============================================================
print("=" * 70)
print("第二部分：画直方图，看单个特征的分布")
print("=" * 70)

fig, axes = plt.subplots(1, 4, figsize=(16, 3.5))
colors = ['#378ADD', '#1D9E75', '#EF9F27', '#D4537E']

for i, col in enumerate(iris.feature_names):
    axes[i].hist(df[col], bins=20, color=colors[i], edgecolor='white', linewidth=0.6)
    axes[i].set_title(col.replace(' (cm)', ''), fontsize=12)
    axes[i].set_xlabel('厘米')
    axes[i].set_ylabel('数量' if i == 0 else '')

fig.suptitle('四个特征的分布 —— 直方图', fontsize=14, y=1.02)
plt.tight_layout()
p1 = os.path.join(OUT, '01_histogram.png')
plt.savefig(p1, dpi=130, bbox_inches='tight')
plt.close()
print("已保存:", p1)
print("""
【怎么看直方图】
  - 横轴是特征值，纵轴是落在这个区间的样本数量
  - 图形对称、像钟形 → 接近正态分布，很多模型喜欢这样的数据
  - 某个特征挤在一端 → 说明区分度差，可能要删掉
""")


# ===============================================================
# 第三部分：散点图 —— 看两个特征能不能区分品种
# ===============================================================
print("=" * 70)
print("第三部分：散点图，看特征之间的区分能力")
print("=" * 70)

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
palette = {'setosa': '#378ADD', 'versicolor': '#1D9E75', 'virginica': '#EF9F27'}

# 左图：花瓣长度 vs 花瓣宽度
for name, group in df.groupby('species_name'):
    axes[0].scatter(group['petal length (cm)'], group['petal width (cm)'],
                    label=name, alpha=0.75, s=45, color=palette[name],
                    edgecolors='white', linewidth=0.8)
axes[0].set_xlabel('花瓣长度 (cm)')
axes[0].set_ylabel('花瓣宽度 (cm)')
axes[0].set_title('花瓣：三个品种几乎完全分开', fontsize=12)
axes[0].legend(title='品种')

# 右图：萼片长度 vs 萼片宽度
for name, group in df.groupby('species_name'):
    axes[1].scatter(group['sepal length (cm)'], group['sepal width (cm)'],
                    label=name, alpha=0.75, s=45, color=palette[name],
                    edgecolors='white', linewidth=0.8)
axes[1].set_xlabel('萼片长度 (cm)')
axes[1].set_ylabel('萼片宽度 (cm)')
axes[1].set_title('萼片：setosa 分得开，另两种纠缠', fontsize=12)
axes[1].legend(title='品种')

fig.suptitle('散点图 —— 哪些特征有区分力？', fontsize=14, y=1.01)
plt.tight_layout()
p2 = os.path.join(OUT, '02_scatter.png')
plt.savefig(p2, dpi=130, bbox_inches='tight')
plt.close()
print("已保存:", p2)
print("""
【怎么看散点图 —— 这是最重要的一种图】
  - 左图：三个品种的颜色块几乎不重叠 → 光用花瓣两个特征就能分得不错
  - 右图：蓝色(setosa)单独一团，但绿色和橙色混在一起 → 萼片区分力弱
  - 结论：花瓣长度和花瓣宽度是关键特征

  这就是「特征工程」的起点 —— 先用眼睛看出哪个特征有用。
  你在做研究时，这类图往往比模型结果更能说明问题。
""")


# ===============================================================
# 第四部分：箱线图 —— 一眼看出分布差异
# ===============================================================
print("=" * 70)
print("第四部分：箱线图，比较不同类别的分布")
print("=" * 70)

fig, axes = plt.subplots(1, 4, figsize=(16, 4))
for i, col in enumerate(iris.feature_names):
    data_by_species = [df[df['species_name'] == s][col].values for s in iris.target_names]
    # 注意：matplotlib 3.9 起，boxplot 的 labels 参数已改名 tick_labels
    # 用 labels= 会报 TypeError: unexpected keyword argument 'labels'
    bp = axes[i].boxplot(data_by_species, tick_labels=iris.target_names, patch_artist=True,
                         widths=0.6)
    for patch, c in zip(bp['boxes'], palette.values()):
        patch.set_facecolor(c)
        patch.set_alpha(0.75)
    for median in bp['medians']:
        median.set_color('#2C2C2A')
    axes[i].set_title(col.replace(' (cm)', ''), fontsize=11)
    axes[i].tick_params(axis='x', rotation=15, labelsize=9)
    axes[i].set_ylabel('厘米' if i == 0 else '')

fig.suptitle('箱线图 —— 每个特征在不同品种间的分布差异', fontsize=14, y=1.02)
plt.tight_layout()
p3 = os.path.join(OUT, '03_boxplot.png')
plt.savefig(p3, dpi=130, bbox_inches='tight')
plt.close()
print("已保存:", p3)
print("""
【怎么看箱线图】
  箱体 = 中间 50% 的数据（下四分位到上四分位）
  中间横线 = 中位数
  须子 = 大致的数据范围
  单独的点 = 离群值

  判断关键：如果三个箱子的高度位置明显错开 → 这个特征有区分力
  花瓣长度那里，三个箱子完全错开 → 最强特征
""")


# ===============================================================
# 第五部分：相关性热力图
# ===============================================================
print("=" * 70)
print("第五部分：相关性热力图，看特征之间是否冗余")
print("=" * 70)

corr = df[iris.feature_names].corr()

fig, ax = plt.subplots(figsize=(6.5, 5.5))
im = ax.imshow(corr, cmap='RdYlBu_r', vmin=-1, vmax=1)

ax.set_xticks(range(len(corr)))
ax.set_yticks(range(len(corr)))
short = [c.replace(' (cm)', '').replace(' ', '\n') for c in corr.columns]
ax.set_xticklabels(short, fontsize=9)
ax.set_yticklabels(short, fontsize=9)

for i in range(len(corr)):
    for j in range(len(corr)):
        ax.text(j, i, f'{corr.iloc[i, j]:.2f}', ha='center', va='center',
                fontsize=10, color='white' if abs(corr.iloc[i, j]) > 0.6 else '#2C2C2A')

plt.colorbar(im, ax=ax, label='相关系数')
ax.set_title('特征相关性矩阵', fontsize=13, pad=12)
plt.tight_layout()
p4 = os.path.join(OUT, '04_correlation.png')
plt.savefig(p4, dpi=130, bbox_inches='tight')
plt.close()
print("已保存:", p4)
print("""
【怎么看相关矩阵】
  +1 = 完全正相关（一个涨另一个也涨）
  -1 = 完全负相关
   0 = 没关系

  这里花瓣长度和花瓣宽度相关系数 0.96 → 高度冗余！
  意思是：这两个特征携带的信息几乎重复，留一个就够了。

  这个判断在真实项目里极其重要 —— 特征冗余会拖慢训练、
  还可能让模型学到虚假规律。
""")

print("=" * 70)
print("第 2 课结束。4 张图都在 outputs/ 目录里，去看看吧。")
print("=" * 70)
