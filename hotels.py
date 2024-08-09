
import requests
import pandas as pd
import re  # Regular expression library for string cleaning
 # Regular expression library for string cleaning

import requests
import pandas as pd

def fetch_hotel_data(search_query):
    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_hotels",
        "q": search_query,
        "gl": "us",
        "hl": "en",
        "currency": "INR",
        "check_in_date": "2024-04-24",
        "check_out_date": "2024-04-25",
        "api_key": "6d3da6b11f95cee42bb81de16eb2b716b1f362601c55f86c9b59c1772bc4bc8f"
    }

    response = requests.get(url, params=params)
    return response.json()

def save_hotels_to_csv(hotel_data):
    hotels_list = []
    if 'properties' in hotel_data:
        for hotel in hotel_data['properties']:
            try:
                if hotel['type'] == 'hotel':  # Ensuring it's a hotel type
                    hotel_name = hotel['name']
                    price_per_night = hotel.get('rate_per_night', {}).get('lowest', 'Not available')
                    original_image = hotel['images'][0]['original_image'] if hotel['images'] else 'No image available'
                    hotels_list.append({"Hotel": hotel_name, "Price": price_per_night, "Image": original_image})
            except KeyError as e:
                print(f"Missing key in data: {e}")
    
    if hotels_list:
        df = pd.DataFrame(hotels_list)
        df.to_csv("hotel_prices.csv", index=False)
        print("Hotel data has been saved to 'hotel_prices.csv'.")
    else:
        print("No hotel data available to save.")

