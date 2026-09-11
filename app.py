
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


# ============================================================
# LOGISIGHT — LAST-MILE DELIVERY INTELLIGENCE
# FA-2 Dashboard
# ============================================================

st.set_page_config(
    page_title="LogiSight | Delivery Intelligence",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------
# UI / UX
# ------------------------------------------------------------
st.markdown(
    """
    <style>
    :root {
        --ink: #073b4c;
        --muted: #638084;
        --teal: #159a9c;
        --mint: #dff7f3;
        --line: #d8ebe8;
        --bg: #f6fbfa;
        --card: #ffffff;
    }

    .stApp {
        background: var(--bg);
    }

    .block-container {
        max-width: 1400px;
        padding-top: 1.2rem;
        padding-bottom: 3rem;
    }

    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid var(--line);
    }

    [data-testid="stSidebar"] .block-container {
        padding-top: 1.5rem;
    }

    .brand {
        padding: 1rem 1.1rem;
        border-radius: 18px;
        background: linear-gradient(135deg, #073b4c, #159a9c);
        color: white;
        margin-bottom: 1.1rem;
        box-shadow: 0 8px 24px rgba(7,59,76,.12);
    }

    .brand-title {
        font-size: 1.35rem;
        font-weight: 800;
        letter-spacing: .03em;
    }

    .brand-subtitle {
        opacity: .85;
        font-size: .82rem;
        margin-top: .15rem;
    }

    .hero {
        padding: 1.6rem 1.8rem;
        border-radius: 22px;
        background:
            radial-gradient(circle at 90% 15%, rgba(21,154,156,.18), transparent 28%),
            linear-gradient(135deg, #e2f8f4 0%, #ffffff 70%);
        border: 1px solid var(--line);
        box-shadow: 0 8px 28px rgba(7,59,76,.06);
        margin-bottom: 1.2rem;
    }

    .hero h1 {
        color: var(--ink);
        margin: 0;
        font-size: 2.45rem;
        font-weight: 800;
        letter-spacing: -.03em;
    }

    .hero p {
        color: var(--muted);
        margin: .45rem 0 0;
        font-size: 1.02rem;
    }

    .eyebrow {
        color: var(--teal);
        font-size: .76rem;
        font-weight: 800;
        letter-spacing: .13em;
        text-transform: uppercase;
        margin-bottom: .35rem;
    }

    .page-title {
        color: var(--ink);
        font-size: 2rem;
        font-weight: 800;
        margin: .1rem 0 .25rem;
        letter-spacing: -.025em;
    }

    .page-subtitle {
        color: var(--muted);
        margin-bottom: 1rem;
    }

    .insight {
        background: #e8f8f5;
        border: 1px solid #cbece7;
        border-left: 5px solid var(--teal);
        padding: .95rem 1rem;
        border-radius: 12px;
        color: #164e63;
        margin: .7rem 0 1rem;
    }

    .mini-card {
        background: var(--card);
        border: 1px solid var(--line);
        border-radius: 16px;
        padding: 1rem;
        box-shadow: 0 5px 18px rgba(7,59,76,.04);
    }

    .status {
        display: inline-block;
        padding: .3rem .65rem;
        border-radius: 999px;
        background: #e8f8f5;
        color: #11787a;
        font-size: .78rem;
        font-weight: 700;
    }

    .nav-note {
        color: var(--muted);
        font-size: .82rem;
        margin: .25rem 0 1rem;
    }

    .footer {
        text-align: center;
        color: #789093;
        padding: 1.2rem 0 .2rem;
        font-size: .82rem;
    }

    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid var(--line);
        padding: .9rem 1rem;
        border-radius: 16px;
        box-shadow: 0 5px 18px rgba(7,59,76,.04);
    }

    div[data-testid="stMetricLabel"] {
        color: var(--muted);
    }

    .stButton > button {
        width: 100%;
        border-radius: 12px;
        border: 1px solid var(--line);
        background: white;
        color: var(--ink);
        font-weight: 650;
    }

    .stButton > button:hover {
        border-color: var(--teal);
        color: var(--teal);
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ------------------------------------------------------------
# Data loading
# ------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent

POSSIBLE_DATA_FILES = [
    BASE_DIR / "Last mile Delivery Data.csv",
    BASE_DIR / "data" / "Last mile Delivery Data.csv",
    BASE_DIR / "last_mile_delivery_data.csv",
    BASE_DIR / "data" / "last_mile_delivery_data.csv",
]


@st.cache_data
def load_data():
    data_file = next((p for p in POSSIBLE_DATA_FILES if p.exists()), None)
    if data_file is None:
        return None, None
    return pd.read_csv(data_file), data_file.name


def clean_and_prepare(raw_df):
    df = raw_df.copy()
    df.columns = df.columns.str.strip()

    text_cols = [
        "Order_ID", "Weather", "Traffic", "Vehicle", "Area", "Category"
    ]
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype("string").str.strip()

    numeric_cols = [
        "Agent_Age", "Agent_Rating", "Store_Latitude", "Store_Longitude",
        "Drop_Latitude", "Drop_Longitude", "Delivery_Time"
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")

    order_date_text = df["Order_Date"].dt.strftime("%Y-%m-%d")
    df["Order_DateTime"] = pd.to_datetime(
        order_date_text + " " + df["Order_Time"].astype("string").str.strip(),
        errors="coerce",
    )
    df["Pickup_DateTime"] = pd.to_datetime(
        order_date_text + " " + df["Pickup_Time"].astype("string").str.strip(),
        errors="coerce",
    )

    df = df.dropna(subset=["Delivery_Time"]).copy()
    df = df[df["Delivery_Time"] >= 0].copy()

    # Time of day
    df["Order_Hour"] = df["Order_DateTime"].dt.hour

    def get_time_of_day(hour):
        if pd.isna(hour):
            return "Unknown"
        hour = int(hour)
        if hour <= 5:
            return "Night"
        if hour <= 11:
            return "Morning"
        if hour <= 16:
            return "Afternoon"
        return "Evening"

    df["Time_of_Day"] = df["Order_Hour"].apply(get_time_of_day)

    # Pickup duration
    df["Pickup_Duration"] = (
        df["Pickup_DateTime"] - df["Order_DateTime"]
    ).dt.total_seconds() / 60
    df.loc[df["Pickup_Duration"] < 0, "Pickup_Duration"] = np.nan

    # Haversine distance
    coordinate_mask = df[
        ["Store_Latitude", "Store_Longitude",
         "Drop_Latitude", "Drop_Longitude"]
    ].notna().all(axis=1)

    df["Delivery_Distance"] = np.nan

    lat1 = np.radians(df.loc[coordinate_mask, "Store_Latitude"])
    lon1 = np.radians(df.loc[coordinate_mask, "Store_Longitude"])
    lat2 = np.radians(df.loc[coordinate_mask, "Drop_Latitude"])
    lon2 = np.radians(df.loc[coordinate_mask, "Drop_Longitude"])

    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = (
        np.sin(dlat / 2) ** 2
        + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    )
    df.loc[coordinate_mask, "Delivery_Distance"] = (
        6371.0 * 2 * np.arcsin(np.sqrt(a))
    )

    # Agent age groups
    df["Agent_Age_Group"] = pd.cut(
        df["Agent_Age"],
        bins=[-np.inf, 24, 40, np.inf],
        labels=["<25", "25–40", "40+"],
    )

    # FA-2 late-delivery rule
    delivery_mean = df["Delivery_Time"].mean()
    delivery_std = df["Delivery_Time"].std()
    late_threshold = delivery_mean + delivery_std
    df["Late_Delivery"] = df["Delivery_Time"] > late_threshold

    return df, late_threshold


raw_df, data_file_name = load_data()

if raw_df is None:
    st.error(
        "Dataset not found. Upload 'Last mile Delivery Data.csv' "
        "in the same GitHub folder as app.py or inside /data."
    )
    st.stop()

df, late_threshold = clean_and_prepare(raw_df)


# ------------------------------------------------------------
# Filters
# ------------------------------------------------------------
weather_options = sorted(df["Weather"].dropna().unique().tolist())
traffic_options = sorted(df["Traffic"].dropna().unique().tolist())
vehicle_options = sorted(df["Vehicle"].dropna().unique().tolist())
category_options = sorted(df["Category"].dropna().unique().tolist())
area_options = sorted(df["Area"].dropna().unique().tolist())

st.sidebar.markdown(
    """
    <div class="brand">
        <div class="brand-title">🚚 LOGISIGHT</div>
        <div class="brand-subtitle">Last-Mile Delivery Intelligence</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown("### Dashboard Filters")
st.sidebar.caption("Use these filters to update every analysis page.")

selected_weather = st.sidebar.multiselect(
    "🌦️ Weather", weather_options, default=weather_options
)
selected_traffic = st.sidebar.multiselect(
    "🚦 Traffic", traffic_options, default=traffic_options
)
selected_vehicle = st.sidebar.multiselect(
    "🚗 Vehicle Type", vehicle_options, default=vehicle_options
)
selected_category = st.sidebar.multiselect(
    "📦 Product Category", category_options, default=category_options
)
selected_area = st.sidebar.multiselect(
    "📍 Area", area_options, default=area_options
)

min_date = df["Order_Date"].min().date()
max_date = df["Order_Date"].max().date()

selected_dates = st.sidebar.date_input(
    "📅 Order Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
    start_date, end_date = selected_dates
else:
    start_date = end_date = selected_dates

if st.sidebar.button("↻ Reset Filters"):
    st.rerun()


filtered = df[
    df["Weather"].isin(selected_weather)
    & df["Traffic"].isin(selected_traffic)
    & df["Vehicle"].isin(selected_vehicle)
    & df["Category"].isin(selected_category)
    & df["Area"].isin(selected_area)
    & (df["Order_Date"].dt.date >= start_date)
    & (df["Order_Date"].dt.date <= end_date)
].copy()


# ------------------------------------------------------------
# Plot helper
# ------------------------------------------------------------
def polish(fig, height=500):
    fig.update_layout(
        height=height,
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0)",
        font=dict(color="#073b4c"),
        margin=dict(l=25, r=25, t=45, b=25),
        hoverlabel=dict(bgcolor="white"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    )
    fig.update_xaxes(showgrid=False, linecolor="#d8ebe8")
    fig.update_yaxes(gridcolor="#e7f0ee", zeroline=False)
    return fig


def show_header(eyebrow, title, subtitle):
    st.markdown(
        f"""
        <div class="eyebrow">{eyebrow}</div>
        <div class="page-title">{title}</div>
        <div class="page-subtitle">{subtitle}</div>
        """,
        unsafe_allow_html=True,
    )


def show_insight(text):
    st.markdown(
        f'<div class="insight"><b>Key Insight:</b> {text}</div>',
        unsafe_allow_html=True,
    )


def safe_corr(data, x, y):
    if len(data) < 2:
        return np.nan
    return data[x].corr(data[y])


# ------------------------------------------------------------
# Navigation
# ------------------------------------------------------------
PAGES = [
    "🏠 Overview",
    "🌧️ Delay Analyzer",
    "🚗 Vehicle Comparison",
    "👤 Agent Performance",
    "🗺️ Area Analysis",
    "📦 Category Analysis",
    "🕐 Time-of-Day",
    "📍 Distance Analyzer",
    "⏱️ Pickup Efficiency",
]

page = st.sidebar.radio("Navigate", PAGES, index=0)

st.sidebar.markdown("---")
st.sidebar.markdown(
    f'<span class="status">● {len(filtered):,} records selected</span>',
    unsafe_allow_html=True,
)
st.sidebar.caption("All charts respond to the filters above.")


# ============================================================
# OVERVIEW
# ============================================================
if page == "🏠 Overview":
    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">LOGISTICS PERFORMANCE DASHBOARD</div>
            <h1>LogiSight Delivery Intelligence</h1>
            <p>Turn last-mile delivery data into clear operational decisions.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption(
        f"Source: {data_file_name}  •  "
        f"{len(df):,} cleaned records  •  "
        f"{len(filtered):,} records in current selection"
    )

    st.markdown("### 📌 Performance Snapshot")

    avg_delivery = filtered["Delivery_Time"].mean()
    delivery_count = len(filtered)
    late_pct = filtered["Late_Delivery"].mean() * 100 if delivery_count else 0
    avg_pickup = filtered["Pickup_Duration"].mean()
    avg_distance = filtered["Delivery_Distance"].mean()

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Average Delivery", f"{avg_delivery:.1f} min" if pd.notna(avg_delivery) else "N/A")
    k2.metric("Total Deliveries", f"{delivery_count:,}")
    k3.metric("Late Deliveries", f"{late_pct:.1f}%")
    k4.metric("Late Threshold", f"{late_threshold:.1f} min")

    st.markdown("### 🔎 Explore the Analysis")

    cards = [
        ("🌧️", "Delay Analyzer", "Weather × traffic and delivery delays.", "🌧️ Delay Analyzer"),
        ("🚗", "Vehicle Comparison", "Compare average delivery time by vehicle.", "🚗 Vehicle Comparison"),
        ("👤", "Agent Performance", "Explore rating, age and delivery time.", "👤 Agent Performance"),
        ("🗺️", "Area Analysis", "Find areas with the highest average time.", "🗺️ Area Analysis"),
        ("📦", "Category Analysis", "Compare distributions and variability.", "📦 Category Analysis"),
        ("🕐", "Time-of-Day", "See how order timing affects performance.", "🕐 Time-of-Day"),
        ("📍", "Distance Analyzer", "Check distance versus delivery time.", "📍 Distance Analyzer"),
        ("⏱️", "Pickup Efficiency", "Explore pickup duration versus delivery time.", "⏱️ Pickup Efficiency"),
    ]

    cols = st.columns(4)
    for i, (icon, title, desc, target) in enumerate(cards):
        with cols[i % 4]:
            st.markdown(
                f"""
                <div class="mini-card">
                    <div style="font-size:1.7rem">{icon}</div>
                    <div style="font-weight:800;color:#073b4c;margin:.35rem 0">{title}</div>
                    <div style="font-size:.83rem;color:#638084">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("Open analysis", key=f"open_{i}"):
                st.session_state["page"] = target
                st.rerun()

    # The radio is the actual navigation control. Keep the cards informative.
    st.markdown("---")
    st.markdown("### 💡 How to use LogiSight")
    st.info(
        "Start with the Performance Snapshot, then use the left navigation to "
        "open one analysis at a time. Filters stay active across all pages, "
        "so you can investigate the same selected segment from different angles."
    )


# ============================================================
# Q1 — DELAY ANALYZER
# ============================================================
elif page == "🌧️ Delay Analyzer":
    show_header(
        "QUESTION 01",
        "Delay Analyzer",
        "How do weather and traffic conditions affect average delivery time?",
    )

    q1 = (
        filtered.groupby(["Weather", "Traffic"], as_index=False)["Delivery_Time"]
        .mean()
        .rename(columns={"Delivery_Time": "Average_Delivery_Time"})
    )

    if q1.empty:
        st.warning("No data matches the current filters.")
    else:
        fig = px.bar(
            q1,
            x="Weather",
            y="Average_Delivery_Time",
            color="Traffic",
            barmode="group",
            text_auto=".1f",
            labels={
                "Weather": "Weather Condition",
                "Average_Delivery_Time": "Average Delivery Time (minutes)",
                "Traffic": "Traffic Condition",
            },
            title="Average Delivery Time by Weather and Traffic",
        )
        fig = polish(fig, 540)
        st.plotly_chart(fig, use_container_width=True)

        worst = q1.loc[q1["Average_Delivery_Time"].idxmax()]
        fastest = q1.loc[q1["Average_Delivery_Time"].idxmin()]
        show_insight(
            f"The slowest filtered combination is <b>{worst['Weather']}</b> weather "
            f"with <b>{worst['Traffic']}</b> traffic at "
            f"<b>{worst['Average_Delivery_Time']:.1f} minutes</b>. "
            f"The fastest is <b>{fastest['Weather']}</b> + "
            f"<b>{fastest['Traffic']}</b> at "
            f"<b>{fastest['Average_Delivery_Time']:.1f} minutes</b>."
        )


# ============================================================
# Q2 — VEHICLE
# ============================================================
elif page == "🚗 Vehicle Comparison":
    show_header(
        "QUESTION 02",
        "Vehicle Comparison",
        "Which vehicle type has the shortest average delivery time?",
    )

    q2 = (
        filtered.groupby("Vehicle", as_index=False)["Delivery_Time"]
        .agg(["mean", "count"])
        .reset_index()
        .rename(columns={"mean": "Average_Delivery_Time", "count": "Deliveries"})
        .sort_values("Average_Delivery_Time")
    )

    if q2.empty:
        st.warning("No data matches the current filters.")
    else:
        fig = px.bar(
            q2,
            x="Vehicle",
            y="Average_Delivery_Time",
            text_auto=".1f",
            hover_data=["Deliveries"],
            labels={
                "Vehicle": "Vehicle Type",
                "Average_Delivery_Time": "Average Delivery Time (minutes)",
                "Deliveries": "Deliveries",
            },
            title="Average Delivery Time by Vehicle",
        )
        fig = polish(fig, 540)
        st.plotly_chart(fig, use_container_width=True)

        fastest = q2.iloc[0]
        slowest = q2.iloc[-1]
        show_insight(
            f"<b>{fastest['Vehicle']}</b> has the shortest average delivery time "
            f"at <b>{fastest['Average_Delivery_Time']:.1f} minutes</b>, while "
            f"<b>{slowest['Vehicle']}</b> is highest at "
            f"<b>{slowest['Average_Delivery_Time']:.1f} minutes</b>."
        )


# ============================================================
# Q3 — AGENT
# ============================================================
elif page == "👤 Agent Performance":
    show_header(
        "QUESTION 03",
        "Agent Performance",
        "How do agent rating and age relate to delivery time?",
    )

    agent_df = filtered.dropna(
        subset=["Agent_Rating", "Agent_Age", "Delivery_Time", "Agent_Age_Group"]
    ).copy()

    if agent_df.empty:
        st.warning("Not enough data for the agent analysis.")
    else:
        corr = safe_corr(agent_df, "Agent_Rating", "Delivery_Time")

        a1, a2, a3 = st.columns(3)
        a1.metric("Average Agent Rating", f"{agent_df['Agent_Rating'].mean():.2f}")
        a2.metric("Average Agent Age", f"{agent_df['Agent_Age'].mean():.1f} yrs")
        a3.metric("Rating ↔ Delivery Correlation", f"{corr:.2f}" if pd.notna(corr) else "N/A")

        fig = px.scatter(
            agent_df,
            x="Agent_Rating",
            y="Delivery_Time",
            color="Agent_Age_Group",
            opacity=.45,
            labels={
                "Agent_Rating": "Agent Rating",
                "Delivery_Time": "Delivery Time (minutes)",
                "Agent_Age_Group": "Age Group",
            },
            hover_data=["Agent_Age", "Vehicle", "Area", "Category"],
            title="Agent Rating vs Delivery Time",
        )
        fig = polish(fig, 570)
        st.plotly_chart(fig, use_container_width=True)

        if pd.isna(corr):
            relation = "A correlation could not be calculated for this selection."
        elif corr < -.2:
            relation = f"The relationship is negative (r ≈ {corr:.2f}), so higher ratings tend to be associated with shorter delivery times."
        elif corr > .2:
            relation = f"The relationship is positive (r ≈ {corr:.2f}), so higher ratings tend to be associated with longer delivery times."
        else:
            relation = f"The linear relationship is weak (r ≈ {corr:.2f}), so rating alone does not strongly explain delivery time."

        show_insight(relation)


# ============================================================
# Q4 — AREA
# ============================================================
elif page == "🗺️ Area Analysis":
    show_header(
        "QUESTION 04",
        "Area Analysis",
        "Which areas have the highest average delivery times?",
    )

    q4 = (
        filtered.groupby("Area", as_index=False)["Delivery_Time"]
        .agg(["mean", "count"])
        .reset_index()
        .rename(columns={"mean": "Average_Delivery_Time", "count": "Deliveries"})
        .sort_values("Average_Delivery_Time", ascending=False)
    )

    if q4.empty:
        st.warning("No data matches the current filters.")
    else:
        fig = px.bar(
            q4,
            x="Average_Delivery_Time",
            y="Area",
            orientation="h",
            text_auto=".1f",
            hover_data=["Deliveries"],
            labels={
                "Average_Delivery_Time": "Average Delivery Time (minutes)",
                "Area": "Area",
                "Deliveries": "Deliveries",
            },
            title="Average Delivery Time by Area",
        )
        fig = polish(fig, max(520, 38 * len(q4)))
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig, use_container_width=True)

        worst = q4.iloc[0]
        show_insight(
            f"<b>{worst['Area']}</b> has the highest average delivery time at "
            f"<b>{worst['Average_Delivery_Time']:.1f} minutes</b> in the current selection."
        )


# ============================================================
# Q5 — CATEGORY
# ============================================================
elif page == "📦 Category Analysis":
    show_header(
        "QUESTION 05",
        "Category Analysis",
        "Which categories have the highest and most variable delivery times?",
    )

    q5 = filtered.dropna(subset=["Category", "Delivery_Time"]).copy()

    if q5.empty:
        st.warning("No data matches the current filters.")
    else:
        stats = (
            q5.groupby("Category")["Delivery_Time"]
            .agg(["mean", "std", "median", "count"])
            .reset_index()
            .rename(
                columns={
                    "mean": "Average",
                    "std": "Std_Dev",
                    "median": "Median",
                    "count": "Deliveries",
                }
            )
        )

        highest_mean = stats.loc[stats["Average"].idxmax()]
        most_variable = stats.loc[stats["Std_Dev"].idxmax()]

        c1, c2, c3 = st.columns(3)
        c1.metric("Highest Average", f"{highest_mean['Average']:.1f} min")
        c2.metric("Highest-Avg Category", str(highest_mean["Category"]))
        c3.metric("Most Variable", str(most_variable["Category"]))

        fig = px.box(
            q5,
            x="Category",
            y="Delivery_Time",
            points=False,
            labels={
                "Category": "Product Category",
                "Delivery_Time": "Delivery Time (minutes)",
            },
            title="Delivery-Time Distribution by Category",
        )
        fig = polish(fig, 560)
        st.plotly_chart(fig, use_container_width=True)

        show_insight(
            f"<b>{highest_mean['Category']}</b> has the highest average delivery time "
            f"({highest_mean['Average']:.1f} min), while <b>{most_variable['Category']}</b> "
            f"has the greatest variability (SD ≈ {most_variable['Std_Dev']:.1f} min)."
        )

        with st.expander("View category statistics"):
            st.dataframe(
                stats.sort_values("Average", ascending=False),
                use_container_width=True,
                hide_index=True,
            )


# ============================================================
# Q6 — TIME OF DAY
# ============================================================
elif page == "🕐 Time-of-Day":
    show_header(
        "QUESTION 06",
        "Time-of-Day Analyzer",
        "Does the time of day when an order is placed influence delivery performance?",
    )

    tod_order = ["Night", "Morning", "Afternoon", "Evening"]

    tod_stats = (
        filtered.groupby("Time_of_Day", as_index=False)["Delivery_Time"]
        .agg(["mean", "count"])
        .reset_index()
        .rename(columns={"mean": "Average_Delivery_Time", "count": "Deliveries"})
    )
    tod_stats["Time_of_Day"] = pd.Categorical(
        tod_stats["Time_of_Day"], categories=tod_order, ordered=True
    )
    tod_stats = tod_stats.sort_values("Time_of_Day")

    if tod_stats.empty:
        st.warning("No data matches the current filters.")
    else:
        fig = px.bar(
            tod_stats,
            x="Time_of_Day",
            y="Average_Delivery_Time",
            text_auto=".1f",
            hover_data=["Deliveries"],
            labels={
                "Time_of_Day": "Time of Day",
                "Average_Delivery_Time": "Average Delivery Time (minutes)",
                "Deliveries": "Deliveries",
            },
            title="Average Delivery Time by Time of Day",
        )
        fig = polish(fig, 520)
        st.plotly_chart(fig, use_container_width=True)

        worst = tod_stats.loc[tod_stats["Average_Delivery_Time"].idxmax()]
        show_insight(
            f"<b>{worst['Time_of_Day']}</b> has the highest average delivery time "
            f"at <b>{worst['Average_Delivery_Time']:.1f} minutes</b>."
        )


# ============================================================
# DISTANCE
# ============================================================
elif page == "📍 Distance Analyzer":
    show_header(
        "DERIVED FEATURE",
        "Distance Analyzer",
        "Does delivery distance correspond to delivery time?",
    )

    distance_df = filtered.dropna(
        subset=["Delivery_Distance", "Delivery_Time"]
    ).copy()

    if len(distance_df) < 2:
        st.warning("Not enough coordinate data for this analysis.")
    else:
        corr = safe_corr(distance_df, "Delivery_Distance", "Delivery_Time")

        c1, c2 = st.columns(2)
        c1.metric("Average Distance", f"{distance_df['Delivery_Distance'].mean():.2f} km")
        c2.metric("Distance ↔ Delivery Correlation", f"{corr:.2f}" if pd.notna(corr) else "N/A")

        # Sample large datasets so the browser stays responsive.
        plot_df = distance_df.sample(min(7000, len(distance_df)), random_state=42)

        fig = px.scatter(
            plot_df,
            x="Delivery_Distance",
            y="Delivery_Time",
            opacity=.35,
            trendline="ols",
            labels={
                "Delivery_Distance": "Delivery Distance (km)",
                "Delivery_Time": "Delivery Time (minutes)",
            },
            hover_data=["Vehicle", "Traffic", "Area", "Category"],
            title="Delivery Distance vs Delivery Time",
        )
        fig = polish(fig, 570)
        st.plotly_chart(fig, use_container_width=True)

        show_insight(
            f"Delivery Distance is calculated from store/drop coordinates using the "
            f"Haversine formula. The correlation with delivery time is "
            f"<b>{corr:.2f}</b>."
        )


# ============================================================
# PICKUP
# ============================================================
elif page == "⏱️ Pickup Efficiency":
    show_header(
        "QUESTION 07",
        "Pickup Efficiency Analyzer",
        "Does pickup duration influence the overall delivery time?",
    )

    pickup_df = filtered.dropna(
        subset=["Pickup_Duration", "Delivery_Time"]
    ).copy()

    if len(pickup_df) < 2:
        st.warning("Not enough pickup-time data for this analysis.")
    else:
        corr = safe_corr(pickup_df, "Pickup_Duration", "Delivery_Time")

        c1, c2 = st.columns(2)
        c1.metric("Average Pickup Duration", f"{pickup_df['Pickup_Duration'].mean():.2f} min")
        c2.metric("Pickup ↔ Delivery Correlation", f"{corr:.2f}" if pd.notna(corr) else "N/A")

        plot_df = pickup_df.sample(min(7000, len(pickup_df)), random_state=42)

        fig = px.scatter(
            plot_df,
            x="Pickup_Duration",
            y="Delivery_Time",
            opacity=.35,
            trendline="ols",
            labels={
                "Pickup_Duration": "Pickup Duration (minutes)",
                "Delivery_Time": "Delivery Time (minutes)",
            },
            hover_data=["Vehicle", "Traffic", "Area", "Category"],
            title="Pickup Duration vs Delivery Time",
        )
        fig = polish(fig, 570)
        st.plotly_chart(fig, use_container_width=True)

        show_insight(
            f"Pickup Duration is calculated as Pickup Time − Order Time. "
            f"The correlation with delivery time is <b>{corr:.2f}</b>."
        )


# ------------------------------------------------------------
# Footer
# ------------------------------------------------------------
st.markdown("---")
st.markdown(
    '<div class="footer">LOGISIGHT • Same Data. Smarter Decisions. • FA-2 Dashboarding & Deployment</div>',
    unsafe_allow_html=True,
)
