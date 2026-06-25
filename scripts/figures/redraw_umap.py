"""
Re-draw UMAP visualization from existing terms-clustered.csv
Fixes: right-panel category mapping + larger labels with centroids.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.patches import Patch

matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial']
matplotlib.rcParams['axes.unicode_minus'] = False

print("Loading terms-clustered.csv ...")
df = pd.read_csv("D:/term/terms-clustered.csv")
print(f"  {len(df):,} rows")
print(f"  Categories: {df['Category'].unique()}")
print(f"  MajorNames: {df['MajorName'].nunique()}")

fig, axes = plt.subplots(1, 2, figsize=(28, 12))

# ====================================================================
# Left: Major clusters with centroid labels
# ====================================================================
ax = axes[0]
major_counts = df["MajorName"].value_counts()
top_majors = [m for m in major_counts.index if m != "噪声点"][:14]
df["PlotMajor"] = df["MajorName"].apply(lambda x: x if x in top_majors else "其他大类")

n_top = len(top_majors)
cmap = plt.cm.tab20
colors_major = [cmap(i / max(n_top, 20)) for i in range(n_top)]

for i, name in enumerate(top_majors):
    mask = df["PlotMajor"] == name
    ax.scatter(df.loc[mask, "UMAP_X"], df.loc[mask, "UMAP_Y"],
               s=1.2, alpha=0.55, color=colors_major[i],
               label=f"{name} ({major_counts.get(name, 0)})", rasterized=True)

    # Centroid label
    cx, cy = df.loc[mask, "UMAP_X"].mean(), df.loc[mask, "UMAP_Y"].mean()
    short_name = name if len(name) <= 12 else name[:10] + "…"
    ax.annotate(short_name, (cx, cy), fontsize=11, fontweight="bold",
                ha="center", va="center",
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                          edgecolor=colors_major[i], alpha=0.85))

# Other
mask_other = df["PlotMajor"] == "其他大类"
if mask_other.sum() > 0:
    ax.scatter(df.loc[mask_other, "UMAP_X"], df.loc[mask_other, "UMAP_Y"],
               s=0.5, alpha=0.15, color="gray",
               label=f"其他大类 ({mask_other.sum()})", rasterized=True)

ax.set_title(f"taVNS 术语 UMAP 投影 — 语义大类", fontsize=16, fontweight="bold")
ax.set_xlabel("UMAP-1", fontsize=12)
ax.set_ylabel("UMAP-2", fontsize=12)
ax.legend(loc="lower left", fontsize=10, markerscale=6, ncol=2,
          framealpha=0.85)

# ====================================================================
# Right: Basic vs Clinical split  (FIXED: use 'basic'/'clinical'/'both')
# ====================================================================
ax2 = axes[1]

cat_map = {
    "basic":    ("基础研究 (Basic)",       "#2196F3"),
    "clinical": ("临床 (Clinical)",       "#4CAF50"),
    "both":     ("交叉 (Both)",           "#FF9800"),
}

legend_elements = []
for cat_eng, (cat_label, color) in cat_map.items():
    mask = df["Category"] == cat_eng
    count = mask.sum()
    if count == 0:
        print(f"  WARNING: no rows for category '{cat_eng}'")
        continue
    print(f"  Plotting {cat_label}: {count:,} points")
    ax2.scatter(df.loc[mask, "UMAP_X"], df.loc[mask, "UMAP_Y"],
                s=1.2, alpha=0.35, color=color,
                label=f"{cat_label} ({count:,})", rasterized=True)
    legend_elements.append(Patch(facecolor=color,
                                 label=f"{cat_label} ({count:,})"))

# Centroid labels
for cat_eng, (cat_label, color) in cat_map.items():
    mask = df["Category"] == cat_eng
    if mask.sum() == 0:
        continue
    cx, cy = df.loc[mask, "UMAP_X"].mean(), df.loc[mask, "UMAP_Y"].mean()
    ax2.annotate(cat_label.split(" ")[0], (cx, cy), fontsize=14,
                 fontweight="bold", ha="center", va="center",
                 bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
                           edgecolor=color, alpha=0.9, linewidth=2))

ax2.set_title("taVNS 术语 UMAP 投影 — 基础研究 vs 临床", fontsize=16, fontweight="bold")
ax2.set_xlabel("UMAP-1", fontsize=12)
ax2.set_ylabel("UMAP-2", fontsize=12)
ax2.legend(handles=legend_elements, loc="lower left", fontsize=11,
           markerscale=6, framealpha=0.85)

plt.tight_layout(pad=2)
outpath = "D:/term/umap_clusters.png"
plt.savefig(outpath, dpi=200, bbox_inches="tight", facecolor="white")
plt.close()
print(f"\n✓ Saved: {outpath}")
print("✅ Done!")
