import pandas as pd, numpy as np, matplotlib.pyplot as plt
from distinctipy import get_colors
plt.rcParams['font.family'] = 'Microsoft YaHei'

df = pd.read_csv('data/clustering/terms-clustered.csv')
major_counts = df['MajorName'].value_counts()
valid_majors = [m for m in major_counts.index.tolist() if 'Brain Regions' not in str(m) and 'Noise' not in str(m)]
years = [str(y) for y in range(2002, 2027)]

annual = {}
for mc in valid_majors:
    sub = df[df['MajorName'] == mc]
    annual[mc] = {int(y): sub[y].sum() for y in years}

annual_df = pd.DataFrame(annual).T
annual_df = annual_df.sort_values(by=list(range(2002, 2027)), ascending=False)

top12 = annual_df.index.tolist()
n = len(top12)

# 12 distinct colors
colors = get_colors(n, exclude_colors=[(1,1,1), (0.92,0.92,0.92), (0.85,0.85,0.85)])

fig, ax = plt.subplots(figsize=(20, 8))
y_vals = np.zeros(len(years))
x = np.arange(len(years))

for i, mc in enumerate(top12):
    vals = np.array([annual[mc].get(int(y), 0) for y in years], dtype=float)
    ax.fill_between(x, y_vals, y_vals + vals, color=colors[i], alpha=0.85, lw=0)
    y_vals = y_vals + vals

# No title, no labels, no legend, no right-side annotations
ax.set_xlim(-0.5, len(years) - 0.5)
ax.set_xticks(x)
ax.set_xticklabels(years, fontsize=15)
ax.set_yticklabels([])
for spine in ['top', 'right', 'left']:
    ax.spines[spine].set_visible(False)

plt.tight_layout(pad=0.5)
fig.savefig('figures/fig1_streamgraph_nolabels.png', dpi=1200, bbox_inches='tight', facecolor='white')
fig.savefig('figures/fig1_streamgraph_nolabels.pdf', bbox_inches='tight', facecolor='white')
print(f'Saved: figures/fig1_streamgraph_nolabels.png ({fig.get_size_inches()} inches)')
