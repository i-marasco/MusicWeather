from fastapi import APIRouter, Query
from datetime import datetime
from app.services.genre_service import get_top_genres
from app.services.genre_service import get_genres_by_period

router = APIRouter()


@router.get("/top")
def top_genres(
    start_date: datetime = Query(None),
    end_date: datetime = Query(None)
):
    return get_top_genres(start_date, end_date)

@router.get("/period")
def genres_by_period(
    start_date: datetime | None = None,
    end_date: datetime | None = None
):
    return get_genres_by_period(start_date, end_date)