import matplotlib.pyplot as plt

def plot_temperature(df):

    # 🔹 Clean temperature
    df["temperature"] = (
        df["temperature"]
        .astype(str)
        .str.replace("°C", "")
        .str.strip()
        .astype(float)
    )

    # 🔹 Time column (string for display)
    time = df["time"].astype(str)

    # 🔹 Temperature values
    temp = df["temperature"]

    # 🔹 Create plot
    plt.figure(figsize=(10, 5))

    # Line plot
    plt.plot(time, temp, marker='o')

    # 🔥 Highlight threshold line (IMPORTANT for validation)
    plt.axhline(y=121, linestyle='--')

    # Labels
    plt.title("Temperature vs Time")
    plt.xlabel("Time")
    plt.ylabel("Temperature (°C)")

    # Rotate time labels (fix your earlier issue)
    plt.xticks(rotation=45)

    # Layout fix
    plt.tight_layout()

    # Save graph
    plt.savefig("output/temperature_graph.png")

    return plt