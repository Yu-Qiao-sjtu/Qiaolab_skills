import pandas as pd, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.font_manager import FontProperties

# ── load ──
df = pd.read_csv('terms-classified.csv')
df_basic = df[df['Category'].isin(['basic','both'])].copy()

yr_old = ['2022','2023','2024']
df_basic['old_sum'] = df_basic[yr_old].sum(axis=1)
df_basic['new_sum'] = df_basic['2025'] + df_basic['2026']

rising = df_basic[
    (df_basic['old_sum'] == 0) &
    (df_basic['2026'] > df_basic['2025']) &
    (df_basic['new_sum'] > 0)
].copy()
rising = rising.sort_values('new_sum', ascending=False)

# ── filter out generic method terms ──
remove = {
    'central mechanism', 'expression level', 'protein level', 'brain tissue',
    'enhancing cognitive function', 'event segmentation', 'inflammatory disease',
    'ongoing event representation', 'transcriptomic analysis',
    'immunofluorescence staining', 'behavioral test', 'western blot analysis',
    'statistical analysis', 'control group', 'experimental group',
    'significant difference', 'significant increase', 'significant decrease',
    'significant effect', 'no significant difference'
}
rising_clean = rising[~rising['TERM'].str.lower().isin([r.lower() for r in remove])]
top = rising_clean.head(15)

# Build data
terms = []
vals_25 = []
vals_26 = []
for _, r in top.iterrows():
    terms.append(r['TERM'])
    vals_25.append(int(r['2025']))
    vals_26.append(int(r['2026']))

# Reverse so strongest at top
terms = terms[::-1]
vals_25 = vals_25[::-1]
vals_26 = vals_26[::-1]

# ── colours ──
GREY  = '#D9D5D0'
RED   = '#C44E52'
WHITE = '#FFFFFF'
BG    = '#FAFAF8'

# ── plot ──
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.edgecolor'] = '#888888'
plt.rcParams['axes.linewidth'] = 0.6

fig, ax = plt.subplots(figsize=(6.5, 6.5))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

N = len(terms)

for i in range(N):
    for j, val in enumerate([vals_25[i], vals_26[i]]):
        xx = j
        yy = i
        if val == 0:
            color = GREY
        else:
            color = RED
        rect = mpatches.FancyBboxPatch(
            (xx - 0.42, yy - 0.38), 0.84, 0.76,
            boxstyle="round,pad=0.04",
            facecolor=color, edgecolor='white', linewidth=1.0
        )
        ax.add_patch(rect)
        if val > 0:
            ax.text(xx, yy, str(val), ha='center', va='center',
                    fontsize=10, fontweight='bold',
                    color='white' if val >= 3 else '#5A1A1A')

# Axes
ax.set_xlim(-0.6, 1.6)
ax.set_ylim(-0.6, N - 0.4)
ax.set_xticks([0, 1])
ax.set_xticklabels(['2025', '2026'], fontsize=13, fontweight='bold')
ax.set_yticks(range(N))
ax.set_yticklabels(terms, fontsize=10)
ax.tick_params(left=False, bottom=False)
ax.xaxis.set_ticks_position('top')
ax.xaxis.set_label_position('top')

# Grid lines (light horizontal)
for i in range(N):
    ax.axhline(y=i + 0.5, color='#E0E0DC', linewidth=0.4, zorder=0)

# Title
ax.set_title('Emerging signals in basic mechanism research (2025–2026)',
             fontsize=13, fontweight='bold', pad=12)

# Legend
leg_vals = [mpatches.Patch(facecolor=RED,  edgecolor='white', label='Active'),
            mpatches.Patch(facecolor=GREY, edgecolor='white', label='Absent')]
ax.legend(handles=leg_vals, loc='lower right', frameon=True,
          facecolor=BG, edgecolor='#CCCCCC', fontsize=9,
          ncol=2, borderpad=0.5)

plt.tight_layout()
fig.savefig('figure_rising_strips.png', dpi=600, facecolor=BG, edgecolor='none')
fig.savefig('figure_rising_strips.pdf', facecolor=BG, edgecolor='none')
plt.close()

print('Done: figure_rising_strips.png + .pdf')
print(f'Terms: {N}')
