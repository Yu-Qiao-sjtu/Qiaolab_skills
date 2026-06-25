# UMAP Semantic Clustering for Term Evolution Data

## 适用场景
- 输入：过滤后的术语逐年频次矩阵（TERM × 25 years）
- 目的：将 15,000+ 术语的 25 维时间演化向量降维到 2D，保留语义近邻关系
- 输出：UMAP 散点图 + HDBSCAN 聚类标签

## Step 1: 特征矩阵构建
- 用 TF-IDF 加权逐年频次（而非原始频次）
- TF-IDF 压低"所有年份都很高"的通用词，抬高"集中出现在某几年"的特异性词
- 每个术语得到一个 25 维向量

## Step 2: UMAP 参数
```python
import umap
reducer = umap.UMAP(
    n_neighbors=15,      # 局部/全局平衡，15 适中
    min_dist=0.1,        # 允许紧密聚合
    metric='cosine',     # 余弦距离关注频率曲线形状相似性
    random_state=42,
    n_epochs=1000        # 充分优化
)
embedding = reducer.fit_transform(tfidf_matrix)
```

## Step 3: HDBSCAN 聚类
```python
import hdbscan
clusterer = hdbscan.HDBSCAN(
    min_cluster_size=30,
    min_samples=5,
    metric='euclidean',
    cluster_selection_method='eom'  # excess of mass
)
labels = clusterer.fit_predict(embedding)
```

## Step 4: 可视化要点
- 图幅 20×13 inch，适配论文
- 点大小 s=30，噪声点 s=0.8 + alpha=0.12
- 14 种 distinctipy 颜色（CIELAB 最大感知距离）
- 图例在左下外侧双列，不挡数据
- 字体：Arial，22pt bold 轴标签 + 标题，15pt 刻度
- 全英文标签
- 输出 600 dpi PNG + 矢量 PDF

## 常见陷阱
- UMAP 坐标无物理含义，只看相对距离
- Brain Regions & Circuits 可能形成巨大的"杂项口袋"（8,000+ 术语）→ 需要分析其 23 个子类
- Noise 约 1,470 术语，是合理的低密度区域，不需要强制聚类
- 不要在 UMAP 图上加凸包/虚线边界——视觉杂乱，且低维边界与高维边界不完全对应
