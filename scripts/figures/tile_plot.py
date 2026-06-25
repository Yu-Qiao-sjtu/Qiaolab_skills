import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Read data
df = pd.read_csv(r'D:\term\burst-terms-full.csv')

# Filter: basic, rising (2026 > 2025), burst (2022-2024 = 0 already)
rising = df[(df['Category'] == 'basic') & (df['2026'] > df['2025'])].copy()

# Sort by total and take top 25
rising = rising.sort_values('Total_2025_2026', ascending=False).head(25)

# Reverse for top-to-bottom display
rising = rising.iloc[::-1]

terms = rising['TERM'].tolist()
val_2025 = rising['2025'].tolist()
val_2026 = rising['2026'].tolist()

# Build data matrix: rows=terms, cols=[2025, 2026]
data = np.column_stack([val_2025, val_2026])

# Colors: gray for 0, red gradient for >0
n_rows = len(terms)
n_cols = 2

fig, ax = plt.subplots(figsize=(4.2, 7.5))

# Draw tiles
for i in range(n_rows):
    for j in range(n_cols):
        v = data[i, j]
        if v == 0:
            color = '#E8E8E8'  # light gray
            text_color = '#AAAAAA'
        else:
            # Red intensity: light red for 1, dark red for 4+
            intensity = min(v, 4) / 4.0
            color = plt.cm.Reds(0.3 + 0.7 * intensity)
            text_color = 'white' if v >= 3 else '#8B0000'
        
        rect = mpatches.FancyBboxPatch(
            (j + 0.08, i + 0.08), 0.84, 0.84,
            boxstyle="round,pad=0.02",
            facecolor=color, edgecolor='white', linewidth=1.2
        )
        ax.add_patch(rect)
        ax.text(j + 0.5, i + 0.5, str(v), ha='center', va='center',
                fontsize=11, fontweight='bold', color=text_color)

# Axes
ax.set_xlim(0, 2)
ax.set_ylim(0, n_rows)
ax.set_xticks([0.5, 1.5])
ax.set_xticklabels(['2025', '2026'], fontsize=14, fontweight='bold')
ax.set_yticks(np.arange(n_rows) + 0.5)
ax.set_yticklabels(terms, fontsize=10.5)
ax.tick_params(left=False, bottom=False)

# Grid lines
for i in range(1, n_rows):
    ax.axhline(i, color='white', linewidth=0.8, alpha=0.5)

ax.set_xlabel('')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)

ax.set_title('Rising Basic-Mechanism Burst Terms\n(2022–2024 absent, 2026 > 2025)', 
             fontsize=14, fontweight='bold', pad=14)

plt.tight_layout()
fig.savefig(r'D:\term\figure_rising_tiles.png', dpi=600, bbox_inches='tight',
            facecolor='white', edgecolor='none')
fig.savefig(r'D:\term\figure_rising_tiles.pdf', bbox_inches='tight',
            facecolor='white', edgecolor='none')
print('Saved figure_rising_tiles.png and .pdf')
