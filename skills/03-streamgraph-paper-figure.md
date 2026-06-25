# Publication-Quality Streamgraph (ThemeRiver)

## 适用场景
- 展示多个主题（≤15 个）在时间轴上的消长
- 论文 Fig 1 级别的核心插图
- 输入：分类后的术语逐年频次汇总（大类 × 年份矩阵）

## 数据准备
```python
# 按 MajorCluster 聚合逐年频次
years = [str(y) for y in range(2002, 2027)]
stream_data = df.groupby('MajorCluster')[years].sum()
# 去掉 Noise 和超大杂项口袋（如 Brain Regions & Circuits 占 >50%）
stream_data = stream_data.drop(['Noise', 'Brain Regions & Circuits'], errors='ignore')
# 按总规模降序排列
stream_data['total'] = stream_data.sum(axis=1)
stream_data = stream_data.sort_values('total', ascending=False).drop(columns='total')
```

## 绘图核心代码
```python
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(30, 12))

x = np.arange(len(years))
y = stream_data.values.T
labels = stream_data.index.tolist()

# 堆叠 + 中心基线
ax.stackplot(x, y, labels=labels, colors=colors,
             edgecolor='white', linewidth=0.3, alpha=0.92,
             baseline='symmetry')

# 右侧标签 + 引导线
for i, label in enumerate(labels):
    last_idx = x[-1]
    mid = np.sum(y[:i+1, -1]) - y[i, -1]/2
    ax.annotate(label, xy=(last_idx, mid),
                xytext=(last_idx + 0.8, mid),
                fontsize=18, ha='left', va='center',
                arrowprops=dict(arrowstyle='-', color='grey', lw=0.5))
```

## 设计规范
| 参数 | 值 | 理由 |
|------|------|------|
| DPI | **1200** | 打印级清晰度 |
| 图幅 | 30×12 inch | 宽幅全景，A4 比例 |
| 标签字号 | **18pt** | A4 纸可读 |
| X 轴刻度 | 18pt | 与标签一致 |
| 标题 | 24pt | 论文 Fig 标题 |
| baseline | symmetry | 中心对称基线，视觉平衡 |
| 配色 | distinctipy | CIELAB 最大感知距离，不会撞色 |
| 白边 | edgecolor='white' | 流层间清晰分隔 |

## 无标签版本（供外部编辑）
```python
# 相同代码但去掉右侧标签和引导线
ax.stackplot(x, y, colors=colors, edgecolor='white',
             linewidth=0.3, alpha=0.92, baseline='symmetry')
fig.savefig('fig1_nolabels.png', dpi=1200)
```

## 常见问题与修复
1. **最大类碾压** → 去掉占比 >30% 的杂项大类
2. **标签重叠** → 单列等距 + 引导线（12 个以内不会重叠）
3. **颜色撞色** → 用 distinctipy CIELAB 算法，排除灰色系
4. **DPI 不足** → 600 起步，论文用 1200
5. **字号过小** → 标签/X 轴统一 18pt，标题 24pt
