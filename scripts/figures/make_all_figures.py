#!/usr/bin/env python3
"""Generate all remaining figures: clinical strip, sankey, treemap, waterfall."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.ticker import FixedLocator
import pandas as pd
import numpy as np
import os

OUTDIR = r'D:\term\figures'
os.makedirs(OUTDIR, exist_ok=True)

# ═══════════════════════════════════════════════════════════════
# FIG 3b: Clinical-layer Rising Signal Strip Chart
# ═══════════════════════════════════════════════════════════════

print('\n=== FIG 3b: Clinical Rising Signals ===')

burst = pd.read_csv(r'D:\term\data\processed\burst-terms-full.csv')
clin = burst[burst['Category'].isin(['clinical', 'both'])].copy()
rising = clin[clin['2026'] > clin['2025']].copy()

# Exclude generic method terms in clinical context
exclude = ['protein level', 'expression level', 'immunofluorescence staining',
           'western blotting', 'p value', 'statistical significance']
rising = rising[~rising['TERM'].str.lower().isin([e.lower() for e in exclude])]

# Take top 15
rising = rising.nlargest(15, 'Total_2025_2026')
rising = rising.sort_values('Total_2025_2026', ascending=True)
N = len(rising)

print(f'Clinical rising signals: {N}')
for _, r in rising.iterrows():
    print(f"  {r['TERM']:55s} 2025={int(r['2025'])} 2026={int(r['2026'])}")

# ── Palette ──
GRAY_ZERO = '#E5E3E0'
RED_PALETTE = {1: '#F2C4C0', 2: '#E89088', 3: '#D05048', 4: '#A82028', 5: '#801018'}

def color_for_freq(f):
    if f <= 0: return GRAY_ZERO
    if f >= 5: return RED_PALETTE[5]
    return RED_PALETTE.get(int(f), RED_PALETTE[1])

def text_color(f):
    return 'white' if f >= 3 else '#333333'

# ── Figure ──
fig, ax = plt.subplots(figsize=(7, max(4, N * 0.38)))
plt.rcParams.update({'font.family': 'serif', 'font.serif': ['Times New Roman', 'DejaVu Serif'],
                     'font.size': 10, 'axes.titlesize': 14, 'axes.labelsize': 12})

bar_h = 0.65
gap = 0.08

for i, (_, row) in enumerate(rising.iterrows()):
    y = i
    f25, f26 = int(row['2025']), int(row['2026'])

    rect25 = mpatches.FancyBboxPatch((0, y - bar_h/2), 1.0, bar_h,
        boxstyle='round,pad=0.015', facecolor=color_for_freq(f25), edgecolor='none')
    ax.add_patch(rect25)

    x26 = 1.0 + gap
    rect26 = mpatches.FancyBboxPatch((x26, y - bar_h/2), 1.0, bar_h,
        boxstyle='round,pad=0.015', facecolor=color_for_freq(f26), edgecolor='none')
    ax.add_patch(rect26)

    if f25 > 0:
        ax.text(0.5, y, str(f25), ha='center', va='center', fontsize=9, fontweight='bold', color=text_color(f25))
    if f26 > 0:
        ax.text(x26 + 0.5, y, str(f26), ha='center', va='center', fontsize=9, fontweight='bold', color=text_color(f26))

ax.set_yticks(range(N))
ax.set_yticklabels(rising['TERM'].tolist(), fontsize=9.5, va='center')
ax.set_ylim(-0.7, N - 0.3)
ax.set_xlim(-0.05, 2.0 + gap + 0.05)
ax.set_xticks([0.5, 1.0 + gap + 0.5])
ax.set_xticklabels(['2025', '2026'], fontsize=12, fontweight='bold')

ax.axvspan(0, 1.0, alpha=0.03, color='black', zorder=-1)
ax.axvspan(1.0 + gap, 2.0 + gap, alpha=0.03, color='black', zorder=-1)

legend_patches = [mpatches.Patch(color=GRAY_ZERO, label='0')]
for v, c in RED_PALETTE.items():
    legend_patches.append(mpatches.Patch(color=c, label=f'{v}' if v < 5 else '5+'))
ax.legend(handles=legend_patches, title='Frequency', loc='upper left',
          bbox_to_anchor=(1.01, 1.0), frameon=True, framealpha=0.9, edgecolor='#CCC',
          fontsize=9, title_fontsize=10, ncol=1, borderpad=0.6, handleheight=1.2, handlelength=1.5)

for spine in ax.spines.values():
    spine.set_visible(False)
ax.tick_params(axis='both', length=0)
ax.set_title('Rising New Signals in Clinical Literature\n(2025\u2009\u2192\u20092026)', fontsize=14, fontweight='bold', pad=14)
plt.tight_layout(pad=0.8)

fig.savefig(os.path.join(OUTDIR, 'fig3b_clinical_rising.png'), dpi=600, bbox_inches='tight', facecolor='white')
fig.savefig(os.path.join(OUTDIR, 'fig3b_clinical_rising.pdf'), bbox_inches='tight', facecolor='white')
print('Saved: fig3b_clinical_rising.png / .pdf')
plt.close()

# ═══════════════════════════════════════════════════════════════
# FIG 4: Sankey Diagram — Research Focus Shift 2022-24 → 2025-26
# ═══════════════════════════════════════════════════════════════

print('\n=== FIG 4: Sankey ===')

terms = pd.read_csv(r'D:\term\data\processed\terms-classified.csv')

# Get MajorCluster info from clustered data
clustered = pd.read_csv(r'D:\term\data\clustering\terms-clustered.csv')

# Merge
m = terms[['TERM']].merge(clustered[['TERM', 'MajorCluster']], on='TERM', how='left')

# Assign MajorCluster to terms
terms['MajorCluster'] = m['MajorCluster']

# Remove noise and brain regions (misc pocket)
terms_clean = terms[~terms['MajorCluster'].isin(['Noise', 'Brain Regions & Circuits'])]
terms_clean = terms_clean[terms_clean['MajorCluster'].notna()]

# Aggregate by MajorCluster for two time windows
year_cols = [str(y) for y in range(2002, 2027)]
# Sum 2022-2024
terms_clean['pre_2024'] = terms_clean[['2022','2023','2024']].sum(axis=1)
terms_clean['post_2025'] = terms_clean[['2025','2026']].sum(axis=1)

# Group by MajorCluster
agg = terms_clean.groupby('MajorCluster').agg(
    pre=('pre_2024', 'sum'),
    post=('post_2025', 'sum'),
    n_terms=('TERM', 'count')
).reset_index()

agg = agg.sort_values('n_terms', ascending=False)
print(agg.to_string())

# ═══════════════════════════════════════════════════════════════
# FIG S1: Treemap
# ═══════════════════════════════════════════════════════════════

print('\n=== FIG S1: Treemap ===')

# Build hierarchy: MajorCluster → MinorCluster → count
hier = clustered[~clustered['MajorCluster'].isin(['Noise', 'Brain Regions & Circuits'])]
hier = hier[hier['MajorCluster'].notna() & hier['MinorCluster'].notna()]

# Group
treemap_data = hier.groupby(['MajorCluster', 'MinorCluster']).size().reset_index(name='count')
treemap_data = treemap_data.sort_values('count', ascending=False)

print(f'Treemap groups: {len(treemap_data)}')
print(treemap_data.head(20).to_string())

# Save treemap data
treemap_data.to_csv(r'D:\term\data\processed\treemap_data.csv', index=False)

# Use squarify
try:
    import squarify
    fig, ax = plt.subplots(figsize=(16, 10))
    
    # Color by MajorCluster
    major_clusters = treemap_data['MajorCluster'].unique()
    # Use distinctipy colors
    from distinctipy import distinctipy as dp
    colors_list = dp.get_colors(len(major_clusters))
    color_map = {mc: colors_list[i] for i, mc in enumerate(major_clusters)}
    
    colors = [color_map[mc] for mc in treemap_data['MajorCluster']]
    
    squarify.plot(sizes=treemap_data['count'], label=treemap_data['MinorCluster'],
                  color=colors, alpha=0.8, ax=ax, text_kwargs={'fontsize': 7})
    
    ax.set_title('Term Classification Hierarchy: Major → Minor Clusters', fontsize=16, fontweight='bold')
    ax.axis('off')
    
    # Legend for major clusters
    patches = [mpatches.Patch(color=color_map[mc], label=f'{mc} ({int(treemap_data[treemap_data["MajorCluster"]==mc]["count"].sum())})')
               for mc in major_clusters]
    ax.legend(handles=patches, loc='upper right', bbox_to_anchor=(1.15, 1.0),
              fontsize=7, title='Major Clusters', title_fontsize=9, ncol=2)
    
    plt.tight_layout()
    fig.savefig(os.path.join(OUTDIR, 'figS1_treemap.png'), dpi=600, bbox_inches='tight', facecolor='white')
    fig.savefig(os.path.join(OUTDIR, 'figS1_treemap.pdf'), bbox_inches='tight', facecolor='white')
    print('Saved: figS1_treemap.png / .pdf')
    plt.close()
except ImportError:
    print('squarify not installed, skipping treemap')

# ═══════════════════════════════════════════════════════════════
# FIG S2: Waterfall Chart — Growth/Decline by Major Cluster
# ═══════════════════════════════════════════════════════════════

print('\n=== FIG S2: Waterfall ===')

agg['delta'] = agg['post'] - agg['pre']
agg = agg.sort_values('delta', ascending=True)

fig, ax = plt.subplots(figsize=(10, 7))
plt.rcParams.update({'font.family': 'serif', 'font.serif': ['Times New Roman', 'DejaVu Serif']})

bars = []
colors_list = []
for i, (_, row) in enumerate(agg.iterrows()):
    d = row['delta']
    color = '#C44E52' if d >= 0 else '#4C72B0'
    bars.append(ax.barh(i, d, color=color, alpha=0.85, edgecolor='white', linewidth=0.5))
    colors_list.append(color)
    
    # Annotate
    x_pos = d + (max(agg['delta'].abs()) * 0.02 if d >= 0 else -max(agg['delta'].abs()) * 0.02)
    ha = 'left' if d >= 0 else 'right'
    ax.text(d, i, f' {d:+.0f} ', ha=ha, va='center', fontsize=9, fontweight='bold',
            color=color)

ax.set_yticks(range(len(agg)))
ax.set_yticklabels(agg['MajorCluster'], fontsize=10)
ax.axvline(0, color='black', linewidth=0.8)
ax.set_xlabel('Δ Frequency (2025-26 mean \u2212 2022-24 mean)', fontsize=12)
ax.set_title('Research Focus Shift by Major Cluster\n(2022-2024 \u2192 2025-2026)', fontsize=14, fontweight='bold')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.tick_params(axis='y', length=0)

# Legend
red_patch = mpatches.Patch(color='#C44E52', label='Growth')
blue_patch = mpatches.Patch(color='#4C72B0', label='Decline')
ax.legend(handles=[red_patch, blue_patch], loc='lower right', fontsize=10)

plt.tight_layout()
fig.savefig(os.path.join(OUTDIR, 'figS2_waterfall.png'), dpi=600, bbox_inches='tight', facecolor='white')
fig.savefig(os.path.join(OUTDIR, 'figS2_waterfall.pdf'), bbox_inches='tight', facecolor='white')
print('Saved: figS2_waterfall.png / .pdf')
plt.close()

print('\n=== ALL DONE ===')
