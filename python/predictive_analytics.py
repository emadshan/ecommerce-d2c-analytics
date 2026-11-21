from pathlib import Path
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
ROOT=Path(__file__).resolve().parents[1]
d=pd.read_csv(ROOT/'data/raw/orders.csv',parse_dates=['order_date'])
d=d[d.order_status.eq('delivered')].sort_values('order_date')
first=d.groupby('customer_id').first()
counts=d.groupby('customer_id').order_id.nunique()
first['repeat']=(counts.reindex(first.index).fillna(0)>=2).astype(int)
X=pd.get_dummies(first[['channel','device','payment_method','city_tier']],drop_first=True,dtype=float)
X['first_month']=first.order_date.dt.month
X['first_order_value']=first.order_value_inr
if first.repeat.nunique()>1:
    a,b,y,z=train_test_split(X,first.repeat,test_size=.25,random_state=20261121,stratify=first.repeat)
    m=LogisticRegression(max_iter=500).fit(a,y)
    print('ROC-AUC:',round(roc_auc_score(z,m.predict_proba(b)[:,1]),3))
    print('Model uses only first-order features; repeat label is subsequent order observed in dataset.')
