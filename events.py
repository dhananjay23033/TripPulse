import requests
import pandas as pd
import requests
import pandas as pd
import re  # Regular expression library for string cleaning
 # Regular expression library for string cleaning

import requests
import pandas as pd
def fetch_event_data(search_query):
    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_events",
        "q": search_query,
        "gl": "us",
        "hl": "en",
        "api_key": "3c4e6621698d3343d49bcfa102076f11e3de5990b34bcf11ac3758d379f72efc"
    }

    response = requests.get(url, params=params)
    return response.json()

def save_events_to_csv(events_data):
    events_list = []
    for event in events_data.get('events_results', []):
        title = event.get('title', 'No title available')
        address = ', '.join(event.get('address', []))
        link = event.get('link', 'No link available')
        image = event.get('image', 'No image available')
        thumbnail = event.get('thumbnail', 'No thumbnail available')
        events_list.append({
            "title": title,
            "address": address,
            "link": link,
            "image_url": image,
            "thumbnail": thumbnail
        })
    
    if events_list:
        df = pd.DataFrame(events_list)
        df.to_csv("event_details.csv", index=False)
        print("Event data has been saved to 'event_details.csv'.")
    else:
        print("No event data available to save.")

