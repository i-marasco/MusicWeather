"""




"""
from app.db.conn import get_connection


def get_weather_historic(start_date=None, end_date=None):
    conn = get_connection()
    try:
        with conn.cursor() as cur:

            query = """
                    SELECT
                        "OBSERVED_AT",
                        "CITY",
                        "LAT",
                        "LON",
                        "TEMPERATURE",
                        "HUMIDITY",
                        "PRESSURE",
                        "WIND_SPEED",
                        "WEATHER_CODE"
                    FROM "WEATHER"."WEATHER_HISTORY"
                    WHERE 1=1
            """
            params = []

            if start_date:
                query += ' AND "OBSERVED_AT" >= %s'
                params.append(start_date)

            if  end_date:
                query += ' AND "OBSERVED_AT" <= %s'
                params.append(end_date)

            query += ' ORDER BY "OBSERVED_AT" DESC'

            cur.execute(query, params)

            columns = [column[0] for column in cur.description]

            return [
                dict(zip(columns, row))
                for row in cur.fetchall()
            ]

    finally:
        conn.close()


def get_weather_daily(start_date = None, end_date = None ):
    conn = get_connection()
    try:
        with conn.cursor() as cur:

            query = """
                SELECT
                    "DAY",
                    "CITY",
                    "LAT",
                    "LON",
                    "AVG_TEMPERATURE",
                    "MIN_TEMPERATURE",
                    "MAX_TEMPERATURE",
                    "AVG_HUMIDITY",
                    "AVG_PRESSURE",
                    "AVG_WIND_SPEED",
                    "MOST_COMMON_WEATHER_CODE"
                FROM "WEATHER"."WEATHER_DAILY_SUMMARY"
                WHERE 1=1
            """
            params = []

            if start_date:
                query += ' AND "DAY" >= %s'
                params.append(start_date)

            if end_date:
                query += ' AND "DAY" <= %s'
                params.append(end_date)

            query += ' ORDER BY "DAY" DESC'

            cur.execute(query, params)

            columns = [column[0] for column in cur.description]

            return [
                dict(zip(columns, row))
                for row in cur.fetchall()
            ]

    finally:
        conn.close()
