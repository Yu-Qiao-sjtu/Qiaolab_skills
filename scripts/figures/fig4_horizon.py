"""Fig 4: Horizon Chart — 12 major clusters × 25 years, compact small-multiples.
Each row is a major cluster; colour intensity = frequency; white band = baseline.
Font sizes: 24pt title, 16pt row labels, 15pt year ticks."""
import pandas as pd, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# ── Load ──
terms = pd.read_csv("data/clustering/terms-clustered.csv")

# Exclude by MajorName (Chinese labels for Brain Regions & Circuits, Noise)
exclude_names = ["脑区与回路", "噪声点"]
terms = terms[~terms["MajorName"].isin(exclude_names)]

year_cols = [str(y) for y in range(2002, 2027)]

# Aggregate by MajorName
clusters = terms.groupby("MajorName")[year_cols].sum()
clusters["Total"] = clusters.sum(axis=1)
clusters = clusters.sort_values("Total", ascending=False).drop(columns="Total")

# Map Chinese → English for display
name_map = {
    "炎症与免疫": "Inflammation & Immunity",
    "刺激参数与设备": "Stimulation Parameters & Devices",
    "自主神经与心血管": "Autonomic & Cardiovascular",
    "精神疾病与情绪": "Psychiatric & Emotional Disorders",
    "核心: vagus nerve, vagus nerve stimulation": "VNS Core Terms",
    "临床试验方法学": "Clinical Trial Methodology",
    "围术期应用": "Perioperative & Surgical",
    "卒中与脑损伤": "Stroke & Brain Injury",
    "认知功能": "Cognitive Function",
    "动物模型": "Animal Models",
    "神经影像": "Neuroimaging",
    "睡眠障碍": "Sleep Disorders",
}
clusters.index = [name_map.get(n, n) for n in clusters.index]

cluster_names = clusters.index.tolist()
n_clusters = len(cluster_names)

# Normalise each row to [0, 1]
data = clusters.values
row_max = data.max(axis=1, keepdims=True)
row_max[row_max == 0] = 1
data_norm = data / row_max

# Horizon bands
n_bands = 4
cmap = LinearSegmentedColormap.from_list("brick", ["#FDEBD0", "#E67E22", "#C0392B", "#78281F"])

fig, axes = plt.subplots(n_clusters, 1, figsize=(26, 2.0 * n_clusters),
                         sharex=True, gridspec_kw={"hspace": 0.05})

for idx, (name, row) in enumerate(clusters.iterrows()):
    ax = axes[idx]
    for j in range(n_bands):
        lo = j / n_bands
        hi = (j + 1) / n_bands
        band_vals = np.clip((data_norm[idx] - lo) / (1.0 / n_bands + 1e-9), 0, 1)
        color = cmap(0.2 + 0.8 * (j / (n_bands - 1)))
        ax.fill_between(range(25), lo, hi,
                        where=band_vals > 0.01,
                        facecolor=color, edgecolor="none", alpha=0.9)
        ax.fill_between(range(25), lo, hi,
                        where=band_vals <= 0.01,
                        facecolor="white", edgecolor="none")

    ax.set_ylim(0, 1)
    ax.set_xlim(-0.5, 24.5)
    ax.axis("off")
    ax.text(-1.5, 0.5, name, ha="right", va="center", fontsize=16,
            fontweight="bold", transform=ax.transAxes, fontfamily="DejaVu Sans")

# Bottom axis
axes[-1].axis("on")
axes[-1].set_xticks(range(0, 25, 4))
axes[-1].set_xticklabels(range(2002, 2027, 4), fontsize=15)
axes[-1].set_yticks([])
for spine in axes[-1].spines.values():
    spine.set_visible(False)
axes[-1].tick_params(bottom=True, left=False, labelsize=15)

fig.suptitle("Horizon Chart: 12 Research Themes Across 25 Years (2002\u20132026)",
             fontsize=24, fontweight="bold", y=0.995)
fig.tight_layout(rect=[0.12, 0.01, 0.98, 0.97])
fig.savefig("figures/fig4_horizon.png", dpi=1200, bbox_inches="tight", facecolor="white")
fig.savefig("figures/fig4_horizon.pdf", bbox_inches="tight", facecolor="white")
plt.close()
print("Fig 4 done —", n_clusters, "clusters")
