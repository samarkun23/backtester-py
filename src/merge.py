import pandas as pd
import glob

# ============================================
# 1. LOAD ALL FILES
# ============================================
files = glob.glob('data/DAT_ASCII_EURUSD_M1_*.csv')
files.sort()

print(f"Found {len(files)} files:")
for f in files:
    print(f"  - {f}")

dfs = []

for file in files:
    # No header, semicolon separated, 6 columns
    df = pd.read_csv(file, sep=';', header=None)
    
    # Column mapping (Date+Time combined in Col 0)
    df.columns = ['DateTime', 'Open', 'High', 'Low', 'Close', 'Volume']
    
    dfs.append(df)
    print(f"Loaded {file}: {len(df)} rows")

# Merge all years
df_all = pd.concat(dfs, ignore_index=True)
print(f"\nTotal M1 rows: {len(df_all)}")

# ============================================
# 2. PARSE DATETIME (combined column)
# ============================================
# Format: "20220102 170300" → YYYYMMDD HHMMSS
df_all['Datetime'] = pd.to_datetime(df_all['DateTime'], format='%Y%m%d %H%M%S')
df_all.set_index('Datetime', inplace=True)
df_all.drop('DateTime', axis=1, inplace=True)

# Convert price columns to float
for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
    df_all[col] = pd.to_numeric(df_all[col], errors='coerce')

# Sort by time
df_all.sort_index(inplace=True)

# Remove duplicates (if any)
df_all = df_all[~df_all.index.duplicated(keep='first')]

print(f"Date range: {df_all.index[0]} to {df_all.index[-1]}")

# ============================================
# 3. RESAMPLE TO H1
# ============================================
df_h1 = df_all.resample('1h').agg({
    'Open': 'first',
    'High': 'max',
    'Low': 'min',
    'Close': 'last',
    'Volume': 'sum'
})

# Drop NaN bars (weekends/holidays)
df_h1.dropna(inplace=True)

# Remove weekends
df_h1 = df_h1[df_h1.index.dayofweek < 5]

print(f"H1 bars after cleanup: {len(df_h1)}")

# ============================================
# 4. SAVE
# ============================================
# Save with proper DateTime column for backtester
df_h1.to_csv('data/EURUSD_H1.csv', date_format='%Y-%m-%d %H:%M:%S')
print(f"\n✅ Saved: data/EURUSD_H1.csv")
print(f"   Columns: {list(df_h1.columns)}")
print(f"   Sample:")
print(df_h1.head(3))

# import pandas as pd

# # Pehli file load kar bina header ke, dekh kitne columns hain
# df = pd.read_csv('data/DAT_ASCII_EURUSD_M1_2022.csv', sep=';', header=None)
# print(f"Number of columns: {df.shape[1]}")
# print(f"\nFirst 2 rows:")
# print(df.head(2))
# print(f"\nColumn values sample:")
# for i in range(df.shape[1]):
#     print(f"  Col {i}: {df.iloc[0, i]}")