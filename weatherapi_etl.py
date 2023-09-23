import json
import pandas as pd
from datetime import datetime
import requests


city_name = "Mumbai"
base_url = "https://api.openweathermap.org/data/2.5/weather?q="
api_key = '{API key}'

full_url = f"{base_url}{city_name}&APPID={api_key}"

def kelvin_to_farenheit(temp_in_kelvin):
    temp_in_farenheit = (temp_in_kelvin - 273.15) * (9/5) + 32
    return temp_in_farenheit

def weather_etl(url):
    response = requests.get(url)
    data = response.json()
    # print(data)


    city = data["name"]
    weather_description = data["weather"][0]['description']
    temp_farenheit = kelvin_to_farenheit(data["main"]["temp"])
    feels_like_farenheit = kelvin_to_farenheit(data["main"]["feels_like"])
    min_temp_farenheit = kelvin_to_farenheit(data["main"]["temp_min"])
    max_temp_farenheit = kelvin_to_farenheit(data["main"]["temp_max"])
    pressure = data["main"]["pressure"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]
    time_of_record = datetime.utcfromtimestamp(data['dt'] + data["timezone"])
    sunrise_time = datetime.utcfromtimestamp(data["sys"]["sunrise"] + data["timezone"])
    sunset_time = datetime.utcfromtimestamp(data["sys"]["sunset"] + data["timezone"])

    transformed_data = {
        "City" : city,
        "Description" : weather_description,
        "Temperature (F)" : temp_farenheit,
        "Feels Like (F)" : feels_like_farenheit,
        "Minimum Temp (F)" : min_temp_farenheit,
        "Maximum Temp (F)" : max_temp_farenheit,
        "Pressure" : pressure,
        "Humidity" : humidity,
        "Wind Speed" : wind_speed,
        "Time of Record" : time_of_record,
        "Sunrise (Local Time)" : sunrise_time,
        "Sunset (Local Time)" : sunset_time
    }

    print(transformed_data)

    transformed_data_list = [transformed_data]
    df_data = pd.DataFrame(transformed_data_list)
    # print(df_data)

    df_data.to_csv("current_weather_data_Mumbai.csv",index=False)

if __name__ == '__main__':
    weather_etl(full_url)
