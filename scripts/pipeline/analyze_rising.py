import pandas as pd

df = pd.read_csv('D:/term/terms-clustered.csv')

# Check major cluster names for interesting IDs
for mc in [15, 7, 4, 11]:
    names = df[df['MajorCluster'] == mc]['MajorName'].unique()
    print(f'MajorCluster {mc}: {names} (count={len(df[df["MajorCluster"]==mc])})')

print()

# Now find truly rising burst terms from basic-mechanism-burst
burst = pd.read_csv('D:/term/basic-mechanism-burst.csv')
rising = burst[burst['2026'] >= burst['2025']].copy()
rising = rising.sort_values('Total_2025_2026', ascending=False)

# Show top 20, filtering out clearly bogus ones
print("Top 30 rising burst terms in basic mechanism:")
for i, row in rising.head(30).iterrows():
    print(f"  {row['TERM']:50s} | {row['SubCategory']:30s} | 2025={row['2025']} | 2026={row['2026']} | Total={row['Total_2025_2026']}")
