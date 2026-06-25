import pandas as pd, numpy as np

df = pd.read_csv('terms-classified.csv')

# Basic mechanism: basic or both
df_basic = df[df['Category'].isin(['basic','both'])].copy()

# Years
yr_cols = [str(y) for y in range(2002,2027)]

# Rising: 2022-2024 all zero, 2026 > 2025, and 2025+2026 > 0
yr_old = ['2022','2023','2024']
df_basic['old_sum'] = df_basic[yr_old].sum(axis=1)
df_basic['new_sum'] = df_basic['2025'] + df_basic['2026']

rising = df_basic[(df_basic['old_sum'] == 0) & (df_basic['2026'] > df_basic['2025']) & (df_basic['new_sum'] > 0)].copy()
rising = rising.sort_values('new_sum', ascending=False)

# Top 20
top = rising.head(20)
for _, r in top.iterrows():
    print(f"{r['TERM']:50s} | 2025={int(r['2025'])} | 2026={int(r['2026'])} | total={int(r['new_sum'])} | cat={r['Category']}")

print(f'\nTotal rising signals in basic: {len(rising)}')
