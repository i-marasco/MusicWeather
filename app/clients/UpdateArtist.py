# Application name	TestApp
# API key	a7955ad0f8a0d65577e476fc67694039
# Shared secret	8bbbba69bd915ca3d07e841a0154bb3d
# Username LevTakeshy

import requests
import psycopg2

# Information to access last.fm API
API_KEY = "a7955ad0f8a0d65577e476fc67694039"
USER = "LevTakeshy"

url = "https://ws.audioscrobbler.com/2.0/"

# DB connection
conn = psycopg2.connect(
    dbname="music",
    user="postgres",
    password="admin",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

cur.execute("""
                SELECT
                    "ARTIST_NAME",
                    COUNT(*) AS plays,
                    MIN("LISTENED_AT") AS first_listened_at
                FROM "MUSIC_TRACK"."LISTENING_HISTORY"
                GROUP BY "ARTIST_NAME"
                ORDER BY plays DESC;
""")

conn.commit()
print(f"Artist updated")