# taVNS Literature Terminology Analysis

**Research question**: Bibliometric and semantic analysis of terminology in the transcutaneous
auricular vagus nerve stimulation (taVNS) literature, 2002–2026.

---

## Directory structure

```
D:\term\
├── README.md                          ← This file
├── pyproject.toml                     ← Python project config (uv)
├── uv.lock                            ← Locked dependencies
├── .python-version                    ← Python 3.11
│
├── data/
│   ├── raw/
│   │   ├── term-entropy.csv           ← Original term × year matrix (16,362 terms)
│   │   └── relative-term-entropy.csv  ← Relative entropy variant
│   │
│   ├── processed/
│   │   ├── term-entropy-filtered.csv  ← After removing taVNS synonyms & function words
│   │   │                                  (15,446 terms × 25 years)
│   │   ├── terms-classified.csv       ← All 15,446 terms with:
│   │   │                                  - basic/clinical/both label
│   │   │                                  - 14 major cluster labels
│   │   │                                  - UMAP x, y coordinates
│   │   │                                  - Annual frequencies (2002–2026)
│   │   ├── term-2025-2026.csv         ← Terms appearing in 2025–2026 only (6,977)
│   │   ├── burst-terms-2025-2026.csv  ← Burst terms: first-ever appearance in 2025–2026
│   │   │                                  (5,680 terms)
│   │   ├── burst-terms-full.csv       ← Burst terms with classification
│   │   └── basic-mechanism-burst.csv  ← Burst terms, basic-mechanism subset (978)
│   │
│   └── clustering/
│       ├── terms-clustered.csv        ← Terms + cluster labels + UMAP coords (2.8 MB)
│       ├── major_clusters_summary.csv ← 14 major cluster summary
│       └── minor_clusters_summary.csv ← 85 sub-cluster summary
│
├── reports/
│   ├── comprehensive-report.txt       ← Full three-dimensional analysis
│   │                                  │   (hotspots + bursts + 2022–2026 evolution)
│   ├── basic-mechanism-report.txt     ← Basic mechanism layer: 3-D analysis
│   │                                  │   (Inflammation, Autonomic/CV, Stroke/TBI,
│   │                                  │    Animal Models, Cognitive Function)
│   ├── semantic-analysis-report.txt   ← First-pass semantic classification (15 categories)
│   ├── cluster_summary.txt            ← UMAP + HDBSCAN clustering report
│   ├── report-basic-clinical.txt      ← Basic vs. clinical stratification
│   ├── cluster_map_utf8.txt           ← Cluster label mapping (internally used)
│   └── cluster_names.txt              ← Human-readable cluster names
│
├── figures/
│   ├── umap_clusters.png              ← UMAP 2-D embedding (15,446 points, 14 classes)
│   ├── figure_rising_strips.png       ← Rising signals (15 terms, tile-style, 600 dpi)
│   └── figure_rising_strips.pdf       ← Vector version for submission
│
├── scripts/
│   ├── main.py                        ← Entry point (placeholder)
│   │
│   ├── pipeline/                      ← Core analysis pipelines (run these first)
│   │   ├── filter_terms.py            ←   Step 1: Remove taVNS synonyms & function words
│   │   ├── semantic_analysis.py       ←   Step 2: Semantic classification of terms
│   │   ├── analyze_2025_2026.py       ←   Step 3a: 2025–2026 hotspot analysis
│   │   ├── analyze_basic_clinical.py  ←   Step 3b: Basic vs clinical stratification
│   │   ├── comprehensive_analysis.py  ←   Step 4: Full 3-D analysis (all layers)
│   │   ├── basic_mechanism_analysis.py←   Step 5: Basic mechanism deep dive
│   │   ├── cluster_analysis.py        ←   Step 6: UMAP + HDBSCAN clustering
│   │   ├── generate_report.py         ←   Report generation utilities
│   │   ├── analyze_rising.py          ←   Rising signal extraction
│   │   └── rising_top20.py            ←   Top rising signal query
│   │
│   ├── figures/                       ← Figure-generation scripts
│   │   ├── plot_umap.py               ←   Initial UMAP plot
│   │   ├── plot_umap_english.py       ←   UMAP with English labels
│   │   ├── plot_umap_hulls.py         ←   UMAP with convex hulls
│   │   ├── plot_umap_large.py         ←   UMAP with larger markers
│   │   ├── redraw_umap.py             ←   Redraw UMAP (various iterations)
│   │   ├── redraw_umap_single.py      ←   Single-panel UMAP
│   │   ├── draw_final_umap.py         ←   Final UMAP figure
│   │   ├── figure_burst.py            ←   Dumbbell burst plot
│   │   ├── plot_dumbbell.py           ←   Dumbbell chart generation
│   │   ├── plot_rising.py             ←   Rising signals – v1
│   │   ├── plot_rising_v2.py          ←   Rising signals – v2
│   │   ├── plot_rising_v3.py          ←   Rising signals – v3
│   │   ├── plot_rising_final.py       ←   Rising signals – final
│   │   ├── fig_rising.py              ←   Rising strip plot
│   │   ├── gen_figure.py              ←   General figure utilities
│   │   ├── fix_strips.py              ←   Strip plot label fix
│   │   └── tile_plot.py               ←   Tile heatmap plot
│   │
│   └── utils/                         ← Debugging & verification scripts
│       ├── check_burst.py
│       ├── check_burst2.py
│       ├── check_cols.py
│       ├── check_terms.py
│       ├── check_terms2.py
│       └── _debug_names.txt
│
└── archive/                           ← Superseded figure iterations
    ├── figure_burst_dumbbell.png/pdf   ← 12-term dumbbell chart
    ├── figure_rising_signals.png/pdf   ← 10-term dumbbell (blank=2025, solid=2026)
    └── figure_rising_tiles.png/pdf     ← 25/50-term tile heatmap
```

