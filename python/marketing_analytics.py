from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
o=pd.read_csv(ROOT/'data/raw/orders.csv')
s=pd.read_csv(ROOT/'data/raw/daily_ad_spend.csv')
c=pd.read_csv(ROOT/'data/raw/campaigns.csv')
sp=s.merge(c,on='campaign_id').groupby('channel').spend_inr.sum()
acq=o.groupby('channel').customer_id.nunique()
out=pd.DataFrame({'spend_inr':sp,'acquired_customers':acq}).fillna(0)
out['cac_inr']=out.spend_inr/out.acquired_customers.clip(lower=1)
out.to_csv(ROOT/'data/exports/marketing_channel_summary.csv')
