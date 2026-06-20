from datetime import datetime, timedelta, timezone
import requests
import os
from app.db.conn import get_connection
from dotenv import load_dotenv

load_dotenv()

OPENMETEO_LAT = os.getenv("OPENMETEO_LAT")
OPENMETEO_LON = os.getenv("OPENMETEO_LON")
OPENMETEO_URL = os.getenv("OPENMETEO_URL")



def get_last_sync(cur):
    cur.execute("""
        SELECT "LAST_SYNC"
        FROM "WEATHER"."WEATHER_SYNC_STATE"
        WHERE "ID" = 'OPENMETEO_MILAN'
    """)
    return cur.fetchone()[0]

def get_last_observed_at(cur):
    cur.execute("""
        SELECT MAX("OBSERVED_AT")
        FROM "WEATHER"."WEATHER_HISTORY"
    """)
    return cur.fetchone()[0]


def get_weather_history(start_date, end_date):
    params = {
        "latitude": OPENMETEO_LAT,
        "longitude": OPENMETEO_LON,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "pressure_msl",
            "wind_speed_10m",
            "weather_code"
        ],
        "timezone": "auto"
    }

    r = requests.get(OPENMETEO_URL, params=params)
    r.raise_for_status()
    return r.json()


def sync_weather():
    conn = get_connection()

    try:
        with conn.cursor() as cur:

            last = get_last_observed_at(cur)

            if last is None:
                start_date = datetime.now(timezone.utc) - timedelta(days=365)
            else:
                start_date = last - timedelta(days=1)

            end_date = datetime.now(timezone.utc)

            data = get_weather_history(start_date, end_date)
            hourly = data["hourly"]
            times = hourly["time"]

            for i in range(len(times)):

                cur.execute("""
                    INSERT INTO "WEATHER"."WEATHER_HISTORY" (
                        "OBSERVED_AT",
                        "CITY",
                        "LAT",
                        "LON",
                        "TEMPERATURE",
                        "HUMIDITY",
                        "PRESSURE",
                        "WIND_SPEED",
                        "WEATHER_CODE"
                    )
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    ON CONFLICT ("OBSERVED_AT", "LAT", "LON")
                    DO UPDATE SET
                        "TEMPERATURE" = EXCLUDED."TEMPERATURE",
                        "HUMIDITY" = EXCLUDED."HUMIDITY",
                        "PRESSURE" = EXCLUDED."PRESSURE",
                        "WIND_SPEED" = EXCLUDED."WIND_SPEED",
                        "WEATHER_CODE" = EXCLUDED."WEATHER_CODE";
                """, (
                    datetime.fromisoformat(times[i]),
                    "Milan",
                    float(OPENMETEO_LAT),
                    float(OPENMETEO_LON),
                    hourly["temperature_2m"][i],
                    hourly["relative_humidity_2m"][i],
                    hourly["pressure_msl"][i],
                    hourly["wind_speed_10m"][i],
                    hourly["weather_code"][i]
                ))

            # UPDATE SYNC STATE BEFORE COMMIT
            update_sync_state(cur, datetime.now(timezone.utc))

            conn.commit()

    finally:
        conn.close()

    print(f"Sync weather from {start_date} to {end_date}")


def update_sync_state(cur, timestamp):
    cur.execute("""
        INSERT INTO "WEATHER"."WEATHER_SYNC_STATE" ("ID", "LAST_SYNC")
        VALUES ('OPENMETEO_MILAN', %s)
        ON CONFLICT ("ID")
        DO UPDATE SET "LAST_SYNC" = EXCLUDED."LAST_SYNC";
    """, (timestamp,))
