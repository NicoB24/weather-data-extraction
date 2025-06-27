import os
from datetime import datetime
from typing import Dict, List

import pandas as pd


def process_weather_data(data: List[Dict[str, float]]) -> pd.DataFrame:
    df = pd.DataFrame(data)

    df["Temperature (F)"] = df["Temperature (C)"] * 9 / 5 + 32
    df["Wind Speed (mph)"] = df["Wind Speed (m/s)"] * 2.23694

    df.sort_values("Temperature (C)", ascending=False, inplace=True)

    # Round numeric columns to 2 decimal places and convert to string
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
    filename = f"weather_data_{timestamp}.csv"
    output_dir = "data"
    full_path = os.path.join(output_dir, filename)

    df.to_csv(full_path, index=False, sep=";", encoding="utf-8-sig")