---

## Analysis pipeline

```
term-entropy.csv (16,362 terms × 25 years)
        │
        ▼
┌─────────────────────┐
│ 1. filter_terms.py  │  Remove taVNS synonyms, abbreviations, function words
└─────────┬───────────┘
          │ 15,446 terms
          ▼
┌─────────────────────────┐
│ 2. cluster_analysis.py  │  Sentence-BERT embedding → UMAP → HDBSCAN
└─────────┬───────────────┘
          │ 14 major classes + 85 sub-classes
          ▼
┌────────────────────────────────┐
│ 3. analyze_basic_clinical.py   │  Stratify all 15,446 terms into:
└─────────┬──────────────────────┘    basic / clinical / both
          │ 5,812 basic | 8,816 clinical | 818 both
          ▼
┌──────────────────────────────────┐
│ 4. comprehensive_analysis.py    │  3-D analysis:
└─────────┬────────────────────────┘    • Hotspots (2025–2026)
          │                             • Burst terms (first appearance 2025–2026)
          │                             • Evolution (2022–2026 trajectories)
          ▼
┌──────────────────────────────────┐
│ 5. basic_mechanism_analysis.py  │  Deep-dive into 5 basic-mechanism sub-layers
└─────────┬────────────────────────┘
          │
          ▼
     Figures & Reports
```

---

## Methods

### Data source
- **term-entropy.csv**: Term × year frequency matrix covering PubMed-indexed taVNS
  literature from 2002 through mid-2026.
- Each row is a term (n-gram); each column is a year; cells are occurrence counts.

### Filtering (Step 1)
- Removed 911 rows containing taVNS synonyms, abbreviations, and spelling variants
  (taVNS, tVNS, aVNS, transcutaneous auricular vagus nerve stimulation, etc.).
- Removed 5 function-word rows (tokenization artifacts: "a b s t r a c t" etc.).
- Result: **15,446 terms**.

### Semantic embedding (Step 2)
- **Model**: `all-MiniLM-L6-v2` (Sentence-BERT, 384-dimensional).
- Term strings (cleaned) were embedded into 384-D vectors.
- **UMAP**: Reduced to 2-D with `n_neighbors=15`, `min_dist=0.1`, `metric='cosine'`.
  UMAP preserves both local and global manifold structure, unlike t-SNE.
- **HDBSCAN**: Density-based clustering with `min_cluster_size=30`. No pre-specified
  number of clusters. Result: 14 major classes + noise.

### Basic vs. clinical stratification (Step 3)
- Keyword-driven rule-based classifier applied to all 15,446 terms.
- Assignment: `basic` (mechanistic, animal, molecular, imaging), `clinical` (trial,
  outcome, patient, surgery, disorder), or `both` (bridging terms).

