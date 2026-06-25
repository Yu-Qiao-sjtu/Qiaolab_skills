import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['mathtext.fontset'] = 'custom'
plt.rcParams['mathtext.default'] = 'regular'
import numpy as np

df = pd.read_csv('terms-clustered.csv')
print(f'Total terms: {len(df)}')

# Map Chinese MajorName to English abbreviations for filtering
name_map = {
    '脑区与回路': 'Brain',
    '噪声': 'Noise',
    '炎症与免疫': 'Inflammation',
    '刺激参数与设备': 'StimParam',
    '精神疾病与情绪': 'Psychiatric',
    '围术期应用': 'Perioperative',
    '自主神经与心血管': 'Autonomic',
    '临床试验方法学': 'TrialMethod',
    '核心: vagus nerve, vagus nerve stimulation': 'VNSCore',
    '卒中与脑损伤': 'Stroke',
    '动物模型': 'AnimalModel',
    '认知功能': 'Cognitive',
    '神经影像': 'Neuroimaging',
    '睡眠障碍': 'Sleep',
}

# Show the actual MajorName values
print('MajorName values:')
for name, count in df['MajorName'].value_counts().items():
    print(f'  [{count:5d}] {repr(name)}')

# Filter for basic mechanism classes
basic_names = ['炎症与免疫', '自主神经与心血管', '卒中与脑损伤', '动物模型', '认知功能']
df_basic = df[df['MajorName'].isin(basic_names)].copy()
print(f'\nBasic mechanism terms: {len(df_basic)}')

# Filter: 2022, 2023, 2024 all zero, 2026 >= 2025
for col in ['2022', '2023', '2024', '2025', '2026']:
    df_basic[col] = df_basic[col].fillna(0).astype(int)

df_basic['sum_early'] = df_basic['2022'] + df_basic['2023'] + df_basic['2024']
df_basic['total_25_26'] = df_basic['2025'] + df_basic['2026']

# Rising: early = 0, 2026 STRICTLY > 2025, total > 0
burst = df_basic[(df_basic['sum_early'] == 0) &
                 (df_basic['2026'] > df_basic['2025']) &
                 (df_basic['total_25_26'] > 0)].copy()
burst = burst.sort_values(['2026', 'total_25_26'], ascending=False)

print(f'\nRising signals (2026 >= 2025, 2022-2024 = 0): {len(burst)}')
print()

for i, (idx, row) in enumerate(burst.head(15).iterrows()):
    print(f"  {i+1:2d}. {row['TERM']:50s} 2025={row['2025']} 2026={row['2026']} [{name_map.get(row['MajorName'], row['MajorName'][:20])}]")

# ---- Figure: CLEAN, NO CATEGORIES ----
top_n = min(10, len(burst))
top = burst.head(top_n).iloc[::-1]  # reverse for bottom-to-top

fig, ax = plt.subplots(figsize=(8.5, 5.0))
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

# Truncate long labels
def short_label(s, maxlen=42):
    if len(s) > maxlen:
        return s[:maxlen-3] + '...'
    return s

labels = [short_label(t) for t in top['TERM'].values]
y_pos = np.arange(len(labels))

# Simple two-color scheme, NO category colors
c25 = '#7f7f7f'   # medium gray for 2025
c26 = '#1a1a1a'   # near-black for 2026
ms = 110           # marker size

for i in range(len(top)):
    y = y_pos[i]
    f25 = top['2025'].iloc[i]
    f26 = top['2026'].iloc[i]

    # connecting line
    ax.plot([f25, f26], [y, y], color='#aaaaaa', linewidth=1.0, zorder=2)

    # 2025 - white open circle
    if f25 > 0:
        ax.scatter(f25, y, s=ms, facecolor='white', edgecolor=c25,
                   linewidth=1.3, zorder=3)
    else:
        ax.scatter(f25, y, s=ms*0.5, marker='D', facecolor='white',
                   edgecolor=c25, linewidth=1.0, zorder=3)

    # 2026 - filled dark circle
    ax.scatter(f26, y, s=ms, facecolor=c26, edgecolor='white',
               linewidth=0.6, zorder=4)

ax.set_yticks(y_pos)
ax.set_yticklabels(labels, fontsize=10.5)
ax.set_xlabel('Frequency in literature (2025\u20132026)', fontsize=11.5, labelpad=10)
ax.set_xlim(-0.5, max(top['2026'].max(), top['2025'].max()) + 1.2)

# Legend
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='white',
           markeredgecolor=c25, markersize=8, label='2025'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor=c26,
           markeredgecolor='white', markersize=8, label='2026'),
]
leg = ax.legend(handles=legend_elements, loc='lower right', frameon=True,
                framealpha=0.95, fontsize=10.5, edgecolor='#cccccc',
                title='Year', title_fontsize=10.5)
leg.get_title().set_fontweight('bold')

# Clean spines
for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
for spine in ['left', 'bottom']:
    ax.spines[spine].set_color('#cccccc')
    ax.spines[spine].set_linewidth(0.5)

ax.tick_params(axis='both', colors='#333333', length=0)
ax.grid(axis='x', color='#e8e8e8', linewidth=0.4, alpha=0.8)
ax.set_axisbelow(True)

ax.set_title('Rising new signals in basic mechanism research\n(terms appearing only in 2025\u20132026, 2026 > 2025)',
             fontsize=12, fontweight='bold', pad=14, color='#1a1a1a')

plt.tight_layout(pad=1.5)
fig.savefig('figure_rising_signals.png', dpi=600, bbox_inches='tight',
            facecolor='white', edgecolor='none')
fig.savefig('figure_rising_signals.pdf', bbox_inches='tight',
            facecolor='white', edgecolor='none')
print('\nSaved: figure_rising_signals.png / .pdf')
