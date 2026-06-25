import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 12

df = pd.read_csv('D:/term/basic-mechanism-burst.csv')

# Get top burst terms: total >= 2, sorted by total desc, then pick top 15 or so
burst = df[df['Total_2025_2026'] >= 2].copy()
burst = burst.sort_values('Total_2025_2026', ascending=False)

# Print all for selection
print(f"Total burst terms with >=2: {len(burst)}")
for i, row in burst.iterrows():
    print(f"  {row['TERM']} | {row['SubCategory']} | 2025={row['2025']} | 2026={row['2026']} | total={row['Total_2025_2026']}")
