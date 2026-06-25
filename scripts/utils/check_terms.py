import pandas as pd
df = pd.read_csv('terms-classified.csv')
df_basic = df[df['Category'].isin(['basic','both'])].copy()
yr_old = ['2022','2023','2024']
df_basic['old_sum'] = df_basic[yr_old].sum(axis=1)
df_basic['new_sum'] = df_basic['2025'] + df_basic['2026']
rising = df_basic[(df_basic['old_sum'] == 0) & (df_basic['2026'] > df_basic['2025']) & (df_basic['new_sum'] > 0)].copy()
rising = rising.sort_values('new_sum', ascending=False)
remove = {'central mechanism','expression level','protein level','brain tissue',
          'enhancing cognitive function','event segmentation','inflammatory disease',
          'ongoing event representation','transcriptomic analysis','immunofluorescence staining',
          'behavioral test','western blot analysis','statistical analysis','control group',
          'experimental group','significant difference','significant increase',
          'significant decrease','significant effect','no significant difference'}
rising_clean = rising[~rising['TERM'].str.lower().isin([r.lower() for r in remove])]
top = rising_clean.head(15)
for _, r in top.iterrows():
    print(f"{r['TERM']:55s} | 25={int(r['2025'])} | 26={int(r['2026'])}")
print(f"\nTotal rising (clean): {len(rising_clean)}")
