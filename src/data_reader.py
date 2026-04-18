import pandas as pd

def read_excel(file_path):
    df = pd.read_excel(file_path, header=4)

    # Clean column names
    df.columns = df.columns.str.strip().str.lower()

    # Select only required columns
    df = df[["time", "temperature", "pressure"]]

    return df