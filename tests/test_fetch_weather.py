from unittest.mock import MagicMock, patch

import requests

from src.fetch_weather import WeatherClient


def mock_successful_response():
    return {
        "current_weather": {
            "temperature": 20.5,
            "windspeed": 3.2,
            "time": "2025-06-27T10:00",
        },
        "hourly": {
            "relative_humidity_2m": [60, 62, 65],
            "time": ["2025-06-27T09:00", "2025-06-27T10:00", "2025-06-27T11:00"],
        },
    }


@patch("src.fetch_weather.requests.Session.get")
def test_fetch_weather_success(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = mock_successful_response()
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    client = WeatherClient()
    city = {"City": "Testville", "Latitude": 12.34, "Longitude": 56.78}
    result = client.fetch_weather(city)

    assert result["City"] == "Testville"
    assert result["Temperature (C)"] == 20.5
    assert result["Wind Speed (m/s)"] == 3.2
    assert result["Humidity (%)"] == 62


@patch("requests.Session.get")
def test_fetch_weather_failure(mock_get):
    # Simulate a requests.exceptions.RequestException instead of Exception
    mock_get.side_effect = requests.exceptions.RequestException("Connection error")

    client = WeatherClient()
    city = {"City": "Failtown", "Latitude": 0, "Longitude": 0}

    result = client.fetch_weather(city)

    assert result == {
        "City": "Failtown",
        "Temperature (C)": None,
        "Wind Speed (m/s)": None,
        "Humidity (%)": None,
    }
