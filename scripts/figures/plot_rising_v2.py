import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

plt.rcParams['font.family'] = 'Arial'

# Load rising burst terms
burst = pd.read_csv('D:/term/basic-mechanism-burst.csv')
rising = burst[(burst['2026'] > burst['2025'])].copy()  # strictly rising
rising = rising.sort_values('Total_2025_2026', ascending=False)

# Curated top rising terms (2026 > 2025)
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
    # if multiple matches, take first
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
    'Inflammation & Immunity': '#E64B35',
    'Stroke & Brain Injury': '#4DBBD5',
    'Autonomic & Cardiovascular': '#00A087',
    'Cognitive Function': '#3C5488',
    'Animal Models': '#F39B7F',
}

fig, ax = plt.subplots(figsize=(7.2, 4.8))

y_pos = range(len(df))

for i, (_, row) in enumerate(df.iterrows()):
    c25 = row['c25']
    c26 = row['c26']
    cat = row['cat']
    color = cat_colors.get(cat, '#888888')
    
    # Dumbbell line (always from c25 to c26, c26 > c25 guaranteed)
    ax.plot([c25, c26], [i, i], color=color, linewidth=3, alpha=0.55, zorder=2, solid_capstyle='round')
    
    # 2025 dot
    if c25 > 0:
        ax.scatter(c25, i, s=140, facecolor='white', edgecolor=color, linewidth=2.2, zorder=4)
        ax.text(c25, i, str(c25), ha='center', va='center', fontsize=8, fontweight='bold', color=color, zorder=5)
    else:
        # Diamond for zero
        ax.scatter(0.04, i, s=50, facecolor=color, edgecolor=color, linewidth=1.2, alpha=0.5, zorder=4, marker='D')
    
    # 2026 dot (filled, larger)
    ax.scatter(c26, i, s=200, facecolor=color, edgecolor='white', linewidth=1.8, zorder=4)
    ax.text(c26, i, str(c26), ha='center', va='center', fontsize=8.5, fontweight='bold', color='white', zorder=5)

# Y-axis
ax.set_yticks(y_pos)
ax.set_yticklabels(df['term'].values, fontsize=9.5)
ax.invert_yaxis()

# X-axis
max_x = df['c26'].max() + 0.5
ax.set_xlabel('Number of publications', fontsize=11, fontweight='bold', color='#444444')
ax.set_xlim(-0.2, max_x)
ax.set_xticks(range(0, int(max_x)+1))
ax.set_xticklabels([str(x) for x in range(0, int(max_x)+1)], fontsize=10)

# Category color bands (right side of term labels)
for i, (_, row) in enumerate(df.iterrows()):
    cat = row['cat']
    color = cat_colors.get(cat, '#888888')
    ax.axhline(y=i, xmin=1.02, xmax=1.06, color=color, linewidth=7, solid_capstyle='butt', clip_on=False)

# Legend
legend_patches = []
for cat in ['Inflammation & Immunity', 'Stroke & Brain Injury', 'Cognitive Function', 'Animal Models']:
    legend_patches.append(mpatches.Patch(color=cat_colors[cat], label=cat))

leg1 = ax.legend(handles=legend_patches, loc='center left', bbox_to_anchor=(1.02, 0.5),
                 fontsize=8.5, frameon=True, edgecolor='#DDDDDD', title='Category',
                 title_fontsize=9.5, handlelength=1.2, handleheight=1.2)

# Year legend
year_handles = [
    plt.scatter([], [], s=80, facecolor='white', edgecolor='#666666', linewidth=2, label='2025'),
    plt.scatter([], [], s=100, facecolor='#666666', edgecolor='white', linewidth=1.5, label='2026'),
]
leg2 = ax.legend(handles=year_handles, loc='lower right', fontsize=9, frameon=True,
                 edgecolor='#DDDDDD', title='Year', title_fontsize=9.5)
ax.add_artist(leg1)

# Title
ax.set_title('De Novo Rising Signals in Basic Mechanism Research\n(New Terms 2025\u20132026, with 2026 > 2025)', 
             fontsize=12, fontweight='bold', pad=10, color='#333333')

# Style
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#CCCCCC')
ax.spines['bottom'].set_color('#CCCCCC')
ax.tick_params(axis='both', colors='#555555', length=4)
ax.grid(axis='x', alpha=0.15, linewidth=0.5)

plt.tight_layout()
fig.savefig('D:/term/figure_rising_signals.png', dpi=600, bbox_inches='tight', facecolor='white')
fig.savefig('D:/term/figure_rising_signals.pdf', bbox_inches='tight', facecolor='white')
print('Saved.')
print(df[['term','cat','c25','c26']].to_string(index=False))
