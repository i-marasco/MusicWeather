from fastapi import APIRouter, Query
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor

router = APIRouter()


def get_connection():
    return psycopg2.connect(
        dbname="music",
        user="postgres",
        password="admin",
        host="localhost",
        port="5432"
    )


@router.get("/history")
def get_history(
    start_date: datetime = Query(...),
    end_date: datetime = Query(...)
):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT "SONG_NAME", "ARTIST_NAME", "LISTENED_AT"
                FROM "MUSIC_TRACK"."LISTENING_HISTORY"
                WHERE "LISTENED_AT" BETWEEN %s AND %s
                ORDER BY "LISTENED_AT" ASC
            """, (start_date, end_date))

            rows = cur.fetchall()

    finally:
        conn.close()

    tracks = [
        {
            "track": r[0],
            "artist": r[1],
            "listened_at": r[2].isoformat()
        }
        for r in rows
    ]

    return {
        "total_plays": len(tracks),
        "tracks": tracks
    }

@router.get("/period")
def get_period(
    start_date: datetime = Query(...),
    end_date: datetime = Query(...)
):
    conn = get_connection()

    query = """
        SELECT
          CASE
            WHEN EXTRACT(HOUR FROM "LISTENED_AT") >= 6 AND EXTRACT(HOUR FROM "LISTENED_AT") < 12 THEN 'M'
            WHEN EXTRACT(HOUR FROM "LISTENED_AT") >= 12 AND EXTRACT(HOUR FROM "LISTENED_AT") < 18 THEN 'A'
            WHEN EXTRACT(HOUR FROM "LISTENED_AT") >= 18 AND EXTRACT(HOUR FROM "LISTENED_AT") < 21 THEN 'E'
            ELSE 'N'
          END AS period,
          COUNT(*) AS plays
        FROM "MUSIC_TRACK"."LISTENING_HISTORY"
        WHERE "LISTENED_AT" BETWEEN %s AND %s
        GROUP BY period
        ORDER BY period;
    """

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (start_date, end_date))
            results = cur.fetchall()

    finally:
        conn.close()

    return {
        "start_date": start_date,
        "end_date": end_date,
        "data": results
    }