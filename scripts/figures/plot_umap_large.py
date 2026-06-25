import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.font_manager as fm

# Use a CJK-capable font available on Windows
font_path = "C:/Windows/Fonts/msyh.ttc"  # Microsoft YaHei
try:
    fm.fontManager.addfont(font_path)
    prop = fm.FontProperties(fname=font_path)
    font_name = prop.get_name()
except:
    font_name = "SimHei"

plt.rcParams.update({
    "font.family": font_name,
    "font.size": 13,
    "axes.labelsize": 16,
    "axes.labelweight": "bold",
    "xtick.labelsize": 13,
    "ytick.labelsize": 13,
})

df = pd.read_csv("terms-clustered.csv")

# Map Chinese names to English
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

major_names_en = sorted(
    [n for n in df["EName"].unique() if n != "Noise"],
    key=lambda n: len(df[df["EName"] == n]),
    reverse=True,
)
palette = plt.cm.tab20(np.linspace(0, 1, len(major_names_en)))

fig, ax = plt.subplots(figsize=(18, 14))

# Noise: grey, tiny
noise = df[df["EName"] == "Noise"]
ax.scatter(
    noise["UMAP_X"], noise["UMAP_Y"],
    c="lightgrey", s=0.5, alpha=0.15, rasterized=True,
)

# Clusters: larger dots (s=8)
for i, name in enumerate(major_names_en):
    sub = df[df["EName"] == name]
    ax.scatter(
        sub["UMAP_X"], sub["UMAP_Y"],
        c=[palette[i]],
        s=8,                    # <-- bigger dots
        alpha=0.55,
        edgecolors="none",
        linewidth=0,
        rasterized=True,
    )

# Legend
patches = []
for i, name in enumerate(major_names_en):
    count = len(df[df["EName"] == name])
    patches.append(
        mpatches.Patch(color=palette[i], label=f"{name} ({count})")
    )

leg = ax.legend(
    handles=patches,
    loc="lower left",
    fontsize=9,
    ncol=2,
    framealpha=0.85,
    bbox_to_anchor=(-0.02, -0.02),
)

ax.set_xlabel("UMAP Dimension 1")
ax.set_ylabel("UMAP Dimension 2")
ax.set_title(
    "taVNS Research Landscape: Semantic Clustering of 15,446 Terms",
    fontsize=18,
    fontweight="bold",
    pad=18,
)
ax.set_xticks([])
ax.set_yticks([])

plt.tight_layout()
fig.savefig("umap_clusters.png", dpi=200, bbox_inches="tight")
print("Done: umap_clusters.png")
print(f"Noise: {len(noise)}, Clustered: {len(df) - len(noise)}")
