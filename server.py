from fastapi import FastAPI, HTTPException
import requests
import os
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

if not OPENWEATHER_API_KEY:
    raise RuntimeError("OPENWEATHER_API_KEY not found in .env")

app = FastAPI(title="MCP Weather Server")

# ---------------------------------
# Helper: Get Lat/Lon safely
# ---------------------------------
def get_lat_lon(city: str):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY
    }

    res = requests.get(url, params=params)
    data = res.json()

    if res.status_code != 200 or "coord" not in data:
        raise HTTPException(status_code=404, detail="City not found")

    return data["coord"]["lat"], data["coord"]["lon"]

# ---------------------------------
# Current Weather
# ---------------------------------
@app.get("/weather")
def get_current_weather(city: str):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }

    res = requests.get(url, params=params)
    data = res.json()

    if res.status_code != 200:
        raise HTTPException(status_code=404, detail=data.get("message", "Error"))

    return {
        "city": city,
        "temperature": data["main"]["temp"],
        "condition": data["weather"][0]["description"]
    }

# ---------------------------------
# 7-Day Forecast (SAFE)
# ---------------------------------
@app.get("/forecast")
def get_7_day_forecast(city: str):
    lat, lon = get_lat_lon(city)

    url = "https://api.openweathermap.org/data/2.5/onecall"
    params = {
        "lat": lat,
        "lon": lon,
        "exclude": "minutely,hourly,alerts",
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }

    res = requests.get(url, params=params)
    data = res.json()

    # 🔥 CRITICAL SAFETY CHECK
    if res.status_code != 200 or "daily" not in data:
        raise HTTPException(
            status_code=500,
            detail=data.get("message", "7-day forecast not available for this API key")
        )

    forecast = []
    for day in data["daily"][:7]:
        forecast.append({
            "day_temperature": day["temp"]["day"],
            "condition": day["weather"][0]["description"]
        })

    return {
        "city": city,
        "forecast": forecast
    }
