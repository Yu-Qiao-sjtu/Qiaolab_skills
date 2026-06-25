import pandas as pd, numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('terms-clustered.csv')

# ── English cluster name mapping ──
name_map = {
    '脑区与回路': 'Brain Regions & Circuits',
    '噪声点': 'Noise',
    '炎症与免疫': 'Inflammation & Immunity',
    '刺激参数与设备': 'Stimulation Parameters & Devices',
    '精神疾病与情绪': 'Psychiatric Disorders & Emotion',
    '围术期应用': 'Perioperative Applications',
    '自主神经与心血管': 'Autonomic & Cardiovascular',
    '临床试验方法学': 'Clinical Trial Methodology',
    '其他: vagus nerve, vagus nerve stimulation': 'VNS Core Terms',
    '卒中与脑损伤': 'Stroke & Brain Injury',
    '动物模型': 'Animal Models',
    '认知功能': 'Cognitive Function',
    '神经影像': 'Neuroimaging',
    '睡眠障碍': 'Sleep Disorders',
}
df['MajorEn'] = df['MajorCluster'].map(name_map).fillna(df['MajorCluster'])

cat_map = {'basic': 'Basic Research', 'clinical': 'Clinical', 'both': 'Both'}
df['CategoryEn'] = df['Category'].map(cat_map)

# ── Colors ──
major_clusters = sorted([c for c in df['MajorEn'].unique() if c != 'Noise'])
cmap = plt.cm.tab20
colors_major = {}
for i, c in enumerate(major_clusters):
    colors_major[c] = cmap(i % 20)
colors_major['Noise'] = '#d0d0d0'

cat_colors = {'Basic Research': '#2166ac', 'Clinical': '#b2182b', 'Both': '#4dac26'}

# ── Figure ──
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(26, 11))
fig.patch.set_facecolor('white')

# ===================== LEFT =====================
mask_noise = df['MajorEn'] == 'Noise'
noise_sample = df[mask_noise].sample(min(mask_noise.sum(), 5000), random_state=42)
ax1.scatter(noise_sample['UMAP_X'], noise_sample['UMAP_Y'],
           c=colors_major['Noise'], s=0.3, alpha=0.12, rasterized=True)

handles_left = []
for cluster in major_clusters:
    mask = df['MajorEn'] == cluster
    n = mask.sum()
    sample_n = min(n, 3000)
    sample = df[mask].sample(sample_n, random_state=42)
    ax1.scatter(sample['UMAP_X'], sample['UMAP_Y'],
               c=[colors_major[cluster]], s=1.2, alpha=0.55, rasterized=True)
    handles_left.append(
        Line2D([0], [0], marker='o', color='w', markerfacecolor=colors_major[cluster],
               markersize=9, label=f'{cluster} ({n:,})')
    )

ax1.set_title('Semantic Clustering of taVNS Research Terms\n(UMAP projection)', fontsize=14, fontweight='bold')
ax1.set_xlabel('UMAP_X'); ax1.set_ylabel('UMAP_Y')
ax1.set_xticks([]); ax1.set_yticks([])

leg1 = ax1.legend(handles=handles_left, loc='upper left', bbox_to_anchor=(1.01, 1),
                  fontsize=7.5, frameon=True, title='Major Clusters',
                  title_fontsize=9.5, ncol=1, borderpad=0.6, handletextpad=0.5,
                  labelspacing=0.3)

# ===================== RIGHT =====================
for cat in ['Basic Research', 'Clinical', 'Both']:
    mask = df['CategoryEn'] == cat
    n = mask.sum()
    sample_n = min(n, 4000)
    sample = df[mask].sample(sample_n, random_state=42)
    ax2.scatter(sample['UMAP_X'], sample['UMAP_Y'],
               c=[cat_colors[cat]], s=1.2, alpha=0.45, rasterized=True,
               label=f'{cat} ({n:,})')

ax2.set_title('Basic Research vs Clinical\n(UMAP projection)', fontsize=14, fontweight='bold')
ax2.set_xlabel('UMAP_X'); ax2.set_ylabel('UMAP_Y')
ax2.set_xticks([]); ax2.set_yticks([])
ax2.legend(loc='upper left', bbox_to_anchor=(1.01, 1),
           fontsize=10, frameon=True, title='Category', title_fontsize=11,
           markerscale=2.2)

plt.tight_layout(pad=2)
fig.savefig('umap_clusters.png', dpi=200, bbox_inches='tight', facecolor='white')
print('Saved umap_clusters.png')
