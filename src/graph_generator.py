import matplotlib.pyplot as plt
import os

def plot_temperature(df):
    os.makedirs("output", exist_ok=True)

    # Data
    time = df["time"]
    temp = df["temperature"]

    # Separate normal and deviation points
    normal_x = []
    normal_y = []
    dev_x = []
    dev_y = []

    for t, val in zip(time, temp):
        if val >= 121:
            normal_x.append(t)
            normal_y.append(val)
        else:
            dev_x.append(t)
            dev_y.append(val)

    # Plot
    plt.figure()

    plt.plot(time, temp, marker='o')

    plt.title("Temperature vs Time")
    plt.xlabel("Time")
    plt.ylabel("Temperature (°C)")

    # FIXES 👇
    plt.xticks(time[::2], rotation=45)
    plt.tight_layout()

    # Save
    file_path = "output/temperature_graph.png"
    plt.savefig(file_path)

    plt.close()

    print(f"Graph saved at {file_path}")