import pandas as pd

df = pd.read_csv('data/processed/terms-classified.csv')

print("Columns:", list(df.columns))
print("\nEntropy stats:")
print(df['Entropy'].describe())
print("\nCategory value counts:")
print(df['Category'].value_counts())
print()

# Basic research + high entropy (top 40)
basic = df[df['Category'] == 'basic'].copy()
basic_sorted = basic.sort_values('Entropy', ascending=False)
basic_high = basic_sorted.head(40)

print("Top 40 basic research terms by entropy:")
print(f"{'Rank':<5} {'Entropy':<8} {'Term'}")
print("-" * 60)
for i, (_, row) in enumerate(basic_high.iterrows(), 1):
    print(f"{i:<5} {row['Entropy']:.4f}  {row['TERM']}")

# Also show the years distribution for the top 5
print("\n\n--- Top 5 high-entropy basic terms: year-by-year ---")
year_cols = [str(y) for y in range(2002, 2027)]
for _, row in basic_high.head(5).iterrows():
    print(f"\n{row['TERM']} (Entropy={row['Entropy']:.4f}):")
    yearly = {y: row[y] for y in year_cols if y in df.columns and pd.notna(row.get(y)) and row[y] > 0}
    # Print compactly
    for y, v in yearly.items():
        print(f"  {y}: {int(v)}", end='')
    print()

# By major cluster
print("\n\n--- High-entropy basic terms by MajorCluster ---")
if 'MajorCluster' in df.columns:
    for cluster in basic_high['MajorCluster'].unique():
        subset = basic_high[basic_high['MajorCluster'] == cluster]
        print(f"\n  {cluster}:")
        for _, row in subset.iterrows():
            print(f"    {row['Entropy']:.4f}  {row['TERM']}")
