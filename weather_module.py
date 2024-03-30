import requests
from datetime import datetime, timedelta
import pandas as pd

user_api = '5dbd96a74070fcd6d3ab24cbb6c63df3'

# Define the path to your dataset
dataset_path = r"C:\Users\vipul\OneDrive\Desktop\ml_project\ml_project\A_A_R.csv"

def get_average_annual_rainfall(city_name, dataset_path):
    try:
        dataset = pd.read_csv(dataset_path)
    except FileNotFoundError:
        print("Error: Dataset file not found.")
        return None
    except Exception as e:
        print("Error:", e)
        return None

    dataset['DISTRICT'] = dataset['DISTRICT'].str.lower()
    city_row = dataset[dataset['DISTRICT'] == city_name.lower()]

    if city_row.empty:
        print(f"No data found for {city_name}.")
        return None

    avg_rainfall = city_row['A_A_R'].values[0]

    return avg_rainfall

def get_weather_data(city_name):
    # Calculate the end date for the forecast (four months from now)
    end_date = datetime.now() + timedelta(days=120)

    complete_api_link = f"https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={user_api}"
    api_link = requests.get(complete_api_link)
    api_data = api_link.json()

    # Extract relevant forecast data for the upcoming four months
    forecasts = api_data['list']
    temp_sum = 0
    humidity_sum = 0
    count = 0

    # Loop through forecasts and consider only those within the next four months
    for forecast in forecasts:
        forecast_date = datetime.strptime(forecast['dt_txt'], '%Y-%m-%d %H:%M:%S')
        if forecast_date.date() <= end_date.date():
            temp = forecast['main']['temp']
            humidity = forecast['main']['humidity']
            temp_celsius = temp - 273.15
            temp_sum += temp_celsius
            humidity_sum += humidity
            count += 1

    # Calculate the average temperature and humidity
    avg_temp = temp_sum / count
    avg_humidity = humidity_sum / count

    # Fetch and return average annual rainfall
    avg_rainfall = get_average_annual_rainfall(city_name, dataset_path)

    return avg_temp, avg_humidity, avg_rainfall

city_name = input("Enter the city name: ")
temperature, humidity, rainfall = get_weather_data(city_name)
print("Weather Data:")
print(f"Temperature: {temperature:.2f} °C")
print(f"Humidity: {humidity:.2f}%")
print(f"Rainfall: {rainfall} mm")
