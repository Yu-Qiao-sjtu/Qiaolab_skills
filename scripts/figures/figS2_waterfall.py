"""Fig S2: Waterfall chart — Δ growth/decline per major cluster.
Δ = mean(2025+2026) − mean(2022+2023+2024).
Font sizes: 24pt title, 18pt axis labels, 14pt bar labels."""
import pandas as pd, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ── Load ──
terms = pd.read_csv("data/clustering/terms-clustered.csv")

# Exclude
exclude_names = ["脑区与回路", "噪声点"]
terms = terms[~terms["MajorName"].isin(exclude_names)]

year_cols = [str(y) for y in range(2002, 2027)]

# Aggregate by MajorName
clusters = terms.groupby("MajorName")[year_cols].sum()

# Map to English
name_map = {
    "炎症与免疫": "Inflammation & Immunity",
    "刺激参数与设备": "Stimulation Params & Devices",
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

early = clusters[["2022", "2023", "2024"]].mean(axis=1)
late = clusters[["2025", "2026"]].mean(axis=1)
delta = late - early
delta = delta.sort_values(ascending=True)

# ── Plot ──
fig, ax = plt.subplots(figsize=(16, 10))
x = np.arange(len(delta))
colors = ["#C0392B" if v >= 0 else "#2980B9" for v in delta.values]

ax.barh(x, delta.values, color=colors, height=0.6, edgecolor="white", linewidth=0.8)

for i, (v, name) in enumerate(zip(delta.values, delta.index)):
    sign = "+" if v >= 0 else ""
    ax.text(v + (1 if v >= 0 else -1), i,
            f"{sign}{v:.0f}",
            ha="left" if v >= 0 else "right",
            va="center", fontsize=14, fontweight="bold",
            color="#C0392B" if v >= 0 else "#2980B9")

ax.set_yticks(x)
ax.set_yticklabels(delta.index, fontsize=18, fontfamily="DejaVu Sans")
ax.set_xlabel("\u0394 mean annual frequency (2025\u201326 \u2212 2022\u201324)",
              fontsize=20, fontweight="bold")
ax.set_title("Theme Growth & Decline\n(Pre-2025 baseline vs 2025\u20132026 surge)",
             fontsize=24, fontweight="bold", pad=20)

ax.axvline(0, color="black", linewidth=1, linestyle="--", alpha=0.4)
ax.tick_params(axis="x", labelsize=15)
for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)

fig.tight_layout(pad=2)
fig.savefig("figures/figS2_waterfall.png", dpi=1200, bbox_inches="tight", facecolor="white")
fig.savefig("figures/figS2_waterfall.pdf", bbox_inches="tight", facecolor="white")
plt.close()
print("Fig S2 done")
