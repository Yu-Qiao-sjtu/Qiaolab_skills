"""Figure 1: Streamgraph — 12 meaningful research themes over 25 years (2002–2026).
   Brain Regions & Circuits (miscellany) and Noise removed.
   Labels right-aligned in a single column with leader lines."""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ── Data ───────────────────────────────────────────────────────────────
df = pd.read_csv(Path(__file__).resolve().parents[2] / "data" / "clustering" / "terms-clustered.csv")
years = [str(y) for y in range(2002, 2027)]

grp = df.groupby("MajorName")[years].sum()

# Map to English names
known = {
    8410: "Brain Regions & Circuits",
    1470: "Noise",
    1248: "Inflammation & Immunity",
    698:  "Stimulation Parameters & Devices",
    650:  "Psychiatric & Emotional Disorders",
    628:  "Perioperative & Surgical",
    615:  "Autonomic & Cardiovascular",
    456:  "Clinical Trial Methodology",
    392:  "VNS Core Terms",
    278:  "Stroke & Brain Injury",
    199:  "Animal Models",
    147:  "Cognitive Function",
    130:  "Neuroimaging",
    125:  "Sleep Disorders",
}
counts_by_name = df.groupby("MajorName").size()
name_map_eng = {}
for orig_name, cnt in counts_by_name.items():
    name_map_eng[orig_name] = known.get(cnt, orig_name)
grp.index = [name_map_eng.get(i, i) for i in grp.index]

# ── Drop Brain Regions & Circuits + Noise ─────────────────────────────
DROP = {"Brain Regions & Circuits", "Noise"}
grp = grp.loc[[lbl for lbl in grp.index if lbl not in DROP]]

# Reorder by total descending
totals = grp.sum(axis=1)
order = totals.sort_values(ascending=False)
grp = grp.loc[order.index]

data = grp.values
labels = grp.index.tolist()
n_clusters, n_years = data.shape
x = np.arange(n_years)

print(f"Clusters after drop: {n_clusters}")
for lbl, tot in zip(labels, totals[order.index]):
    print(f"  {lbl}: {int(tot)}")

# ── Streamgraph baseline ──────────────────────────────────────────────
def stream_baseline(data):
    cum = np.zeros(data.shape[1])
    baselines = np.zeros_like(data)
    for i in range(data.shape[0]):
        baselines[i] = cum
        cum += data[i]
    mid = cum / 2
    return baselines - mid

base = stream_baseline(data)
ymin = base.min()
ymax = (base + data).max()

# ── Colors ─────────────────────────────────────────────────────────────
from distinctipy import get_colors

# Generate 12 maximally distinct colors, excluding white/near-white
raw_colors = get_colors(n_clusters, exclude_colors=[(1, 1, 1), (0.95, 0.95, 0.95)],
                        pastel_factor=0.5, rng=42)
colors = ["#{:02x}{:02x}{:02x}".format(int(r*255), int(g*255), int(b*255))
          for r, g, b in raw_colors]
print("Generated colors:", colors)

# ── Plot ───────────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 10,
})

fig, ax = plt.subplots(figsize=(30, 12))

# Build polygons
for i in range(n_clusters):
    y0 = base[i]
    y1 = base[i] + data[i]
    verts_top = list(zip(x, y1))
    verts_bot = list(zip(x[::-1], y0[::-1]))
    verts = verts_top + verts_bot
    poly = plt.Polygon(verts, facecolor=colors[i], edgecolor="white",
                       linewidth=0.4, alpha=0.92)
    ax.add_patch(poly)

# ── Right-side labels — one column, spaced to match stream thickness ───
last_x = n_years - 1
# Calculate midpoint of each stream at the right edge
midpoints = []
for i in range(n_clusters):
    my = base[i, last_x] + data[i, last_x] / 2
    midpoints.append(my)

# Sort entries top-to-bottom by midpoint
entries = list(zip(range(n_clusters), labels, midpoints))
entries.sort(key=lambda t: t[2], reverse=True)

# Place labels uniformly across the full y-range with direct leader lines
# Each label gets equal vertical space; leader line connects to actual stream midpoint
y_range = ymax - ymin
label_spacing = y_range / (n_clusters + 1)
label_positions = [ymax - (j + 1) * label_spacing for j in range(n_clusters)]

text_x = last_x + 3.0  # all labels in one column further right

for j, (orig_i, lbl, actual_my) in enumerate(entries):
    label_y = label_positions[j]

    # Leader line from stream edge to label
    ax.plot([last_x + 0.1, text_x - 0.3], [actual_my, label_y],
            color="#888888", linewidth=0.5, linestyle="-", clip_on=False)

    ax.text(text_x, label_y, lbl, va="center", ha="left",
            fontsize=18, fontweight="bold", color="#222222")

# Axes
ax.set_xlim(-0.5, last_x + 11)
ax.set_ylim(ymin * 1.03, ymax * 1.08)
ax.set_xticks(x)
ax.set_xticklabels([str(y) for y in range(2002, 2027)],
                   rotation=45, ha="right", fontsize=18)
ax.set_yticks([])
for spine in ["top", "right", "left"]:
    ax.spines[spine].set_visible(False)
ax.tick_params(left=False)

# Title
ax.set_title("Evolution of taVNS Research Themes (2002–2026)",
             fontsize=24, fontweight="bold", pad=20)

# ── Save ───────────────────────────────────────────────────────────────
out_dir = Path(__file__).resolve().parents[2] / "figures"
out_dir.mkdir(exist_ok=True)

for fmt, dpi in [("png", 1200), ("pdf", None)]:
    path = out_dir / f"fig1_streamgraph.{fmt}"
    fig.savefig(path, dpi=dpi, bbox_inches="tight", facecolor="white", edgecolor="none")
    print(f"Saved: {path}")

plt.close()
print("Done — 12 meaningful themes, labels in one column with leader lines.")
