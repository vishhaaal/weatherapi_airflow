# WeatherAPI ETL with Airflow

This repository contains a data pipeline implemented with Apache Airflow to extract weather data from an external API, transform it, and load it into a CSV file. The pipeline retrieves current weather data for Mumbai from the WeatherMap API, converts temperature values from Kelvin to Fahrenheit, and saves the transformed data in a CSV file.

## Prerequisites

Before running the pipeline, make sure you have the following prerequisites installed:

- Apache Airflow
- Pandas
- Python 3.x

## Setup

1. Clone this repository to your local machine:

   ```
   git clone https://github.com/vishhaaal/weatherapi_airflow.git
   ```

2. Install the required Python packages:

   ```
   pip install -r requirements.txt
   ```

3. Configure Airflow with your settings, including setting up connections to the WeatherMap API by updating the `airflow.cfg` file.

4. Create a DAG (Directed Acyclic Graph) for the ETL process by copying and pasting the provided code into a Python file within your Airflow DAGs directory.

5. Start Airflow's web server and scheduler:

   ```
   airflow webserver -p 8080
   airflow scheduler
   ```

6. Access the Airflow web UI by navigating to `http://localhost:8080` in your web browser. You can use the web UI to trigger and monitor the pipeline.

## Usage

Once the setup is complete, you can use the Airflow web interface to trigger the `weather_api` DAG. This DAG consists of the following tasks:

1. **weather_api_ready**: This task checks if the WeatherMap API is accessible before proceeding.

2. **extract_api_data**: This task extracts weather data for Mumbai from the WeatherMap API.

3. **transform_load_weather_data**: This task transforms the extracted data, converting temperature values to Fahrenheit, and loads it into a CSV file.

You can schedule the DAG to run periodically by modifying the `schedule_interval` parameter in the DAG definition. By default, it runs daily.

## Output

The transformed weather data is saved in a CSV file with a timestamp appended to its name. The CSV file is created in the same directory as the Python script. The file name format is `current_weather_data_Mumbai<timestamp>.csv`.

## Author

- Author: Vishal (GitHub: [vishhaaal](https://github.com/vishhaaal))

Feel free to customize this README to include additional information about your project or any specific instructions for your users.