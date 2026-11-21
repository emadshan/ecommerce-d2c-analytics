"""Generate reproducible synthetic Indian D2C e-commerce data."""
from pathlib import Path
import argparse
import numpy as np
import pandas as pd

SEED = 20261121
START = "2025-05-01"
END = "2026-10-31"
OUT = Path(__file__).resolve().parents[1] / "data" / "raw"

CITIES = [
    ("Mumbai","Maharashtra","400001","tier1"),("Delhi","Delhi","110001","tier1"),
    ("Bengaluru","Karnataka","560001","tier1"),("Hyderabad","Telangana","500001","tier1"),
    ("Chennai","Tamil Nadu","600001","tier1"),("Pune","Maharashtra","411001","tier1"),
    ("Kochi","Kerala","682001","tier2"),("Kozhikode","Kerala","673001","tier2"),
    ("Jaipur","Rajasthan","302001","tier2"),("Lucknow","Uttar Pradesh","226001","tier2"),
    ("Indore","Madhya Pradesh","452001","tier2"),("Coimbatore","Tamil Nadu","641001","tier2"),
    ("Guwahati","Assam","781001","tier2"),("Patna","Bihar","800001","tier2"),
    ("Alappuzha","Kerala","688001","tier3"),("Kannur","Kerala","670001","tier3"),
    ("Siliguri","West Bengal","734001","tier3"),("Gaya","Bihar","823001","tier3"),
    ("Udaipur","Rajasthan","313001","tier3"),("Mysuru","Karnataka","570001","tier3")
]
CHANNELS = ["paid_social","branded_search","nonbrand_search","organic","affiliate","marketplace","direct"]
PAYMENTS = ["COD","UPI","prepaid_card","netbanking"]
DEVICES = ["mobile","desktop","tablet"]
CATEGORIES = ["Womenwear","Menswear","Footwear","Accessories","Ethnicwear"]

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--orders",type=int,default=60000)
    p.add_argument("--seed",type=int,default=SEED)
    p.add_argument("--output",type=Path,default=OUT)
    a=p.parse_args()
    rng=np.random.default_rng(a.seed); out=a.output; out.mkdir(parents=True,exist_ok=True)
    n=a.orders
    dates=pd.date_range(START,END,freq="D")
    # Festive and sale-event seasonality.
    weights=np.ones(len(dates))
    for i,d in enumerate(dates):
        if d.month in [10,11]: weights[i]*=2.2
        if d.month in [5,8]: weights[i]*=1.35
        if d.day in [10,11,12,25,26]: weights[i]*=1.15
    weights/=weights.sum()
    order_dates=pd.to_datetime(rng.choice(dates.to_numpy(),size=n,p=weights))
    city_weights=np.array([.10,.09,.09,.07,.06,.06,.05,.05,.05,.05,.04,.04,.03,.03,.02,.02,.02,.02,.02,.02],dtype=float)
    city_weights=city_weights/city_weights.sum()
    city_idx=rng.choice(len(CITIES),n,p=city_weights)
    city_rows=[CITIES[i] for i in city_idx]
    city=np.array([x[0] for x in city_rows],object)
    state=np.array([x[1] for x in city_rows],object)
    pincode=np.array([x[2] for x in city_rows],object)
    tier=np.array([x[3] for x in city_rows],object)
    # Inconsistent spelling is deliberately present in raw customer records.
    city_raw=city.copy()
    for i in rng.choice(n,size=max(1,int(n*.012)),replace=False):
        city_raw[i] = {"Bengaluru":"Bangalore","Kozhikode":"Calicut","Mumbai":"MUMBAI"}.get(city[i],city[i]+" ")
    customers_n=max(12000,int(n*.58))
    customer_ids=np.array([f"C{x:06d}" for x in range(1,customers_n+1)])
    order_customer=rng.choice(customer_ids,n,replace=True)
    cust_first=pd.DataFrame({"customer_id":customer_ids})
    cust_city_idx=rng.integers(0,len(CITIES),customers_n)
    cust_first["city"]=[CITIES[i][0] for i in cust_city_idx]
    cust_first["state"]=[CITIES[i][1] for i in cust_city_idx]
    cust_first["pincode"]=[CITIES[i][2] for i in cust_city_idx]
    cust_first["city_tier"]=[CITIES[i][3] for i in cust_city_idx]
    cust_first["created_at"]=pd.to_datetime(START)+pd.to_timedelta(rng.integers(0,540,customers_n),unit="D")
    cust_first["acquisition_channel"]=rng.choice(CHANNELS,customers_n,p=[.25,.13,.12,.18,.07,.15,.10])
    cust_first["email_opt_in"]=rng.choice([True,False],customers_n,p=[.68,.32])
    cust_first["customer_city_raw"]=cust_first["city"]
    for i in rng.choice(customers_n,size=int(customers_n*.01),replace=False):
        cust_first.loc[i,"customer_city_raw"]=str(cust_first.loc[i,"city"])+" "
    cust_first.loc[rng.choice(customers_n,int(customers_n*.004),replace=False),"pincode"]=None
    # Acquisition mix is also the cohort source. Paid-social-acquired customers
    # are sampled more frequently to encode stronger repeat-purchase propensity.
    customer_weights=np.where(cust_first.acquisition_channel.eq("paid_social"),1.8,
                     np.where(cust_first.acquisition_channel.eq("branded_search"),0.8,1.0)).astype(float)
    customer_weights=customer_weights/customer_weights.sum()
    order_customer=rng.choice(customer_ids,n,replace=True,p=customer_weights)

    products_n=90
    products=pd.DataFrame({"product_id":[f"P{x:04d}" for x in range(1,products_n+1)]})
    products["product_name"]=[f"{rng.choice(['Everyday','Classic','Premium','Urban','Festive'])} {rng.choice(['Kurta','Tee','Dress','Sneaker','Shirt','Bag','Denim','Top'])} {i:02d}" for i in range(products_n)]
    products["category"]=rng.choice(CATEGORIES,products_n)
    products["mrp_inr"]=rng.choice([699,899,999,1299,1499,1799,2199,2499,2999,3499],products_n)
    products["unit_cost_inr"]=(products.mrp_inr*rng.uniform(.28,.43,products_n)).round(2)
    products["gst_rate"]=0.05
    products["active"]=True
    pmap=products.set_index("product_id")

    acq_map=cust_first.set_index("customer_id").acquisition_channel.to_dict()
    channel=np.array([acq_map[cid] for cid in order_customer],dtype=object)
    device=rng.choice(DEVICES,n,p=[.79,.18,.03])
    payment=rng.choice(PAYMENTS,n,p=[.42,.34,.20,.04])
    # tier-3 COD RTO elevated; prepaid lower.
    rto_prob=np.where(payment=="COD",np.where(tier=="tier3",.31,np.where(tier=="tier2",.22,.15)),.045)
    outcome=np.where(rng.random(n)<rto_prob,"RTO","delivered")
    status=np.where(outcome=="RTO","cancelled","delivered")
    festive=np.array([d.month in [10,11] for d in order_dates])
    discount=np.clip(rng.normal(np.where(festive,.27,.13),.08,n),0,.55)
    # GST-inclusive order item totals; 1-3 lines.
    line_counts=rng.choice([1,2,3],n,p=[.58,.32,.10])
    order_rows=[]; item_rows=[]
    for i in range(n):
        oid=f"O{i+1:07d}"; count=int(line_counts[i]); subtotal=0.; cost=0.
        for j in range(count):
            pi=int(rng.integers(0,products_n)); prod=products.iloc[pi]
            qty=int(rng.choice([1,1,1,2],p=[.55,.25,.15,.05]))
            unit=float(prod.mrp_inr); line_gross=unit*qty*(1-discount[i])
            line_cost=float(prod.unit_cost_inr)*qty
            subtotal+=line_gross; cost+=line_cost
            item_rows.append((f"{oid}-{j+1}",oid,prod.product_id,qty,unit,round(line_gross,2),round(line_cost,2)))
        shipping=0 if subtotal>=1499 else 79
        total=round(subtotal+shipping,2)
        order_rows.append((oid,order_customer[i],order_dates[i],channel[i],device[i],payment[i],status[i],outcome[i],
                           city[i],state[i],pincode[i],tier[i],round(discount[i],4),shipping,total,round(cost,2),
                           rng.choice(["website","marketplace"],p=[.72,.28]),rng.choice(["web","app"],p=[.74,.26])))
    orders=pd.DataFrame(order_rows,columns=["order_id","customer_id","order_date","channel","device","payment_method","order_status","delivery_outcome","city","state","pincode","city_tier","discount_rate","shipping_fee_inr","order_value_inr","estimated_cogs_inr","sales_platform","platform_type"])
    items=pd.DataFrame(item_rows,columns=["order_item_id","order_id","product_id","quantity","unit_price_inr","line_revenue_inr","line_cogs_inr"])
    # Campaigns and spend, with branded search capturing demand at low apparent CAC.
    campaigns=pd.DataFrame([
        ("CAM01","Meta prospecting","paid_social","prospecting"),
        ("CAM02","Google brand","branded_search","brand"),
        ("CAM03","Google nonbrand","nonbrand_search","prospecting"),
        ("CAM04","Affiliate partners","affiliate","partner"),
        ("CAM05","Marketplace ads","marketplace","marketplace")
    ],columns=["campaign_id","campaign_name","channel","campaign_type"])
    spend_rows=[]
    for d in dates:
        for _,c in campaigns.iterrows():
            base={"paid_social":65000,"branded_search":10000,"nonbrand_search":28000,"affiliate":9000,"marketplace":22000}[c.channel]
            season=1.6 if d.month in [10,11] else 1.0
            spend_rows.append((d,c.campaign_id,round(base*season*rng.uniform(.65,1.35),2),int(base/10*rng.uniform(.6,1.5))))
    spend=pd.DataFrame(spend_rows,columns=["spend_date","campaign_id","spend_inr","impressions"])
    # Returns: ~5.5% of delivered orders, delayed return timestamps.
    delivered=orders[orders.order_status=="delivered"]
    ret_mask=rng.random(len(delivered))<.055
    ret_orders=delivered.loc[ret_mask]
    returns=pd.DataFrame({
        "return_id":[f"R{x+1:06d}" for x in range(len(ret_orders))],
        "order_id":ret_orders.order_id.to_numpy(),
        "return_date":(pd.to_datetime(ret_orders.order_date).to_numpy()+pd.to_timedelta(rng.integers(3,25,len(ret_orders)),unit="D")),
        "return_reason":rng.choice(["size_issue","quality","changed_mind","damaged","late_delivery"],len(ret_orders),p=[.42,.22,.18,.08,.10]),
        "refund_amount_inr":(ret_orders.order_value_inr.to_numpy()*rng.uniform(.45,1,len(ret_orders))).round(2),
        "return_status":"completed"
    })
    # Event stream: mobile checkout payment step deliberately underperforms.
    ev=[]
    event_id=1
    event_names=["session_start","view_item","add_to_cart","begin_checkout","add_shipping_info","add_payment_info","purchase"]
    for i in range(n):
        oid=f"O{i+1:07d}"; dt=pd.Timestamp(order_dates[i])
        # Non-purchasing sessions represented by synthetic order-linked session funnel.
        session=f"S{i+1:07d}"
        base_steps=event_names if status[i]=="delivered" else event_names[:-1]
        # Device friction: mobile loses a material share between shipping and payment.
        bot_session=rng.random()<.035
        steps=["session_start","view_item","add_to_cart","begin_checkout","add_shipping_info"]
        if not (device[i]=="mobile" and rng.random()<.29):
            steps.append("add_payment_info")
            if status[i]=="delivered": steps.append("purchase")
        for k,ename in enumerate(steps):
            ts=dt+pd.Timedelta(minutes=int(k*3+rng.integers(0,3)))
            touch_channel=(channel[i] if k==len(steps)-1 else rng.choice(CHANNELS))
            bot=bot_session
            ev.append((f"E{event_id:09d}",session,order_customer[i],oid,ts,ename,device[i],touch_channel,
                       None if rng.random()<.13 else f"utm_{touch_channel}",bot,
                       rng.choice(["/","/collections/new","/products/item","/checkout","/payment"])))
            event_id+=1
            if rng.random()<.012: # duplicate event with distinct event_id, same event semantics
                ev.append((f"E{event_id:09d}",session,order_customer[i],oid,ts,ename,device[i],touch_channel,
                           None if rng.random()<.13 else f"utm_{touch_channel}",bot,"/duplicate"))
                event_id+=1
    events=pd.DataFrame(ev,columns=["event_id","session_id","customer_id","order_id","event_timestamp","event_name","device","channel","utm_campaign","is_bot","page_path"])
    # Late arriving events: shift a small number of ingestion timestamps.
    events["ingested_at"]=pd.to_datetime(events.event_timestamp)+pd.to_timedelta(rng.integers(0,72,len(events)),unit="h")
    # Experiment assignments with three deterministic planted treatments.
    assignments=[]
    for exp,prob in [("EXP_POSITIVE",.5),("EXP_INCONCLUSIVE",.5),("EXP_GUARDRAIL",.5)]:
        for cid in customer_ids:
            assignments.append((exp,cid,rng.choice(["control","treatment"]),pd.Timestamp(START)+pd.Timedelta(days=int(rng.integers(0,500)))))
    expdf=pd.DataFrame(assignments,columns=["experiment_id","customer_id","variant","assigned_at"])
    # Outcomes are generated from variant effects; exposed in experiment outcome table for reproducible readouts.
    # Positive: +8% relative conversion; inconclusive: +1%; guardrail: +2% conversion but +18% refund risk.
    expdf["converted"]=0
    expdf["refund_or_complaint"]=0
    for exp,g in expdf.groupby("experiment_id"):
        base=.105
        for idx,row in g.iterrows():
            tr=row.variant=="treatment"
            pconv=base*({"EXP_POSITIVE":1.15,"EXP_INCONCLUSIVE":1.01,"EXP_GUARDRAIL":1.02}[exp] if tr else 1)
            expdf.loc[idx,"converted"]=int(rng.random()<pconv)
            pguard=.045*({"EXP_GUARDRAIL":1.18}.get(exp,1.0) if tr else 1)
            expdf.loc[idx,"refund_or_complaint"]=int(rng.random()<pguard)
    # Small missingness/outliers deliberately in raw source.
    orders.loc[rng.choice(n,int(n*.002),replace=False),"pincode"]=None
    orders.loc[rng.choice(n,int(n*.001),replace=False),"order_value_inr"]*=8
    tables={"customers":cust_first,"products":products,"orders":orders,"order_items":items,
            "returns":returns,"events":events,"campaigns":campaigns,"daily_ad_spend":spend,
            "experiment_assignments":expdf}
    for name,df in tables.items():
        df.to_csv(out/f"{name}.csv",index=False)
        print(f"{name}: {len(df):,} rows")
    print(f"Saved deterministic synthetic data to {out}")

if __name__=="__main__": main()
