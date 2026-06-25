"""Plot UMAP with dashed convex hulls around each cluster (English labels)."""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import warnings
warnings.filterwarnings("ignore")

# ── Load ──────────────────────────────────────────────────
df = pd.read_csv("terms-clustered.csv")

# ── Map cluster IDs → English names ───────────────────────
name_map = {
    -1: "Noise",
     0: "Psychiatric & Emotional Disorders",
     1: "Sleep Disorders",
     2: "Clinical Trial Methodology",
     3: "Animal Models",
     4: "Cognitive Function",
     5: "Autonomic & Cardiovascular",
     6: "Neuroimaging",
     7: "Stroke & Brain Injury",
     8: "Autonomic & Cardiovascular",
     9: "VNS Core Terms",
    10: "Stimulation Parameters & Devices",
    11: "Inflammation & Immunity",
    12: "Psychiatric & Emotional Disorders",
    13: "Perioperative & Surgical",
    14: "Perioperative & Surgical",
    15: "Inflammation & Immunity",
    16: "Psychiatric & Emotional Disorders",
    17: "Brain Regions & Circuits",
}

df["EName"] = df["MajorCluster"].map(name_map).fillna("Other")

# ── Palette (distinct colors for unique names) ────────────
unique_names = sorted(set(name_map.values()))
palette_20 = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
    "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
    "#aec7e8", "#ffbb78", "#98df8a", "#ff9896", "#c5b0d5",
    "#c49c94", "#f7b6d2", "#c7c7c7", "#dbdb8d", "#9edae5",
]
color_map = {n: palette_20[i % len(palette_20)] for i, n in enumerate(unique_names)}
# Override noise to grey
color_map["Noise"] = "#d0d0d0"

# ── Plot ──────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(24, 20))
fig.patch.set_facecolor("white")
ax.set_facecolor("#f8f8fb")

# Plot noise first (behind everything, smallest dots)
noise_df = df[df["EName"] == "Noise"]
if len(noise_df) > 0:
    ax.scatter(
        noise_df["UMAP_X"], noise_df["UMAP_Y"],
        s=0.8, alpha=0.12, color="#cccccc",
        edgecolors="none", rasterized=True,
    )

# Plot each non-noise cluster
for name in [n for n in unique_names if n != "Noise"]:
    sub = df[df["EName"] == name]
    ax.scatter(
        sub["UMAP_X"], sub["UMAP_Y"],
        s=2.5, alpha=0.40, color=color_map[name],
        edgecolors="none", rasterized=True,
    )

# No convex hull outlines — clean scatter only

# ── Legend ────────────────────────────────────────────────
# One entry per unique English name, show combined count
handles = []
for name in unique_names:
    count = df[df["EName"] == name].shape[0]
    h = Line2D(
        [0], [0], marker="o", color="w", markerfacecolor=color_map[name],
        markersize=10, label=f"{name}  (n={count:,})",
    )
    handles.append(h)

legend = ax.legend(
    handles=handles, loc="lower left", fontsize=8.5,
    framealpha=0.92, ncol=2, markerscale=1.1,
    title="Clusters", title_fontsize=10,
    borderpad=0.6, labelspacing=0.4, handletextpad=0.5,
)
legend.get_frame().set_linewidth(0.4)

# ── Axis labels ───────────────────────────────────────────
ax.set_xlabel("UMAP-1", fontsize=16, weight="bold")
ax.set_ylabel("UMAP-2", fontsize=16, weight="bold")
ax.tick_params(labelsize=13)
ax.grid(True, alpha=0.12, linewidth=0.4)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
fig.savefig("umap_clusters.png", dpi=200, bbox_inches="tight")
print("Saved: umap_clusters.png (clean scatter, no hulls)")
