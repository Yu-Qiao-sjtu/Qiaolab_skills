"""Fig S1: Treemap — Major → Minor cluster hierarchy.
Area ∝ term count per minor cluster. Colour = major cluster.
Font sizes: 24pt title, internal labels auto-sized."""
import pandas as pd, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import squarify

# ── Load ──
terms = pd.read_csv("data/clustering/terms-clustered.csv")

# Exclude
exclude_names = ["脑区与回路", "噪声点"]
terms = terms[~terms["MajorName"].isin(exclude_names)]

# Aggregate Major → Minor
minor = terms.groupby(["MajorName", "MinorCluster"]).size().reset_index(name="Count")
minor = minor[minor["Count"] >= 8]
minor = minor.sort_values("Count", ascending=False)

# Map Chinese → English for major clusters
name_map = {
    "炎症与免疫": "Inflammation & Immunity",
    "刺激参数与设备": "Stimulation Params & Devices",
    "自主神经与心血管": "Autonomic & Cardiovascular",
    "精神疾病与情绪": "Psychiatric & Emotional",
    "核心: vagus nerve, vagus nerve stimulation": "VNS Core Terms",
    "临床试验方法学": "Clinical Trial Methodology",
    "围术期应用": "Perioperative & Surgical",
    "卒中与脑损伤": "Stroke & Brain Injury",
    "认知功能": "Cognitive Function",
    "动物模型": "Animal Models",
    "神经影像": "Neuroimaging",
    "睡眠障碍": "Sleep Disorders",
}
minor["MajorEN"] = minor["MajorName"].map(name_map)

major_names = minor["MajorEN"].unique()
n_majors = len(major_names)

palette = [
    "#576081", "#55FB5B", "#F55DF4", "#F0AC57", "#59C7F3",
    "#7457FB", "#C0F783", "#D3575A", "#FCA6C8", "#60A25A",
    "#90FED9", "#B39DDB",
]
major_color = dict(zip(major_names, palette[:n_majors]))

fig, ax = plt.subplots(figsize=(22, 14))
sizes = minor["Count"].values
labels = []
for _, row in minor.iterrows():
    maj_en = row["MajorEN"]
    if isinstance(maj_en, float) and np.isnan(maj_en):
        maj_en = str(row["MajorName"])[:20]
    short = f"{maj_en[:20]} #{int(row['MinorCluster'])}"
    labels.append(f"{short}\n({row['Count']})")

colors = [major_color[m] for m in minor["MajorEN"].values]

squarify.plot(sizes=sizes, label=labels, color=colors, alpha=0.85,
              ax=ax, text_kwargs={"fontsize": 11, "fontfamily": "DejaVu Sans",
                                  "wrap": True}, pad=2)

ax.set_axis_off()
ax.set_title("Term Hierarchy: Major \u2192 Minor Clusters\n(Area \u221d Term Count, \u2265 8 terms per subgroup)",
             fontsize=24, fontweight="bold", pad=20)

from matplotlib.patches import Patch
legend_patches = [Patch(facecolor=major_color[m], label=m, alpha=0.85) for m in major_names]
ax.legend(handles=legend_patches, loc="upper left", bbox_to_anchor=(0.01, 0.99),
          fontsize=13, framealpha=0.9, ncol=2)

fig.tight_layout(pad=1)
fig.savefig("figures/figS1_treemap.png", dpi=1200, bbox_inches="tight", facecolor="white")
fig.savefig("figures/figS1_treemap.pdf", bbox_inches="tight", facecolor="white")
plt.close()
print("Fig S1 done")
