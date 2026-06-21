"""
-------------------------------------------------------------------------------------------------
listening.py
-------------------------------------------------------------------------------------------------
Purpose:
        Output the song listened in a period or historic.

Source:
        "MUSIC_TRACK"."LISTENING_HISTORY"

Inputs:
        start_date[optional]:  start date of the selection period.
        end_date[optional]: end date of the selection period.

Output:
        /history:
            Return the song listened in a period or historic.
        /period:
            Return the period of listening M: Morning, A: Afternoon, E: Evening, N: Night.
"""

from fastapi import APIRouter, Query
from datetime import datetime
from app.services.listening_services import get_listening_history, get_listening_period

router = APIRouter()

@router.get("/history")
def get_history(
    start_date: datetime = Query(None),
    end_date: datetime = Query(None)
):
    return get_listening_history(start_date, end_date)


@router.get("/period")
def get_period(
    start_date: datetime = Query(None),
    end_date: datetime = Query(None)
):
    return get_listening_period(start_date, end_date)
