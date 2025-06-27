import importlib
import os
import tempfile

import pandas as pd
import pytest

import src.config as config
from src.processor import process_weather_data, visualize_temperatures


def sample_df():
    return pd.DataFrame(
        {
            "City": ["Alpha", "Beta", "Gamma"],
            "Temperature (C)": [15.0, 20.5, 10.0],
            "Wind Speed (m/s)": [2.0, 3.5, 1.5],
        }
    )


def test_process_weather_data_valid():
    data = [
        {"City": "X", "Temperature (C)": 10, "Wind Speed (m/s)": 1},
        {"City": "Y", "Temperature (C)": 15, "Wind Speed (m/s)": 2},
    ]
    df = process_weather_data(data)

    assert set(df.columns).issuperset(
        {
            "City",
            "Temperature (C)",
            "Temperature (F)",
            "Wind Speed (m/s)",
            "Wind Speed (mph)",
        }
    )
    assert df["Temperature (F)"].iloc[0] == "50.0"
    assert df["Wind Speed (mph)"].iloc[1] == "4.5"  # 2 * 2.23694 = 4.47 → rounded


def test_process_weather_data_missing_columns():
    with pytest.raises(ValueError):
        process_weather_data([{"City": "X", "Temperature (C)": 10}])


def test_export_to_csv_creates_file(monkeypatch):
    with tempfile.TemporaryDirectory() as tmpdir:
        # Patch config.DATA_DIR before importing processor
        monkeypatch.setattr(config, "DATA_DIR", tmpdir)

        # Re-import the processor module to pick up the patched config
        import src.processor

        importlib.reload(src.processor)

        df = pd.DataFrame(
            {
                "Col1": [1, 2],
                "Col2": ["a", "b"],
            }
        )

        # Call the function using the reloaded processor
        src.processor.export_to_csv(df)

        files = os.listdir(tmpdir)
        csv_files = [f for f in files if f.endswith(".csv")]
        assert len(csv_files) == 1
        assert csv_files[0].startswith(src.processor.EXPORT_FILENAME_PREFIX)


def test_visualize_temperatures_creates_plot():
    df = sample_df()
    with tempfile.TemporaryDirectory() as tmpdir:
        visualize_temperatures(df, output_dir=tmpdir)
        files = os.listdir(tmpdir)
        png_files = [
            f
            for f in files
            if f.startswith("temperature_by_city") and f.endswith(".png")
        ]
        assert len(png_files) == 1
