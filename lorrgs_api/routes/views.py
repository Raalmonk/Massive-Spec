"""Routes for serving the frontend."""
import os
from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/")
def index():
    """Serve the Timeline V2 HTML."""
    # Since main.py runs from root, we look for front_end/timelinev2.html
    return FileResponse(os.path.join("front_end", "timelinev2.html"))

@router.get("/api.js")
def api_js():
    """Serve the API JS file."""
    return FileResponse(os.path.join("front_end", "api.js"))


@router.get("/spell_data.json")
def spell_data():
    """Serve the spell_data.json file."""
    return FileResponse("spell_data.json")
