
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# ============================================================
# LOGISIGHT — LAST-MILE DELIVERY INTELLIGENCE
# ============================================================

st.set_page_config(
    page_title="LogiSight | Delivery Intelligence",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ------------------------- PREMIUM UI ------------------------
st.markdown("""
<style>
:root{
    --forest:#244f42;
    --green:#4c8b70;
    --sage:#e7f1eb;
    --pale:#f5f8f5;
    --cream:#fbfcfa;
    --ink:#173f34;
    --muted:#70847c;
    --line:#dbe7e0;
    --gold:#b59a63;
}

.stApp{
    background:
      radial-gradient(circle at 85% 0%,rgba(76,139,112,.12),transparent 25%),
      linear-gradient(180deg,#fbfcfa 0%,#f3f7f4 100%);
}
.block-container{max-width:1550px;padding:1.15rem 1.35rem 3rem;}
[data-testid="column"]{min-width:0;}

.rail{
    background:rgba(255,255,255,.78);
    border:1px solid var(--line);
    border-radius:22px;
    padding:1rem;
    box-shadow:0 12px 32px rgba(36,79,66,.06);
    position:sticky;
    top:1rem;
}
.brand{
    background:linear-gradient(145deg,#234d40,#4c8b70);
    color:white;border-radius:18px;padding:1rem;
    box-shadow:0 10px 25px rgba(36,79,66,.15);
    margin-bottom:1rem;
}
.brand-name{font-size:1.35rem;font-weight:900;letter-spacing:.08em;}
.brand-sub{font-size:.62rem;letter-spacing:.14em;opacity:.8;margin-top:.2rem;}
.rail-heading{color:var(--ink);font-size:.72rem;font-weight:850;text-transform:uppercase;letter-spacing:.13em;margin:.9rem 0 .45rem;}
.guide{
    color:var(--muted);font-size:.76rem;line-height:1.48;
    background:#f7faf8;border:1px solid var(--line);
    border-radius:14px;padding:.8rem;
}
.filter-panel{
    background:rgba(255,255,255,.88);
    border:1px solid var(--line);border-radius:22px;
    padding:1rem;box-shadow:0 12px 32px rgba(36,79,66,.06);
}
.filter-title{color:var(--ink);font-size:1.05rem;font-weight:850;}
.filter-sub{color:var(--muted);font-size:.72rem;margin:.15rem 0 .8rem;}
.hero{
    padding:1.8rem 2rem;border:1px solid var(--line);border-radius:26px;
    background:
      radial-gradient(circle at 88% 20%,rgba(76,139,112,.19),transparent 24%),
      linear-gradient(135deg,#e5f0e9,#fff 72%);
    box-shadow:0 14px 40px rgba(36,79,66,.08);margin-bottom:1rem;
}
.hero h1{margin:0;color:var(--ink);font-size:2.45rem;font-weight:900;letter-spacing:-.045em;}
.hero p{margin:.4rem 0 0;color:var(--muted);font-size:1rem;max-width:760px;}
.eyebrow{color:var(--green);font-size:.67rem;font-weight:900;letter-spacing:.16em;text-transform:uppercase;}
.page-title{color:var(--ink);font-size:2rem;font-weight:900;letter-spacing:-.035em;margin:.15rem 0 .2rem;}
.page-subtitle{color:var(--muted);font-size:.98rem;margin-bottom:1rem;}
.question{
    background:#fff;border:1px solid var(--line);border-radius:16px;
    padding:.85rem 1rem;margin:.65rem 0 1rem;
    box-shadow:0 6px 18px rgba(36,79,66,.045);
}
.question-label{color:var(--gold);font-size:.64rem;font-weight:900;letter-spacing:.14em;text-transform:uppercase;}
.question-text{color:var(--ink);font-size:1rem;font-weight:750;margin-top:.2rem;}
.insight{
    background:linear-gradient(135deg,#edf6f1,#fff);
    border:1px solid #cfe2d8;border-left:4px solid var(--green);
    border-radius:14px;padding:.9rem 1rem;margin:.75rem 0;
    color:#315c4e;box-shadow:0 6px 18px rgba(36,79,66,.04);
}
.impact{
    background:linear-gradient(135deg,#e3f0e8,#fff);
    border:1px solid #cfe2d8;border-left:5px solid var(--green);
    border-radius:15px;padding:.9rem 1rem;margin-bottom:1rem;
}
.impact-title{color:var(--green);font-size:.68rem;font-weight:900;letter-spacing:.13em;text-transform:uppercase;}
.impact-main{color:var(--ink);font-weight:750;margin-top:.25rem;}
.impact-small{color:var(--muted);font-size:.75rem;margin-top:.2rem;}
.pill{
    display:inline-block;background:#edf5f0;color:var(--green);
    border:1px solid #d4e5dc;border-radius:999px;padding:.25rem .6rem;
    font-size:.7rem;font-weight:800;margin-bottom:.5rem;
}
div[data-testid="stMetric"]{
    background:#fff;border:1px solid var(--line);border-radius:16px;
    box-shadow:0 7px 20px rgba(36,79,66,.045);padding:.85rem;
}
.stButton>button{
    border-radius:11px;border:1px solid #d0e0d8;background:#fff;
    color:var(--ink);font-weight:700;
}
.stButton>button:hover{border-color:var(--green);color:var(--green);}
[data-testid="stForm"]{border:0!important;padding:0!important;}
.small-note{color:var(--muted);font-size:.75rem;}
.footer{text-align:center;color:#82938c;font-size:.75rem;padding-top:1rem;}
</style>
""", unsafe_allow_html=True)

BASE_DIR = Path(__file__).resolve().parent
MASCOT_CANDIDATES = [
    BASE_DIR/"mascot.png", BASE_DIR/"mascot.jpg", BASE_DIR/"mascot.webp",
    BASE_DIR/"assets"/"mascot.png", BASE_DIR/"assets"/"mascot.webp",
]
MASCOT_PATH = next((p for p in MASCOT_CANDIDATES if p.exists()), None)

DATA_FILES = [
    BASE_DIR/"Last mile Delivery Data.csv",
    BASE_DIR/"data"/"Last mile Delivery Data.csv",
    BASE_DIR/"last_mile_delivery_data.csv",
    BASE_DIR/"data"/"last_mile_delivery_data.csv",
]

@st.cache_data
def load_data():
    path = next((p for p in DATA_FILES if p.exists()), None)
    if path is None:
        return None, None
    return pd.read_csv(path), path.name

def prepare(raw):
    df = raw.copy()
    df.columns = df.columns.str.strip()

    for c in ["Order_ID","Weather","Traffic","Vehicle","Area","Category"]:
        df[c] = df[c].astype("string").str.strip()

    for c in ["Agent_Age","Agent_Rating","Store_Latitude","Store_Longitude",
              "Drop_Latitude","Drop_Longitude","Delivery_Time"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
    date_txt = df["Order_Date"].dt.strftime("%Y-%m-%d")

    df["Order_DateTime"] = pd.to_datetime(
        date_txt+" "+df["Order_Time"].astype("string").str.strip(), errors="coerce"
    )
    df["Pickup_DateTime"] = pd.to_datetime(
        date_txt+" "+df["Pickup_Time"].astype("string").str.strip(), errors="coerce"
    )

    df = df.dropna(subset=["Delivery_Time"]).copy()
    df = df[df["Delivery_Time"] >= 0].copy()

    df["Order_Hour"] = df["Order_DateTime"].dt.hour

    def tod(h):
        if pd.isna(h): return "Unknown"
        h=int(h)
        if h<=5: return "Night"
        if h<=11: return "Morning"
        if h<=16: return "Afternoon"
        return "Evening"

    df["Time_of_Day"] = df["Order_Hour"].apply(tod)

    df["Pickup_Duration"] = (
        df["Pickup_DateTime"]-df["Order_DateTime"]
    ).dt.total_seconds()/60
    df.loc[df["Pickup_Duration"]<0,"Pickup_Duration"] = np.nan

    df["Delivery_Distance"] = np.nan
    mask=df[["Store_Latitude","Store_Longitude","Drop_Latitude","Drop_Longitude"]].notna().all(axis=1)
    lat1=np.radians(df.loc[mask,"Store_Latitude"]); lon1=np.radians(df.loc[mask,"Store_Longitude"])
    lat2=np.radians(df.loc[mask,"Drop_Latitude"]); lon2=np.radians(df.loc[mask,"Drop_Longitude"])
    dlat=lat2-lat1; dlon=lon2-lon1
    a=np.sin(dlat/2)**2+np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2
    df.loc[mask,"Delivery_Distance"]=6371*2*np.arcsin(np.sqrt(a))

    df["Agent_Age_Group"]=pd.cut(
        df["Agent_Age"],[-np.inf,24,40,np.inf],labels=["<25","25–40","40+"]
    )

    threshold=df["Delivery_Time"].mean()+df["Delivery_Time"].std()
    df["Late_Delivery"]=df["Delivery_Time"]>threshold
    return df, threshold

raw, filename=load_data()
if raw is None:
    st.error("Dataset not found. Put 'Last mile Delivery Data.csv' beside app.py or inside /data.")
    st.stop()

df, late_threshold=prepare(raw)

weather_options=sorted(df["Weather"].dropna().unique().tolist())
traffic_options=sorted(df["Traffic"].dropna().unique().tolist())
vehicle_options=sorted(df["Vehicle"].dropna().unique().tolist())
category_options=sorted(df["Category"].dropna().unique().tolist())
area_options=sorted(df["Area"].dropna().unique().tolist())
min_date=df["Order_Date"].min().date()
max_date=df["Order_Date"].max().date()

PAGES=[
    "🏠 Overview","🌧️ Delay Analyzer","🚗 Vehicle Comparison",
    "👤 Agent Performance","🗺️ Area Analysis","📦 Category Analysis",
    "🕐 Time-of-Day","📍 Distance Analyzer","⏱️ Pickup Efficiency"
]

if "page" not in st.session_state:
    st.session_state.page=PAGES[0]

if "filters" not in st.session_state:
    st.session_state.filters={
        "weather":weather_options,"traffic":traffic_options,"vehicle":vehicle_options,
        "category":category_options,"area":area_options,
        "start":min_date,"end":max_date
    }

# ======================= THREE COLUMNS =======================
left, center, right = st.columns([1.02, 2.45, .92], gap="large")

# -------------------------- LEFT -----------------------------
with left:
    st.markdown(
        '<div class="brand"><div class="brand-name">LOGISIGHT</div>'
        '<div class="brand-sub">LAST-MILE DELIVERY INTELLIGENCE</div></div>',
        unsafe_allow_html=True
    )
    st.markdown('<div class="rail-heading">Navigation</div>', unsafe_allow_html=True)

    for i, name in enumerate(PAGES):
        active=st.session_state.page==name
        if st.button(
            ("● " if active else "")+name,
            key=f"nav_{i}", use_container_width=True,
            type="primary" if active else "secondary"
        ):
            st.session_state.page=name
            st.rerun()

    st.markdown('<div class="rail-heading">Manager workflow</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="guide"><b>1</b> Choose a business question.<br><br>'
        '<b>2</b> Refine the segment on the right.<br><br>'
        '<b>3</b> Click <b>Apply filters</b>.<br><br>'
        '<b>4</b> Read the before → after impact.<br><br>'
        '<b>5</b> Use the graph to support a decision.</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="rail-heading">Dashboard status</div>', unsafe_allow_html=True)
    st.caption(f"Dataset: {len(df):,} cleaned records")
    st.caption(f"Current view: {len(df):,} records before filters")

    if MASCOT_PATH:
        st.markdown('<div class="rail-heading">Your co-pilot</div>', unsafe_allow_html=True)
        st.image(str(MASCOT_PATH), use_container_width=True)
    else:
        st.caption("Mascot ready: add `mascot.png` beside `app.py`.")

# -------------------------- RIGHT ----------------------------
with right:
    st.markdown(
        '<div class="filter-panel"><div class="eyebrow">CONTROL PANEL</div>'
        '<div class="filter-title">Refine analysis</div>'
        '<div class="filter-sub">Changes are held until you press Apply.</div></div>',
        unsafe_allow_html=True
    )

    old=st.session_state.filters
    with st.form("filters", border=False):
        w=st.multiselect("🌦️ Weather",weather_options,default=old["weather"])
        t=st.multiselect("🚦 Traffic",traffic_options,default=old["traffic"])
        v=st.multiselect("🚗 Vehicle",vehicle_options,default=old["vehicle"])
        c=st.multiselect("📦 Category",category_options,default=old["category"])
        a=st.multiselect("📍 Area",area_options,default=old["area"])
        dates=st.date_input(
            "📅 Order dates",value=(old["start"],old["end"]),
            min_value=min_date,max_value=max_date
        )
        apply=st.form_submit_button("✓  Apply filters",use_container_width=True,type="primary")

    if apply:
        if isinstance(dates,tuple) and len(dates)==2:
            start,end=dates
        else:
            start=end=dates
        st.session_state.previous_filters=st.session_state.filters.copy()
        st.session_state.filters={
            "weather":w,"traffic":t,"vehicle":v,"category":c,"area":a,
            "start":start,"end":end
        }
        st.session_state.filter_applied=True
        st.rerun()

    if st.button("Reset filters",use_container_width=True,key="reset"):
        st.session_state.previous_filters=st.session_state.filters.copy()
        st.session_state.filters={
            "weather":weather_options,"traffic":traffic_options,"vehicle":vehicle_options,
            "category":category_options,"area":area_options,
            "start":min_date,"end":max_date
        }
        st.session_state.filter_applied=True
        st.rerun()

filters=st.session_state.filters
filtered=df[
    df["Weather"].isin(filters["weather"])
    &df["Traffic"].isin(filters["traffic"])
    &df["Vehicle"].isin(filters["vehicle"])
    &df["Category"].isin(filters["category"])
    &df["Area"].isin(filters["area"])
    &(df["Order_Date"].dt.date>=filters["start"])
    &(df["Order_Date"].dt.date<=filters["end"])
].copy()

# ------------------------- CENTER ----------------------------
with center:
    # Explain exactly what changed after Apply.
    if st.session_state.pop("filter_applied",False):
        prev=st.session_state.pop("previous_filters",None)
        if prev is not None:
            old_df=df[
                df["Weather"].isin(prev["weather"])
                &df["Traffic"].isin(prev["traffic"])
                &df["Vehicle"].isin(prev["vehicle"])
                &df["Category"].isin(prev["category"])
                &df["Area"].isin(prev["area"])
                &(df["Order_Date"].dt.date>=prev["start"])
                &(df["Order_Date"].dt.date<=prev["end"])
            ]
            old_avg=old_df["Delivery_Time"].mean()
            new_avg=filtered["Delivery_Time"].mean()
            old_late=old_df["Late_Delivery"].mean()*100 if len(old_df) else np.nan
            new_late=filtered["Late_Delivery"].mean()*100 if len(filtered) else np.nan

            if pd.notna(old_avg) and pd.notna(new_avg):
                delta=new_avg-old_avg
                pct=(delta/old_avg*100) if old_avg else 0
                movement="increased" if delta>0 else "decreased" if delta<0 else "stayed the same"
                st.markdown(
                    f'<div class="impact"><div class="impact-title">✓ Filter change applied</div>'
                    f'<div class="impact-main">Average delivery time <b>{movement}</b> by '
                    f'<b>{abs(delta):.1f} min ({abs(pct):.1f}%)</b>.</div>'
                    f'<div class="impact-small">Previous: <b>{old_avg:.1f} min</b> → '
                    f'Current: <b>{new_avg:.1f} min</b> &nbsp;•&nbsp; '
                    f'Late rate: <b>{old_late:.1f}%</b> → <b>{new_late:.1f}%</b></div></div>',
                    unsafe_allow_html=True
                )

    st.markdown(f'<div class="pill">● {len(filtered):,} deliveries selected</div>',unsafe_allow_html=True)
    page=st.session_state.page

    def header(kicker,title,subtitle):
        st.markdown(f'<div class="eyebrow">{kicker}</div><div class="page-title">{title}</div>'
                    f'<div class="page-subtitle">{subtitle}</div>',unsafe_allow_html=True)

    def question(text):
        st.markdown(f'<div class="question"><div class="question-label">Manager question</div>'
                    f'<div class="question-text">{text}</div></div>',unsafe_allow_html=True)

    def insight(text):
        st.markdown(f'<div class="insight"><b>Key insight:</b> {text}</div>',unsafe_allow_html=True)

    def polish(fig,height=520):
        fig.update_layout(
            template="plotly_white",height=height,
            paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(255,255,255,0)",
            font=dict(color="#173f34"),margin=dict(l=25,r=25,t=55,b=30),
            hoverlabel=dict(bgcolor="white"),
            legend=dict(orientation="h",yanchor="bottom",y=1.02,x=0)
        )
        fig.update_xaxes(showgrid=False,linecolor="#dbe7e0")
        fig.update_yaxes(gridcolor="#e7efeb",zeroline=False)
        return fig

    # ====================== OVERVIEW =========================
    if page=="🏠 Overview":
        st.markdown(
            '<div class="hero"><div class="eyebrow">LOGISTICS PERFORMANCE DASHBOARD</div>'
            '<h1>LogiSight Delivery Intelligence</h1>'
            '<p>Turn last-mile delivery data into clear operational decisions — one manager question at a time.</p></div>',
            unsafe_allow_html=True
        )
        st.caption(f"Source: {filename}  •  {len(df):,} cleaned records  •  {len(filtered):,} in current view")

        avg=filtered["Delivery_Time"].mean()
        late=filtered["Late_Delivery"].mean()*100 if len(filtered) else 0
        pickup=filtered["Pickup_Duration"].mean()
        distance=filtered["Delivery_Distance"].mean()

        k1,k2,k3,k4=st.columns(4)
        k1.metric("Average delivery",f"{avg:.1f} min" if pd.notna(avg) else "N/A")
        k2.metric("Deliveries",f"{len(filtered):,}")
        k3.metric("Late delivery rate",f"{late:.1f}%")
        k4.metric("Late threshold",f"{late_threshold:.1f} min")

        st.markdown("### What can the manager investigate?")
        cards=[
            ("🌧️","Delay Analyzer","Weather + traffic"),
            ("🚗","Vehicle Comparison","Vehicle performance"),
            ("👤","Agent Performance","Rating + age"),
            ("🗺️","Area Analysis","Area performance"),
            ("📦","Category Analysis","Distribution"),
            ("🕐","Time-of-Day","Order timing"),
            ("📍","Distance Analyzer","Distance effect"),
            ("⏱️","Pickup Efficiency","Pickup effect"),
        ]
        cols=st.columns(4)
        for i,(icon,title,desc) in enumerate(cards):
            with cols[i%4]:
                st.markdown(
                    f'<div class="guide" style="min-height:80px;margin-bottom:.7rem">'
                    f'<div style="font-size:1.3rem">{icon}</div>'
                    f'<b style="color:#173f34">{title}</b><br>{desc}</div>',
                    unsafe_allow_html=True
                )
        st.info("Use the navigation on the left. Filters on the right stay active across every analysis.")

    # ======================= Q1 ==============================
    elif page=="🌧️ Delay Analyzer":
        header("QUESTION 01","Delay Analyzer","Weather × traffic and average delivery time")
        question("How do weather and traffic conditions affect average delivery time?")
        q=filtered.groupby(["Weather","Traffic"],as_index=False)["Delivery_Time"].mean()
        if q.empty:
            st.warning("No data matches the current filters.")
        else:
            fig=px.bar(q,x="Weather",y="Delivery_Time",color="Traffic",barmode="group",
                       text_auto=".1f",labels={"Delivery_Time":"Average delivery time (min)"},
                       title="Average Delivery Time by Weather and Traffic")
            st.plotly_chart(polish(fig),use_container_width=True)
            worst=q.loc[q["Delivery_Time"].idxmax()]
            insight(f"The slowest selected combination is <b>{worst['Weather']}</b> weather with "
                    f"<b>{worst['Traffic']}</b> traffic at <b>{worst['Delivery_Time']:.1f} minutes</b>.")

    # ======================= Q2 ==============================
    elif page=="🚗 Vehicle Comparison":
        header("QUESTION 02","Vehicle Comparison","Compare delivery performance across vehicle types")
        question("Which vehicle type has the shortest average delivery time?")
        q=filtered.groupby("Vehicle",as_index=False)["Delivery_Time"].agg(["mean","count"]).reset_index()
        q=q.rename(columns={"mean":"Average","count":"Deliveries"}).sort_values("Average")
        if q.empty:
            st.warning("No data matches the current filters.")
        else:
            fig=px.bar(q,x="Vehicle",y="Average",text_auto=".1f",hover_data=["Deliveries"],
                       labels={"Average":"Average delivery time (min)","Vehicle":"Vehicle type"},
                       title="Average Delivery Time by Vehicle")
            st.plotly_chart(polish(fig),use_container_width=True)
            insight(f"<b>{q.iloc[0]['Vehicle']}</b> has the shortest selected average at "
                    f"<b>{q.iloc[0]['Average']:.1f} minutes</b>.")

    # ======================= Q3 ==============================
    elif page=="👤 Agent Performance":
        header("QUESTION 03","Agent Performance","Explore rating, age and delivery-time relationships")
        question("How do agent rating and age relate to delivery time?")
        q=filtered.dropna(subset=["Agent_Rating","Agent_Age","Delivery_Time","Agent_Age_Group"])
        if len(q)<2:
            st.warning("Not enough data for this analysis.")
        else:
            corr=q["Agent_Rating"].corr(q["Delivery_Time"])
            a,b,c=st.columns(3)
            a.metric("Average rating",f"{q['Agent_Rating'].mean():.2f}")
            b.metric("Average agent age",f"{q['Agent_Age'].mean():.1f} yrs")
            c.metric("Rating ↔ delivery r",f"{corr:.2f}")
            sample=q.sample(min(7000,len(q)),random_state=42)
            fig=px.scatter(sample,x="Agent_Rating",y="Delivery_Time",color="Agent_Age_Group",
                           opacity=.45,hover_data=["Agent_Age","Vehicle","Area","Category"],
                           labels={"Agent_Rating":"Agent rating","Delivery_Time":"Delivery time (min)",
                                   "Agent_Age_Group":"Age group"},
                           title="Agent Rating vs Delivery Time")
            st.plotly_chart(polish(fig,560),use_container_width=True)
            insight(f"The rating/delivery-time correlation is <b>{corr:.2f}</b>. "
                    "A value close to zero indicates a weak linear relationship.")

    # ======================= Q4 ==============================
    elif page=="🗺️ Area Analysis":
        header("QUESTION 04","Area Analysis","Locate areas with slower average delivery performance")
        question("Which areas have the highest average delivery times?")
        q=filtered.groupby("Area",as_index=False)["Delivery_Time"].agg(["mean","count"]).reset_index()
        q=q.rename(columns={"mean":"Average","count":"Deliveries"}).sort_values("Average",ascending=False)
        if q.empty:
            st.warning("No data matches the current filters.")
        else:
            fig=px.bar(q,x="Average",y="Area",orientation="h",text_auto=".1f",
                       hover_data=["Deliveries"],labels={"Average":"Average delivery time (min)"},
                       title="Average Delivery Time by Area")
            fig.update_layout(yaxis={"categoryorder":"total ascending"})
            st.plotly_chart(polish(fig,max(500,35*len(q))),use_container_width=True)
            insight(f"<b>{q.iloc[0]['Area']}</b> has the highest selected average delivery time "
                    f"at <b>{q.iloc[0]['Average']:.1f} minutes</b>.")

    # ======================= Q5 ==============================
    elif page=="📦 Category Analysis":
        header("QUESTION 05","Category Analysis","Compare delivery-time distributions and variability")
        question("Which categories have the highest and most variable delivery times?")
        q=filtered.dropna(subset=["Category","Delivery_Time"])
        if q.empty:
            st.warning("No data matches the current filters.")
        else:
            stats=q.groupby("Category")["Delivery_Time"].agg(["mean","std","median","count"]).reset_index()
            hi=stats.loc[stats["mean"].idxmax()]
            var=stats.loc[stats["std"].idxmax()]
            a,b,c=st.columns(3)
            a.metric("Highest average",f"{hi['mean']:.1f} min")
            b.metric("Highest-avg category",str(hi["Category"]))
            c.metric("Most variable",str(var["Category"]))
            fig=px.box(q,x="Category",y="Delivery_Time",points=False,
                       labels={"Delivery_Time":"Delivery time (min)"},
                       title="Delivery-Time Distribution by Category")
            st.plotly_chart(polish(fig,560),use_container_width=True)
            insight(f"<b>{hi['Category']}</b> has the highest selected average ({hi['mean']:.1f} min), "
                    f"while <b>{var['Category']}</b> has the highest variability (SD {var['std']:.1f} min).")
            with st.expander("View category statistics"):
                st.dataframe(stats.sort_values("mean",ascending=False),use_container_width=True,hide_index=True)

    # ======================= Q6 ==============================
    elif page=="🕐 Time-of-Day":
        header("QUESTION 06","Time-of-Day Analyzer","Compare performance across order times")
        question("Does the time of day when an order is placed influence delivery performance?")
        order=["Night","Morning","Afternoon","Evening"]
        q=filtered.groupby("Time_of_Day",as_index=False)["Delivery_Time"].agg(["mean","count"]).reset_index()
        q=q.rename(columns={"mean":"Average","count":"Deliveries"})
        q["Time_of_Day"]=pd.Categorical(q["Time_of_Day"],categories=order,ordered=True)
        q=q.sort_values("Time_of_Day")
        if q.empty:
            st.warning("No data matches the current filters.")
        else:
            fig=px.bar(q,x="Time_of_Day",y="Average",text_auto=".1f",hover_data=["Deliveries"],
                       labels={"Average":"Average delivery time (min)","Time_of_Day":"Time of day"},
                       title="Average Delivery Time by Time of Day")
            st.plotly_chart(polish(fig),use_container_width=True)
            worst=q.loc[q["Average"].idxmax()]
            insight(f"<b>{worst['Time_of_Day']}</b> has the highest selected average at "
                    f"<b>{worst['Average']:.1f} minutes</b>.")

    # ======================= DISTANCE =========================
    elif page=="📍 Distance Analyzer":
        header("DERIVED FEATURE","Distance Analyzer","Test whether delivery distance corresponds to delivery time")
        question("Does delivery distance correspond to delivery time?")
        q=filtered.dropna(subset=["Delivery_Distance","Delivery_Time"])
        if len(q)<2:
            st.warning("Not enough coordinate data for this analysis.")
        else:
            corr=q["Delivery_Distance"].corr(q["Delivery_Time"])
            a,b=st.columns(2)
            a.metric("Average distance",f"{q['Delivery_Distance'].mean():.2f} km")
            b.metric("Distance ↔ delivery r",f"{corr:.2f}")
            sample=q.sample(min(7000,len(q)),random_state=42)
            fig=px.scatter(sample,x="Delivery_Distance",y="Delivery_Time",opacity=.35,
                           trendline="ols",labels={"Delivery_Distance":"Distance (km)",
                           "Delivery_Time":"Delivery time (min)"},title="Distance vs Delivery Time")
            st.plotly_chart(polish(fig,560),use_container_width=True)
            insight(f"The calculated Haversine distance has a correlation of <b>{corr:.2f}</b> "
                    "with delivery time in the current selection.")

    # ======================= PICKUP ===========================
    elif page=="⏱️ Pickup Efficiency":
        header("QUESTION 07","Pickup Efficiency Analyzer","Explore pickup duration and overall delivery time")
        question("Does pickup duration influence the overall delivery time?")
        q=filtered.dropna(subset=["Pickup_Duration","Delivery_Time"])
        if len(q)<2:
            st.warning("Not enough pickup-time data for this analysis.")
        else:
            corr=q["Pickup_Duration"].corr(q["Delivery_Time"])
            a,b=st.columns(2)
            a.metric("Average pickup duration",f"{q['Pickup_Duration'].mean():.2f} min")
            b.metric("Pickup ↔ delivery r",f"{corr:.2f}")
            sample=q.sample(min(7000,len(q)),random_state=42)
            fig=px.scatter(sample,x="Pickup_Duration",y="Delivery_Time",opacity=.35,
                           trendline="ols",labels={"Pickup_Duration":"Pickup duration (min)",
                           "Delivery_Time":"Delivery time (min)"},title="Pickup Duration vs Delivery Time")
            st.plotly_chart(polish(fig,560),use_container_width=True)
            insight(f"Pickup duration has a correlation of <b>{corr:.2f}</b> with delivery time "
                    "in the current selection.")

    st.markdown('<div class="footer">LOGISIGHT • Same data. Smarter decisions. • FA-2</div>',unsafe_allow_html=True)
