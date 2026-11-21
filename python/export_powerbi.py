from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/'data/raw'; SRC=ROOT/'data/exports'; DST=SRC/'powerbi'; DST.mkdir(exist_ok=True)
# Build a star-schema-friendly order fact with finance fields used by DAX.
orders=pd.read_csv(RAW/'orders.csv')
returns=pd.read_csv(RAW/'returns.csv')
refunds=returns.groupby('order_id').refund_amount_inr.sum()
orders['refund_inr']=orders.order_id.map(refunds).fillna(0)
delivered=orders.order_status.eq('delivered')
orders['net_sales_inr']=0.0
orders.loc[delivered,'net_sales_inr']=orders.loc[delivered,'order_value_inr']/1.05-orders.loc[delivered,'refund_inr']/1.05
orders['contribution_inr']=orders.net_sales_inr-orders.estimated_cogs_inr-orders.shipping_fee_inr-65
orders.to_csv(DST/'Orders.csv',index=False)
returns.to_csv(DST/'Returns.csv',index=False)
spend=pd.read_csv(RAW/'daily_ad_spend.csv')
spend.to_csv(DST/'Spend.csv',index=False)
products=pd.read_csv(RAW/'products.csv')
products.to_csv(DST/'Products.csv',index=False)
customers=pd.read_csv(RAW/'customers.csv')
customers.to_csv(DST/'Customers.csv',index=False)
for name in ['executive_kpis','funnel_by_device','cohort_retention','rfm_segments','channel_economics','monthly_pnl','rto_by_tier_payment','experiment_readouts','attribution_comparison','monthly_demand_forecast']:
    f=SRC/f'{name}.csv'
    if f.exists(): pd.read_csv(f).to_csv(DST/f'{name}.csv',index=False)
print('Power BI model tables and analytical exports:',DST)
