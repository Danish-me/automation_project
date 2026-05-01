import matplotlib.pyplot as plt
import os

from src.data_processor import (
    get_temperature_series,
    process_datetime,
    detect_phases
)


def plot_temperature(df):
    """
    Generate temperature graph with phase highlighting
    + save image for PDF
    """

    # ✅ Prepare data
    df = process_datetime(df)
    df = get_temperature_series(df)
    df = detect_phases(df)

    # ✅ Create figure
    plt.figure(figsize=(10, 5))

    # 🔹 Main temperature line
    plt.plot(df["Datetime"], df["Temp"], label="Temperature (°C)")

    # 🔹 Highlight Sterilization Phase
    steril_df = df[df["Phase"] == "Sterilization"]

    if not steril_df.empty:
        plt.fill_between(
            steril_df["Datetime"],
            steril_df["Temp"],
            alpha=0.3,
            label="Sterilization Phase"
        )

    # 🔹 Labels
    plt.xlabel("Time")
    plt.ylabel("Temperature (°C)")
    plt.title("Autoclave Temperature Profile")

    plt.legend()
    plt.grid(True)

    # ✅ Save graph for PDF
    os.makedirs("output", exist_ok=True)
    graph_path = "output/temperature_graph.png"
    plt.savefig(graph_path, bbox_inches="tight")

    return plt