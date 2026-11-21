from pathlib import Path
import pandas as pd
from scipy.stats import chi2_contingency
ROOT=Path(__file__).resolve().parents[1]
d=pd.read_csv(ROOT/'data/raw/experiment_assignments.csv')
for name,g in d.groupby('experiment_id'):
    print(name, g.groupby('variant').agg(n=('customer_id','size'),conversion=('converted','mean'),guardrail=('refund_or_complaint','mean')))
    print('SRM chi-square p:',chi2_contingency(pd.crosstab(g.variant,g.variant))[1])
