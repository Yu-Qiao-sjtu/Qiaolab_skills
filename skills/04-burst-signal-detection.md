# Burst Signal Detection & Rising Signal Visualization

## 适用场景
- 从术语演化数据中检测"2025-2026 首次出现"的突发术语
- 进一步筛选"上升新信号"（2026 > 2025）
- 生成论文级别的色条/哑铃图展示

## Step 1: 突发术语检测
```python
# 条件：2002-2024 所有列 = 0，且 2025+2026 > 0
years_pre = [str(y) for y in range(2002, 2025)]
df['pre_sum'] = df[years_pre].sum(axis=1)
burst = df[(df['pre_sum'] == 0) & (df[['2025','2026']].sum(axis=1) > 0)]

# 上升信号：2026 > 2025（严格大于，不含持平）
rising = burst[burst['2026'] > burst['2025']]
```

## Step 2: 术语筛选
- **排除方法学通用词**：protein level, expression level, immunofluorescence staining, western blot, statistical significance 等
- **保留有生物学含义的词**：BDNF, synaptic plasticity, GLP-1, entorhinal cortex, macrophage polarization 等
- **数量**：论文主图 10-15 个，补充材料可扩展至 50+

## Step 3: 色条图（Tufte 风格）
```python
# 关键设计原则
# - 灰色 #E5E3E0 = 频次为 0（该年未出现）
# - 暖砖红 = 频次 > 0，深浅随频次递增
# - 白字标注频次（深色格），深红字（浅色格）
# - 圆角色条（FancyBboxPatch），非方形
# - 横式布局：术语在左，年份列在右
# - 图幅：确保最长术语完整显示（左边距 35-40%）
# - 排序：按 2026 降序
# - 字体：Times New Roman（论文衬线体）
# - 去掉所有类别/分组标注——极简
```

## Step 4: 设计迭代教训
- ❌ 棒棒糖图太低级
- ❌ 亮品红+蓝色太丑 → 暖砖红 + 暖灰
- ❌ 55 个术语太多 → 10-15 个
- ❌ 方形色块生硬 → 圆角色条（FancyBboxPatch）
- ❌ 标签被截断 → 左 margin 38% + xlim 负偏移
- ❌ 类别标注多余 → 极简双色

## 诚实原则
- 基础机制层信号偏弱（最高 0→4），这是数据特性
- 临床层信号更强（postoperative delirium 0→11）
- 论文中应诚实对比两者，这本身就是发现
