import requests
from twilio.rest import Client



STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_API_KEY = "redacted"
STOCK_API_ENDPOINT = "https://www.alphavantage.co/query"

NEWS_API_KEY = "redacted"
NEWS_API_ENDPOINT = "https://newsapi.org/v2/everything"

TWILIO_SID = "redacted"
TWILIO_TOKEN = "redacted"

UP_ARROW = "🔺"
DOWN_ARROW = "🔻"

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY,
}

response = requests.get(STOCK_API_ENDPOINT, params=stock_params)
response.raise_for_status()

stock_data = response.json()

# previous_day = stock_data["Meta Data"]["3. Last Refreshed"]
# print(previous_day)

days_list = list(stock_data["Time Series (Daily)"])
yesterday = days_list[0]
day_before_yesterday = days_list[1]

yesterday_close = float(stock_data["Time Series (Daily)"][yesterday]["4. close"])
day_before_close = float(stock_data["Time Series (Daily)"][day_before_yesterday]["4. close"])

difference = yesterday_close - day_before_close
up_down = None
if difference > 0:
    up_down = UP_ARROW
else:
    up_down = DOWN_ARROW
percent_change = round(difference / day_before_close * 100)

if abs(percent_change) > 5:

    news_params = {
        "qInTitle": COMPANY_NAME,
        "apiKey": NEWS_API_KEY,
    }

    news_response = requests.get(NEWS_API_ENDPOINT, params=news_params)
    news_response.raise_for_status()

    # news_data = news_response.json()
    articles = news_response.json()["articles"]
    three_articles = articles[:3]

    # headlines = []
    # for item in news_data["articles"]:
    #     if "Tesla" in item["title"]:
    #         headlines.append(item["title"])

    formatted_articles = [f"{STOCK}: {up_down}{percent_change}%\nHeadline: {article['title']}.\nBrief: {article['description']}" for article in three_articles]

    client = Client(TWILIO_SID, TWILIO_TOKEN)
    for article in formatted_articles:
        message = client.messages.create(
                body=article,
                from_="redacted",
                to="redacted"
            )
        print(message.status)


# headlines = {title for title in news_data["articles"]["title"] if "Tesla" in title}
# print(headlines)

