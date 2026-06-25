"""Fig X: Connected Scatter — Basic Research High-Entropy Terms
Gapminder-style: X=Total frequency, Y=Entropy, Bubble=2025-26 activity, Color=MajorCluster
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

# ── Load ──────────────────────────────────────────────────
df = pd.read_csv("data/clustering/terms-clustered.csv")

yr_cols = [str(y) for y in range(2002, 2027)]

# Filter: basic research only, entropy > 0, at least some presence
df["Total"] = df[yr_cols].sum(axis=1)
mask = (
    (df["Category"] == "basic")
    & (df["Entropy"] > 0)
    & (df["Total"] >= 3)
)
base = df[mask].copy()

# 2025-2026 activity
base["recent"] = base["2025"] + base["2026"]

# ── Cluster mapping ──────────────────────────────────────
# Keep only meaningful clusters, group small ones
cluster_counts = base.groupby("MajorCluster").size()
big_clusters = cluster_counts[cluster_counts >= 5].index.tolist()
base["plot_cluster"] = base["MajorCluster"].where(base["MajorCluster"].isin(big_clusters), "Other")

# Color palette — distinctipy-inspired
cluster_colors = {
    "Inflammation & Immunity": "#E41A1C",
    "Stimulation Parameters & Devices": "#377EB8",
    "Autonomic & Cardiovascular": "#4DAF4A",
    "VNS Core Terms": "#984EA3",
    "Psychiatric & Emotional Disorders": "#FF7F00",
    "Clinical Trial Methodology": "#A65628",
    "Perioperative & Surgical": "#F781BF",
    "Stroke & Brain Injury": "#999999",
    "Animal Models": "#66C2A5",
    "Cognitive Function": "#FC8D62",
    "Neuroimaging": "#8DA0CB",
    "Sleep Disorders": "#E78AC3",
    "Brain Regions & Circuits": "#A6D854",
    "Noise": "#B3B3B3",
    "Other": "#CCCCCC",
}

# ── Plot ──────────────────────────────────────────────────
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 10,
    "axes.labelsize": 14,
    "axes.titlesize": 18,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
})

fig, ax = plt.subplots(figsize=(12, 9))
fig.patch.set_facecolor("white")
ax.set_facecolor("#FAFAFA")

# Size mapping: recent activity → bubble size
min_sz, max_sz = 15, 300
if base["recent"].max() > base["recent"].min():
    sizes = min_sz + (max_sz - min_sz) * (base["recent"] - base["recent"].min()) / (base["recent"].max() - base["recent"].min())
else:
    sizes = np.full(len(base), 80)

# Plot clusters in order of size
plot_order = base.groupby("plot_cluster").size().sort_values(ascending=False).index
handles = []
for cl in plot_order:
    sub = base[base["plot_cluster"] == cl]
    color = cluster_colors.get(cl, "#999999")
    ax.scatter(
        sub["Total"], sub["Entropy"],
        s=sizes[sub.index],
        c=color, alpha=0.55, edgecolors="white", linewidth=0.4,
        zorder=2,
    )
    handles.append(mpatches.Patch(color=color, alpha=0.7, label=f"{cl} (n={len(sub)})"))

# ── Annotate high-entropy / high-total terms ──────────────
# Select terms to label: top entropy AND decent total
label_candidates = base[(base["Entropy"] >= 2.0) & (base["Total"] >= 5)].copy()
# Add a few high-entropy terms even with lower total
extra = base[(base["Entropy"] >= 2.5) & (base["Total"] < 5)]
label_candidates = pd.concat([label_candidates, extra]).drop_duplicates()

labeled = set()
for _, row in label_candidates.iterrows():
    term = row["TERM"]
    if term in labeled:
        continue
    labeled.add(term)
    offset = 0.12
    ax.annotate(
        term,
        (row["Total"], row["Entropy"]),
        xytext=(row["Total"] + offset, row["Entropy"] + offset * 0.3),
        fontsize=7.5, fontstyle="italic", color="#333333",
        arrowprops=dict(arrowstyle="-", color="#AAAAAA", lw=0.5),
        zorder=10,
    )

# ── Labels ────────────────────────────────────────────────
ax.set_xlabel("Total Frequency (2002–2026)", fontweight="bold", fontsize=16)
ax.set_ylabel("Entropy (bits)", fontweight="bold", fontsize=16)
ax.set_title("Basic Research: Term Impact vs. Persistence", fontweight="bold", fontsize=20, pad=18)

# ── Quadrant annotations ──────────────────────────────────
x_mid = base["Total"].median()
y_mid = base["Entropy"].median()
quadrant_style = dict(fontsize=10, fontstyle="italic", color="#888888", ha="center", va="center")
ax.text(base["Total"].max() * 0.85, base["Entropy"].max() * 0.88, "HIGH IMPACT\nHIGH PERSISTENCE\nFoundation terms", **quadrant_style)
ax.text(base["Total"].max() * 0.85, base["Entropy"].min() * 1.5, "HIGH IMPACT\nLOW PERSISTENCE\nBurst terms", **quadrant_style)
ax.text(base["Total"].min() * 2, base["Entropy"].max() * 0.88, "NICHE\nHIGH PERSISTENCE\nEnduring niche", **quadrant_style)
ax.text(base["Total"].min() * 2, base["Entropy"].min() * 1.5, "LOW IMPACT\nLOW PERSISTENCE\nTransient", **quadrant_style)

# ── Legend ────────────────────────────────────────────────
leg = ax.legend(
    handles=handles, loc="upper left", frameon=True,
    fontsize=9, title="Research Domain", title_fontsize=10,
    ncol=1, handlelength=1.5, handleheight=1.2,
)
leg.get_frame().set_alpha(0.85)

# Bubble size legend
for sz, label in [(50, "1"), (120, "5"), (250, "10+")]:
    ax.scatter([], [], s=sz, c="#666666", alpha=0.35, edgecolors="white", linewidth=0.3,
               label=f"2025-26 freq: {label}")
# Instead add a small annotation
ax.text(base["Total"].max() * 0.15, base["Entropy"].max() * 0.08,
        "Bubble size = 2025–2026 activity",
        fontsize=9, fontstyle="italic", color="#666666", ha="center")

ax.grid(True, alpha=0.2, linestyle="--")
ax.set_xlim(left=-0.5)
ax.set_ylim(bottom=-0.05, top=base["Entropy"].max() + 0.3)

plt.tight_layout()
for fmt, dpi in [("png", 1200), ("pdf", None)]:
    path = f"figures/fig_connected_scatter.{fmt}"
    plt.savefig(path, dpi=dpi, bbox_inches="tight", facecolor="white", edgecolor="none")
    print(f"Saved: {path}")
plt.close()
print("Done: Connected Scatter")
