"""Routes for serving the frontend."""
import os
from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/")
@router.head("/")
@router.get("/timeline.html")
@router.head("/timeline.html")
def index():
    """Serve the timeline HTML."""
    # Since main.py runs from root, we look for front_end/timeline.html
    return FileResponse(os.path.join("front_end", "timeline.html"))


@router.get("/timelinev2.html")
@router.head("/timelinev2.html")
def timeline_legacy():
    """Old bookmarked address — serves a page that redirects to timeline.html."""
    return FileResponse(os.path.join("front_end", "timelinev2.html"))


@router.get("/main_menu.html")
@router.head("/main_menu.html")
def main_menu():
    """Serve the main menu HTML."""
    return FileResponse(os.path.join("front_end", "main_menu.html"))

@router.get("/api.js")
def api_js():
    """Serve the API JS file."""
    return FileResponse(os.path.join("front_end", "api.js"))


@router.get("/spell_data.json")
def spell_data():
    """Serve the spell_data.json file."""
    return FileResponse("spell_data.json")
