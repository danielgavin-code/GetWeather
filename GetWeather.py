#!/usr/bin/python

#           
#     Title    : daily_Weather.py 
#     Version  : 1.0
#     Date     : 19 May 2025
#     Author   : Daniel Gavin
#
#     Function : Weather module for Daily Briefing. 
#              : - Connect to OpenWeatherMap.org via API
#              : - Download  daily weather summary.
#              : - Determine if you should pack an umbrella.
#              : - Display output.
#
#     Modification History
#
#     Date     : 19 May 2025
#     Author   : Daniel Gavin
#     Changes  : New file.
# 
#     Date     : 19 May 2025
#     Author   : Daniel Gavin
#     Changes  : Added the following to the output ... 
#              : - Current Temp 
#
#     Date     : 19 May 2025
#     Author   : Daniel Gavin
#     Changes  : Cleaned up output formatting.
#
#     Date     : 20 May 2025
#     Author   : Daniel Gavin
#     Changes  : Added support for default variables in env file.
#              : - zip, city, state
#
#     Date     : 21 May 2025
#     Author   : Daniel Gavin
#     Changes  : Added support for units ...
#              : - Imperial
#              : - Standard
#              : - Metric
#
#     Date     : 21 May 2025
#     Author   : Daniel Gavin
#     Changes  : Cleaned formatting.
#
#     Date     : 
#     Author   : 
#     Changes  : 
# 

import os
import argparse
import requests

from dotenv   import load_dotenv
from datetime import datetime

VERSION = '1.05'

load_dotenv(dotenv_path="GetWeather.env")

API_KEY       = os.getenv("WEATHER_API_KEY") 
DEFAULT_ZIP   = os.getenv("DEFAULT_ZIP")
DEFAULT_CITY  = os.getenv("DEFAULT_CITY")
DEFAULT_STATE = os.getenv("DEFAULT_STATE")

#############################################################################
#
# Procedure   : GetWeather()
#
# Description : Fetch weather from OpenWeather API
#             : Uses Geo API to get lat/lon from ZIP or city/state.
#             : Fetches full forecast using One Call API 3.0.
#
# Input       : zipCode - string ZIP code (optional)
#             : city    - string city name (optional)
#             : state   - string state code (optional)
#
# Returns     : dictionary - JSON response from OpenWeather API
#
###############################################################################

def GetWeather(zipCode=None, city=None, state=None, units="Imperial"):

    #
    # Get latitude and longitude from OpenWeather geo API
    #

    if zipCode:
        geoUrl = f"http://api.openweathermap.org/geo/1.0/zip?zip={zipCode},US&appid={API_KEY}"

    elif city and state:
        geoQuery = f"{city},{state},US"
        geoUrl   = f"http://api.openweathermap.org/geo/1.0/direct?q={geoQuery}&limit=1&appid={API_KEY}"

    else:
        print("[ERROR] No location provided. Use --zip or --city and --state.")
        return None

    geoResponse = requests.get(geoUrl)

    if geoResponse.status_code != 200:
        print("[ERROR] Unable to fetch geolocation data")
        return None

    geoData = geoResponse.json()

    if not geoData:
        print("[ERROR] No geolocation data found")
        return None

    # direct city lookup returns a list
    # zip lookup returns an object

    if isinstance(geoData, list):
        lat = geoData[0]["lat"]
        lon = geoData[0]["lon"]

    else:
        lat = geoData["lat"]
        lon = geoData["lon"]

    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,alerts&appid={API_KEY}&units={units}"
    response = requests.get(url)

    if response.status_code != 200:
        print("[ERROR] Unable to fetch weather data")
        return None

    today = datetime.today().strftime("%Y%m%d")

    return response.json()


#############################################################################
#     
# Procedure   : PackUmbrella()
#     
# Description : Read in weather data and determine if we need an umbrella. 
#     
# Input       : weatherData - JSON weather data from OpenWeatherMap
#             : day         - integer index of forecast day (0 = today)
#
# Returns     : string - 'Yes (45%)' or 'No (12%)' etc.
#
###############################################################################

def PackUmbrella(weatherData, day=0):

    retVal = ""

    try:
        weather         = weatherData["daily"][day]["weather"][0]["main"].lower()
        rainProbability = weatherData["daily"][day]["pop"]
        rainPercent     = int(rainProbability * 100)

        if "rain" in weather or rainProbability > 0.3:
            retVal = f"Yes ({rainPercent}%)"

        else:
            retVal = f"No ({rainPercent}%)"

    except Exception as e:
        print(f"[ERROR] Unable to determine umbrella status: {e}")
        retVal = "Unknown"

    return retVal


