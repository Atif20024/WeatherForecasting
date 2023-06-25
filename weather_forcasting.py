# I want to Create a command-line tool that accepts a city's name and returns the current weather forecast.
# Leverage OpenWeatherMap API to fetch weather data and parse it using Python.
# The solution should demonstrate how GitHub Copilot can help you with API usage, data parsing, and error handling.

# how do i start?
import requests
import json
import argparse
from datetime import datetime

# type of input to accept
# we need to give option to give input in any order, using some library we can decide if the agument is city or country
# also we ca give option to give input as a string and we do NER to decide what information is present in the string.
# it can be any date, time, city, country, etc.
import os
os.environ["OpenWeatherAPIkey"] = "6fb77227d78ecc1a79afb55a2d91f825"

parser = argparse.ArgumentParser(description='Get weather forecast for a city')
parser.add_argument('city', type=str, help='City name')
args = parser.parse_args()

api_key  = os.environ.get('OpenWeatherAPIkey')
# get weather data from openweathermap.org api using lat long

# i want to convert city name to lat long using openweathermap.org api
def city_to_lat_long(city):
    # error handling for unavailable city
    if not city:
        return None
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['coord']
    else:
        return None


def get_weather_data(city):
    # error handling for unavailable city
    if not city:
        return None
    url = f'http://api.openweathermap.org/data/2.5/weather?lat={city["lat"]}&lon={city["lon"]}&appid={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


# parse weather data
def parse_weather_data(data):
    if data:
        return {
            'city': data['name'],
            'country': data['sys']['country'],
            'temp': data['main']['temp'],
            'temp_min': data['main']['temp_min'],
            'temp_max': data['main']['temp_max'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'wind_speed': data['wind']['speed'],
            'wind_deg': data['wind']['deg'],
            'weather': data['weather'][0]['main'],
            'weather_desc': data['weather'][0]['description'],
            'clouds': data['clouds']['all'],
            'timezone': data['timezone'],
            'visibility': data['visibility'],
            'dt': data['dt']
        }
    else:
        return None


def modify_weather_data(data):
    # convert temperature from kelvin to celsius round off to 1 decimal place

    data['temp'] = round(data['temp'] - 273.15,1)
    # convert max temperature from kelvin to celcius round off to 1 decimal place
    
    data['temp_max'] = round(data['temp_max'] - 273.15,1)
    # convert min temperature from kelvin to celcius
    data['temp_min'] = round(data['temp_min'] - 273.15,1)
    # convert wind speed from m/s to km/h
    data['wind_speed'] = data['wind_speed'] * 3.6
    # convert visibility from m to km
    data['visibility'] = data['visibility'] / 1000
    # convert date time from unix timestamp to date time format. only want date not time
    data['dt'] = datetime.fromtimestamp(data['dt']).strftime('%Y-%m-%d')
    # extract humidity and pressure, Weather description, feels like, city, country 
    data = {key: data[key] for key in data.keys() & {'feels like', 'Weather Description', 'humidity', 'pressure', 'city', 'country', 'temp', 'temp_min', 'temp_max', 'wind_speed', 'wind_deg', 'weather', 'weather_desc', 'clouds', 'timezone', 'visibility', 'dt'}}

    return data

# convert the data to news presenter format
def create_summary(data):
    summary = f'Weather in {data["city"]}, {data["country"]} on {data["dt"]}: Weather condition is {data["weather_desc"]}. The temperature is {data["temp"]}°C. The maximum temperature is {data["temp_max"]}°C and the minimum temperature is {data["temp_min"]}°C. The humidity is {data["humidity"]}% and the pressure is {data["pressure"]} hPa. The wind speed is {data["wind_speed"]} km/h and the wind degree is {data["wind_deg"]}°. The cloudiness is {data["clouds"]}% and the visibility is {data["visibility"]} km.'
    return summary


# main function

def main():
    # describe the steps
    # 1. get city name from user
    # 2. convert city name to lat long
    # 3. get weather data from openweathermap.org api using lat long
    # 4. parse weather data
    # 5. print weather data
    
    city = args.city
    cityto_lat_long = city_to_lat_long(city)
    data = get_weather_data(cityto_lat_long)
    data = parse_weather_data(data)
    data = modify_weather_data(data)
    summary = create_summary(data)
    print(summary)

# run main function
if __name__ == '__main__':
    main()


