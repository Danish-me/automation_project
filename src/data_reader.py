import pandas as pd

def read_excel(file_path):
    df = pd.read_excel(file_path, header=0)

    # Clean columns
    df.columns = df.columns.str.strip()

    # ✅ Handle Date + Time
    if "Date" in df.columns and "Time" in df.columns:
        df["Datetime"] = pd.to_datetime(df["Date"].astype(str) + " " + df["Time"].astype(str))
    elif "Time" in df.columns:
        df["Datetime"] = pd.to_datetime(df["Time"])
    else:
        df["Datetime"] = pd.date_range(start="2025-01-01", periods=len(df), freq="1min")

    return df