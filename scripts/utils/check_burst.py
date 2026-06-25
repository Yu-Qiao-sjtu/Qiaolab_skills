import pandas as pd
df = pd.read_csv('D:/term/basic-mechanism-burst.csv')
cols = df.columns.tolist()
print('Columns:', cols)
terms = ['oxidative stress','traumatic brain injury','macrophage polarization',
         'immune-inflammatory responses','remote ischemic conditioning',
         'closed-loop neurostimulation','entorhinal cortex','synaptic plasticity',
         'myocardial infarction','continuous glucose monitoring','chronic heart failure']
for t in terms:
    row = df[df['TERM'].str.strip().str.lower() == t.lower()]
    if len(row) > 0:
        r = row.iloc[0]
        print(f"{t}: 2025={r['2025']}, 2026={r['2026']}, total={r['Total_2025_2026']}")
    else:
        print(f"{t}: NOT FOUND")
