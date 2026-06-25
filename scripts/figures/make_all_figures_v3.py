#!/usr/bin/env python3
"""Generate all remaining figures v3: clinical strip, treemap, waterfall."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np
import squarify
import os

OUTDIR = r'D:\term\figures'
os.makedirs(OUTDIR, exist_ok=True)

plt.rcParams.update({'font.family': 'serif', 'font.serif': ['Times New Roman', 'DejaVu Serif'],
                     'font.size': 10, 'axes.titlesize': 14, 'axes.labelsize': 12})

# ═══════════════════════════════════════════════════════════════
# FIG 3b: Clinical-layer Rising Signal Strip Chart
# ═══════════════════════════════════════════════════════════════

print('\n=== FIG 3b: Clinical Rising Signals ===')

burst = pd.read_csv(r'D:\term\data\processed\burst-terms-full.csv')
clin = burst[burst['Category'].isin(['clinical', 'both'])].copy()
rising = clin[clin['2026'] > clin['2025']].copy()

exclude = ['protein level', 'expression level', 'immunofluorescence staining',
           'western blotting', 'p value', 'statistical significance',
           'noninvasive neuromodulation technique']
rising = rising[~rising['TERM'].str.lower().isin([e.lower() for e in exclude])]

rising = rising.nlargest(15, 'Total_2025_2026')
rising = rising.sort_values('Total_2025_2026', ascending=True)
N = len(rising)

for _, r in rising.iterrows():
    print(f"  {r['TERM']:50s} 2025={int(r['2025'])} 2026={int(r['2026'])}")

GRAY = '#E5E3E0'
RED = {1: '#F2C4C0', 2: '#E89088', 3: '#D05048', 4: '#A82028', 5: '#801018'}

def cf(f):
    if f <= 0: return GRAY
    if f >= 5: return RED[5]
    return RED.get(int(f), RED[1])

def tc(f):
    return 'white' if f >= 3 else '#333'

fig, ax = plt.subplots(figsize=(6.5, max(3.8, N * 0.36)))
bar_h, gap = 0.62, 0.06

for i, (_, row) in enumerate(rising.iterrows()):
    y = i
    f25, f26 = int(row['2025']), int(row['2026'])
    rect25 = mpatches.FancyBboxPatch((0, y - bar_h/2), 1.0, bar_h,
        boxstyle='round,pad=0.012', facecolor=cf(f25), edgecolor='none')
    ax.add_patch(rect25)
    x26 = 1.0 + gap
    rect26 = mpatches.FancyBboxPatch((x26, y - bar_h/2), 1.0, bar_h,
        boxstyle='round,pad=0.012', facecolor=cf(f26), edgecolor='none')
    ax.add_patch(rect26)
    if f25 > 0:
        ax.text(0.5, y, str(f25), ha='center', va='center', fontsize=8.5, fontweight='bold', color=tc(f25))
    if f26 > 0:
        ax.text(x26 + 0.5, y, str(f26), ha='center', va='center', fontsize=8.5, fontweight='bold', color=tc(f26))

ax.set_yticks(range(N))
ax.set_yticklabels(rising['TERM'].tolist(), fontsize=9, va='center')
ax.set_ylim(-0.7, N - 0.3)
ax.set_xlim(-0.05, 2.0 + gap + 0.05)
ax.set_xticks([0.5, 1.0 + gap + 0.5])
ax.set_xticklabels(['2025', '2026'], fontsize=12, fontweight='bold')
for spine in ax.spines.values(): spine.set_visible(False)
ax.tick_params(axis='both', length=0)

legend_patches = [mpatches.Patch(color=GRAY, label='0')]
for v, c in RED.items():
    legend_patches.append(mpatches.Patch(color=c, label=f'{v}' if v < 5 else '5+'))
ax.legend(handles=legend_patches, title='Frequency', loc='upper left',
          bbox_to_anchor=(1.01, 1.0), frameon=True, framealpha=0.9, edgecolor='#CCC',
          fontsize=9, title_fontsize=10, ncol=1, borderpad=0.6, handleheight=1.2, handlelength=1.5)
ax.set_title('Rising New Signals in Clinical Literature\n(2025\u2009\u2192\u20092026)', fontsize=14, fontweight='bold', pad=12)
plt.tight_layout(pad=0.8)
fig.savefig(os.path.join(OUTDIR, 'fig3b_clinical_rising.png'), dpi=600, bbox_inches='tight', facecolor='white')
fig.savefig(os.path.join(OUTDIR, 'fig3b_clinical_rising.pdf'), bbox_inches='tight', facecolor='white')
print('Saved: fig3b_clinical_rising.png / .pdf')
plt.close()

# ═══════════════════════════════════════════════════════════════
# Load & prepare data
# ═══════════════════════════════════════════════════════════════

print('\n=== Loading clustered data ===')
terms = pd.read_csv(r'D:\term\data\clustering\terms-clustered.csv')

MAJOR_MAP = {
    -1: 'Noise', 0: 'Psychiatric & Emotional Disorders', 1: 'Sleep Disorders',
    2: 'Clinical Trial Methodology', 3: 'Animal Models', 4: 'Cognitive Function',
    5: 'Autonomic & Cardiovascular', 6: 'Neuroimaging', 7: 'Stroke & Brain Injury',
    8: 'Autonomic & Cardiovascular', 9: 'VNS Core Terms',
    10: 'Stimulation Parameters & Devices', 11: 'Inflammation & Immunity',
    12: 'Psychiatric & Emotional Disorders', 13: 'Perioperative & Surgical',
    14: 'Perioperative & Surgical', 15: 'Inflammation & Immunity',
    16: 'Psychiatric & Emotional Disorders', 17: 'Brain Regions & Circuits',
}
terms['MajorNameEN'] = terms['MajorCluster'].map(MAJOR_MAP)

# Clean minor names: extract English part after ': '
def clean_minor_name(name):
    if not isinstance(name, str): return str(name)
    if ': ' in name:
        return name.split(': ', 1)[1]
    return name

terms['MinorNameClean'] = terms['MinorName'].apply(clean_minor_name)

terms_clean = terms[~terms['MajorNameEN'].isin(['Noise', 'Brain Regions & Circuits'])]
terms_clean = terms_clean[terms_clean['MajorNameEN'].notna()]

# Aggregation for waterfall
terms_clean['pre'] = terms_clean[['2022','2023','2024']].sum(axis=1)
terms_clean['post'] = terms_clean[['2025','2026']].sum(axis=1)

agg = terms_clean.groupby('MajorNameEN').agg(
    pre=('pre', 'sum'), post=('post', 'sum'), n_terms=('TERM', 'count')
).reset_index()
agg['delta'] = agg['post'] - agg['pre']
agg = agg.sort_values('delta', ascending=True)
print(agg.to_string())

# ═══════════════════════════════════════════════════════════════
# FIG 4: Horizon Chart — 12 clusters × 25 years
# ═══════════════════════════════════════════════════════════════

print('\n=== FIG 4: Horizon Chart ===')

# Build yearly sums per major cluster
years = [str(y) for y in range(2002, 2027)]
yearly = terms_clean.groupby('MajorNameEN')[years].sum()

# Sort clusters by total size
yearly['total'] = yearly.sum(axis=1)
yearly = yearly.sort_values('total', ascending=False)
clusters = yearly.index.tolist()
yearly = yearly.drop(columns=['total'])

fig, axes = plt.subplots(len(clusters), 1, figsize=(18, 1.8 * len(clusters)), sharex=True)

# Banded color scheme per cluster
from distinctipy import distinctipy as dp
colors_rgb = dp.get_colors(len(clusters))
cluster_colors = {c: colors_rgb[i] for i, c in enumerate(clusters)}

for i, cluster in enumerate(clusters):
    ax = axes[i]
    vals = yearly.loc[cluster].values.astype(float)
    
    # Normalize per cluster for horizon bands
    vmax = vals.max()
    if vmax == 0: vmax = 1
    
    n_bands = 5
    for band in range(n_bands):
        lo = band * vmax / n_bands
        hi = (band + 1) * vmax / n_bands
        band_vals = np.clip(vals, lo, hi) - lo
        alpha = 0.3 + 0.7 * (band + 1) / n_bands
        ax.fill_between(range(len(vals)), 0, band_vals, 
                        color=cluster_colors[cluster], alpha=alpha, linewidth=0)
    
    ax.set_ylim(0, vmax * 1.05)
    ax.set_yticks([])
    ax.set_ylabel(cluster, fontsize=9, rotation=0, ha='right', va='center',
                  labelpad=10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.tick_params(axis='x', length=0)

# X-axis labels every 4 years
axes[-1].set_xticks(range(0, 25, 4))
axes[-1].set_xticklabels([str(y) for y in range(2002, 2027, 4)], fontsize=10)
axes[-1].spines['bottom'].set_visible(True)

fig.suptitle('Research Theme Evolution Across Major Clusters (2002\u20132026)', 
             fontsize=16, fontweight='bold', y=1.01)
plt.tight_layout()
fig.savefig(os.path.join(OUTDIR, 'fig4_horizon.png'), dpi=600, bbox_inches='tight', facecolor='white')
fig.savefig(os.path.join(OUTDIR, 'fig4_horizon.pdf'), bbox_inches='tight', facecolor='white')
print('Saved: fig4_horizon.png / .pdf')
plt.close()

# ═══════════════════════════════════════════════════════════════
# FIG S1: Treemap — Major→Minor hierarchy
# ═══════════════════════════════════════════════════════════════

print('\n=== FIG S1: Treemap ===')

hier = terms_clean.dropna(subset=['MinorNameClean'])
td = hier.groupby(['MajorNameEN', 'MinorNameClean']).size().reset_index(name='count')
td = td[td['count'] >= 10]  # filter tiny groups for readability
td = td.sort_values('count', ascending=False)

print(f'Treemap groups: {len(td)}')
for _, r in td.head(20).iterrows():
    print(f"  {r['MajorNameEN']:40s} | {r['MinorNameClean']:40s} | {r['count']}")

majors = td['MajorNameEN'].unique()
colors_list = dp.get_colors(len(majors))
color_map = {m: colors_list[i] for i, m in enumerate(majors)}

fig, ax = plt.subplots(figsize=(20, 12))
rect_colors = [color_map[m] for m in td['MajorNameEN']]

# Truncate long labels for display
short_labels = []
for n in td['MinorNameClean']:
    if len(str(n)) > 35:
        short_labels.append(str(n)[:32] + '...')
    else:
        short_labels.append(str(n))

squarify.plot(sizes=td['count'], label=short_labels,
              color=rect_colors, alpha=0.82, ax=ax,
              text_kwargs={'fontsize': 6.5, 'color': '#222', 'wrap': True})

ax.set_title('Term Classification Hierarchy: Major \u2192 Minor Clusters', fontsize=16, fontweight='bold', pad=14)
ax.axis('off')

patches = [mpatches.Patch(color=color_map[m], 
                          label=f'{m} ({int(td[td["MajorNameEN"]==m]["count"].sum())})')
           for m in majors]
ax.legend(handles=patches, loc='upper right', bbox_to_anchor=(1.16, 1.0),
          fontsize=7.5, title='Major Clusters', title_fontsize=9, ncol=1)
plt.tight_layout()
fig.savefig(os.path.join(OUTDIR, 'figS1_treemap.png'), dpi=600, bbox_inches='tight', facecolor='white')
fig.savefig(os.path.join(OUTDIR, 'figS1_treemap.pdf'), bbox_inches='tight', facecolor='white')
print('Saved: figS1_treemap.png / .pdf')
plt.close()

# ═══════════════════════════════════════════════════════════════
# FIG S2: Waterfall
# ═══════════════════════════════════════════════════════════════

print('\n=== FIG S2: Waterfall ===')

agg_wf = agg.sort_values('delta', ascending=True)

fig, ax = plt.subplots(figsize=(11, 7.5))

for i, (_, row) in enumerate(agg_wf.iterrows()):
    d = row['delta']
    color = '#C44E52' if d >= 0 else '#4C72B0'
    ax.barh(i, d, color=color, alpha=0.85, edgecolor='white', linewidth=0.5)
    x_off = max(agg_wf['delta'].abs()) * 0.015
    ha = 'left' if d >= 0 else 'right'
    ax.text(d + (x_off if d >= 0 else -x_off), i, f' {d:+.0f}', ha=ha, va='center',
            fontsize=10, fontweight='bold', color=color)

ax.set_yticks(range(len(agg_wf)))
ax.set_yticklabels(agg_wf['MajorNameEN'], fontsize=10.5)
ax.axvline(0, color='black', linewidth=0.8)
ax.set_xlabel('\u0394 Frequency (2025-26 sum \u2212 2022-24 sum)', fontsize=13)
ax.set_title('Research Focus Shift by Major Cluster\n(2022\u20132024 \u2192 2025\u20132026)', fontsize=15, fontweight='bold', pad=14)
for spine in ['top', 'right']: ax.spines[spine].set_visible(False)
ax.tick_params(axis='y', length=0)
ax.legend(handles=[mpatches.Patch(color='#C44E52', label='Growth'),
                    mpatches.Patch(color='#4C72B0', label='Decline')],
          loc='lower right', fontsize=10)
plt.tight_layout()
fig.savefig(os.path.join(OUTDIR, 'figS2_waterfall.png'), dpi=600, bbox_inches='tight', facecolor='white')
fig.savefig(os.path.join(OUTDIR, 'figS2_waterfall.pdf'), bbox_inches='tight', facecolor='white')
print('Saved: figS2_waterfall.png / .pdf')
plt.close()

print('\n=== ALL DONE ===')
