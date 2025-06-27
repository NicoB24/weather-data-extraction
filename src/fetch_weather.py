# Since the `current_weather` endpoint does not provide humidity, we request the hourly
# relative humidity (`relative_humidity_2m`) alongside the current weather data.
# The function then matches the timestamp of
# the current weather (`current_weather.time`)
# with the closest timestamp from the hourly data. This is done by
# parsing all timestamps into datetime objects
# and finding the hourly timestamp with the smallest time
# difference to the current weather time.
# Finally, it returns a dictionary with the city name, temperature in Celsius,
# wind speed in meters per second, and the matched humidity percentage.

import logging
from typing import Any, Dict
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from dateutil import parser
from src.config import BASE_URL



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

class WeatherClient:
    def __init__(self):
        self.session = requests.Session()
        retries = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET"]
        )
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def fetch_weather(self, city: Dict[str, Any]) -> Dict[str, Any]:
        params = {
            "latitude": city["Latitude"],
            "longitude": city["Longitude"],
            "current_weather": True,
            "hourly": "relative_humidity_2m",
            "timezone": "auto",
        }

        try:
            response = self.session.get(BASE_URL, params=params, timeout=(3, 5))
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching data for {city['City']}: {e}")
            return {
                "City": city["City"],
                "Temperature (C)": None,
                "Wind Speed (m/s)": None,
                "Humidity (%)": None,
            }

        current = data.get("current_weather", {})
        humidity_hourly = data.get("hourly", {}).get("relative_humidity_2m", [])
        times = data.get("hourly", {}).get("time", [])

        humidity = None
        if current and humidity_hourly and times:
            current_time = current.get("time")
            current_dt = parser.isoparse(current_time)
            times_dt = [parser.isoparse(t) for t in times]
            closest_idx = min(
                range(len(times_dt)),
                key=lambda i: abs(times_dt[i] - current_dt)
            )
            humidity = humidity_hourly[closest_idx]

        return {
            "City": city["City"],
            "Temperature (C)": current.get("temperature"),
            "Wind Speed (m/s)": current.get("windspeed"),
            "Humidity (%)": humidity,
        }
