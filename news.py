import subprocess
import sys
import csv
from flask import Flask, request, render_template
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from pysentimiento import create_analyzer# Function to get news based on the query

# # Function to dynamically install required packages
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
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.headless = True
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver
def get_news(query, limit=50, country_code='us'):
    driver = setup_driver()
    formatted_query = '+'.join(query.split())
    news_url = f"https://www.google.com/search?q={formatted_query}&tbm=nws&source=lnt&tbs=sbd:1&gl={country_code}"
    driver.get(news_url)
    wait = WebDriverWait(driver, 10)
    news_list = []
    try:
        while len(news_list) < limit:
            time.sleep(2)
            news_boxes = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="rso"]/div/div/div/div/div/a')))
            for box in news_boxes:
                if len(news_list) >= limit:
                    break
                title_element = box.find_element(By.XPATH, './/div[@class="n0jPhd ynAwRc MBeuO nDgy9d"]')
                title = title_element.text
                link = box.get_attribute('href')
                news_list.append({'title': title, 'link': link})
            next_button = driver.find_element(By.XPATH, '//a[@id="pnnext"]')
            next_button.click()
    except Exception as e:
        print(f"Error during news collection or navigation: {e}")
    finally:
        driver.quit()
    
    # Save news to CSV
    with open('news_list.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'URL'])
        for news in news_list:
            writer.writerow([news['title'], news['link']])
    return news_list

# Sentiment analyzer
analyzer = create_analyzer(task="sentiment", lang="en")

# Analyze sentiment of each news article from CSV
# Analyze sentiment of each news article from CSV
def analyze_titles(csv_path):
    # Read the news titles from CSV
    with open(csv_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Skip the header
        news_data = [row for row in reader]

    # Analyze sentiment and append results
    analyzed_data = []
    for row in news_data:
        if len(row) < 2:
            continue
        title = row[0]
        url = row[1]
        analysis = analyzer.predict(title)
        sentiment = max(analysis.probas, key=analysis.probas.get)
        score = analysis.probas[sentiment]
        analyzed_data.append(row + [sentiment, score])

    # Write the updated data back to the CSV
    with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers + ['Sentiment', 'Score'])
        writer.writerows(analyzed_data)