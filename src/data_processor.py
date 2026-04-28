import pandas as pd


# =========================
# 🔹 CLEANING FUNCTION
# =========================
def clean_data(df):
    df = df.copy()

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower()

    # Clean temperature
    df["temperature"] = (
        df["temperature"]
        .astype(str)
        .str.replace("°C", "", regex=False)
        .str.strip()
        .astype(float)
    )

    # Clean pressure
    df["pressure"] = (
        df["pressure"]
        .astype(str)
        .str.replace("KPa", "", regex=False)
        .str.strip()
        .astype(float)
    )

    return df


# =========================
# 🔹 PROCESS DATA
# =========================
def process_data(df):
    df = clean_data(df)

    return {
        "temp_min": df["temperature"].min(),
        "temp_max": df["temperature"].max(),
        "temp_avg": df["temperature"].mean(),
        "press_min": df["pressure"].min(),
        "press_max": df["pressure"].max(),
        "press_avg": df["pressure"].mean(),
    }


# =========================
# 🔹 F0 CALCULATION
# =========================
def calculate_f0(df):
    df = clean_data(df)

    F0 = 0
    for T in df["temperature"]:
        contribution = 10 ** ((T - 121) / 10)
        F0 += contribution  # assuming 1 min interval

    return F0


# =========================
# 🔹 VALIDATION (TEMP + PRESS)
# =========================
def validate_data(df):
    df = clean_data(df)

    temp_fail = df[df["temperature"] < 121]
    press_fail = df[df["pressure"] != 115]

    if temp_fail.empty and press_fail.empty:
        return "PASS"
    else:
        return (
            f"FAIL  | Temp Issues: {len(temp_fail)} "
            f"| Pressure Issues: {len(press_fail)}"
        )


# =========================
# 🔹 F0 VALIDATION
# =========================
def validate_f0(f0_value):
    return "PASS" if f0_value >= 12 else "FAIL"


# =========================
# 🔹 FULL BATCH ANALYSIS
# =========================
def analyze_batch(df):
    df = clean_data(df)

    deviations = []

    for _, row in df.iterrows():

        if row["temperature"] < 121:
            deviations.append(
                f"Temp low at {row['time']} ({row['temperature']}°C)"
            )

        if row["pressure"] != 115:
            deviations.append(
                f"Pressure issue at {row['time']} ({row['pressure']} KPa)"
            )

    status = "PASS" if not deviations else "FAIL"

    return status, deviations