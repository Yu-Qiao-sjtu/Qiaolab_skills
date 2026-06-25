"""Fig 3b: Clinical-layer rising new signals (colour strips).
Matches the style of figure_rising_strips.png (basic layer).
Font sizes: 22pt title, 16pt labels, 14pt internal numbers — A4 readable."""
import pandas as pd, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# ── Load ──
burst = pd.read_csv("data/processed/burst-terms-full.csv")

# ── Filter clinical ──
clin = burst[burst["Category"].isin(["clinical", "both"])].copy()
clin["Total"] = clin["2025"].fillna(0) + clin["2026"].fillna(0)

# Rising: 2026 > 2025, AND 2022-2024 absent (already guaranteed by burst definition)
rising = clin[clin["2026"].fillna(0) > clin["2025"].fillna(0)].copy()

# Exclude generic method / stats terms
exclude = {
    "protein level", "expression level", "immunofluorescence staining",
    "western blot", "p value", "standard deviation", "statistical significance",
    "data analysis", "control group", "placebo", "double blind", "single blind",
    "significant difference", "adverse events", "inclusion criteria",
    "exclusion criteria", "informed consent", "body mass index",
    "blood pressure", "heart rate", "body weight",
}
rising = rising[~rising["TERM"].str.lower().isin(exclude)]

# Top 15
rising = rising.nlargest(15, "Total")
terms_list = list(reversed(rising["TERM"].values))
v25 = list(reversed(rising["2025"].fillna(0).astype(int).values))
v26 = list(reversed(rising["2026"].fillna(0).astype(int).values))

# ── Plot ──
fig, ax = plt.subplots(figsize=(14, 9))
y = np.arange(len(terms_list))
max26 = max(v26) if max(v26) > 0 else 1

for i, t in enumerate(terms_list):
    # 2025 bar
    if v25[i] == 0:
        ax.add_patch(
            FancyBboxPatch(
                (-0.35, i - 0.35), 0.01, 0.7,
                boxstyle="round,pad=0.03",
                facecolor="#E5E3DF", edgecolor="none", zorder=1,
            )
        )
    else:
        ax.add_patch(
            FancyBboxPatch(
                (-0.35, i - 0.35), 0.01, 0.7,
                boxstyle="round,pad=0.03",
                facecolor="#E8A87C", edgecolor="none", zorder=1,
            )
        )
        ax.text(
            -0.1, i, str(v25[i]),
            ha="center", va="center", fontsize=14, color="#7B3F1A",
            fontweight="bold", zorder=3,
        )

    # 2026 bar
    w26 = v26[i] / max26 * 0.65
    if v26[i] > 0:
        ax.add_patch(
            FancyBboxPatch(
                (-0.35, i - 0.35), w26, 0.7,
                boxstyle="round,pad=0.03",
                facecolor="#C0392B", edgecolor="none", zorder=2,
            )
        )
        ax.text(
            -0.35 + w26 / 2, i, str(v26[i]),
            ha="center", va="center", fontsize=14, color="white",
            fontweight="bold", zorder=3,
        )

# Column headers
ax.text(0.01, 0.5, "2025", transform=ax.transAxes, ha="center", va="center",
        fontsize=18, fontweight="bold", color="#7B3F1A", rotation=90)
ax.text(0.03, 0.5, "2026", transform=ax.transAxes, ha="center", va="center",
        fontsize=18, fontweight="bold", color="#C0392B", rotation=90)

ax.set_ylim(-0.5, len(terms_list) - 0.5)
ax.set_xlim(-0.4, 0.8)
ax.set_yticks(y)
ax.set_yticklabels(terms_list, fontsize=16, fontfamily="DejaVu Sans")
ax.set_xticks([])
for spine in ax.spines.values():
    spine.set_visible(False)
ax.tick_params(left=False)

ax.set_title(
    "Rising New Signals in Clinical Research\n(2002\u20132024 absent, 2026 > 2025)",
    fontsize=22, fontweight="bold", pad=20,
)

fig.tight_layout(pad=2)
fig.savefig("figures/fig3b_clinical_rising.png", dpi=1200,
            bbox_inches="tight", facecolor="white")
fig.savefig("figures/fig3b_clinical_rising.pdf",
            bbox_inches="tight", facecolor="white")
plt.close()
print("Fig 3b done —", len(terms_list), "terms")
