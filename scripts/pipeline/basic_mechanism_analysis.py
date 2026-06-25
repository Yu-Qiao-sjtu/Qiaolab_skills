import pandas as pd
import numpy as np

df = pd.read_csv(r'D:\term\terms-clustered.csv')

# Define basic mechanism clusters
# Inflammation & Immunity: clusters 11 + 15
# Autonomic & Cardiovascular: clusters 5 + 8
# Stroke & Brain Injury: cluster 7
# Animal Models: cluster 3
# Cognitive Function: cluster 4

basic_clusters = {
    'Inflammation & Immunity': [11, 15],
    'Autonomic & Cardiovascular': [5, 8],
    'Stroke & Brain Injury': [7],
    'Animal Models': [3],
    'Cognitive Function': [4],
}

# Filter to basic mechanism terms only
basic_mask = df['MajorCluster'].isin([c for cl in basic_clusters.values() for c in cl])
basic_df = df[basic_mask].copy()

# Add sub-category label
def get_subcat(mc):
    for name, clusters in basic_clusters.items():
        if mc in clusters:
            return name
    return 'Other'

basic_df['SubCategory'] = basic_df['MajorCluster'].apply(get_subcat)

year_cols = [str(y) for y in range(2002, 2027)]

output_lines = []
output_lines.append("=" * 80)
output_lines.append("BASIC MECHANISM LAYER — THREE-DIMENSIONAL ANALYSIS")
output_lines.append("=" * 80)
output_lines.append("")

# ============================================================
# DIMENSION 1: 2025-2026 HOT TOPICS
# ============================================================
output_lines.append("─" * 80)
output_lines.append("DIMENSION 1: 2025–2026 RESEARCH HOTSPOTS")
output_lines.append("─" * 80)
output_lines.append("")

for cat_name, clusters in basic_clusters.items():
    cat_df = basic_df[basic_df['SubCategory'] == cat_name]
    total_terms = len(cat_df)
    active_25_26 = len(cat_df[cat_df['Total_2025_2026'] > 0])
    
    output_lines.append(f"### {cat_name}  ({total_terms} terms, {active_25_26} active in 2025-2026)")
    output_lines.append("")
    output_lines.append(f"{'Rank':<6} {'Term':<55} {'2025':>6} {'2026':>6} {'Total':>6}")
    output_lines.append("-" * 80)
    
    top_terms = cat_df.nlargest(20, 'Total_2025_2026')[['TERM', '2025', '2026', 'Total_2025_2026']]
    for i, (_, row) in enumerate(top_terms.iterrows(), 1):
        output_lines.append(f"{i:<6} {row['TERM']:<55} {int(row['2025']):>6} {int(row['2026']):>6} {int(row['Total_2025_2026']):>6}")
    
    output_lines.append("")
    output_lines.append("")

# ============================================================
# DIMENSION 2: BURST TERMS (first appeared in 2025-2026)
# ============================================================
output_lines.append("─" * 80)
output_lines.append("DIMENSION 2: BURST TERMS — First Appearance in 2025–2026")
output_lines.append("─" * 80)
output_lines.append("")

# Find burst terms: sum(2002..2024) == 0 and sum(2025,2026) > 0
year_cols_before = [str(y) for y in range(2002, 2025)]
basic_df['pre_2025_sum'] = basic_df[year_cols_before].sum(axis=1)
burst_df = basic_df[(basic_df['pre_2025_sum'] == 0) & (basic_df['Total_2025_2026'] > 0)]

# Count unique burst per category
burst_counts = burst_df['SubCategory'].value_counts()
output_lines.append(f"Total burst terms: {len(burst_df)}")
output_lines.append(f"  Basic Research overall: {len(burst_df)}")
output_lines.append("")

for cat_name in basic_clusters:
    cat_burst = burst_df[burst_df['SubCategory'] == cat_name]
    cnt = len(cat_burst)
    output_lines.append(f"  {cat_name}: {cnt}")
output_lines.append("")

for cat_name in basic_clusters:
    cat_burst = burst_df[burst_df['SubCategory'] == cat_name]
    if len(cat_burst) == 0:
        output_lines.append(f"### {cat_name}: NO burst terms")
        output_lines.append("")
        continue
    
    output_lines.append(f"### {cat_name} — Top Burst Terms (by 2025+2026 frequency)")
    output_lines.append("")
    output_lines.append(f"{'Term':<55} {'2025':>6} {'2026':>6} {'Total':>6}")
    output_lines.append("-" * 75)
    
    top_burst = cat_burst.nlargest(20, 'Total_2025_2026')[['TERM', '2025', '2026', 'Total_2025_2026']]
    for _, row in top_burst.iterrows():
        output_lines.append(f"{row['TERM']:<55} {int(row['2025']):>6} {int(row['2026']):>6} {int(row['Total_2025_2026']):>6}")
    
    output_lines.append("")

# ============================================================
# DIMENSION 3: 2022-2026 EVOLUTION
# ============================================================
output_lines.append("─" * 80)
output_lines.append("DIMENSION 3: 2022–2026 EVOLUTION TRENDS")
output_lines.append("─" * 80)
output_lines.append("")

# Overall yearly activity per category
output_lines.append("### Annual Active Terms per Category (2022–2026)")
output_lines.append("")
years_5 = ['2022', '2023', '2024', '2025', '2026']
header = f"{'Category':<35}"
for y in years_5:
    header += f" {y:>6}"
