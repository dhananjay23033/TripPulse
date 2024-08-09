
import requests
import pandas as pd
import re  # Regular expression library for string cleaning

def get_airport_codes(city_from, city_to):
    # Define the dictionary mapping cities to airport IATA codes
    airports = {
        "delhi": "DEL",
        "mumbai": "BOM",
        "bangalore": "BLR",
        "chennai": "MAA",
        "kolkata": "CCU",
        "hyderabad": "HYD",
        "ahmedabad": "AMD",
        "pune": "PNQ",
        "goa": "GOI",
        "haridwar":"DED",
        "jaipur": "JAI",
        "lucknow": "LKO",
        "kochi": "COK",
        "thiruvananthapuram": "TRV",
        "bhopal": "BHO",
        "indore": "IDR",
        "nagpur": "NAG",
        "visakhapatnam": "VTZ",
        "bhubaneswar": "BBI",
        "patna": "PAT",
        "ranchi": "IXR",
        "gurgaon": "DEL",
        "noida": "DEL",
        "ghaziabad": "DEL",
        "faridabad": "DEL",
        "chandigarh": "IXC",
        "srinagar": "SXR",
        "amritsar": "ATQ",
        "dehradun": "DED",
        "shimla": "SLV",
        "jammu": "IXJ",
        "kanpur": "KNU",
        "agra": "AGR",
        "varanasi": "VNS",
        "allahabad": "IXD",
        "surat": "STV",
        "vadodara": "BDQ",
        "rajkot": "RAJ",
        "meerut": "DEL",
        "durgapur": "RDP",
        "siliguri": "IXB",
        "nashik": "ISK",
        "aurangabad": "IXU",
        "madurai": "IXM",
        "coimbatore": "CJB",
        "tiruchirappalli": "TRZ",
        "mangalore": "IXE",
        "mysore": "MYQ",
        "tirupati": "TIR",
        "udaipur": "UDR",
        "jodhpur": "JDH",
        "kozhikode": "CCJ",
        "guwahati": "GAU",
        "imphal": "IMF",
        "dimapur": "DMU",
        "shillong": "SHL",
        "dibrugarh": "DIB",
        "silchar": "IXS"
    }
    
    # Normalize the input by converting to lower case
    city_from = city_from.lower()
    city_to = city_to.lower()
    
    # Get airport codes from the dictionary
    airport_from = airports.get(city_from, "Airport code not found")
    airport_to = airports.get(city_to, "Airport code not found")
    
    # Return a dictionary with the results
    return {"from": airport_from, "to": airport_to}

# Example usage
from_city = "Gurgaon"
to_city = "Mumbai"
result = get_airport_codes(from_city, to_city)
print(f"From {from_city} (airport: {result['from']}) to {to_city} (airport: {result['to']}).")



def fetch_flight_data(departure_id, arrival_id):
    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_flights",
        "departure_id": departure_id,
        "arrival_id": arrival_id,
        "gl": "us",
        "hl": "en",
        "currency": "INR",
        "outbound_date": "2024-05-24",
        "return_date": "2024-05-25",
        "api_key": "6d3da6b11f95cee42bb81de16eb2b716b1f362601c55f86c9b59c1772bc4bc8f"
    }

    response = requests.get(url, params=params)
    return response.json()

def clean_price(price_str):
    # Removes any character that is not a digit or comma
    cleaned_price = re.sub(r'[^\d,]', '', price_str)
    return cleaned_price

def save_flights_to_csv(flight_data):
    flights_list = []
    for flight_group in flight_data.get('best_flights', []):
        for flight in flight_group.get('flights', []):
            airline = flight.get('airline')
            price = flight_group.get('price', 'Not available')
            cleaned_price = clean_price(str(price))  # Clean the price string
            flights_list.append({"Airline": airline, "Price": cleaned_price})
    
    if flights_list:
        df = pd.DataFrame(flights_list)
        df.to_csv("flight_prices.csv", index=False)
        print("Flight data has been saved to 'flight_prices.csv'.")
    else:
        print("No flight data available to save.")