"""Run the portfolio analysis end-to-end on generated CSVs."""
from pathlib import Path
import json, warnings
import numpy as np, pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, classification_report
from scipy.stats import chi2_contingency, norm, chisquare

ROOT=Path(__file__).resolve().parents[1]; RAW=ROOT/"data/raw"; OUT=ROOT/"data/exports"; PROC=ROOT/"data/processed"
OUT.mkdir(parents=True,exist_ok=True); PROC.mkdir(parents=True,exist_ok=True)
def read(name,dates=None): return pd.read_csv(RAW/f"{name}.csv",parse_dates=dates or [])
def main():
    orders=read("orders",["order_date"]); customers=read("customers",["created_at"]); events=read("events",["event_timestamp","ingested_at"])
    items=read("order_items"); returns=read("returns",["return_date"]); spend=read("daily_ad_spend",["spend_date"])
    exp=read("experiment_assignments",["assigned_at"])
    # Quality profile before cleaning.
    quality=[]
    for name in ["customers","products","orders","order_items","returns","events","campaigns","daily_ad_spend","experiment_assignments"]:
        df=pd.read_csv(RAW/f"{name}.csv")
        quality.append({"table":name,"rows":len(df),"duplicate_rows":int(df.duplicated().sum()),"null_cells":int(df.isna().sum().sum())})
    pd.DataFrame(quality).to_csv(OUT/"data_quality_profile.csv",index=False)
    events=events[~events.is_bot.astype(str).str.lower().isin(["true","1"])].drop_duplicates(["session_id","event_name","event_timestamp"])
    delivered=orders[orders.order_status=="delivered"].copy()
    ret=returns.groupby("order_id").refund_amount_inr.sum()
    delivered["refund_inr"]=delivered.order_id.map(ret).fillna(0)
    delivered["net_sales_inr"]=delivered.order_value_inr/1.05-delivered.refund_inr/1.05
    delivered["contribution_inr"]=delivered.net_sales_inr-delivered.estimated_cogs_inr-delivered.shipping_fee_inr-65
    delivered["month"]=delivered.order_date.dt.to_period("M").astype(str)
    kpis=pd.DataFrame([{
        "orders":len(orders),"delivered_orders":len(delivered),"rto_rate":(orders.delivery_outcome=="RTO").mean(),
        "gross_order_value_inr":orders.order_value_inr.sum(),"net_sales_inr":delivered.net_sales_inr.sum(),
        "contribution_inr":delivered.contribution_inr.sum(),"contribution_margin_pct":delivered.contribution_inr.sum()/max(delivered.net_sales_inr.sum(),1),
        "aov_inr":orders.order_value_inr.mean(),"return_rate":len(returns)/max(len(delivered),1)
    }])
    kpis.to_csv(OUT/"executive_kpis.csv",index=False)
    # Funnel by device from clean events.
    funnel=events.groupby(["device","event_name"]).session_id.nunique().unstack(fill_value=0)
    funnel.to_csv(OUT/"funnel_by_device.csv")
    # Cohort retention: repeat active purchase in month offsets.
    cust_order=delivered[["customer_id","order_date"]].copy()
    cust_order["month"]=cust_order.order_date.dt.to_period("M")
    first=cust_order.groupby("customer_id").month.min().rename("cohort")
    cust_order=cust_order.join(first,on="customer_id")
    cust_order["month_n"]=(cust_order.month.dt.year-cust_order.cohort.dt.year)*12+(cust_order.month.dt.month-cust_order.cohort.dt.month)
    cohorts=cust_order.groupby(["cohort","month_n"]).customer_id.nunique().rename("customers").reset_index()
    sizes=first.groupby(first).size()
    cohorts["cohort_size"]=cohorts.cohort.map(sizes); cohorts["retention"]=cohorts.customers/cohorts.cohort_size
    cohorts.to_csv(OUT/"cohort_retention.csv",index=False)
    # RFM + K-means.
    ref=delivered.order_date.max()+pd.Timedelta(days=1)
    rfm=delivered.groupby("customer_id").agg(last_order=("order_date","max"),frequency=("order_id","nunique"),monetary=("order_value_inr","sum"))
    rfm["recency_days"]=(ref-rfm.last_order).dt.days
    features=np.log1p(rfm[["recency_days","frequency","monetary"]].clip(lower=0))
    if len(features)>=4:
        X=StandardScaler().fit_transform(features)
        rfm["segment"]=KMeans(n_clusters=4,random_state=20261121,n_init=10).fit_predict(X)
    else: rfm["segment"]=0
    rfm.reset_index().to_csv(OUT/"rfm_segments.csv",index=False)
    # Channel economics / last-touch and first-touch sensitivities.
    channel_orders=delivered.groupby("channel").agg(customers=("customer_id","nunique"),orders=("order_id","nunique"),revenue=("net_sales_inr","sum")).reset_index()
    spend_ch=spend.merge(read("campaigns"),on="campaign_id").groupby("channel").spend_inr.sum()
    channel_orders["spend_inr"]=channel_orders.channel.map(spend_ch).fillna(0)
    channel_orders["cac_inr"]=channel_orders.spend_inr/channel_orders.customers.clip(lower=1)
    channel_orders["roas"]=channel_orders.revenue/channel_orders.spend_inr.replace(0,np.nan)
    repeat_by_channel=delivered.groupby("channel").customer_id.agg(lambda s:(s.value_counts()>=2).mean())
    channel_orders["repeat_customer_share"]=channel_orders.channel.map(repeat_by_channel)
    channel_orders.to_csv(OUT/"channel_economics.csv",index=False)
    # Attribution models: first, last, linear and position-based on event paths.
    paths=events.sort_values("event_timestamp").groupby("session_id").channel.agg(list)
    attrib=[]
    for model in ["first_touch","last_touch","linear","position_based"]:
        credit={}
        for path in paths:
            uniq=path
            if not uniq: continue
            if model=="first_touch": alloc={uniq[0]:1}
            elif model=="last_touch": alloc={uniq[-1]:1}
            elif model=="linear": alloc={x:1/len(uniq) for x in uniq}
            else:
                alloc={}
                if len(uniq)==1: alloc[uniq[0]]=1
                else:
                    alloc[uniq[0]]=0.4; alloc[uniq[-1]]=0.4
                    for x in uniq[1:-1]: alloc[x]=alloc.get(x,0)+0.2/(len(uniq)-2) if len(uniq)>2 else 0
            for c,v in alloc.items(): credit[c]=credit.get(c,0)+v
        for c,v in credit.items(): attrib.append((model,c,v))
    pd.DataFrame(attrib,columns=["model","channel","credited_sessions"]).to_csv(OUT/"attribution_comparison.csv",index=False)
    # Tier x payment RTO.
    rto=orders.groupby(["city_tier","payment_method"]).delivery_outcome.apply(lambda s:(s=="RTO").mean()).rename("rto_rate").reset_index()
    rto.to_csv(OUT/"rto_by_tier_payment.csv",index=False)
    # Monthly P&L proxy.
    pnl=delivered.groupby("month").agg(net_sales=("net_sales_inr","sum"),cogs=("estimated_cogs_inr","sum"),shipping=("shipping_fee_inr","sum"),orders=("order_id","nunique"),contribution=("contribution_inr","sum")).reset_index()
    pnl["marketing_spend"]=pnl.month.map(spend.assign(month=spend.spend_date.dt.to_period("M").astype(str)).groupby("month").spend_inr.sum()).fillna(0)
    pnl["contribution_after_marketing"]=pnl.contribution-pnl.marketing_spend
    pnl.to_csv(OUT/"monthly_pnl.csv",index=False)
    # Experiments: two-proportion z-test, SRM chi-square and guardrail.
    reads=[]
    for eid,g in exp.groupby("experiment_id"):
        counts=g.groupby("variant").agg(n=("customer_id","count"),conv=("converted","sum"),guard=("refund_or_complaint","sum"))
        c=counts.loc["control"]; t=counts.loc["treatment"]
        p1=c.conv/c.n; p2=t.conv/t.n; pooled=(c.conv+t.conv)/(c.n+t.n)
        se=np.sqrt(pooled*(1-pooled)*(1/c.n+1/t.n))
        z=(p2-p1)/se if se else 0; p=2*(1-norm.cdf(abs(z)))
        diff=p2-p1; ci=(diff-1.96*np.sqrt(p1*(1-p1)/c.n+p2*(1-p2)/t.n),diff+1.96*np.sqrt(p1*(1-p1)/c.n+p2*(1-p2)/t.n))
        chi=chisquare([c.n,t.n],f_exp=[(c.n+t.n)/2,(c.n+t.n)/2]).pvalue
        gdiff=t.guard/t.n-c.guard/c.n
        mde80=(1.96+0.84)*np.sqrt(2*pooled*(1-pooled)/min(c.n,t.n))
        if gdiff>0.003:
            decision="KILL"
        elif diff>0 and p<0.05:
            decision="SHIP"
        else:
            decision="ITERATE"
        reads.append({"experiment_id":eid,"control_n":c.n,"treatment_n":t.n,"approx_mde_80pct":mde80,"control_conversion":p1,"treatment_conversion":p2,"absolute_lift":diff,"p_value":p,"ci_low":ci[0],"ci_high":ci[1],"guardrail_delta":gdiff,"srm_p_value":chi,"decision":decision})
    pd.DataFrame(reads).to_csv(OUT/"experiment_readouts.csv",index=False)
    # Lean repeat purchase classifier using first order cohort-level features.
    first_orders=delivered.sort_values("order_date").groupby("customer_id").first()
    order_counts=delivered.groupby("customer_id").order_id.nunique()
    cust=first_orders[["order_date","order_value_inr","channel","device","payment_method","city_tier"]].copy()
    cust["repeat"]=(order_counts.reindex(cust.index).fillna(0)>=2).astype(int)
    if len(cust)>50 and cust.repeat.nunique()>1:
        X=pd.get_dummies(cust[["channel","device","payment_method","city_tier"]],drop_first=True,dtype=float)
        X["first_month"]=cust.order_date.dt.month
        X["first_order_value"]=cust.order_value_inr
        Xtr,Xte,ytr,yte=train_test_split(X,cust.repeat,test_size=.25,random_state=20261121,stratify=cust.repeat)
        model=LogisticRegression(max_iter=500).fit(Xtr,ytr); pred=model.predict_proba(Xte)[:,1]
        score=roc_auc_score(yte,pred)
        pd.DataFrame({"feature":X.columns,"coefficient":model.coef_[0]}).to_csv(OUT/"repeat_model_coefficients.csv",index=False)
        (OUT/"repeat_model_metrics.json").write_text(json.dumps({"roc_auc":score,"n_test":len(yte)},indent=2))
    # Monthly demand forecast: seasonal-naive baseline plus 3-month moving average.
    monthly=orders.groupby(orders.order_date.dt.to_period("M").astype(str)).size().rename("orders").reset_index()
    monthly.columns=["month","orders"]
    monthly["forecast_next_month"]=monthly.orders.tail(3).mean()
    monthly.to_csv(OUT/"monthly_demand_forecast.csv",index=False)
    print("Analytics complete. Exports:",OUT)
if __name__=="__main__": main()
