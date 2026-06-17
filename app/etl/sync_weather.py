"""
-------------------------------------------------------------------------------------------------
sync_weather.py
-------------------------------------------------------------------------------------------------
Purpose:

Source:

Input:

Output:

Note:

"""
from datetime import datetime
import requests
import os
from app.db.conn import get_connection
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
OPENWEATHER_LAT = os.getenv("OPENWEATHER_LAT")
OPENWEATHER_LON = os.getenv("OPENWEATHER_LON")

OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"


def sync_weather():

    params = {
        "lat": OPENWEATHER_LAT,
        "lon": OPENWEATHER_LON,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }

    r = requests.get(OPENWEATHER_URL, params=params)
    data = r.json()
    print(data)

    conn = get_connection()

    try:
        with conn.cursor() as cur:

            cur.execute("""
                INSERT INTO "WEATHER"."WEATHER_HISTORY" (
                    "OBSERVED_AT",
                    "CITY",
                    "LAT",
                    "LON",
                    "TEMPERATURE",
                    "FEELS_LIKE",
                    "HUMIDITY",
                    "PRESSURE",
                    "WEATHER_MAIN",
                    "WEATHER_DESCRIPTION",
                    "WIND_SPEED",
                    "CLOUDINESS",
                    "SUNRISE",
                    "SUNSET"
                )
                VALUES (
                    %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s,
                    %s, %s,
                    %s, %s
                );
            """, (
                datetime.now(),
                data.get("name"),
                data["coord"]["lat"],
                data["coord"]["lon"],
                data["main"]["temp"],
                data["main"]["feels_like"],
                data["main"]["humidity"],
                data["main"]["pressure"],
                data["weather"][0]["main"],
                data["weather"][0]["description"],
                data["wind"]["speed"],
                data["clouds"]["all"],
                datetime.fromtimestamp(data["sys"]["sunrise"]),
                datetime.fromtimestamp(data["sys"]["sunset"])
            ))

            conn.commit()

    finally:
        conn.close()


sync_weather()