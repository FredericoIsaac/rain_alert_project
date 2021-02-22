import requests
import os
from twilio.rest import Client
from datetime import datetime


API_KEY = os.environ.get("OWN_API_KEY")
OWN_Endpoint = "http://api.openweathermap.org/data/2.5/onecall"
MY_LAT = 38.776168
MY_LON = -9.108620
ACCOUNT_SID = os.environ.get("OWN_ACCOUNT_SID")
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
PHONE_NUMBER_TWILLIO = os.environ.get("OWN_PHONE_NUMBER_TWILLIO")
PHONE_NUMBER = os.environ.get("OWN_PHONE_NUMBER")

parameters = {
    "lat": MY_LAT,
    "lon": MY_LON,
    "units": "metric",
    "appid": API_KEY,
    "exclude": "minutely,daily"
}

response = requests.get(url=OWN_Endpoint, params=parameters)
response.raise_for_status()
weather_data = response.json()


def sunrise_sunset(current_data) -> tuple:
    sunset = datetime.fromtimestamp(int(current_data["current"]["sunset"]))
    sunrise = datetime.fromtimestamp(int(current_data["current"]["sunrise"]))
    return sunrise, sunset


def will_rain(weather):
    weather_12_hours = weather["hourly"][:12]

    for hourly_weather in weather_12_hours:
        weather_id = hourly_weather["weather"][0]["id"]
        if int(weather_id) < 700:
            return True

    return False


schedule_sun = sunrise_sunset(weather_data)

if will_rain(weather_data):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages\
        .create(body=f"It's Going to rain today. Remember to bring an ☂\n"
                     f"Sunrise: {schedule_sun[0]}\n"
                     f"Sunset: {schedule_sun[1]}",
                from_=PHONE_NUMBER_TWILLIO,
                to=PHONE_NUMBER
                )
    print(message.status)