### Three-dimensional analysis (Steps 4–5)
1. **Hotspots (2025–2026)**: Top terms by combined 2025+2026 frequency.
2. **Burst terms**: Terms with 0 occurrences in 2002–2024 that first appear in
   2025–2026 (i.e., research frontier emergence).
3. **Evolution (2022–2026)**: Trajectory analysis: growth rates, peak timing,
   and decline patterns across the recent 5-year window.

---

## Key findings

### 14 semantic clusters

| # | Cluster | Terms | Core semantics |
|:--:|---------|:-----:|----------------|
| 1 | Brain Regions & Circuits | 8,410 | Connectivity, electrophysiology, behavior, anatomy |
| 2 | Inflammation & Immunity | 1,248 | Cholinergic anti-inflammatory pathway, cytokines, α7nAChR |
| 3 | Noise | 1,470 | Cross-domain / transitional concepts |
| 4 | Stimulation Parameters & Devices | 698 | Parameters, devices, rTMS/tDCS comparison |
| 5 | Psychiatric & Emotional Disorders | 650 | Depression, anxiety, epilepsy, Parkinson's |
| 6 | Perioperative & Surgical | 628 | Postoperative delirium, pain, recovery |
| 7 | Autonomic & Cardiovascular | 615 | HRV, blood pressure, autonomic regulation |
| 8 | Clinical Trial Methodology | 456 | Sham stimulation, RCT, blinding |
| 9 | VNS Core Terms | 392 | taVNS vs. implantable VNS distinction |
| 10 | Stroke & Brain Injury | 278 | Ischemic/hemorrhagic stroke, TBI, plasticity |
| 11 | Animal Models | 199 | Rat/mouse models, behavioral tests |
| 12 | Cognitive Function | 147 | Neuromodulation techniques, BDNF |
| 13 | Neuroimaging | 130 | fNIRS, fMRI, DTI |
| 14 | Sleep Disorders | 125 | Sleep quality, insomnia, PSQI |

### 2025–2026 strongest rising signals (basic mechanism layer)

| Term | 2025 | 2026 | Biological meaning |
|------|:----:|:----:|--------------------|
| mediation analysis | 0 | 4 | Causal mechanism inference |
| brain-derived neurotrophic factor | 1 | 3 | Neurotrophin / plasticity marker |
| entorhinal cortex | 0 | 3 | Memory pathway target |
| auricular concha | 0 | 3 | Precise stimulation target |
| fNIRS | 1 | 2 | Portable neuroimaging |
| synaptic plasticity | 1 | 2 | Synaptic mechanism |
| macrophage polarization | 0 | 2 | Immune cell phenotype |
| glucagon-like peptide-1 | 0 | 2 | Gut-brain axis |
| parasympathetic reactivation | 0 | 2 | Autonomic recovery |
| oligodendrocyte precursor cells | 0 | 2 | Glial biology |

### 2025–2026 strongest rising signals (clinical layer)

| Term | 2025 | 2026 | Clinical meaning |
|------|:----:|:----:|-------------------|
| postoperative delirium | 5 | 6 | **Strongest new clinical signal** |
| postoperative recovery | 2 | 3 | Surgical recovery |
| perioperative anxiety | 1 | 3 | Preoperative anxiety |
| long COVID | 3 | 2 | Novel indication |
| breast cancer | 2 | 2 | Oncology expansion |
| insomnia severity index | 4 | 0 | Standardised sleep scale |

### 2022–2026 trajectory highlights
- **Continuous growth**: HRV, locus coeruleus, postoperative delirium
- **Peak at 2025**: Most terms show a 2025 publication surge, consistent with
  field-wide growth.
- **Declining**: Generic framework terms (e.g., "vagus nerve stimulation",
  "brain regions") → research specialization and terminology diversification.
- **Methodological maturation**: "mediation analysis" emerging in 2026 signals
  a shift from efficacy-only to mechanism-causal study designs.

---

## Dependencies

Managed with `uv`. Key packages:

```
pandas, numpy, scipy, scikit-learn
matplotlib
umap-learn, hdbscan
sentence-transformers (all-MiniLM-L6-v2)
torch
```

Install: `uv sync`

---

## Citation

Analysis performed in WispTerm. Data derived from PubMed-indexed taVNS literature
(2002–2026). Term extraction and entropy calculation by prior pipeline (see
`term-entropy.csv` metadata for details).
