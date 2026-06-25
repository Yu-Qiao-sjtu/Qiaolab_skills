#!/usr/bin/env python3
"""Plot rising signals (2026 > 2025) from basic mechanism layer as horizontal color strips."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.ticker import FixedLocator
import pandas as pd
import numpy as np
import os

# ── Load data ──────────────────────────────────────────────────
df = pd.read_csv('basic-mechanism-burst.csv')

# Rising signals only: 2026 > 2025
rising = df[df['2026'] > df['2025']].copy()
rising = rising.nlargest(55, 'Total_2025_2026')

# Sort: bottom = strongest (highest total)
rising = rising.sort_values('Total_2025_2026', ascending=True)
N = len(rising)

print(f'Rising signals plotted: {N}')
for _, r in rising.iterrows():
    print(f"  {r['TERM']:50s} {r['SubCategory']:30s} 2025={int(r['2025'])} 2026={int(r['2026'])}")

# ── Color palette ──────────────────────────────────────────────
# Elegant warm-toned palette for paper
GRAY_ZERO = '#E5E3E0'       # warm light gray for frequency=0

# Red progression (warm brick red)
RED_PALETTE = {
    1: '#F2C4C0',   # pale rose
    2: '#E89088',   # medium rose
    3: '#D05048',   # strong red
    4: '#A82028',   # deep brick red
    5: '#801018',   # darkest for 5+
}

def color_for_freq(f):
    if f <= 0:
        return GRAY_ZERO
    if f >= 5:
        return RED_PALETTE[5]
    return RED_PALETTE.get(int(f), RED_PALETTE[1])

def text_color_for_freq(f):
    """White text on dark cells, dark text on light cells."""
    if f >= 3:
        return 'white'
    return '#333333'

# ── Figure setup ───────────────────────────────────────────────
# Narrow, tall figure suitable for paper single column
fig, ax = plt.subplots(figsize=(5.5, max(6, N * 0.33)))

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'STIXGeneral', 'DejaVu Serif'],
    'font.size': 9,
    'axes.titlesize': 11,
    'axes.labelsize': 10,
})

# ── Draw ───────────────────────────────────────────────────────
bar_height = 0.7
gap_between_years = 0.08   # tiny white gap between 2025 and 2026 segments

for i, (_, row) in enumerate(rising.iterrows()):
    y = i
    freq25 = int(row['2025'])
    freq26 = int(row['2026'])

    # Draw two horizontal segments per row
    # 2025 segment (left)
    c25 = color_for_freq(freq25)
    rect25 = mpatches.FancyBboxPatch(
        (0, y - bar_height/2),
        1.0, bar_height,
        boxstyle='round,pad=0.015',
        facecolor=c25, edgecolor='none', linewidth=0
    )
    ax.add_patch(rect25)

    # 2026 segment (right)
    x26_start = 1.0 + gap_between_years
    c26 = color_for_freq(freq26)
    rect26 = mpatches.FancyBboxPatch(
        (x26_start, y - bar_height/2),
        1.0, bar_height,
        boxstyle='round,pad=0.015',
        facecolor=c26, edgecolor='none', linewidth=0
    )
    ax.add_patch(rect26)

    # Annotate frequency number on red cells
    if freq25 > 0:
        ax.text(0.5, y, str(freq25), ha='center', va='center',
                fontsize=7.5, fontweight='bold', color=text_color_for_freq(freq25))
    if freq26 > 0:
        ax.text(x26_start + 0.5, y, str(freq26), ha='center', va='center',
                fontsize=7.5, fontweight='bold', color=text_color_for_freq(freq26))

# ── Y-axis: term labels ────────────────────────────────────────
term_labels = rising['TERM'].tolist()
ax.set_yticks(range(N))
ax.set_yticklabels(term_labels, fontsize=8, va='center')
ax.set_ylim(-0.7, N - 0.3)

# ── X-axis ─────────────────────────────────────────────────────
ax.set_xlim(-0.05, 2.0 + gap_between_years + 0.05)
ax.set_xticks([0.5, 1.0 + gap_between_years + 0.5])
ax.set_xticklabels(['2025', '2026'], fontsize=10, fontweight='bold')
ax.xaxis.set_ticks_position('none')

# Light column background tints
ax.axvspan(0, 1.0, alpha=0.03, color='black', zorder=-1)
ax.axvspan(1.0 + gap_between_years, 2.0 + gap_between_years, alpha=0.03, color='black', zorder=-1)

# ── Legend ─────────────────────────────────────────────────────
legend_patches = []
legend_patches.append(mpatches.Patch(color=GRAY_ZERO, label='0'))
for v, c in RED_PALETTE.items():
    legend_patches.append(mpatches.Patch(color=c, label=f'{v}' if v < 5 else '5+'))

leg = ax.legend(
    handles=legend_patches,
    title='Frequency',
    loc='upper left',
    bbox_to_anchor=(1.01, 1.0),
    frameon=True,
    framealpha=0.9,
    edgecolor='#CCCCCC',
    fontsize=8,
    title_fontsize=9,
    ncol=1,
    borderpad=0.6,
    handleheight=1.2,
    handlelength=1.5,
    labelspacing=0.4,
)
leg.get_frame().set_linewidth(0.5)

# ── Styling ────────────────────────────────────────────────────
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.tick_params(axis='y', length=0)
ax.tick_params(axis='x', length=0)

# Title
ax.set_title(
    'Rising New Signals in Basic Mechanism Literature\n(2025\u2009\u2192\u20092026, previously absent)',
    fontsize=11, fontweight='bold', pad=14
)

plt.tight_layout(pad=0.8)

# ── Save ───────────────────────────────────────────────────────
fig.savefig('figure_rising_strips.png', dpi=600, bbox_inches='tight',
            facecolor='white', edgecolor='none')
fig.savefig('figure_rising_strips.pdf', bbox_inches='tight',
            facecolor='white', edgecolor='none')
print('\nSaved: figure_rising_strips.png / .pdf')
