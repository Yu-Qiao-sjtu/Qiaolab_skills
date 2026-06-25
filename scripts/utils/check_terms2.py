import pandas as pd

df = pd.read_csv('D:/term/terms-clustered.csv')
print("Columns:", df.columns.tolist())

terms = ['oxidative stress','traumatic brain injury','synaptic plasticity','bdnf level','transcriptomic analysis',
         'noninvasive neuromodulation technique','macrophage polarization','glucagon-like peptide-1',
         'immune-inflammatory responses','remote ischemic conditioning']
for t in terms:
    row = df[df['TERM'].str.lower() == t.lower()]
    if len(row) > 0:
        maj = row.iloc[0].get('MajorCluster', '?')
        minc = row.iloc[0].get('MinorCluster', '?')
        sub = row.iloc[0].get('SubCategory', '?')
        print(f'\n{t}: MajorCluster={maj}, MinorCluster={minc}, SubCategory={sub}')
        for c in ['2025','2026']:
            if c in df.columns:
                print(f'  {c}={row.iloc[0][c]}')
    else:
        print(f'\n{t}: NOT FOUND')
