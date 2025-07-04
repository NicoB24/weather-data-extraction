# flake8: noqa: E402

import os
from datetime import datetime
from typing import Dict, List

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.config import DATA_DIR, EXPORT_FILENAME_PREFIX


def process_weather_data(data: List[Dict[str, float]]) -> pd.DataFrame:
    df = pd.DataFrame(data).copy()

    required_cols = ["Temperature (C)", "Wind Speed (m/s)"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    df["Temperature (C)"] = pd.to_numeric(df["Temperature (C)"], errors="coerce")
    df["Wind Speed (m/s)"] = pd.to_numeric(df["Wind Speed (m/s)"], errors="coerce")

    df["Temperature (F)"] = df["Temperature (C)"] * 9 / 5 + 32
    df["Wind Speed (mph)"] = df["Wind Speed (m/s)"] * 2.23694

    df.sort_values("Temperature (C)", ascending=True, inplace=True)

    columns_to_format = [
        "Temperature (C)",
        "Temperature (F)",
        "Wind Speed (m/s)",
        "Wind Speed (mph)",
    ]
    df[columns_to_format] = df[columns_to_format].round(1).astype(str)

    return df


def export_to_csv(df: pd.DataFrame) -> None:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{EXPORT_FILENAME_PREFIX}{timestamp}.csv"
    os.makedirs(DATA_DIR, exist_ok=True)
    full_path = os.path.join(DATA_DIR, filename)

    df.to_csv(full_path, index=False, sep=";", encoding="utf-8-sig")


def visualize_temperatures(df, output_dir="data"):
    os.makedirs(output_dir, exist_ok=True)

    df_plot = df.copy()
    # Set 'City' as a categorical variable to preserve order in the plot
    df_plot["City"] = pd.Categorical(
        df_plot["City"], categories=df_plot["City"], ordered=True
    )

    plt.figure(figsize=(10, 6))
    sns.barplot(
        y="City", x="Temperature (C)", data=df_plot, palette="viridis", orient="h"
    )

    plt.title("Temperature by City")
    plt.ylabel("City")
    plt.xlabel("Temperature (°C)")
    plt.tight_layout()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"temperature_by_city_{timestamp}.png"
    output_path = os.path.join(output_dir, filename)

    plt.savefig(output_path)
    plt.close()
