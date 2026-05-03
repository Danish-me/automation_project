import pandas as pd

# =========================
# 🔹 STANDARDIZE COLUMNS
# =========================

def standardize_columns(df):
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()
    return df


# =========================
# 🔹 TEMPERATURE HANDLING
# =========================

def get_temperature_columns(df):
    return [col for col in df.columns if "channel" in col or "temp" in col]


def clean_temperature(df):
    temp_cols = get_temperature_columns(df)

    if not temp_cols:
        raise ValueError("No temperature columns found")

    for col in temp_cols:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace("°c", "", regex=False)
            .str.replace(",", "", regex=False)
            .str.strip()
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=temp_cols, how="all")

    # Cold spot (minimum temp)
    df["temp"] = df[temp_cols].min(axis=1)

    return df, temp_cols


# =========================
# 🔹 DATETIME HANDLING
# =========================

def process_datetime(df):

    if "date" in df.columns and "time" in df.columns:
        df["datetime"] = pd.to_datetime(df["date"] + " " + df["time"])

    elif "time" in df.columns:
        df["datetime"] = pd.to_datetime(df["time"])

    else:
        df["datetime"] = pd.date_range(
            start="2025-01-01", periods=len(df), freq="1min"
        )

    return df


# =========================
# 🔹 F0 CALCULATION
# =========================

def calculate_f0(df):

    df = standardize_columns(df)
    df = process_datetime(df)
    df, temp_cols = clean_temperature(df)

    z = 10
    T_ref = 121.1

    df["f0_increment"] = 10 ** ((df["temp"] - T_ref) / z)

    df["dt"] = df["datetime"].diff().dt.total_seconds().fillna(60) / 60

    df["f0"] = df["f0_increment"] * df["dt"]

    return round(df["f0"].sum(), 2)


# =========================
# 🔹 VALIDATION
# =========================

def validate_data(df):

    df = standardize_columns(df)
    df, temp_cols = clean_temperature(df)

    deviations = []

    for col in temp_cols:
        low_temp = df[df[col] < 121]

        for _, row in low_temp.iterrows():
            time_val = row.get("time", "N/A")
            deviations.append(f"{col} low at {time_val} ({row[col]}°C)")

    status = "PASS" if not deviations else "FAIL"

    return status, deviations


# =========================
# 🔹 F0 VALIDATION
# =========================

def validate_f0(f0_value):
    return "PASS" if f0_value >= 12 else "FAIL"


# =========================
# 🔹 FINAL ANALYSIS
# =========================

def analyze_batch(df):

    f0_value = calculate_f0(df)
    f0_status = validate_f0(f0_value)

    temp_status, deviations = validate_data(df)

    # FINAL DECISION (GxP logic)
    final_status = "PASS" if (f0_status == "PASS" and temp_status == "PASS") else "FAIL"

    return {
        "f0_value": f0_value,
        "f0_status": f0_status,
        "temp_status": temp_status,
        "final_status": final_status,
        "deviations": deviations
    }