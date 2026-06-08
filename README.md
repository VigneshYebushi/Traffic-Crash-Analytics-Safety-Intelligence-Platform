# Traffic Crash Analytics & Safety Intelligence Platform

## Project Overview

This project analyzes Chicago Traffic Crash data using Python, SQLite, SQL, Pandas, and Streamlit.

The objective is to identify crash patterns, injury trends, hotspot locations, high-risk time periods, and contributing factors that affect road safety.

---

## Technologies Used

* Python
* SQLite
* Pandas
* Streamlit
* SQL

---

## Project Structure

TRAFFIC_CRASH_PROJECT

* Data/

  * Traffic_CrashesData.csv (Source Dataset)

* Database/

  * traffic_crashes.db (SQLite Database)

* Results/

  * Query Result CSV Files

* load_data.py

  * Loads CSV data into SQLite

* analysis_queries.py

  * Executes and validates SQL queries

* streamlit_app.py

  * Main application for dashboard visualization

* Traffic_Crash_Analytics.pptx

  * Project Presentation

* Traffic_Crash_Analytics.pdf

  * Project Presentation (PDF Version)

* README.md

  * Project Documentation

---

## Features

* Load traffic crash data into SQLite database
* Execute 15 SQL analytical queries
* Generate business insights
* Export query results to CSV
* Interactive Streamlit dashboard

---

## Installation & Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/<your-username>/Traffic_Crash_Project.git
```

### Step 2: Navigate to the Project Directory

```bash
cd Traffic_Crash_Project
```

### Step 3: Install Required Dependencies

```bash
pip install pandas streamlit
```

### Step 4: Load the Dataset into SQLite

```bash
python load_data.py
```

This creates the SQLite database and loads the crash records into the `CrashTable`.

### Step 5: (Optional) Execute SQL Queries

```bash
python analysis_queries.py
```

This script executes all analytical SQL queries and generates query result files.

### Step 6: Launch the Streamlit Dashboard

```bash
streamlit run streamlit_app.py
```

### Step 7: Open the Dashboard

After running the above command, open the local URL displayed in the terminal:

```text
http://localhost:8501
```

You can now explore crash analysis results, business insights, and dashboard visualizations interactively.



---

## Key Analysis Performed

1. Weather and crash type analysis
2. Injury hotspot streets
3. Injury percentage by crash type
4. Peak crash hour analysis
5. Night-time crash causes
6. Daylight vs darkness injury comparison
7. Traffic control device impact analysis
8. Crash hotspot location identification
9. Street injury rate analysis
10. Year-wise crash type trends
11. Day-of-week crash analysis
12. High-risk time period analysis
13. Contributing cause analysis
14. Year-over-year crash growth analysis
15. Hotspot zone identification

---

## Author

Vignesh Yebushi
