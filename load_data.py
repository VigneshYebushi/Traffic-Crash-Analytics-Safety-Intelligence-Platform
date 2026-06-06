import pandas as pd
import sqlite3 #version3 of sqlite
df = pd.read_csv("Data/Traffic_Crashes_Data.csv")
print("Dataset shape:",df.shape)#returns rows n columns of dataset
conn = sqlite3.connect("Database/traffic_crashes.db")
"""
creates the db file inside the database folder if not exists
if exists directly open the db file 
then the database folder is connected to sqlite
"""

df.to_sql(        #converts df to sql
    "CrashTable", #creating the table inside db
    conn,
    if_exists="replace",
    index=False
)
print("Data loaded into SQLite successfully!")
conn.close() 