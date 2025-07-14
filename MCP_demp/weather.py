from mcp.server.fastmcp import FastMCP
import pandas as pd 
import openmeteo_requests
import requests_cache
from retry_requests import retry
from langchain.tools import tool
from datetime import date 

mcp=FastMCP('Weather')

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

@mcp.tool()
def get_weather(lat,long,today,tomorrow):
    """ 
    from the location get the latitude and longitude 
    """
    # today=date.today().strftime("%Y-%m-%d")
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": long,
        "hourly": ["temperature_2m", "relative_humidity_2m", "dew_point_2m", "precipitation", "rain", "weather_code", "wind_speed_10m", "wind_speed_100m", "wind_gusts_10m", "cloud_cover"],
        "timezone": "GMT",
        "temperature_unit": "fahrenheit",
        "wind_speed_unit": "mph",
        "timeformat": "unixtime"
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation {response.Elevation()} m asl")
    print(f"Timezone {response.Timezone()}{response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
    hourly_dew_point_2m = hourly.Variables(2).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(3).ValuesAsNumpy()
    hourly_rain = hourly.Variables(4).ValuesAsNumpy()
    hourly_weather_code = hourly.Variables(5).ValuesAsNumpy()
    hourly_wind_speed_10m = hourly.Variables(6).ValuesAsNumpy()
    hourly_wind_speed_100m = hourly.Variables(7).ValuesAsNumpy()
    hourly_wind_gusts_10m = hourly.Variables(8).ValuesAsNumpy()
    hourly_cloud_cover = hourly.Variables(9).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start = pd.to_datetime(hourly.Time(), unit = "s", utc = True).tz_convert("America/Chicago"),
        end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True).tz_convert("America/Chicago"),
        freq = pd.Timedelta(seconds = hourly.Interval()),
        inclusive = "left"
    )}

    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
    hourly_data["dew_point_2m"] = hourly_dew_point_2m
    hourly_data["precipitation"] = hourly_precipitation
    hourly_data["rain"] = hourly_rain
    hourly_data["weather_code"] = hourly_weather_code
    hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
    hourly_data["wind_speed_100m"] = hourly_wind_speed_100m
    hourly_data["wind_gusts_10m"] = hourly_wind_gusts_10m
    hourly_data["cloud_cover"] = hourly_cloud_cover
    
    hourly_dataframe = pd.DataFrame(data = hourly_data)
    hourly_dataframe["day"] = hourly_dataframe["date"].dt.day
    hourly_dataframe["hour"] = hourly_dataframe["date"].dt.hour
    hourly_dataframe["year"] = hourly_dataframe['date'].dt.year
    hourly_dataframe['month']=hourly_dataframe['date'].dt.month
    hourly_dataframe['date_UTC']=pd.to_datetime(hourly_dataframe['date'], utc=True)
    # return hourly_dataframe

    # Return a string summary
    sample = hourly_dataframe.head(5).to_string(index=False)
    return f"Here’s a snapshot of upcoming weather:\n{sample}"

if __name__=="__main__":
    mcp.run(transport='stdio')
