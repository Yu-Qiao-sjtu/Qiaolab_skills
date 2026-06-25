"""
Final UMAP: large points (s=30), legend font = title font (22pt bold), English, single panel.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

font_path = "C:/Windows/Fonts/msyh.ttc"
try:
    fm.fontManager.addfont(font_path)
    prop = fm.FontProperties(fname=font_path)
    font_name = prop.get_name()
except:
    font_name = "Arial"

plt.rcParams.update({
    "font.family": font_name,
})

print("Loading terms-clustered.csv ...")
df = pd.read_csv("D:/term/terms-clustered.csv")
print(f"  {len(df):,} rows")

# English name mapping
name_map = {
    "脑区与回路": "Brain Regions & Circuits",
    "刺激参数与设备": "Stimulation Parameters & Devices",
    "炎症与免疫": "Inflammation & Immunity",
    "临床试验方法学": "Clinical Trial Methodology",
    "动物模型": "Animal Models",
    "自主神经与心血管": "Autonomic & Cardiovascular",
    "精神疾病与情绪": "Psychiatric & Emotional Disorders",
    "围术期应用": "Perioperative & Surgical",
    "神经影像": "Neuroimaging",
    "其他: vagus nerve, vagus nerve stimulation": "VNS Core Terms",
    "噪声点": "Noise",
    "卒中与脑损伤": "Stroke & Brain Injury",
    "睡眠障碍": "Sleep Disorders",
    "认知功能": "Cognitive Function",
}
df["EName"] = df["MajorName"].map(name_map)

# Sort by size
major_names_en = sorted(
    [n for n in df["EName"].unique() if n != "Noise"],
    key=lambda n: len(df[df["EName"] == n]),
    reverse=True,
)
palette = plt.cm.tab20(np.linspace(0, 1, len(major_names_en)))

fig, ax = plt.subplots(figsize=(20, 14))

# Noise: grey, small
noise = df[df["EName"] == "Noise"]
ax.scatter(
    noise["UMAP_X"], noise["UMAP_Y"],
    c="lightgrey", s=8, alpha=0.12, rasterized=True,
)

# Clusters: big dots
for i, name in enumerate(major_names_en):
    sub = df[df["EName"] == name]
    ax.scatter(
        sub["UMAP_X"], sub["UMAP_Y"],
        c=[palette[i]],
        s=30,
        alpha=0.55,
        edgecolors="none",
        linewidth=0,
        rasterized=True,
    )

# Legend on the right, outside the plot
import matplotlib.patches as mpatches
patches = []
for i, name in enumerate(major_names_en):
    count = len(df[df["EName"] == name])
    patches.append(
        mpatches.Patch(color=palette[i], label=f"{name} ({count})")
    )

leg = ax.legend(
    handles=patches,
    loc="center left",
    fontsize=22,
    ncol=1,
    framealpha=0.85,
    bbox_to_anchor=(1.02, 0.5),
    title="Clusters",
    title_fontsize=22,
)

ax.set_xlabel("UMAP Dimension 1", fontsize=22, fontweight="bold")
ax.set_ylabel("UMAP Dimension 2", fontsize=22, fontweight="bold")
ax.set_title(
    "taVNS Research Landscape: Semantic Clustering of 15,446 Terms",
    fontsize=22,
    fontweight="bold",
    pad=18,
)
ax.tick_params(axis='both', labelsize=15)

plt.tight_layout(pad=2)
outpath = "D:/term/umap_clusters.png"
fig.savefig(outpath, dpi=200, bbox_inches="tight", facecolor="white")
plt.close()
print(f"\nSaved: {outpath}")
print(f"Noise: {len(noise):,}, Clustered: {len(df) - len(noise):,}")
print("Done!")
