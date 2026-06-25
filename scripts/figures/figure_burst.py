"""Publication-quality Dumbbell Chart: Emerging Burst Terms (2025–2026)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import numpy as np

# ── Data ──────────────────────────────────────────────────────────
data = [
    # (term, 2025, 2026, category)
    ("myocardial infarction",       5, 1, "Autonomic & Cardiovascular"),
    ("oxidative stress",            0, 4, "Inflammation & Immunity"),
    ("chronic heart failure",       4, 0, "Autonomic & Cardiovascular"),
    ("traumatic brain injury",      0, 4, "Stroke & Brain Injury"),
    ("continuous glucose monitoring",4, 0, "Inflammation & Immunity"),
    ("synaptic plasticity",         0, 3, "Stroke & Brain Injury"),
    ("remote ischemic conditioning",0, 2, "Stroke & Brain Injury"),
    ("macrophage polarization",     0, 2, "Inflammation & Immunity"),
    ("glucagon-like peptide-1",     0, 2, "Inflammation & Immunity"),
    ("immune-inflammatory responses",0,2, "Inflammation & Immunity"),
    ("bdnf level",                  0, 2, "Inflammation & Immunity"),
    ("closed-loop neurostimulation",0, 1, "Cognitive Function"),
]

# ── Style constants ───────────────────────────────────────────────
CATEGORIES = ["Inflammation & Immunity",
              "Autonomic & Cardiovascular",
              "Stroke & Brain Injury",
              "Cognitive Function"]

CAT_COLORS = {
    "Inflammation & Immunity":      "#E64B35",
    "Autonomic & Cardiovascular":   "#4DBBD5",
    "Stroke & Brain Injury":        "#00A087",
    "Cognitive Function":           "#3C5488",
}

YEAR_COLORS = ["#B0BEC5", "#263238"]

# ── Figure setup ──────────────────────────────────────────────────
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.labelsize": 11,
    "axes.linewidth": 0.6,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "figure.dpi": 150,
    "savefig.dpi": 600,
    "savefig.bbox": "tight",
})

fig, ax = plt.subplots(figsize=(7.2, 5.2))

# ── Y ordering: by category then total frequency ──────────────────
data.sort(key=lambda d: (CATEGORIES.index(d[3]), -(d[1] + d[2])))
terms = [d[0] for d in data]
y_pos = list(range(len(data)))

# ── Draw dumbbells ────────────────────────────────────────────────
for i, (term, v25, v26, cat) in enumerate(data):
    color = CAT_COLORS[cat]
    ax.plot([v25, v26], [i, i], color=color, linewidth=1.2, alpha=0.7, zorder=2)
    ax.scatter(v25, i, s=80, color=YEAR_COLORS[0], edgecolors=color,
               linewidths=1.2, zorder=3)
    ax.scatter(v26, i, s=80, color=YEAR_COLORS[1], edgecolors=color,
               linewidths=1.2, zorder=3)

# ── Category separator lines ──────────────────────────────────────
prev_cat = None
for i, (_, _, _, cat) in enumerate(data):
    if cat != prev_cat and prev_cat is not None:
        ax.axhline(y=i - 0.5, color="#CFD8DC", linewidth=0.5, linestyle=":", zorder=1)
    prev_cat = cat

# ── Category labels (right margin) ────────────────────────────────
ax_right = ax.twinx()
ax_right.set_ylim(ax.get_ylim())
ax_right.set_yticks([])

cat_ranges = {}
for i, (_, _, _, cat) in enumerate(data):
    cat_ranges.setdefault(cat, []).append(i)

for cat, indices in cat_ranges.items():
    mid = (indices[0] + indices[-1]) / 2
    ax_right.annotate(
        cat, xy=(1.02, mid), xycoords=("axes fraction", "data"),
        fontsize=8.5, fontweight="bold", color=CAT_COLORS[cat],
        ha="left", va="center",
        bbox=dict(boxstyle="round,pad=0.15", facecolor="white",
                  edgecolor=CAT_COLORS[cat], linewidth=0.6, alpha=0.9),
    )

# ── Axes styling ──────────────────────────────────────────────────
ax.set_yticks(list(y_pos))
ax.set_yticklabels(terms)
ax.set_xlabel("Frequency in literature", fontweight="bold")
ax.set_xlim(-0.5, 6.2)
ax.xaxis.set_major_locator(mticker.MultipleLocator(1))
ax.xaxis.set_minor_locator(mticker.MultipleLocator(0.5))

ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.tick_params(axis="both", length=4, width=0.6)

# ── Legend ────────────────────────────────────────────────────────
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker="o", color="w", markerfacecolor=YEAR_COLORS[0],
           markeredgecolor="#607D8B", markersize=9, label="2025"),
    Line2D([0], [0], marker="o", color="w", markerfacecolor=YEAR_COLORS[1],
           markeredgecolor="#607D8B", markersize=9, label="2026"),
]
leg = ax.legend(handles=legend_elements, loc="upper right",
                frameon=True, framealpha=0.9, edgecolor="#BDBDBD",
                title="Year", title_fontsize=9)
leg.get_frame().set_linewidth(0.5)

# ── Title ─────────────────────────────────────────────────────────
ax.set_title("Emerging Terms in Basic Mechanism Research (2025\u20132026)",
             fontweight="bold", pad=12)

# ── Grid ──────────────────────────────────────────────────────────
ax.grid(axis="x", color="#ECEFF1", linewidth=0.5, alpha=0.8)
ax.set_axisbelow(True)

# ── Save ──────────────────────────────────────────────────────────
plt.tight_layout(pad=1.2)
fig.savefig("figure_burst_dumbbell.png", dpi=600, bbox_inches="tight",
            facecolor="white", edgecolor="none")
fig.savefig("figure_burst_dumbbell.pdf", bbox_inches="tight",
            facecolor="white", edgecolor="none")
plt.close()
print("Saved: figure_burst_dumbbell.png + .pdf")
