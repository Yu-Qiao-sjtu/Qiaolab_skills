import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

plt.rcParams['font.family'] = 'DejaVu Sans'

# ── Data: 15 rising signals ──
data = [
    ("synaptic plasticity",                    1, 2),
    ("gadd45 beta",                            0, 2),
    ("hearing thresholds",                     0, 2),
    ("computational modeling",                 0, 2),
    ("macrophage polarization",                0, 2),
    ("noise exposure",                         0, 2),
    ("oligodendrocyte precursor cells",        0, 2),
    ("parasympathetic reactivation",            0, 2),
    ("physical exercise",                      0, 2),
    ("promising neuromodulatory approach",     0, 2),
    ("fNIRS",                                  1, 2),
    ("auricular concha",                       0, 3),
    ("entorhinal cortex",                      0, 3),
    ("brain-derived neurotrophic factor",      1, 3),
    ("mediation analysis",                     0, 4),
]

data.sort(key=lambda x: x[1] + x[2])
labels = [d[0] for d in data]
vals_2025 = [d[1] for d in data]
vals_2026 = [d[2] for d in data]
n = len(labels)

# ── Generous layout ──
fig, ax = plt.subplots(figsize=(14, 9))
# Wide left margin to fit the longest label
fig.subplots_adjust(left=0.38, right=0.90, top=0.90, bottom=0.06)

row_h = 0.40
strip_h = 0.32
strip_w = 2.0
gap = 0.28

x25 = 0.0
x26 = strip_w + gap

gray = '#E5E3E0'
red25 = '#E8A090'
red26 = '#C0503C'

for i in range(n):
    y = i * row_h
    yc = y + strip_h / 2

    # 2025
    fc25 = gray if vals_2025[i] == 0 else red25
    ax.add_patch(FancyBboxPatch((x25, y), strip_w, strip_h,
        boxstyle="round,pad=0.04", linewidth=0, facecolor=fc25, clip_on=False))

    # 2026
    fc26 = gray if vals_2026[i] == 0 else red26
    ax.add_patch(FancyBboxPatch((x26, y), strip_w, strip_h,
        boxstyle="round,pad=0.04", linewidth=0, facecolor=fc26, clip_on=False))

    # Value text
    for xl, v in [(x25, vals_2025[i]), (x26, vals_2026[i])]:
        if v > 0:
            ax.text(xl + strip_w / 2, yc, str(v),
                    ha='center', va='center', fontsize=12, fontweight='bold',
                    color='white' if v >= 3 else '#6B2020', clip_on=False)

    # Label — right-aligned sharply at x = -0.15
    ax.text(-0.15, yc, labels[i], ha='right', va='center',
            fontsize=13, color='#1A1A1A', clip_on=False)

# Column headers
ytop = (n - 1) * row_h + strip_h + 0.25
ax.text(x25 + strip_w / 2, ytop, '2025', ha='center', va='bottom',
        fontsize=15, fontweight='bold', color='#555', clip_on=False)
ax.text(x26 + strip_w / 2, ytop, '2026', ha='center', va='bottom',
        fontsize=15, fontweight='bold', color='#555', clip_on=False)

# Legend
ly = -0.65
ax.add_patch(FancyBboxPatch((0, ly), 0.45, 0.28, boxstyle="round,pad=0.02",
    linewidth=0, facecolor=gray, clip_on=False))
ax.text(0.60, ly + 0.14, 'Absent  (0)', va='center', fontsize=10, color='#888', clip_on=False)
ax.add_patch(FancyBboxPatch((2.5, ly), 0.45, 0.28, boxstyle="round,pad=0.02",
    linewidth=0, facecolor=red26, clip_on=False))
ax.text(3.10, ly + 0.14, 'Present  (1+)', va='center', fontsize=10, color='#888', clip_on=False)

# Titles
ty = ytop + 0.65
cx = (x25 + x26 + strip_w) / 2
ax.text(cx, ty, 'Rising Signals in Basic Mechanism Research (2025\u20132026)',
        ha='center', va='bottom', fontsize=16, fontweight='bold', color='#1A1A1A', clip_on=False)
ax.text(cx, ty - 0.38,
        'Terms absent during 2022\u20132024, emerging in 2025 and growing in 2026',
        ha='center', va='top', fontsize=11, fontstyle='italic', color='#999', clip_on=False)

# Bounds — generous left room so labels never clip
ax.set_xlim(-8, x26 + strip_w + 0.5)   # 8 data-units of label space
ax.set_ylim(ly - 0.5, ty + 0.6)
ax.axis('off')

fig.savefig(r'D:\term\figure_rising_strips.png', dpi=600, bbox_inches='tight',
            facecolor='white', edgecolor='none')
fig.savefig(r'D:\term\figure_rising_strips.pdf', bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close(fig)

print("OK")
