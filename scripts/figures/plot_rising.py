import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['mathtext.fontset'] = 'custom'
plt.rcParams['mathtext.rm'] = 'Arial'

# Load rising burst terms
burst = pd.read_csv('D:/term/basic-mechanism-burst.csv')
rising = burst[burst['2026'] >= burst['2025']].copy()
rising = rising.sort_values('Total_2025_2026', ascending=False)

# Manually curate top rising terms — remove fragments, duplicates, generic
curated = [
    # Total=3
    ('synaptic plasticity', 'Stroke & Brain Injury'),
    ('noninvasive neuromodulation technique', 'Cognitive Function'),
    # Total=2, 0→2 (pure de novo)
    ('transcriptomic analysis', 'Inflammation & Immunity'),
    ('macrophage polarization', 'Inflammation & Immunity'),
    ('immune-inflammatory responses', 'Inflammation & Immunity'),
    ('glucagon-like peptide-1', 'Inflammation & Immunity'),
    ('oligodendrocyte precursor cells', 'Inflammation & Immunity'),
    ('gadd45 beta', 'Inflammation & Immunity'),
    ('promoting neuroplasticity', 'Stroke & Brain Injury'),
    ('remote ischemic conditioning', 'Stroke & Brain Injury'),
    # Total=2, 1→1 (stable new)
    ('bdnf level', 'Inflammation & Immunity'),
    ('blood pressure variability', 'Autonomic & Cardiovascular'),
    ('autonomic dysregulation', 'Autonomic & Cardiovascular'),
    ('locus coeruleus-norepinephrine activity', 'Inflammation & Immunity'),
]

# Build data rows
rows = []
for term, cat in curated:
    r = rising[(rising['TERM'] == term) & (rising['SubCategory'] == cat)]
    if len(r) == 0:
        # fallback: search by term only
        r = rising[rising['TERM'] == term]
    if len(r) > 0:
        rows.append({
            'term': term,
            'cat': cat,
            'c25': int(r.iloc[0]['2025']),
            'c26': int(r.iloc[0]['2026']),
            'total': int(r.iloc[0]['Total_2025_2026']),
        })

df = pd.DataFrame(rows)
df = df.sort_values('total', ascending=True)

# Category colors (colorblind-friendly from ggsci NPC / Nature palette)
cat_colors = {
    'Inflammation & Immunity': '#E64B35',      # red
    'Stroke & Brain Injury': '#4DBBD5',         # cyan/teal
    'Autonomic & Cardiovascular': '#00A087',    # green
    'Cognitive Function': '#3C5488',            # navy blue
}

# Shorter display labels
label_map = {
    'Inflammation & Immunity': 'Inflammation\n& Immunity',
    'Stroke & Brain Injury': 'Stroke &\nBrain Injury',
    'Autonomic & Cardiovascular': 'Autonomic &\nCardiovascular',
    'Cognitive Function': 'Cognitive\nFunction',
}

# Build figure
fig, ax = plt.subplots(figsize=(7.5, 5.5))

y_pos = range(len(df))

for i, (_, row) in enumerate(df.iterrows()):
    c25 = row['c25']
    c26 = row['c26']
    cat = row['cat']
    color = cat_colors.get(cat, '#888888')
    
    # Dumbbell line
    ax.plot([c25, c26], [i, i], color=color, linewidth=2.5, alpha=0.7, zorder=2)
    
    # 2025 dot (if > 0, otherwise a small marker at x=0)
    if c25 > 0:
        ax.scatter(c25, i, s=160, facecolor='white', edgecolor=color, linewidth=2.5, zorder=4)
        ax.text(c25, i, str(c25), ha='center', va='center', fontsize=8.5, fontweight='bold', color=color, zorder=5)
    else:
        ax.scatter(0.05, i, s=60, facecolor=color, edgecolor=color, linewidth=1.5, alpha=0.6, zorder=4, marker='D')
    
    # 2026 dot
    if c26 > 0:
        ax.scatter(c26, i, s=240, facecolor=color, edgecolor='white', linewidth=2, zorder=4)
        ax.text(c26, i, str(c26), ha='center', va='center', fontsize=9, fontweight='bold', color='white', zorder=5)

# Y-axis labels
ax.set_yticks(y_pos)
ax.set_yticklabels(df['term'].values, fontsize=10)
ax.invert_yaxis()

# X-axis
ax.set_xlabel('Number of publications mentioning the term', fontsize=12, fontweight='bold')
ax.set_xlim(-0.3, 3.8)
ax.set_xticks([0, 1, 2, 3])
ax.set_xticklabels(['0', '1', '2', '3'], fontsize=11)

# Category color bands on right
for i, (_, row) in enumerate(df.iterrows()):
    cat = row['cat']
    color = cat_colors.get(cat, '#888888')
    ax.axhline(y=i, xmin=0.92, xmax=0.95, color=color, linewidth=6, solid_capstyle='butt')

# Legend for categories (right side boxes)
legend_patches = []
for cat, abbr in [('Inflammation & Immunity', 'Inflammation\n& Immunity'),
                   ('Stroke & Brain Injury', 'Stroke &\nBrain Injury'),
                   ('Autonomic & Cardiovascular', 'Autonomic &\nCardiovascular'),
                   ('Cognitive Function', 'Cognitive\nFunction')]:
    legend_patches.append(mpatches.Patch(color=cat_colors[cat], label=abbr))

leg1 = ax.legend(handles=legend_patches, loc='upper left', bbox_to_anchor=(1.01, 0.98),
                 fontsize=9, frameon=True, edgecolor='#CCCCCC', title='Category',
                 title_fontsize=10, handlelength=1.5, handleheight=1.5)

# Year legend (top right inside)
year_elements = [
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='white', markeredgecolor='#555555', 
               markersize=10, markeredgewidth=2, label='2025'),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#555555', markeredgecolor='white', 
               markersize=12, markeredgewidth=2, label='2026'),
]
leg2 = ax.legend(handles=year_elements, loc='upper right', fontsize=10, frameon=True, 
                 edgecolor='#CCCCCC', title='Year', title_fontsize=10)

ax.add_artist(leg1)

# Title
ax.set_title('Rising New Signals in Basic Mechanism Research\n(Emerging Terms 2025\u20132026, 2026 \u2265 2025)', 
             fontsize=13, fontweight='bold', pad=12)

# Style
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#AAAAAA')
ax.spines['bottom'].set_color('#AAAAAA')
ax.tick_params(axis='both', colors='#555555')
ax.grid(axis='x', alpha=0.2, linewidth=0.5)

plt.tight_layout()

# Save
fig.savefig('D:/term/figure_rising_signals.png', dpi=600, bbox_inches='tight', facecolor='white')
fig.savefig('D:/term/figure_rising_signals.pdf', bbox_inches='tight', facecolor='white')

print(f"Saved. {len(df)} terms plotted.")
print(df[['term','cat','c25','c26','total']].to_string(index=False))
