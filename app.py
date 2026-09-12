
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
    --bg:#120f10;
    --panel:#1d1819;
    --panel2:#241d1f;
    --burgundy:#7b2946;
    --burgundy2:#9f3d5d;
    --forest:#315b4d;
    --sage:#6f9a86;
    --champagne:#c8aa73;
    --cream:#f3eee6;
    --muted:#a99f99;
    --line:#3a3032;
    --gold:#c8aa73;
}

.stApp{
    background:
      radial-gradient(circle at 78% 4%,rgba(159,61,93,.20),transparent 25%),
      radial-gradient(circle at 15% 30%,rgba(49,91,77,.14),transparent 28%),
      linear-gradient(135deg,#0f0d0e 0%,#171213 52%,#120f10 100%);
    color:var(--cream);
}
.block-container{max-width:1580px;padding:4.5rem 1.25rem 3rem;}
[data-testid="column"]{min-width:0;}

/* Luxury three-panel shell */
.rail,.filter-panel{
    background:linear-gradient(160deg,rgba(36,29,31,.96),rgba(27,22,23,.96));
    border:1px solid var(--line);border-radius:22px;
    box-shadow:0 20px 55px rgba(0,0,0,.28);
}
.rail{padding:1rem;position:sticky;top:4.75rem;}
.brand{
    background:linear-gradient(145deg,#5d1e35 0%,#7b2946 55%,#315b4d 140%);
    color:#fff;border:1px solid rgba(200,170,115,.22);border-radius:18px;padding:1rem;
    box-shadow:0 14px 30px rgba(0,0,0,.25);margin-bottom:1rem;
}
.brand-name{font-size:1.35rem;font-weight:900;letter-spacing:.10em;}
.brand-sub{font-size:.62rem;letter-spacing:.14em;opacity:.78;margin-top:.2rem;}
.rail-heading{color:#d7c9b7;font-size:.68rem;font-weight:850;text-transform:uppercase;letter-spacing:.16em;margin:.95rem 0 .5rem;}
.guide{
    color:#b7ada7;font-size:.76rem;line-height:1.52;
    background:rgba(255,255,255,.025);border:1px solid #342b2d;
    border-radius:14px;padding:.8rem;
}
.filter-panel{padding:1rem;margin-bottom:.75rem;}
.filter-title{color:var(--cream);font-size:1.02rem;font-weight:850;}
.filter-sub{color:var(--muted);font-size:.72rem;margin:.15rem 0 .8rem;}

/* Main content */
.hero{
    padding:1.85rem 2rem;border:1px solid #433538;border-radius:26px;
    background:
      radial-gradient(circle at 88% 20%,rgba(159,61,93,.24),transparent 26%),
      linear-gradient(135deg,#2a2022 0%,#211a1c 72%);
    box-shadow:0 18px 50px rgba(0,0,0,.26);margin-bottom:1.15rem;
}
.hero h1{margin:0;color:#f5efe7;font-size:2.45rem;font-weight:900;letter-spacing:-.045em;}
.hero p{margin:.45rem 0 0;color:#aaa09a;font-size:1rem;max-width:760px;}
.eyebrow{color:var(--champagne);font-size:.64rem;font-weight:900;letter-spacing:.18em;text-transform:uppercase;}
.page-title{color:#f4eee6;font-size:2rem;font-weight:900;letter-spacing:-.035em;margin:.18rem 0 .3rem;}
.page-subtitle{color:#aaa09a;font-size:.96rem;margin-bottom:1.15rem;}
.question{
    background:linear-gradient(135deg,#21191b,#1c1718);border:1px solid #3b3032;border-radius:16px;
    padding:.9rem 1rem;margin:.7rem 0 1.35rem;box-shadow:0 8px 24px rgba(0,0,0,.18);
}
.question-label{color:var(--champagne);font-size:.61rem;font-weight:900;letter-spacing:.15em;text-transform:uppercase;}
.question-text{color:#eee7df;font-size:1rem;font-weight:750;margin-top:.22rem;}
.insight{
    background:linear-gradient(135deg,#241b1e,#1b1718);
    border:1px solid #493238;border-left:4px solid var(--burgundy2);
    border-radius:14px;padding:.9rem 1rem;margin:.95rem 0;
    color:#d8cec7;box-shadow:0 8px 22px rgba(0,0,0,.18);
}
.impact{
    background:linear-gradient(135deg,#302127,#211a1c);
    border:1px solid #54353e;border-left:5px solid var(--champagne);
    border-radius:15px;padding:.95rem 1rem;margin-bottom:1.1rem;
    box-shadow:0 10px 28px rgba(0,0,0,.22);
}
.impact-title{color:var(--champagne);font-size:.66rem;font-weight:900;letter-spacing:.13em;text-transform:uppercase;}
.impact-main{color:#f0e8df;font-weight:750;margin-top:.28rem;}
.impact-small{color:#a99f99;font-size:.75rem;margin-top:.2rem;}
.pill{
    display:inline-block;background:rgba(123,41,70,.18);color:#d7b9c3;
    border:1px solid #573342;border-radius:999px;padding:.28rem .65rem;
    font-size:.68rem;font-weight:800;margin-bottom:.65rem;
}
div[data-testid="stMetric"]{
    background:linear-gradient(145deg,#211a1c,#1b1718);border:1px solid #393033;border-radius:16px;
    box-shadow:0 10px 26px rgba(0,0,0,.20);padding:.85rem;
}
div[data-testid="stMetric"] label{color:#9f9691!important;}
div[data-testid="stMetric"] [data-testid="stMetricValue"]{color:#f3eee6!important;}
.stButton>button{
    border-radius:11px;border:1px solid #46383b;background:#211a1c;
    color:#e9e1d9;font-weight:700;transition:.2s ease;
}
.stButton>button:hover{border-color:var(--champagne);color:#f0d9a5;background:#292022;}
div[data-testid="column"] .stButton>button{min-height:2.45rem;}
.stButton>button[kind="primary"]{
    background:linear-gradient(135deg,#6e233e,#922f50)!important;border:1px solid #b05a76!important;
    color:#fff!important;box-shadow:0 8px 20px rgba(123,41,70,.28);
}
[data-testid="stForm"]{border:0!important;padding:0!important;}
[data-testid="stMultiSelect"], [data-testid="stDateInput"]{margin-bottom:.2rem;}
.stMultiSelect div[data-baseweb="select"]>div,.stDateInput input{
    background:#191516!important;border-color:#403437!important;color:#eee7df!important;
}
.stMultiSelect div[data-baseweb="select"] span{color:#e8ddd5!important;}
.stCaption,.small-note{color:#8f8783!important;font-size:.73rem;}
.footer{text-align:center;color:#706866;font-size:.72rem;padding-top:1.25rem;letter-spacing:.05em;}

/* Decision intelligence cards */
.stakeholder-card{min-height:170px;padding:1.05rem 1.1rem;margin-bottom:.9rem;background:linear-gradient(145deg,#211a1c,#191516);border:1px solid #3a3032;border-radius:16px;box-shadow:0 10px 24px rgba(0,0,0,.18);}
.stakeholder-title{color:#d7c9b7;font-size:1rem;font-weight:900;margin-bottom:.45rem;}
.stakeholder-text{color:#aaa09a;font-size:.78rem;line-height:1.48;}
.risk-card{padding:1.35rem 1.2rem;background:linear-gradient(145deg,#2b1d22,#1b1718);border:1px solid #54353e;border-radius:18px;text-align:center;margin:.7rem 0 1rem;}
.risk-value{font-size:3.1rem;font-weight:950;color:#f3eee6;line-height:1.05;}
.risk-label{font-size:.68rem;color:#c8aa73;font-weight:900;letter-spacing:.14em;text-transform:uppercase;margin-top:.3rem;}
.formula{background:#191516;border:1px solid #393033;border-radius:12px;padding:.75rem 1rem;color:#cfc4bb;font-family:monospace;font-size:.82rem;margin:.7rem 0;}
/* Overview investigation cards */
.overview-card{
    min-height:118px;
    padding:1rem 1.05rem;
    margin-bottom:.9rem;
    background:linear-gradient(145deg,#211a1c,#191516);
    border:1px solid #3a3032;
    border-radius:16px;
    box-shadow:0 10px 24px rgba(0,0,0,.18);
}
.overview-card-icon{font-size:1.45rem;line-height:1;margin-bottom:.65rem;}
.overview-card-title{color:#d7c9b7;font-size:.94rem;font-weight:850;line-height:1.25;}
.overview-card-desc{color:#9f9691;font-size:.76rem;line-height:1.35;margin-top:.28rem;}

/* Give Plotly titles breathing room and keep charts inside their cards */
.plotly-chart-container{margin-top:.15rem;}
.js-plotly-plot{border:1px solid #342b2d;border-radius:18px;overflow:hidden;background:#1b1718;}
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
    "🏠 Overview","💡 Executive Insights","🎯 Probability & Risk",
    "🌧️ Delay Analyzer","🚗 Vehicle Comparison",
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

# ======================= NAVIGATION COLLAPSE =================
if "nav_open" not in st.session_state:
    st.session_state.nav_open = True

# ======================= THREE COLUMNS =======================
if st.session_state.nav_open:
    left, center, right = st.columns([1.02, 2.45, .92], gap="large")
else:
    center, right = st.columns([3.18, .92], gap="large")
    left = None

# -------------------------- LEFT -----------------------------
if left is not None:
    with left:
        if st.button("‹  Close menu", key="close_navigation", use_container_width=True):
            st.session_state.nav_open = False
            st.rerun()
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
            '<b>5</b> Check probability and risk.<br><br>'
             '<b>6</b> Use the insight to support a decision.</div>',
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
    with st.form("filter_form", border=False):
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
    if not st.session_state.nav_open:
        open_col, _ = st.columns([0.12, 0.88])
        with open_col:
            if st.button("☰", key="open_navigation", help="Open navigation", use_container_width=True):
                st.session_state.nav_open = True
                st.rerun()
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
            template="plotly",height=height,
            paper_bgcolor="#1b1718",plot_bgcolor="#1b1718",
            font=dict(color="#eee7df",family="Inter, Arial, sans-serif"),
            margin=dict(l=42,r=32,t=105,b=42),
            title=dict(x=0.02,xanchor="left",y=0.98,yanchor="top",font=dict(size=20,color="#f1e9df")),
            colorway=["#8f3453","#c8aa73","#4f806d","#b9657f","#8d9d92","#a98452"],
            hoverlabel=dict(bgcolor="#241d1f",font_color="#f3eee6",bordercolor="#594047"),
            legend=dict(orientation="h",yanchor="bottom",y=1.03,x=0,font=dict(color="#c8bfba")),
            bargap=.25
        )
        fig.update_xaxes(showgrid=False,linecolor="#4a3b3e",tickfont=dict(color="#a99f99"),title_font=dict(color="#d7cec7"))
        fig.update_yaxes(gridcolor="#30282a",zeroline=False,tickfont=dict(color="#a99f99"),title_font=dict(color="#d7cec7"))
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
            ("💡","Executive Insights","Manager + stakeholder brief"),
            ("🎯","Probability & Risk","Chance of late delivery"),
            ("🌧️","Delay Analyzer","Weather + traffic"),
            ("🚗","Vehicle Comparison","Vehicle performance"),
            ("👤","Agent Performance","Rating + age"),
            ("🗺️","Area Analysis","Area performance"),
            ("📦","Category Analysis","Delivery-time distribution"),
            ("🕐","Time-of-Day","Order timing"),
            ("📍","Distance Analyzer","Distance effect"),
            ("⏱️","Pickup Efficiency","Pickup effect"),
        ]
        cols=st.columns(2, gap="medium")
        for i,(icon,title,desc) in enumerate(cards):
            with cols[i%2]:
                st.markdown(
                    f'<div class="overview-card">'
                    f'<div class="overview-card-icon">{icon}</div>'
                    f'<div class="overview-card-title">{title}</div>'
                    f'<div class="overview-card-desc">{desc}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
        st.info("Use the navigation on the left. Filters on the right stay active across every analysis.")

    # ================= EXECUTIVE INSIGHTS ====================
    elif page=="💡 Executive Insights":
        header("DECISION INTELLIGENCE","Executive Insights","Turn the selected data into actions for managers and stakeholders")
        question("What are the most important operational signals in the current selection?")

        if filtered.empty:
            st.warning("No data matches the current filters.")
        else:
            n=len(filtered)
            avg=filtered["Delivery_Time"].mean()
            late=filtered["Late_Delivery"].mean()*100

            # Core findings
            wt=filtered.groupby(["Weather","Traffic"])["Delivery_Time"].mean().reset_index()
            worst_wt=wt.loc[wt["Delivery_Time"].idxmax()] if len(wt) else None
            veh=filtered.groupby("Vehicle")["Delivery_Time"].agg(["mean","count"]).reset_index().sort_values("mean")
            best_vehicle=veh.iloc[0] if len(veh) else None
            area=filtered.groupby("Area")["Delivery_Time"].agg(["mean","count"]).reset_index().sort_values("mean",ascending=False)
            worst_area=area.iloc[0] if len(area) else None
            cat=filtered.groupby("Category")["Late_Delivery"].agg(["mean","count"]).reset_index().sort_values("mean",ascending=False)
            worst_cat=cat.iloc[0] if len(cat) else None
            q=filtered.dropna(subset=["Agent_Rating","Delivery_Time"])
            rating_corr=q["Agent_Rating"].corr(q["Delivery_Time"]) if len(q)>1 else np.nan

            a,b,c,d=st.columns(4)
            a.metric("Selected deliveries",f"{n:,}")
            b.metric("Average delivery",f"{avg:.1f} min")
            c.metric("Late delivery rate",f"{late:.1f}%")
            d.metric("Late threshold",f"{late_threshold:.1f} min")

            st.markdown("### What the data is saying")
            findings=[]
            if worst_wt is not None:
                findings.append(f"The slowest weather–traffic combination is <b>{worst_wt['Weather']}</b> + <b>{worst_wt['Traffic']}</b>, averaging <b>{worst_wt['Delivery_Time']:.1f} min</b>.")
            if best_vehicle is not None:
                findings.append(f"<b>{best_vehicle['Vehicle']}</b> has the fastest selected vehicle average at <b>{best_vehicle['mean']:.1f} min</b> across {int(best_vehicle['count']):,} deliveries.")
            if worst_area is not None:
                findings.append(f"<b>{worst_area['Area']}</b> is the slowest selected area at <b>{worst_area['mean']:.1f} min</b>; it may deserve a bottleneck review.")
            if worst_cat is not None:
                findings.append(f"<b>{worst_cat['Category']}</b> has the highest selected late-delivery rate at <b>{worst_cat['mean']*100:.1f}%</b> among {int(worst_cat['count']):,} deliveries.")
            if pd.notna(rating_corr):
                direction="negative" if rating_corr<0 else "positive" if rating_corr>0 else "near-zero"
                findings.append(f"Agent rating has a <b>{direction}</b> linear correlation with delivery time of <b>{rating_corr:.2f}</b>; this should be treated as association, not proof of causation.")

            for i,text in enumerate(findings[:5],1):
                st.markdown(f'<div class="insight"><b>Finding {i}</b><br>{text}</div>',unsafe_allow_html=True)

            st.markdown("### Stakeholder notes")
            cols=st.columns(3)
            notes=[
                ("👔 Manager","Prioritise the slowest weather–traffic combinations and highest-delay areas. Use the filters to test whether the pattern remains when the analysis is narrowed to a specific vehicle, category or date range."),
                ("⚙️ Operations","Use the fastest vehicle group as a comparison benchmark, then investigate pickup duration, distance and time-of-day on the corresponding pages. The dashboard supports investigation rather than claiming a single cause."),
                ("📈 Investor / Stakeholder","The strongest signal is operational consistency: repeatable monitoring of delay rate, delivery time and risk can support scalable decision-making. Treat these historical results as evidence for further investigation, not as financial forecasts."),
            ]
            for col,(title,text) in zip(cols,notes):
                with col:
                    st.markdown(f'<div class="stakeholder-card"><div class="stakeholder-title">{title}</div><div class="stakeholder-text">{text}</div></div>',unsafe_allow_html=True)

            st.markdown("### Recommended next actions")
            actions=[]
            if worst_wt is not None: actions.append(f"Review staffing/fleet readiness for {worst_wt['Weather']} weather + {worst_wt['Traffic']} traffic.")
            if worst_area is not None: actions.append(f"Investigate the operational bottlenecks behind {worst_area['Area']}.")
            if worst_cat is not None: actions.append(f"Check whether {worst_cat['Category']} orders need a different handling or dispatch process.")
            actions.append("Use Probability & Risk to estimate historical late-delivery likelihood for a chosen operating scenario.")
            for act in actions:
                st.markdown(f"- {act}")

    # ================= PROBABILITY & RISK ====================
    elif page=="🎯 Probability & Risk":
        header("PROBABILITY","Delivery Risk Analyzer","Estimate historical late-delivery probability for a selected operating scenario")
        question("Given these conditions, how likely was a delivery to be late in the historical dataset?")

        st.markdown('<div class="formula">P(Late | conditions) = number of late deliveries under the selected conditions ÷ total deliveries under the selected conditions</div>',unsafe_allow_html=True)
        st.caption("This is an empirical probability from the dataset, not a machine-learning prediction. Late is defined using the dashboard's mean + 1 standard deviation threshold.")

        pc1,pc2,pc3=st.columns(3)
        with pc1:
            pw=st.selectbox("Weather scenario",["Any"]+weather_options,key="prob_weather")
            pt=st.selectbox("Traffic scenario",["Any"]+traffic_options,key="prob_traffic")
        with pc2:
            pv=st.selectbox("Vehicle scenario",["Any"]+vehicle_options,key="prob_vehicle")
            pa=st.selectbox("Area scenario",["Any"]+area_options,key="prob_area")
        with pc3:
            pcat=st.selectbox("Category scenario",["Any"]+category_options,key="prob_category")
            st.caption("The scenario selectors are independent of the right-side dashboard filters.")

        scenario=df.copy()
        if pw!="Any": scenario=scenario[scenario["Weather"]==pw]
        if pt!="Any": scenario=scenario[scenario["Traffic"]==pt]
        if pv!="Any": scenario=scenario[scenario["Vehicle"]==pv]
        if pa!="Any": scenario=scenario[scenario["Area"]==pa]
        if pcat!="Any": scenario=scenario[scenario["Category"]==pcat]

        if scenario.empty:
            st.warning("No historical deliveries match this scenario. Try a broader combination.")
        else:
            probability=scenario["Late_Delivery"].mean()*100
            late_n=int(scenario["Late_Delivery"].sum())
            total_n=len(scenario)
            risk="HIGH" if probability>=60 else "MODERATE" if probability>=30 else "LOW"
            r1,r2,r3=st.columns([1.35,1,1])
            with r1:
                st.markdown(f'<div class="risk-card"><div class="risk-value">{probability:.1f}%</div><div class="risk-label">Historical probability of late delivery · {risk} risk</div></div>',unsafe_allow_html=True)
            r2.metric("Comparable deliveries",f"{total_n:,}")
            r3.metric("Late deliveries",f"{late_n:,}")

            # show on-time vs late probability
            probs=pd.DataFrame({"Outcome":["On time","Late"],"Probability":[100-probability,probability]})
            fig=px.bar(probs,x="Outcome",y="Probability",text_auto=".1f",labels={"Probability":"Historical probability (%)"},title="Historical Outcome Probability")
            st.plotly_chart(polish(fig,460),use_container_width=True)

            st.markdown("### How to read this")
            st.markdown(f'<div class="insight">In the historical data, <b>{late_n:,} of {total_n:,}</b> comparable deliveries were classified as late. That gives an empirical late-delivery probability of <b>{probability:.1f}%</b> for this scenario. The result becomes more informative when the comparable-delivery count is large enough to support a stable comparison.</div>',unsafe_allow_html=True)

            # Factor risk table within current scenario
            st.markdown("### Risk by operating factor")
            risk_rows=[]
            for col,label in [("Weather","Weather"),("Traffic","Traffic"),("Vehicle","Vehicle"),("Area","Area"),("Category","Category")]:
                tmp=scenario.groupby(col)["Late_Delivery"].agg(["mean","count"]).reset_index()
                for _,row in tmp.sort_values("mean",ascending=False).head(3).iterrows():
                    risk_rows.append({"Factor":label,"Condition":row[col],"Late probability (%)":row["mean"]*100,"Deliveries":int(row["count"])})
            if risk_rows:
                rt=pd.DataFrame(risk_rows).sort_values("Late probability (%)",ascending=False)
                st.dataframe(rt,use_container_width=True,hide_index=True)

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
            st.markdown('<div class="plotly-chart-container">',unsafe_allow_html=True)
            st.plotly_chart(polish(fig),use_container_width=True)
            st.markdown('</div>',unsafe_allow_html=True)
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
            st.markdown('<div class="plotly-chart-container">',unsafe_allow_html=True)
            st.plotly_chart(polish(fig),use_container_width=True)
            st.markdown('</div>',unsafe_allow_html=True)
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
            st.markdown('<div class="plotly-chart-container">',unsafe_allow_html=True)
            st.plotly_chart(polish(fig,560),use_container_width=True)
            st.markdown('</div>',unsafe_allow_html=True)
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
            st.markdown('<div class="plotly-chart-container">',unsafe_allow_html=True)
            st.plotly_chart(polish(fig,max(500,35*len(q))),use_container_width=True)
            st.markdown('</div>',unsafe_allow_html=True)
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
            st.markdown('<div class="plotly-chart-container">',unsafe_allow_html=True)
            st.plotly_chart(polish(fig,560),use_container_width=True)
            st.markdown('</div>',unsafe_allow_html=True)
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
            st.markdown('<div class="plotly-chart-container">',unsafe_allow_html=True)
            st.plotly_chart(polish(fig),use_container_width=True)
            st.markdown('</div>',unsafe_allow_html=True)
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
            st.markdown('<div class="plotly-chart-container">',unsafe_allow_html=True)
            st.plotly_chart(polish(fig,560),use_container_width=True)
            st.markdown('</div>',unsafe_allow_html=True)
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
            st.markdown('<div class="plotly-chart-container">',unsafe_allow_html=True)
            st.plotly_chart(polish(fig,560),use_container_width=True)
            st.markdown('</div>',unsafe_allow_html=True)
            insight(f"Pickup duration has a correlation of <b>{corr:.2f}</b> with delivery time "
                    "in the current selection.")

    st.markdown('<div class="footer">LOGISIGHT • Evidence → Probability → Decision • FA-2</div>',unsafe_allow_html=True)
