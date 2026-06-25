"""
taVNS Term Clustering: UMAP + HDBSCAN for 大类/小类 discovery.
Outputs:
  - terms-clustered.csv       (all terms with cluster labels)
  - umap_clusters.png          (2D UMAP visualization)
  - cluster_summary.txt        (major/minor cluster descriptions)
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

# 1. Load data ----------------------------------------------------------
print("Loading data...")
df = pd.read_csv("D:/term/terms-classified.csv")
print(f"  Loaded {len(df):,} terms")

# Clean term text: strip, remove surrounding quotes
terms_raw = df["TERM"].astype(str).str.strip().str.strip('"').str.strip("'").tolist()
print(f"  Unique terms: {len(set(terms_raw)):,}")

# 2. Embed with sentence-transformers -----------------------------------
print("\nLoading embedding model...")
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")

print(f"  Embedding {len(terms_raw):,} terms...")
embeddings = model.encode(terms_raw, show_progress_bar=True, batch_size=256)
print(f"  Embedding shape: {embeddings.shape}")

# 3. UMAP dimensionality reduction --------------------------------------
print("\nRunning UMAP...")
import umap

# UMAP to 2D for visualization
umap_2d = umap.UMAP(
    n_components=2,
    n_neighbors=15,
    min_dist=0.1,
    metric="cosine",
    random_state=42,
    verbose=True,
)
embeddings_2d = umap_2d.fit_transform(embeddings)
df["UMAP_X"] = embeddings_2d[:, 0]
df["UMAP_Y"] = embeddings_2d[:, 1]
print(f"  2D UMAP done. Range X: [{embeddings_2d[:,0].min():.2f}, {embeddings_2d[:,0].max():.2f}]")

# UMAP to 5D for clustering (better cluster separation)
umap_5d = umap.UMAP(
    n_components=5,
    n_neighbors=15,
    min_dist=0.0,
    metric="cosine",
    random_state=42,
    verbose=True,
)
embeddings_5d = umap_5d.fit_transform(embeddings)
print(f"  5D UMAP done.")

# 4. HDBSCAN 大类 clustering --------------------------------------------
print("\nRunning HDBSCAN for 大类 (major clusters)...")
import hdbscan

# Try multiple min_cluster_size to find a good granularity
# We want ~8-20 major clusters
for min_size in [80, 100, 120, 150, 200, 250, 300]:
    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=min_size,
        min_samples=5,
        metric="euclidean",
        cluster_selection_epsilon=0.5,
        cluster_selection_method="eom",
    )
    labels = clusterer.fit_predict(embeddings_5d)
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise = (labels == -1).sum()
    print(f"  min_cluster_size={min_size:3d} → {n_clusters:3d} clusters, {n_noise:5d} noise ({n_noise/len(labels)*100:.1f}%)")

# Pick min_cluster_size=120 as a good balance
BEST_MIN_SIZE = 120
clusterer_major = hdbscan.HDBSCAN(
    min_cluster_size=BEST_MIN_SIZE,
    min_samples=5,
    metric="euclidean",
    cluster_selection_epsilon=0.5,
    cluster_selection_method="eom",
)
major_labels = clusterer_major.fit_predict(embeddings_5d)
n_major = len(set(major_labels)) - (1 if -1 in major_labels else 0)
n_noise_major = (major_labels == -1).sum()
print(f"\n  Selected: {n_major} major clusters, {n_noise_major} noise ({n_noise_major/len(major_labels)*100:.1f}%)")
df["MajorCluster"] = major_labels

# 5. Label major clusters with c-TF-IDF --------------------------------
print("\nLabeling major clusters...")
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter

def label_clusters(terms, labels, max_keywords=8):
    """Use c-TF-IDF to find top keywords per cluster."""
    cluster_docs = {}
    for term, label in zip(terms, labels):
        if label == -1:
            continue
        cluster_docs.setdefault(label, []).append(term)
    
    # Build cluster documents
    cluster_ids = sorted(cluster_docs.keys())
    documents = [" ".join(cluster_docs[c]) for c in cluster_ids]
    
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 3),
        max_features=5000,
        sublinear_tf=True,
    )
    try:
        tfidf_matrix = vectorizer.fit_transform(documents)
    except:
        # Fallback: simple word count
        results = {}
        for i, cid in enumerate(cluster_ids):
            word_counts = Counter(" ".join(cluster_docs[cid]).split())
            results[cid] = [w for w, _ in word_counts.most_common(max_keywords)]
        return results
    
    feature_names = vectorizer.get_feature_names_out()
    results = {}
    for i, cid in enumerate(cluster_ids):
        row = tfidf_matrix[i].toarray().flatten()
        top_indices = row.argsort()[-max_keywords:][::-1]
        keywords = [feature_names[j] for j in top_indices if row[j] > 0]
        results[cid] = keywords
    return results

major_keywords = label_clusters(terms_raw, major_labels)

# Assign human-readable major class names
def name_major_cluster(keywords):
    """Heuristic naming based on top keywords."""
    kw_str = " ".join(keywords).lower()
    
    if any(w in kw_str for w in ["postoperative", "surgery", "perioperative", "surgical", "anesthesia"]):
        return "围术期应用"
    if any(w in kw_str for w in ["depression", "anxiety", "mood", "psychiatric", "mental health", "bipolar", "antidepressant", "psycholog"]):
        return "精神疾病与情绪"
    if any(w in kw_str for w in ["pain", "headache", "migraine", "analges", "nocicept", "chronic pain"]):
        return "疼痛与镇痛"
    if any(w in kw_str for w in ["epilep", "seizure", "convuls"]):
        return "癫痫"
    if any(w in kw_str for w in ["stroke", "ischemia", "infarction", "cerebral", "brain injury", "traumatic brain", "tbi"]):
        return "卒中与脑损伤"
    if any(w in kw_str for w in ["cognit", "memory", "learning", "attention", "executive function", "neuropsycholog"]):
        return "认知功能"
    if any(w in kw_str for w in ["sleep", "insomnia", "circadian"]):
        return "睡眠障碍"
    if any(w in kw_str for w in ["inflammat", "cytokine", "immune", "tnf", "il-", "nf-kb", "oxidative stress", "antioxid"]):
        return "炎症与免疫"
    if any(w in kw_str for w in ["hpa", "cortisol", "hormone", "endocrine", "ghrelin", "leptin", "melatonin"]):
        return "神经内分泌"
    if any(w in kw_str for w in ["heart rate variability", "hrv", "autonomic", "sympathetic", "parasympathetic", "vagal tone", "cardiac", "baroreflex", "blood pressure"]):
        return "自主神经与心血管"
    if any(w in kw_str for w in ["gastrointestin", "gastric", "gut", "intestinal", "bowel", "nausea", "vomit", "colitis", "ibs", "motility"]):
        return "消化系统"
    if any(w in kw_str for w in ["fmri", "eeg", "meg", "pet", "spect", "neuroimaging", "bold", "resting state", "functional connectivity", "default mode", "functional mri"]):
        return "神经影像"
    if any(w in kw_str for w in ["locus coeruleus", "nucleus", "brainstem", "amygdala", "hippocamp", "prefrontal", "insula", "cingulate", "thalamus", "cortex", "basal ganglia", "striatum", "hypothalamus"]):
        return "脑区与回路"
    if any(w in kw_str for w in ["sham", "randomized", "controlled trial", "placebo", "blind", "rct", "protocol", "outcome", "primary outcome", "secondary", "endpoint"]):
        return "临床试验方法学"
    if any(w in kw_str for w in ["neuromodulation", "stimulation parameter", "pulse width", "frequency", "intensity", "dose", "electrode", "current", "waveform", "device", "ear clip"]):
        return "刺激参数与设备"
    if any(w in kw_str for w in ["auricular", "ear", "cymba", "tragus", "acupoint", "acupuncture", "transcutaneous", "percutaneous"]):
        return "耳部刺激定位"
    if any(w in kw_str for w in ["neuroplasticity", "synaptic", "bdnf", "neurotroph", "plasticity", "long-term potentiation", "ltd"]):
        return "神经可塑性"
    if any(w in kw_str for w in ["neurotransmitter", "dopamin", "serotonin", "norepinephrin", "acetylcholin", "gaba", "glutamat", "receptor"]):
        return "神经递质与受体"
    if any(w in kw_str for w in ["parkinson", "alzheimer", "dementia", "neurodegenerat"]):
        return "神经退行性疾病"
    if any(w in kw_str for w in ["cancer", "tumor", "oncology", "chemotherap"]):
        return "肿瘤"
    if any(w in kw_str for w in ["covid", "sars", "coronavirus", "long covid", "post-covid"]):
        return "COVID-19"
    if any(w in kw_str for w in ["diabetes", "glucose", "insulin", "metabolic", "obesity"]):
        return "代谢与内分泌疾病"
    if any(w in kw_str for w in ["animal", "rat", "mouse", "mice", "rodent", "model", "canine", "dog"]):
        return "动物模型"
    if any(w in kw_str for w in ["safety", "adverse event", "side effect", "complication", "tolerability", "feasibility"]):
        return "安全性与耐受性"
    if any(w in kw_str for w in ["heart failure", "myocardial", "cardiovascular disease", "hypertension", "arrhythmia"]):
        return "心血管疾病"
    if any(w in kw_str for w in ["rehabilitation", "physical therapy", "motor", "gait", "balance", "mobility"]):
        return "康复与运动功能"
    
    # Fallback
    if len(keywords) >= 2:
        return f"其他: {keywords[0]}, {keywords[1]}"
    return f"其他: {keywords[0] if keywords else 'unknown'}"

major_names = {}
for cid, kws in major_keywords.items():
    name = name_major_cluster(kws)
    major_names[cid] = name
    print(f"  Cluster {cid} ({len([l for l in major_labels if l==cid]):4d} terms): {name}")
    print(f"    Keywords: {', '.join(kws[:6])}")

df["MajorName"] = df["MajorCluster"].map(major_names).fillna("噪声点")

# 6. HDBSCAN 小类 clustering (within each major cluster) ----------------
print("\n\nRunning HDBSCAN for 小类 (sub-clusters) within each major cluster...")

def subcluster_group(terms_sub, emb_sub, min_size_ratio=0.05):
    """Run HDBSCAN on a subset; return labels."""
    n = len(emb_sub)
    if n < 20:
        return np.zeros(n, dtype=int)  # too small, single cluster
    
    min_cluster = max(5, int(n * min_size_ratio))
    min_cluster = min(min_cluster, 50)  # cap
    
    sub_clusterer = hdbscan.HDBSCAN(
        min_cluster_size=min_cluster,
        min_samples=3,
        metric="euclidean",
        cluster_selection_epsilon=0.3,
        cluster_selection_method="eom",
    )
    return sub_clusterer.fit_predict(emb_sub)

all_minor_labels = np.full(len(df), -1, dtype=int)
minor_names_map = {}  # (major_cluster, minor_cluster) -> name

for major_cid in sorted(set(major_labels)):
    if major_cid == -1:
        continue
    
    mask = major_labels == major_cid
    indices = np.where(mask)[0]
    terms_sub = [terms_raw[i] for i in indices]
    emb_sub = embeddings_5d[indices]
    
    n_sub = len(emb_sub)
    print(f"\n  Major Cluster {major_cid} ({major_names[major_cid]}, {n_sub} terms):")
    
    sub_labels = subcluster_group(terms_sub, emb_sub, min_size_ratio=0.05)
    n_subclusters = len(set(sub_labels)) - (1 if -1 in sub_labels else 0)
    
    all_minor_labels[indices] = sub_labels
    
    # Label subclusters
    sub_keywords = label_clusters(terms_sub, sub_labels, max_keywords=6)
    for sub_cid, kws in sorted(sub_keywords.items()):
        count = (sub_labels == sub_cid).sum()
        sub_name = f"{major_names[major_cid]}: {', '.join(kws[:3])}"
        minor_names_map[(major_cid, sub_cid)] = sub_name
        print(f"    Sub {sub_cid}: {count:4d} terms — {', '.join(kws[:4])}")

df["MinorCluster"] = all_minor_labels
df["MinorName"] = df.apply(
    lambda r: minor_names_map.get((r["MajorCluster"], r["MinorCluster"]), 
                                   f"{r.get('MajorName','')}: 噪声" if r["MinorCluster"] == -1 else f"{r.get('MajorName','')}: {r['MinorCluster']}"),
    axis=1
)

# 7. Statistical summary --------------------------------------------------
print("\n\n====== CLUSTER SUMMARY ======")

# Major cluster stats
print("\n--- 大类 (Major Clusters) ---")
major_stats = df.groupby("MajorName").agg(
    Count=("TERM", "count"),
    Sum_2025_2026=("Total_2025_2026", "sum"),
).sort_values("Count", ascending=False)
print(major_stats.to_string())

# Minor cluster stats (top 30)
print("\n--- 小类 Top 30 (Minor Clusters) ---")
minor_stats = df.groupby("MinorName").agg(
    Count=("TERM", "count"),
    Sum_2025_2026=("Total_2025_2026", "sum"),
).sort_values("Count", ascending=False)
print(minor_stats.head(30).to_string())

# 8. Save outputs ---------------------------------------------------------
print("\n\nSaving outputs...")

# Save full CSV
df.to_csv("D:/term/terms-clustered.csv", index=False)
print("  ✓ terms-clustered.csv")

# Save summary report
with open("D:/term/cluster_summary.txt", "w", encoding="utf-8") as f:
    f.write("========================================\n")
    f.write("taVNS 术语聚类分析报告 (UMAP + HDBSCAN)\n")
    f.write("========================================\n\n")
    f.write(f"总术语数: {len(df):,}\n")
    f.write(f"大类数: {n_major}\n")
    f.write(f"噪声点: {n_noise_major:,} ({n_noise_major/len(df)*100:.1f}%)\n\n")
    
    f.write("--- 大类 ---\n")
    f.write(major_stats.to_string())
    f.write("\n\n--- 小类 Top 50 ---\n")
    f.write(minor_stats.head(50).to_string())
    
    f.write("\n\n--- 各类别 Top 10 术语 (2025-2026合计频次) ---\n")
    for mname in major_stats.index:
        f.write(f"\n## {mname}\n")
        sub = df[df["MajorName"] == mname].nlargest(10, "Total_2025_2026")
        for _, row in sub.iterrows():
            f.write(f"  {row['TERM']:50s}  {row['Total_2025_2026']:4d}\n")

print("  ✓ cluster_summary.txt")

# 9. Visualization ---------------------------------------------------------
print("\nGenerating UMAP plot...")
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.patches import Patch

matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial']
matplotlib.rcParams['axes.unicode_minus'] = False

fig, axes = plt.subplots(1, 2, figsize=(28, 12))

# ------------------------------------------------------------------
# Left: Major clusters with centroid labels
# ------------------------------------------------------------------
ax = axes[0]
major_counts = df["MajorName"].value_counts()
top_majors = [m for m in major_counts.index if m != "噪声点"][:14]
df["PlotMajor"] = df["MajorName"].apply(lambda x: x if x in top_majors else "其他大类")

# Use a bigger palette for better distinction
n_top = len(top_majors)
cmap = plt.cm.tab20
colors_major = [cmap(i / max(n_top, 20)) for i in range(n_top)]

for i, name in enumerate(top_majors):
    mask = df["PlotMajor"] == name
    ax.scatter(df.loc[mask, "UMAP_X"], df.loc[mask, "UMAP_Y"],
               s=1.2, alpha=0.55, color=colors_major[i],
               label=f"{name} ({major_counts.get(name, 0)})", rasterized=True)

    # Centroid label
    cx, cy = df.loc[mask, "UMAP_X"].mean(), df.loc[mask, "UMAP_Y"].mean()
    # Shorten long names for display
    short_name = name if len(name) <= 12 else name[:10] + "…"
    ax.annotate(short_name, (cx, cy), fontsize=11, fontweight="bold",
                ha="center", va="center",
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                          edgecolor=colors_major[i], alpha=0.85))

# Other
mask_other = df["PlotMajor"] == "其他大类"
if mask_other.sum() > 0:
    ax.scatter(df.loc[mask_other, "UMAP_X"], df.loc[mask_other, "UMAP_Y"],
               s=0.5, alpha=0.15, color="gray",
               label=f"其他大类 ({mask_other.sum()})", rasterized=True)

ax.set_title(f"taVNS 术语 UMAP 投影 — 语义大类 (共 {n_major} 类)", fontsize=16, fontweight="bold")
ax.set_xlabel("UMAP-1", fontsize=12)
ax.set_ylabel("UMAP-2", fontsize=12)
ax.legend(loc="lower left", fontsize=10, markerscale=6, ncol=2,
          framealpha=0.85)

# ------------------------------------------------------------------
# Right: Basic vs Clinical split
# ------------------------------------------------------------------
ax2 = axes[1]

# Map English categories to Chinese labels
cat_map = {
    "basic":    ("基础研究 (Basic)",       "#2196F3"),
    "clinical": ("临床 (Clinical)",       "#4CAF50"),
    "both":     ("交叉 (Both)",           "#FF9800"),
}

legend_elements = []
for cat_eng, (cat_label, color) in cat_map.items():
    mask = df["Category"] == cat_eng
    count = mask.sum()
    if count == 0:
        continue
    # Sample large categories for speed; still show all points
    ax2.scatter(df.loc[mask, "UMAP_X"], df.loc[mask, "UMAP_Y"],
                s=1.2, alpha=0.35, color=color,
                label=f"{cat_label} ({count:,})", rasterized=True)
    legend_elements.append(Patch(facecolor=color,
                                 label=f"{cat_label} ({count:,})"))

# Centroid labels for the 3 categories
for cat_eng, (cat_label, color) in cat_map.items():
    mask = df["Category"] == cat_eng
    if mask.sum() == 0:
        continue
    cx, cy = df.loc[mask, "UMAP_X"].mean(), df.loc[mask, "UMAP_Y"].mean()
    ax2.annotate(cat_label.split(" ")[0], (cx, cy), fontsize=14,
                 fontweight="bold", ha="center", va="center",
                 bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
                           edgecolor=color, alpha=0.9, linewidth=2))

ax2.set_title("taVNS 术语 UMAP 投影 — 基础研究 vs 临床", fontsize=16, fontweight="bold")
ax2.set_xlabel("UMAP-1", fontsize=12)
ax2.set_ylabel("UMAP-2", fontsize=12)
ax2.legend(handles=legend_elements, loc="lower left", fontsize=11,
           markerscale=6, framealpha=0.85)

plt.tight_layout(pad=2)
plt.savefig("D:/term/umap_clusters.png", dpi=200, bbox_inches="tight",
            facecolor="white")
plt.close()
print("  ✓ umap_clusters.png")

print("\n✅ All done!")
