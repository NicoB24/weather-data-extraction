from typing import Any, Dict

import requests
from dateutil import parser

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


def fetch_weather(city: Dict[str, Any]) -> Dict[str, Any]:
    base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": city["Latitude"],
        "longitude": city["Longitude"],
        "current_weather": True,
        "hourly": "relative_humidity_2m",
        "timezone": "auto",
    }

    response = requests.get(base_url, params=params)
    response.raise_for_status()
    data = response.json()

    current = data.get("current_weather", {})
    humidity_hourly = data.get("hourly", {}).get("relative_humidity_2m", [])
    times = data.get("hourly", {}).get("time", [])

    humidity = None
    if current and humidity_hourly and times:
        current_time = current.get("time")
        # Parse current_time to datetime
        current_dt = parser.isoparse(current_time)

        # Parse all times to datetime and find closest
        times_dt = [parser.isoparse(t) for t in times]
        # Find index of closest time
        closest_idx = min(
            range(len(times_dt)), key=lambda i: abs(times_dt[i] - current_dt)
        )

        humidity = humidity_hourly[closest_idx]

    return {
        "City": city["City"],
        "Temperature (C)": current.get("temperature"),
        "Wind Speed (m/s)": current.get("windspeed"),
        "Humidity (%)": humidity,
    }
