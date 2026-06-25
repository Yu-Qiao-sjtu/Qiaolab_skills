import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

plt.rcParams['font.family'] = 'Arial'

# Load rising burst terms
burst = pd.read_csv('D:/term/basic-mechanism-burst.csv')
rising = burst[(burst['2026'] > burst['2025'])].copy()
rising = rising.sort_values('Total_2025_2026', ascending=False)

curated = [
    ('synaptic plasticity', 'Stroke & Brain Injury'),
    ('noninvasive neuromodulation technique', 'Cognitive Function'),
    ('transcriptomic analysis', 'Inflammation & Immunity'),
    ('macrophage polarization', 'Inflammation & Immunity'),
    ('immune-inflammatory responses', 'Inflammation & Immunity'),
    ('glucagon-like peptide-1', 'Inflammation & Immunity'),
    ('oligodendrocyte precursor cells', 'Inflammation & Immunity'),
    ('gadd45 beta', 'Inflammation & Immunity'),
    ('promoting neuroplasticity', 'Stroke & Brain Injury'),
    ('remote ischemic conditioning', 'Stroke & Brain Injury'),
    ('inflammatory disease', 'Inflammation & Immunity'),
    ('noise exposure', 'Animal Models'),
]

rows = []
for term, cat in curated:
    r = rising[rising['TERM'] == term]
    if len(r) == 0:
        continue
    row_data = r.iloc[0]
    rows.append({
        'term': term,
        'cat': cat,
        'c25': int(row_data['2025']),
        'c26': int(row_data['2026']),
        'total': int(row_data['Total_2025_2026']),
    })

df = pd.DataFrame(rows)
df = df.sort_values('total', ascending=True)

cat_colors = {
    'Inflammation & Immunity': '#D43F3A',
    'Stroke & Brain Injury': '#4A9EC8',
    'Cognitive Function': '#3A5F8A',
    'Animal Models': '#E8925E',
}

fig, ax = plt.subplots(figsize=(7.8, 4.8))
fig.subplots_adjust(right=0.72)

y_pos = range(len(df))

# Draw category background shading
cat_boundaries = {}
for i, (_, row) in enumerate(df.iterrows()):
    cat = row['cat']
    if cat not in cat_boundaries:
        cat_boundaries[cat] = [i, i]
    else:
        cat_boundaries[cat][1] = i

# Alternate category background
for cat, (ymin, ymax) in cat_boundaries.items():
    color = cat_colors.get(cat, '#888888')
    ax.axhspan(ymin - 0.45, ymax + 0.45, facecolor=color, alpha=0.06, zorder=0)

for i, (_, row) in enumerate(df.iterrows()):
    c25 = row['c25']
    c26 = row['c26']
    cat = row['cat']
    color = cat_colors.get(cat, '#888888')
    
    # Dumbbell line
    ax.plot([c25, c26], [i, i], color=color, linewidth=3.2, alpha=0.5, zorder=2, solid_capstyle='round')
    
    # 2025 dot
    if c25 > 0:
        ax.scatter(c25, i, s=130, facecolor='white', edgecolor=color, linewidth=2, zorder=4)
        ax.text(c25, i, str(c25), ha='center', va='center', fontsize=7.5, fontweight='bold', color=color, zorder=5)
    else:
        ax.scatter(0.04, i, s=45, facecolor=color, edgecolor=color, linewidth=1, alpha=0.45, zorder=4, marker='D')
    
    # 2026 dot
    ax.scatter(c26, i, s=190, facecolor=color, edgecolor='white', linewidth=1.8, zorder=4)
    ax.text(c26, i, str(c26), ha='center', va='center', fontsize=8, fontweight='bold', color='white', zorder=5)

# Y-axis
ax.set_yticks(y_pos)
ax.set_yticklabels(df['term'].values, fontsize=9)
ax.invert_yaxis()
ax.tick_params(axis='y', length=0)

# X-axis
max_x = df['c26'].max() + 0.4
ax.set_xlabel('Publications', fontsize=11, fontweight='bold', color='#333333')
ax.set_xlim(-0.15, max_x)
ax.set_xticks(range(0, int(max_x)+1))

# Legend (outside, right)
legend_patches = []
for cat in ['Inflammation & Immunity', 'Stroke & Brain Injury', 'Cognitive Function', 'Animal Models']:
    legend_patches.append(mpatches.Patch(color=cat_colors[cat], label=cat, alpha=0.9))

leg1 = ax.legend(handles=legend_patches, loc='center left', bbox_to_anchor=(1.02, 0.62),
                 fontsize=9, frameon=True, edgecolor='#CCCCCC', facecolor='white',
                 title='Category', title_fontsize=10, handlelength=1.3, handleheight=1.3,
                 borderpad=0.8)
ax.add_artist(leg1)

# Year legend
year_handles = [
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='white', markeredgecolor='#555555',
               markersize=9, markeredgewidth=1.8, label='2025'),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#555555', markeredgecolor='white',
               markersize=10, markeredgewidth=1.5, label='2026'),
]
leg2 = ax.legend(handles=year_handles, loc='center left', bbox_to_anchor=(1.02, 0.25),
                 fontsize=9, frameon=True, edgecolor='#CCCCCC', title='Year', title_fontsize=10,
                 borderpad=0.8)
ax.add_artist(leg2)

# Category labels on right side of plot area
for cat, (ymin, ymax) in cat_boundaries.items():
    ymid = (ymin + ymax) / 2
    color = cat_colors.get(cat, '#888888')
    short = cat.replace('Inflammation & Immunity', 'Inflammation\n& Immunity')\
               .replace('Stroke & Brain Injury', 'Stroke &\nBrain Injury')
    ax.text(max_x + 0.03, ymid, short, fontsize=8, fontweight='bold', color=color,
            ha='left', va='center')

ax.set_title('De Novo Rising Signals in Basic Mechanism\n(New Terms 2025\u20132026, 2026 > 2025)', 
             fontsize=12, fontweight='bold', pad=10, color='#222222')

# Style
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#CCCCCC')
ax.spines['bottom'].set_color('#CCCCCC')
ax.tick_params(axis='both', colors='#555555', length=4)
ax.grid(axis='x', alpha=0.12, linewidth=0.5)

plt.tight_layout()
fig.savefig('D:/term/figure_rising_signals.png', dpi=600, bbox_inches='tight', facecolor='white')
fig.savefig('D:/term/figure_rising_signals.pdf', bbox_inches='tight', facecolor='white')
print('Saved.')
