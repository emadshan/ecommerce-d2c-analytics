from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
for f in sorted((ROOT/'data/raw').glob('*.csv')):
    d=pd.read_csv(f)
    print(f'{f.name:30} rows={len(d):>9,} duplicates={d.duplicated().sum():>6,} null_cells={d.isna().sum().sum():>7,}')
