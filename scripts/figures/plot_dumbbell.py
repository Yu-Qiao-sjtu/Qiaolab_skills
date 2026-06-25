import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 11

# ── Data ──────────────────────────────────────────────────
df = pd.read_csv('D:/term/basic-mechanism-burst.csv')

# Curated top 14 burst terms with good category diversity
selected = [
    ("myocardial infarction",           "Autonomic & Cardiovascular"),
    ("continuous glucose monitoring",   "Inflammation & Immunity"),
    ("chronic heart failure",           "Autonomic & Cardiovascular"),
    ("autonomic imbalance",             "Autonomic & Cardiovascular"),
    ("neuromodulation technique",       "Cognitive Function"),
    ("noninvasive neuromodulation technique", "Cognitive Function"),
    ("acute mental stress",             "Autonomic & Cardiovascular"),
    ("ventricular ejection fraction",   "Autonomic & Cardiovascular"),
    ("synaptic plasticity",             "Stroke & Brain Injury"),
    ("macrophage polarization",         "Inflammation & Immunity"),
    ("glucagon-like peptide-1",         "Inflammation & Immunity"),
    ("immune-inflammatory responses",   "Inflammation & Immunity"),
    ("remote ischemic conditioning",    "Stroke & Brain Injury"),
    ("oligodendrocyte precursor cells", "Inflammation & Immunity"),
]

rows = []
for term, cat in selected:
    match = df[(df['TERM'].str.strip().str.lower() == term.lower()) & 
               (df['SubCategory'].str.strip() == cat)]
    if len(match) > 0:
        r = match.iloc[0]
        rows.append({
            'term': term,
            'cat': cat,
            'y2025': int(r['2025']),
            'y2026': int(r['2026']),
            'total': int(r['Total_2025_2026']),
        })

data = pd.DataFrame(rows)
# Sort: by category then by total desc
cat_order = ['Autonomic & Cardiovascular', 'Inflammation & Immunity', 
             'Stroke & Brain Injury', 'Cognitive Function']
data['cat_rank'] = data['cat'].apply(lambda x: cat_order.index(x) if x in cat_order else 99)
data = data.sort_values(['cat_rank', 'total'], ascending=[True, False])
data = data.reset_index(drop=True)

# ── Colors ────────────────────────────────────────────────
# High-contrast year colors
COLOR_2025 = '#0072B5'   # deep blue
COLOR_2026 = '#D41159'   # vivid crimson/magenta

# Category colors (muted, used only for the connecting line and right-side labels)
cat_palette = {
    'Autonomic & Cardiovascular': '#648FFF',
    'Inflammation & Immunity':    '#DC267F',
    'Stroke & Brain Injury':      '#FE6100',
    'Cognitive Function':         '#785EF0',
}

# Short labels for right side
short_cat = {
    'Autonomic & Cardiovascular': 'Cardiovascular',
    'Inflammation & Immunity':    'Inflammation',
    'Stroke & Brain Injury':      'Stroke / TBI',
    'Cognitive Function':         'Cognitive',
}

# ── Plot ──────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7.2, 5.6))

n = len(data)
y_positions = range(n)

# Horizontal dumbbell: 2025 (left) -> 2026 (right)
for i, row in data.iterrows():
    cat = row['cat']
    line_color = cat_palette.get(cat, '#AAAAAA')
    ax.plot([row['y2025'], row['y2026']], [i, i],
            color=line_color, linewidth=2.2, solid_capstyle='round', zorder=2)

# Scatter points — larger, distinct colors
ax.scatter(data['y2025'], y_positions, s=140, c=COLOR_2025, 
           edgecolors='white', linewidth=0.8, zorder=4, label='2025')
ax.scatter(data['y2026'], y_positions, s=140, c=COLOR_2026,
           edgecolors='white', linewidth=0.8, zorder=4, label='2026')

# Y-axis labels (terms)
ax.set_yticks(y_positions)
ax.set_yticklabels(data['term'], fontsize=11, fontstyle='italic')

# X-axis
max_x = max(data['y2025'].max(), data['y2026'].max()) + 1
ax.set_xlim(-0.3, max_x)
ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
ax.set_xlabel('Frequency in literature', fontsize=13, fontweight='bold')

# Category grouping — add faint horizontal separators and right-side labels
prev_cat = None
boundaries = []
for i, row in data.iterrows():
    cat = row['cat']
    if cat != prev_cat and prev_cat is not None:
        boundaries.append(i - 0.5)
    prev_cat = cat

for b in boundaries:
    ax.axhline(y=b, color='#CCCCCC', linewidth=0.7, linestyle=':')

# Right-side category labels
prev_cat = None
cat_start = {}
cat_end = {}
for i, row in data.iterrows():
    cat = row['cat']
    if cat != prev_cat:
        cat_start[cat] = i
        if prev_cat is not None:
            cat_end[prev_cat] = i - 1
    prev_cat = cat
cat_end[prev_cat] = n - 1

for cat in cat_start:
    mid = (cat_start[cat] + cat_end[cat]) / 2
    ax.text(max_x + 0.25, mid, short_cat.get(cat, cat),
            fontsize=10, fontweight='bold', color=cat_palette.get(cat, '#555555'),
            ha='left', va='center')

# Legend — prominent, top right inside
legend = ax.legend(loc='upper right', fontsize=12, frameon=True,
                   framealpha=0.95, edgecolor='#CCCCCC',
                   markerscale=1.3, handletextpad=0.8, borderpad=0.7)
# Make legend text bold
for text in legend.get_texts():
    text.set_fontweight('bold')

# Style
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#AAAAAA')
ax.spines['bottom'].set_color('#AAAAAA')
ax.tick_params(axis='both', colors='#333333', labelsize=10)
ax.yaxis.set_tick_params(pad=8)

# Title
ax.set_title('Bursting terms emerging in 2025–2026\n(previously absent from taVNS literature)',
             fontsize=14, fontweight='bold', pad=14)

plt.tight_layout(rect=[0, 0, 0.85, 1])  # make room for right labels

fig.savefig('D:/term/figure_burst_dumbbell.png', dpi=600, bbox_inches='tight',
            facecolor='white', edgecolor='none')
fig.savefig('D:/term/figure_burst_dumbbell.pdf', bbox_inches='tight',
            facecolor='white', edgecolor='none')
print("Done: figure_burst_dumbbell.png + .pdf")
