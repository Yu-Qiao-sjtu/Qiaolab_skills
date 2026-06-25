import pandas as pd

df = pd.read_csv('terms-clustered.csv')
mapping = df[['MajorCluster','MajorName']].drop_duplicates().sort_values('MajorCluster')
for _, row in mapping.iterrows():
    print(row['MajorCluster'], '->', row['MajorName'])
print('---')
print('Columns with UMAP:', [c for c in df.columns if 'UMAP' in c.upper()])
