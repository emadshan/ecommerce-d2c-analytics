from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
d=pd.read_csv(ROOT/'data/raw/orders.csv',parse_dates=['order_date'])
d.groupby(d.order_date.dt.to_period('M')).size().plot(kind='line',title='Monthly order volume')
plt.ylabel('Orders'); plt.tight_layout(); plt.savefig(ROOT/'data/exports/monthly_orders.png',dpi=150)
print(d.describe(include='all').to_string())
