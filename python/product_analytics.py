from pathlib import Path
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
ROOT=Path(__file__).resolve().parents[1]
o=pd.read_csv(ROOT/'data/raw/orders.csv',parse_dates=['order_date'])
d=o[o.order_status.eq('delivered')]
rfm=d.groupby('customer_id').agg(recency=('order_date',lambda s:(d.order_date.max()-s.max()).days),frequency=('order_id','nunique'),monetary=('order_value_inr','sum'))
rfm['cluster']=KMeans(n_clusters=4,random_state=20261121,n_init=10).fit_predict(StandardScaler().fit_transform(rfm))
rfm.to_csv(ROOT/'data/exports/rfm_kmeans.csv')
