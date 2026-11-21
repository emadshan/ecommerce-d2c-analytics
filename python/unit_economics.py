from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
o=pd.read_csv(ROOT/'data/raw/orders.csv')
r=pd.read_csv(ROOT/'data/raw/returns.csv')
d=o[o.order_status.eq('delivered')].copy()
refund=r.groupby('order_id').refund_amount_inr.sum()
d['refund']=d.order_id.map(refund).fillna(0)
d['net_sales']=d.order_value_inr/1.05-d.refund/1.05
d['contribution']=d.net_sales-d.estimated_cogs_inr-d.shipping_fee_inr-65
d.to_csv(ROOT/'data/exports/order_contribution.csv',index=False)
