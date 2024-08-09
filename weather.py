import requests
import json
from dateutil.relativedelta import relativedelta
import datetime
import pandas as pd
from opencage.geocoder import OpenCageGeocode

def get_country_coordinates(country_name):    
    geocoder = OpenCageGeocode('453c2a70a757416ea757168a8eef03f2')
    query = f'{country_name}'
    results = geocoder.geocode(query)

    if results and len(results):
        latitude = results[0]['geometry']['lat']
        longitude = results[0]['geometry']['lng']
        return latitude, longitude
    else:
        print("Could not find coordinates for the country.")
        return None

def call_api(date, lat, long):

    api_url = "https://api.open-meteo.com/v1/forecast?latitude={}&longitude={}&daily=temperature_2m_max,temperature_2m_min&start_date={}&end_date={}".format(lat, long, date, date)

    # if year is other than 2024
    if date[:4] != "2024":
        api_url = "https://archive-api.open-meteo.com/v1/archive?latitude={}&longitude={}&start_date={}&end_date={}&daily=temperature_2m_max,temperature_2m_min".format(lat, long, date, date)

    try:
        response = requests.get(api_url).text
        data = json.loads(response)
        daily = data["daily"]
        min_temp_list = daily["temperature_2m_min"]
        max_temp_list = daily["temperature_2m_max"]

        # get max and min temperatures
        min_temp = min_temp_list[0]
        max_temp = max_temp_list[0]

        return max_temp, min_temp

    except Exception as e:
        print("Error: {}".format(e))
        return 0.0, 0.0

def avg_weather(date, lat, long):
    max_temperature = ""
    min_temperature = ""
    # take average of past 10 years record
    avg_max_temperature = 0.0
    avg_min_temperature = 0.0
    date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    for i in range(1, 11):
        date_minus_i_years = date - relativedelta(years=i)
        date_minus_i_years_str = date_minus_i_years.strftime("%Y-%m-%d")
        max_temp, min_temp = call_api(date_minus_i_years_str, lat, long)
        avg_max_temperature += max_temp
        avg_min_temperature += min_temp
    avg_max_temperature /= 10
    avg_min_temperature /= 10
    max_temperature = avg_max_temperature
    min_temperature = avg_min_temperature
    return max_temperature, min_temperature

def calculate_weather_score(date, destination):
    lat, long = get_country_coordinates(destination)
    if lat is None : lat = 28.6519
    if long is None: long = 77.2315

    current_max, current_min = call_api(date, lat, long)
    avg_max, avg_min = avg_weather(date, lat, long)

    max_deviation_percentage = (abs(current_max - avg_max) / avg_max)
    min_deviation_percentage = (abs(current_min - avg_min) / avg_min)
    
    # Calculate the average score
    avg_score = (max_deviation_percentage + min_deviation_percentage)
    
    return avg_score