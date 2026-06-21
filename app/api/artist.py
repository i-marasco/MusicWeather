"""
-------------------------------------------------------------------------------------------------
artist.py
-------------------------------------------------------------------------------------------------
Purpose:
        Output all the artist listened.

Source:
        "MUSIC_TRACK"."ARTISTS"

Inputs:
        None

Output:
        /artist:
        Artist name and first time listened.
"""

from fastapi import APIRouter
from app.services. artist_services import get_artist

router = APIRouter()

@router.get("/artist")
def artist(
):
    return get_artist()


