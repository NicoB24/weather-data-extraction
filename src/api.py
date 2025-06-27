import os
import re
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from src.main import main

DATA_DIR = "data"

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Weather API is running."}


@app.post("/generate")
def generate():
    try:
        main()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during generation: {e}")

    return {"message": "Weather data and plot generated."}


def get_latest_file(pattern: str) -> str:
    matched_files = []
    for filename in os.listdir(DATA_DIR):
        if re.match(pattern, filename):
            match = re.search(r"(\d{8}_\d{6})", filename)
            if match:
                timestamp_str = match.group(1)
                timestamp = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
                matched_files.append((timestamp, filename))

    if not matched_files:
        raise HTTPException(status_code=404, detail="No matching files found")

    # Sort by timestamp
    matched_files.sort(reverse=True)
    latest_filename = matched_files[0][1]
    return os.path.join(DATA_DIR, latest_filename)


@app.get("/download-csv")
def download_csv():
    pattern = r"weather_data_\d{8}_\d{6}\.csv"
    file_path = get_latest_file(pattern)
    return FileResponse(
        file_path, media_type="text/csv", filename=os.path.basename(file_path)
    )


@app.get("/plot")
def get_plot():
    pattern = r"temperature_by_city_\d{8}_\d{6}\.png"
    file_path = get_latest_file(pattern)
    return FileResponse(
        file_path, media_type="image/png", filename=os.path.basename(file_path)
    )
