import pandas as pd
import sqlite3
df = pd.read_csv("Data/Traffic_Crashes_Data.csv")
print("Dataset shape:",df.shape)
# Create database connection
conn = sqlite3.connect("Database/traffic_crashes.db")

# Load dataframe into SQLite
df.to_sql(
    "CrashTable",
    conn,
    if_exists="replace",
    index=False
)

print("Data loaded into SQLite successfully!")

conn.close()