import sqlite3
import pandas as pd

conn = sqlite3.connect("Database/traffic_crashes.db")

# Query - Row Count
query = """
SELECT COUNT(*) AS total_rows
FROM CrashTable;
"""

result1 = pd.read_sql(query, conn) #stores total rows of table
print(result1) 
print("-" * 50)

# Query - Schema Information
query = """
PRAGMA table_info(CrashTable); 
"""                             #pragma commands the sqlite for particular action

result2 = pd.read_sql(query, conn)

print("Table Schema")
print(result2)

#Query1-Find the top 5 most dangerous combinations of weather and crash type based on total crashes.  

query1 = """
SELECT
    WEATHER_CONDITION,
    FIRST_CRASH_TYPE,
    COUNT(*) AS total_crashes
FROM CrashTable
GROUP BY WEATHER_CONDITION, FIRST_CRASH_TYPE
ORDER BY total_crashes DESC
LIMIT 5;
"""
                                                #order by arranges the values in high to low with DESC
                                                #group by combines/merge same values into one
result1 = pd.read_sql(query1, conn)

print("Query 1")
print(result1)
result1.to_csv(
    "Results/query1_weather_crash_type.csv",
    index=False
)

#query2-Identify the top 10 streets with the highest number of injury crashes.
query2 = """
SELECT
    STREET_NAME,
    COUNT(*) AS injury_crashes
FROM CrashTable
WHERE INJURIES_TOTAL > 0
GROUP BY STREET_NAME
ORDER BY injury_crashes DESC
LIMIT 10;
"""

result2 = pd.read_sql(query2, conn)

print("\nQuery 2")
print(result2)
result2.to_csv(
    "Results/query2_injury_streets.csv",
    index=False
)

#query3- Find the percentage of crashes that resulted in injuries for each crash type. 
query3 = """
SELECT
    FIRST_CRASH_TYPE,
    ROUND(
        100.0 * SUM(CASE
                        WHEN INJURIES_TOTAL > 0 THEN 1
                        ELSE 0
                    END)
        / COUNT(*),
        2
    ) AS injury_percentage
FROM CrashTable
GROUP BY FIRST_CRASH_TYPE
ORDER BY injury_percentage DESC;
"""
#converts each crash to 1 results no.of crashes caused injuries 
result3 = pd.read_sql(query3, conn)

print("\nQuery 3")
print(result3)
result3.to_csv(
    "Results/query3_injury_percentage.csv",
    index=False
)


#query4-Determine the peak crash hour for each month. 
query4 = """
SELECT CRASH_MONTH, CRASH_HOUR, total_crashes 
FROM (
    SELECT CRASH_MONTH,
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
"""
#inner query uses ROW_NUMBER() with PARTITION BY CRASH_MONTH to rank the hours within each month based on crash count, from highest to lowest
#then all the top hours in each month are picked n displayed in outer query
result4 = pd.read_sql(query4, conn)

print("\nQuery 4")
print(result4)
result4.to_csv(
    "Results/query4_peak_crash_hour.csv",
    index=False
)

#query5-Find the top 5 primary causes of crashes during night time(CRASH_HOUR ≥ 18).  
query5 = """
SELECT
    PRIM_CONTRIBUTORY_CAUSE AS primary_crash_cause,
    COUNT(*) AS total_crashes
FROM CrashTable
WHERE CRASH_HOUR >= 18
GROUP BY primary_crash_cause
ORDER BY total_crashes DESC
LIMIT 5;
"""

result5 = pd.read_sql(query5, conn)

print("\nQuery 5")
print(result5)
result5.to_csv(
    "Results/query5_night_causes.csv",
    index=False
)

#query6-Compare average number of injuries in daylight vs darkness conditions. 
query6 = """
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

GROUP BY LIGHT_GROUP

ORDER BY avg_injuries DESC;
"""
result6 = pd.read_sql(query6, conn)

print("\nQuery 6")
print(result6)
result6.to_csv(
    "Results/query6_daylight_darkness.csv",
    index=False
)

#query7
query7 = """
SELECT
    TRAFFIC_CONTROL_DEVICE,
    ROUND(AVG(INJURIES_TOTAL), 2) AS avg_injuries
FROM CrashTable
GROUP BY TRAFFIC_CONTROL_DEVICE
ORDER BY avg_injuries DESC
LIMIT 1;
"""

result7 = pd.read_sql(query7, conn)

print("\nQuery 7")
print(result7)
result7.to_csv(
    "Results/query7_traffic_control_device.csv",
    index=False
)


#query8
query8 = """
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
"""

result8 = pd.read_sql(query8, conn)

print("\nQuery 8")
print(result8)
result8.to_csv(
    "Results/query8_hot_locations.csv",
    index=False
)
#query9
query9 = """
SELECT
    STREET_NAME,

    COUNT(*) AS total_crashes,

    SUM(
        CASE
            WHEN INJURIES_TOTAL > 0 THEN 1
            ELSE 0
        END
    ) AS injury_crashes,

    ROUND(
        100.0 *
        SUM(
            CASE
                WHEN INJURIES_TOTAL > 0 THEN 1
                ELSE 0
            END
        )
        /
        COUNT(*),
        2
    ) AS injury_rate

FROM CrashTable

GROUP BY STREET_NAME

HAVING COUNT(*) > 100

ORDER BY injury_rate DESC

LIMIT 5;
"""

result9 = pd.read_sql(query9, conn)

print("\nQuery 9")
print(result9)
result9.to_csv(
    "Results/query9_injury_rate_streets.csv",
    index=False
)
#query10
query10 = """
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
"""

result10 = pd.read_sql(query10, conn)

print("\nQuery 10")
print(result10)
result10.to_csv(
    "Results/query10_common_crash_type.csv",
    index=False
)
#query11
query11 = """
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
"""

result11 = pd.read_sql(query11, conn)

print("\nQuery 11")
print(result11)
result11.to_csv(
    "Results/query11_day_of_week.csv",
    index=False
)
#query12
query12 = """
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

ORDER BY total_injuries DESC;
"""

result12 = pd.read_sql(query12, conn)

print("\nQuery 12")
print(result12)
result12.to_csv(
    "Results/query12_time_bucket.csv",
    index=False
)
#query13
query13 = """
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
"""

result13 = pd.read_sql(query13, conn)

print("\nQuery 13")
print(result13)
result13.to_csv(
    "Results/query13_contributing_causes.csv",
    index=False
)

#query14
query14 = """
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
        )
        * 100.0
        /
        LAG(total_crashes)
        OVER (
            ORDER BY year
        ),
        2
    ) AS growth_rate_percent

FROM YearlyCrashes

ORDER BY year;
"""

result14 = pd.read_sql(query14, conn)

print("\nQuery 14")
print(result14)
result14.to_csv(
    "Results/query14_growth_rate.csv",
    index=False
)
#query15
query15 = """
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

result15 = pd.read_sql(query15, conn)

print("\nQuery 15")
print(result15)
result15.to_csv(
    "Results/query15_hotspot_zones.csv",
    index=False
)
conn.close()

