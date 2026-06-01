import streamlit as st
import sqlite3
import pandas as pd

# Page Config
st.set_page_config(
    page_title="Traffic Crash Analytics",
    layout="wide"
)

# Title
st.title(
    "Traffic Crash Analytics & Safety Intelligence Platform"
)

st.write(
    "Chicago Traffic Crash Analysis using SQLite, Python and Streamlit"
)

# Sidebar
st.sidebar.title("Navigation")

page = st.sidebar.selectbox(
    "Select Section",
    [
        "Project Overview",
        "Query Results"
    ]
)

# Database Connection
conn = sqlite3.connect(
    "Database/traffic_crashes.db"
)

# Dashboard Metrics
total_crashes = pd.read_sql(
    """
    SELECT COUNT(*) AS total
    FROM CrashTable
    """,
    conn
).iloc[0, 0]

total_years = pd.read_sql(
    """
    SELECT COUNT(DISTINCT year)
    FROM CrashTable
    """,
    conn
).iloc[0, 0]

total_types = pd.read_sql(
    """
    SELECT COUNT(DISTINCT FIRST_CRASH_TYPE)
    FROM CrashTable
    """,
    conn
).iloc[0, 0]

# Project Overview Page
if page == "Project Overview":

    st.header("Project Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Crashes",
        f"{total_crashes:,}"
    )

    col2.metric(
        "Years Covered",
        total_years
    )

    col3.metric(
        "Crash Types",
        total_types
    )

# Query Results Page
if page == "Query Results":

    st.header("SQL Query Results")

    query_files = {
        "Query 1": "Results/query1_weather_crash_type.csv",
        "Query 2": "Results/query2_injury_streets.csv",
        "Query 3": "Results/query3_injury_percentage.csv",
        "Query 4": "Results/query4_peak_crash_hour.csv",
        "Query 5": "Results/query5_night_causes.csv",
        "Query 6": "Results/query6_daylight_darkness.csv",
        "Query 7": "Results/query7_traffic_control_device.csv",
        "Query 8": "Results/query8_hot_locations.csv",
        "Query 9": "Results/query9_injury_rate_streets.csv",
        "Query 10": "Results/query10_common_crash_type.csv",
        "Query 11": "Results/query11_day_of_week.csv",
        "Query 12": "Results/query12_time_bucket.csv",
        "Query 13": "Results/query13_contributing_causes.csv",
        "Query 14": "Results/query14_growth_rate.csv",
        "Query 15": "Results/query15_hotspot_zones.csv"
    }

    selected_query = st.selectbox(
        "Select Query",
        list(query_files.keys())
    )

    df = pd.read_csv(
        query_files[selected_query]
    )
    query_descriptions = {
    "Query 1": "Top 5 most dangerous weather and crash type combinations.",
    "Query 2": "Streets with highest injury counts.",
    "Query 3": "Percentage of crashes resulting in injuries.",
    "Query 4": "Peak crash hour for each crash type.",
    "Query 5": "Most common causes of nighttime crashes.",
    "Query 6": "Comparison of average injuries in daylight vs darkness.",
    "Query 7": "Traffic control device with highest average injuries.",
    "Query 8": "Top 5 crash hotspot locations.",
    "Query 9": "Streets with highest injury rates.",
    "Query 10": "Most common crash type by year.",
    "Query 11": "Day of week with highest average crashes per hour.",
    "Query 12": "High-risk time periods based on injuries.",
    "Query 13": "Top contributing causes for each crash type.",
    "Query 14": "Year-over-year crash growth analysis using LAG().",
    "Query 15": "Top hotspot zones using rounded coordinates."
}

    st.subheader(selected_query)

    st.info(
        query_descriptions[selected_query]
    )

    st.dataframe(
        df,
        use_container_width=True
    )
conn.close()