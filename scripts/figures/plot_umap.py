import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
matplotlib.rcParams['axes.unicode_minus'] = False

df = pd.read_csv('terms-clustered.csv')

# Map MajorCluster integer to English names (based on earlier analysis)
name_map = {
    -1: 'Noise',
    0: 'Psychiatric & Emotional Disorders',
    1: 'Sleep Disorders',
    2: 'Clinical Trial Methodology',
    3: 'Animal Models',
    4: 'Cognitive Function',
    5: 'Autonomic & Cardiovascular',
    6: 'Neuroimaging',
    7: 'Stroke & Brain Injury',
    8: 'Autonomic & Cardiovascular',
    9: 'VNS Core Terms',
    10: 'Stimulation Parameters & Devices',
    11: 'Inflammation & Immunity',
    12: 'Psychiatric & Emotional Disorders',
    13: 'Perioperative & Surgical',
    14: 'Perioperative & Surgical',
    15: 'Inflammation & Immunity',
    16: 'Psychiatric & Emotional Disorders',
    17: 'Brain Regions & Circuits'
}

df['cluster_name'] = df['MajorCluster'].map(name_map)

# Colors - 14 distinct colors
colors = {
    'Brain Regions & Circuits': '#1f77b4',
    'Inflammation & Immunity': '#ff7f0e',
    'Stimulation Parameters & Devices': '#2ca02c',
    'Psychiatric & Emotional Disorders': '#d62728',
    'Perioperative & Surgical': '#9467bd',
    'Autonomic & Cardiovascular': '#8c564b',
    'Clinical Trial Methodology': '#e377c2',
    'VNS Core Terms': '#7f7f7f',
    'Stroke & Brain Injury': '#bcbd22',
    'Animal Models': '#17becf',
    'Cognitive Function': '#aec7e8',
    'Neuroimaging': '#ffbb78',
    'Sleep Disorders': '#98df8a',
    'Noise': '#d3d3d3'
}

counts = df['cluster_name'].value_counts()

# Order by size (Noise last)
ordered = [c for c in counts.index if c != 'Noise'] + (['Noise'] if 'Noise' in counts.index else [])

fig, ax = plt.subplots(figsize=(20, 13))

# Noise first (bottom layer)
noise_df = df[df['cluster_name'] == 'Noise']
ax.scatter(noise_df['UMAP_X'], noise_df['UMAP_Y'], s=20, c='lightgray', alpha=0.06,
           edgecolors='none')

# Each cluster
for name in ordered:
    if name == 'Noise':
        continue
    sub = df[df['cluster_name'] == name]
    ax.scatter(sub['UMAP_X'], sub['UMAP_Y'], s=30, c=colors[name], alpha=0.75,
               edgecolors='white', linewidth=0.3, label=f'{name} ({counts[name]:,})')

ax.set_xlabel('UMAP 1', fontsize=22, fontweight='bold')
ax.set_ylabel('UMAP 2', fontsize=22, fontweight='bold')
ax.tick_params(labelsize=15)
ax.set_title('Semantic Clustering of taVNS Research Terms\n(HDBSCAN + UMAP)', 
             fontsize=20, fontweight='bold', pad=18)

# Legend on right side, outside
legend = ax.legend(loc='center left', bbox_to_anchor=(1.02, 0.5), fontsize=13,
                   markerscale=1.2, frameon=True, edgecolor='#cccccc',
                   title='Cluster', title_fontsize=14)
legend.get_title().set_fontweight('bold')

plt.tight_layout()
fig.savefig('umap_clusters.png', dpi=180, bbox_inches='tight', facecolor='white')
plt.close()
print('Done: umap_clusters.png')
print(f'Total points plotted: {len(df)}')
print('Cluster counts:')
for name in ordered:
    print(f'  {name}: {counts[name]:,}')
