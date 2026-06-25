import csv
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('term-entropy-filtered.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# Clean header keys (strip whitespace, BOM already handled)
cleaned = []
for r in rows:
    nr = {}
    for k, v in r.items():
        nk = k.strip()
        if nk == '\ufeffTERM':
            nk = 'TERM'
        nr[nk] = v.strip()
    cleaned.append(nr)

rows = cleaned

# Filter: terms with non-zero in 2025 or 2026
y2025_2026 = []
for r in rows:
    val25 = int(r.get('2025', '0') or '0')
    val26 = int(r.get('2026', '0') or '0')
    if val25 > 0 or val26 > 0:
        y2025_2026.append((r['TERM'], val25, val26, val25 + val26, float(r.get('Entropy', '0') or '0')))

# Sort by total descending
y2025_2026.sort(key=lambda x: x[3], reverse=True)

print(f'Terms appearing in 2025-2026: {len(y2025_2026)}')

# Summary stats
only_25 = sum(1 for t, v25, v26, tot, e in y2025_2026 if v25 > 0 and v26 == 0)
only_26 = sum(1 for t, v25, v26, tot, e in y2025_2026 if v25 == 0 and v26 > 0)
both = sum(1 for t, v25, v26, tot, e in y2025_2026 if v25 > 0 and v26 > 0)
print(f'  Only 2025: {only_25}')
print(f'  Only 2026: {only_26}')
print(f'  Both years: {both}')
print()

print(f'{"TERM":<60} {"2025":>6} {"2026":>6} {"Total":>6} {"Entropy":>8}')
print('-' * 90)

for term, v25, v26, tot, ent in y2025_2026[:100]:
    print(f'{term:<60} {v25:>6} {v26:>6} {tot:>6} {ent:>8.3f}')

# Also save full list
with open('term-2025-2026.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['TERM', '2025', '2026', 'Total', 'Entropy'])
    for term, v25, v26, tot, ent in y2025_2026:
        writer.writerow([term, v25, v26, tot, f'{ent:.4f}'])

print(f'\nFull list saved to term-2025-2026.csv ({len(y2025_2026)} rows)')
