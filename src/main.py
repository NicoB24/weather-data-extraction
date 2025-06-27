import logging
from src.cities import cities
from src.fetch_weather import WeatherClient
from src.processor import export_to_csv, process_weather_data

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def main() -> None:
    client = WeatherClient()
    all_data = []

    for city in cities:
        weather = client.fetch_weather(city)
        all_data.append(weather)

    if not all_data:
        logging.warning("No data fetched.")
        return

    df = process_weather_data(all_data)
    export_to_csv(df)
    logging.info("Weather data exported to 'data' folder.")


if __name__ == "__main__":
    main()
