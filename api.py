from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import os
import re
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
    files = [f for f in os.listdir(DATA_DIR) if re.match(pattern, f)]
    if not files:
        return None

    files.sort(key=lambda x: re.findall(r"\d{8}_\d{6}", x)[0], reverse=True)
    return os.path.join(DATA_DIR, files[0])


@app.get("/download-csv")
def download_csv():
    pattern = r"weather_data_\d{8}_\d{6}\.csv"
    file_path = get_latest_file(pattern)
    if not file_path:
        raise HTTPException(status_code=404, detail="No CSV file found.")
    return FileResponse(file_path, media_type="text/csv", filename=os.path.basename(file_path))


@app.get("/plot")
def get_plot():
    pattern = r"temperature_by_city_\d{8}_\d{6}\.png"
    file_path = get_latest_file(pattern)
    if not file_path:
        raise HTTPException(status_code=404, detail="No plot image found.")
    return FileResponse(file_path, media_type="image/png", filename=os.path.basename(file_path))
