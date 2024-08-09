from weather import *

def calculate_sentiment_score(csv_file):
    df = pd.read_csv(csv_file)
    avg_score = 0
    len = 0
    for score, sentiment in zip(df['Score'], df['Sentiment']):
        if(sentiment=="NEG"):
            avg_score -= score
            len+=1
        elif(sentiment=="POS"):
            avg_score += score
            len+=1
    return 1 if len==0 else avg_score / len

def calculate_budget_score(budget, csv_file):
    df = pd.read_csv(csv_file)
    cnt_range = 0
    total_valid_prices = 0
    
    for price in df['Price']:
        if isinstance(price, str):
            # Handle string values
            # Remove currency symbol and commas from the string and convert to numeric
            try:
                price = float(price.replace("₹", "").replace(",", ""))
            except:
                continue

        # Check if price is NaN
        if pd.isnull(price):
            continue  # Skip NaN values
        
        # Check if price is within budget
        if price <= budget:
            cnt_range += 1
        
        total_valid_prices += 1

    # Check if there are no valid prices
    if total_valid_prices == 0:
        print(f"Empty csv : {csv_file}")
        return 1
    
    return cnt_range / total_valid_prices

"""""
returns below scores in %:-
    1. recommendation_score: overall recommendation after multiplyting with weights
    2. weather_score : how much % the weather is unsuitable
    3. sentiment_str : 
    4. transport_score : 
    5. hotel_score : 
"""""
def calculate_recommendation_score(date, destination, hotel_budget: float, transport_budget: float):
    weights = [0.25, 0.35, 0.2, 0.2]
    weather_score = calculate_weather_score(date, destination)
    sentiment_score = calculate_sentiment_score("news_list.csv")
    transport_score = calculate_budget_score(transport_budget, "flight_prices.csv")
    hotel_score = calculate_budget_score(hotel_budget, "hotel_prices.csv")
    tot_score =  (weights[0] * (1-weather_score) +
            weights[1] * sentiment_score +
            weights[2] * transport_score +
            weights[3] * hotel_score)
    sentiment_str = "Negative" if sentiment_score*100 < 10 else "Positive"
    print(f"total score = {tot_score} , weather score = {weather_score} , sentiment score = {sentiment_score} , transport score = {transport_score} , hotel score = {hotel_score}")
    return round(tot_score*100), round(weather_score*100), sentiment_str, round(transport_score*100), round(hotel_score*100)

# # Example usage:
# print(calculate_recommendation_score("2024-04-24",2000,10000))