"""




"""
from datetime import datetime, date
from fastapi import APIRouter, Query
from typing import Optional
from app.services.weather_services import get_weather_daily, get_weather_historic

router = APIRouter()

@router.get("/history")
def history(
        start_date: Optional[datetime] = Query(None),
        end_date: Optional[datetime] = Query(None)
):
    return get_weather_historic(start_date, end_date)


@router.get("/daily")
def daily(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None)
):
    return get_weather_daily(start_date, end_date)