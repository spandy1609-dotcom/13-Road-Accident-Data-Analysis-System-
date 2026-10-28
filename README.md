# Road Accident Data Analysis System

A beginner-friendly Python project to analyze recorded road accident patterns by date/time, region, road, vehicle type, severity, and optional weather. It includes a Streamlit dashboard, CSV data management, simple validation, sample synthetic records, and charts.

## Features
- Upload an accident CSV file
- View total records, monthly trends, hourly patterns, region counts, vehicle types, and severity distribution
- Add a record through the app
- Check for missing/invalid dates and missing key fields
- Export currently loaded records to CSV
- Uses only non-identifying fields

## Tech stack
- Python
- Pandas and NumPy
- Matplotlib
- Streamlit
- CSV storage; optional MySQL schema is included in `sql/schema.sql`

## Setup (Windows)
1. Install Python 3.10 or newer.
2. Extract the ZIP file.
3. Open Command Prompt in the extracted project folder.
4. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
6. Run the dashboard:
   ```bash
   streamlit run app.py
   ```
7. Open the local address printed by Streamlit in your browser.

## Sample dataset
The `data/accidents.csv` file contains synthetic demonstration records. It is not official accident data and must not be presented as real-world evidence.

## CSV format
Required columns:
- `accident_datetime` — date and time such as `2026-01-10 08:30:00`
- `region`
- `road_name`
- `vehicle_type`
- `severity` — suggested values: `Minor`, `Serious`, `Fatal`, `Unknown`

Optional:
- `weather`

No personally identifying information should be included.

## MySQL option
Run `sql/schema.sql` in MySQL Workbench to create the database and tables. The Streamlit demo uses CSV storage by default so it can run without a database server. The schema is provided for a MySQL extension.

## Limitations
- Counts are counts of records, not crash risk rates.
- More records in an area do not automatically mean the area is more dangerous; traffic volume, population, reporting practices, and data coverage matter.
- Observational patterns do not prove causation.
- The included dataset is synthetic.
