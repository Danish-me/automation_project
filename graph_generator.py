import matplotlib.pyplot as plt
import os

from data_processor import (
    get_temperature_series,
    process_datetime,
    detect_phases
)

def plot_temperature(df):

    df = process_datetime(df)
    df = get_temperature_series(df)
    df = detect_phases(df)

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(df["datetime"], df["temp"], label="Temperature (°C)")

    steril_df = df[df["phase"] == "Sterilization"]

    if not steril_df.empty:
        ax.fill_between(
            steril_df["datetime"],
            steril_df["temp"],
            alpha=0.3,
            label="Sterilization Phase"
        )

    ax.set_xlabel("Time")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("Autoclave Temperature Profile")
    ax.legend()
    ax.grid(True)

    os.makedirs("output", exist_ok=True)
    graph_path = "output/temperature_graph.png"

    plt.savefig(graph_path, bbox_inches="tight")
    plt.close()

    return fig
print("GRAPH GENERATOR NEW VERSION 🚀")