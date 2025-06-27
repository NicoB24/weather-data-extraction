# 🌤️ Weather Data Extraction API

A Python-based tool and API to extract, process, and visualize weather data for a fixed list of cities.  
Includes scripts for data fetching, CSV report generation, plotting, and a FastAPI backend to expose these features via HTTP.

---

## 🚀 Features

- Fetch weather data for a predefined list of cities  
- Generate CSV reports with the latest weather data   
- FastAPI server exposing endpoints for data generation, CSV download, and plotting  
- Docker support for containerized API deployment  
- Testing with `pytest`  
- Code style and type checking with `black`, `isort`, `flake8`, and `mypy`

---

## 🛠️ Technologies

- Python 3.8+  
- [FastAPI](https://fastapi.tiangolo.com/) v0.95.2  
- [Pandas](https://pandas.pydata.org/) v2.0.3  
- Uvicorn (ASGI server)  
- pytest for testing  
- black, isort, flake8, mypy for code quality and formatting

---

## ⚙️ Local Development Setup

### 1. Create and activate virtual environment

```
python3 -m venv venv
source venv/bin/activate
```

### 2. Create and activate virtual environment
```
pip install -r requirements.txt
```

### Run main script
```
python -m src.main
```
After that you will find the .csv and the .png files in the data folder.

### Run Tests
```
pytest tests/
```

### Code Style and Linting
```
black src/
isort src/
flake8 src/
mypy src/
```

### Run API Server Locally
```
uvicorn api:app --reload
```
Access the API at: http://127.0.0.1:8000

### 🐳 Run API Server with Docker
Build image
```
docker build -t weather-api .
```
Run container
```
docker run --name weather-api-container -p 8000:8000 weather-api
```
 
## 🔧 API Usage Examples
Generate weather data (POST):
```
curl -X POST http://127.0.0.1:8000/generate
```
Download latest generated CSV:
```
http://127.0.0.1:8000/download-csv
```
Get latest temperature plot:
```
http://127.0.0.1:8000/plot
```

## 💡 Notes & Possible Improvements
- Fixed city list: Both main script and API use a hardcoded list of cities. Could be improved by fetching cities dynamically from an external API or database.
- CSV download: Currently only the latest generated CSV is downloadable. Adding support for downloading by date would be valuable.
- Fetching logic: fetch_weather.py is synchronous and simple to avoid rate limiting. Async requests or caching could boost performance.
- Testing: Add more API endpoint tests to cover edge cases and error handling.
- Error handling & logging: Could be enhanced for production readiness.
- Add CI/CD
