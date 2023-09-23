import json
from airflow import DAG
from datetime import datetime,timedelta
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.operators.python import PythonOperator
import pandas as pd
import os


def kelvin_to_farenheit(temp_in_kelvin):
    temp_in_farenheit = (temp_in_kelvin - 273.15) * (9/5) + 32
    return temp_in_farenheit


def transform_load_data(task_instance):
    data = task_instance.xcom_pull(task_ids ="extract_api_data")
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

    transformed_data_list = [transformed_data]
    df_data = pd.DataFrame(transformed_data_list)

    now = datetime.now()
    dt_string = now.strftime("%d%m%Y%H%M%S")
    file_name = 'current_weather_data_Mumbai' + dt_string + '.csv'
    current_directory = os.path.dirname(__file__)
    file_path = os.path.join(current_directory, file_name)
    df_data.to_csv(file_path, index=False)
    
default_args = {
    'owner' : 'vishal',
    'depends_on_past' : False,
    'start_date' : datetime(2023,9,22),
    'retries' : 5,
    'retry_delay' : timedelta(minutes = 2)
}

with DAG(
    dag_id = 'weather_api',
    default_args = default_args,
    schedule_interval = '@daily',
    catchup = False
)as dag:
    task1 = HttpSensor(
        task_id = 'weather_api_ready',
        http_conn_id = 'weathermap_api',
        endpoint = '/data/2.5/weather?q=Mumbai&appid={api_key}'
    )

    task2 = SimpleHttpOperator(
        task_id = 'extract_api_data',
        http_conn_id = 'weathermap_api',
        endpoint = '/data/2.5/weather?q=Mumbai&appid={api_key}',
        method="GET",
        response_filter=lambda r : json.loads(r.text),
        log_response=True
    )

    task3 = PythonOperator(
        task_id = 'transform_load_weather_data',
        python_callable = transform_load_data
    )


    task1 >> task2 >> task3