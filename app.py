import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
DATA_FILE = DATA_DIR / "accidents.csv"

st.set_page_config(page_title="Road Accident Data Analysis", page_icon="🚦", layout="wide")
st.title("🚦 Road Accident Data Analysis System")
st.caption("Analyze recorded accident patterns by time, location, vehicle type, severity, and weather.")

REQUIRED = ["accident_datetime", "region", "road_name", "vehicle_type", "severity"]
OPTIONAL = ["weather"]

def load_data():
    if DATA_FILE.exists():
        df = pd.read_csv(DATA_FILE)
        return df
    return pd.DataFrame(columns=REQUIRED + OPTIONAL)

def validate_data(df):
    issues = []
    missing_cols = [c for c in REQUIRED if c not in df.columns]
    if missing_cols:
        issues.append("Missing required columns: " + ", ".join(missing_cols))
        return issues
    parsed = pd.to_datetime(df["accident_datetime"], errors="coerce")
    bad_dates = int(parsed.isna().sum())
    if bad_dates:
        issues.append(f"{bad_dates} row(s) have missing or invalid accident date/time.")
    for col in ["region", "road_name", "vehicle_type", "severity"]:
        missing = int(df[col].isna().sum() + (df[col].astype(str).str.strip() == "").sum())
        if missing:
            issues.append(f"{missing} row(s) have missing {col} values.")
    allowed = {"Minor", "Serious", "Fatal", "Unknown"}
    invalid_severity = int((~df["severity"].fillna("Unknown").astype(str).str.title().isin(allowed)).sum())
    if invalid_severity:
        issues.append(f"{invalid_severity} row(s) have severity outside: Minor, Serious, Fatal, Unknown.")
    return issues

df = load_data()
with st.sidebar:
    st.header("Data source")
    upload = st.file_uploader("Upload accident CSV", type=["csv"])
    if upload is not None:
        try:
            df = pd.read_csv(upload)
            st.success("Uploaded CSV loaded for this session.")
        except Exception as exc:
            st.error(f"Could not read CSV: {exc}")
    st.markdown("---")
    st.caption("Demo dataset is synthetic. Replace it with public or properly anonymized records.")

tab1, tab2, tab3 = st.tabs(["Dashboard", "Explore records", "Data quality"])

with tab1:
    if df.empty:
        st.info("No records found. Add a CSV in the sidebar or use the included sample dataset.")
    else:
        issues = validate_data(df)
        work = df.copy()
        work["accident_datetime"] = pd.to_datetime(work["accident_datetime"], errors="coerce")
        work["severity"] = work["severity"].fillna("Unknown").astype(str).str.title()
        work["region"] = work["region"].fillna("Unknown").astype(str)
        work["vehicle_type"] = work["vehicle_type"].fillna("Unknown").astype(str)
        work["month"] = work["accident_datetime"].dt.to_period("M").astype(str)
        work["hour"] = work["accident_datetime"].dt.hour
        c1, c2, c3 = st.columns(3)
        c1.metric("Recorded accidents", f"{len(work):,}")
        c2.metric("Locations/regions", f"{work['region'].nunique():,}")
        c3.metric("Rows with invalid date/time", f"{work['accident_datetime'].isna().sum():,}")
        st.warning("Counts show recorded accidents only; they do not prove what caused accidents.")
        left, right = st.columns(2)
        with left:
            st.subheader("Accidents by month")
            monthly = work.dropna(subset=["accident_datetime"]).groupby("month").size()
            if not monthly.empty:
                fig, ax = plt.subplots()
                monthly.plot(kind="bar", ax=ax)
                ax.set_xlabel("Month")
                ax.set_ylabel("Recorded accidents")
                ax.tick_params(axis="x", rotation=45)
                fig.tight_layout()
                st.pyplot(fig)
                plt.close(fig)
            else:
                st.info("No valid dates available for monthly chart.")
        with right:
            st.subheader("Severity distribution")
            severity_counts = work["severity"].value_counts()
            if not severity_counts.empty:
                fig, ax = plt.subplots()
                severity_counts.plot(kind="bar", ax=ax)
                ax.set_xlabel("Recorded severity")
                ax.set_ylabel("Number of records")
                ax.tick_params(axis="x", rotation=0)
                fig.tight_layout()
                st.pyplot(fig)
                plt.close(fig)
        left, right = st.columns(2)
        with left:
            st.subheader("Regions with most records")
            region_counts = work["region"].value_counts().head(10)
            st.bar_chart(region_counts)
        with right:
            st.subheader("Vehicle types")
            vehicle_counts = work["vehicle_type"].value_counts()
            st.bar_chart(vehicle_counts)
        st.subheader("Recorded accidents by hour of day")
        hourly = work.dropna(subset=["accident_datetime"]).groupby("hour").size().reindex(range(24), fill_value=0)
        st.line_chart(hourly)

with tab2:
    st.subheader("Accident records")
    if df.empty:
        st.info("Upload a CSV or add records to data/accidents.csv.")
    else:
        st.dataframe(df, use_container_width=True)
        csv_bytes = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download current records as CSV", csv_bytes, "accidents_export.csv", "text/csv")
    st.markdown("### Add one record")
    with st.form("add_record"):
        dcol1, dcol2 = st.columns(2)
        date_value = dcol1.date_input("Accident date")
        time_value = dcol2.time_input("Accident time")
        region = st.text_input("Region / area")
        road_name = st.text_input("Road name (optional)", value="")
        vehicle = st.selectbox("Vehicle type", ["Car", "Motorcycle", "Bus", "Truck", "Auto-rickshaw", "Bicycle", "Pedestrian", "Other", "Unknown"])
        severity = st.selectbox("Recorded severity", ["Minor", "Serious", "Fatal", "Unknown"])
        weather = st.selectbox("Weather (optional)", ["Unknown", "Clear", "Rain", "Fog", "Other"])
        submitted = st.form_submit_button("Save record")
        if submitted:
            if not region.strip():
                st.error("Please enter a region / area.")
            else:
                new_row = {
                    "accident_datetime": f"{date_value} {time_value}",
                    "region": region.strip(),
                    "road_name": road_name.strip(),
                    "vehicle_type": vehicle,
                    "severity": severity,
                    "weather": weather
                }
                current = load_data()
                current = pd.concat([current, pd.DataFrame([new_row])], ignore_index=True)
                current.to_csv(DATA_FILE, index=False)
                st.success("Record saved to data/accidents.csv. Refresh the page to update dashboard.")

with tab3:
    st.subheader("Data quality checks")
    if df.empty:
        st.info("No data to validate yet.")
    else:
        issues = validate_data(df)
        st.write(f"**Rows checked:** {len(df)}")
        if issues:
            for issue in issues:
                st.warning(issue)
        else:
            st.success("No issues found by the basic validation checks.")
        st.markdown("**Privacy reminder:** Do not upload names, phone numbers, vehicle registration numbers, exact personal addresses, or other identifying details.")
        st.markdown("**Interpretation reminder:** Location/time counts are descriptive associations, not proof of causation. Consider population, traffic volume, and reporting differences before comparing locations.")
