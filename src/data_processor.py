import pandas as pd

# =========================
# 🔹 TEMPERATURE HANDLING
# =========================

def get_temperature_columns(df):
    """Auto-detect temperature columns (Channel-based or Temp-based)"""
    return [col for col in df.columns if "channel" in col.lower() or "temp" in col.lower()]


def get_temperature_series(df):

    temp_cols = [col for col in df.columns if "Channel" in col or "Temp" in col]

    if not temp_cols:
        raise ValueError("No temperature columns found")

    # ✅ CLEAN ALL TEMPERATURE COLUMNS
    for col in temp_cols:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace("°C", "", regex=False)
            .str.replace(",", "", regex=False)
            .str.strip()
        )

        # Convert to numeric (VERY IMPORTANT)
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # ✅ Drop rows where all temps are NaN
    df = df.dropna(subset=temp_cols, how="all")

    # ✅ Cold spot calculation
    df["Temp"] = df[temp_cols].min(axis=1)

    return df
print(df[temp_cols].head())
    
# =========================
# 🔹 DATETIME HANDLING
# =========================

def process_datetime(df):
    """Flexible datetime handling (Date+Time / Time only / No time)"""

    if "Date" in df.columns and "Time" in df.columns:
        df["Datetime"] = pd.to_datetime(df["Date"] + " " + df["Time"])

    elif "Time" in df.columns:
        df["Datetime"] = pd.to_datetime(df["Time"])

    else:
        # fallback (1-minute interval)
        df["Datetime"] = pd.date_range(
            start="2025-01-01", periods=len(df), freq="1min"
        )

    return df


# =========================
# 🔹 PHASE DETECTION
# =========================

def detect_phases(df):
    """Classify cycle phases"""

    df["Phase"] = "Preheating"

    # Sterilization (Hold)
    df.loc[(df["Temp"] >= 121) & (df["Temp"] <= 135), "Phase"] = "Sterilization"

    # Cooling
    df.loc[df["Temp"] < 100, "Phase"] = "Cooling"

    return df


# =========================
# 🔹 DATA CLEANING
# =========================

def clean_data(df):
    """Clean temperature & pressure values (if present)"""

    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()

    if "temperature" in df.columns:
        df["temperature"] = (
            df["temperature"]
            .astype(str)
            .str.replace("°C", "", regex=False)
            .str.strip()
            .astype(float)
        )

    if "pressure" in df.columns:
        df["pressure"] = (
            df["pressure"]
            .astype(str)
            .str.replace("kpa", "", regex=False)
            .str.strip()
            .astype(float)
        )

    return df


# =========================
# 🔹 BASIC SUMMARY
# =========================

def process_data(df):
    """Return summary stats"""

    df = clean_data(df)

    summary = {}

    if "temperature" in df.columns:
        summary.update({
            "temp_min": df["temperature"].min(),
            "temp_max": df["temperature"].max(),
            "temp_avg": df["temperature"].mean(),
        })

    if "pressure" in df.columns:
        summary.update({
            "press_min": df["pressure"].min(),
            "press_max": df["pressure"].max(),
            "press_avg": df["pressure"].mean(),
        })

    return summary


# =========================
# 🔹 F0 CALCULATION (UNIVERSAL)
# =========================

def calculate_f0(df):
    """Universal F0 calculation (multi-channel + flexible time)"""

    df = process_datetime(df)
    df = get_temperature_series(df)

    z = 10
    T_ref = 121.1

    # Lethality
    df["F0_increment"] = 10 ** ((df["Temp"] - T_ref) / z)

    # Time delta (minutes)
    df["dt"] = df["Datetime"].diff().dt.total_seconds().fillna(60) / 60

    df["F0"] = df["F0_increment"] * df["dt"]

    return df["F0"].sum()


# =========================
# 🔹 VALIDATION (TEMP + PRESS)
# =========================

def validate_data(df):
    """Check temp and pressure limits"""

    df = clean_data(df)

    deviations = []

    if "temperature" in df.columns:
        temp_fail = df[df["temperature"] < 121]
        deviations.extend(
            [f"Temp low at {row.get('time','N/A')} ({row['temperature']}°C)"
             for _, row in temp_fail.iterrows()]
        )

    if "pressure" in df.columns:
        press_fail = df[df["pressure"] != 115]
        deviations.extend(
            [f"Pressure issue at {row.get('time','N/A')} ({row['pressure']} kPa)"
             for _, row in press_fail.iterrows()]
        )

    status = "PASS" if not deviations else "FAIL"

    return status, deviations


# =========================
# 🔹 F0 VALIDATION
# =========================

def validate_f0(f0_value):
    return "PASS" if f0_value >= 12 else "FAIL"


# =========================
# 🔹 FULL BATCH ANALYSIS
# =========================

def analyze_batch(df):
    """Final batch evaluation"""

    status, deviations = validate_data(df)

    return status, deviations
print(df[temp_cols].head())