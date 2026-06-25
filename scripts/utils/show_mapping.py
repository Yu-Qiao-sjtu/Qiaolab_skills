import pandas as pd
df = pd.read_csv(r'D:\term\data\clustering\terms-clustered.csv')
mapping = df[['MajorCluster','MajorName']].drop_duplicates().sort_values('MajorCluster')
mapping.to_csv(r'D:\term\data\processed\major_cluster_names.csv', index=False)
for _, r in mapping.iterrows():
    print(f'{r.MajorCluster:3d} -> {r.MajorName}')