#############################################################################
#
# Procedure   : ParseArgs()
#
# Description : Parses command-line arguments using argparse.
#
# Input       : -none-
#
# Returns     : namespace - parsed command-line arguments
#
###############################################################################

def ParseArgs():

    parser = argparse.ArgumentParser(
        description="GetWeather: command line tool to fetch weather"
    )

    parser.add_argument("--zip",      type=str,                     help="ZIP code (e.g. 11211)")
    parser.add_argument("--city",     type=str,                     help="City name (weather app format)")
    parser.add_argument("--state",    type=str,                     help="State code (if using --city)")
    parser.add_argument("--days",     type=int, default=1,          help="Forecast days (1–10)")
    parser.add_argument("--units",    type=str, default="Imperial", help="Imperial, Standard, or Metric")
    parser.add_argument("--version",  action="store_true",          help="Display version and exit")

    return parser.parse_args()


############################################################################
#
# Procedure   : Main
#
# Description : Entry point.
#
# Input       : -none-
#
# Returns     : -none-
#
###############################################################################

def Main():

    units       = ""
    weatherData = ""

    args = ParseArgs()

    if args.version:
        print("Version: " + VERSION)
        return

    print("")
    print("🌤️   Fetching weather for your daily briefing ...\n")

    if args.units:

        units = args.units

        if not units:

            units = os.getenv("DEFAULT_UNITS")

    #
    # fetch weather based on arguments
    #

    if args.zip:
        zipCode = args.zip
        weatherData = GetWeather(zipCode=zipCode, units=units)

    elif args.city and args.state:
        city        = args.city
        state       = args.state
        weatherData = GetWeather(city=city, state=state, units=units)

    elif DEFAULT_ZIP:
        weatherData = GetWeather(zipCode=DEFAULT_ZIP, units=units)

    elif DEFAULT_CITY and DEFAULT_STATE:
        weatherData = GetWeather(city=DEFAULT_CITY, state=DEFAULT_STATE, units=units)

    else:
        print("[ERROR] You must provide either --zip or --city with --state.")
        return

    #
    # print current temperature immediately after banner
    #

    if weatherData:

        unitIndicator = ""
        currentTemp   = weatherData["current"]["temp"]

        if units.lower() == 'metric':

            unitIndicator = "°C"
            print(f"🌡️   Current Temp:\t{currentTemp}" + unitIndicator + "\n")

        elif units.lower() == 'imperial':

            unitIndicator = "°F"
            print(f"🌡️   Current Temp:\t{currentTemp}" + unitIndicator + "\n")

        else:
            print(f"🌡️   Current Temp:\t{currentTemp}\n")

        #
        # print forecast for number of days requested
        #

        numDays = args.days
        maxDaysAvailable = len(weatherData.get("daily", []))

        if numDays > maxDaysAvailable:
            print(f"[WARNING] Only {maxDaysAvailable} days of forecast available. Showing {maxDaysAvailable}-day forecast.\n")
            numDays = maxDaysAvailable 

        for i in range(numDays):

            dayData       = weatherData["daily"][i]
            tempHigh      = dayData["temp"]["max"]
            tempLow       = dayData["temp"]["min"]
            feelsLike     = weatherData["current"]["feels_like"] if i == 0 else dayData["feels_like"]["day"]
            umbrella      = PackUmbrella(weatherData, day=i)

            # format date as "May 19"
            forecastDate  = datetime.fromtimestamp(dayData["dt"]).strftime("%b %d")

            if i == 0:
                label = f"Today ({forecastDate})"
            elif i == 1:
                label = f"Tomorrow ({forecastDate})"
            else:
                label = f"{datetime.fromtimestamp(dayData['dt']).strftime('%A')} ({forecastDate})"

            print(f"📅  {label}")
            print("🌡️   High Temp:\t\t"  + str(tempHigh)  + unitIndicator)
            print("❄️   Low Temp:\t\t"    + str(tempLow)   + unitIndicator)
            print("💨  Feels Like:\t\t"  + str(feelsLike) + unitIndicator)
            print("☂️   Pack Umbrella:\t" + umbrella)
            print("")


if __name__ == "__main__":
    Main()

