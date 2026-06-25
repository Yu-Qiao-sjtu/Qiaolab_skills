"""Fig Y: Parallel Coordinates — Basic High-Entropy Terms × 25 Years
Dark lines = high entropy (foundation terms), light = low entropy (burst terms)
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from matplotlib.colorbar import Colorbar

# ── Load ──────────────────────────────────────────────────
df = pd.read_csv("data/clustering/terms-clustered.csv")

yr_cols = [str(y) for y in range(2002, 2027)]
years = list(range(2002, 2027))

# Filter: basic research only, entropy > 0, some annual presence
df["Total"] = df[yr_cols].sum(axis=1)
mask = (df["Category"] == "basic") & (df["Entropy"] > 0) & (df["Total"] >= 3)
base = df[mask].copy()

# Build matrix: terms × years
mat = base[yr_cols].values.astype(float)

# ── Normalize: each term's peak = 1 ───────────────────────
row_max = mat.max(axis=1, keepdims=True)
row_max[row_max == 0] = 1  # avoid div by zero
mat_norm = mat / row_max

# ── Select terms to plot ──────────────────────────────────
# Take top N by entropy, but ensure diversity
# Reset index so positional indexing works
base_r = base.reset_index(drop=True)
# Recompute mat + mat_norm on base_r
mat_r = base_r[yr_cols].values.astype(float)
row_max_r = mat_r.max(axis=1, keepdims=True)
row_max_r[row_max_r == 0] = 1
mat_norm_r = mat_r / row_max_r

top_n = 60
top_terms = base_r.nlargest(top_n, "Entropy")
top_positions = top_terms.index  # now 0..n-1
mat_top = mat_norm_r[top_positions]
entropies = top_terms["Entropy"].values

# ── Plot ──────────────────────────────────────────────────
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 11,
})

fig, ax = plt.subplots(figsize=(16, 10))
fig.patch.set_facecolor("white")
ax.set_facecolor("#FCFCFC")

# Colormap: light gray (low entropy) → dark blue (high entropy)
norm = Normalize(vmin=entropies.min(), vmax=entropies.max())
cmap = plt.cm.viridis

# Draw each line
for i in range(len(top_terms)):
    y_vals = mat_top[i]
    color = cmap(norm(entropies[i]))
    alpha = 0.15 + 0.85 * (entropies[i] - entropies.min()) / (entropies.max() - entropies.min())
    lw = 0.8 + 2.5 * (entropies[i] - entropies.min()) / (entropies.max() - entropies.min())
    ax.plot(years, y_vals, color=color, alpha=alpha, linewidth=lw, zorder=2)

# ── Highlight top 8 terms ─────────────────────────────────
top8 = top_terms.head(8)
for _, row in top8.iterrows():
    pos = row.name  # positional index in base_r
    y_vals = mat_norm_r[pos]
    ax.plot(years, y_vals, color="#D41159", linewidth=2.2, alpha=0.95, zorder=5)
    # Label at last year
    ax.annotate(
        row["TERM"],
        (2026.1, y_vals[-1]),
        fontsize=8.5, fontweight="bold", color="#D41159",
        va="center", zorder=10,
    )

# ── Labels ────────────────────────────────────────────────
ax.set_xlabel("Year", fontweight="bold", fontsize=17)
ax.set_ylabel("Normalized Frequency (peak = 1.0)", fontweight="bold", fontsize=17)
ax.set_title("Basic Research: Temporal Profiles of High-Entropy Foundation Terms", fontweight="bold", fontsize=20, pad=18)

ax.set_xlim(2001.5, 2027.5)
ax.set_ylim(-0.05, 1.15)
ax.set_xticks(years)
ax.set_xticklabels([str(y) for y in years], rotation=45, ha="right", fontsize=10)

# ── Colorbar ──────────────────────────────────────────────
sm = ScalarMappable(norm=norm, cmap=cmap)
cbar = fig.colorbar(sm, ax=ax, shrink=0.6, aspect=30, pad=0.015)
cbar.set_label("Entropy (bits)", fontsize=13, fontweight="bold")
cbar.ax.tick_params(labelsize=11)

# Annotation
ax.text(0.985, 0.08,
        "Magenta highlights = highest-entropy foundation terms\n"
        "Dark lines = high entropy (persistent across decades)\n"
        "Light lines = low entropy (concentrated in few years)",
        transform=ax.transAxes, fontsize=9, fontstyle="italic", color="#555555",
        ha="right", va="bottom",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="#DDDDDD", alpha=0.85))

ax.grid(True, alpha=0.15, axis="y", linestyle="--")

plt.tight_layout()
for fmt, dpi in [("png", 1200), ("pdf", None)]:
    path = f"figures/fig_parallel_coords.{fmt}"
    plt.savefig(path, dpi=dpi, bbox_inches="tight", facecolor="white", edgecolor="none")
    print(f"Saved: {path}")
plt.close()
print("Done: Parallel Coordinates")
