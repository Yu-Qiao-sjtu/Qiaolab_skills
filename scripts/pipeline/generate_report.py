"""Generate summary report and UMAP plot from clustered data."""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# Force English-friendly font fallback
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = ['Arial']
matplotlib.rcParams['axes.unicode_minus'] = False

df = pd.read_csv("D:/term/terms-clustered.csv")
print(f"Loaded {len(df)} terms")

# 1. Summary report
with open("D:/term/cluster_summary.txt", "w", encoding="utf-8") as f:
    f.write("=" * 70 + "\n")
    f.write("taVNS Term Clustering Analysis Report\n")
    f.write("UMAP + HDBSCAN Semantic Clustering\n")
    f.write("=" * 70 + "\n\n")
    f.write(f"Total terms: {len(df):,}\n")
    f.write(f"Major clusters: {df['MajorName'].nunique()}\n")
    f.write(f"Minor clusters: {df['MinorName'].nunique()}\n")
    f.write(f"Noise points: {df['MajorCluster'].eq(-1).sum():,}\n\n")
    
    # Major clusters
    f.write("-" * 70 + "\n")
    f.write("MAJOR CLUSTERS (14 classes)\n")
    f.write("-" * 70 + "\n\n")
    
    major_stats = df.groupby("MajorName").agg(
        Count=("TERM", "count"),
        Sum_2025_2026=("Total_2025_2026", "sum"),
        Sum_2022_2026=("Total_2022_2026", "sum"),
        BasicCount=("Category", lambda x: (x == "基础研究").sum()),
        ClinicalCount=("Category", lambda x: (x == "临床").sum()),
    ).sort_values("Count", ascending=False)
    
    for idx, row in major_stats.iterrows():
        f.write(f"## {idx}\n")
        f.write(f"   Terms: {int(row['Count']):,} | 2025-2026 freq: {int(row['Sum_2025_2026']):,} | "
                f"2022-2026 freq: {int(row['Sum_2022_2026']):,}\n")
        f.write(f"   Basic: {int(row['BasicCount']):,} | Clinical: {int(row['ClinicalCount']):,}\n")
        
        # Top 5 terms in this cluster by 2025-2026 frequency
        top = df[df["MajorName"] == idx].nlargest(5, "Total_2025_2026")
        f.write("   Top terms: " + " | ".join(f"{r['TERM']}({int(r['Total_2025_2026'])})" for _, r in top.iterrows()) + "\n\n")
    
    # Minor clusters
    f.write("-" * 70 + "\n")
    f.write("MINOR CLUSTERS (85 sub-classes, top 50 shown)\n")
    f.write("-" * 70 + "\n\n")
    
    minor_stats = df.groupby("MinorName").agg(
        Count=("TERM", "count"),
        Sum_2025_2026=("Total_2025_2026", "sum"),
    ).sort_values("Count", ascending=False)
    
    for i, (idx, row) in enumerate(minor_stats.head(50).iterrows()):
        f.write(f"{i+1:2d}. {idx}\n")
        f.write(f"    Terms: {int(row['Count']):,} | 2025-2026 freq: {int(row['Sum_2025_2026']):,}\n")
        top = df[df["MinorName"] == idx].nlargest(5, "Total_2025_2026")
        f.write("    Top: " + " | ".join(f"{r['TERM']}({int(r['Total_2025_2026'])})" for _, r in top.iterrows()) + "\n\n")
    
    f.write("=" * 70 + "\n")
    f.write("End of Report\n")

print("Saved cluster_summary.txt")

# 2. UMAP plot
fig, axes = plt.subplots(1, 2, figsize=(24, 10))

# Use abbreviated English names for display
major_abbrev = {
    "自主神经与心血管": "Autonomic/CV",
    "脑区与回路": "Brain Regions",
    "炎症与免疫": "Inflammation/Immune",
    "刺激参数与设备": "Stimulation/Tech",
    "精神疾病与情绪": "Psychiatric/Mood",
    "围术期应用": "Perioperative",
    "临床试验方法学": "Clinical Trial Methods",
    "卒中与脑损伤": "Stroke/Brain Injury",
    "动物模型": "Animal Models",
    "认知功能": "Cognitive Function",
    "神经影像": "Neuroimaging",
    "睡眠障碍": "Sleep Disorders",
}
# Get the actual names in the data
actual_majors = df["MajorName"].value_counts().head(12).index.tolist()
# Filter to ones we have abbreviations for
plot_majors = [m for m in actual_majors if m in major_abbrev]
other_mask = ~df["MajorName"].isin(plot_majors)

# Left: Major clusters
ax = axes[0]
colors = plt.cm.tab20(np.linspace(0, 1, len(plot_majors) + 1))
for i, name in enumerate(plot_majors):
    mask = df["MajorName"] == name
    count = mask.sum()
    ax.scatter(df.loc[mask, "UMAP_X"], df.loc[mask, "UMAP_Y"],
               s=0.8, alpha=0.6, color=colors[i], 
               label=f"{major_abbrev[name]} ({count:,})", rasterized=True)
if other_mask.sum() > 0:
    ax.scatter(df.loc[other_mask, "UMAP_X"], df.loc[other_mask, "UMAP_Y"],
               s=0.3, alpha=0.15, color="gray", label=f"Other ({other_mask.sum():,})", rasterized=True)

ax.set_title("taVNS Terms UMAP — Semantic Clusters (14 Major Classes)", fontsize=13, fontweight='bold')
ax.set_xlabel("UMAP-1")
ax.set_ylabel("UMAP-2")
ax.legend(loc="lower left", fontsize=7, markerscale=6, ncol=2, framealpha=0.8)

# Right: Basic vs Clinical
ax2 = axes[1]
cat_colors = {"基础研究": "#2196F3", "临床": "#4CAF50", "交叉": "#FF9800"}
cat_labels = {"基础研究": "Basic Research", "临床": "Clinical", "交叉": "Overlap"}
for cat, color in cat_colors.items():
    mask = df["Category"] == cat
    count = mask.sum()
    ax2.scatter(df.loc[mask, "UMAP_X"], df.loc[mask, "UMAP_Y"],
                s=0.8, alpha=0.3, color=color, rasterized=True)
    ax2.scatter([], [], s=30, color=color, label=f"{cat_labels[cat]} ({count:,})")

ax2.set_title("taVNS Terms UMAP — Basic Research vs Clinical", fontsize=13, fontweight='bold')
ax2.set_xlabel("UMAP-1")
ax2.set_ylabel("UMAP-2")
ax2.legend(loc="lower left", fontsize=9, markerscale=2, framealpha=0.8)

plt.tight_layout()
plt.savefig("D:/term/umap_clusters.png", dpi=150, bbox_inches="tight", facecolor='white')
plt.close()
print("Saved umap_clusters.png")

# 3. Save a simplified Chinese-friendly version too
# Generate a clean summary CSV for major clusters
major_export = major_stats.copy()
major_export.index.name = "MajorCluster"
major_export.to_csv("D:/term/major_clusters_summary.csv")
print("Saved major_clusters_summary.csv")

minor_export = minor_stats.copy()
minor_export.index.name = "MinorCluster"
minor_export.to_csv("D:/term/minor_clusters_summary.csv")
print("Saved minor_clusters_summary.csv")

print("\nDone!")