output_lines.append(header)
output_lines.append("-" * 70)

for cat_name in basic_clusters:
    cat_df = basic_df[basic_df['SubCategory'] == cat_name]
    line = f"{cat_name:<35}"
    for y in years_5:
        active = (cat_df[y] > 0).sum()
        line += f" {active:>6}"
    output_lines.append(line)

output_lines.append("")

# Top growing terms (2022-2024 avg vs 2025-2026 avg)
output_lines.append("### Top Growing Terms: 2022–2024 vs 2025–2026")
output_lines.append("(Δ = avg_2025_26 - avg_2022_24, min 5 occurrences in 2025-2026)")
output_lines.append("")

basic_df['avg_22_24'] = basic_df[['2022','2023','2024']].mean(axis=1)
basic_df['avg_25_26'] = basic_df[['2025','2026']].mean(axis=1)
basic_df['delta'] = basic_df['avg_25_26'] - basic_df['avg_22_24']

growing = basic_df[basic_df['Total_2025_2026'] >= 5].nlargest(30, 'delta')

output_lines.append(f"{'Term':<55} {'2022':>5} {'2023':>5} {'2024':>5} {'2025':>5} {'2026':>5} {'Avg22-24':>9} {'Avg25-26':>9} {'Δ':>7} {'Category':>30}")
output_lines.append("-" * 140)

for _, row in growing.iterrows():
    output_lines.append(
        f"{row['TERM']:<55} {int(row['2022']):>5} {int(row['2023']):>5} {int(row['2024']):>5} "
        f"{int(row['2025']):>5} {int(row['2026']):>5} {row['avg_22_24']:>9.2f} {row['avg_25_26']:>9.2f} "
        f"{row['delta']:>7.2f} {row['SubCategory']:>30}"
    )

output_lines.append("")

# Top declining terms
output_lines.append("### Top Declining Terms: 2022–2024 vs 2025–2026")
output_lines.append("(Δ = avg_2025_26 - avg_2022_24, min 5 occurrences in 2022-2024)")
output_lines.append("")

basic_df['total_22_24'] = basic_df[['2022','2023','2024']].sum(axis=1)
declining = basic_df[basic_df['total_22_24'] >= 5].nsmallest(30, 'delta')

output_lines.append(f"{'Term':<55} {'2022':>5} {'2023':>5} {'2024':>5} {'2025':>5} {'2026':>5} {'Avg22-24':>9} {'Avg25-26':>9} {'Δ':>7} {'Category':>30}")
output_lines.append("-" * 140)

for _, row in declining.iterrows():
    output_lines.append(
        f"{row['TERM']:<55} {int(row['2022']):>5} {int(row['2023']):>5} {int(row['2024']):>5} "
        f"{int(row['2025']):>5} {int(row['2026']):>5} {row['avg_22_24']:>9.2f} {row['avg_25_26']:>9.2f} "
        f"{row['delta']:>7.2f} {row['SubCategory']:>30}"
    )

output_lines.append("")
output_lines.append("")

# Year-by-year of key terms per category
output_lines.append("### Key Terms Year-by-Year Trajectory (2022→2026)")
output_lines.append("")

for cat_name in basic_clusters:
    cat_df = basic_df[basic_df['SubCategory'] == cat_name]
    key_terms = cat_df.nlargest(8, 'Total_2025_2026')
    
    output_lines.append(f"#### {cat_name}")
    output_lines.append("")
    output_lines.append(f"{'Term':<50} {'2022':>5} {'2023':>5} {'2024':>5} {'2025':>5} {'2026':>5} {'Trend':>10}")
    output_lines.append("-" * 90)
    
    for _, row in key_terms.iterrows():
        y22, y23, y24, y25, y26 = int(row['2022']), int(row['2023']), int(row['2024']), int(row['2025']), int(row['2026'])
        avg_early = (y22+y23+y24)/3 if (y22+y23+y24) > 0 else 0
        avg_late = (y25+y26)/2 if (y25+y26) > 0 else 0
        if avg_late > avg_early + 1:
            trend = "↑ RISING"
        elif avg_late < avg_early - 1:
            trend = "↓ FALLING"
        elif y25 == 0 and y26 == 0:
            trend = "· GONE"
        elif (y22+y23+y24) == 0:
            trend = "⚡ NEW"
        else:
            trend = "→ STABLE"
        
        output_lines.append(f"{row['TERM']:<50} {y22:>5} {y23:>5} {y24:>5} {y25:>5} {y26:>5} {trend:>10}")
    
    output_lines.append("")

# ============================================================
# Save report
# ============================================================
report_text = "\n".join(output_lines)
with open(r'D:\term\basic-mechanism-report.txt', 'w', encoding='utf-8') as f:
    f.write(report_text)

print("Report saved to D:\\term\\basic-mechanism-report.txt")
print(f"Total basic mechanism terms analyzed: {len(basic_df)}")
print(f"Burst terms (new in 2025-2026): {len(burst_df)}")

# Also save burst terms CSV
burst_df[['TERM', 'SubCategory', '2025', '2026', 'Total_2025_2026']].to_csv(
    r'D:\term\basic-mechanism-burst.csv', index=False, encoding='utf-8-sig'
)
print("Burst terms CSV saved to D:\\term\\basic-mechanism-burst.csv")
