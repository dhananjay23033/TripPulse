
import subprocess
import sys
import csv
import datetime
from flask import Flask, request, render_template
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from pysentimiento import create_analyzer
import requests
import pandas as pd
import re 
from flights import *
from hotels import *
from events import *
from news import *
from score import *
from datetime import date
# Function to dynamically install required packages
# def install(package):
#     subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# # List of required packages
# required_packages = ["flask", "selenium", "webdriver-manager", "pysentimiento"]

# # Install required packages
# for package in required_packages:
#     install(package)

app = Flask(__name__)

# Function to set up the Selenium driver
def setup_driver():
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


@app.route('/')
def home():
    return render_template('simple_index.html')
# Route to handle the form submission and process the news search
@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    source = request.form['from']
    hbudget = float(request.form['hbudget'])
    fbudget = float(request.form['fbudget'])
    # print(hbudget)
    # print(fbudget)  
    news_query= query+"+%28travel+OR+flights+OR+tourist+OR+festival+OR+events+OR+fair+OR+riot+OR+protest%29"
    # news_query= query
    country_code = 'us'  # Default to US, modify as needed
    get_news(news_query, country_code=country_code)
    analyzed_articles = analyze_titles("news_list.csv")
    hotel_data = fetch_hotel_data(query)
    save_hotels_to_csv(hotel_data)
    city_to=query
    city_from=source
    airport_dict=get_airport_codes(city_from, city_to)
    # print(airport_dict)
    flight_data = fetch_flight_data(airport_dict['to'], airport_dict['from'])
    save_flights_to_csv(flight_data)
    event_data = fetch_event_data(query)
    save_events_to_csv(event_data)
    # Read events from CSV and convert to list of dicts
    # date="2024-05-02"
    

    # curr_date = date.today()
    curr_date = "2024-05-02"
    # formatted_date = curr_date.strftime("%Y-%m-%d")
    # score = calculate_recommendation_score(date,query, hbudget, fbudget)
    # print(score*100)

    tot_score, weather_score, sentiment_str, flights_score, hotels_score = calculate_recommendation_score(curr_date, query, hbudget, fbudget)
    # weather_score = (100-weather_score)*3

    hotels = []
    with open('hotel_prices.csv', mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            hotels.append(row)

    events = []
    with open('event_details.csv', mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            events.append(row)

    return render_template('results.html', events=events, hotels=hotels, 
                           weather_score=weather_score, flights_score=flights_score,
                           hotels_score=hotels_score, sentiment_str=sentiment_str, tot_score=tot_score, query=query)

if __name__ == '__main__':
    app.run(debug=True)
