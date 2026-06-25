"""
Re-draw UMAP: single panel, English labels, larger axis fonts.
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial']
matplotlib.rcParams['axes.unicode_minus'] = False

print("Loading terms-clustered.csv ...")
df = pd.read_csv("D:/term/terms-clustered.csv")
print(f"  {len(df):,} rows")

fig, ax = plt.subplots(figsize=(16, 14))

major_counts = df["MajorName"].value_counts()
# Exclude noise
top_majors = [m for m in major_counts.index if m != "噪声点"][:14]
df["PlotMajor"] = df["MajorName"].apply(lambda x: x if x in top_majors else "Other")

n_top = len(top_majors)
cmap = plt.cm.tab20
colors_major = [cmap(i / max(n_top, 20)) for i in range(n_top)]

for i, name in enumerate(top_majors):
    mask = df["PlotMajor"] == name
    ax.scatter(df.loc[mask, "UMAP_X"], df.loc[mask, "UMAP_Y"],
               s=1.2, alpha=0.55, color=colors_major[i],
               label=f"{name} ({major_counts.get(name, 0)})", rasterized=True)

# Other
mask_other = df["PlotMajor"] == "Other"
if mask_other.sum() > 0:
    ax.scatter(df.loc[mask_other, "UMAP_X"], df.loc[mask_other, "UMAP_Y"],
               s=0.5, alpha=0.15, color="gray",
               label=f"Other ({mask_other.sum()})", rasterized=True)

ax.set_title("taVNS Terminology — UMAP Semantic Clusters", fontsize=18, fontweight="bold")
ax.set_xlabel("UMAP-1", fontsize=16)
ax.set_ylabel("UMAP-2", fontsize=16)
ax.tick_params(axis='both', labelsize=13)
ax.legend(loc="lower left", fontsize=10, markerscale=6, ncol=2, framealpha=0.85)

plt.tight_layout(pad=2)
outpath = "D:/term/umap_clusters.png"
plt.savefig(outpath, dpi=200, bbox_inches="tight", facecolor="white")
plt.close()
print(f"\nSaved: {outpath}")
print("Done!")
