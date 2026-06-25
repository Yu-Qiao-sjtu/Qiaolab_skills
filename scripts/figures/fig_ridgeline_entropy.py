"""
Fig X: Ridgeline plot — entropy distribution of basic-research terms across 12 themes.
Uses MajorCluster to index themes, bypassing garbled Chinese column.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d
import warnings
warnings.filterwarnings("ignore")

# ── Load ─────────────────────────────────────────────────────────
df = pd.read_csv("data/clustering/terms-clustered.csv", encoding="utf-8")

# Map MajorCluster → English theme name
# (derived from major_clusters_summary.csv inspection)
cluster_to_theme = {
    -1: "EXCLUDE",      # noise / 噪声点
    0:  "Psychiatric & Emotional Disorders",
    1:  "Sleep Disorders",
    2:  "Clinical Trial Methodology",
    3:  "Animal Models",
    4:  "Cognitive Function",
    5:  "Autonomic & Cardiovascular",
    6:  "Neuroimaging",
    7:  "Psychiatric & Emotional Disorders",  # duplicate
    8:  "Autonomic & Cardiovascular",         # duplicate
    9:  "VNS Core Terms",
    10: "Stimulation Parameters & Devices",
    11: "Inflammation & Immunity",
    12: "Psychiatric & Emotional Disorders",  # duplicate
    13: "Perioperative & Surgical",
    14: "Perioperative & Surgical",           # duplicate
    15: "Inflammation & Immunity",            # duplicate
    16: "Psychiatric & Emotional Disorders",  # duplicate
    17: "EXCLUDE",     # Brain Regions & Circuits
}
df["Theme"] = df["MajorCluster"].map(cluster_to_theme)

# Filter: basic research only, entropy > 0, exclude trash
basic = df[(df["Category"] == "basic") & (df["Entropy"] > 0) & (df["Theme"] != "EXCLUDE")].copy()

# Theme order by count
theme_counts = basic.groupby("Theme").size().sort_values(ascending=False)
themes = list(theme_counts.index)
n_themes = len(themes)

print(f"Basic terms with entropy>0: {len(basic)}")
for t in themes:
    vals = basic[basic["Theme"] == t]["Entropy"]
    print(f"  {t}: n={len(vals)}, median={vals.median():.3f}, max={vals.max():.3f}")

# ── Colors ───────────────────────────────────────────────────────
from distinctipy import get_colors
colors = get_colors(n_themes, pastel_factor=0.3)
theme_color = dict(zip(themes, colors))

# ── Plot ─────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(22, 16), dpi=1200)
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

entropy_max = np.ceil(basic["Entropy"].max() * 10) / 10 + 0.1
n_bins = 80
bins = np.linspace(0, entropy_max, n_bins + 1)
bin_centers = (bins[:-1] + bins[1:]) / 2
x_smooth = np.linspace(0, entropy_max, 300)
overlap = 1.6
sigma = 1.0

for i, theme in enumerate(themes):
    vals = basic[basic["Theme"] == theme]["Entropy"].dropna().values
    n = len(vals)
    if n < 3:
        continue

    hist, _ = np.histogram(vals, bins=bins)
    hist = hist.astype(float)
    hist_smooth = gaussian_filter1d(hist, sigma=sigma)
    hist_smooth = np.interp(x_smooth, bin_centers, hist_smooth)
    hist_smooth = hist_smooth / max(hist_smooth.max(), 1e-9)

    base_y = i * overlap
    color = theme_color[theme]

    ax.fill_between(x_smooth, base_y, base_y + hist_smooth,
                    color=color, alpha=0.78, linewidth=0.3, edgecolor="white")

    # Median diamond
    median_val = np.median(vals)
    idx = np.argmin(np.abs(x_smooth - median_val))
    med_y = base_y + hist_smooth[idx]
    ax.plot(median_val, med_y, marker="D", color="white", markersize=9,
            markeredgecolor="#333333", markeredgewidth=0.8, zorder=10)

    # Right-side label
    ax.text(entropy_max + 0.15, base_y + 0.36, theme,
            fontsize=18, fontweight="bold", color=color, va="center",
            ha="left", fontfamily="Times New Roman")
    ax.text(entropy_max + 0.15, base_y + 0.04, f"n={n}",
            fontsize=13, color="#888888", va="center",
            ha="left", fontfamily="Times New Roman")

ax.set_ylim(-0.5, (n_themes - 1) * overlap + 1.5)
ax.set_xlim(-0.1, entropy_max + 6.5)

ax.set_xlabel("Entropy (bits)", fontsize=24, fontweight="bold", fontfamily="Times New Roman")
ax.tick_params(axis="x", labelsize=16)
ax.set_xticks([0, 1, 2, 3])

ax.set_yticks([])
for spine in ["top", "right", "left"]:
    ax.spines[spine].set_visible(False)

ax.set_title("Entropy Distribution of Basic Research Terms Across Themes",
             fontsize=26, fontweight="bold", fontfamily="Times New Roman", pad=22)

fig.text(0.915, 0.94, "◆ = median entropy", fontsize=14, fontfamily="Times New Roman",
         ha="right", va="top", color="grey")

plt.tight_layout(pad=1.5)
fig.savefig("figures/fig_ridgeline_basic_entropy.png", dpi=1200, bbox_inches="tight", facecolor="white")
fig.savefig("figures/fig_ridgeline_basic_entropy.pdf", bbox_inches="tight", facecolor="white")
print("Saved: figures/fig_ridgeline_basic_entropy.png + .pdf")
