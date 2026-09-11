
import math
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ============================================================
# LOGISIGHT — LAST-MILE DELIVERY INTELLIGENCE DASHBOARD
# FA-2: Dashboarding and Deployment
# Based on the FA-1 storyboard:
#   Q1 Weather + Traffic
#   Q2 Vehicle
#   Q3 Agent Rating + Age
#   Q4 Area
#   Q5 Category
#   Q6 Time of Day
#   Q7 Pickup Duration
# Plus: Delivery Distance
# ============================================================

st.set_page_config(
    page_title="LogiSight | Delivery Intelligence",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------
# Styling
# ------------------------------------------------------------
st.markdown(
    """
    <style>
    .main {
        background: #f4fbfa;
    }
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }
    .hero {
        padding: 1.5rem 1.8rem;
        border-radius: 18px;
        background: linear-gradient(135deg, #dff7f3 0%, #eefcf9 55%, #d9f0ed 100%);
        border: 1px solid #c7e8e3;
        margin-bottom: 1rem;
    }
    .hero h1 {
        margin: 0;
        color: #073b4c;
        font-size: 2.4rem;
    }
    .hero p {
        margin: 0.45rem 0 0;
        color: #287d7a;
        font-size: 1.05rem;
    }
    .section-title {
        color: #073b4c;
        margin-top: 1.2rem;
        margin-bottom: 0.2rem;
    }
    .insight {
        background: #e5f6f3;
        border-left: 5px solid #159a9c;
        padding: 0.9rem 1rem;
        border-radius: 10px;
        color: #164e63;
        margin-top: 0.4rem;
    }
    .small-note {
        color: #52757a;
        font-size: 0.9rem;
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

    df = pd.read_csv(data_file)
    return df, data_file.name


def clean_and_prepare(raw_df):
    df = raw_df.copy()

    # Remove accidental spaces from column names.
    df.columns = df.columns.str.strip()

    # Clean text columns.
    text_cols = [
        "Order_ID",
        "Weather",
        "Traffic",
        "Vehicle",
        "Area",
        "Category",
    ]
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype("string").str.strip()

    # Numeric columns.
    numeric_cols = [
        "Agent_Age",
        "Agent_Rating",
        "Store_Latitude",
        "Store_Longitude",
        "Drop_Latitude",
        "Drop_Longitude",
        "Delivery_Time",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Date/time conversion.
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
    df["Order_DateTime"] = pd.to_datetime(
        df["Order_Date"].dt.strftime("%Y-%m-%d")
        + " "
        + df["Order_Time"].astype("string").str.strip(),
        errors="coerce",
    )
    df["Pickup_DateTime"] = pd.to_datetime(
        df["Order_Date"].dt.strftime("%Y-%m-%d")
        + " "
        + df["Pickup_Time"].astype("string").str.strip(),
        errors="coerce",
    )

    # Remove rows where the main analysis target is unavailable.
    df = df.dropna(subset=["Delivery_Time"]).copy()

    # Keep realistic non-negative delivery times.
    df = df[df["Delivery_Time"] >= 0].copy()

    # --------------------------------------------------------
    # Q6: Time of Day
    # --------------------------------------------------------
    df["Order_Hour"] = df["Order_DateTime"].dt.hour

    def time_of_day(hour):
        if pd.isna(hour):
            return "Unknown"
        hour = int(hour)
        if 0 <= hour <= 5:
            return "Night"
        if 6 <= hour <= 11:
            return "Morning"
        if 12 <= hour <= 16:
            return "Afternoon"
        return "Evening"

    df["Time_of_Day"] = df["Order_Hour"].apply(time_of_day)

    # --------------------------------------------------------
    # Q6/Q7: Pickup Duration
    # Pickup duration = Pickup Time - Order Time
    # --------------------------------------------------------
    df["Pickup_Duration"] = (
        df["Pickup_DateTime"] - df["Order_DateTime"]
    ).dt.total_seconds() / 60

    # Invalid negative durations are treated as missing.
    df.loc[df["Pickup_Duration"] < 0, "Pickup_Duration"] = np.nan

    # --------------------------------------------------------
    # Q6/Distance: Haversine distance from store to drop point
    # --------------------------------------------------------
    def haversine_km(lat1, lon1, lat2, lon2):
        lat1, lon1, lat2, lon2 = map(
            np.radians, [lat1, lon1, lat2, lon2]
        )

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = (
            np.sin(dlat / 2) ** 2
            + np.cos(lat1)
            * np.cos(lat2)
            * np.sin(dlon / 2) ** 2
        )

        return 6371.0 * 2 * np.arcsin(np.sqrt(a))

    coordinate_mask = df[
        [
            "Store_Latitude",
            "Store_Longitude",
            "Drop_Latitude",
            "Drop_Longitude",
        ]
    ].notna().all(axis=1)

    df["Delivery_Distance"] = np.nan
    df.loc[coordinate_mask, "Delivery_Distance"] = haversine_km(
        df.loc[coordinate_mask, "Store_Latitude"],
        df.loc[coordinate_mask, "Store_Longitude"],
        df.loc[coordinate_mask, "Drop_Latitude"],
        df.loc[coordinate_mask, "Drop_Longitude"],
    )

    # --------------------------------------------------------
    # Q3: Agent age groups
    # --------------------------------------------------------
    df["Agent_Age_Group"] = pd.cut(
        df["Agent_Age"],
        bins=[-np.inf, 24, 40, np.inf],
        labels=["<25", "25–40", "40+"],
    )

    # --------------------------------------------------------
    # Late delivery definition from FA-2:
    # Delivery_Time > mean + 1 standard deviation
    # --------------------------------------------------------
    delivery_mean = df["Delivery_Time"].mean()
    delivery_std = df["Delivery_Time"].std()
    late_threshold = delivery_mean + delivery_std

    df["Late_Delivery"] = df["Delivery_Time"] > late_threshold

    return df, late_threshold


raw_df, data_file_name = load_data()

if raw_df is None:
    st.error(
        "Dataset not found. Put 'Last mile Delivery Data.csv' "
        "in the same folder as app.py or inside a 'data' folder."
    )
    st.stop()

df, late_threshold = clean_and_prepare(raw_df)


# ------------------------------------------------------------
# Sidebar filters
# ------------------------------------------------------------
st.sidebar.markdown("## 🚚 LOGISIGHT")
st.sidebar.caption("Delivery Intelligence")

st.sidebar.markdown("### Filters")

weather_options = sorted(df["Weather"].dropna().unique().tolist())
traffic_options = sorted(df["Traffic"].dropna().unique().tolist())
vehicle_options = sorted(df["Vehicle"].dropna().unique().tolist())
category_options = sorted(df["Category"].dropna().unique().tolist())
area_options = sorted(df["Area"].dropna().unique().tolist())

selected_weather = st.sidebar.multiselect(
    "Weather",
    weather_options,
    default=weather_options,
)

selected_traffic = st.sidebar.multiselect(
    "Traffic",
    traffic_options,
    default=traffic_options,
)

selected_vehicle = st.sidebar.multiselect(
    "Vehicle Type",
    vehicle_options,
    default=vehicle_options,
)

selected_category = st.sidebar.multiselect(
    "Product Category",
    category_options,
    default=category_options,
)

selected_area = st.sidebar.multiselect(
    "Area",
    area_options,
    default=area_options,
)

min_date = df["Order_Date"].min().date()
max_date = df["Order_Date"].max().date()

selected_dates = st.sidebar.date_input(
    "Order Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
    start_date, end_date = selected_dates
else:
    start_date = end_date = selected_dates

# ------------------------------------------------------------
# Apply filters
# ------------------------------------------------------------
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
# Header
# ------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <h1>LogiSight Delivery Intelligence</h1>
        <p>
            From delivery data to smarter operational decisions —
            explore what affects delivery performance.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption(
    f"Source: {data_file_name}  •  "
    f"{len(df):,} cleaned records available  •  "
    f"{len(filtered):,} records after current filters"
)


# ------------------------------------------------------------
# KPI summary
# ------------------------------------------------------------
st.markdown('<h2 class="section-title">📌 Performance Overview</h2>',
            unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)

avg_delivery = filtered["Delivery_Time"].mean()
delivery_count = len(filtered)
late_pct = (
    filtered["Late_Delivery"].mean() * 100
    if len(filtered) > 0
    else 0
)
avg_pickup = filtered["Pickup_Duration"].mean()
avg_distance = filtered["Delivery_Distance"].mean()

k1.metric(
    "Average Delivery Time",
    f"{avg_delivery:.1f} min" if not pd.isna(avg_delivery) else "N/A",
)

k2.metric(
    "Total Deliveries",
    f"{delivery_count:,}",
)

k3.metric(
    "Late Delivery %",
    f"{late_pct:.1f}%",
)

k4.metric(
    "Late Threshold",
    f"{late_threshold:.1f} min",
)


# ------------------------------------------------------------
# Q1 — Delay Analyzer
# Weather × Traffic → Average Delivery Time
# ------------------------------------------------------------
st.markdown(
    '<h2 class="section-title">🌧️ 1. Delay Analyzer</h2>',
    unsafe_allow_html=True,
)
st.caption("How do weather and traffic conditions affect average delivery time?")

q1 = (
    filtered.groupby(["Weather", "Traffic"], as_index=False)["Delivery_Time"]
    .mean()
    .rename(columns={"Delivery_Time": "Average_Delivery_Time"})
)

if not q1.empty:
    fig1 = px.bar(
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
    )
    fig1.update_layout(
        height=470,
        legend_title="Traffic",
        margin=dict(l=20, r=20, t=30, b=20),
    )
    st.plotly_chart(fig1, use_container_width=True)

    worst_q1 = q1.loc[q1["Average_Delivery_Time"].idxmax()]
    st.markdown(
        f"""
        <div class="insight">
        <b>Key Insight:</b> The slowest filtered combination is
        <b>{worst_q1["Weather"]}</b> weather with
        <b>{worst_q1["Traffic"]}</b> traffic
        ({worst_q1["Average_Delivery_Time"]:.1f} minutes average).
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.info("No data matches the selected filters.")


# ------------------------------------------------------------
# Q2 + Q3 — Vehicle and Agent
# ------------------------------------------------------------
st.markdown(
    '<h2 class="section-title">🚲 2–3. Vehicle & Agent Performance</h2>',
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Vehicle Comparison")
    st.caption("Which vehicle type has the shortest average delivery time?")

    q2 = (
        filtered.groupby("Vehicle", as_index=False)["Delivery_Time"]
        .mean()
        .sort_values("Delivery_Time")
        .rename(columns={"Delivery_Time": "Average_Delivery_Time"})
    )

    if not q2.empty:
        fig2 = px.bar(
            q2,
            x="Vehicle",
            y="Average_Delivery_Time",
            text_auto=".1f",
            labels={
                "Vehicle": "Vehicle Type",
                "Average_Delivery_Time": "Average Delivery Time (minutes)",
            },
        )
        fig2.update_layout(height=420, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig2, use_container_width=True)

        fastest = q2.iloc[0]
        st.markdown(
            f"""
            <div class="insight">
            <b>Key Insight:</b> <b>{fastest["Vehicle"]}</b>
            has the shortest average delivery time at
            <b>{fastest["Average_Delivery_Time"]:.1f} minutes</b>
            in the current selection.
            </div>
            """,
            unsafe_allow_html=True,
        )

with col2:
    st.markdown("#### Agent Performance")
    st.caption(
        "How do agent rating and age relate to delivery time?"
    )

    agent_df = filtered.dropna(
        subset=["Agent_Rating", "Agent_Age", "Delivery_Time", "Agent_Age_Group"]
    )

    if not agent_df.empty:
        fig3 = px.scatter(
            agent_df,
            x="Agent_Rating",
            y="Delivery_Time",
            color="Agent_Age_Group",
            opacity=0.45,
            labels={
                "Agent_Rating": "Agent Rating",
                "Delivery_Time": "Delivery Time (minutes)",
                "Agent_Age_Group": "Age Group",
            },
            hover_data=["Agent_Age", "Vehicle", "Area", "Category"],
        )
        fig3.update_layout(height=420, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig3, use_container_width=True)

        rating_corr = agent_df["Agent_Rating"].corr(
            agent_df["Delivery_Time"]
        )

        if pd.isna(rating_corr):
            relation_text = "A correlation could not be calculated for the current selection."
        elif rating_corr < -0.2:
            relation_text = (
                f"A negative relationship is visible (correlation ≈ {rating_corr:.2f}), "
                "meaning higher ratings tend to be associated with shorter delivery times."
            )
        elif rating_corr > 0.2:
            relation_text = (
                f"A positive relationship is visible (correlation ≈ {rating_corr:.2f}), "
                "meaning higher ratings tend to be associated with longer delivery times."
            )
        else:
            relation_text = (
                f"The linear relationship is weak (correlation ≈ {rating_corr:.2f}), "
                "so rating alone does not strongly explain delivery time."
            )

        st.markdown(
            f"""
            <div class="insight">
            <b>Key Insight:</b> {relation_text}
            </div>
            """,
            unsafe_allow_html=True,
        )


# ------------------------------------------------------------
# Q4 + Q5 — Area and Category
# ------------------------------------------------------------
st.markdown(
    '<h2 class="section-title">🗺️ 4–5. Area & Category Analysis</h2>',
    unsafe_allow_html=True,
)

col3, col4 = st.columns(2)

with col3:
    st.markdown("#### Area Heatmap")
    st.caption("Which areas have the highest average delivery times?")

    q4 = (
        filtered.groupby("Area", as_index=False)["Delivery_Time"]
        .mean()
        .sort_values("Delivery_Time", ascending=False)
    )

    if not q4.empty:
        heat_data = q4.set_index("Area")[["Delivery_Time"]]

        fig4 = px.imshow(
            heat_data,
            text_auto=".1f",
            aspect="auto",
            labels={
                "x": "",
                "y": "Area",
                "color": "Avg Delivery Time (min)",
            },
        )
        fig4.update_layout(height=420, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig4, use_container_width=True)

        worst_area = q4.iloc[0]
        st.markdown(
            f"""
            <div class="insight">
            <b>Key Insight:</b> <b>{worst_area["Area"]}</b>
            has the highest average delivery time in the current selection:
            <b>{worst_area["Delivery_Time"]:.1f} minutes</b>.
            </div>
            """,
            unsafe_allow_html=True,
        )

with col4:
    st.markdown("#### Category Distribution")
    st.caption("Which categories have the highest and most variable times?")

    q5 = filtered.dropna(subset=["Category", "Delivery_Time"])

    if not q5.empty:
        fig5 = px.box(
            q5,
            x="Category",
            y="Delivery_Time",
            points=False,
            labels={
                "Category": "Product Category",
                "Delivery_Time": "Delivery Time (minutes)",
            },
        )
        fig5.update_layout(height=420, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig5, use_container_width=True)

        category_stats = (
            q5.groupby("Category")["Delivery_Time"]
            .agg(["mean", "std"])
            .reset_index()
        )

        highest_mean = category_stats.loc[
            category_stats["mean"].idxmax()
        ]
        most_variable = category_stats.loc[
            category_stats["std"].idxmax()
        ]

        st.markdown(
            f"""
            <div class="insight">
            <b>Key Insight:</b> <b>{highest_mean["Category"]}</b>
            has the highest average delivery time
            ({highest_mean["mean"]:.1f} min), while
            <b>{most_variable["Category"]}</b> has the greatest
            delivery-time variability (SD ≈ {most_variable["std"]:.1f} min).
            </div>
            """,
            unsafe_allow_html=True,
        )


# ------------------------------------------------------------
# Q6 — Time-of-Day Analyzer
# ------------------------------------------------------------
st.markdown(
    '<h2 class="section-title">🕐 6. Time-of-Day Analyzer</h2>',
    unsafe_allow_html=True,
)
st.caption(
    "Does the time of day when an order is placed influence delivery performance?"
)

tod_order = ["Night", "Morning", "Afternoon", "Evening"]

q6 = (
    filtered.dropna(subset=["Time_of_Day"])
    .groupby(["Order_Hour", "Time_of_Day"], as_index=False)["Delivery_Time"]
    .mean()
)

if not q6.empty:
    fig6 = px.bar(
        q6,
        x="Order_Hour",
        y="Delivery_Time",
        color="Time_of_Day",
        text_auto=".1f",
        labels={
            "Order_Hour": "Order Hour",
            "Delivery_Time": "Average Delivery Time (minutes)",
            "Time_of_Day": "Time of Day",
        },
    )
    fig6.update_layout(
        height=440,
        xaxis=dict(dtick=1),
        margin=dict(l=20, r=20, t=20, b=20),
    )
    st.plotly_chart(fig6, use_container_width=True)

    tod_stats = (
        filtered.groupby("Time_of_Day")["Delivery_Time"]
        .mean()
        .reindex(tod_order)
        .dropna()
    )

    if not tod_stats.empty:
        worst_tod = tod_stats.idxmax()
        st.markdown(
            f"""
            <div class="insight">
            <b>Key Insight:</b> <b>{worst_tod}</b> has the highest
            average delivery time in the current selection
            ({tod_stats.max():.1f} minutes).
            </div>
            """,
            unsafe_allow_html=True,
        )


# ------------------------------------------------------------
# Distance Analyzer — derived from coordinates
# ------------------------------------------------------------
st.markdown(
    '<h2 class="section-title">📍 Distance Analyzer</h2>',
    unsafe_allow_html=True,
)
st.caption(
    "Does delivery distance correspond to delivery time?"
)

distance_df = filtered.dropna(
    subset=["Delivery_Distance", "Delivery_Time"]
)

if len(distance_df) >= 2:
    fig_distance = px.scatter(
        distance_df,
        x="Delivery_Distance",
        y="Delivery_Time",
        opacity=0.35,
        trendline="ols",
        labels={
            "Delivery_Distance": "Delivery Distance (km)",
            "Delivery_Time": "Delivery Time (minutes)",
        },
        hover_data=["Vehicle", "Traffic", "Area", "Category"],
    )
    fig_distance.update_layout(
        height=440,
        margin=dict(l=20, r=20, t=20, b=20),
    )
    st.plotly_chart(fig_distance, use_container_width=True)

    distance_corr = distance_df["Delivery_Distance"].corr(
        distance_df["Delivery_Time"]
    )

    st.markdown(
        f"""
        <div class="insight">
        <b>Derived Feature:</b> Delivery Distance is calculated using
        the store and drop latitude/longitude coordinates with the
        Haversine formula.
        <br><br>
        <b>Correlation with delivery time:</b> {distance_corr:.2f}
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.info("Not enough coordinate data for the distance analysis.")


# ------------------------------------------------------------
# Q7 — Pickup Efficiency
# ------------------------------------------------------------
st.markdown(
    '<h2 class="section-title">⏱️ 7. Pickup Efficiency Analyzer</h2>',
    unsafe_allow_html=True,
)
st.caption(
    "Does pickup duration influence the overall delivery time?"
)

pickup_df = filtered.dropna(
    subset=["Pickup_Duration", "Delivery_Time"]
)

if len(pickup_df) >= 2:
    fig7 = px.scatter(
        pickup_df,
        x="Pickup_Duration",
        y="Delivery_Time",
        opacity=0.35,
        trendline="ols",
        labels={
            "Pickup_Duration": "Pickup Duration (minutes)",
            "Delivery_Time": "Delivery Time (minutes)",
        },
        hover_data=["Vehicle", "Traffic", "Area", "Category"],
    )
    fig7.update_layout(
        height=440,
        margin=dict(l=20, r=20, t=20, b=20),
    )
    st.plotly_chart(fig7, use_container_width=True)

    pickup_corr = pickup_df["Pickup_Duration"].corr(
        pickup_df["Delivery_Time"]
    )

    st.markdown(
        f"""
        <div class="insight">
        <b>Derived Feature:</b> Pickup Duration =
        Pickup Time − Order Time.
        <br><br>
        <b>Correlation with delivery time:</b> {pickup_corr:.2f}
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.info("Not enough pickup-time data for this analysis.")


# ------------------------------------------------------------
# Optional visual: delivery-time distribution
# ------------------------------------------------------------
with st.expander("📊 Optional Analysis — Delivery Time Distribution"):
    fig_hist = px.histogram(
        filtered,
        x="Delivery_Time",
        nbins=40,
        labels={"Delivery_Time": "Delivery Time (minutes)"},
    )
    fig_hist.add_vline(
        x=late_threshold,
        line_dash="dash",
        annotation_text="Late threshold",
    )
    fig_hist.update_layout(height=400)
    st.plotly_chart(fig_hist, use_container_width=True)


# ------------------------------------------------------------
# Data quality / methodology
# ------------------------------------------------------------
with st.expander("🧹 Data Preparation & Methodology"):
    st.write(
        """
        **Cleaning**
        - Trimmed whitespace from categorical/text fields.
        - Converted numeric columns to numeric data types.
        - Converted date/time fields into usable datetime values.
        - Removed rows without Delivery_Time.
        - Removed negative Delivery_Time values.
        - Invalid negative Pickup_Duration values are treated as missing.

        **Derived variables**
        - Time_of_Day from Order_Time.
        - Pickup_Duration = Pickup_Time − Order_Time.
        - Delivery_Distance using the Haversine formula from store/drop coordinates.
        - Agent_Age_Group: <25, 25–40, 40+.
        - Late_Delivery = Delivery_Time > mean + 1 standard deviation.

        **Core metrics**
        - Average Delivery Time.
        - Delivery Count.
        - Late Delivery Percentage.
        - Standard deviation for delivery-time variability.
        """
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Raw Records", f"{len(raw_df):,}")
    c2.metric("Cleaned Records", f"{len(df):,}")
    c3.metric("Removed Records", f"{len(raw_df) - len(df):,}")


# ------------------------------------------------------------
# Footer
# ------------------------------------------------------------
st.markdown("---")
st.caption(
    "LOGISIGHT • Same Data. Smarter Decisions. • "
    "FA-2 Dashboarding & Deployment"
)
