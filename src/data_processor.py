def process_data(df):
    result = {}

    # Clean data
    df["temperature"] = df["temperature"].str.replace("°C", "").str.strip().astype(float)
    df["pressure"] = df["pressure"].str.replace("KPa", "").str.strip().astype(float)

    # Temperature
    result["temp_min"] = df["temperature"].min()
    result["temp_max"] = df["temperature"].max()
    result["temp_avg"] = df["temperature"].mean()

    # Pressure
    result["press_min"] = df["pressure"].min()
    result["press_max"] = df["pressure"].max()
    result["press_avg"] = df["pressure"].mean()

    return result

def validate_data(df):
    temp_fail = df[df["temperature"] < 120-121]
    press_fail = df[df["pressure"] != 115]

    if temp_fail.empty and press_fail.empty:
        return "PASS ✅"
    else:
        return f"FAIL ❌ | Temp Issues: {len(temp_fail)} | Pressure Issues: {len(press_fail)}"    


def analyze_batch(df):
    deviations = []

    for _, row in df.iterrows():
        if row["temperature"] < 121:
            deviations.append(f"Temp low at {row['time']} ({row['temperature']}°C)")

        if row["pressure"] != 115:
            deviations.append(f"Pressure issue at {row['time']} ({row['pressure']} KPa)")

    status = "PASS ✅" if len(deviations) == 0 else "FAIL ❌"

    return status, deviations    