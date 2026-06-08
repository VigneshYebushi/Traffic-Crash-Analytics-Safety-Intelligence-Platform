import streamlit as st
import sqlite3
import pandas as pd

# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="Traffic Crash Analytics",
    layout="wide"
)

# -------------------------
# Title
# -------------------------
st.title("Traffic Crash Analytics & Safety Intelligence Platform")

st.write(
    "Chicago Traffic Crash Analysis using SQLite, Python and Streamlit"
)

# -------------------------
# Sidebar
# -------------------------
st.sidebar.title("Navigation")

page = st.sidebar.selectbox(
    "Select Section",
    [
        "Project Overview",
        "Query Results"
    ]
)

# -------------------------
# Database Connection
# -------------------------
conn = sqlite3.connect(
    "Database/traffic_crashes.db"
)

# -------------------------
# Dashboard Metrics
# -------------------------
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

# -------------------------
# Project Overview Page
# -------------------------
if page == "Project Overview":

    st.header("Project Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Crashes",
        f"{total_crashes:,}"
    )

    col2.metric(
        "Years Covered",
        int(total_years)
    )

    col3.metric(
        "Crash Types",
        int(total_types)
    )

# -------------------------
# Query Results Page
# -------------------------
elif page == "Query Results":

    st.header("SQL Query Results")

    query_sql = {

        "Query 1": """
        SELECT
            WEATHER_CONDITION,
            FIRST_CRASH_TYPE,
            COUNT(*) AS total_crashes
        FROM CrashTable
        GROUP BY WEATHER_CONDITION, FIRST_CRASH_TYPE
        ORDER BY total_crashes DESC
        LIMIT 5;
        """,

        "Query 2": """
        SELECT
            STREET_NAME,
            COUNT(*) AS injury_crashes
        FROM CrashTable
        WHERE INJURIES_TOTAL > 0
        GROUP BY STREET_NAME
        ORDER BY injury_crashes DESC
        LIMIT 10;
        """,

        "Query 3": """
        SELECT
            FIRST_CRASH_TYPE,
            ROUND(
                100.0 *
                SUM(
                    CASE
                        WHEN INJURIES_TOTAL > 0
                        THEN 1
                        ELSE 0
                    END
                ) / COUNT(*),
                2
            ) AS injury_percentage
        FROM CrashTable
        GROUP BY FIRST_CRASH_TYPE
        ORDER BY injury_percentage DESC;
        """,

        "Query 4": """
        SELECT CRASH_MONTH, CRASH_HOUR, total_crashes 
        FROM (
            SELECT 
                CRASH_MONTH,
                CRASH_HOUR,
                COUNT(*) AS total_crashes,
                ROW_NUMBER() OVER(
                    PARTITION BY CRASH_MONTH
                    ORDER BY COUNT(*) DESC
                ) AS rn
            FROM CrashTable
            GROUP BY CRASH_MONTH, CRASH_HOUR
        )
        WHERE rn = 1
        ORDER BY CRASH_MONTH;
        """,

        "Query 5": """
        SELECT
            PRIM_CONTRIBUTORY_CAUSE AS primary_crash_cause,
            COUNT(*) AS total_crashes
        FROM CrashTable
        WHERE CRASH_HOUR >= 18
        GROUP BY PRIM_CONTRIBUTORY_CAUSE
        ORDER BY total_crashes DESC
        LIMIT 5;
        """,
        "Query 6": """
        SELECT
            CASE
                WHEN LIGHTING_CONDITION = 'DAYLIGHT'
                    THEN 'DAYLIGHT'
                WHEN LIGHTING_CONDITION IN (
                    'DARKNESS',
                    'DARKNESS, LIGHTED ROAD'
                )
                    THEN 'DARKNESS'
                ELSE 'OTHER'
            END AS LIGHT_GROUP,
            ROUND(AVG(INJURIES_TOTAL), 2) AS avg_injuries
        FROM CrashTable
        GROUP BY light_group
        ORDER BY avg_injuries DESC;
        """,

        "Query 7": """
        SELECT
            TRAFFIC_CONTROL_DEVICE,
            ROUND(AVG(INJURIES_TOTAL), 2) AS avg_injuries
        FROM CrashTable
        GROUP BY TRAFFIC_CONTROL_DEVICE
        ORDER BY avg_injuries DESC
        LIMIT 1;
        """,

        "Query 8": """
        SELECT
            LATITUDE,
            LONGITUDE,
            COUNT(*) AS total_crashes
        FROM CrashTable
        WHERE LATITUDE IS NOT NULL
                AND LONGITUDE IS NOT NULL
        GROUP BY LATITUDE, LONGITUDE
        ORDER BY total_crashes DESC
        LIMIT 5;
        """,

        "Query 9": """
        SELECT
            STREET_NAME,
            COUNT(*) AS total_crashes,
            SUM(CASE
                    WHEN INJURIES_TOTAL > 0 THEN 1
                    ELSE 0
                END
            )AS injury_crashes,
            ROUND(
                100.0 *
                SUM(CASE
                        WHEN INJURIES_TOTAL > 0 THEN 1
                        ELSE 0
                    END) / 
                COUNT(*),
                2
            ) AS injury_rate
        FROM CrashTable
        GROUP BY STREET_NAME
        HAVING COUNT(*) > 100
        ORDER BY injury_rate DESC
        LIMIT 5;
        """,

        "Query 10": """
        WITH CrashCounts AS (
            SELECT
                year,
                FIRST_CRASH_TYPE,
                COUNT(*) AS total_crashes
            FROM CrashTable
            GROUP BY year, FIRST_CRASH_TYPE
        ),
        RankedCrashTypes AS (
            SELECT
                year,
                FIRST_CRASH_TYPE,
                total_crashes,
                ROW_NUMBER() OVER (
                    PARTITION BY year
                    ORDER BY total_crashes DESC
                ) AS rn
            FROM CrashCounts
        )
        SELECT
            year,
            FIRST_CRASH_TYPE,
            total_crashes
        FROM RankedCrashTypes
        WHERE rn = 1
        ORDER BY year;
        """,
    
        "Query 11": """
        WITH DayHourCounts AS (
            SELECT
                CRASH_DAY_OF_WEEK,
                CRASH_HOUR,
                COUNT(*) AS crash_count
            FROM CrashTable
            GROUP BY CRASH_DAY_OF_WEEK, CRASH_HOUR
        )
        SELECT
            CRASH_DAY_OF_WEEK,
            ROUND(AVG(crash_count), 2) AS avg_crashes_per_hour
        FROM DayHourCounts
        GROUP BY CRASH_DAY_OF_WEEK
        ORDER BY avg_crashes_per_hour DESC
        LIMIT 1;
        """,

        "Query 12": """
        SELECT
            CASE
                WHEN CRASH_HOUR BETWEEN 6 AND 11
                    THEN 'Morning'
                WHEN CRASH_HOUR BETWEEN 12 AND 17
                    THEN 'Afternoon'
                WHEN CRASH_HOUR BETWEEN 18 AND 23
                    THEN 'Evening'
                ELSE 'Night'
            END AS time_bucket,
            SUM(INJURIES_TOTAL) AS total_injuries
        FROM CrashTable
        GROUP BY time_bucket
        ORDER BY total_injuries DESC
        LIMIT 1;
        """,

        "Query 13": """
        WITH CauseCounts AS (
            SELECT
                FIRST_CRASH_TYPE,
                PRIM_CONTRIBUTORY_CAUSE,
                COUNT(*) AS total_crashes
        FROM CrashTable
        GROUP BY
            FIRST_CRASH_TYPE,
            PRIM_CONTRIBUTORY_CAUSE
        ),
        RankedCauses AS (
            SELECT
                FIRST_CRASH_TYPE,
                PRIM_CONTRIBUTORY_CAUSE,
                total_crashes,
                ROW_NUMBER() OVER (
                    PARTITION BY FIRST_CRASH_TYPE
                    ORDER BY total_crashes DESC
                ) AS rn
            FROM CauseCounts
        )
        SELECT
            FIRST_CRASH_TYPE,
            PRIM_CONTRIBUTORY_CAUSE,
            total_crashes
        FROM RankedCauses
        WHERE rn <= 3
        ORDER BY
            FIRST_CRASH_TYPE,
            rn;
        """,

        "Query 14": """
        WITH YearlyCrashes AS (
            SELECT
                year,
                COUNT(*) AS total_crashes
            FROM CrashTable
            GROUP BY year
        )
        SELECT
            year,
            total_crashes,
            LAG(total_crashes)
            OVER (
                ORDER BY year
            ) AS previous_year_crashes,
        ROUND(
            (
                total_crashes -
                LAG(total_crashes)
                OVER (
                    ORDER BY year
                )
            ) * 100.0 /
            LAG(total_crashes)
            OVER (
                ORDER BY year
            ),
            2
        ) AS growth_rate_percent
    FROM YearlyCrashes
    ORDER BY year;
    """,

    "Query 15": """ 
    SELECT
        ROUND(LATITUDE, 2) AS zone_latitude,
        ROUND(LONGITUDE, 2) AS zone_longitude,
        COUNT(*) AS total_crashes
    FROM CrashTable
    WHERE LATITUDE IS NOT NULL
        AND LONGITUDE IS NOT NULL   
    GROUP BY
        ROUND(LATITUDE, 2),
        ROUND(LONGITUDE, 2)
    ORDER BY total_crashes DESC
    LIMIT 10;
    """
        }

    selected_query = st.selectbox(
        "Select Query",
        list(query_sql.keys())
    )

    df = pd.read_sql(
        query_sql[selected_query],
        conn
    )

    query_descriptions = {

        "Query 1":
        "Top 5 most dangerous weather and crash type combinations.",

        "Query 2":
        "Streets with highest injury counts.",

        "Query 3":
        "Percentage of crashes resulting in injuries.",

        "Query 4":
        "Peak crash hour analysis.",

        "Query 5":
        "Most common causes of nighttime crashes.",

        "Query 6":
        "Comparison of average injuries in daylight vs darkness.",

        "Query 7":
        "Traffic control devices with highest average injuries.",

        "Query 8":
        "Top 5 crash hotspot locations.",

        "Query 9":
        "Streets with highest injury rates.",

        "Query 10":
        "Most common crash type by year.",
        
        "Query 11": 
        "Day of week with highest average crashes per hour.",
        
        "Query 12": 
        "High-risk time periods based on injuries.",
        
        "Query 13":
        "Top contributing causes for each crash type.",
        
        "Query 14": 
        "Year-over-year crash growth analysis using LAG().",
    
        "Query 15": 
        "Top hotspot zones using rounded coordinates."
    }

    business_insights = {

        "Query 1":
        "Clear weather conditions account for most crashes, indicating that traffic volume and driver behavior play a greater role than weather.",

        "Query 2":
        "A small number of streets contribute disproportionately to injury crashes and should be prioritized for safety measures.",

        "Query 3":
        "Certain crash types result in injuries more frequently, helping identify high-risk crash categories.",

        "Query 4":
        "Peak crash hours vary across months, enabling better traffic monitoring and resource allocation.",

        "Query 5":
        "Nighttime crashes are strongly linked to driver behavior and reduced visibility conditions.",

        "Query 6":
        "Darkness conditions show higher average injuries, highlighting the importance of visibility improvements.",

        "Query 7":
        "Specific traffic control devices are associated with higher injury severity and may require further evaluation.",

        "Query 8":
        "Crash hotspots can be targeted for enforcement, engineering improvements, and public awareness programs.",

        "Query 9":
        "Some streets have high injury rates despite lower crash volumes, indicating greater crash severity.",

        "Query 10":
        "The most common crash type changes over time, revealing evolving traffic patterns.",

        "Query 11":
        "Certain days of the week experience consistently higher crash activity and require focused interventions.",

        "Query 12":
        "Afternoon and evening periods contribute the highest injury burden and should receive priority attention.",

        "Query 13":
        "Driver-related factors remain the leading contributors across multiple crash categories.",

        "Query 14":
        "Growth trends help assess whether road safety initiatives are improving or worsening crash outcomes.",

        "Query 15":
        "Hotspot zones identify geographic regions requiring immediate safety improvements."
    }
    st.subheader(selected_query)

    st.info(
        query_descriptions[selected_query]
    )

    st.dataframe(
        df,
        width="stretch"
    )
    
    st.success(
    business_insights[selected_query]
    )

# -------------------------
# Close Connection
# -------------------------
conn.close()