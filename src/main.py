from src.cities import cities
from src.fetch_weather import fetch_weather
from src.processor import export_to_csv, process_weather_data


def main() -> None:
    all_data = []

    for city in cities:
        try:
            weather = fetch_weather(city)
            all_data.append(weather)
        except Exception as e:
            print(f"Error fetching data for {city['City']}: {e}")

    if not all_data:
        print("No data fetched.")
        return

    df = process_weather_data(all_data)
    export_to_csv(df)
    print("Weather data exported to 'data folder'")


if __name__ == "__main__":
    main()
